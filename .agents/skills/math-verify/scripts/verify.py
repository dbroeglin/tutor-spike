#!/usr/bin/env python3
"""Symbolic checks for tutoring claims.

Run with: uv run --with sympy verify.py <command> [args...]

Exit codes are deliberately three-valued:

    0  the claim holds
    1  the claim does not hold
    2  the check could not be performed

**2 is not 1.** A tool failure is not evidence that the student is wrong. Report it as
unverified rather than grading on it.
"""

from __future__ import annotations

import json
import sys

try:
    import sympy
    from sympy.parsing.sympy_parser import parse_expr
except ImportError:  # pragma: no cover - the tier-2 path
    print(json.dumps({
        "verified": None,
        "error": "sympy unavailable - label the claim UNVERIFIED",
    }))
    raise SystemExit(2)


def parse(text):
    return parse_expr(text, evaluate=False)


def emit(verified, **extra):
    payload = {"verified": verified}
    payload.update(extra)
    print(json.dumps(payload, indent=2, default=str))
    return 0 if verified else 1


def equivalent(a, b):
    """Structural equality is not mathematical equality.

    (1/2)*log(x**2) and log(x) have different trees and the same value. Compare the
    simplified difference, and fall back to numeric sampling when simplify gives up
    on something it cannot normalise.
    """
    diff = sympy.simplify(sympy.expand(a - b))
    if diff == 0:
        return True, "simplify(a - b) == 0"
    try:
        free = sorted(a.free_symbols | b.free_symbols, key=str)
        samples = [0.37, 1.13, 2.71, 4.2]
        for i in range(len(samples)):
            subs = {s: sympy.Rational(str(samples[(i + j) % len(samples)]))
                    for j, s in enumerate(free)}
            value = complex(diff.subs(subs).evalf())
            if abs(value) > 1e-9:
                return False, "numeric counterexample at %s" % {str(k): str(v)
                                                                for k, v in subs.items()}
        return True, "simplify inconclusive; numerically equal at all sample points"
    except (TypeError, ValueError, AttributeError):
        return False, "simplify(a - b) = %s" % diff


def cmd_equal(args):
    a, b = parse(args[0]), parse(args[1])
    ok, why = equivalent(a, b)
    return emit(ok, lhs=a, rhs=b, reason=why)


def cmd_simplify(args):
    expr = parse(args[0])
    return emit(True, expr=expr, simplified=sympy.simplify(expr))


def cmd_deriv(args):
    expr, var = parse(args[0]), sympy.Symbol(args[1])
    actual = sympy.diff(expr, var)
    if len(args) < 3:
        return emit(True, derivative=actual)
    ok, why = equivalent(actual, parse(args[2]))
    return emit(ok, correct=actual, claimed=parse(args[2]), reason=why)


def cmd_integral(args):
    expr, var = parse(args[0]), sympy.Symbol(args[1])
    actual = sympy.integrate(expr, var)
    if len(args) < 3:
        return emit(True, integral=actual, note="constant of integration omitted")
    claimed = parse(args[2])
    # Antiderivatives are equal only up to a constant, so differentiate both
    # instead of comparing them directly.
    ok, why = equivalent(sympy.diff(claimed, var), expr)
    return emit(ok, correct=actual, claimed=claimed,
                reason="compared by differentiating the claim: " + why)


def cmd_limit(args):
    expr, var = parse(args[0]), sympy.Symbol(args[1])
    point = sympy.oo if args[2] in ("oo", "inf") else parse(args[2])
    actual = sympy.limit(expr, var, point)
    if len(args) < 4:
        return emit(True, limit=actual)
    ok, why = equivalent(actual, parse(args[3]))
    return emit(ok, correct=actual, claimed=parse(args[3]), reason=why)


def cmd_ode(args):
    """Verify a claimed solution by substituting it into the equation."""
    x = sympy.Symbol("x")
    f = sympy.Function("f")
    equation = sympy.sympify(args[0], locals={"f": f, "x": x})
    candidate = parse(args[1])
    substituted = equation.subs(f(x), candidate).doit()

    # When both sides land on the same expression sympy collapses Eq to a
    # BooleanTrue/False, which has no .lhs -- that collapse IS the answer.
    if isinstance(substituted, sympy.logic.boolalg.BooleanAtom):
        return emit(bool(substituted), equation=equation, candidate=candidate,
                    residual=0 if substituted else "sides differ")

    residual = sympy.simplify(substituted.lhs - substituted.rhs)
    return emit(residual == 0, equation=equation, candidate=candidate, residual=residual)


def cmd_matrix(args):
    """eigenvalues of a matrix given as a nested python list."""
    matrix = sympy.Matrix(sympy.sympify(args[0]))
    # eigenvals() keys are sympy expressions; json needs string keys.
    eigenvalues = {str(value): multiplicity
                   for value, multiplicity in matrix.eigenvals().items()}
    return emit(True, matrix=matrix, eigenvalues=eigenvalues,
                det=matrix.det(), rank=matrix.rank())


COMMANDS = {
    "equal": (cmd_equal, 2, "<expr_a> <expr_b>"),
    "simplify": (cmd_simplify, 1, "<expr>"),
    "deriv": (cmd_deriv, 2, "<expr> <var> [claimed]"),
    "integral": (cmd_integral, 2, "<expr> <var> [claimed]"),
    "limit": (cmd_limit, 3, "<expr> <var> <point> [claimed]"),
    "ode": (cmd_ode, 2, "<Eq(f(x).diff(x), ...)> <candidate>"),
    "matrix": (cmd_matrix, 1, "<[[a,b],[c,d]]>"),
}


def main(argv):
    if len(argv) < 2 or argv[1] not in COMMANDS:
        print("usage: verify.py <command> [args]", file=sys.stderr)
        for name, (_, _, usage) in sorted(COMMANDS.items()):
            print("  %-9s %s" % (name, usage), file=sys.stderr)
        return 2

    handler, arity, usage = COMMANDS[argv[1]]
    args = argv[2:]
    if len(args) < arity:
        print("usage: verify.py %s %s" % (argv[1], usage), file=sys.stderr)
        return 2

    try:
        return handler(args)
    except Exception as exc:
        # Exit 2, never 1: the check failed, which says nothing about the claim.
        print(json.dumps({
            "verified": None,
            "error": "%s: %s" % (type(exc).__name__, exc),
            "note": "check failed - report as UNVERIFIED, do not grade on this",
        }, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

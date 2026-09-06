---
name: math-verify
description: Check a symbolic mathematical claim with sympy before asserting it — equality of expressions, derivatives, integrals, ODE solutions, limits, series, and matrix results. Use before telling a student that an answer is wrong, before presenting a counterexample, and before claiming two expressions are equivalent. Falls back to labelling claims UNVERIFIED when sympy is unavailable.
---

# Math verify

**A tutor that confidently mis-grades a correct answer is worse than no tutor.** It destroys the
trust the whole method depends on, and the student cannot tell which of your other assertions
are also wrong.

So: check before you assert.

## When to use it

Always, before:

- telling him an answer is wrong;
- claiming two expressions are or are not equivalent (his form may be algebraically equal to
  yours and look nothing like it);
- presenting a counterexample — a broken counterexample hands him a reason to keep his rule;
- asserting a derivative, integral, limit, series, eigenvalue or ODE solution.

Not needed for arithmetic you can do reliably in your head, or for questions about method
rather than result.

**The most important case is the false negative.** `2sin(x)cos(x)` and `sin(2x)`,
`(1/2)ln(x²)` and `ln|x|`, `c₁e^t + c₂e^{-t}` and `A cosh t + B sinh t` — all equal, all
look wrong at a glance. Structural comparison is not equivalence; use `simplify` on the
difference.

## Usage

```
uv run --with sympy .agents/skills/math-verify/scripts/verify.py equal "(x+3)**2" "x**2+9"
uv run --with sympy .agents/skills/math-verify/scripts/verify.py deriv "sin(3*x)" x "cos(3*x)"
uv run --with sympy .agents/skills/math-verify/scripts/verify.py integral "1/x" x "log(x)"
uv run --with sympy .agents/skills/math-verify/scripts/verify.py ode "Eq(f(x).diff(x), f(x))" "exp(x)"
uv run --with sympy .agents/skills/math-verify/scripts/verify.py limit "(x**2-1)/(x-1)" x 1
uv run --with sympy .agents/skills/math-verify/scripts/verify.py simplify "2*sin(x)*cos(x)"
```

Output is JSON with `verified: true|false`. Exit code 0 means the claim holds, 1 means it does
not, 2 means the check itself failed — and **2 is not 1**. A tool error is not evidence that the
student is wrong. Say so rather than guessing.

For anything the script does not cover, call sympy directly:

```
uv run --with sympy python -c "import sympy; ..."
```

Prefer `sympy.simplify(a - b) == 0` over `a == b`; the latter compares expression trees, not
values.

## Finding a counterexample

To *disprove* a student's rule, a numeric substitution is usually better than symbolic
manipulation: it is concrete, he can check it himself in ten seconds, and it cannot be argued
with.

```
uv run --with sympy python -c "
import sympy
a, b = sympy.symbols('a b')
lhs, rhs = (a+b)**2, a**2 + b**2
print(sympy.simplify(lhs - rhs))
print([(v, (lhs-rhs).subs({a: v[0], b: v[1]})) for v in [(1,1),(2,3)]])
"
```

Pick the *smallest* numbers that break the rule. `a = b = 1` is ideal — the arithmetic is
trivial, so he cannot retreat into computation, and the gap is undeniable.

## Tier degradation

| Tier | Behaviour |
|---|---|
| 3 | Verify everything as above. |
| 2 / 1 | sympy unavailable. **Label every symbolic claim `UNVERIFIED`** and say plainly that you could not check it. |

At tier ≤ 2, prefer method questions over grading, and let him do the verification: "substitute
`a = b = 1` and tell me what you get" is both a valid probe and a way of outsourcing the check
to arithmetic he can trust.

Never silently drop the label. The student needs to know which claims were machine-checked.

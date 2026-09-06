# Seeded misconception catalogue

The **hypothesis space**, not the student model. These are candidate bugs students in general
hold. What *this* student actually holds lives in the vault ledger
(`Learner Model/Misconceptions/`), written by `learner-model`.

Use this to generate candidates. When one is confirmed, the ledger entry records
`catalog_id: CAT-XXX-NN` so that recurrence can be traced back to a known pattern.

**Kept deliberately small.** 26 sharp entries beat 200 vague ones: every extra candidate makes
a splitting probe harder to design. Add an entry only when a bug is observed that none of these
explains — and when you do, file it by the same rule below.

**Filing rule.** An entry lives in the most primitive domain in which its rule is *statable*,
not where it is usually met. `det(A+B) = det A + det B` is a linear algebra manifestation of
`CAT-ALG-01`; it gets its own entry only because the surface structure needs its own probe.

---

## Algebra

`CAT-ALG-01` — **Linearity over-generalization**
: `f(a+b) = f(a) + f(b)` for any `f`. The most productive bug in mathematics.
: Surfaces as `(a+b)² = a² + b²`, `√(a²+b²) = a+b`, `ln(a+b) = ln a + ln b`,
  `1/(a+b) = 1/a + 1/b`, `sin(a+b) = sin a + sin b`.
: **Boundary:** additivity holds only for linear `f`.
: **Probe:** numeric substitution — `a = b = 1` breaks it instantly and undeniably.

`CAT-ALG-02` — **Cancellation of terms as if they were factors**
: `(a+b)/a = b`, `(x²+x)/x = x²`.
: **Boundary:** you may cancel a *factor* of the whole numerator, never a term.
: **Probe:** ask him to cancel in `(a·b)/a` and `(a+b)/a` back to back and justify the
  difference.

`CAT-ALG-03` — **Exponent rule conflation**
: `(a^m)^n = a^(m+n)` or `a^m · a^n = a^(mn)`.
: **Probe:** `2³ · 2² ` vs `(2³)²` computed numerically.

`CAT-ALG-04` — **Sign not distributed across a subtraction**
: `-(a - b) = -a - b`.
: **Probe:** evaluate at `a=1, b=1`; then ask where the second sign went.

`CAT-ALG-05` — **`√(x²) = x`**
: Absolute value dropped.
: **Boundary:** `√(x²) = |x|`; equals `x` only for `x ≥ 0`.
: **Probe:** `x = -3`.

`CAT-ALG-06` — **Zero-product property over-generalized**
: `ab = c ⟹ a = c or b = c`, applied when `c ≠ 0`.
: **Boundary:** the property is specifically about `0`.
: **Probe:** `(x-1)(x-2) = 6` solved by setting each factor to 6.

`CAT-ALG-07` — **Logarithm/exponential structure confusion**
: `ln(ab) = ln a · ln b`, `e^(a+b) = e^a + e^b`, `ln(a/b) = ln a / ln b`.
: **Probe:** ask him to state which operation the log *converts* into which.

`CAT-ALG-08` — **Equation and expression conflated**
: Adding a term "to both sides" of an expression; "solving" `x² + 3x`.
: **Boundary:** operations preserving equality require an equality to preserve.
: **Probe:** "simplify `x² + 3x`" immediately after "solve `x² + 3x = 0`".

---

## Calculus

`CAT-CAL-01` — **Chain rule truncation**
: `d/dx f(g(x)) = f'(g(x))`; inner derivative omitted.
: **Probe:** an inner function whose derivative is not 1 *and* an outer function that is the
  identity, to separate this from "inner derivative is always 1".

`CAT-CAL-02` — **Product rule as product of derivatives**
: `(fg)' = f'g'`.
: **Probe:** `f = g = x`, where the wrong rule gives `1` and the right one `2x`.

`CAT-CAL-03` — **Quotient rule order inversion**
: Numerator written `f g' - f' g`.
: **Probe:** `d/dx (x/1)` and `d/dx (1/x)`; sign error shows immediately.

`CAT-CAL-04` — **Power rule applied to a variable exponent**
: `d/dx a^x = x·a^(x-1)`, or `d/dx x^x` by either single rule.
: **Boundary:** the power rule needs a constant exponent; exponentials need `ln a`.
: **Probe:** `d/dx 2^x` at `x = 0`, checked numerically.

`CAT-CAL-05` — **Reverse power rule over-applied to `1/x`**
: `∫ x⁻¹ dx = x⁰/0`.
: **Boundary:** `n = -1` is the excluded case.
: **Probe:** ask what the formula does at `n = -1` before giving the answer.

`CAT-CAL-06` — **Constant of integration treated as decorative**
: Dropped, or added once at the end of a multi-step problem.
: **Probe:** an initial-value problem where the constant carries the entire answer.

`CAT-CAL-07` — **Definite integral is area**
: Sign ignored; `∫` of a negative region reported as positive.
: **Boundary:** it is *signed* area.
: **Probe:** `∫₀^{2π} sin x dx`.

`CAT-CAL-08` — **Substitution without transforming everything**
: `dx` not converted, or limits left in the original variable.
: **Probe:** a definite integral where untransformed limits give a plausible-looking wrong
  number.

`CAT-CAL-09` — **Limit equals function value**
: Continuity assumed everywhere; removable discontinuities invisible.
: **Probe:** `lim_{x→1} (x²-1)/(x-1)` and then "what is the function's value at 1?"

`CAT-CAL-10` — **Terms → 0 implies the series converges**
: The divergence test read backwards.
: **Boundary:** `aₙ → 0` is necessary, not sufficient.
: **Probe:** the harmonic series.

`CAT-CAL-11` — **Partial derivative treated as total derivative**
: Other variables' dependence on the differentiation variable ignored.
: **Probe:** `f(x, y(x))` where `y` visibly depends on `x`.

---

## Linear algebra

`CAT-LIN-01` — **Matrix multiplication assumed commutative**
: `AB = BA`, or factoring `(A+B)² = A² + 2AB + B²`.
: **Boundary:** only for commuting matrices.
: **Probe:** two explicit 2×2 matrices; let him compute both orders.

`CAT-LIN-02` — **Inverse/transpose of a product without reversing order**
: `(AB)⁻¹ = A⁻¹B⁻¹`, `(AB)ᵀ = AᵀBᵀ`.
: **Probe:** verify `(AB)(B⁻¹A⁻¹) = I` and let him try it his way.

`CAT-LIN-03` — **`det(A+B) = det A + det B`**
: `CAT-ALG-01` in matrix costume; needs its own probe because the surface structure is
  unfamiliar enough that transfer from algebra usually fails.
: **Probe:** `A = B = I` in 2×2 — `det` gives 4, not 2.

`CAT-LIN-04` — **Eigenvector treated as unique**
: One vector rather than a one-dimensional (or larger) eigenspace; normalisation confused with
  uniqueness.
: **Probe:** "is `2v` also an eigenvector? what is the full solution set?"

`CAT-LIN-05` — **Eigenvalues assumed additive or multiplicative across matrices**
: `λ(A+B) = λ(A) + λ(B)`.
: **Probe:** two matrices with known spectra whose sum has neither.

`CAT-LIN-06` — **Spanning set assumed to be a basis**
: Independence never checked; "these vectors span, so they're a basis".
: **Boundary:** basis = spanning **and** independent.
: **Probe:** three vectors spanning a plane in `ℝ³`.

`CAT-LIN-07` — **Subspace test skipped**
: A subset not containing `0`, or not closed under addition, called a subspace.
: **Probe:** the line `y = x + 1`.

---

## Differential equations

`CAT-ODE-01` — **Separation applied to a non-separable equation**
: Forcing `dy/dx = f(x,y)` into `g(y)dy = h(x)dx` when it does not factor.
: **Probe:** `y' = x + y` — ask him to show the factorisation explicitly.

`CAT-ODE-02` — **General solution missing the homogeneous part**
: Only the particular solution reported, or superposition applied to a *nonlinear* equation.
: **Boundary:** superposition is a property of linearity.
: **Probe:** verify that his solution family satisfies the initial condition for arbitrary
  data; it cannot.

`CAT-ODE-03` — **Repeated roots handled as distinct**
: `c₁e^{rt} + c₂e^{rt}` instead of `(c₁ + c₂t)e^{rt}`.
: **Probe:** ask how many independent solutions a second-order equation must have, then count
  his.

`CAT-ODE-04` — **Initial conditions applied too early**
: Constants fixed before the general solution is complete, losing solution branches.
: **Probe:** a problem where an early substitution silently discards a term.

`CAT-ODE-05` — **`dy/dx` manipulated as an unconditional fraction**
: Leibniz notation over-trusted; separation used to justify steps it does not license.
: **Boundary:** the fraction manipulation is shorthand for the chain rule and substitution.
: **Probe:** ask him to justify the step, not repeat it.

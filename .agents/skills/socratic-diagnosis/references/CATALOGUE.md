# Seeded misconception catalogue

The **hypothesis space**, not the student model. These are candidate bugs students in general
hold. What *this* student actually holds lives in the vault ledger
(`Learner Model/Misconceptions/`), written by `learner-model`.

Use this to generate candidates. When one is confirmed, the ledger entry records
`catalog_id: CAT-XXX-NN` so that recurrence can be traced back to a known pattern.

**Kept deliberately small.** 53 sharp entries beat 200 vague ones: every extra candidate makes
a splitting probe harder to design. Add an entry only when a bug is observed that none of these
explains — and when you do, file it by the same rule below.

**Filing rule.** An entry lives in the most primitive domain in which its rule is *statable*,
not where it is usually met. `det(A+B) = det A + det B` is a linear algebra manifestation of
`CAT-ALG-01`; it gets its own entry only because the surface structure needs its own probe.

---

## Logic and proof

Bugs at this level corrupt every domain downstream, and they hide easily: a student who
reaches a true conclusion by an invalid route looks correct. In proof-based courses this is the
highest-yield section in the catalogue — check it before blaming the subject matter.

`CAT-LOG-01` — **Converse taken for granted**
: `A ⟹ B` used as `B ⟹ A`. In an "if and only if" task, only the easy direction is proved and
  the proof is declared finished (French: *si et seulement si*).
: **Boundary:** the two directions are separate theorems; either can be true alone.
: **Probe:** ask which direction he has just proved, then ask for a counterexample to the
  other. "Every square is a rectangle" — is every rectangle a square?

`CAT-LOG-02` — **Quantifier order swapped**
: `∀x ∃y P(x,y)` treated as `∃y ∀x P(x,y)`. The witness is allowed to depend on `x` in one and
  not the other.
: **Probe:** "every integer has a larger integer" versus "there is an integer larger than every
  integer" — same words, one true.

`CAT-LOG-03` — **General claim established on an instance**
: One example, or one convenient special case, offered as proof of a universally quantified
  statement. Distinct from `CAT-LOG-01`: the logic form is right, the scope is not.
: **Boundary:** an example refutes a `∀` claim but never proves one; it *does* prove a `∃` claim.
: **Probe:** "you verified it for `n = 3`; what changes when `n` is arbitrary?"

`CAT-LOG-04` — **Conclusion used as a hypothesis**
: Circular proof. Typically the target equality is manipulated on both sides until `0 = 0`, and
  the chain is never reversed or justified as reversible.
: **Boundary:** working backwards is legitimate only when every step is an equivalence.
: **Probe:** "which line is your hypothesis and which is what you are proving?" then ask him to
  rewrite the argument forwards.

---

## Sets and maps

`CAT-SET-01` — **`f⁻¹(B)` read as requiring `f` to be invertible**
: The preimage notation is taken to presuppose a bijection, so the student refuses to write
  `f⁻¹(B)` for a non-injective `f` — or, worse, silently assumes injectivity to proceed
  (French: *image réciproque*).
: **Boundary:** `f⁻¹(B)` is defined for every map; `f⁻¹` as a *map* needs bijectivity.
: **Probe:** `f(x) = x²` on `ℝ`, `B = [0,4]`. What is `f⁻¹(B)`? Does `f⁻¹` exist as a function?

`CAT-SET-02` — **Direct and inverse image treated as mutually cancelling**
: `f(f⁻¹(B)) = B` and `f⁻¹(f(A)) = A` asserted in general.
: **Boundary:** `f(f⁻¹(B)) ⊆ B` with equality iff `f` is surjective onto `B`;
  `A ⊆ f⁻¹(f(A))` with equality iff `f` is injective.
: **Probe:** `f(x) = x²`, `A = {1}` — compute `f⁻¹(f(A))`.

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

## Complex numbers

`CAT-CPX-01` — **Argument treated as a number rather than a class mod `2π`**
: `Arg(e^{i7π/3}) = 7π/3`; `e^{i7π/3}` and `e^{iπ/3}` believed to be different numbers.
: **Boundary:** the argument is defined only mod `2π`; the *principal* argument is the
  representative in `(-π, π]`.
: **Probe:** "how many distinct complex numbers have argument `7π/3`?" then have him plot both.

`CAT-CPX-02` — **Quadrant discarded when recovering an argument**
: `θ = arctan(y/x)` regardless of the signs of `x` and `y`, placing `-√3 + i` at `-π/6`.
: **Boundary:** `arctan` returns values in `(-π/2, π/2)`, so it cannot reach quadrants II and
  III; the quadrant must be restored from the signs of `x` and `y`.
: **Probe:** ask for the argument of `z` and of `-z`. The ratio `y/x` is identical for both, so
  a rule that reads only the ratio cannot distinguish them.

`CAT-CPX-03` — **Only one root reported where `n` exist**
: One square root of a negative number; one cube root of `-8i`; a complex quadratic root given
  without its conjugate partner.
: **Boundary:** a nonzero complex number has exactly `n` distinct `n`-th roots, equally spaced
  by `2π/n` on a circle of radius `|z|^{1/n}`.
: **Probe:** "your root has modulus `r` and argument `θ` — what else raised to the `n`-th power
  lands on the same number?"

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

## Multivariable calculus

`CAT-MVC-01` — **Directional derivative taken along a non-unit vector**
: `D_b f(p) = ∇f(p) · b` with `|b| ≠ 1`, so the reported rate scales with the length of `b`.
: **Boundary:** the directional derivative is defined along a *unit* vector; normalise first, or
  divide by `|b|`.
: **Probe:** compute along `b` and along `2b`. The direction did not change — so why did the
  rate double?

`CAT-MVC-02` — **Point and displacement vector conflated**
: The direction from `p` toward `b` taken to be `b` rather than `b - p`; points added together
  as though they were vectors.
: **Boundary:** points are positions; displacements are *differences* of positions. Only the
  latter can be scaled and added.
: **Probe:** "what is the direction from `p` to `b` when `p = b`?" His rule returns `b`; the
  answer is the zero vector.

`CAT-MVC-03` — **Derivative shape not tracked**
: `∇f` (column), `Df` (row), and `DG` (matrix) used interchangeably; a gradient expected for a
  vector-valued map, or a Jacobian expected to be a single column.
: **Boundary:** the shape is forced by the dimensions of domain and codomain, not chosen.
: **Probe:** ask for the dimensions of every factor *before* any entry is computed; a
  non-conformable product settles it without arithmetic.

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

`CAT-LIN-08` — **Pairwise independence taken for independence of the family**
: "No two of them are proportional, so the family is free" (French: *famille libre*).
: **Boundary:** independence is a condition on *all* coefficients at once, not on pairs.
: **Probe:** `sin x`, `cos x`, `sin(x + π/4)` — every pair is independent, yet
  `sin(x+π/4) = (sin x + cos x)/√2`. Three vectors in a 2-dimensional span are always dependent.

`CAT-LIN-09` — **Sum of subspaces assumed direct**
: `F + G` written `F ⊕ G` without checking `F ∩ G = {0}`, and
  `dim(F+G) = dim F + dim G` asserted in general.
: **Boundary:** Grassmann — `dim(F+G) = dim F + dim G − dim(F∩G)`.
: **Probe:** two distinct planes through the origin in `ℝ³`: `3 + 3 ≠ dim(F+G) ≤ 3`.

`CAT-LIN-10` — **"The" supplement treated as unique**
: A supplementary subspace spoken of as *the* supplement, or identified with the set-theoretic
  complement, or assumed orthogonal (French: *un supplémentaire*, never *le*).
: **Boundary:** supplements exist in abundance and are essentially never unique; the complement
  of a subspace is not even a subspace.
: **Probe:** in `ℝ²` with `F` the `x`-axis, give two different supplements. Is `ℝ² \ F` one?

`CAT-LIN-11` — **Projection assumed orthogonal**
: `Ker p` and `Im p` believed perpendicular rather than merely supplementary, so a projector is
  reconstructed with the wrong direction.
: **Boundary:** `p∘p = p` gives `E = Ker p ⊕ Im p` and nothing more; orthogonality is an extra
  hypothesis requiring an inner product.
: **Probe:** project onto the `x`-axis along the line `y = x`. Where does `(0,1)` land?

`CAT-LIN-12` — **Rank–nullity anchored to the wrong space**
: `dim Ker f + dim Im f` set equal to the dimension of the *codomain*, or of `Im f`.
: **Boundary:** the sum is the dimension of the **domain** (French: *théorème du rang*).
: **Probe:** `f : ℝ³ → ℝ²`, `f(x,y,z) = (x,y)`. Rank 2, nullity 1, sum 3 — the domain, not 2.

`CAT-LIN-13` — **Injective ⟺ surjective applied outside endomorphisms**
: The finite-dimensional equivalence transferred to maps between spaces of different dimension.
: **Boundary:** it needs `dim E = dim F`; for an endomorphism it is automatic.
: **Probe:** `ℝ² → ℝ³`, `(x,y) ↦ (x,y,0)` — injective, not surjective.

`CAT-LIN-14` — **Union of subspaces assumed to be a subspace**
: `F ∪ G` called a subspace because both parts are.
: **Boundary:** the union is a subspace only when one contains the other; the intersection is
  always fine, which is what makes the asymmetry easy to miss.
: **Probe:** the two axes in `ℝ²` — `(1,0) + (0,1) = (1,1)` lies on neither.

`CAT-LIN-15` — **`det(λA) = λ det A`**
: Scalar pulled out once instead of once per row. A sibling of `CAT-LIN-03`, but it survives
  even after that one is repaired, because here the student *is* using multilinearity — just not
  counting the rows.
: **Boundary:** `det(λA) = λⁿ det A` for `A` of size `n`.
: **Probe:** `A = [[1,2],[3,5]]`, `det A = −1`. Compute `det(2A)`: it is `−4`, not `−2`.

`CAT-LIN-16` — **Elementary row operations assumed to preserve the determinant**
: All three operations treated as neutral because "they don't change the solution set".
: **Boundary:** adding a multiple of a row leaves `det` alone; swapping two rows flips the sign;
  scaling a row by `λ` multiplies `det` by `λ`. Only the first is free.
: **Probe:** `B = [[1,2],[3,4]]`, `det B = −2`. Swap the rows: `+2`. Scale row 1 by 3: `−6`.
  Add `2R₁` to `R₂`: still `−2`.

`CAT-LIN-17` — **Matrix of a map written with the images of the basis vectors as rows**
: `mat(f)` built by writing `f(e_j)` along row `j` instead of column `j`, giving the transpose
  — which then silently breaks every later computation, including `mat(f∘g)`.
: **Boundary:** columns are images; the `j`-th column holds the coordinates of `f(e_j)`.
: **Probe:** a deliberately non-symmetric map on `ℝ²`, e.g. `f(x,y) = (x + 2y,\ y)`. Build the
  matrix, then check `mat(f)·e₁` really is `f(e₁)`.

---

## Ordinary differential equations

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

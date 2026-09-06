# Probe taxonomy

Ten probe types. Each is good at something different; the skill is picking the one that splits
your current candidate set.

Before asking any probe, write down what each candidate predicts. **If two candidates predict
the same answer, the probe is wasted.**

---

## 1. Predict–observe–explain

Ask for a prediction and a commitment *before* revealing anything. Then show the result. Then
ask him to explain the gap.

> "Before we compute it — what do you expect `d/dx sin(3x)` to be? Commit to an answer."

The commitment is not a formality. Without it there is no surprise, and without surprise the
old rule survives contact with the counterexample. This is the default opening for any repair.

## 2. Contrasting cases / near-miss pairs

Two problems, nearly identical on the surface, where the rule applies to one and not the other.

> `(a·b)/a` and `(a+b)/a`
> `d/dx (x²)` and `d/dx (2^x)`

Best probe type for **boundary** confusion, which is most misconceptions. The closer the pair,
the sharper the diagnosis — a distant pair lets him attribute the difference to "a different
kind of problem".

## 3. Error-first (find the flaw)

Present worked reasoning containing one specific bug and ask him to find it.

Reveals whether he can *detect* the rule as wrong even when he cannot avoid producing it — a
genuinely different capability, and the difference tells you whether to teach the rule or teach
monitoring. Seed the flaw with the exact candidate you are testing.

## 4. Boundary probing

> "When would that be false?"

The single highest-yield question in the whole taxonomy. Fluent-but-not-mastered students give
correct answers and cannot name a single boundary. Required before promoting any concept to
`mastered`.

## 5. Misconception-mapped multiple choice

Every distractor is the answer produced by one specific candidate bug. His choice names his
rule.

> `(x + 3)² = ?`
> (a) `x² + 6x + 9` — correct
> (b) `x² + 9` — CAT-ALG-01
> (c) `x² + 3x + 9` — partial distribution
> (d) `x² + 6x + 3` — constant not squared

Cheapest probe to grade and the most information per question, but only if the distractors are
built from real candidates. Randomly wrong options teach you nothing.

## 6. Explain-back

> "Explain that rule to me as if I were about to make the mistake you just made."

Exposes memorised procedure with no model behind it. A student who can execute but not explain
is `fluent`, not `mastered`, and will fail under variation.

## 7. Transfer probe

Same underlying rule, unfamiliar surface structure. `det(A+B)` for a student whose linearity
bug was diagnosed on `(a+b)²`.

Required as step 7 of every repair. **The transfer problem must not look like the original** —
that is the usual reason a repair passes and then relapses two weeks later.

## 8. Justification probe

Applied to a **correct** answer: "why does that work?"

Right answers from wrong rules are the expensive case; they are invisible until they fail, and
by then they have been reinforced. Never let a correct answer close an inquiry without one of
these.

## 9. Limiting and degenerate cases

`n = 0`, `x → ∞`, the identity matrix, the zero vector, `a = b`.

Cheap, fast, and devastating to over-generalised rules — most wrong rules break at a degenerate
case, and the arithmetic is easy enough that he cannot hide behind computation.

## 10. Counterexample demand

> "Give me a case where that fails."

Tests whether he holds the rule *as* a rule with scope, or as a universal truth. Inability to
produce a counterexample to a false universal is itself the diagnosis.

---

## Choosing

| Situation | Probe |
|---|---|
| Two candidates predict the same thing | Change the surface structure so they diverge (§2, §9) |
| He is right but you are unsure why | Justification (§8) |
| He is stuck and frustrated | Error-first (§3) — lower stakes, no need to produce |
| You need to confirm before naming a bug | Transfer (§7) — reproduction under variation |
| Checking for mastery vs fluency | Boundary (§4), explain-back (§6) |
| Repairing a confirmed bug | Predict–observe–explain (§1) then contrasting cases (§2) |
| Fast triage across many concepts | Mapped MCQ (§5) |

**One probe at a time.** A batch lets him answer the easy one and quietly skip the sharp one,
and you lose the discrimination the sharp one was designed to give.

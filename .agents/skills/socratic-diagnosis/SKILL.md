---
name: socratic-diagnosis
description: Find out exactly which wrong rule a student is using, by treating diagnosis as hypothesis testing over candidate bugs, then repair it. Use when a student makes a mathematical error, gives a right answer for possibly wrong reasons, is stuck, or when grilling a topic to find hidden misconceptions. Includes a seeded catalogue of common algebra, calculus, linear algebra and ODE bugs, a probe taxonomy for designing discriminating questions, and a repair protocol that survives relapse.
---

# Socratic diagnosis

Marking an answer wrong tells you nothing you can act on. The goal is to identify the
**generative rule** producing the error.

A misconception is not a gap — it is a *rule*. `(a+b)² = a² + b²`, `ln(a+b) = ln a + ln b` and
`√(a²+b²) = a + b` are one rule wearing three costumes: `f(a+b) = f(a) + f(b)`. Because it is a
rule, it makes predictions. That is what makes diagnosis tractable: you can choose the question
whose answer differs across competing candidates, instead of asking more questions and hoping.

Students hold wrong rules because those rules **worked** on everything they had met. Treat the
misconception as a rational inference from limited data, not as carelessness.

## The loop

1. **Observe** an error, or pick a target concept to probe.
2. **Generate candidates**, in this priority order:
   - active ledger entries in the relevant domain **and its prerequisite domains** — read the
     course hub's `primary_domains` and `prerequisite_domains` to know which those are;
   - `references/CATALOGUE.md` entries touching the concept;
   - novel hypotheses induced from the specific error, if nothing above explains it.
3. **Rank by prior.** A ledger entry with `confidence: 0.8` outranks any catalogue base rate —
   it is evidence about *this* student. Prefer the smallest set that explains the error.
4. **Design a splitting probe.** See `references/PROBES.md`. A probe is worth asking only if
   the candidates predict *different* answers to it.
5. **Update** confidence from the response.
6. **Stop** when one candidate dominates, or when the evidence says it was a slip.

Step 2 is where the domain taxonomy earns its keep: a DE error pulls in Calculus and Algebra
candidates, because that is where the rules actually live.

**Keep the hypothesis space small.** A bloated candidate set makes discriminating probes
*harder* to design, not easier — with twelve candidates, almost no single question splits them.
Three to five is the working range.

## Designing a probe that splits

The test of a probe: *before* asking, write down what each candidate predicts. If two
candidates predict the same answer, the probe cannot distinguish them — design a different one.

Worked example. He writes `d/dx sin(3x) = cos(3x)`. Candidates:

| # | Candidate | Predicts for `d/dx (5x)³` |
|---|---|---|
| A | Chain rule truncation — omits the inner derivative | `3(5x)²` |
| B | Believes the inner function's derivative is always 1 | `3(5x)²` |
| C | Slip | correct: `15(5x)²` |

A and B predict the same thing, so that probe separates only C. To split A from B, use an inner
function whose derivative is *not* constant — `d/dx (x²+1)³`. A gives `3(x²+1)²`; B also gives
`3(x²+1)²`. Still no split. The real discriminator is asking him to **state the rule** and then
apply it where the outer function is the identity: `d/dx (x²+1)` — B predicts `1`, A predicts
`2x`. Now the probe does work.

That is the discipline: if you cannot say in advance what each candidate predicts, you are not
diagnosing, you are quizzing.

## Slip or bug

A **slip** is inconsistent and self-correctable. A **bug** reproduces under variation.

Before naming anything, reproduce it — same rule, different surface structure. Then ask him to
check his own work; a slip is usually caught immediately, a bug is defended.

**Do not create a ledger entry for a typo.** Every spurious entry inflates the hypothesis space
for every future session and corrupts the confidence figures.

## Repair protocol

Repairs that skip steps relapse. Run all eight.

1. **Elicit a prediction and get a commitment.** Ask what he expects *before* showing anything.
   Without commitment there is no surprise, and without surprise nothing changes.
2. **Present the contrasting case** where his rule fails — as close as possible to cases where
   it succeeded.
3. **Let him observe the failure.** Do not narrate it. If you say "see, that's wrong", you have
   done the cognitive work he needed to do.
4. **Ask him to explain why the rule broke.**
5. **Co-construct the corrected rule together with its boundary condition.** A rule without a
   boundary is just another over-generalisation waiting to happen.
6. **Explain why the old rule worked in every prior case he had met.** ← the usually-skipped one
7. **Transfer test** on unfamiliar surface structure. Same rule, different clothes.
8. **Schedule re-probes at 1 / 7 / 28 days** via `learner-model`.

**Step 6 is why repaired misconceptions relapse.** If the correction feels arbitrary, the old
rule remains the more economical explanation of everything he has seen, and it comes back under
load. Show him that his rule was a *reasonable generalisation from a biased sample* — it held
for every `f` he had met because every one of them happened to be linear.

## Recurrence is a signal, not a new bug

If a resolved misconception resurfaces in a **different course**, do not open a new entry.
Reopen the existing one, increment `repair_attempts`, add the course to `surfaced_in`.

`repair_attempts > 1` means the previous repair was surface-level — almost always step 6 was
skipped, or step 7 used a transfer problem too close to the original. On a reopen, change the
approach rather than repeating it: a different contrasting case, a different representation
(graphical instead of symbolic), a different entry point.

This detection is only possible because the entry was never course-scoped in the first place.

## Grilling stance

- Ask for the **rule**, not just the answer. "What are you using here, and when does it apply?"
- Ask for **boundaries**. "When would that be false?" is the single highest-yield question.
- Ask for **justification of correct answers**. A right answer from a wrong rule is a bug you
  have not found yet, and it is the most expensive kind — it is invisible until it fails.
- **Never confirm before he commits.** Praise given early ends the inquiry.
- Do not soften a contradiction. Do not lead with "great question". Let the surprise land.
- One probe at a time. A batch of questions lets him answer the easy one and skip the sharp one.

## Verification

Before asserting that something is mathematically wrong, check it with `math-verify`. Below
tier 3 sympy is unavailable — say **UNVERIFIED** rather than asserting. Confidently mis-grading
a correct answer destroys the trust the whole method depends on.

## Recording the outcome

Hand everything to `learner-model`: confirmed bugs with dated evidence, updated confidences,
concept levels, next probe dates, and a session note. Diagnosis that is not written down was a
conversation, not tutoring.

---
name: learner-model
description: Read and write the student model in the Obsidian vault — misconception ledger, concept mastery, session logs, and the .base dashboards. Use when recording what a student got wrong or right, checking what is due for review, looking up open misconceptions before a session, scheduling re-probes, or adding a course dashboard. Owns every frontmatter schema; any skill that writes learner-model notes must follow the schemas here.
---

# Learner model

The vault *is* the database. Notes hold the data in frontmatter, `.base` files are saved
queries over it. There is no second store and no cache — if it is not in a note, it is not
known.

This skill owns the schemas. `socratic-diagnosis`, `tutor-session` and `course-authoring` all
write learner-model notes, and they all follow this file. Schema drift silently empties
dashboards, so there is exactly one place the schemas are written down:
`references/SCHEMAS.md`.

## The one rule that everything else depends on

**A misconception is filed under the domain its rule belongs to, never under the course that
surfaced it.**

A course is a *vehicle*. A domain is a *body of knowledge*. The student meets
`(a+b)² = a² + b²` while doing differential equations, but the rule `f(a+b) = f(a) + f(b)` is
statable without any calculus at all — so it is an **Algebra** bug, and it is filed in
`Learner Model/Misconceptions/Algebra/`.

File the rule, not the symptom. Ask: *what is the most primitive domain in which this wrong
rule can be stated?* That is the domain.

Why it matters, concretely: file that bug under "Differential Equations" and when the student
later studies linear algebra the tutor has no reason to look for it, re-diagnoses it from
scratch, and loses the one genuinely valuable fact — that **it is the same bug resurfacing**,
which is the signal that the repair was surface-level.

**Course names are never domain names.** There is no `Misconceptions/Vector Spaces/` folder and
there must never be one; a Vector Spaces course surfaces `Linear Algebra` bugs. Course names
appear only as *values* in `surfaced_in` and `required_by.course`. `scripts/check_env.py` fails
the probe if a domain folder matches a course folder.

Domain folders are created on demand. Only domains the student has actually touched exist.

## Object model

| Object | Lives in | Answers |
|---|---|---|
| Misconception | `Learner Model/Misconceptions/<Domain>/M### - <name>.md` | What wrong rule does he hold, how sure are we, when do we re-check? |
| Concept | `Learner Model/Concepts/<Domain>/<Concept>.md` | How well does he know this, when is it due, which courses need it? |
| Session | `Learner Model/Sessions/<year>/YYYY-MM-DD - <mode> - <topic>.md` | What happened, what was probed, what changed? |
| Course | `Courses/<Course>/<Course> - Course Hub.md` | Which domains does this course exercise? (owned by `course-authoring`) |

Read `references/SCHEMAS.md` before writing any of them. Read `references/DASHBOARDS.md` when
adding a course or changing a `.base` file.

**Catalogue vs. ledger — do not confuse them.** The *catalogue* in
`socratic-diagnosis/references/CATALOGUE.md` is the generic hypothesis space: bugs students in
general have. The *ledger* here is the posterior: bugs **this** student has actually
demonstrated. The catalogue is a prior and ships with the skill; the ledger is evidence and
lives in the vault.

## Allocating a misconception id

`id` is global, stable and never reused. Wikilinks point at note *names* containing the id, so
renumbering breaks links — ids are permanent once written.

Before minting one:

1. Scan **every** domain folder, not just the one you are writing to:
   `Learner Model/Misconceptions/**/*.md`.
2. Take `max(id) + 1`, formatted `M%03d`.
3. Write the note in the same step, before doing anything else.

`check_env.py` reports `next_misconception_id`, but that is a **snapshot from session start**.
If you have already written a misconception this session it is stale — re-scan. Never derive an
id from a count (a deletion would recycle it) and never pick one from memory.

If two entries turn out to be the same bug, **merge with `aliases`** — put the loser's id in
the winner's `aliases` list and set the loser to `status: resolved`. Do not renumber.

## Writing evidence

**Do not create a ledger entry for a slip.** A slip is inconsistent and self-correctable; a bug
reproduces under variation. Require reproduction before naming something. A ledger full of
typos makes the confidence figures meaningless and inflates the hypothesis space, which makes
discriminating probes *harder* to design.

When a bug is confirmed:

- **New bug** → mint an id, `status: active`, `confidence` from the strength of the evidence,
  `first_observed` today, `next_probe` today + 1 day.
- **Already in the ledger** → raise `confidence`, update `last_probed`, increment `probe_count`.
- **Resolved bug resurfacing** → do not create a new entry. Reopen the existing one:
  `status: active`, increment `repair_attempts`, add the current course to `surfaced_in`.
  This is the highest-signal event the model can record — it means the repair did not take.
- **Evidence against** → lower `confidence`. Below `0.2` set `status: resolved` rather than
  deleting; the history is the point.

Always append a dated evidence line to the note body: the actual prompt, his actual answer, and
what it discriminated. Frontmatter carries the state; the body carries the proof.

## Scheduling

Re-probe a repaired misconception at **1 / 7 / 28 days**. Set `next_probe` when you write the
outcome, never later.

Concept review intervals expand on success and collapse on failure:

| Outcome | New `review_interval_days` |
|---|---|
| Correct and fluent | `interval × 2`, capped at 90 |
| Correct but slow or hesitant | unchanged |
| Wrong | `1`, and check for an open misconception |

`next_review = last_assessed + review_interval_days`.

A concept with an open high-severity misconception is **not** eligible for interval expansion,
whatever the answer looked like. Fluency on top of a broken rule is memorisation.

## Reading before a session

At session start read in this order — cheapest first, and each step narrows the next:

1. `Learner Model/Review Queue.base` — what is due today.
2. The course hub's `primary_domains` + `prerequisite_domains`.
3. Open misconceptions in *those domains only*.
4. Concept levels for the target topic.

Step 2 is what makes step 3 cheap: a Differential Equations session loads `Calculus`, `Algebra`
and `Linear Algebra` candidates and ignores everything else.

## Tier degradation

| Tier | Behaviour |
|---|---|
| 3 | Read and write notes directly or via the Obsidian CLI. Full scheduling. |
| 2 | Read and write markdown; no `check_env.py`, so scan the folders yourself for ids. |
| 1 | No vault access. Keep the log in the conversation and **give the student the exact note content to paste**, frontmatter included. Never claim a note was written. |

At tier 1, state plainly at the end which notes need creating. A learner model the student
believes is being maintained, but is not, is worse than none.

## Checklist before finishing a session

- [ ] Every confirmed bug has a ledger entry with today's evidence appended.
- [ ] Every entry touched has `last_probed` and `next_probe` set.
- [ ] Every concept exercised has `level`, `last_assessed`, `next_review`, `evidence_count`.
- [ ] A session note exists, with `domains` reflecting what was *actually* exercised.
- [ ] No new domain folder shares a name with a course.

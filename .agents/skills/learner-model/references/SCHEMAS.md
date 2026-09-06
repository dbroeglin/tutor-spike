# Frontmatter schemas

**This file is the single source of truth.** Every skill that writes a learner-model note
follows it exactly. The `.base` dashboards query these property names; a typo does not raise an
error, it silently produces an empty dashboard, which is much worse.

Rules that apply to all schemas:

- Dates are `YYYY-MM-DD`, unquoted.
- Wikilinks in frontmatter are **quoted strings**: `"[[Chain Rule]]"`.
- Use **name-only** wikilinks, not path-qualified ones. Note names are vault-unique by
  convention.
- Empty list → `[]`. Unknown scalar → `null`. Never omit a key that the schema defines;
  a missing key and an empty one behave differently in Bases filters.

---

## Misconception

`Learner Model/Misconceptions/<Domain>/M### - <name>.md`

```yaml
---
type: misconception
id: M012                    # global, stable, never reused. See "Allocating an id".
catalog_id: CAT-ALG-01      # null if novel / induced from this student
name: Linearity over-generalization
domain: Algebra             # most primitive domain the rule is statable in
surfaced_in:                # many-to-many: courses where it was actually observed
  - Differential Equations
concepts:                   # concept notes this bug damages
  - "[[Chain Rule]]"
  - "[[Logarithm Laws]]"
aliases: []                 # ids merged INTO this entry when two proved to be one bug
status: active              # active | repairing | resolved
severity: high              # high | medium | low
confidence: 0.8             # 0.0-1.0, posterior that he actually holds this rule
first_observed: 2026-01-12
last_probed: 2026-01-19
next_probe: 2026-01-26
probe_count: 3
repair_attempts: 1
---
```

| Field | Notes |
|---|---|
| `id` | Permanent. Renumbering breaks wikilinks. Merge via `aliases` instead. |
| `domain` | The filing decision. Never a course name. |
| `severity` | `high` = corrupts downstream reasoning; `low` = local and self-limiting. |
| `confidence` | Rises with reproduction under variation, falls with counter-evidence. |
| `repair_attempts` | `> 1` means a repair failed. The most interesting number in the ledger. |

**Body layout.** Frontmatter carries state; the body carries proof.

```markdown
## The wrong rule
f(a+b) = f(a) + f(b), applied to any f that looks like an operation.

## Correct rule and its boundary
Additivity holds only for linear f. Boundary: f(x) = cx (and, with homogeneity, linear maps).

## Evidence
- 2026-01-19 — asked to expand (x+3)²; wrote x² + 9. Reproduced on (a+b)³, so not a slip.
- 2026-01-12 — wrote ln(x+1) = ln x + ln 1 unprompted mid-solution.

## Why the wrong rule felt right
Every f he had met before was a scaling. Distributivity of × over + generalises silently.
```

---

## Concept

`Learner Model/Concepts/<Domain>/<Concept>.md`

```yaml
---
type: concept
concept: Eigenvalues
domain: Linear Algebra      # where the concept lives, not where it is used
required_by:                # list of objects — courses that depend on it
  - course: Differential Equations
    plan_week: 0            # 0 = prerequisite
  - course: Vector Spaces
    plan_week: 6            # core content in that course
level: practiced            # unseen | introduced | practiced | fluent | mastered
last_assessed: 2026-01-19
next_review: 2026-01-26
review_interval_days: 7
evidence_count: 4
open_misconceptions:
  - "[[M012 - Linearity over-generalization]]"
---
```

**`required_by` is the load-bearing field.** It is what lets a course dashboard show
prerequisite concepts that live in other domains — the DE dashboard surfaces `Eigenvalues`
without owning it.

It is a list of objects, and Bases queries it with
`required_by.map(value.course).contains("<Course>")`. Keep the shape exactly as above:
flattening it to a list of strings would lose `plan_week` and break the course dashboards'
week-0 split.

**The case worth understanding.** `Eigenvalues` above is *one* note that is a week-0
prerequisite for one course and week-6 core content for another. One mastery level, one review
schedule, one evidence count. Practising it in either course improves the other's dashboard
automatically — because the fact was never stored per-course. Filed under courses, this note
would exist twice, the copies would diverge, and the tutor would re-teach something already
fluent.

**Mastery ladder.**

| Level | Means |
|---|---|
| `unseen` | Not yet encountered. |
| `introduced` | Has seen it; cannot yet use it unaided. |
| `practiced` | Correct on familiar surface structure, slow or with hints. |
| `fluent` | Correct and quick on unfamiliar surface structure. |
| `mastered` | Fluent, *and* can state the boundary conditions and explain why they hold. |

The gap between `fluent` and `mastered` is where misconceptions hide. Do not promote to
`mastered` on correct answers alone — require an explanation of when the rule fails.

---

## Session

`Learner Model/Sessions/<year>/YYYY-MM-DD - <mode> - <topic>.md`

```yaml
---
type: session
date: 2026-01-19
mode: grill                 # grill | teach | check | review
course: Differential Equations    # the vehicle; null for a course-less session
domains: [Calculus, Algebra]      # what was ACTUALLY exercised
concepts: ["[[Chain Rule]]"]
duration_min: 35
misconceptions_probed: ["[[M012 - Linearity over-generalization]]"]
misconceptions_found: []
outcome: partial-repair     # diagnosed | partial-repair | repaired | no-change | blocked
tier: 3                     # capability tier the session actually ran at
---
```

`course` and `domains` differ on purpose, and the difference is the whole model in miniature:
the session happened *inside* a DE course but exercised *calculus and algebra*. Recording only
the course would lose that.

Record `tier` because a tier-1 session's conclusions are weaker — nothing was symbolically
verified.

---

## Course

`Courses/<Course>/<Course> - Course Hub.md`. Owned by `course-authoring`; reproduced here
because `Courses.base` and the diagnosis loop both read it.

```yaml
---
type: course
course: Differential Equations    # canonical name; the join key used everywhere else
status: active                    # planned | active | paused | complete
started: 2026-09-03
primary_domains:                  # domains this course mainly exercises — NOT folders
  - Differential Equations
  - Linear Algebra
prerequisite_domains:
  - Calculus
  - Algebra
sources:                          # open list; shape varies by course
  - title: Introduction to Differential Equations, Second Edition
    kind: book                    # book | video | papers | notes | mixed
    nav: "[[Introduction to Differential Equations - TOC]]"
plan: "[[Differential Equations - Learning Plan]]"
prerequisite_index: "[[Differential Equations - Prerequisite Exercise Index]]"
---
```

`primary_domains` + `prerequisite_domains` are what make candidate generation mechanical: they
are exactly the ledger folders to load when a session is scoped to this course.

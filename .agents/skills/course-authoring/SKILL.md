---
name: course-authoring
description: Create or extend a course in the vault from source material — a book, PDFs, a video series, papers, or notes. Use when the student wants to start studying a new subject, add a textbook or course to the vault, generate a learning plan with progress gates, or build prerequisite diagnostic exercises. Produces the course core contract that tutor-session and learner-model depend on.
---

# Course authoring

A course lives in `Courses/<Course>/` and satisfies a fixed **core contract**. Content below
that contract varies freely — one course is a textbook, the next may be several PDFs, a video
series, or a problem set.

## The core contract

Every course has exactly these, named by this pattern:

| Note | Purpose |
|---|---|
| `<Course> - Course Hub.md` | Entry point and course record. `type: course`. |
| `<Course> - Learning Plan.md` | Sequenced plan with progress gates. |
| `Prerequisite Exercises/` + `<Course> - Prerequisite Exercise Index.md` | Entry diagnostics. |
| `Resources/` | Source material, whatever the format. |
| `<Course> - Learner Dashboard.base` | Course-scoped view of the global learner model. |

A course with no prerequisites still gets the index, listing none. The contract is what other
skills rely on; do not make it conditional.

**The hub is the stable interface.** `tutor-session` reads the hub and the plan and nothing
else. That is what makes the rest free to vary.

## Source-specific material hangs off the hub

Anything determined by the *shape* of the source is named `<source title> - <artifact>` and
declared in the hub's `sources:` frontmatter:

```yaml
sources:
  - title: Introduction to Differential Equations, Second Edition
    kind: book
    nav: "[[Introduction to Differential Equations - TOC]]"
```

| `kind` | Typical `nav` artifact |
|---|---|
| `book` | TOC and section tracker |
| `video` | Lecture index with timestamps |
| `papers` | Reading list with dependency order |
| `notes` | Topic index |
| `mixed` | One entry per source |

A course may have several sources. The consequence: **no other skill needs to know what format
a course's source is in.** Adding a video course later changes only the authoring branch here,
not the tutor's reading path.

Do not invent structure for formats you have not been given. Solve the source you have.

## Procedure

1. **Read the source.** Do not summarise from the title. Extract the real structure, the
   difficulty gradient, and where it assumes knowledge it does not teach.
2. **Identify domains.** Fill `primary_domains` (what the course mainly exercises) and
   `prerequisite_domains` (what it assumes). These drive candidate generation in
   `socratic-diagnosis`, so be accurate rather than generous.
   **Never use the course name as a domain.** A Vector Spaces course exercises `Linear Algebra`.
3. **Write the hub** using the `type: course` schema in
   `learner-model/references/SCHEMAS.md`.
4. **Write the plan** — phases with explicit **gates**. A gate is a capability statement he can
   be tested against ("can classify an ODE and justify the method"), not a chapter number.
5. **Build prerequisite diagnostics** — see below.
6. **Copy a learner dashboard** — see `learner-model/references/DASHBOARDS.md`. Copy an existing
   `.base` and replace every occurrence of the old course name.
7. **Verify** — run `uv run scripts/check_env.py` and confirm the new course appears in
   `Courses.base` with no domain/course collision.

## Prerequisite exercises

These are the first evidence the learner model ever gets, so build them to diagnose, not to
grade.

- **One concept per exercise**, so a wrong answer localises.
- **Map distractors to catalogue entries.** Every wrong option should be the answer produced by
  a specific bug in `socratic-diagnosis/references/CATALOGUE.md`, and the answer key should say
  which. An unmapped distractor tells you he is wrong but not why, which is the thing the whole
  system exists to avoid.
- **Include a boundary question** per topic: "when does this rule fail?"
- **Include the rubric and key in the note**, with the misconception each wrong answer implies.
- Name them `NN - <Concept>.md` and list them in the index.

Note that prerequisite exercises usually belong to *other* domains than the course — the
Differential Equations course's prerequisites are calculus, analysis and linear algebra. That
is expected and is exactly why the learner model is indexed by domain.

## Linking

Write **name-only wikilinks** — `[[01 - Differentiation Rules]]`, not
`[[Courses/X/Prerequisite Exercises/01 - Differentiation Rules]]`.

Note names are vault-unique by convention (the `<Course> - <artifact>` prefix guarantees it for
course-level notes). Path-qualified links once turned a two-folder reorganisation into a
241-link migration; do not recreate that debt.

## Do not reorganise the student's content

Existing course content is his. Prerequisite exercises stay in the course folder even when they
belong to another domain. The domain taxonomy is enforced in the learner model, which is the
layer that has to query correctly — not in the content layer, which only has to be browsable.

# Dashboards

Six views over the same notes. No data is duplicated: a `.base` file queries the whole vault
and filters, so a course-scoped dashboard can sit *inside* the course folder while reading the
same global, un-duplicated learner model. Locality of browsing without duplication of data.

| File | Location | Shows |
|---|---|---|
| `Misconceptions.base` | `Learner Model/` | Active bugs grouped by domain; overdue probes; relapsed bugs |
| `Concept Mastery.base` | `Learner Model/` | Mastery ladder by domain; weakest first; concepts shared across courses |
| `Review Queue.base` | `Learner Model/` | Everything due today, both re-probes and reviews |
| `Courses.base` | `Courses/` | Course registry: status, domains, source kinds |
| `<X> - Learner Dashboard.base` | `Courses/<X>/` | One course's slice: prerequisites, course concepts, bugs, session history |

Syntax reference: the `obsidian-bases` skill. Validate any edit by parsing it as YAML before
declaring it done — Bases reports a generic error and gives no line number.

## Adding a course dashboard

This is the whole procedure. Copy an existing dashboard and change the course-name string.

1. Copy `Courses/Differential Equations/DE - Learner Dashboard.base` to
   `Courses/<New Course>/<New Course> - Learner Dashboard.base`.
2. Replace **every** occurrence of `Differential Equations` with the new course name. There are
   several: three in the global `filters` block, two in the `week` / `also_in` / `bug_courses`
   formulas, and two in view-level filters. Search the file; do not edit from memory.
3. Parse it as YAML to confirm it is still valid.

That is all. No data migrates, no note changes, no other dashboard is affected — which is the
point of indexing the learner model by domain rather than by course.

## The filter that does the work

```yaml
filters:
  or:
    - and:
        - 'type == "misconception"'
        - 'surfaced_in && surfaced_in.contains("Differential Equations")'
    - and:
        - 'type == "concept"'
        - 'required_by && required_by.map(value.course).contains("Differential Equations")'
    - and:
        - 'type == "session"'
        - 'course == "Differential Equations"'
```

Three different relationships to one course, expressed three different ways because the
underlying relations genuinely differ:

- a **misconception** was *observed* in the course — a flat list of course names;
- a **concept** is *required by* the course at a plan position — a list of objects, so
  `map(value.course)` first;
- a **session** *happened in* the course — a single scalar.

The `&&` guards matter. `surfaced_in.contains(...)` on a note where `surfaced_in` is absent
throws rather than returning false, and one throwing row empties the whole view.

## The week-0 split

The course dashboard separates prerequisites from course content using `plan_week`:

```yaml
'required_by.filter(value.course == "Differential Equations").map(value.plan_week).contains(0)'
```

`filter()` first, then `map()` — a concept required by two courses has two `plan_week` values,
and without the filter a week-0 prerequisite of *another* course would show up as a
prerequisite of this one. This is exactly the shared-concept case (`Eigenvalues`: week 0 for
DE, week 6 for Vector Spaces), so it is not hypothetical.

## Gotchas

- **`order` is column order, not sort order.** Sorting is done in the Obsidian UI by clicking a
  column. To make a meaningful default order available, expose a numeric rank formula
  (see `formula.rank` in `Concept Mastery.base`) and let the student sort on it.
- **Guard every property access with `if(...)` or `&&`.** Notes that predate a schema addition
  will lack the key.
- **Duration is not a number.** `(date(a) - today())` returns a Duration; take `.days` before
  applying `.round()`.
- **Quoting.** Wrap a formula containing double quotes in single quotes.
- **Empty dashboards usually mean schema drift, not an empty vault.** If a view goes blank,
  check the property names against `SCHEMAS.md` before assuming there is no data.

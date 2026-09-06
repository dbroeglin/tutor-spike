#!/usr/bin/env python3
"""Environment probe for the AI tutor.

Two jobs, one file:

  * ``doctor``  -- classify the current environment into a capability tier and
    report what is missing. Run as the first action of a tutoring session.
  * ``--init``  -- scaffold the vault folders the learner model needs. Run once
    at setup, safe to re-run.

Stdlib only, on purpose: this must run via ``uv run`` with no dependency
resolution, so that the probe costs one fast call and can never itself be the
thing that fails.

The probe is *self-classifying*. Tier 2 and tier 1 environments have no shell,
so they cannot execute this file at all -- and that failure is the answer. If
you are reading this script's output, you are at tier 3 unless a check below
says otherwise.

Exit codes: 0 = healthy at the detected tier, 1 = degraded (see "missing").
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_VAULT = Path.home() / "OneDrive" / "Obsidian" / "AITutorSpike"

# Folders the learner model needs. Domain subfolders (Algebra, Calculus, ...)
# are deliberately absent: they are created on demand, so the vault only ever
# shows domains the student has actually touched.
REQUIRED_DIRS = (
    "Courses",
    "Learner Model",
    "Learner Model/Misconceptions",
    "Learner Model/Concepts",
    "Learner Model/Sessions",
)

REQUIRED_BASES = (
    "Courses/Courses.base",
    "Learner Model/Misconceptions.base",
    "Learner Model/Concept Mastery.base",
    "Learner Model/Review Queue.base",
)

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)


def resolve_vault(explicit: str | None) -> Path:
    """Vault location is host configuration, never tutoring logic."""
    for candidate in (explicit, os.environ.get("TUTOR_VAULT")):
        if candidate:
            return Path(candidate).expanduser()
    return DEFAULT_VAULT


def read_frontmatter(path: Path) -> dict:
    """Minimal scalar frontmatter reader.

    Only top-level ``key: value`` scalars are returned -- enough to identify a
    note's ``type`` and ``id`` without pulling in a YAML dependency. Nested
    structures are ignored rather than half-parsed.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def scan(vault: Path) -> dict:
    """Count learner-model objects and find the next free misconception id."""
    counts = {"course": 0, "misconception": 0, "concept": 0, "session": 0}
    max_id = 0
    if vault.is_dir():
        for note in vault.rglob("*.md"):
            if ".obsidian" in note.parts:
                continue
            fields = read_frontmatter(note)
            note_type = fields.get("type", "")
            if note_type in counts:
                counts[note_type] += 1
            if note_type == "misconception":
                match = re.fullmatch(r"M(\d+)", fields.get("id", ""))
                if match:
                    max_id = max(max_id, int(match.group(1)))
    return {
        "counts": counts,
        # Snapshot only. learner-model MUST re-scan immediately before minting
        # an id -- notes written during the session invalidate this number.
        "next_misconception_id": "M%03d" % (max_id + 1),
    }


def check_domain_collisions(vault: Path) -> list:
    """Enforce the invariant that course names are never domain names.

    A domain folder that matches a course folder means someone filed a bug
    under the course that surfaced it. That silently breaks cross-course
    recurrence detection, which is the whole point of the domain taxonomy.
    """
    courses = vault / "Courses"
    if not courses.is_dir():
        return []
    course_names = {p.name for p in courses.iterdir() if p.is_dir()}
    collisions = []
    for group in ("Misconceptions", "Concepts"):
        root = vault / "Learner Model" / group
        if not root.is_dir():
            continue
        for domain in root.iterdir():
            if domain.is_dir() and domain.name in course_names:
                collisions.append("Learner Model/%s/%s" % (group, domain.name))
    return collisions


def probe(vault: Path) -> dict:
    checks = {}
    missing = []

    checks["python"] = sys.version.split()[0]

    checks["uv"] = shutil.which("uv") is not None
    if not checks["uv"]:
        missing.append("uv (needed by math-verify for symbolic checking)")

    sympy_ok = False
    if checks["uv"]:
        try:
            sympy_ok = subprocess.run(
                ["uv", "run", "--quiet", "--with", "sympy",
                 "python", "-c", "import sympy"],
                capture_output=True, timeout=180,
            ).returncode == 0
        except (OSError, subprocess.SubprocessError):
            sympy_ok = False
    checks["sympy"] = sympy_ok
    if not sympy_ok:
        missing.append("sympy (math-verify must label claims UNVERIFIED)")

    obsidian = shutil.which("obsidian") or shutil.which("Obsidian.com")
    checks["obsidian_cli"] = obsidian is not None
    if obsidian is None:
        missing.append("obsidian CLI (fall back to direct filesystem access)")

    checks["vault"] = str(vault)
    checks["vault_exists"] = vault.is_dir()
    if not vault.is_dir():
        missing.append("vault not found at %s (set TUTOR_VAULT)" % vault)

    absent_dirs = [d for d in REQUIRED_DIRS if not (vault / d).is_dir()]
    absent_bases = [b for b in REQUIRED_BASES if not (vault / b).is_file()]
    checks["missing_dirs"] = absent_dirs
    checks["missing_bases"] = absent_bases
    if absent_dirs:
        missing.append("vault folders missing (%d) -- run with --init" % len(absent_dirs))
    if absent_bases:
        missing.append("dashboards missing (%d) -- see learner-model skill" % len(absent_bases))

    collisions = check_domain_collisions(vault)
    checks["domain_course_collisions"] = collisions
    if collisions:
        missing.append(
            "INVARIANT VIOLATION: domain folder shares a course name -- "
            + ", ".join(collisions)
        )

    # Reaching this line at all proves a shell exists, which is the tier-3
    # discriminator. Everything above only downgrades usable capability.
    result = {
        "tier": 3,
        "tier_name": "full (shell + filesystem)",
        "checks": checks,
        "missing": missing,
        "healthy": not missing,
    }
    if vault.is_dir():
        result.update(scan(vault))
    return result


def init(vault: Path) -> list:
    created = []
    for rel in REQUIRED_DIRS:
        target = vault / rel
        if not target.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            created.append(rel)
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vault", help="vault path (default: $TUTOR_VAULT)")
    parser.add_argument("--init", action="store_true",
                        help="create missing vault folders, then probe")
    args = parser.parse_args()

    vault = resolve_vault(args.vault)

    created = []
    if args.init:
        if not vault.is_dir():
            print("refusing to scaffold: %s does not exist" % vault, file=sys.stderr)
            return 1
        created = init(vault)

    result = probe(vault)
    if created:
        result["created"] = created

    print(json.dumps(result, indent=2))

    if created:
        print("\ncreated %d folder(s): %s" % (len(created), ", ".join(created)),
              file=sys.stderr)
    if result["missing"]:
        print("\ndegraded:", file=sys.stderr)
        for item in result["missing"]:
            print("  - %s" % item, file=sys.stderr)
        return 1
    print("\ntier 3, healthy.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

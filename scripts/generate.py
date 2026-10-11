#!/usr/bin/env python3

"""Build one RenderCV document per role.

For every file in rendercv/variants/, merge the shared files with that
variant's headline, summary, projects and skills order, and write
rendercv/cv.<variant>.generated.yaml.
"""

from copy import deepcopy
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "rendercv"
PROJECTS_DIR = SRC / "projects"
VARIANTS_DIR = SRC / "variants"

# Order matters: this is the top-level key order of the output.
SHARED_FILES = [
    "locale.yaml",
    "settings.yaml",
    "base.yaml",
    "design.yaml",
]

REQUIRED_VARIANT_KEYS = ["output_name", "summary", "projects", "skills_order"]


def fail(message):
    sys.exit(f"error: {message}")


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def pick_highlights(entry, highlight_set):
    """Use highlights_<set> if the entry has it, otherwise highlights."""
    entry = dict(entry)
    if highlight_set:
        alternative = entry.get(f"highlights_{highlight_set}")
        if alternative is not None:
            entry["highlights"] = alternative
    # RenderCV rejects unknown fields, so drop our helper keys.
    return {
        key: value
        for key, value in entry.items()
        if key != "id" and not key.startswith("highlights_")
    }


def build_projects(variant_name, variant, project_sets):
    available = sorted(path.stem for path in PROJECTS_DIR.glob("*.yaml"))
    projects = []
    for project in variant["projects"]:
        path = PROJECTS_DIR / f"{project}.yaml"
        if not path.exists():
            fail(
                f"variant '{variant_name}' lists project '{project}', but "
                f"{path.relative_to(ROOT)} does not exist. "
                f"Available projects: {', '.join(available)}"
            )
        projects.append(pick_highlights(load_yaml(path), project_sets.get(project)))

    unused = set(project_sets) - set(variant["projects"])
    if unused:
        fail(
            f"variant '{variant_name}' sets highlights for projects it does "
            f"not include: {', '.join(sorted(unused))}"
        )
    return projects


def build_experience(variant_name, experience, experience_sets):
    ids = [entry.get("id") for entry in experience]
    unknown = set(experience_sets) - set(ids)
    if unknown:
        fail(
            f"variant '{variant_name}' sets highlights for unknown experience "
            f"ids: {', '.join(sorted(unknown))}. Known ids: "
            f"{', '.join(i for i in ids if i)}"
        )
    return [
        pick_highlights(entry, experience_sets.get(entry.get("id")))
        for entry in experience
    ]


def build_skills(variant_name, skills, order):
    by_label = {group["label"]: group for group in skills}
    unknown = [label for label in order if label not in by_label]
    if unknown:
        fail(
            f"variant '{variant_name}' orders unknown skills groups: "
            f"{', '.join(unknown)}. Known groups: {', '.join(by_label)}"
        )
    # Groups the variant leaves out are not shown.
    return [by_label[label] for label in order]


def build_variant(variant_name, variant, shared):
    missing = [key for key in REQUIRED_VARIANT_KEYS if key not in variant]
    if missing:
        fail(f"variant '{variant_name}' is missing: {', '.join(missing)}")

    highlight_sets = variant.get("highlight_sets") or {}
    project_sets = highlight_sets.get("projects") or {}
    experience_sets = highlight_sets.get("experience") or {}

    document = deepcopy(shared)
    base_cv = document["cv"]
    base_sections = base_cv.pop("sections")

    # Keep the headline right after the name, as in the original cv.yaml.
    cv = {}
    for key, value in base_cv.items():
        cv[key] = value
        if key == "name":
            cv["headline"] = variant.get("headline")
    cv.setdefault("headline", variant.get("headline"))

    projects = build_projects(variant_name, variant, project_sets)

    sections = {"summary": variant["summary"]}
    for key, value in base_sections.items():
        if key == "experience":
            sections[key] = build_experience(variant_name, value, experience_sets)
            sections["projects"] = projects
        elif key == "skills":
            sections[key] = build_skills(variant_name, value, variant["skills_order"])
        else:
            sections[key] = [
                pick_highlights(entry, None) if isinstance(entry, dict) else entry
                for entry in value
            ]
    sections.setdefault("projects", projects)

    cv["sections"] = sections
    document["cv"] = cv
    return document


shared = {}

# Merge top-level files
for filename in SHARED_FILES:
    path = SRC / filename
    if not path.exists():
        fail(f"{path.relative_to(ROOT)} does not exist")
    shared.update(load_yaml(path))

variant_paths = sorted(VARIANTS_DIR.glob("*.yaml"))
if not variant_paths:
    fail(f"no variants found in {VARIANTS_DIR.relative_to(ROOT)}")

# Build everything first so a broken variant leaves no partial output.
documents = {
    path.stem: build_variant(path.stem, load_yaml(path), shared)
    for path in variant_paths
}

# Remove output from variants that no longer exist.
for old in SRC.glob("cv.*.generated.yaml"):
    old.unlink()

for variant_name, document in documents.items():
    output = SRC / f"cv.{variant_name}.generated.yaml"
    with open(output, "w", encoding="utf-8") as f:
        yaml.dump(
            document,
            f,
            sort_keys=False,
            allow_unicode=True,
        )
    print(f"Generated {output}")

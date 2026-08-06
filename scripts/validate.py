#!/usr/bin/env python3
"""Dependency-free validation for the Agent Software Map repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "README.zh-CN.md",
    "SKILL.md",
    "LICENSE",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "asm-template.md",
    "examples/ASM-OBS-Studio.md",
    "evals/ASM-OBS-Test.md",
    "agents/openai.yaml",
    ".github/workflows/validate.yml",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_skill(errors: list[str]) -> None:
    path = ROOT / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md must start with valid YAML frontmatter")
        return

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            fail(errors, f"unsupported frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    if set(fields) != {"name", "description"}:
        fail(errors, "SKILL.md frontmatter must contain only name and description")
    name = fields.get("name", "")
    if name != "agent-software-map":
        fail(errors, "skill name must be agent-software-map")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(errors, "skill name must use lowercase hyphen-case")
    description = fields.get("description", "")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        fail(errors, "skill description is empty or invalid")


def validate_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            link = raw.split("#", 1)[0]
            if not link or re.match(r"^(?:https?://|mailto:)", link):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                fail(errors, f"broken link in {path.relative_to(ROOT)}: {raw}")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    if not errors:
        validate_skill(errors)
        validate_links(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Agent Software Map repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

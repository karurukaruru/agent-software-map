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
    "SKILL.zh-CN.md",
    "asm-template.md",
    "asm-template.zh-CN.md",
    "references/ASM-After-Effects.md",
    "LICENSE",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "agents/openai.yaml",
    ".github/workflows/validate.yml",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKILL_SECTIONS = (
    "# 0. Core design principles",
    "# 4. Important objects and relationships",
    "# 8. Observation methods",
    "# 10. Operational contracts",
    "# 13. Failure and recovery model",
    "# 20. Incremental updates",
)
ZH_SKILL_SECTIONS = (
    "# 0. 核心设计原则",
    "# 4. 软件主要操作对象及其关系",
    "# 8. 观察方式",
    "# 10. 操作契约",
    "# 13. 失败与恢复模型",
    "# 20. 增量更新",
)
TEMPLATE_SECTIONS = (
    "## 3. Important objects and relationships",
    "## 5. Key states and their effects",
    "## 7. Observation methods",
    "## 8. Control methods and selection rules",
    "## 9. High-value operational contracts",
    "## 12. Failure and recovery model",
    "## 15. High-value unknowns",
)
ZH_TEMPLATE_SECTIONS = (
    "## 3. 主要对象及关系",
    "## 5. 关键状态与状态影响",
    "## 7. 观察通道",
    "## 8. 控制通道与选择规则",
    "## 9. 高价值操作契约",
    "## 12. 失败与恢复模型",
    "## 15. 高价值未知项",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require_sections(
    errors: list[str], relative: str, headings: tuple[str, ...]
) -> None:
    text = read(relative)
    for heading in headings:
        if heading not in text:
            fail(errors, f"{relative} is missing a required section: {heading}")


def validate_skill(errors: list[str]) -> None:
    text = read("SKILL.md")
    if len(text.splitlines()) > 500:
        fail(errors, "SKILL.md exceeds the recommended 500-line progressive-disclosure limit")

    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md must start with valid YAML frontmatter")
        return

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            fail(errors, f"unsupported SKILL.md frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    if set(fields) != {"name", "description"}:
        fail(errors, "SKILL.md frontmatter must contain only name and description")
    if fields.get("name") != "agent-software-map":
        fail(errors, "skill name must be agent-software-map")
    description = fields.get("description", "")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        fail(errors, "skill description is empty or invalid")

    require_sections(errors, "SKILL.md", SKILL_SECTIONS)
    require_sections(errors, "SKILL.zh-CN.md", ZH_SKILL_SECTIONS)


def validate_templates(errors: list[str]) -> None:
    require_sections(errors, "asm-template.md", TEMPLATE_SECTIONS)
    require_sections(errors, "asm-template.zh-CN.md", ZH_TEMPLATE_SECTIONS)

    english = read("asm-template.md")
    for marker in ("verified", "documented", "inferred", "unknown", "unverified", "Idempotency"):
        if marker not in english:
            fail(errors, f"asm-template.md is missing a key term: {marker}")

    chinese = read("asm-template.zh-CN.md")
    for marker in ("已验证", "有文档依据", "推断", "未知", "结果尚未验证", "幂等性"):
        if marker not in chinese:
            fail(errors, f"asm-template.zh-CN.md is missing a key term: {marker}")


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
        validate_templates(errors)
        validate_links(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Agent Software Map repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

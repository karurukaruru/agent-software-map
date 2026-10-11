# Agent Software Map

> Give an agent a map before it operates unfamiliar software.

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/specification)
[![Validate](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml/badge.svg)](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v1.0.0-blue)](#project-status)

[中文说明](README.zh-CN.md)

## What is an Agent Software Map?

An Agent Software Map (ASM) is a structured Markdown file that gives an agent the operational knowledge it needs before working with a specific software application.

It is not a software encyclopedia or a rewritten user manual. An ASM focuses on information that materially changes execution quality: how to identify the correct object, observe important state, choose an appropriate control method, verify the real result, and recover from failure.

```text
[User Task]
  -> Identify Software / Version / Environment
  -> Resolve Object + inspect decision-relevant State
  -> Find the matching ASM
  -> Load the minimum relevant Context
  -> Choose Capability + Observation / Control methods
  -> Preflight Target / State / Risk
  -> Execute
  -> Verify the real Software State
       ├─ Success --------------------------> Complete
       ├─ Partial completion / Unverified --+
       └─ Failure --------------------------+-> Re-observe State
                                                -> Recover / Switch method / Ask user

[Knowledge gap or observed conflict]
  -> Check Sources
  -> Observation
  -> Controlled probe, only when necessary and safe
  -> Label Evidence: verified / documented / inferred / unknown
  -> Incrementally update ASM
  -> Resume the runtime Workflow and verify again
```

The goal is not to eliminate exploration. It is to avoid making every agent rediscover the same operational facts through trial and error.

## Quick start

Install the repository as an Agent Skill:

```bash
# OpenAI Codex
git clone https://github.com/karurukaruru/agent-software-map.git ~/.codex/skills/agent-software-map

# Claude Code
git clone https://github.com/karurukaruru/agent-software-map.git ~/.claude/skills/agent-software-map
```

Then provide the target software, version, platform, and any material you already have:

```text
Use $agent-software-map to create an ASM for Adobe After Effects on Windows.
Use the files I provided first. Mark uncertain claims as unknown, and do not invent menus, parameters, APIs, paths, errors, or success states.
```

Generated maps use the following name:

```text
ASM-<Software-Name>.md
```

## What an ASM records

Depending on the software and task, an ASM may include:

- Identity, version, environment, scope, and boundaries.
- Sources, evidence levels, and validation status.
- Important objects, relationships, and stable addressing methods.
- States that change what the agent should do next.
- A capability tree organized around user goals.
- Observation and control methods, with selection rules.
- Operational contracts for high-value or failure-prone actions.
- Real success checks, partial-completion checks, and unverified outcomes.
- Failure signals, recovery, retry safety, side effects, and safety boundaries.
- Version differences, high-value unknowns, and incremental updates.

Not every ASM needs every section. Effective knowledge density matters more than document length.

## Reference implementation

[Adobe After Effects ASM](references/ASM-After-Effects.md) is the first full reference included in this repository. It demonstrates object modeling, state checks, execution choices, operational contracts, result verification, failure recovery, and explicit unknowns.

Claims inside a reference ASM must keep their evidence labels. Documentation-based or inferred behavior must not be presented as live-tested behavior.

## Optional template

The [English template](asm-template.md) and [Chinese template](asm-template.zh-CN.md) are optional checklists. They can help start a new map, but they are not a schema that must be filled mechanically. In many cases, working directly from [the Skill](SKILL.md) and the available evidence produces a better ASM.

## Core principles

- Prefer user-provided files, screenshots, recordings, projects, and constraints.
- Record information that reduces wrong-object edits, state mistakes, tool misuse, false success reports, or unsafe retries.
- If critical state is unknown, observe before acting.
- Do not treat a successful tool response or completed click as proof that the task succeeded.
- After a failure, inspect the real state before retrying.
- Prefer minimal edits to existing user data and establish a recovery point before irreversible actions.
- Preserve version and environment boundaries. Do not generalize a local observation without evidence.
- Update an ASM incrementally when real operation reveals reusable knowledge.

The complete design rules are in [SKILL.md](SKILL.md). The original Chinese design master is preserved in [SKILL.zh-CN.md](SKILL.zh-CN.md).

## Repository structure

```text
.
├── SKILL.md / SKILL.zh-CN.md
├── asm-template.md / asm-template.zh-CN.md
├── references/
│   ├── ASM-After-Effects.md
│   └── workflows/ (14 task-specific cards + index)
├── scripts/validate.py
├── agents/openai.yaml
├── .github/
├── README.md / README.zh-CN.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── LICENSE
```

## Publishing the Skill

Before publishing or installing the repository as a Skill, check the current [Agent Skills specification](https://agentskills.io/specification) and the following repository-specific items:

- Keep `SKILL.md` at the Skill root. Its YAML frontmatter is the discovery and triggering entry point; `description` should state both what the Skill does and when an Agent should load it.
- Keep `name` equal to the parent directory name. It must be 1–64 characters, use lowercase letters, numbers, and hyphens only, and contain no leading, trailing, or consecutive hyphens.
- Use `agent-software-map` as the repository and installed folder name. Avoid an extra nested directory such as `.../skills/agent-software-map/agent-software-map/SKILL.md`.
- Commit text as UTF-8 with LF line endings. This repository's `.gitattributes` already defines the expected normalization.
- Keep the Skill self-contained. Commit every local file referenced by a Markdown link, and use relative links so the Skill also works after cloning into an Agent's Skill directory.
- Follow progressive disclosure: keep the main `SKILL.md` below the recommended 500 lines and roughly 5,000 tokens, and move detailed material to focused `references/`, `scripts/`, or `assets/` resources loaded on demand. This repository's English entry is currently about 400 lines.
- Keep file references shallow—prefer files directly under `references/`, `scripts/`, or `assets/` rather than chains of nested references.
- Remove credentials, tokens, private paths, personal recordings, customer data, and unpublished licensed material before upload.
- Preserve evidence labels. A documented or inferred claim must not be presented as a live-tested result.
- Run `python scripts/validate.py` from the repository root before committing or tagging a release.

Evaluation results should include their task, model, environment, initial state, permissions, validity rules, and observable outcomes. This repository does not make a performance claim until those results are published with enough context to interpret them.

The After Effects map now includes [14 focused PV workflow cards](references/workflows/README.md). They cover typography, illustration rigs, cameras, shapes, compositing, and delivery. Recipes and parameter examples require validation in the target environment; this update does not include an AE runtime test.

## Project status

`v1.0.0` is the first public release of the current ASM design. The format is usable, but individual maps still need evidence appropriate to their target software version and environment. A map is not validated merely because it follows the structure.

## Contributing and security

Corrections from real software use are especially valuable. See [CONTRIBUTING.md](CONTRIBUTING.md). Report sensitive issues according to [SECURITY.md](SECURITY.md), not in a public issue.

## License

Agent Software Map is released under the [MIT License](LICENSE). Software, plugins, and adapters described by reference maps belong to their respective owners; this repository does not include their source code or licensed content.

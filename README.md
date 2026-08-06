# Agent Software Map

> Give AI agents a map before they operate unfamiliar software.

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/specification)
[![Validate](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml/badge.svg)](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.1.0%20candidate-orange)](#project-status)

[中文说明](README.zh-CN.md)

## The problem

An agent may be able to click, type, and call tools without understanding the software in front of it. That often leads to blind exploration, repeated actions, incorrect state assumptions, and unsafe guesses.

An **Agent Software Map (ASM)** is a structured Markdown file that gives the agent software-specific operational knowledge before it acts.

| Without an ASM | With an ASM |
|---|---|
| Rediscovers menus and object relationships | Starts with a capability map |
| Guesses whether an action succeeded | Checks observable success conditions |
| Misses state traps and destructive effects | Receives safety boundaries and recovery notes |
| Treats documentation as tested behavior | Tracks documented, verified, and inferred claims separately |

## Quick start

Install this repository as an Agent Skill:

```bash
# Claude Code
git clone https://github.com/karurukaruru/agent-software-map.git ~/.claude/skills/agent-software-map

# OpenAI Codex
git clone https://github.com/karurukaruru/agent-software-map.git ~/.codex/skills/agent-software-map
```

Then ask:

```text
Use $agent-software-map to create an ASM for OBS Studio.
```

The recognized Agent Skills entry point is the required file [`SKILL.md`](SKILL.md). Generated maps use names such as `ASM-OBS-Studio.md`.

## What an ASM contains

Every map has four sections:

1. **Identity** — software, version, platform, scope, and confidence.
2. **Sources** — evidence, with user-provided material first.
3. **Capability tree** — stable objects and workflows down to actionable leaves.
4. **Function cards** — purpose, entry point, procedure, success check, and operational patches.

Operational patches capture the details most likely to decide whether an agent succeeds: state assumptions, version differences, destructive effects, naming rules, hidden dependencies, common mistakes, and recovery steps.

Start from the [English template](asm-template.md) or [Chinese template](asm-template.zh-CN.md). You can also attach an existing `ASM-<Software>.md` directly before asking an agent to operate that software.

## OBS example and case study

- [OBS Studio ASM](examples/ASM-OBS-Studio.md) ([中文](examples/ASM-OBS-Studio.zh-CN.md))
- [OBS case-study protocol](evals/ASM-OBS-Test.md) ([中文](evals/ASM-OBS-Test.zh-CN.md))

The OBS map is currently a documentation-based candidate for OBS Studio 32.2.1 and has not completed live validation on the target machine.

Two attempted comparison runs were interrupted before completion: one by provider quota exhaustion and one by an API failure. The author manually counted 41 points at interruption in one run and roughly 40–50 in the other, but neither value is a final score. They are excluded from results and must not be used to claim an improvement.

## Evaluation rules

- Keep model, task, machine, initial state, time limit, tools, and permission mode constant.
- Use fresh sessions for baseline and ASM-assisted conditions.
- Discard runs interrupted by quota, API, network, or machine failure.
- Score only observable completed requirements.
- With one valid run per condition, call the result a **case study**, not a benchmark.
- Publish ties, regressions, and incomplete results honestly.

## Repository layout

```text
.
├── SKILL.md                   # Required Agent Skills entry point
├── agents/openai.yaml         # Codex UI metadata
├── asm-template.md            # English output template
├── asm-template.zh-CN.md      # Chinese output template
├── examples/                  # Completed software maps
├── evals/                     # Reproducible case-study protocols
├── scripts/validate.py        # Dependency-free repository checks
├── README.md / README.zh-CN.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE
```

## Project status

`v0.1.0` candidate includes the format, generator skill, bilingual templates, one documentation-based OBS example, and a controlled evaluation protocol. A public release tag and valid completed OBS comparison are still pending.

## Contributing and security

Corrections from real software use are especially valuable. See [CONTRIBUTING.md](CONTRIBUTING.md). Report sensitive problems according to [SECURITY.md](SECURITY.md), not in a public issue.

## License

Agent Software Map is released under the [MIT License](LICENSE). OBS Studio is a separate project licensed under GPL-2.0-or-later; this repository does not contain OBS source code.

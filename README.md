# Agent Software Map

> Give agents a map before they operate unfamiliar software.

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/specification)
[![Validate](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml/badge.svg)](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.0.0%20experimental-orange)](#project-status)

[中文说明](README.zh-CN.md)

## What Is an Agent Software Map?

An **ASM (Agent Software Map)** is a structured Markdown file that gives an agent the software-specific operational knowledge it needs before taking action.

  [Target Software]
        |
        v
[Confirm Software Details] -> [Gather Information] -> [Build Capability Tree] -> [Document Functions] -> [Validate] -> [Generate ASM]
                                                                                                                    |
                                                                                                                    v
                                                                                                         ASM-OBS-Studio.md
                                                                                                                    |
                                                                                                                    v
                                                                                                        [Operate / Test]
                                                                                                                    |
                                                                                                                    v
                                                                                                       Real-World Feedback
                                                                                                                    |
                                                                                                                    +----> Update ASM

## Quick Start

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

Generated ASMs use names such as `ASM-OBS-Studio.md`.

## What an ASM Contains

Every ASM has four parts:

1. **Identity** — software, version, platform, scope, and confidence.
2. **Information sources** — supporting evidence, with user-provided material listed first.
3. **Capability tree** — stable objects and workflows expanded down to actionable leaves.
4. **Functions** — purpose, entry point, steps, success criteria, and operational patches.

Operational patches capture the details most likely to affect an agent's work: state, version differences, destructive effects, naming rules, hidden dependencies, common mistakes, and recovery methods.

Start from the [English template](asm-template.md) or [Chinese template](asm-template.zh-CN.md). You can also give an agent an existing `ASM-<Software>.md` before it operates the software.

## OBS Example and Case Study

- [OBS Studio ASM](examples/ASM-OBS-Studio.md) ([中文](examples/ASM-OBS-Studio.zh-CN.md))
- [OBS case-study protocol](evals/ASM-OBS-Test.md) ([中文](evals/ASM-OBS-Test.zh-CN.md))

The OBS map is currently a documentation-based candidate for OBS Studio 32.2.1 and has not yet been tested on the target computer.

August 6, 2026

Neither comparison attempt was completed. One stopped when the provider quota ran out, and the other stopped because of an API error. The author manually counted 41 points at interruption in one attempt and approximately 40–50 points in the other. Neither is a final score. Both must be excluded from the results and must not be used to claim an improvement.

## Evaluation Rules

- Keep the model, task, computer, initial state, time limit, tools, and permission mode the same.
- Use fresh sessions for the baseline and ASM-assisted conditions.
- Discard runs interrupted by quota, API, network, or computer failure.
- Score only directly observable completed items.
- With only one valid run per condition, describe the result as a **case study**, not a benchmark.
- Report ties, regressions, and incomplete results honestly.

## Repository Layout

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

## Project Status

`v0.0.0` is an experimental preview that includes the format, generator Skill, English and Chinese templates, a documentation-based OBS example, and a controlled evaluation protocol. The format may still change, and a valid completed OBS comparison is still pending.

## Contributing and Security

Corrections based on real-world use are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Report sensitive security issues according to [SECURITY.md](SECURITY.md), not in a public issue.

## License

Agent Software Map is available under the [MIT License](LICENSE). OBS Studio is a separate project licensed under GPL-2.0-or-later; this repository does not contain OBS source code.

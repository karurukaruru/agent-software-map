# Agent Software Map

> Give an agent a map before it operates unfamiliar software.

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/specification)
[![Validate](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml/badge.svg)](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.0.0%20experimental-orange)](#project-status)

[中文说明](README.zh-CN.md)

## What Is an Agent Software Map?
An ASM (Agent Software Map) is a structured Markdown file that provides an agent with operational knowledge about a specific software application before the agent begins interacting with it.


Install this repository as an Agent Skill:
[Target Software]
        |
        v
[Identify Software] -> [Collect Sources] -> [Build Capability Tree] -> [Document Functions] -> [Validate] -> [Generate ASM]
                                                                                                           |
                                                                                                           v
                                                                                              ASM-OBS-Studio.md
                                                                                                           |
                                                                                                           v
                                                                                               [Execution / Testing]
                                                                                                           |
                                                                                                           v
                                                                                                  Execution Feedback
                                                                                                           |
                                                                                                           +----> Update ASM
```bash
# Claude Code
git clone https://github.com/karurukaruru/agent-software-map.git ~/.claude/skills/agent-software-map

# OpenAI Codex
git clone https://github.com/karurukaruru/agent-software-map.git ~/.codex/skills/agent-software-map
```

Then submit a request such as:

```text
Use $agent-software-map to create an ASM for OBS Studio.
```

The recognized Agent Skills entry point is the required file [`SKILL.md`](SKILL.md). Generated maps use names such as `ASM-OBS-Studio.md`.

##What Does an ASM Contain?

Each ASM contains four main sections:

Identity — software name, version, platform, scope, and confidence level.

Sources — supporting evidence, with user-provided materials listed first.

Capability Tree — a hierarchical model that expands stable objects and workflows into executable leaf nodes.

Functions — purpose, entry point, procedure, success checks, and operation patches.

Operation patches capture details that are most likely to affect an agent's ability to operate the software correctly, including state-dependent behavior, version differences, destructive effects, naming rules, hidden dependencies, common errors, and recovery procedures.

Start from the [English template](asm-template.md) or [Chinese template](asm-template.zh-CN.md). You can also attach an existing `ASM-<Software>.md` directly before asking an agent to operate that software.

## OBS example and case study

- [OBS Studio ASM](examples/ASM-OBS-Studio.md) ([中文](examples/ASM-OBS-Studio.zh-CN.md))
- [OBS case-study protocol](evals/ASM-OBS-Test.md) ([中文](evals/ASM-OBS-Test.zh-CN.md))

The OBS map is currently a documentation-based candidate for OBS Studio 32.2.1 and has not completed live validation on the target machine.

Two attempted comparison runs were interrupted before completion: one by provider quota exhaustion and one by an API failure. The author manually counted 41 points at interruption in one run and roughly 40–50 in the other, but neither value is a final score. They are excluded from results and must not be used to claim an improvement.

##August 6, 2026 Test Attempt

Neither of the two controlled comparison runs was completed. One run was interrupted because the service provider's quota was exhausted, and the other was interrupted by an API error.

At the time of interruption, the author manually estimated one run at 41 points and the other at approximately 40–50 points. These are not final scores. They must be excluded from the results and must not be used to claim that the ASM improved performance.

Evaluation Rules

Keep the model, task, computer, initial state, time limit, tools, and permission mode identical across conditions.

Use a fresh session for both the baseline condition and the ASM-assisted condition.

Invalidate any run interrupted by quota limits, API errors, network failures, or computer failures.

Score only completion criteria that can be directly observed.

When only one valid run exists for each condition, describe the result as a case test, not a benchmark.

Publish ties, regressions, and incomplete results honestly.

Project Structure
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

`v0.0.0` is an experimental preview. It includes the format, generator skill, bilingual templates, one documentation-based OBS example, and a controlled evaluation protocol. The format may change, and a valid completed OBS comparison is still pending.

## Contributing and security

Corrections from real software use are especially valuable. See [CONTRIBUTING.md](CONTRIBUTING.md). Report sensitive problems according to [SECURITY.md](SECURITY.md), not in a public issue.

## License

Agent Software Map is released under the [MIT License](LICENSE). OBS Studio is a separate project licensed under GPL-2.0-or-later; this repository does not contain OBS source code.

# Agent Software Map

> 让 Agent 在操作陌生软件前先拿到一张地图。

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/specification)
[![Validate](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml/badge.svg)](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v1.0.0-blue)](#项目状态)

[English](README.md)

## 什么是 Agent Software Map

Agent Software Map（ASM）是一份结构化 Markdown 文件，在 Agent 操作特定软件前提供真正影响执行结果的操作知识。

它不是软件百科，也不是重新整理一遍用户手册。ASM 关注的是：怎样找到正确对象、怎样看清关键状态、怎样选择合适的操作方式、怎样验证真实结果，以及失败后怎样恢复。

```text
[User Task]
  -> 识别 Software / Version / Environment
  -> 定位 Object + 检查影响决策的 State
  -> 查找匹配的 ASM
  -> 只加载当前任务需要的 Context
  -> 选择 Capability + Observation / Control 方式
  -> Preflight Target / State / Risk
  -> Execute
  -> 验证真实 Software State
       ├─ Success --------------------------> Complete
       ├─ Partial completion / Unverified --+
       └─ Failure --------------------------+-> 重新 Observation
                                                -> Recover / 切换方式 / 请求用户介入

[Knowledge gap 或实际行为与 ASM 冲突]
  -> 检查 Sources
  -> Observation
  -> 仅在必要且安全时进行 Controlled probe
  -> 标记 Evidence：verified / documented / inferred / unknown
  -> 增量更新 ASM
  -> 回到 Runtime Workflow 并再次 Verify
```

ASM 的目标不是消灭探索，而是不让每个 Agent 都用重复试错重新发现同一批操作知识。

## 快速开始

把仓库安装为 Agent Skill：

```bash
# OpenAI Codex
git clone https://github.com/karurukaruru/agent-software-map.git ~/.codex/skills/agent-software-map

# Claude Code
git clone https://github.com/karurukaruru/agent-software-map.git ~/.claude/skills/agent-software-map
```

然后提供目标软件、版本、平台和已有材料，例如：

```text
使用 $agent-software-map，为 Windows 上的 Adobe After Effects 创建一份 ASM。
先使用我提供的文件；不能确认的内容标记为未知，不要编造菜单、参数、API、路径、错误信息或成功状态。
```

生成文件统一命名为：

```text
ASM-<Software-Name>.md
```

## ASM 记录什么

根据软件和任务，一份 ASM 可以包含：

- 软件身份、版本、环境、范围与边界。
- 来源、证据等级与验证状态。
- 重要对象、对象关系和稳定定位方法。
- 会改变下一步决策的关键状态。
- 围绕用户目标组织的能力树。
- 观察方式、操作方式与选择规则。
- 高价值或容易失败动作的操作契约。
- 真实成功检查、部分完成判断和尚未验证结果。
- 失败特征、恢复、重试安全、副作用和安全边界。
- 版本差异、高价值未知项和增量更新记录。

不是每份 ASM 都需要填满全部章节。有效知识密度比文件长度更重要。

## 参考实现

[Adobe After Effects ASM](references/ASM-After-Effects.md) 是仓库当前的完整参考实现，展示了对象模型、状态检查、操作选择、操作契约、结果验证、失败恢复和未知项的写法。

参考 ASM 中的结论必须保留证据标记。仅有文档依据或推断的内容，不能写成已经在真实软件中验证。

## 可选模板

[中文模板](asm-template.zh-CN.md)和[英文模板](asm-template.md)只是可选检查清单，不是必须机械填满的格式。很多情况下，直接依据 [Skill](SKILL.zh-CN.md) 和已有证据创建 ASM 会更合适。

## 核心原则

- 优先使用用户提供的文件、截图、录像、项目和约束。
- 只记录能减少错对象、状态误判、工具误选、成功误报或危险重试的信息。
- 关键状态未知时先观察，再操作。
- 工具返回成功或 GUI 点击完成，不等于任务已经成功。
- 第一次失败后先检查真实状态，不无条件重试。
- 修改用户已有数据时优先最小修改；不可逆动作前建立恢复点。
- 保留版本和环境边界，不把局部观察无证据地推广为通用规则。
- 真实操作发现可复用的新知识后，局部更新 ASM。

完整中文设计规则见 [SKILL.zh-CN.md](SKILL.zh-CN.md)。Agent Skill 的标准入口是 [SKILL.md](SKILL.md)。

## 仓库结构

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

## Skill 上传注意事项

把仓库上传或安装为 Skill 前，先核对当前 [Agent Skills specification](https://agentskills.io/specification)，再检查以下仓库事项：

- `SKILL.md` 必须位于 Skill 根目录。YAML frontmatter 是 Skill 的发现与触发入口；`description` 应同时说明 Skill 能做什么，以及 Agent 什么时候应加载它。
- `name` 必须与父目录名称一致，长度为 1–64 个字符，只能使用小写英文字母、数字和连字符，不能以连字符开头或结尾，也不能出现连续连字符。
- 仓库名和安装目录统一使用 `agent-software-map`。不要形成 `.../skills/agent-software-map/agent-software-map/SKILL.md` 这种多套一层的目录。
- 文本文件使用 UTF-8 和 LF。仓库中的 `.gitattributes` 已规定标准化方式。
- Skill 应能够独立使用。Markdown 链接引用的本地文件必须一并提交，并尽量使用相对链接，保证 clone 到 Agent 的 Skill 目录后仍然有效。
- 使用 progressive disclosure：主 `SKILL.md` 建议低于 500 行、约 5,000 tokens；详细内容放入按需加载的 `references/`、`scripts/` 或 `assets/`。当前英文入口约 400 行。
- 文件引用尽量保持一层深度，优先直接引用 `references/`、`scripts/` 或 `assets/` 下的文件，不建立多层 Reference 链。
- 上传前移除 credential、token、私有路径、个人录屏、客户数据和未获许可的材料。
- 保留 Evidence 等级。只有文档依据或推断的结论，不能写成已经完成 live test。
- commit 或创建 release tag 前，在仓库根目录运行 `python scripts/validate.py`。

实验结果应同时说明 Task、Model、Environment、Initial State、Permission、有效性规则和可观察结果。在这些信息完整公开前，本仓库不根据未完成或缺少上下文的结果宣称性能提升。

After Effects 地图新增 [14 张按需 PV 工作流卡片](references/workflows/README.md)，覆盖文字、插画、相机、图形、合成与交付。配方与示例参数仍需目标环境验证；本次更新没有执行 AE 实机测试。

## 项目状态

`v1.0.0` 是当前 ASM 设计的首次公开发布。格式已经可以使用，但每一份软件地图仍需要与目标软件版本和环境相符的证据。文件符合结构，不代表其中内容已经得到真实验证。

## 贡献与安全

真实软件操作中发现的修正尤其有价值，参见 [CONTRIBUTING.md](CONTRIBUTING.md)。敏感问题请按 [SECURITY.md](SECURITY.md) 私下报告，不要发到公开 Issue。

## 许可证

Agent Software Map 使用 [MIT License](LICENSE)。参考地图中描述的软件、插件和适配器属于各自权利人；本仓库不包含它们的源代码或授权内容。

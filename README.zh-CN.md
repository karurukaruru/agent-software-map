# Agent Software Map

> 让 AI 代理在操作陌生软件前先拿到一张地图。

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/specification)
[![Validate](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml/badge.svg)](https://github.com/karurukaruru/agent-software-map/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.0.0%20experimental-orange)](#项目状态)

[English](README.md)

## 要解决的问题

代理即使会点击、输入和调用工具，也不一定理解眼前的软件。结果往往是盲目探索、重复操作、错误判断状态，甚至做出不安全的猜测。

**ASM（Agent Software Map，代理软件地图）**是一份结构化 Markdown 文件，在代理行动前提供特定软件的操作知识。

| 没有 ASM | 有 ASM |
|---|---|
| 临时寻找菜单和对象关系 | 先读取能力地图 |
| 猜测操作是否成功 | 检查可观察的成功条件 |
| 忽略状态陷阱和破坏性影响 | 获得安全边界与恢复说明 |
| 把文档内容当成实测结果 | 区分“有文档依据、已验证、推断” |

## 快速开始

把本仓库安装为 Agent Skill：

```bash
# Claude Code
git clone https://github.com/karurukaruru/agent-software-map.git ~/.claude/skills/agent-software-map

# OpenAI Codex
git clone https://github.com/karurukaruru/agent-software-map.git ~/.codex/skills/agent-software-map
```

然后提出请求：

```text
使用 $agent-software-map 为 OBS Studio 创建一份 ASM。
```

Agent Skills 规范要求的识别入口是 [`SKILL.md`](SKILL.md)，不能改成 `ASM.md`。生成出来的软件地图则采用 `ASM-OBS-Studio.md` 这样的名称。

## ASM 包含什么

每份地图包含四部分：

1. **身份**——软件、版本、平台、范围和置信度。
2. **来源**——证据，用户提供的资料排在最前。
3. **能力树**——从稳定对象和工作流展开到可执行叶节点。
4. **功能卡片**——作用、入口、步骤、成功检查和操作补丁。

操作补丁记录最可能影响代理成败的细节：状态假设、版本差异、破坏性影响、命名规则、隐藏依赖、常见错误和恢复方法。

可以从[英文模板](asm-template.md)或[中文模板](asm-template.zh-CN.md)开始，也可以在操作软件前直接把已有的 `ASM-<软件>.md` 提供给代理。

## OBS 示例与案例测试

- [OBS Studio ASM 中文版](examples/ASM-OBS-Studio.zh-CN.md)（[English](examples/ASM-OBS-Studio.md)）
- [OBS 案例测试协议](evals/ASM-OBS-Test.zh-CN.md)（[English](evals/ASM-OBS-Test.md)）

OBS 地图目前是面向 OBS Studio 32.2.1、基于官方文档整理的候选版，尚未在目标电脑完成真实操作验证。

今天两次对照尝试都没有完成：一次因服务商额度耗尽中断，另一次因 API 报错中断。作者在中断时人工统计，一次为 41 分，另一次约为 40–50 分；两者都不是最终分数，必须从结果中排除，也不能用于宣称效果提升。

## 评测规则

- 模型、任务、电脑、初始状态、时间限制、工具和权限模式保持一致。
- 基线组与 ASM 组使用全新会话。
- 因额度、API、网络或电脑故障中断的运行作废。
- 只评分可以直接观察到的完成项。
- 每种条件只有一次有效运行时，只能称为**案例测试**，不能称为 benchmark。
- 平局、退步和未完成结果也应如实发布。

## 项目结构

```text
.
├── SKILL.md                   # Agent Skills 必需入口
├── agents/openai.yaml         # Codex 界面元数据
├── asm-template.md            # 英文输出模板
├── asm-template.zh-CN.md      # 中文输出模板
├── examples/                  # 已完成的软件地图
├── evals/                     # 可复现案例测试协议
├── scripts/validate.py        # 无第三方依赖的仓库检查
├── README.md / README.zh-CN.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE
```

## 项目状态

`v0.0.0` 是实验性预览版，已经包含格式、生成 Skill、中英文模板、一个基于文档的 OBS 示例和受控测试协议。格式仍可能变化，有效完成的 OBS 对照结果也仍待补充。

## 贡献与安全

欢迎提交真实操作中发现的界面差异和修正，参见 [CONTRIBUTING.md](CONTRIBUTING.md)。敏感安全问题请按 [SECURITY.md](SECURITY.md) 处理，不要发到公开 Issue。

## 许可证

Agent Software Map 使用 [MIT License](LICENSE)。OBS Studio 是使用 GPL-2.0-or-later 的独立项目；本仓库不包含 OBS 源码。

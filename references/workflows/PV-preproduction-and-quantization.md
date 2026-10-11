# After Effects PV 前期准备与分镜量化

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：动态歌词 PV、音乐视觉、音 MAD、角色介绍 PV，或任何含音频、歌词、分镜和多个段落的 AE 任务。
>
> 加载方式：与 `../ASM-After-Effects.md` 的身份、状态、控制通道、操作契约、UNKNOWN 恢复和安全规则一起使用；本卡不替代主 ASM。
>

## 1. 证据与边界

- `[推断]`：候选制作流程展示的候选 AE 操作；需按目标 AE build、OS、UI language 与控制通道复核。
- `[设计候选]`：候选流程中的工作流经验或默认组织方式；用户既有流程优先。
- `[待验证]`：菜单、导入行为或环境差异仍需 feature probe。
- 快捷键只描述默认/示例路径。执行 GUI 前读取实际 Keyboard Shortcuts；结构化通道可直接修改 DOM，不必模拟按键。

## 2. 输入审计

在创建 Comp 或批量 mutation 前建立任务 manifest：

| 输入 | 最少记录 | 阻塞条件 |
|---|---|---|
| 音频 | 文件 identity、时长、采样范围、许可状态。 | 缺定稿版本或目标时段不明。 |
| 歌词/字幕 | 文本版本、语言、时间信息、允许改写范围。 | 内容或使用权不明；不得自行补歌词。 |
| 分镜/参考 | 文件 identity、时间基准、只读参考方式。 | 依赖分镜但无法读取或时间基准不明。 |
| 角色/PSD/图片 | 文件、层结构预期、许可、是否允许切层/替换。 | 需破坏性改源文件且无副本。 |
| 字体/效果/插件 | 允许清单、安装状态、替代策略。 | 仅当用户要求必须一致且依赖缺失时阻塞。 |
| 输出 | width/height、fps、duration、音频、codec/container、路径与覆盖策略。 | 目标规格或覆盖授权不明。 |

先核对输入存在性、可读性和版本，再进入制作。模板、插件和参考不能扩大用户已授权的资产范围。[设计候选]

## 3. Transform 与时间线短契约

这些规则只在 GUI 路径或解释用户快捷键意图时使用；实际写入仍遵守主 ASM 9.4 的稳定 Property path、before/after 回读与时间量化。

| 意图 | 候选路径 | 执行规则与验证 | 证据 |
|---|---|---|---|
| Position | `P` | 读取 `ADBE Position`、value type、keys/expression；写后核对 keyTime/keyValue。 | `[推断]` |
| Scale | `S` | 百分比值围绕 Anchor 生效；先确认 2D/3D 维度和 Anchor。 | `[推断]` |
| Rotation | `R` | 围绕 Anchor 旋转；不要把示例 UI 的圈数/角度显示当通用数据格式。 | `[推断]` |
| Opacity | `T` | 0–100 的淡入淡出是候选低复杂度路径；写后检查可读停留和遮挡。 | `[推断]` |
| Anchor Point | `A` | 改 Anchor 会改变内容相对锚点及后续 Scale/Rotation 参考中心；必须加视觉采样。 | `[推断]` |
| 移动 layer in point 到 CTI | `[` | 修改前后回读 in/out/startTime；若本机绑定不同，走菜单/脚本。 | `[推断]` |
| 移动 layer out point 到 CTI | `]` | 同上；不得生成 `outPoint <= inPoint`。 | `[推断]` |
| 修剪 CTI 左侧/右侧 | `Alt+[` / `Alt+]` | 修改已有 timing；先快照，写后核对保留区间及关键事件。 | `[推断]` |
| 在 CTI 拆分 layer | `Ctrl+Shift+D` | 非幂等；先查同 source 的相邻边界是否已存在；写后核对 layer count、两层 source 与 in/out。 | `[推断]` |

对围绕底边增长、门轴旋转、相框弹出等动画，先设置并验证 Anchor，再写 Scale/Rotation keys。若 timeout，先按 layer ID/source/timing 判断是否已修改或拆分，禁止原样重试。

## 4. GUI 工作区准备与恢复

仅在任务依赖 GUI 时读取 `workspace_ready`：[推断]

- 当前工作区名称已知；Project、Composition/Layer 与 Timeline 可见。
- 任务需要时，Align/Paragraph 可见；不自动关闭用户其他面板。
- 时间线需要能观察目标层、CTI、in/out 和关键帧；“把时间线做得很大”只是示例偏好。
- 候选流程采用 `Window > Workspace > Save as New Workspace` 与 `Reset to Saved Layout`；菜单文字/位置需在目标 build、本地化界面 probe。
- 界面失序时优先保存当前项目状态，再重置到用户已保存布局；不得覆盖用户唯一工作区或强行模仿示例布局。
- Motion Tools、MultiEase、Baramoji、FastShape、TextEvo、Notepad 等均为可选面板。先探测，缺失时使用 AE 内置能力或省略，不得阻塞基础流程。[设计候选]

## 5. PV 项目组织与模板

若用户没有既有规范，可建议以下语义目录；名称和编号均可替换：[设计候选]

```text
segments-or-comps/
artwork-and-audio/
components-or-precomps/
video-assets/
image-assets/
other/
```

规则：

1. 先读取现有 Project FolderItem 与引用；已有结构优先，不为套模板重排用户资产。
2. 新建前给目录写唯一 operation tag 或确认等价目录不存在。
3. 创建后按 FolderItem 类型、父路径、名称和成员回读；不得只看 Project 面板位置。
4. 候选流程采用“新项目加载模板”偏好设置；其菜单和行为为 `[推断]`，执行前运行 LP-03。
5. 模板只能含空目录、非敏感默认设置和明确允许复用的公开组件。禁止夹带素材、私有路径、字体/插件隐式依赖或凭证。
6. 模板不可用时，回退到 ID/tag 驱动的 JSX/MCP 创建空 FolderItem；不为修模板阻塞当前项目。

## 6. PSD 与参考资产导入

### 6.1 PSD 候选导入方式

候选为 `Composition - Retain Layer Sizes` + `Editable Layer Styles`。[推断]

前置：复制/只读保护原 PSD；记录 PSD identity、预期层数、AE build、UI language 与导入选项。

写后必须回读：

- 新建 Comp/Footage identity 与父目录；
- 层数、名称、source、bounds、Anchor；
- layer styles 是否存在且可编辑；
- 缺失字体/样式、合并层、异常 bounds 或离线 source。

只有结构和至少一个采样帧通过后，才能判定“适合分层动画”。LP-04 通过前不把菜单名或具体 PSD 行为标为 `[已验证]`。

### 6.2 只读参考通道

当任务依赖 storyboard/reference 时，建立至少一种明确来源：[推断]

- Layer Viewer；
- reference comp；
- 带时间戳的导出帧/contact sheet；
- 外部只读 manifest。

参考窗口只用于观察，不是对象定位真相源。用素材创建 Comp 后必须回读 duration、fps、pixelAspect、audio 和尺寸；不能因为拖放成功就假定时间基准正确。

## 7. 分镜量化工作流

目标：把长片拆成有边界、有复用关系、有验收状态的工作包，而不是复制示例成片。[设计候选]

```text
输入审计
-> 锁定 Main Comp 与 storyboard 时间基准
-> 识别镜头/段落边界
-> 建立 segment manifest
-> 用 markers 或专用覆盖条表达边界
-> 统计总段数、独立段数、复用映射
-> 为每段绑定目标 Comp 与变化项
-> 结构回读 + 采样帧
-> 再进入批量制作
```

推荐 manifest 字段：

```text
segment_id, in, out, storyboard_ref, target_comp_id,
reuse_of, allowed_changes, status, operation_id, review_notes
```

可选覆盖条方法：在 storyboard 上方创建带任务命名空间的 Shape Layer，并在边界拆分。[推断] 若已有 comp markers、外部 EDL/CSV 或更可靠结构，不必创建覆盖条。

状态建议：`未开始 -> 结构完成 -> 关键帧完成 -> 视觉待审 -> 测试渲染通过 -> 已交付`。[设计候选]

成功验证：

- 每段 `in < out`，相邻边界重叠/空隙符合 brief；
- manifest 总段数等于 markers/覆盖条表达的段数；
- 独立段与 `reuse_of` 映射无环且目标存在；
- 重复段明确允许变化的歌词、颜色、时长或局部元素；
- Comp 清单与 segment 状态一致；
- 关键边界两侧有采样帧，避免把同一镜头误拆或漏拆。

## 8. 幂等性、失败恢复与安全

- Folder/Comp/Layer 创建、duplicate、split、marker add 均不可盲重试；使用 operation ID、comment/tag、source/timing 指纹查重。
- 修剪与 source 替换会改已有用户数据；执行前保存检查点和 before snapshot。
- timeout 后先比较 item/layer count、IDs、in/out、markers 与 manifest；分类为未发生、成功、部分完成或 UNKNOWN。
- 部分完成时从最近一致的 segment 边界恢复，不从头重建所有段。
- 不下载、导入或复制未授权素材、字体、模板、歌词或插件。

## 9. 待验证项

- LP-01：Transform 快捷键、Property 与 Anchor 方向。
- LP-02：入出点、修剪、拆分及重复执行检测。
- LP-03：目标 AE build 的新项目模板加载。
- LP-04：指定 PSD 样例的导入结构。
- LP-05：segment manifest 与 AE markers/覆盖条的双向一致性。

全部通过标准见主 ASM 14.3；当前状态均为 `未执行`。

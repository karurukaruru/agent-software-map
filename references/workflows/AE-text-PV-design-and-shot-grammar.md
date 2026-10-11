# After Effects 文字 PV 设计与镜头语法

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：用户要求日系文字 PV、Vocaloid MV、Kinetic Typography，或只提供歌曲、歌词、插画和较宽泛的风格描述。
>

## 1. 证据与适用边界

- ``：字幕明确讲解 2D/3D、字体、文本属性、运动模糊、帧率、景深、Glow、实拍合成、Camera、Text Animator、Track Matte、Blend Mode、路径文字及多种效果。
- ``：其中一支视频抽样直接看到字体对比、24/4 fps 对比、文本/插画遮罩、路径文字、插件与噪声示例。
- ``：另一支视频抽样直接看到 2D/3D 对比、Camera/焦点示意、Shape 拆解、Luma Matte、素材插件、合成与统一滤镜示例。
- ``：用户对实作工程逐镜复盘并亲自校正后的偏好；仅在同一用户或明确启用配置时使用。
- ``：用户参考截图的结构观察；不授权复刻作品资产、字形或具体镜头。
- 示例作者的镜头、配色、字体、插画、角色和成片不是交付模板；学习的是决策关系与验证方法。
- 本卡不能把主观“好看”变成软件事实；结构可机器验证，画面风格必须人工 review。

## 2. 先决定表达系统，不先堆效果

每个段落先回答：

```text
这句歌词承担什么作用
-> 阅读优先还是情绪冲击优先
-> 文字与插画如何分区/重叠
-> 固定 2D、2.5D 视差，还是 3D+Camera
-> 入场、稳定可读、出场各占多少时间
-> 需要哪一种主运动、哪一种辅助质感
-> 如何与前后镜头建立视觉连续性
```

默认不允许同一镜头同时加入多个没有语义职责的效果。每个效果必须标记 `role`：`entry`、`readability`、`emphasis`、`transition`、`depth`、`texture` 或 `unification`。

## 3. Shot manifest

设计阶段先生成可审查 manifest，不直接进 AE：

```text
shot_id, time_in, time_out, lyric_id, semantic_role,
layout_mode, text_zone, subject_zone, overlap_rule,
font_role, font_candidates, text_attributes,
space_mode, camera_role, depth_plan,
entry, readable_hold, exit, transition_in, transition_out,
motion_blur_intent, temporal_style, effects[],
asset_ids[], adapter_preferences[], fallbacks[],
machine_checks[], human_review[], operation_id
```

要求：

- `lyric_id` 必须引用已确认歌词；不得自行改词。
- `font_candidates` 必须在目标机器检查可用性、授权和字形覆盖。
- `readable_hold` 优先满足阅读；装饰动画不得吞掉整句。
- `effects[]` 每项只有一个主要职责，并提供无插件 fallback。
- 用户给了明确逐镜设计时按用户设计执行；用户只给中等 brief 时先提交 manifest/contact sheet 供批准。

## 4. 2D、2.5D 与 3D+Camera 选择

| 模式 | 适用 | 代价/风险 | 最小验证 |
|---|---|---|---|
| 2D 固定视点 | 字体造型、平面排版、快速切镜、可读性优先 | 空间变化较少，需要靠文字层本身进退场 | Transform/Text Animator keys、bounds、可读时段 |
| 2.5D 视差 | 单图拆层、前中后景、轻微镜头运动 | 放大露底、边缘穿帮、层间深度不自然 | 分层边缘、工作区全程覆盖、三时点视差 |
| 3D+Camera | 穿梭、焦点转移、空间编排、文字沿 Z 展开 | Camera/焦点/景深复杂，错误时可读性下降 | active Camera、Z/parent、focus、前中后帧与露底 |

候选流程把“是否使用 Camera”作为开始前的重要分叉。 这不是强制使用 3D；如果情绪和阅读目标不需要深度，2D 是更稳妥的选择。

## 5. 字体与文本属性

### 5.1 字体角色

先定义角色，再选字体：`display`、`lyric_body`、`accent`、`annotation`。字体的历史分类或情绪标签只能作为候选，不是自动真理。

控制规则：

1. 检查语言覆盖、标点、假名/汉字/拉丁字母、字重和 variable axes。
2. 同一段默认限制主字体角色数量；新增字体必须有层级或语义理由。
3. 记录实际解析字体与 fallback；缺字不得静默替换。
4. 字体、字号、行距、tracking、方向、对齐、换行和 sourceRectAtTime 一并回读。

### 5.2 文本装饰

颜色、描边、阴影、Glow、混合模式服务于世界观和可读性。示例特别提醒装饰过多容易产生“电视字幕”感，而无装饰也可以成为设计选择。

- 先用字号、字重、明度、位置和留白建立层级，再加描边/阴影。
- 为可读性添加的效果必须做 `on/off` 对比；若画面世界观与可读性冲突，交给人工 reviewer 取舍。
- 不能把某一具体字体、描边宽度、Glow 数值写成日系 PV 默认。

### 5.3 文字载体与粒度选择

- 将主歌词、注释、装饰纹理分配不同职责；颜色、字号、字重与填充/描边服从当前 brief。
- 按节奏选择整行、词块、逐字或乐句分组；词内错帧与词间停顿分别记录，不把等间隔错帧当唯一方案。
- `TextLayer=0` 不等于画面无文字；继续检查 Shape 路径、AI/PSD/PNG 字形和预渲染视频。名称与路径复杂度只能辅助判断，需视觉确认。
- 仅烘焙字形可见时，原始字体、文字动画器和源 key 保持未知；保留可编辑文字源以便后续修改。

## 6. 文字与插画的空间合同

单图 + 歌词是“区域争夺”。可选布局：

1. **空间分区**：文字与主体分别占据不同区域。
2. **前后层次**：文字放主体后或前，使用 Alpha/Track Matte 保留人物轮廓。
3. **局部反差**：重叠区域切换填充/描边/阴影，但保持文字整体一致。
4. **Blend 实验**：Difference 等模式可制造交互色；必须验证背景变化时仍可读。
5. **路径文字**：文本沿 mask path，边距/Offset 驱动；逐字符闪烁可由 Text Animator 完成。

任何 matte/blend/path 修改后都要回读关系和属性，并在背景明暗变化、人物边缘和稳定阅读时段采样。复杂字形排布须人工检查。

## 7. 运动与时间质感

- Position、Scale、Rotation、Opacity 是整层基础；逐字符使用 Text Animator/Selector 或已验证 adapter。
- 慢速 zoom 或缓慢 Camera drift 可避免完全静止，但必须有边界和露底检查；不是每镜强制移动。
- Motion Blur 开/关是风格决定：逼真连续运动通常开启，插画/切帧感可关闭。
- Posterize Time/低 fps 用于有意的切帧或赛璐珞感；不得把主 Comp fps 随意改低。对目标层/预合成应用并回读作用范围。
- 手工逐帧或逐字 key 可提高针对性，但成本高；先在重点词/重拍使用，不把所有歌词都拆层。
- Echo、wiggle、残像和弹跳只作辅助质感；不得破坏阅读停留。

## 8. 插件是 adapter，不是能力定义

可选工具包括 Animation Composer、AEJuice、Deep Glow、Saber、Trapcode Form、Fast Chromatic Aberration、GG Decomposition、Newton 等。

执行顺序：

```text
先定义视觉职责
-> probe 插件/版本/参数树/授权
-> 可用：在独立测试层验证
-> 不可用：内置 Text Animator/Shape/Glow/通道偏移/手动 key fallback
-> 无等价 fallback：降级并说明，不自动安装
```

素材包/预设能节省时间，但必须核对许可证、来源、可编辑性和风格一致性。不得把插件示例资产当成用户项目素材。

## 9. 双层验收

机器检查：歌词、字体解析、timing、bounds、安全区、matte/blend/path 关系、Camera/parent/Z、effect stack、keys、工作区覆盖、测试渲染可解码。

人工检查：字形气质、主次层级、图文关系、阅读路径、动势、情绪、节奏、原创性、参考相似度与全片一致性。

## 10. 失败恢复

- brief 过泛：停止直接制作完整片，先交 3–5 个代表镜头的 manifest/style frame。
- 字体缺失/缺字：保留原文本与候选清单，请用户提供或批准替代。
- Camera 让文字难读：暂时旁路 Camera/DOF，恢复 2D readable baseline，再逐项加入深度。
- 插件错误：disable 最近 adapter，恢复 before stack，切换内置 fallback。
- timeout：按 operation tag、layer/effect/animator count、keys 和关系查重，不重放整段。

## 11. 待验证

- P0 TPV-DE-01：中等详细 brief → shot manifest → 人工批准。
- P0 AP-TX-01：TextDocument/Text Animator/Selector。
- P0 AP-MO-01：Transform keys/interpolation。
- P0 AP-3D-01：3D/Camera/Null/active Camera。
- P2 AP-PL-01：第三方插件 adapter。
- P2 AP-ST-01：日系文字 PV 人工视觉 rubric。

当前均为 `未执行`。

# After Effects 歌词文字动画

> 触发：歌词、字幕、标题或按字符进退场；尤其是 TextEvo/内置 Text Animator 选择。
>
> 验证状态：可复用候选配方；使用前需在目标 AE/控制通道验证。数值为示例起点，不是通用默认。
>


## 1. 证据与 adapter 顺序

- `[推断]`：示例展示的候选文字操作。
- `[推断]`：动画设计默认，可由 brief 覆盖。
- `[推断]`：TextEvo/Motion Tools、插件参数、字形行为与人工风格判断需 probe。
- ``：画面直接可见 AE 2026、TextEvo effect、Strength/Delay/Direction/From Index/Random Seed、Position/Scale/Opacity/Tracking 及同层多个 TextEvo 实例；不证明目标环境可用。

选择顺序：

```text
读取 TextLayer/TextDocument 与字体
-> 先选择 AE 内置 Text Animator + Selector
   -> 需要第三方能力时：probe TextEvo adapter
   -> 插件可用且任务匹配：在副本测试
   -> 结构化通道仍不支持：最小 Layer Transform 动画或请求人工
```

插件缺失不得阻塞 baseline，也不得虚构同名参数。

## 2. 歌词动画 manifest

每段文字至少记录：

```text
lyric_id, text, language, font/fallback, in, readable_until, out,
entry_adapter, exit_adapter, per_character, operation_id, review_notes
```

前置检查：文本内容和授权、语言/换行、字体可用性、TextDocument、sourceRectAtTime/bounds、safe area、layer in/out、markers、已有 animators/effects/keys/expression。

不得自行补写歌词；文字内容、时间和字体不明会直接影响交付时应请求用户确认。

## 3. 通用文字动画合同

### 最小写入

1. 按 TextLayer ID + lyric_id 定位；同 operation tag 已存在则复用/修改。
2. 先写并回读 TextDocument/字体/段落，再写动画。
3. Entry、readable hold、exit 分成明确时段；出场不能早于 `readable_until`。
4. 只添加实现 brief 所需的 Position/Scale/Opacity/Tracking；避免无目的堆叠。
5. 按帧量化 keys；同一时间已有等价 key 时不重复添加。

### 回读与验证

- TextDocument、字体实际解析、层 timing、animator/effect 实例树；
- key time/value/interpolation 或 selector/Strength 状态；
- 入场前、入场中、稳定可读、出场中、出场后采样；
- OCR/字符串核对、bounds、安全区、遮挡、字符重叠和可读停留；
- 中日韩混排、标点、竖排或复杂 shaping 必须实机/人工检查。

## 4. TextEvo adapter

TextEvo 是第三方 effect，不是 AE baseline。[推断]

### 前置

- 插件/adapter 版本、effect `matchName` 和实际参数树可读；
- 目标 TextLayer 唯一；现有 TextEvo 实例、名称、Strength keys 与 style 已快照；
- 进场/出场、按字符还是同步、偏移方向和可读时段已明确。

### 候选模型

- 示例以 Strength `100 -> 0` 表示从偏移状态回到原排版，`0 -> 100` 用于反向出场 `[推断]`；以目标插件候选为准。
- Position/Scale/Opacity/Tracking/Delay/Direction 等只能在参数树确认后写。
- 同层多实例时为实例命名/打 tag，例如 entry/opacity/exit，避免仅用 index。[推断]
- Toggle Hold、短 key 间距、逐字符 Delay 和预设保存均需 feature probe；预设不得写入未授权私有路径。

### 验证与恢复

- 回读实例数、名称/tag、Strength/Style/Delay 等参数及 keys；
- 采样确认红色辅助框/插件 UI 不是最终渲染内容；
- timeout 后查实例数和 tags，禁止再加一组 TextEvo；
- 插件错误或丢失时恢复 before effect stack，切换内置 Text Animator；
- Motion Tools Elastic 属双插件路径，缺任一项即降级。

## 5. 内置 Text Animator fallback

目标：用 AE 内置 Text Animator 的 Position/Scale/Opacity 等属性与 Selector 实现同步或逐字符动画。[推断]

1. 枚举目标 TextLayer 的现有 Animator/Selector tree，按 tag/name 消歧。
2. 不存在等价 animator 时才创建；添加结构后从 TextLayer 根重新取引用。
3. 添加所需动画属性，设置偏移状态；使用 Range Selector 的 Offset/Start/End 与 Advanced/Shape 控制范围和节奏。
4. 具体 matchName、selector 单位、Shape 和 based-on 选项必须由目标 AE DOM probe，不能从 GUI 文案猜。
5. 回读 animator/selector/属性/keys，采样逐字符次序、标点和换行。

若 adapter 不能结构化控制 Text Animator，但能精确控制 Layer Transform，降级为整层入退场并向用户说明不含逐字符效果。

## 6. 泛化决策层（让 Agent 自己设计，而非照抄）

给定一句**没见过的歌词**，Agent 不应只套 2D 词卡样板，而应按下面链条从已知锚点**推导合理变体**。锚点 = 候选示例；区间 = 推断（标注 `[推断]`）。

### 6.1 可调旋钮（从示例起点提炼）

| 旋钮 | 示例起点 | 可调方向（推断） |
|---|---|---|
| 错帧量 | 0.05s@60fps=3帧（词卡）；0.066s@30fps=2帧（3D标题） | 越大越"碎/抖/松"，越小越"齐/紧/稳"；配曲风选 |
| 闪烁次数 | 词卡 7keys=3次（`50→0→100→0→100→0→100`） | 0次=直接显现（冷静）；1次=单闪；3次=顿闪（凌厉打拍） |
| 入画方向 | 右上/左上都有（斜向是家族特征） | 斜向任何方向均可，选远离主体/留白的方向 |
| 字号 | 250px（大字卡）/131px（3D标题）/64px（字幕） | 由信息层级决定，见 6.2 |
| 位移插值 | BEZIER ~0.6s 缓落 | 该候选的位移使用 BEZIER 缓落；其他方案可选匀速或硬切 |
| 闪烁插值 | HOLD 硬切 | 闪烁永远硬切（HOLD），不缓变 |
| 时长 | 卡 0.85–1.72s（因句长） | 随句长/歌词密度 |

### 6.2 决策链（未知歌词 → motion plan）

1. **定信息层级** → 决定字号/结构：主歌词=大字词卡（250px 量级，逐字+描边孪生）；镜头内角色情绪字=3D 标题（~131px，逐字+描边）；说明/滚动=底部字幕（~64px+阴影）。
2. **定节奏** → 决定错帧量与闪烁次数：打拍/凌厉→多闪+短错帧；舒缓/叙事→少闪或无闪+BEZIER 缓落。
3. **定空间** → 决定入画方向：远离主体/往留白方向斜落。
4. 生成 motion plan（结构+参数+理由）给用户审查，再执行。

### 6.3 诚实边界

- 锚点之外的所有取值都是 `[推断]`，可执行但未逐镜头验证；Agent 应回读并抽样帧，必要时请求用户确认，不冒充候选。
- 机器只断言结构/时序/边界/文本正确；"有情绪/日系感/弹得自然"必须人工审查。
- 用户不必给每个参数；可给 reference、强弱、阅读优先级和禁用效果，Agent 再生成可审查的 motion plan。
- 不得牺牲歌词可读时长（出场不早于 `readable_until`）。

## 7. timeout 与失败恢复

- TextLayer、Animator、Selector、effect 实例、preset 和 keys 都可能非幂等。
- timeout 后读取 layer ID、lyric_id、animator/effect count、tags、key times 和文本；不整段重放。
- 文字消失：先查 layer timing、opacity、Strength/selector、enabled 和字体；逐级 disable 最近动画定位。
- 字符顺序异常：检查 language、Direction、based-on、selector 与插件 Delay；不随机改 seed。
- 字体缺失或 shaping 错误：记录实际 fallback；请求用户字体或选择获授权替代，不能偷偷下载。

## 8. 待验证

- P0 AP-TX-01：TextDocument、内置 Text Animator/Selector 与时序。
- P0 AP-MO-01：文字 Transform keys/interpolation。
- P2 AP-PL-01：TextEvo/Motion Tools adapter。
- P2 AP-ST-01：日系歌词动画人工 rubric。

当前均为 `未执行`。

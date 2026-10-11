# After Effects PV 构图与视觉验收

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：PV 构图、歌词排版、角色视觉包装、画面分层，或对“画面太空/太乱/文字不清楚”的诊断。
>
> 加载方式：与 `../ASM-After-Effects.md` 及必要的前期工作流卡一起使用；本卡不把示例风格变成默认成片模板。
>

## 1. 证据与决策边界

- `[推断]`：候选制作流程展示的候选 AE 操作；需目标环境回读。
- `[设计候选]`：可由用户覆盖的设计/工作流默认。
- `[待验证]`：插件、effect 参数、审美或行为仍需 probe/人工判断。
- ``：用户参考截图的直接结构观察；只用于层级/色彩/框架分析，不授权复刻。
- 示例画面、角色、歌词、构图和作者风格只用于理解操作关系，不得复刻或作为交付资产。

## 2. 可替换角色组件

候选流程把 body/face 等部件组织进不同表情的预合成，并在主 Comp 复用。[设计候选]

候选操作：duplicate 预合成/图层、重命名、在既有 Layer 上以 `Alt` 拖入素材替换 source。[推断]

操作契约：

1. 锁定目标 Comp/Layer ID，记录原 source、name、timing、Transform、parent、matte、effects。
2. 查找等价表情组件/operation tag；duplicate 非幂等，不存在时才创建。
3. 替换前确认新 source 类型、尺寸、duration 和 alpha 满足目标。
4. 替换后回读 source identity；Transform、parent、matte、effects 和 layer timing 应按 brief 保留。
5. 在至少三个相关时间点采样，检查边界、anchor 偏移、遮挡和表情是否符合目标。
6. 候选流程中的删除/移动 face 层是工程特例；不得对用户源组件做通用删除。需要编辑时先复制组件。

## 3. 四层画面诊断模型

仅在需要诊断层次或空洞感时使用，不要求每个画面凑齐四层。[设计候选]

```text
Foreground       光效、粒子、边框等主体前元素
Subject          角色或核心文字
Back/Mid-ground  容器、建筑、图案与主体后装饰
Background       色调与空间基础
```

机器可检查：语义分组/tag、layer order、enabled/opacity、主体/歌词边界、前景是否意外遮挡、mid-ground 是否侵入可读区。

必须人工判断：是否好看、层次是否足够、氛围是否适合歌曲、画面是否过满/过空。极简、纯文字、扁平或有意拥挤的 brief 可明确覆盖该模型。


## 4. 容器、Matte 与前景效果

### 4.1 容器 / 相框

候选例使用非标准比例 Comp、Shape 和透明开口构造拍立得式容器。[推断]

- `1080×1440` 只是该示例的设计选择，不是 PV 默认尺寸。
- 创建前确认目标 Comp 尺寸、容器 bounds、主体安全区和预期层顺序。
- 若使用 Track Matte + Invert Matte：先读取 matte source/target、mode 与 layer order；写后重新读取关系，并采样验证开口透明、背景可见、主体未被误遮挡。[推断]
- Matte/shape/effect 结构变更后重新获取 Property 引用；不沿用旧 index。
- timeout 后先查容器 Comp、shape/matte 层数与关系；不得重复 add/duplicate。

### 4.2 Lens Flare / CC Jaws 等候选效果


强制流程：

1. 在目标 build 枚举可用 effect，记录 `matchName`、实例数和参数树。
2. 参数名、范围、默认值和本地化显示名不得从示例画面硬编码。
3. 写后回读目标实例与参数；比较前后采样帧。
4. effect 缺失时使用 Shape/Mask/内置替代，或按 brief 省略；不得偷偷安装插件。

## 5. 文字、小装饰与可选插件

- Tracking、font size/weight、opacity、shadow 与 blend mode 是候选设计手段，不是固定配方。[推断]
- `Screen` 可作为去除深色背景、保留浅色线条的候选 blend；必须检查实际素材 alpha/颜色和合成结果。[推断]
- Bencode、Kana 类文本工具、Motion Tools、MultiEase、Baramoji、FastShape、TextEvo、Notepad 等全部是可选第三方能力。[待验证]
- 先探测安装状态、版本与可调用接口；缺失时以 Text/Shape/Mask/内置动画器替代或省略。
- 歌词验收优先于装饰：文字内容/语言正确、目标时段可见、未裁切、未越安全区、未被主体/边框遮挡；OCR 只作辅助，最终可读性需人工 review。

## 6. 四项设计诊断

以下是 review 问题，不是自动生成公式。[设计候选]

| 原则 | 可操作默认 | 机器断言 | 人工判断 |
|---|---|---|---|
| Contrast 对比 | 需要层级而元素权重全同时，只改变一至两个维度，如 size/weight/value/color/spacing。 | 主/次对象属性有显式差异；文本未越界。 | 主次是否清楚、对比是否合适。 |
| Repetition 重复 | 复用一个已标识源组件与可追踪副本，不手工重建近似对象。 | count、source、间距、层顺序与 bounds。 | 重复是否形成节奏而非机械堆叠。 |
| Alignment 对齐 | 先声明锚点：Comp 中心、主体边缘、网格/安全区或文本基线。 | Position/bounds 与锚线误差在显式容差内。 | 视觉平衡、光学对齐是否需要偏移。 |
| Proximity 接近 | 同语义元素分组；为歌词保留不受主体干扰的可读区。 | 组内/组间距离、交叠、越界和安全区。 | 分组是否自然、阅读路径是否清楚。 |

用户指定自由散布、极简、拥挤、故意失衡等风格时，记录覆盖理由和新的验收标准，而不是强行修回示例默认。

## 7. 重复与对齐短契约

### 7.1 规律重复

1. 锁定 source component、目标 Comp、数量、方向、间距/路径和边界。
2. 为每个副本分配 operation tag；创建前查重。
3. duplicate 或生成副本；不要假设 `Ctrl+D` 是唯一通道。
4. 回读每个 layer ID、source、Position/Rotation/Scale 和 layer order。
5. 检查越界、遮挡、同源更新影响和采样帧。

duplicate 非幂等。timeout 后以 tags、source、count 与位置指纹判断，不得再次全量复制。[推断]


### 7.2 对齐

1. 声明 `align_target`（selection、composition、safe area、guide 或对象 bounds）与轴。
2. 使用 Align panel、数值 Transform 或脚本；GUI 前确认 panel 状态和本地化。
3. 对 TextLayer 同时考虑 sourceRectAtTime/baseline 与 Anchor；不能只比较 Position。
4. 回读 bounds/Position，按像素或 comp 百分比容差验证；再由人工检查光学对齐。

## 8. 创意 brief 与参考边界

开始视觉设计前记录：[设计候选]

- 允许使用的参考和许可证；
- 禁止复制的特定角色、镜头、构图、字形处理或作者表达；
- 角色/品牌关键词和允许的隐喻；
- 必须保留的文字、颜色、logo 与可读性要求；
- 用户希望的风格、允许偏离的范围与人工 reviewer。

参考用于分析层级、色彩、节奏和排法，不授权下载或复用参考作品的图片、音乐、字体、模板、镜头或项目文件。角色设定关联、隐喻是否恰当和相似度/原创性必须进入人工 review。

## 9. 双层验收

### 9.1 结构/机器验收

- 目标 Comp/Layer/effect/matte 真实存在且 identity 正确；
- layer order、source、parent/matte、timing、enabled/opacity 与 tags 正确；
- 文本内容、时间、bounds、安全区与遮挡检查通过；
- 重复对象 count/间距、对齐误差和分组边界满足显式参数；
- 多个时点 contact sheet 与测试渲染无意外黑帧/空帧。

### 9.2 人工验收

- 主次层级、氛围、阅读路径、光学对齐与对比强度；
- 角色/歌曲主题关联；
- 字幕实际可读性；
- 原创性、授权边界与是否过度接近参考；
- 风格是否满足 brief。

机器验收通过不能替代人工审美结论；人工说“好看”也不能替代对象/时序/产物验证。

## 11. 待验证项

- LP-06：Track Matte + Invert Matte 容器结构与视觉洞口。
- LP-07：Lens Flare / CC Jaws 的目标 build `matchName` 与参数路径。
- LP-08：重复、对齐、接近的结构化检查实现。
- LP-09：独立人工 visual review rubric。

全部通过标准见主 ASM 14.3；当前状态均为 `未执行`。

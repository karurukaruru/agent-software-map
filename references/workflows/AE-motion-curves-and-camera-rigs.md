# After Effects 动态曲线与相机 Rig

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：大量进退场、镜头转场、关键帧曲线、维度分离或多级 Null 控制。
>

## 1. 证据与 baseline

- `[推断]`：候选流程采用的候选操作；需结构化回读。
- `[设计候选]`：节奏和日系风格默认；用户可覆盖。
- `[待验证]`：插件、曲线视觉质量或 clip 外 key 行为需 probe/人审。
- ``：AE 26.2.1x2 + MCP 上已写入、回读并以代表帧观察的局部动画行为。
- baseline 是 AE 内置 keyframe/interpolation/ease、Transform、Separate Dimensions 与 Null；插件只加速操作。

## 2. 动画操作合同

### 前置状态

- target Comp/Layer/Property 唯一；
- value type、现值、expression、numKeys、keyTime/value/interpolation/ease 已读取；
- layer in/out、clip 边界、fps 与目标动作时段已明确；
- 操作目的、operation ID 与是否允许覆盖既有 keys 已明确。

### 最小写入

1. 时间按 frameDuration 量化。
2. 同时刻已有 key 时修改目标 key，不新建邻近重复 key。
3. 只写本动作负责的 Property；Position/Rotation/Scale/Opacity 不因“丰富”而全部加入。[设计候选]
4. 默认匀速、Easy Ease、hold 或自定义曲线必须来自 brief/动作意图；F9 不是质量保证。[推断]
5. 结构性变化或 expression 写入后从 Layer 根重新取引用。

### 回读与视觉验证

- nearest key、时间、value、interpolation、ease/tangent；
- 多时点 `valueAtTime`；
- 起点、25%、50%、75%、终点及运动极值采样；
- 越界、闪切、文字可读停留、与 marker/clip 边界关系。

## 3. 曲线决策

- 同距离下时间更短或 Value 曲线更陡通常代表更快 `[推断]`；不要把 Graph Editor 的视觉形状直接当跨 Property 可比速度。
- 从静止到静止且未要求硬切/匀速时，Ease 可作可解释候选 `[设计候选]`。
- Rotation、Position 等可错开起始时刻以形成层次 `[设计候选]`；必须记录每个 Property 的职责和时序。
- 是否“有力”“利落”“柔和”由人工 rubric 判断；机器只断言曲线/keys 和边界。

## 4. Separate Dimensions

适用：同一 Position 的 X/Y/Z 需要独立 timing/easing，或一个维度承担镜头进场、另一个承担持续运动。[推断]

1. 读取 Position 是否已分离、维度数、所有 keys/expression。
2. 若 expression 或 adapter 不支持分离属性，先停止并选择 parent Null fallback。
3. 只在语义明确时分离；写后重新解析 X/Y/(Z) property paths。
4. 回读每个维度 keys/valueAtTime；采样验证合成运动与分离前预期一致。
5. timeout 后先检查分离状态；不得再次触发 toggle。

Separate Dimensions 是结构变化，不应被视为可盲重试的普通 set。

## 5. 多级 Null Rig

适用：同一 Camera/主体 Transform 被多段动作覆盖，或需要把推进、平移、旋转分开维护。[设计候选]

```text
subject-or-camera
-> translation_null
-> rotation_null
-> push_or_transition_null
```

规则：

- 先枚举已有 parent chain；禁止循环 parent。
- 每个 Null 写职责名/tag，只操作约定维度。
- 创建/parent 非幂等；新建前查 operation ID。
- 回读 parent chain、threeDLayer、Transform 和 keys；在关键段落采样。
- 能直接在单一 Property 清晰完成时，不为“专业感”增加多余 Null。

## 6. 弹性与第三方工具

Motion Tools Elastic/MultiEase 等不是 baseline。[待验证]

```text
probe plugin/version/adapter
-> 读取现有 interpolation/expression
-> 若插件要求线性 keys，先经用户意图确认再转换
-> 应用一次
-> 回读 expression/keys
-> 采样越界与抖动
-> 缺失则内置 ease/手工 keys/不使用弹性
```

不得伪造同名插件参数。插件 expression 失败时恢复原 expression/interpolation；不要叠加第二个弹性实例。

## 7. 可选 `style_profile=japanese_pv`

仅在用户明确要求日系、锐利或强入场时启用：[设计候选]

- 可考虑强进场、错位 Transform、较弱出场或持续运动；
- clip 外 1–2 帧的极端 key 只是示例策略，执行前记录 layer outPoint 和文字可读结束时刻；
- 教育字幕、无障碍阅读、平缓/完整动作 brief 禁止自动套用；
- 所有数值、曲线和强弱必须由 reference/brief 决定；
- 输出需人工评价“日系感/利落感”，机器只检查 timing、越界、可读性和 key 结构。

## 8. timeout 与冲突恢复

- key/add expression/Null 创建均不可盲重试。
- timeout 后按 Layer ID、Property path、frame-tolerant key time、value、operation tag 和 expression hash 查重。
- 发现部分 keys 已写入：恢复到 before snapshot或只补缺失成员，禁止整套重放。
- 同一 Property 存在未知来源 keys/expression 时停止覆盖，先确认保留/合并/替换策略。
- 多 Null 失控时从最外层开始只读审计，找到最小异常节点；不直接 unparent 全链。

## 9. 待验证

- P0 AP-MO-01：keys/interpolation/ease 与 Separate Dimensions。
- P0 AP-3D-01：Camera/Null parent 与 active Camera。
- P2 AP-PL-01：Motion Tools/MultiEase adapter。
- P2 AP-ST-01：日系运动 profile 人工 rubric。

当前均为 `未执行`。

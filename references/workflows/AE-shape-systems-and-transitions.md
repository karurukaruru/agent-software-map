# After Effects Shape 图形系统与转场

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：文字 PV 需要圆、线、射线、虚线、纹章、规律图案、强调符号，或需要以图形材质完成场景过渡。
>

## 1. 核心原则

圆、方、三角、线是可复用的最小单位，不是固定风格。通过 Stroke/Fill、Dashes、Trim Paths、Repeater 与 Merge Paths 组合成较复杂的动态图形，再把它们作为强调、背景纹理或 Matte 转场。

Agent 应创建“参数化资产”，而不是每个镜头手工重搭近似图形。

## 2. Shape asset manifest

```text
asset_id, role, comp_id, layer_id,
primitive_paths[], operators[], style_tokens,
animation_channels[], timing, anchor_rule,
repeat_count, repeat_transform, matte_role,
operation_id, adapter, fallback, review_notes
```

`role` 至少区分 `accent`、`background_texture`、`transition_matte`、`frame`。同一资产的副本引用同一 source/precomp 或明确记录派生关系。

## 3. 资产构建合同

### 3.1 通用步骤

1. 锁定目标 Comp 和 ShapeLayer ID；读取 contents/property tree、Transform、timing、已有 tag。
2. 若相同 `asset_id/operation_id` 已存在则复用或最小修改；Shape contents add 非幂等。
3. 从 primitive 开始，一次添加一个 operator；每次结构改变后从 ShapeLayer 根重新取得引用。
4. 使用目标 build 实际枚举的 `matchName` 和 propertyValueType；不从本地化 GUI 文案猜路径。
5. 回读路径数、operator 顺序、参数、keys、bounds 和渲染采样。

### 3.2 候选结构

- 波纹：圆路径 + Stroke 宽度/Scale 动画，复制多份并错时。
- 射线：线段 + Trim Paths，再以 Repeater 径向复制。
- 虚线环：Stroke Dashes + 圆路径，可复制并错时。
- 镂空环：外/内路径 + Merge Paths 的差集类模式。
- 规律图案：简单路径 + Repeater 的 Position/Rotation/Scale。

以上只定义构成关系；示例中的 9 份、16 条线等数量是示例，不得成为默认值。

## 4. Trim Paths、Repeater 与 Merge Paths

### Trim Paths

- 明确 Start/End/Offset 谁承担入场、退场或旋转职责。
- 回读 units、keys、operator 作用范围和 path order。
- 多 path 同层时检查是 simultaneously 还是 individually 的实际行为；未 probe 不猜。

### Repeater

- `count` 必须有限且来自 manifest；先小数量 probe，防止重资产/渲染爆炸。
- 记录 repeater transform 的 anchor/position/rotation/scale 与累积效果。
- timeout 后按 operator count、name/tag、count 和 transform 指纹查重。

### Merge Paths

- Add/Subtract/Intersect/Exclude 类语义必须在目标 AE 枚举并做小样；示例翻译名不能当 matchName。
- path order 会改变布尔结果；修改前保存原 contents 顺序。
- 验证填充、洞口、边缘、缩放和运动中的拓扑；失败时恢复 before contents。

## 5. Shape 驱动的 Matte 转场

候选流程采用把大量形状从黑到白的变化作为亮度 Matte，连接两个场景。

合同：

```text
准备 transition precomp
-> 声明 source shot / destination shot / duration
-> 构造灰度或 alpha 覆盖动画
-> 读取目标 build 的 matte 关系与 mode
-> 写入并回读 source/target/order/mode
-> 采样 before / 25% / 50% / 75% / after
-> 检查全屏覆盖、黑边、闪帧和重复帧
```

- 不假设黑白方向；如果结果反向，修改 invert/matte 逻辑而不是随意倒置所有 key。
- transition_matte 与可见装饰分离；Matte 层的颜色/alpha 只服务遮罩。
- 转场 duration 需按节奏量化，并为两镜保留足够可读时段。
- 目标 AE 新旧 Track Matte API 差异需 feature probe。

## 6. 可见装饰与背景纹理

- 装饰只补充视觉平衡、重拍或运动方向；不得侵入歌词安全区。
- 规律图案可做背景，但必须限制对比度、密度和运动速度。
- 同一章节复用 style tokens：stroke、fill、line cap、dash、scale、timing family；跨章节变化要有叙事理由。
- 给装饰层设置明确 in/out，避免全片无意义常驻。

## 7. 预设、素材包与 fallback

Animation Composer、AEJuice 等可提供 Shape/transition/illustration 资产。

- 先探测插件/包是否存在、版本、授权、导入后是否可编辑。
- 导入后立即记录 source、fonts/effects、分辨率、duration 和依赖。
- 预设与模板需重命名/tag，避免黑盒层混入工程。
- baseline fallback 是内置 ShapeLayer + Mask/Track Matte；外部插件缺失不能阻塞基本转场。

## 8. 验收与恢复

机器：contents tree、operator 数/顺序、keys、repeat count、bounds、layer order、matte 关系、五时点覆盖、渲染时间上限。

人工：形状是否抢主体、线条/图案是否与字体和歌曲一致、转场是否自然、密度与节奏是否过度。

故障恢复：

- 重复生成：按 asset/operation tags 合并判断，不直接删未知图层。
- 画面全黑/全透明：旁路 matte，检查 mode、方向、layer timing 和预合成 alpha。
- Repeater 过重：降低测试 count/分辨率，保留 manifest 目标值，不能让 AE 无上限计算。
- Merge Paths 错乱：恢复 before contents/order，逐个 path/operator 重建小样。

## 9. 待验证

- P1 TPV-SH-01：Shape contents、Trim Paths、Repeater、Merge Paths 与 Matte 转场。
- P1 LP-06：Track Matte/Invert Matte 关系。
- P1 AP-MO-01：Shape 参数 keys/interpolation。
- P2 AP-PL-01：素材包/第三方 Shape adapter。

当前均为 `未执行`。

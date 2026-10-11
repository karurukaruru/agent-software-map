# After Effects 3D 相机与视差

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：需要 3D layer、Z 空间、Camera、视差、景深或整体镜头运动的合成。
>
>

## 1. 证据与 baseline

- `[推断]`：候选流程采用的候选 AE 操作；目标 build 仍需回读。
- `[设计候选]`：镜头与工作流默认，可由 brief 覆盖。
- `[待验证]`：renderer/effect/参数或人工视觉判断仍需 probe。
- baseline 优先使用 AE 内置 Camera、Null、3D layer 与 Transform；Motion Tools 等扩展不进入前置条件。

## 2. 3D 场景前置状态

执行前读取：

- target Comp ID、renderer、尺寸、fps、duration；
- 所有 Camera/Light/Null/AV/Text/Shape layer 的 ID、enabled、threeDLayer、parent、index；
- 参与视差层的 Position/Scale/Orientation/X-Y-Z Rotation、Anchor、source bounds；
- 当前 active Camera、viewer 视图和已有 camera cuts；
- 背景覆盖范围、alpha/底色及运动极值时刻；
- 既有 keys/expression 与 operation tags。

不要为单层平面或纯文字镜头强行启用 3D。[设计候选]

## 3. Renderer 选择

1. 先读取现有 renderer 与合成依赖；不要盲改客户工程。
2. Classic 3D 是示例的保守默认 `[设计候选]`，不是普适最优。
3. Advanced 3D / Cinema 4D 只有在目标功能需要且 feature probe 通过后选择 `[推断]`。
4. 修改 renderer 后回读 renderer、3D layer 可用属性和采样帧；若外观或能力退化，恢复 before 值。

## 4. 建立视差场景

```text
锁定 Comp 与 renderer
-> 给背景/中景/主体/前景标记语义组
-> 只对需要空间关系的层启用 3D
-> 分配明确 Z Position
-> 必要时以 Scale 补偿远离 Camera 的背景覆盖
-> 创建或复用唯一 Camera
-> 起中末与运动极值采样
-> 回读对象关系并保存检查点
```

写入规则：

- threeDLayer、Z Position、Scale 都用稳定 Layer ID + Property path；不依赖 UI 列位置。
- Z 与 Scale 的具体值来自 brief/镜头 framing，不复制示例数值。
- 使用 Top/Custom + Active Camera 双视图或结构化坐标审计判断前后关系。[推断]
- 背景 Scale 补偿后检查分辨率、锐度和像素化；不能只验证“覆盖了”。

## 5. Camera 操作契约

### 前置状态

- Camera 数量、层顺序、enabled 和当前 active Camera 已知；
- focal length/zoom、Position、Point of Interest、Orientation、rotations 与 keys 已快照；
- 目标是平移、推进、旋转、景深还是镜头切换已明确。

### 最小写入

1. 查找相同 operation tag 的 Camera；不存在时才创建。
2. 创建后按 Layer ID/type 定位，写入明确的 camera options 与 Transform。
3. 若需要整体平移而不希望围绕 POI 旋转，创建/复用 3D Null 并 parent Camera；优先移动 Null Position。[推断]
4. 复杂镜头可使用职责单一的多级 Null，但每级只负责推进、平移或旋转之一。[设计候选]

### 回读与验证

- Camera/Null IDs、threeDLayer、parent chain、层顺序、enabled；
- focal length/zoom、Position/POI/Orientation/rotations 与 keys；
- parent chain 无循环；只有预期 Camera 在目标时段生效；
- 起中末与速度/旋转极值帧显示预期视差、framing 和主体可见性。

### 幂等性与恢复

- Camera、Null、parent 和 key 创建均不可盲重试。
- timeout 后枚举 Camera/Null、tags、parent、key times；分类为未发生、完成、部分完成或 UNKNOWN。
- active Camera 异常时先停下，枚举所有 Camera 的层顺序/enabled；不立即删除”多余”Camera。

## 6. 焦距与景深边界

- 35/50mm、广角/长焦及“速度感/稳重感”只是示例镜头语言默认 `[设计候选]`；用户 reference 优先。
- 写后必须回读实际 camera option，并用相同时间点的 framing/透视对比确认。
- Depth of Field 是否启用、aperture/blur 与渲染成本需显式记录 `[推断]`；不得因示例偏好自动关闭。
- 若用户只需局部柔化，可用后期 blur 作为可选 fallback，但它不等价于真实 DOF。

## 7. Camera 运动露边

候选修复顺序：

1. 先确认是背景 bounds 不足，而不是 Camera/层 Z 或 Scale 错误。
2. 优先使用超尺寸背景、Scale 补偿或预合成扩展。
3. 仅在 effect 存在时测试 CC Repetile 类边缘扩展；枚举 `matchName` 和参数，数值不硬编码。[推断]
4. 检查起中末及运动极值帧的透明露底、接缝、镜像重复和变形。
5. 失败时恢复 effect stack/Scale before snapshot，再选替代方案。

## 8. 失败信号

| 信号 | 先查什么 | 恢复 |
|---|---|---|
| Camera 新建后原动画消失 | active Camera、Camera 层顺序/enabled。 | 恢复目标 Camera 优先级，不盲删。 |
| 没有视差 | 参与层 threeDLayer 与 Z 差异。 | 只修缺失的 3D/Z 状态。 |
| 平移变成绕点旋转 | POI、Orientation、parent rig。 | 回滚 keys；以 3D Null 承担平移。 |
| 背景露底 | bounds、Z、Scale、运动极值。 | Scale/超尺寸背景/受控扩展。 |
| 画面看对但结构错 | viewer 视角或错误 Camera。 | 回读 active Camera；用目标 Camera 渲染采样。 |

## 9. 待验证

- P0 AP-3D-01：renderer、3D layer、Z、Camera、Null parent 与 active Camera。
- P1 AP-3D-02：Camera 运动覆盖和边缘修复。
- P2 AP-ST-01：焦距情绪 profile 的人工 rubric。

当前均为 `未执行`。

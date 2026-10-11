# After Effects 合成与素材融合

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：角色/背景/光效需要统一色温、饱和度、对比、空气感、轮廓光或 Matte 边缘。
>

## 1. 证据与 baseline

- `[推断]`：候选流程采用的候选 AE 操作。
- `[设计候选]`：调色/氛围默认，必须允许用户覆盖。
- `[待验证]`：effect/参数、插件和主观融合度需 probe/人审。
- baseline 优先使用目标 AE 中实际枚举到的内置 effect；YY Ramp 等第三方能力只作 adapter。

## 2. 合成 brief 与作用范围

执行前明确：

- 目标情绪/参考色、是否允许改变角色肤色/品牌色/背景；
- 哪些层应受影响，使用全局 Adjustment Layer、局部预合成还是单层 effect；
- 目标时段、layer order、blend mode、opacity 与已有 color pipeline；
- 文字/Logo 必须保持的可读性和颜色；
- before 帧、测试渲染与人工 reviewer。

“让人物融入背景”是设计目标 `[设计候选]`，不是可由单个数值证明的软件状态。

## 3. Effect stack 通用合同

```text
锁定 target/scope
-> 枚举 Effect Parade 与可用 matchName
-> 保存 before 参数/实例数/层顺序
-> 添加或修改一个最小 effect
-> 回读实例与参数
-> effect on/off 同时点采样
-> 检查文字、alpha、clipping 与作用范围
-> 再决定下一层 stack
```

- effect add 非幂等；timeout 后先查实例数、自定义名称、matchName 和参数指纹。
- 参数显示名、本地化文字、默认值和范围不得从视频硬编码。
- Adjustment Layer 必须回读 adjustmentLayer/enabled、in/out、layer order 与影响范围。
- 堆栈顺序改变可能改变结果；重排前后都要回读。

## 4. 候选调色与空气感

| 目的 | 候选 | 边界与验证 | 证据 |
|---|---|---|---|
| 色彩统一 | CC Toner/Tritone + 部分 Blend w/ Original | 枚举 effect/参数；保留原色；检查肤色/品牌色和 on/off 帧。 | `[推断]` `` |
| 对比 | Curves | 曲线不硬编码；检查高光 clipping、暗部死黑和文字。 | `[推断]` `` |
| 柔化 | Gaussian Blur + 低 opacity Adjustment Layer | 数值仅由画面决定；防文字/轮廓过糊。 | `[推断]` |
| 快速色调 | Hue/Saturation Colorize + blend | 仅用户允许整体调色时；回读 hue/saturation/lightness/blend。 | `[推断]` `` |
| 局部光影 | Gradient/Shape/透明度或 YY Ramp adapter | YY Ramp 缺失时走内置 fallback；不阻塞。 | `[推断]` |

示例数值和色相只可作为实验起点，不进入默认合同。

## 5. 背光轮廓候选 stack

候选链：Drop Shadow/Shadow Only → Gaussian Blur → 着色/Gradient → CC Composite/Behind。[推断]

操作规则：

1. 在独立副本/测试 Comp 上 feature probe 每个 effect 与参数树。
2. 保存原 alpha、effect stack 和 layer source。
3. 一次添加一个 effect，分别回读；不整链盲写。
4. 在发丝、半透明边缘、强反差区域和运动帧采样。
5. CC Composite/Behind 的实际 alpha/transfer 行为未验证前不得推广。
6. 缺插件着色时使用内置 Gradient Ramp/Fill/Shape 或省略轮廓光。

## 6. Matte 边缘清理

Simple Choker 等 Matte 候选只在确有黑/白边时使用。[推断]

- 先确认边缘问题来自 matte，而非缩放、颜色管理或源素材。
- 保存原 alpha 与 before 帧；以最小值逐步修改。
- 检查头发、细线、半透明和运动模糊区域；过度 choke 会不可逆地丢视觉细节。
- 结构回读通过但边缘变差时立即恢复 before effect/参数。

## 7. 双层验收

机器断言：

- Adjustment Layer/effect 实例、matchName、参数、enabled、blend、opacity、in/out、layer order；
- 目标范围内有像素变化，范围外没有非预期变化；
- alpha、黑/白边、亮部/暗部 clipping、文字 bounds 与可读性测试；
- 测试渲染可解码且颜色管理/分辨率与目标一致。

人工判断：

- 人物是否融入、轮廓是否自然、氛围是否适合；
- 肤色/品牌色是否可接受、背景是否抢主体；
- 光影方向是否自洽、是否“调色过度”；
- 歌词与 UI 是否仍清楚。

## 8. 失败恢复

- stack 部分完成：先回读真实实例/顺序，不重放整链。
- 出现全黑/全白/色偏：逐个 disable 最近 effect 定位，不删除所有效果。
- 参数路径找不到：重新枚举 matchName/参数树，禁止按显示名猜。
- plugin 缺失：记录降级，切换内置 fallback；不自动安装。
- 调色正确但主体仍“浮”：回到光向、层次、边缘、景深和 shadow 的人工诊断，不继续随机加 effect。

## 9. 待验证

- P1 AP-CO-01：Adjustment Layer 与内置候选 effect stack。
- P1 AP-3D-02：运动帧边缘/露底与 effect 修复。
- P2 AP-PL-01：YY Ramp 等第三方 adapter。
- P2 AP-ST-01：氛围与融合度人工 rubric。

当前均为 `未执行`。

# After Effects 文字 PV 风格统一与后期

> 验证状态：候选流程；使用前需在目标 AE/控制通道验证。
> 通用规则：先保存 before 状态；按稳定对象定位写入；结构回读与多时点视觉检查分别验收，无法检查的结果标为 `unverified`。

> 触发：素材来源/画风不一致、实拍与插画混合、需要噪声/故障/手绘质感，或多个预设/素材包段落缺少统一感。
>

## 1. 两类问题先分开

1. **融合问题**：不同素材的色彩、清晰度、噪声、光向、alpha、帧率与镜头运动不一致。
2. **风格问题**：作品需要手绘、低帧率、故障、颗粒、扫描线、色差或统一滤镜。

不能用重滤镜掩盖错误的抠像、露底、字幕错字或图层关系。先完成结构/融合 baseline，再做风格化。

## 2. 合成基线顺序

可考虑的实拍绿幕示例顺序可转成候选诊断链：

```text
稳定/运动匹配
-> 去除源噪声（若会妨碍 key）
-> Key/Mask 与边缘清理
-> 色彩/曝光/色温匹配
-> 清晰度与镜头模糊匹配
-> 全局重新加入统一噪声/扫描线/颗粒
-> 必要时加入统一镜头漂移
```

这是诊断顺序，不是每个项目都要全部使用。对插画/CG 同样比较色彩、边缘、纹理、光向和运动，而不是机械套用 Keylight。

每步遵守 Effect stack 合同：单项写入、回读、on/off 同时点采样、检查 alpha/文字/作用范围，再继续下一项。

## 3. 噪声与故障词汇表

可考虑多种常见候选：

| 视觉职责 | baseline 候选 | 风险/验证 |
|---|---|---|
| 细线抖动/模拟干扰 | Wave Warp 或受控 expression | 边缘裁切、文字变形、频率与采样混叠 |
| 块状水平错位 | Fractal Noise + Displacement Map | map 范围、位移方向、alpha 与文字可读性 |
| 有机扭曲 | Turbulent Displace | 细节损失、边缘穿帮、作用层范围 |
| 像素化/跳块 | Mosaic + keys/遮罩 | 字幕不可读、分辨率变化、闪烁安全 |
| 残像 | Echo | alpha 累积、拖尾遮字、渲染成本 |
| 低帧率 | Posterize Time | 音画节奏、运动跳变、作用范围 |
| 色差 | 通道偏移 baseline；插件 adapter 可选 | 黑边、过量 RGB 偏移、全片滥用 |
| 手工噪声 | 逐帧 Shape/Text/图像序列 | 工时、可编辑性、帧编号完整性 |

Holomatrix、Fast Chromatic Aberration、Glitch Pack 等只作 adapter。用户说“加点故障”时，Agent 必须先选一种主要职责和强度范围，不同时叠加所有候选。

## 4. 风格 profile

可建立项目级 style manifest：

```text
style_id, chapters[], palette, contrast_range,
texture_family, temporal_sampling, edge_character,
glow_policy, chromatic_policy, camera_noise_policy,
protected_layers[], excluded_shots[], adapters[],
before_refs[], review_refs[], operation_id
```

- `protected_layers` 默认包含歌词、Logo、法务文字和需保持准确颜色的品牌元素。
- 全局 Adjustment Layer/预合成 effect 必须明确 in/out、layer order 和 exclusions。
- 章节可改变风格，但共享一至两个稳定 token，以避免完全割裂。

## 5. 全局滤镜与图像序列往返

候选流程采用先从 AE 导出连续编号图像，再用 Photoshop Action 对每帧施加统一绘画质感，并认为强风格处理能让不同来源素材更像同一环境。

这是高成本、可能破坏可逆性的可选路径，不能作为默认：

1. 保留可编辑 `.aep`、无滤镜 master 和 before 测试段。
2. 只对 1–3 秒代表段导出版本化 image sequence，确认色彩管理、alpha、位深、fps 与编号。
3. 审查 Action/脚本步骤、输入/输出目录、覆盖策略和插件依赖；禁止处理原始素材。
4. 输出到新目录，核对首末帧、连续编号、分辨率、alpha 与失败帧。
5. 重新导入 AE，以单独预合成/替换候选方式 A/B；检查声音同步与帧率。
6. 人工批准后才扩大到全段；失败时回到无滤镜 master。

不得声称“一个滤镜可以自动解决所有融合问题”。它可降低风格差异的显著性，但无法修复错误 matte、运动、透视、光向或叙事设计。

## 6. 插件/跨软件适配器

可选工具包括 Photoshop Actions、Animation Composer、AEJuice、Deep Glow、Saber、Trapcode Form、Element 3D、Newton、C4D、Fresco 等。

- 每个 adapter 记录版本、许可证、输入/输出类型、可编辑性、色彩/alpha、失败恢复和内置 fallback。
- 外部软件往返必须使用版本化中间产物和 manifest；不能覆盖原始素材或唯一 master。
- C4D/Fresco/Photoshop 输出是外部产物，AE 中还要验证 duration、fps、alpha、色彩和重新链接。
- 不为获得示例同款结果而自动购买、下载或安装插件/素材。

## 7. 统一性验收

机器可以比较：

- effect/Adjustment Layer 作用范围、enabled、stack、keys 与 exclusions；
- 分镜间亮度/饱和度/色温/噪声强度的统计异常；
- alpha、边缘、黑白位 clipping、工作区覆盖、帧连续性与可解码性；
- 受保护文字的 bounds、颜色偏差、OCR 辅助和可读停留。

人工必须判断：

- 素材是否像处于同一视觉世界；
- 噪声/故障是否有情绪与节奏作用而非遮丑；
- 全局滤镜是否破坏人物、字体和层级；
- 章节变化是否丰富但仍属于同一作品。

## 8. 失败恢复

- 全局效果污染字幕：把 protected layers 移到作用范围外或建立受控 matte；不复制未知层堆补丁。
- 强滤镜掩盖细节：恢复 before stack，降低单项强度并逐项 A/B。
- image sequence 缺帧：停止全片处理，按 manifest 对缺失编号重跑到新目录。
- 外部插件缺失：disable adapter，使用内置 baseline 或保留无该风格版本。
- timeout/批处理状态未知：检查输出编号、mtime、日志和目标层实例；不得整批盲重跑覆盖已有帧。

## 9. 待验证

- P1 TPV-FX-01：噪声/故障 baseline 与全局 style layer。
- P1 AP-CO-01：Adjustment Layer/effect stack。
- P2 AP-PL-01：第三方/跨软件 adapter。
- P2 AP-ST-01：风格统一人工 rubric。
- P2 TPV-RT-01：版本化 image sequence → 外部处理 → AE 重导入往返。

当前均为 `未执行`。

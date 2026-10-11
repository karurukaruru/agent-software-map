# AE 模块化 Cyber-PV 制作语法

> 触发：多章节、多角色、文字与图形包装、相机运动密集的音乐视觉工程。
> 验证状态：可复用候选配方；使用前需在目标 AE/控制通道验证。数值为示例起点，不是通用默认。

## 1. 证据边界与文字载体审计

- DOM 结构、视觉序列和源参数分别记录；只有具备实际回读与可复核产物的目标环境行为才可标记 verified。
- 无 TextLayer 时，继续检查 Shape 路径、分层设计稿、静态字形与预渲染视频。路径数量/图层名不能单独证明字形来源，须观察实际画面。
- 预渲染载体能支持运动与构图分析，不能恢复原始字体、逐字 keys、easing 或内部 effect stack；这些保持 unknown。
- 分段采样只能说明采样帧；出现新源资料时重新验证，不把抽样结论称为完整源级恢复。

## 2. 模块关系

- 主合成装配章节、持续框架与跨段转场。
- 章节将前景文字、人物空间、后景纹理分为独立职责轨。
- 角色状态组件复用；相机 optics 与父级 Null 的运动职责分开。
- Primary 主句须可读；Secondary 是注释，Texture 只承担纹理与节奏。
- 配置持续 HUD 是一种设计选择；数量、颜色、字体和图形 token 由当前 brief 定义。

## 3. 故障检查

- 检查每条表达式的 expressionError，跨语言环境不要仅凭 expressionEnabled 判断健康。
- 帧导出 API 需实际探测；使用临时 Render Queue 时先保存既有队列状态，确认 idle，结束后恢复状态并核对真实文件。

## 4. 融会贯通：从设计意图到 AE 工程

### 4.1 先设计“统一中的变化”

先把歌曲拆为章节，而不是先做镜头。每章只填写七项：叙事职责、能量等级、主色、字体角色、密度、空间模式、进入/离开桥。全片再固定一个不会消失的 invariant HUD。执行规则：

- 每章只主动改变明度、字体职责、密度、材质、空间中的 2–3 个轴；其余继承全局系统；
- 高密度爆发之后安排低密度叙事段，让下一次爆发重新获得尺度；
- 副歌复现不复制镜头：保留同一语义骨架，更换色彩、角色、尺度或空间强度。

### 4.2 四种镜头句型

把复杂画面先归入句型，再选择资产和运动：

1. **中心舞台型**：主体居中，巨大 Logo/空间字与 HUD 包围；适合世界观、群像和高潮。
2. **偏侧海报型**：角色占一侧，主字占负空间；靠尺寸、裁切和前后遮挡建立层级。
3. **文字场型**：角色弱化，主字、重复词、环形字或像素阵列成为画面主体；适合节奏密集段。
4. **叙事停顿型**：低饱和/暗底、单字或小句、长持有和轻漂；用于呼吸、歌词理解与能量重置。

同一章节最多同时使用两个主句型。若主体、主字、纹理字和 HUD 都在争夺第一层级，先降密度，不靠更多 Glow 补救。

### 4.3 三轨章节模板

```text
Chapter_XX
├─ BACK_PRE（环境 / 空间字 / 材质；可预渲染）
├─ CHARACTER_STAGE（角色状态组件 + Camera/Null + 遮挡）
├─ FRONT_TYPE（主字 / 次字 / ticker / HUD 微标签）
├─ LOCAL_ADJ（章节色彩与冲击效果）
└─ AUDIO_REF（明确音频开关与时间基准）

FINAL_ASSEMBLER
├─ Chapter_01 ... Chapter_N
├─ GLOBAL_HUD
├─ BOUNDARY_BRIDGES
├─ GLOBAL_GRADE
└─ MASTER_AUDIO
```

主合成不承载镜头内部细节。角色状态必须组件化；Camera 负责 optics，Null 负责镜头运动；前/后景预渲染必须保留对应源工程和字体 manifest，避免丢失可编辑信息。

### 4.4 文字实现载体选择

| 需求 | 首选载体 | 原因与边界 |
|---|---|---|
| 文案、字体、逐字时序仍需修改 | TextLayer + Text Animator | 语义和排版最可编辑；用 matchName/Source Text 回读 |
| 字形要独立扭曲、碎裂、布尔或路径级变形 | Text → Shape 的版本化副本 | 保留原 TextLayer 隐藏备份；转换后文字语义和字体关系会丢失 |
| 手绘/定制字形需逐字调度 | 独立 PNG/AI/Shape 字形 | 建字形 manifest；不要只靠含糊图层名定位 |
| 复杂插件效果已锁定或跨机交付 | 预渲染 MOV/图像序列 | 同时交付源 AEP、字体/插件清单和 alpha/color-space 说明 |

判断 Shape 是否来自文字，不能看图层名称。应综合字符级 Vector Group、闭合轮廓/洞形、路径与顶点复杂度、字形组命名和原 TextLayer 备份。

### 4.5 运动编排顺序

运动按尺度自上而下设计：

1. 章节边界：决定硬切、共享 token、亮度、失焦、同词/材质或颜色/方向匹配桥；
2. 镜头：用 Camera parent Null 写约 0.6–2.8s 的空间运动；
3. 主体与主字：以 0.4–1.6s 的入画、聚合、裁切、缩放或旋转完成语义动作；
4. 次字与纹理：错帧、重复、ticker、环形或像素换位；
5. 微动：wiggle、audio amplitude、mosaic/displacement/glow，只提供连续能量，不移动可读主句的阅读锚点。

时间参数由歌曲重拍、阅读时长和镜头尺度标定，不从历史工程的统计量推断当前作品。

### 4.6 效果与可读性合同

- 主字先在无效果状态下通过稳定帧可读性，再添加轮廓、Glow、Blur 或 Displacement；
- 清晰主体与材质副本分层，避免在唯一可读层上同时堆模糊、色散和位移；
- 每章选一个主 effect stack、一个辅助 stack、一个转场 stack，不把五个家族全量叠加；
- Adjustment Layer 只承担局部章节 grade 或短冲击；全局 grade 与章节 grade 分开；
- Primary / Secondary / Texture 三层中，只有 Primary 必须持续可读；Texture 可以越界、重复和失真，但不得伪装成第二主句。

### 4.7 从零构建顺序

```text
歌曲章节表
-> invariant HUD 与 token 库
-> 字体 manifest / 角色状态 / 图形 token 组件库
-> 每章确定 1–2 个镜头句型与 2–3 个变化轴
-> 建三轨 Chapter 模板
-> 每镜头 Camera + Null
-> 主字与主体 semantic motion
-> 次字 / texture rhythm
-> 章节 effect stack 与 audio micro-motion
-> FINAL_ASSEMBLER 与边界桥
-> 结构、表达式、视觉、真实输出四重验收
```

## 5. 验收、失败恢复与学习闭环

### 5.1 四重验收

1. **结构**：Project Item/Layer/Precomp 引用图、启用状态、in/out、parent、3D、Camera/Null 对、source path；
2. **动画**：keys、插值、ease、expression 与 `expressionError`；音频驱动和人工语义 key 分开审计；
3. **视觉**：每章前/中/后、所有边界双帧、文字入场/稳定/出场、HUD 连续性、Primary 可读性；
4. **输出**：真实渲染文件存在、尺寸/帧率/alpha/color 正确；临时 RQ item 已删除、既有 queue 状态恢复。

若结构通过但画面失败，不能报告成功；若画面看似正确但表达式错误或源缺失，只能报告 partial completion。

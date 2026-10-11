# Agent Software Map — Adobe After Effects

> 文档状态：公开参考草案（包含按需工作流；本仓库未提供可复现的 AE 实机验证记录）
>
> 生成日期：2026-08-14
>
> 默认平台：Windows / macOS
>
> 历史研究基线：After Effects 26.3（June 2026），不代表当前最新版；实际执行必须以目标机器 `app.version`、build 和能力探针为准
> 主要自动化层：ExtendScript / JSX；候选适配器：`a-y-ibrahim/after-effects-mcp` 1.11.1，commit `5f9f6fb42698f8d3f83a2b7fbec926d0cc416e64`

## 0. 如何使用本 ASM

本文件不是 AE 功能百科。它服务于需要真实操作 AE 的 Agent，重点回答：

1. 当前真正要操作哪个对象；
2. 执行前必须读取哪些状态；
3. 选择 MCP、JSX、GUI、CEP 还是 aerender；
4. 动作返回后如何证明项目和产物真的正确；
5. 超时、部分完成或对象失效后如何恢复；
6. 哪些动作不能盲目重复或未经确认执行。

### 证据标记

- `[A]`：Adobe 当前官方产品文档或官方发布说明。
- `[B]`：Adobe 官方 GitHub、SDK、示例或开发资料；未必逐项覆盖当前 AE。
- `[C]`：高价值社区维护对象参考；需在当前版本做能力探针。
- `[D]`：候选 MCP 的固定源码、测试、README 或 changelog；只说明该实现。
- `[E]`：对本地资料和固定源码的静态审计结论；需运行时复核。
- `[已验证]`：只用于目标 AE/目标 MCP 上已经实际读取或执行并回读确认的行为。本版尚无此等级的 live-AE 结论。

- `[推断]`：可复用候选规则，需目标环境探针；不等于实机验证。
- `[设计候选]`：可由 brief 覆盖的工作流或审美选择。
- `[待验证]`：行为、参数或兼容性尚未确认。

### 执行时的最小加载顺序

1. 第 1、2、4 节：身份、对象、当前状态；
2. 第 7 节：当前可用控制通道；
3. 第 8 节：若使用候选 MCP，加载其适配器规则；
4. 第 9 节：目标动作对应的操作契约；
5. 第 11、12 节：失败恢复与安全边界。

---

PV / 音乐视觉任务按需读取 [工作流索引](workflows/README.md)，只加载当前任务涉及的卡片。卡片按通用制作职责组织。

## 1. 身份、范围与边界

### 1.1 软件身份

- 软件：Adobe After Effects。
- 领域：基于图层、属性和时间的合成、运动图形、视觉效果与渲染。
- 核心自动化对象入口：`app -> project -> items/comp/layers/properties/renderQueue`。[C]
- 脚本语言：ExtendScript / `.jsx`；它是老式 ECMAScript 环境，不等于 Node，也不等于现代 JavaScript expression engine。[A][C]
- Expression 运行在单个 Property 的求值上下文；可驱动属性，但不是外部命令桥，也不能代替项目结构脚本。[A]

### 1.2 本版覆盖

- 打开项目后的结构化观察；
- 项目项、合成、素材引用、图层及其关系；
- 文字层、调整层、摄像机、常见 AV/Shape/Text 层；
- Transform、效果、蒙版、标记、关键帧与表达式；
- 音频信息、波形/峰值辅助和 PV/MAD 卡点工作流；
- 保存、Render Queue、aerender 与输出产物验证；
- JSX、候选 MCP 文件桥、CEP/evalScript 和 GUI 的选择；
- 超时、部分修改、陈旧结果、对象引用失效与恢复。

### 1.3 本版不默认覆盖

- C++ 原生 effect、AEGP、AEIO 或新媒体格式插件开发；
- 未经实测的第三方插件、字体、模板、Output Module、codec；
- 用 AE 承担完整非线性剪辑、修音、混音或降噪；
- Beta 26.5 API；
- 把 Photoshop/Premiere 的 UXP 能力外推到 AE；
- 未保存项目的后台 aerender；
- 依赖屏幕固定坐标、面板焦点或本地化显示名的脆弱自动化。

### 1.4 第一原则

- 结构化读取优先于视觉猜测。
- 稳定 ID / 引用优先于名称；名称优先于界面位置。
- `matchName` 优先于本地化 display name。
- 写动作的“成功返回”不是最终成功；必须重新读取真实状态。
- timeout / Esc / 连接中断只表示结果未知，不表示 AE 已回滚。
- create/add/duplicate/delete/render 等非幂等动作不得盲重试。
- 修改已有工程时做最小变更；高风险任务先保存或创建版本化检查点。

---

## 2. 主要对象及关系

```text
Application app
└─ Project app.project
   ├─ ItemCollection project.items
   │  ├─ FolderItem
   │  ├─ FootageItem
   │  └─ CompItem
   │     ├─ settings / work area / markers
   │     └─ LayerCollection comp.layers
   │        ├─ AVLayer ── source -> FootageItem | CompItem | other AVItem
   │        │  ├─ TextLayer
   │        │  └─ ShapeLayer
   │        ├─ CameraLayer
   │        └─ LightLayer
   │
   │        Layer is also a PropertyGroup
   │        ├─ ADBE Transform Group
   │        ├─ ADBE Effect Parade
   │        ├─ Masks / indexed groups
   │        └─ type-specific groups
   │           └─ PropertyGroup -> Property -> value/expression/keyframes
   │
   └─ RenderQueue
      └─ RenderQueueItem -> CompItem
         └─ OutputModule(s) -> File
```

### 2.1 关系规则

- `.aep` 通常保存素材引用而不是媒体本体；移动源文件会使 Footage 离线。[A]
- 同一个 FootageItem 或 CompItem 可被多个 AVLayer 引用；修改源合成可能影响全部引用它的图层。
- Pre-compose 会创建/使用 CompItem，并把原层关系迁入或引用新合成；执行前必须明确是否移动所有属性，以及是否会改变当前合成中的渲染语义。
- Adjustment Layer、track matte、parenting、3D camera 等效果依赖层关系和层顺序；只验证单层属性不够。
- Keyframe 不是持久 DOM 对象，只是某个 Property 上的 1-based key index；插入/删除后 index 会变。[C]
- Property 没有持久 ID；其稳定性来自“稳定 Layer + `matchName` 路径 + 实例鉴别”。
- Effect 是 `ADBE Effect Parade` 中的属性组；同一 `matchName` 可存在多个实例，需再用实例 index、自定义名称或参数指纹消歧。

---

## 3. 对象识别与稳定定位

### 3.1 Project Item / Composition

优先顺序：

1. 同一项目内已知 `Item.id`，使用 `app.project.itemByID(id)`；
2. 在 `Item.comment` 等位置写入 namespaced 业务 UUID，并遍历确认唯一；
3. `parentFolder` 路径 + 对象类型 + name + settings/source 指纹；
4. 仅在无其他选择时使用 project index 或单独名称。

关键约束：

- `Item.id` 在保存并重开同一项目后稳定；项目导入另一个项目时会重新分配。[C]
- 名称可重复；index 会随增加、删除、移动或重排改变。
- 对名字选择器必须先统计命中数；不是 1 就停止或进一步消歧。

### 3.2 Layer

优先顺序：

1. AE 22.0+：`Layer.id` + `Project.layerByID(id)`，随后核对 containing comp；
2. 业务 UUID/comment + comp identity；
3. comp identity + layer type + name + source identity + timing 指纹；
4. layer index 只能用于同一短事务的“刚读取，立即写入”。

关键约束：

- duplicate/delete/move 会改变 layer index。
- 不能用当前 selection 或 activeItem 代替稳定 target；它们只能作为用户意图线索。
- 通过 ID 找到层后仍需核对父合成、类型和 source，避免沿用旧项目上下文。

### 3.3 Property / Effect / Mask

- 从 layer 根逐级重新取得，例如：

```jsx
var p = layer
  .property("ADBE Transform Group")
  .property("ADBE Position");
```

- 属性、效果与多数内置组使用 locale-independent `matchName`。
- 对 indexed group 执行 `addProperty()` / remove 后，旧的兄弟属性引用可能变成 `Object is Invalid`；结构变更后必须从根重新取引用。[C]
- 读取 `propertyValueType` 后再决定值维度；2D/3D Position、颜色、Shape、TextDocument 不能混用通用数字数组。
- 候选 MCP 若只接受 comp/layer 名称或 index，调用前先 `inspect-*`，断言唯一；复杂任务可用受审查的 `execute-script` 建立 ID-based wrapper。

### 3.4 Keyframe

稳定标识组合：

- property 的稳定 `matchName` 路径；
- 时间，按 `comp.frameDuration` 量化或使用容差；
- 预期 value / interpolation 指纹。

写入后重新运行：

1. `nearestKeyIndex(time)`；
2. 检查 `keyTime` 与目标时间容差；
3. 检查 `keyValue`、interpolation、ease/tangent（若任务相关）。

不要保存 key index 供后续长事务使用。

---

## 4. 关键状态与前置观察

### 4.1 连接与环境状态

执行 mutation 前至少获取：

- AE 是否运行、Bridge 是否响应；
- `app.version`、build、OS、UI language；
- 脚本文件/网络权限是否开启；
- project 是否存在、是否有绝对保存路径；
- project identity、active item / active comp；
- MCP server 与 panel protocol 是否匹配；
- 两端 shared directory 是否一致且可读写；
- 已安装字体、效果、预设、Render Settings / Output Module templates 和 codec（仅在任务依赖时读取）。

不要把面板焦点、viewer zoom、当前工具或 GUI selection 当作稳定前提，除非动作本身必须依赖 GUI。

### 4.2 Project 状态

读取：

- `project.file`、项目项总数、activeItem、selection；
- item 的 id/name/type/parentFolder；
- bit depth、time display、expression engine、颜色设置（动作相关时）；
- 当前任务是否已发生 mutation；
- 上次显式保存路径、时间和文件 mtime/size。

`Project.dirty` 在社区指南中属于 undocumented，不能作为安全关键的唯一未保存判断。[C]

### 4.3 Composition 状态

读取：

- id、name、width、height、pixelAspect；
- duration、frameRate、frameDuration、displayStartTime/frame；
- work area、renderer、resolutionFactor、backgroundColor；
- layer count；每层 id/index/name/type/source/parent/timing；
- enabled/locked/solo/shy/3D/adjustment/motion blur flags；
- selected layers 仅作为用户上下文。

### 4.4 Layer / Property 状态

按任务读取：

- layer source、parent、in/out/start、time remap、matte、blend mode；
- Transform 的值、keys、expression；
- Effects 的实例 index/name/matchName/enabled/子属性；
- Masks、markers、text document、audio flags；
- Property 的 `propertyValueType`、value、`numKeys`；
- 若有 expression：`expressionEnabled`、源码、`expressionError`、`valueAtTime(t, false)`。

若 Property 已有 keys，直接 `setValue()` 可能失败或破坏意图；先判定应该设置静态值、某时刻值还是某个 key。

### 4.5 Render 状态

读取：

- RenderQueue items、每项 comp identity、render flag、status、time span；
- render template / output module template；
- `OutputModule.file`；
- 输出父目录可写性；
- 旧产物的存在性、mtime、size，必要时 hash；
- aerender 使用的 `.aep` 保存时间是否晚于最后一次相关 mutation。

---

## 5. 能力树

```text
After Effects
├─ 项目管理
│  ├─ 打开/检查/保存项目
│  ├─ 导入与重连素材
│  └─ 创建、查找和整理 Project Item
├─ 合成管理
│  ├─ 创建/修改合成设置
│  ├─ 嵌套、预合成与本地化副本
│  └─ 工作区间与标记
├─ 图层与关系
│  ├─ 创建/复制/删除/重排图层
│  ├─ source、parent、matte、blend、3D、switches
│  └─ Text / Shape / AV / Camera / Light / Adjustment
├─ 属性与动画
│  ├─ 静态值、关键帧、插值、ease
│  ├─ expression
│  ├─ effects / presets
│  └─ masks / markers / text animators
├─ 音频与节奏
│  ├─ 音频元数据与电平
│  ├─ waveform / transient 分析
│  └─ markers、卡点与数据驱动动画
├─ 观察与验证
│  ├─ inspect project/comp/layer/property
│  ├─ expression 求值
│  ├─ see-frame / contact-sheet / reference diff
│  └─ 文件与媒体产物验证
├─ 输出
│  ├─ Render Queue
│  ├─ aerender
│  └─ 日志、状态与交付检查
└─ 诊断与恢复
   ├─ Bridge health / version / path
   ├─ timeout / UNKNOWN 判定
   ├─ before/after snapshot
   └─ Undo、checkpoint 或版本化输出恢复
```

---

## 6. 观察通道

按可靠性和语义使用，不机械固定单一优先级：

1. **结构观察**：候选 MCP `inspect-comp` / `inspect-layer`，或只读 JSX 返回 JSON。
2. **求值观察**：`valueAtTime`、`expressionError`、keyframe state、RenderQueue status。
3. **视觉观察**：`see-frame`、`contact-sheet`、`match-reference` 或 GUI 预览。
4. **外部事实**：项目/输出文件存在性、mtime、size、hash、序列完整性、媒体解码/探测。

### 6.1 观察规则

- 执行前读取 before snapshot；执行后必须重新从 AE DOM 获取 after snapshot。
- 写工具自己的返回值只能证明“它声称执行了什么”，不能替代回读。
- `see-frame` 只证明某个采样时刻；不证明全片 timing。
- `contact-sheet` 是时间采样；不证明每帧无黑帧或无闪烁。
- difference map 只证明像素差异，不自动证明语义正确。
- 渲染任务必须加入第 4 级验证；仅 `RQItemStatus.DONE` 仍不足以证明文件可交付。

---

## 7. 控制通道与选择规则

### 7.1 直接 JSX / ExtendScript

入口：[A]

- `File > Scripts`；
- `Run Script File`；
- ScriptUI Panels；
- Windows `afterfx.exe -r <absolute-jsx-path>`。

适合：

- 精确访问 AE DOM；
- 需要稳定 ID / `matchName` path 的自定义批量动作；
- dedicated MCP tool 不覆盖但 scripting DOM 可覆盖的能力。

限制：

- `afterfx -r` 不天然提供结构化返回和 command correlation；
- ExtendScript 运行在 AE 主线程；长脚本可能阻塞；
- 需要自行实现 try/catch、JSON envelope、operation ID、超时语义和结果验证；
- Esc 不证明回滚。

### 7.2 MCP + ScriptUI 文件桥（候选主路径）

适合：

- Agent 需要结构化工具、状态读取、视觉帧回传与错误 envelope；
- dedicated tool 能完整表达目标且目标选择器已消歧；
- 需要串行 command ID、Bridge health 和统一审计。

限制：

- 当前工作区只保存了候选实现，尚未安装或 live probe；
- 多数工具仍依赖名称/index，缺少通用 `itemId/layerId` selector；
- 文件桥 timeout 后动作可能已经发生；
- MCP 返回 `success` 后仍必须 inspect/视觉/文件验证。

### 7.3 CEP + `CSInterface.evalScript`

适合：

- 需要 HTML UI、网络/Node 逻辑和 host JSX 结合的面板；
- 已有 CEP 工程需要接入 Agent。

限制：[B]

- CEP JS 与 ExtendScript 是两个运行时，边界是字符串；复杂参数/返回值要 JSON 编码；
- 未捕获错误常退化为 `EvalScript error.`；
- host 脚本仍在主线程执行；应批量而不是大量往返；
- Adobe CEP 12 矩阵明确到 AE 25.0，本资料未得到 AE 26.3 同等级兼容矩阵，必须实机探针。

### 7.4 GUI / Computer Use

用于：

- 打开 Bridge panel、启用权限、处理必须人工选择的模态流程；
- 视觉布局、文本可读性、构图和主观质量判断；
- 结构接口确实无法触达的命令。

不要用于：

- 本可以通过 ID / `matchName` 稳定定位的对象；
- 需要批量精确数值或可重复验证的修改；
- 以固定屏幕坐标作为长期合同。

### 7.5 Expression

- 只用于 Property 随时间求值或属性关联。[A]
- 写入后验证：启用状态、源码、`expressionError` 为空，以及一个或多个时刻的 `valueAtTime`。
- 不用 expression 创建/删除项目对象、保存项目或发送外部命令。

### 7.6 aerender

- 适合已保存项目的后台或批量渲染。[A]
- 它读取磁盘项目，不读取 AE 当前未保存的内存状态。
- 参数真相以目标机器 `aerender -help` 为准；记录完整命令、exit code、stdout/stderr 和产物。

### 7.7 通道选择决策

```text
先确认目标与状态
  ├─ 有 dedicated MCP tool，参数完整、selector 唯一、结果可回读
  │    -> MCP tool
  ├─ MCP 缺 ID selector 或能力，但 JSX DOM 可精确完成
  │    -> 受审查的 ID-based JSX / execute-script
  ├─ 需要已有面板 UI/网络/Node 逻辑
  │    -> CEP + evalScript（先做兼容探针）
  ├─ 需要后台渲染已保存项目
  │    -> aerender
  ├─ 依赖视觉判断或设置 UI
  │    -> GUI / visual tool
  └─ 超出 scripting DOM 的原生能力
       -> 评估 C++ SDK / AEGP / AEIO，不在 P0 自动化中硬猜
```

---

## 8. 候选 MCP 适配器卡

### 8.1 身份与验证状态

- 仓库：`a-y-ibrahim/after-effects-mcp`。[D]
- 固定 commit：`5f9f6fb42698f8d3f83a2b7fbec926d0cc416e64`。
- package version：`1.11.1`；Node `>=18`。
- Bridge protocol：`1.11.0-mcp-enhanced`。
- README / `docs/TOOLS.md` 声称 48 tools；本地固定源码实际注册 **51 个唯一 tool**。[D][E]
- MCP server metadata 仍可能报告 `1.0.0`；不能用它判断包版本。[D]
- 本版没有安装依赖、build 或连接 AE 26.3；状态为“候选适配器，未认证”。

### 8.2 真实调用链

```text
MCP client
  -> stdio -> Node MCP server
  -> mutex 串行 clear/write/wait
  -> ae_command.json { command, args, commandId }
  -> ScriptUI panel mcp-bridge-auto.jsx 轮询
  -> ExtendScript handler 修改/读取 AE DOM
  -> ae_mcp_result.json { ..., _commandId }
  -> Node 校验 command ID，返回 MCP content / isError
```

Windows 默认 shared folder 为 `%LOCALAPPDATA%\ae-mcp-bridge`；macOS fallback 为 `~/Documents/ae-mcp-bridge`。若用 `AE_MCP_BRIDGE_DIR` 覆盖，Node 与 AE 两端必须一致。[D]

### 8.3 健康检查

每个会修改工程的工作流首先执行 `check-bridge`，要求：

- panel 正在运行并响应；
- `bridgeVersion === 1.11.0-mcp-enhanced`；
- `versionMatch === true`；
- 返回当前 AE version、project、active comp；
- shared directory 与预期一致；
- 脚本文件/网络权限已开启。

若失败：先修复 panel、权限、版本或目录；不要继续 mutation。

### 8.4 当前固定源码的 51 个工具

以下仅是能力目录；精确参数以运行中 MCP `tools/list` 为第一真相源，以固定 `src/index.ts` 为第二真相源。

- 通用/诊断：`run-script`、`get-results`、`get-help`、`check-bridge`、`run-bridge-test`、`test-animation`、`execute-script`。
- 合成/图层/检查：`create-composition`、`set-composition-properties`、`create-text-layer`、`localize-comp`、`populate-template`、`create-adjustment-layer`、`create-camera`、`duplicate-layer`、`delete-layer`、`center-layers`、`set-layer-mask`、`batch-set-layer-properties`、`inspect-comp`、`inspect-layer`、`get-layer-clip-frames`。
- 关键帧/表达式/数据：`setLayerKeyframe`、`setLayerExpression`、`animate-to-audio`、`animate-from-data`。
- 效果/预设：`apply-effect`、`add-any-effect`、`apply-effect-template`、`list-layer-effects`、`list-available-effects`、`set-effect-property`、`set-effect-keyframe`、`remove-effect`、`mcp_aftereffects_get_effects_help`、`list-presets`、`search-presets`、`apply-preset`。
- 音频/标记：`get-audio-info`、`set-audio-levels`、`analyze-audio-waveform`、`add-marker`、`add-markers-bulk`。
- 视觉验证：`see-frame`、`contact-sheet`、`match-reference`。
- 渲染：`add-to-render-queue`、`render-queue`、`start-render`、`render-aerender`、`render-status`。

### 8.5 MCP 工具选择规则

- 调试顺序：`check-bridge` -> `inspect-comp` -> `inspect-layer` -> mutation -> 再次 inspect -> 视觉/文件验证。
- dedicated tool 能完整表达目标时优先使用，因 schema 较明确；但 selector 不唯一时先停下消歧。
- `execute-script` 只用于 dedicated tool 缺口、ID-based wrapper 或精确批量操作；调用前必须声明副作用、目标、回读方式和 timeout 后恢复方式。
- `run-script` 的文档称 read-only，但固定源码 allowlist 含 create/set/apply/delete 等 mutation command；必须按具体 script 名分类，不能把整个工具当只读。[D][E]
- `execute-script` 的工具说明曾声称自动 undo group，但固定 Bridge 源码明确把 `executeScript` 放入 `NO_UNDO_GROUP_COMMANDS`；按源码处理为**没有自动 undo group**。[D][E]
- `startRender`、`addToRenderQueue`、`manageRenderQueue`、`seeFrame`、`contactSheet`、`matchReference` 同样不在自动 undo group 内。[D]
- 其余许多 mutation 只有“一个 undo group”的可恢复性，不具有异常自动回滚或事务原子性。

### 8.6 MCP 返回判定

Bridge/Node 的 command ID 匹配、`status`、`success` 和 `error` envelope 可用于判断传输层，但最终状态分四类：

- `成功`：返回正常，且独立回读/产物验证通过；
- `失败`：返回错误，且回读确认目标未达到；
- `部分完成`：返回错误/超时，但项目发生了部分预期 mutation；
- `UNKNOWN / 结果尚未验证`：超时、陈旧/partial result、Bridge 断连或无可靠回读。

UNKNOWN 时不得直接重试非幂等动作。

---

## 9. 高价值操作契约

### 9.1 连接、预检与目标解析

**目标**：在任何 mutation 前建立可复现的 AE、项目和目标对象上下文。

**步骤**：

1. `check-bridge` 或只读 JSX 获取 AE/Bridge/project 状态。
2. 记录 AE version/build、OS、UI language、项目绝对路径。
3. 若项目未保存且任务会修改大量内容，先请求/执行版本化保存检查点。
4. `inspect-comp` / 自定义只读 JSX 枚举候选 Comp，并记录 id、name、settings。
5. `inspect-layer` 或按 ID 读取目标层；对名称匹配要求命中数为 1。
6. 读取目标 property path、value type、keys/expression 和 before snapshot。
7. 生成业务 operation ID；对 create/add 类操作先搜索已有同 operation tag 产物。

**成功验证**：所有关键状态已知，target 唯一，前置条件满足，before snapshot 可用于恢复/对比。

**幂等性**：只读，可安全重复；但要防陈旧 Bridge result，要求 command ID 匹配。

### 9.2 创建或修改 Composition

**适用**：创建新 Comp，或修改尺寸、时长、帧率等。

**前置**：

- 项目已打开；
- 新建前确认名称/tag 不与既有目标冲突；
- 修改前确认嵌套引用、渲染队列和层 timing 的影响；
- frame rate、duration、width/height/pixelAspect 已明确。

**通道**：`create-composition`、`set-composition-properties`，或 ID-based JSX。

**成功验证**：

- 重新按 Item ID 或唯一 tag 查找；
- 核对 name、type、width、height、pixelAspect、duration、frameRate；
- 创建动作检查 item count 增量；
- 若有视觉内容，至少渲染一帧。

**重试**：create 不可盲重试；先查 operation tag / 同 settings 指纹。绝对 set 在没有关联副作用时通常可重试，但修改时长/帧率后仍要检查层、key 和 nested comp 语义。

### 9.3 创建、复制、删除或批量修改 Layer

**前置**：

- target comp identity 已锁定；
- 目标 layer selector 唯一；
- 读取 layer count、顺序、source、parent、matte、locked 状态；
- 对 delete/duplicate 记录 before snapshot 和业务 operation ID。

**通道**：dedicated MCP tools；若需要稳定 ID、parent/matte/precomp 等复杂关系，使用受审查 JSX。

**成功验证**：

- 重新读取 comp layers；
- 核对新/修改层的 ID、type、source、name、index、in/out/start、parent；
- 对批量修改逐层校验，不以“批处理成功”代替成员检查；
- 对原对象做负向检查，确认未误改或误删；
- 有视觉关系时执行 `see-frame`。

**重试**：

- create/duplicate/delete：不可直接重复；
- 绝对属性 set：先回读再决定；
- timeout 后按 ID/tag 和 layer count 判断动作是否已发生。

**安全**：删除层、批量改层、改变 source/parent/matte 前需要保存或可恢复检查点；删除属于高影响动作。

### 9.4 设置 Property、关键帧和缓动

**前置**：

- 目标 layer 和 property path 已稳定定位；
- 已读取 `propertyValueType`、value、keys、expression；
- 时间已按 comp frameDuration 处理；
- 确认是设置静态值、在某时刻设值，还是修改既有 key。

**通道**：`batch-set-layer-properties`、`setLayerKeyframe`、`set-effect-property`、`set-effect-keyframe` 或 JSX。

**步骤**：

1. 从 layer 根重新取得 property 引用。
2. 若有 expression，先决定保留、禁用还是移除；不得默默覆盖。
3. 对已有 keys 的属性避免直接 `setValue()`。
4. 对相同时间设 key 时使用帧容差，避免浮点误差产生邻近重复 key。
5. 结构性 add/remove 后重新取 Property 引用。

**成功验证**：

- 重新获取 property；
- 核对静态 value，或 `nearestKeyIndex` + `keyTime` + `keyValue`；
- 需要时核对 interpolation、ease/tangent；
- 用多个时点 `valueAtTime` 或 contact sheet 检查 timing。

**重试**：绝对 set 通常近似幂等；setValueAtTime 只有在时间量化一致时才近似幂等。

### 9.5 写入或移除 Expression

**前置**：保存原 expression、enabled 状态、error 和若干时点求值。

**通道**：`setLayerExpression` 或 JSX。

**成功验证**：

- `expressionEnabled` 符合要求；
- 源码回读一致；
- `expressionError` 为空；
- 多个关键时点 `valueAtTime(t, false)` 可求值且语义合理；
- 必要时渲染采样帧。

**失败恢复**：恢复原 expression/enabled；重新求值。不要把 modern expression syntax 直接复制到 ExtendScript command 中。

### 9.6 添加/修改 Effect 或 Preset

**前置**：

- 目标机器确认存在目标 effect `matchName` 或 preset 文件；
- 目标 layer 唯一；
- 读取 effect 实例列表及参数树；
- 明确重复应用是否允许。

**通道**：effect/preset dedicated tools 或 JSX `ADBE Effect Parade.addProperty(matchName)`。

**成功验证**：

- 重新读取 Effect Parade；
- 确认预期 `matchName` 的实例数和目标实例；
- 重新读取参数值/keys；
- 视觉效果任务增加前后帧或 diff 验证。

**重试**：apply/add 通常非幂等，会产生重复实例；timeout 后先查实例数和参数指纹。

### 9.7 音频分析、标记与 PV/MAD 卡点

**目标**：以音频结构辅助 marker、文字/角色动画，不把“振幅大”等同于“音乐上重要”。

**前置**：

- 音频 source、采样范围、comp fps 和目标片段已明确；
- layer marker 与 comp marker 的归属已明确；
- 旧 markers/keys 已快照；
- 若用 `analyze-audio-waveform`，输入格式/ffmpeg 可用性已确认。

**建议工作流**：

1. 先标记乐句、歌词起点、强拍、停顿与段落转折，而不是机械标记每个峰值。
2. `get-audio-info` / waveform 分析生成候选 peaks。
3. 人工/规则筛选音乐语义上的重要点。
4. `add-markers-bulk` 写入带 operation tag/comment 的 markers。
5. 对角色跳动、歌词入场使用绝对时间 key；常规重复段才考虑 loop expression。
6. 关键时点 contact sheet + 音频/时间标记联合复核。

**成功验证**：marker count、time、comment、duration 回读；关键帧与 marker 时间容差内一致；视觉采样显示重音动作和歌词可读停留。

**重试**：add marker/keyframe 非幂等；先按时间容差 + comment/tag 查重。

### 9.8 保存项目与建立检查点

**前置**：目标绝对路径明确；覆盖策略明确；外部素材依赖已知。

**步骤**：

1. 高风险任务前优先保存当前版本；需要时另存 `project_vNNN.aep`。
2. mutation 完成且回读通过后显式保存。
3. 保存后读取 `project.file`，检查目标文件存在、mtime 更新、size > 0。
4. 高价值项目可另开副本或重新加载后复查核心对象 ID/属性。

**安全**：不静默关闭未保存项目；不未经确认覆盖用户唯一项目文件。

### 9.9 加入 Render Queue 并前景渲染

**前置**：

- target comp identity 唯一；
- template 在本机存在；
- output path 绝对、父目录可写；
- 旧文件策略为拒绝、版本化或明确覆盖；
- 项目已保存检查点。

**步骤**：

1. `add-to-render-queue`。
2. `render-queue` 回读，确认 target comp、`QUEUED`、time span、template 和 output file。
3. 拒绝 `NEEDS_OUTPUT`。
4. `start-render`；注意 AE UI 会阻塞。
5. 等待最终 status；timeout 只表示等待超时，渲染可能仍在进行。
6. 验证输出文件/序列。

**成功验证**：

- RQ status 最终为 `DONE`；
- 文件/序列存在、mtime 晚于任务开始、size > 0；
- 图像序列检查首帧、末帧和预期编号范围；
- 媒体可解码，且分辨率、帧率、时长、音频流符合要求；
- 最终视觉抽帧复核。

**重试**：render 非幂等；失败重试使用新的版本化输出路径，保留旧日志和失败产物。

### 9.10 aerender 后台渲染

**前置**：项目必须保存，保存 mtime 晚于最后相关 mutation；`aerender -help` 已在目标机器探针；output 策略明确。

**通道**：候选 `render-aerender` 或直接进程调用。

**成功验证**：exit code 0、日志显示完成，再执行与 9.9 相同的产物/媒体/视觉验证。

**失败特征**：磁盘项目过旧、comp 名歧义、template 缺失、素材/字体/effect 缺失、output path 无效。

### 9.11 任意 `execute-script`

**风险等级**：高。它可越过 dedicated schema，固定源码中没有自动 undo group。

**执行前必须有**：

- 代码正文审查；
- 明确 target ID 与 property path；
- 输入参数 allowlist 和类型验证；
- 副作用列表；
- before snapshot；
- timeout；
- JSON-serializable 返回；
- 独立 after-read 和失败恢复方案。

**禁止**：

- 拼接未经转义的用户输入成 JSX；
- 在目标不唯一时按第一个名称/index 操作；
- 在脚本中静默删除、覆盖、关闭、渲染或访问任意文件；
- 认为无异常即成功；
- timeout 后原样重跑。

---

### 9.12 第三方预设与脚本适配器

**状态**：`[待验证]`；本仓库不提供第三方脚本的内部 API 捕获、闭包改写或专有表达式副本。

1. 核对已安装版本、许可、公开接口和目标层；没有公开接口时选择 GUI 或内置 Text Animator。
2. 保存目标层、选中状态、效果/动画器树和关键帧；先在副本上应用一次。
3. 枚举真实生成的效果、动画器、控制层和表达式错误；不要把 UI 名称当稳定 API。
4. 回读结构并检查入场、阅读、退场代表帧；结构正确只支持结构验收。
5. 超时后先检查实际实例数量和状态；恢复 before 状态或只补缺失部分。
6. 切换项目、重载脚本或重启 AE 后重新探测接口；不得假设全局对象仍有效。

### 9.13 脚本属性与视觉验收探针

**状态**：`[待验证]`。以下是目标环境检查项，不是 AE 26.x 通用认证：

- 从 `ADBE Transform Group` 重新取得 Position/Scale/Rotation/Anchor，检查返回值与维度；结构修改后不要沿用旧引用。
- 插值与 blend 使用目标宿主的命名枚举；不要把某次回读的整数常量写成跨版本合同。
- `setTemporalEaseAtKey` 的数组规格按实际 property value type 确认；空间 Position 与非空间多维属性不能只按坐标数量类推。
- `TextDocument` 的填充开关与 RGB 颜色分开处理。候选脚本使用 `applyFill=false`、`applyStroke=true`，设置有效 strokeColor/strokeWidth 后将文档写回；先在独立文字层探测。禁止以 `fillColor=null` 代替无填充设置。
- 字体应回读实际解析的字体标识；文本 bounds 与 Anchor 在修改字体/字号/文本后重新计算。
- `expressionEnabled` 不足以证明健康；同时检查 `expressionError` 与若干时点的求值。
- 改 `startTime`、parent、matte 或分离维度后，回读 in/out、keys 和世界坐标，确认时间/空间关系没有意外变化。
- 宿主对象的方法保持其对象上下文；接口失败先查引用、类型和版本，不推断某个函数名被 AE 全局保留。
- 可反射到的方法不等于可调用。帧导出失败时，先探测独立单帧 Render Queue；保存并恢复既有 queue 状态，核对实际产物文件。
- 静态回读不能证明像素正确；缺字体、媒体、插件或渲染通道时，视觉结果保持 `unverified`。

---

## 10. 高价值工作流

### 10.1 通用可靠 mutation

```text
Bridge/AE health
-> 记录版本与项目 identity
-> 解析稳定 target
-> before snapshot + 唯一性断言
-> operation ID / 查重
-> 执行一个边界清晰的动作
-> 检查 command/error envelope
-> 从 AE DOM 重新读取
-> 需要时视觉/文件验证
-> 保存检查点
-> 记录 after snapshot
```

### 10.2 文字层创建与动画

```text
确认目标 Comp
-> 查重业务 tag/name + type
-> 创建 TextLayer
-> 回读 layer ID、TextDocument、timing、Transform
-> 设置文字与样式
-> 回读字体/方向/对齐（目标机器字体必须存在）
-> 设置关键帧/表达式
-> 回读 keys/expression/valueAtTime
-> see-frame + contact-sheet
-> 检查可读停留、运动模糊、入退场 timing
-> 保存
```

### 10.3 15 秒音MAD / PV 练习

```text
确认定稿音频与 10–20 秒范围
-> 建立 MAIN / scene / lyric / character 结构
-> 读取 waveform，建立乐句/重音/歌词 markers
-> 先做节奏与镜头草稿
-> 角色轻跳（Position/Scale，避免变形）
-> 歌词入场、稳定可读、退出
-> Mask/Matte 或转场
-> Motion Blur 与颜色统一
-> contact-sheet 看节奏
-> 只渲染工作区测试
-> 检查音画同步、错字、黑帧、素材/音频
-> 版本化保存与最终输出
```

### 10.4 timeout / UNKNOWN 恢复

```text
停止发送新 mutation
-> check-bridge
-> 记录原 command ID / operation ID
-> inspect target 与相关计数/状态
-> 判断：未发生 | 已成功 | 部分完成 | 仍 UNKNOWN
-> 已成功：继续独立验证
-> 未发生：修复前置条件后才可重试
-> 部分完成：最小恢复；必要时从 checkpoint
-> 仍 UNKNOWN：请求人工判断或恢复备份
```

---

### 10.5 PV 制作与参考工程分析

- 使用 [工作流索引](workflows/README.md) 选择前期、文字、插画、相机、图形、合成或后期卡片。
- 分析参考工程时，将 DOM 结构、视觉观察和源参数恢复分开；烘焙图像/视频不能提供原始字体、key 或插件参数。
- 只读捕获资料可能包含私有文本和路径；默认保留在该任务环境，公开地图只记录抽象方法。
- 以原始工程的实际状态为依据；所有重建另存，结构与多时点视觉对照共同验收。

---

## 11. 失败模式与恢复

### 11.1 Bridge / transport

| 失败信号 | 可能原因 | 处理 |
|---|---|---|
| 所有工具 timeout | panel 未打开、auto-run 未启用、权限未开 | 打开 panel、启用文件/网络权限，重新 `check-bridge` |
| version mismatch | server 与已安装 panel 不同版本 | 重新安装 bridge、重启 AE 与 MCP client |
| shared folder 无结果 | Node/AE 路径不同、OneDrive 重定向、权限/锁 | 比对实际路径；两端统一 `AE_MCP_BRIDGE_DIR` |
| stale / wrong result | 旧 panel 无 command ID、陈旧结果文件 | 要求 `_commandId` 精确匹配；升级 panel |
| partial JSON | 写入过程中读取或文件锁 | 继续只读轮询；不要另发 mutation 覆盖单一 command file |

### 11.2 Object model

| 失败信号 | 原因 | 恢复 |
|---|---|---|
| 找错层/合成 | 名称重复、index 漂移、activeItem 变化 | 停止；按 ID/父对象/type/source 重新消歧 |
| `Object is Invalid` | indexed group add/remove 后旧引用失效 | 从稳定 Layer 根重新获取 property tree |
| `setValue` 失败 | Property 已有 keyframes | 改用 setValueAtTime/AtKey，先回读 keys |
| 维度/类型错误 | 2D/3D、颜色、Shape/TextDocument 不匹配 | 读取 `propertyValueType`，构造正确类型 |
| display name 找不到 | UI 本地化或用户重命名 | 使用 `matchName`；必要时枚举可用效果 |

### 11.3 Execution

- 模态框可能阻塞主线程，导致 Bridge 无法写结果；候选 Bridge 会 suppress dialogs，但这也可能隐藏需要用户决定的问题。
- timeout 或 Esc 后动作可能部分完成；状态为 UNKNOWN。
- undo group 只把动作组合进 Undo history；异常不会自动 Undo。
- 若确定某命令单独形成 undo group、其后无用户动作，才可考虑受控执行一次 Undo；否则从保存点/备份恢复。
- 恢复后重新检查 Bridge、project identity 和目标对象，不沿用旧引用。

### 11.4 Render / file

- aerender 看不到未保存 mutation：保存并核对 mtime 后重试。
- `NEEDS_OUTPUT`：修复 OutputModule.file，不启动 render。
- 缺字体/effect/template/footage：记录依赖并在目标机补齐或替换，不假定跨机器一致。
- 旧文件被误当新结果：比较任务开始时间、mtime/size/hash，并使用版本化路径。
- PNG/序列异步落盘或暂时锁定：等待文件结构完整，不以路径刚出现为完成。

---

## 12. 安全边界

### 12.1 默认需要更高确认或检查点

- 删除 Project Item、Layer、Effect、Marker、RenderQueue item；
- 覆盖 `.aep`、素材或输出文件；
- 批量改层、替换 source、改变嵌套/parent/matte；
- 清空 Render Queue；
- 任意 `execute-script`；
- 关闭项目/AE；
- 启动长时间、可能覆盖产物或消耗大量资源的 render；
- 写入任意文件路径或访问网络。

### 12.2 具体规则

- 删除/覆盖前记录 exact target、影响引用、是否可逆、恢复文件。
- 不在用户唯一项目文件上做未经确认的覆盖；优先版本化另存。
- 不静默关闭未保存工程。
- 不把用户文本直接拼成 JSX、expression 或 shell command。
- 不泄露项目路径、素材路径、用户名、许可证、token 或内部日志中的敏感信息。
- 视觉 scratch、临时渲染和失败产物应使用独立目录；确认不再作为证据后再清理。
- 批量动作要有上限、target allowlist 和 dry-run/preview（可行时）。

---

## 13. 版本与环境差异

- 历史资料基线：AE 26.3；目标机器仍需记录完整 build。[A]
- AE 22.0+ 有 persistent `Layer.id` / `Project.layerByID`；使用前 feature detection。[C]
- AE 26.0 增加 variable font axis、`Property.propertyParameters`、`Property.valueText` 等 hook；旧版本不可假设存在。[A/C]
- AE 26.3 增加 Parametric Mesh scripting 对象和 Advanced 3D camera properties；需要时 feature detection。[A/C]
- Beta 26.5 GuideOptions 不进入默认路径；enum 必须比较常量而非 raw integer。
- Expression JavaScript engine 可较现代；`.jsx` ExtendScript 仍是 ES3 时代环境。
- Windows/macOS 菜单与脚本路径不同；候选 MCP shared folder 规则不同。
- 旧教程的概念可用，但菜单、模板、输出建议需按当前版本核对。
- UI language 会影响显示名和菜单命令；属性/效果尽量用 `matchName`。
- 候选 MCP changelog 记录 AE 26.3x 某构建上直接 `layer.property(transformMatchName)` 可能返回 null；先取 `ADBE Transform Group` 再取子属性。此为第三方实测，不是 Adobe 合同。[D]

---

## 14. 当前未知项与下一轮验证任务

### 14.1 高价值未知

- 目标机器实际 AE version/build、OS、UI language。
- 候选 MCP 是否为用户最终采用的实现。
- 运行中的 `tools/list` 是否与固定源码 51 tools 一致。
- ScriptUI bridge 是否可安装、自动轮询、写入结果和正确报告 protocol。
- AE 26.3 上核心 create/set/inspect/save/RQ/aerender 是否逐项兼容。
- CEP 12 在目标 AE 26.3 build 上的实际兼容性。
- 目标机器字体、effects、presets、templates、codec、ffmpeg 和输出路径权限。
- 候选 MCP 名称/index selector 在真实重名工程中的失败行为。
- GUI focus、模态框、缓存与播放状态可否稳定观察。

### 14.2 建议 live probe 顺序

1. 在副本项目中运行 `check-bridge`，记录 protocol/AE/project/path。
2. 运行时 `tools/list`，保存 tool 名与 schema hash。
3. 只读：inspect project/comp/layer/property。
4. 低风险 create：新建带唯一 tag 的测试 Comp/TextLayer。
5. set Transform、keyframe、expression，并结构回读。
6. Effect/Mask/Marker 测试并视觉验证。
7. 保存到版本化测试 `.aep`，检查文件。
8. Render Queue 渲染一帧到新路径；验证 PNG。
9. aerender 已保存测试项目；保存进程日志与产物。
10. 模拟 timeout/Bridge 重启，确认 UNKNOWN 恢复流程。
11. 测试完成后只删除明确属于测试命名空间的对象/文件。

通过前不要把本 ASM 中 `[C][D][E]` 行为升级为 `[已验证]`。

---

## 15. ASM 自检结果

- **对象**：覆盖 Project/Item/Comp/Layer/Property/Keyframe/RenderQueue 的关系与稳定定位。
- **状态**：列出连接、项目、合成、图层、属性和渲染的前置读取。
- **能力**：以用户目标组织，而非复制菜单。
- **观察**：区分结构、求值、视觉和外部产物。
- **控制**：说明 JSX、MCP、CEP、GUI、expression、aerender 的选择条件。
- **操作**：为 create、layer、keyframe、expression、effect、音频、保存、render、任意 JSX 提供契约。
- **验证**：禁止把 tool success 当最终结果。
- **失败**：覆盖 timeout/UNKNOWN、部分完成、对象失效、渲染旧产物与恢复。
- **安全**：对删除、覆盖、批量修改、任意脚本和渲染给出具体边界。
- **体积**：保留高价值规则；不复制 51 个工具的完整 schema。

本版结论：足够作为 AE 26.x + 候选 MCP 的第一版执行地图，但不是生产兼容认证。下一步价值来自目标 AE 的 live probes，而不是继续堆普通教程。

---

## 16. 来源索引

### 可公开核对的来源

- [Adobe After Effects：Scripts](https://helpx.adobe.com/after-effects/using/scripts.html)：脚本入口、权限与运行方式。[A]
- [Adobe After Effects Developer](https://developer.adobe.com/after-effects/)：Adobe 开发入口与扩展能力。[A]
- [Adobe After Effects：Expression language](https://helpx.adobe.com/after-effects/using/expression-language.html)：expression 与 script 的边界。[A]
- [Adobe After Effects：Expression language reference](https://helpx.adobe.com/after-effects/using/expression-language-reference.html)：expression 对象与语义。[A]
- [候选 After Effects MCP 实现](https://github.com/a-y-ibrahim/after-effects-mcp)：第三方适配器公开仓库；本 ASM 中的适配器结论限定到文件头记录的固定 commit，不代表其所有未来版本。[D]

### 验证边界

新增工作流中的运行时行为与数值保持候选状态；结构检查、视觉检查和真实输出分别验收。执行前核对目标软件版本、实际工具 schema 和受控探针；固定适配器 commit 是历史研究对象，不是当前版本承诺。

补充官方说明：

- [Character panel：填充与描边](https://helpx.adobe.com/after-effects/desktop/add-text/formatting-characters-and-paragraphs/formatting-characters-character-panel.html)。
- [Keyframe interpolation：时间与空间插值](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/animation-keyframes/keyframe-interpolation.html)。
- [Keying：素材键控与透明度检查](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/keying/keying.html)。

## 17. 公开增量记录

### 2026-10-11 — 工作流整理与发布审查

- 新增 14 张可按需加载的 PV/AE 工作流卡片及索引。
- 按制作职责组织通用方法与示例；保留按需加载结构。
- 所有新增运行时行为保持待验证；没有执行 AE 或 MCP 实机测试。
- 补充文字填充、空间缓动、表达式、引用图、音频和视觉验收的边界。

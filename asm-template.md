# Agent Software Map — <Software Name>

> Optional checklist. Keep only information that improves execution. Mark insufficiently supported claims as `unknown`; do not guess merely to fill the template.

## 0. How to use this ASM

- Minimum loading order: identity and scope → target objects and state → relevant capability or operational contract → failure recovery.
- Evidence labels: `verified` / `documented` / `inferred` / `unknown`.
- Applicable software version, platform, and environment: <fill in>.

## 1. Identity, scope, and boundaries

| Field | Content |
|---|---|
| Software | |
| Version or range | |
| Operating system | |
| Interface language | |
| Known extensions | |
| Available automation | API / CLI / native scripting / GUI / computer use / other |
| In scope | |
| Out of scope | |

## 2. Sources and evidence

| Source | Evidence level | Version/environment | Supported claim |
|---|---|---|---|
| User-provided material | | | |
| Official documentation, source, API, or release notes | | | |
| Direct observation or controlled test | | | |

## 3. Important objects and relationships

```text
<Software root>
├── <Object A>
│   └── <Child of A>
└── <Object B>
```

Record only relationships that affect targeting, edit scope, references, copying, or deletion.

## 4. Object identification and stable addressing

| Object | Preferred address | Fallback | Ambiguity rule |
|---|---|---|---|
| | Unique ID / stable reference / full path | Parent + type + name | Never silently select the first match |

## 5. Key states and their effects

| State | How to observe it | Effect on the next action | Prohibited or gated action |
|---|---|---|---|
| | | | |

## 6. Capability tree

Organize capabilities around user goals and stable objects. If several interfaces perform the same underlying action, keep one capability node and describe the alternatives in its operational contract.

```text
<Software>
├── <User goal A>
│   └── <Actionable capability>
└── Diagnostics and recovery
    └── <Observation or recovery capability>
```

## 7. Observation methods

| State to observe | Preferred method | Fallback | Limit or ambiguity |
|---|---|---|---|
| | Structured query / API / script | GUI | |

## 8. Control methods and selection rules

| Method | Verified capability | Important limit | When to choose it |
|---|---|---|---|
| API / CLI / script / GUI / other | | | |

Prefer the method with the best success rate, clearest state, strongest verification, and smallest side effects for the current task. Do not impose a universal interface hierarchy.

## 9. High-value operational contracts

### 9.1 <Operation name>

**Goal**

<Describe the user outcome, not a button.>

**Applicable scenario and preconditions**

- <When to use or avoid it>
- <Required state before execution>

**Target object and disambiguation**

- Type, parent, ID/path, and name: <fill in>
- Multiple matches: <rule>

**Parameters**

- <Only constraints, units, ranges, defaults, or version differences that materially affect the result and are not already obvious from the tool schema.>

**Execution methods and selection rule**

- <Method, entry point, known boundary, and selection condition>

**Procedure**

1. Observe the state that affects the result.
2. Resolve and confirm the target object.
3. Apply the minimum necessary change.
4. Read the real post-operation state.

**Expected state transition**

```text
<Before> → <After>
```

**Success verification**

- <Object exists, properties match, output exists and is readable, final result is observable, and so on.>
- If only the execution response is available, mark the result `unverified`.

**Failure, recovery, and retry**

- Failure signals: <real, evidenced signals>
- Partial completion: <how to determine completed work>
- Recovery: stop → observe real state → find the smallest recovery point → retry, switch methods, or request intervention.
- Idempotency: safe to repeat / inspect before repeating / unsafe to repeat directly.

**Side effects and safety boundary**

- <Impact, reversibility, checkpoint or confirmation requirement, and recovery>

**Evidence**

- <Sources for state, parameters, behavior, tested environment, and version range>

## 10. High-value workflows

```text
Confirm target and state
→ Use operational contract A
→ Verify checkpoint
→ Branch on observed state
→ Use operational contract B
→ Final verification
→ Save or establish a checkpoint
```

Record ordering, state dependencies, decision branches, verification checkpoints, and recovery positions. Reference existing contracts instead of duplicating them.

## 11. Global decision rules

- Existing target: decide whether to reuse, modify, or create; do not duplicate automatically.
- Unknown critical state: observe before acting.
- First execution failure: inspect state and cause before retrying.
- Tool reports success but the result cannot be checked: mark `unverified`.
- Existing user data: prefer the smallest sufficient edit.
- Irreversible action: create a recovery point and request confirmation appropriate to the impact.

## 12. Failure and recovery model

| Failure mode | Signal | Possible partial result | Smallest recovery point | Next choice |
|---|---|---|---|---|
| | | | | Retry / switch method / user intervention |

## 13. Safety boundaries

| High-impact action | Impact and reversibility | Requirement before execution | Recovery |
|---|---|---|---|
| Delete / overwrite / publish / send / pay / change permissions | | | |

## 14. Version and environment differences

Record only differences that change the agent's decision or execution path.

| Version/platform/environment | Difference | Decision impact | Evidence |
|---|---|---|---|
| | | | |

## 15. High-value unknowns

- `unknown`: <A question that affects current or future tasks and is worth validating.>

## 16. Self-check and incremental updates

Does this map reduce wrong-object edits, state mistakes, poor method selection, pointless exploration, false success reports, and recovery risk? If it only lists features or buttons, compress and restructure it.

| Date | Version/environment | New evidence | Local change | Validation status |
|---|---|---|---|---|
| | | | | |

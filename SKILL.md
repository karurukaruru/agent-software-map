---
name: agent-software-map
description: Create, validate, use, and incrementally update Agent Software Maps (ASMs). Before operating software, check for a map covering the same product, version, or software class; use it to choose observation and control methods, inspect state, execute safely, verify the real result, and recover from failure. Use this skill both to create new maps and to preserve reusable knowledge learned from real software operation.
---

# Agent Software Map

> Give an agent a map before it operates unfamiliar software.

An Agent Software Map (ASM) is not a user tutorial, a software encyclopedia, or a rewritten manual. It externalizes operational knowledge that an experienced user relies on but an agent may not know.

Its purpose is to reduce:

- blind exploration and repeated trial and error;
- state and target-object mistakes;
- poor execution-method selection;
- false reports of success;
- unsafe retries and avoidable side effects;
- repeated rediscovery of the same failure and recovery knowledge.

An ASM serves a capable reasoning agent. Record information the agent is likely to lack and that materially changes task success, verification, or safety.

The complete Chinese design master is available in [SKILL.zh-CN.md](SKILL.zh-CN.md).

---

# 0. Core design principles

## 0.1 Prefer information gain

Before adding an item, ask whether omitting it would make an agent likely to:

- guess incorrectly;
- require extra attempts;
- select the wrong method;
- operate on the wrong object;
- fail to verify the result;
- repeat a failed action without understanding the state;
- cause a meaningful side effect; or
- rediscover the same fact in a future task.

Prefer software- or version-specific behavior, hidden and state-dependent behavior, important object relationships, stable addressing, method boundaries, non-obvious parameter constraints, real success checks, failure signals, recovery, retry safety, and expert preflight checks.

Avoid software history, promotional description, obvious button explanations, duplicated tool schemas, unrelated features, unverifiable speculation, and background material that does not improve execution.

## 0.2 Do not build an encyclopedia

Prioritize frequent, valuable, failure-prone, state-sensitive, multi-method, high-impact, and repeatedly encountered tasks. A simple capability may need one line; a complex or risky operation may need a complete operational contract. Low-value capabilities may be omitted.

The value of an ASM comes from effective knowledge density, not length or feature count.

## 0.3 Reduce low-value exploration, not all exploration

When relevant knowledge exists:

```text
Identify object -> Inspect state -> Read ASM -> Choose capability
-> Choose execution method -> Execute -> Verify
```

When a material unknown remains:

```text
Observe -> Define the knowledge gap -> Check reliable sources
-> Run a low-risk controlled probe if necessary -> Validate the conclusion
-> Update the ASM locally -> Continue the task -> Verify again
```

Do not enter a no-information loop of attempt, failure, identical retry, and random variation. Every action should be supported by existing ASM knowledge, current observation, a reliable source, a controlled test, or a reasonable inference marked as such.

## 0.4 Learn and update incrementally

An ASM is not immutable. Real operation, observation, failure, recovery, version changes, interface changes, and environment changes may reveal reusable knowledge.

Start a learning cycle when the current map cannot guide the next step, conflicts with observed behavior, lacks an important state or relationship, omits a useful method or limitation, or contains a less reliable execution or verification path.

Do not use irreversible or high-risk actions merely to acquire knowledge. Preserve recovery options, minimize scope, and request authority when the required experiment would delete, overwrite, publish, send, pay, modify important user data, or change system state.

---

# 1. Recommended ASM structure

An ASM may contain:

1. software identity, environment, scope, and boundaries;
2. sources and evidence levels;
3. important objects and relationships;
4. stable object identification and addressing;
5. decision-relevant states and their effects;
6. a goal-oriented capability tree;
7. observation methods;
8. control methods, selection rules, and result classification;
9. high-value operational contracts and workflows;
10. global decision rules;
11. failure and recovery models;
12. safety boundaries;
13. version and environment differences;
14. high-value unknowns;
15. validation status; and
16. incremental update records.

Name generated maps:

```text
ASM-<Software-Name>.md
```

Do not force every map to contain every section. Omit sections without execution value.

---

# 2. Identity and scope

Record the software name, version or range, operating system, interface language when relevant, target workflows, known extensions, available automation or control capabilities, explicit coverage, and explicit exclusions.

Use information already provided by the user. Ask only when missing information would materially change the path, result, or safety of the task.

---

# 3. Sources and evidence

Prefer sources in this order:

1. user-provided files, screenshots, recordings, project files, links, and constraints;
2. official documentation;
3. official source code;
4. official interface definitions;
5. official release notes;
6. direct observation of the target environment;
7. controlled tests; and
8. high-quality community material.

Label important knowledge:

- `verified`: directly observed or tested in the stated version and environment;
- `documented`: supported by a reliable official source but not tested in the target environment;
- `inferred`: derived from evidence and still needs confirmation;
- `unknown`: current evidence is insufficient.

Never invent menus, parameters, APIs, defaults, paths, errors, or success states. Do not present documentation as a live test or generalize one platform or version without evidence.

---

# 4. Important objects and relationships

Record the objects an agent must identify, select, create, modify, or delete, plus relationships that change targeting or impact.

Important relationships include containment, parent-child ownership, references, shared use, independent copying, deletion impact, and whether editing one object affects every place that references it.

Do not model every internal object type. Keep relationships whose omission could cause wrong-target edits, duplicate creation, or incorrect impact estimates.

---

# 5. Stable object identification

Prefer addressing methods in this order when available:

1. unique ID;
2. stable object reference;
3. complete object path;
4. parent + type + name;
5. type + name;
6. name;
7. interface position.

Later methods are usually more ambiguous. If several objects match, never silently choose the first. Use parent context, type, name, ID, path, and observable state to disambiguate. Ask the user only if the target still cannot be resolved safely.

---

# 6. Decision-relevant state

Record states whose misclassification could disable a capability, target the wrong object, repeat an action, misreport success, or create an incorrect result.

Examples include whether the application and project are open, the active document or object, current selection, mode or workspace, long-running operations, saved or modified state, permissions, focus, and pending or partially completed actions.

For important operations, record required pre-state, in-progress state, expected post-state, failure state, and any state in which repetition is unsafe.

---

# 7. Capability tree

Organize capabilities around user goals, stable objects, and real workflows. Do not copy menus, buttons, windows, or settings pages mechanically.

Expand the tree only until a leaf can be expressed as a clear operation. If several interfaces perform the same underlying action, keep one capability node and document the methods inside its operational contract.

---

# 8. Observation methods

An ASM must explain not only how to act, but how to read the current state.

Prefer structured, machine-readable, low-ambiguity observation over visual inference. Use visual observation when structured state is unavailable or the user-visible result itself must be judged.

Keep observation and control methods conceptually separate. A method that can execute an action may not be able to verify its result.

---

# 9. Execution methods and result classification

For important capabilities, record available methods, verified coverage, meaningful limits, the selection rule, and how the real result can be checked.

Choose the method that best fits the current task, expresses parameters clearly, behaves predictably, supports verification, depends less on screen position or focus, and minimizes side effects. Do not impose one universal interface ranking.

After execution, do not claim success merely because an interface returned success, a script did not throw, or a click completed. Inspect the real software state whenever possible.

Classify the outcome as:

- `success`;
- `failure`;
- `partial completion`; or
- `unverified`.

If the result cannot be checked reliably, use `unverified`.

---

# 10. Operational contracts

Use a complete contract for operations that are state-sensitive, parameter-heavy, available through several methods, failure-prone, easy to target incorrectly, destructive, difficult to verify, unsafe to repeat, or high impact.

A contract should contain the sections that add value:

## Operation name and goal

Use a stable name and describe the final user outcome, not a button.

## Applicable scenario and preconditions

State when the operation should or should not be used, and the required project, object, selection, mode, running-task, output-path, or permission state.

## Target object and disambiguation

Specify type, parent, unique ID, path, name, and ambiguity rules as needed.

## Material parameters

Record units, valid ranges, defaults, version differences, and constraints only when they materially affect the result and are not already clear from the interface schema.

## Execution methods and selection rule

List confirmed methods, their boundaries, and the condition under which each should be selected.

## Procedure and expected transition

Use short, explicit, conditional steps. Avoid vague instructions such as "configure correctly," "adjust as needed," or "make it look right." Record meaningful before-to-after state transitions.

## Success verification

Check the real object, attributes, software state, output file, readability, timeline, preview, or other observable user result. If this cannot be done, mark the result `unverified`.

## Failure, recovery, and retry safety

Record evidenced failure signals. After failure:

```text
Stop -> Read real state -> Determine failure/partial completion/success
-> Locate the cause -> Return to a controlled state
-> Retry, switch methods, or request intervention
```

State whether repetition is safe, requires a state check, or is unsafe. Pay particular attention to creation, key insertion, file writing, messaging, publishing, payment, deletion, movement, and renaming.

## Side effects and safety boundary

Record modifications to existing data, shared references, overwritten files, deleted objects, focus or active-object changes, external effects, resource use, cost, confirmation requirements, checkpoints, and recovery.

## Evidence

Record the source of state rules, parameters, behavior, tested environment, and known version range.

---

# 11. High-value workflows

A workflow combines operations into a real task. Record ordering, state dependencies, important branches, mandatory verification checkpoints, and the recovery position after failure.

Reference existing operational contracts rather than duplicating them.

---

# 12. Global decision rules

- Existing target: decide whether to reuse, modify, or create; do not duplicate automatically.
- Unknown critical state: observe before acting.
- First execution failure: inspect state and cause before retrying.
- Claimed success without verification: classify as `unverified`.
- Multiple execution methods: prefer higher reliability, clearer state, stronger verification, and fewer side effects.
- Existing user data: prefer the smallest sufficient modification.
- Irreversible action: establish a recovery point and request confirmation appropriate to the impact.

---

# 13. Failure and recovery model

Record software-level failure modes when useful: loss of response or focus, unexpected project state, stale interface state, invalid references or paths, missing extensions, insufficient permissions, version changes, and partially completed output.

Recovery principles:

1. stop expanding the impact;
2. preserve recoverable information;
3. observe the real state;
4. determine what already completed;
5. find the smallest recovery point;
6. recover rather than restarting blindly; and
7. request user intervention when safe judgment is impossible.

---

# 14. Safety boundaries

Mark deletion, overwrite, publishing, live output, sending, payment, credentials, permissions, system settings, and existing user data explicitly.

State what is affected, whether it is reversible, whether confirmation is required, how to create a checkpoint, and how to recover. "Be careful" is not a safety rule.

---

# 15. Version and environment differences

Record only differences that change an agent's decision or execution path: platform-specific menus, renamed functions, version-only interfaces, extension dependencies, or hardware-dependent behavior.

Do not build a large compatibility table without execution value.

---

# 16. High-value unknowns

Write `unknown` when evidence is insufficient. Maintain a short list of unknowns that materially affect current or likely future tasks and can become later validation work.

---

# 17. Context loading strategy

Large ASMs do not need to be loaded in full for every task. Prefer:

1. identity and scope;
2. current state rules;
3. the relevant capability;
4. the relevant operational contract; and
5. applicable failure and recovery rules.

Load other capabilities, workflows, and history only when needed.

---

# 18. Validate the ASM

Check:

- **Information value:** Does the map reduce exploration, or duplicate common knowledge and tool schemas?
- **Objects:** Can the agent identify the exact target and handle duplicate names?
- **State:** Does it know what to inspect before acting?
- **Capabilities:** Is the tree organized around goals rather than menus?
- **Observation:** Are important states readable through the least ambiguous method?
- **Control:** Are execution methods and selection rules clear?
- **Operations:** Do complex actions have preconditions, targets, and real success checks?
- **Failure:** Are useful failure signals, recovery, and unsafe retries documented?
- **Safety:** Do high-impact operations have concrete boundaries?
- **Size:** Can repetition or non-executable background material be removed?

---

# 19. Final value test

Assume a strong reasoning agent with general software-operation ability and some basic product knowledge, but no experience with the current version and environment.

Does this ASM provide information the agent otherwise lacks, more reliable state and target identification, better method selection, less pointless exploration, stronger result verification, and better failure recovery?

If it merely teaches the agent which buttons exist, revise it.

---

# 20. Incremental updates

After real operation, update only the knowledge affected by new evidence: object models, addressing, states, capabilities, observation, method mappings, contracts, selection rules, failure signals, recovery, version differences, and unknowns.

Preserve verified knowledge that remains valid. When direct testing conflicts with prior documentation, record the tested software version, platform, environment, conditions, and observed result. Do not generalize a local result without evidence.

---

# 21. Final goal

Without an ASM:

```text
Observe -> Guess -> Attempt -> Fail -> Guess again -> Switch method -> Repeat
```

With an ASM:

```text
Identify object -> Inspect state -> Choose capability and method
-> Execute -> Verify -> Complete
```

After failure:

```text
Recognize failure -> Re-observe state -> Determine partial completion
-> Use a known recovery path -> Continue safely
```

The value of an ASM must ultimately be demonstrated through real tasks, not by how large or complicated the document appears.

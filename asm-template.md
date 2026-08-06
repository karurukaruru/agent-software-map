# ASM: <Software Name>

> One-line description of what the software does.

## 0. Identity

| Field | Value |
|---|---|
| Name | |
| Version | |
| Category | |
| Platforms | |
| Summary | |

> **Scope:** State which windows, modes, or workflows this map covers.
>
> **Confidence:** Tested / Documentation-based, not tested / Mixed. Mark unresolved facts as `(unverified)` where they occur.

## 1. Sources

List the evidence used to build this ASM. Put user-provided material first.

- **User-provided:** <link, screenshot, sample file, manual, or reported behavior>
- **Agent-retrieved · Official:** <source>
- **Agent-retrieved · Direct test:** <test performed and observed result>
- **Agent-retrieved · Community:** <source and why it is credible>

## 2. Capability tree

Write the hierarchy down to actionable leaves.

```text
<Software>
├── Main window
│   ├── File
│   │   ├── Open
│   │   └── Export
│   └── Edit
│       └── Undo
└── Settings
    └── Output
```

## 3. Function cards

Create one card for every capability-tree leaf.

### [<Path>] <Function>

**Introduction**

- **Purpose:**
- **Entry point:**
- **Procedure:**
- **Success check:**

**Operational patches**

- Preconditions, state assumptions, destructive effects, version differences, common mistakes, recovery steps, or expert details.

<!-- Repeat until every leaf has a card. -->

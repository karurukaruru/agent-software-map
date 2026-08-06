# ASM: <Software Name>

> One sentence explaining what the software does.

## 0. Identity

| Field | Value |
|---|---|
| Name | |
| Version | |
| Category | |
| Platform | |
| Summary | |

> **Scope:** State which windows, modes, or workflows this map covers.
>
> **Confidence:** Tested / Documentation-based, not tested / Mixed. Mark facts that cannot be confirmed as `(unverified)` where they appear.

## 1. Sources

List the evidence used to create this ASM, with user-provided material first.

- **User-provided:** <link, screenshot, sample file, manual, or reported behavior>
- **Agent search · Official:** <source>
- **Agent search · Direct test:** <test performed and observed result>
- **Agent search · Community:** <source and why it is credible>

## 2. Capability Tree

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

## 3. Function Cards

Write one card for every leaf in the capability tree.

### [<Path>] <Function>

**Introduction**

- **Purpose:**
- **Entry point:**
- **Procedure:**
- **Success criteria:**

**Operational Patches**

- Preconditions, state assumptions, destructive effects, version differences, common mistakes, recovery steps, usage details, and so on.

<!-- Repeat cards until every leaf is covered. -->

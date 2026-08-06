---
name: agent-software-map
description: Create or update an Agent Software Map (ASM) that helps AI agents operate unfamiliar software safely and reliably. Use when a user asks to map a desktop app, CLI, web app, or API; document its capabilities and workflows; build function cards; or improve an existing ASM from documentation and observed behavior.
---

# Agent Software Map

Create a compact, evidence-aware operational map for an AI agent. Optimize for successful action, state awareness, and safe recovery—not for feature-list completeness.

## Use the standard structure

Start from [asm-template.md](asm-template.md). Produce these sections in order:

1. Identity
2. Sources and confidence
3. Capability tree
4. Function cards

Name the result `ASM-<Software-Name>.md`.

## 1. Establish scope

Record the software name, version or version range, platform, interface language when relevant, and intended workflows. State what is excluded.

Use information already supplied by the user before asking questions. Ask only when a missing choice changes the map materially or creates safety risk.

## 2. Gather evidence

Prefer evidence in this order:

1. User-provided files, links, screenshots, recordings, and constraints
2. Official product documentation, source repositories, release notes, and help text
3. Direct observation or a controlled test
4. Reputable community material for gaps only

Label each source and what it supports. Distinguish:

- `Verified`: directly observed in the named version and platform
- `Documented`: supported by an official source but not tested locally
- `Inferred`: a reasoned conclusion that still needs confirmation

Never convert a documented claim into a tested claim. Do not invent menu names, shortcuts, defaults, paths, or success states.

## 3. Build the capability tree

Organize capabilities by the user's mental model and the software's stable objects, not by every visible control.

Good top-level branches usually include:

- setup and identity
- content or object management
- input and output
- execution or runtime state
- diagnostics and recovery
- automation and integration
- safety and permissions

Stop expanding a branch when a leaf can be represented by one function card with one clear success condition. Merge duplicate paths that reach the same underlying operation.

## 4. Write function cards

Create cards for high-value leaves first. Every card must contain:

- **Purpose**: the user outcome
- **Entry**: the menu, command, screen, API, or prerequisite state
- **Procedure**: short ordered actions with decision points
- **Success check**: visible or machine-readable evidence of completion
- **Patches**: common mistakes, state traps, platform differences, recovery, and safety boundaries

Use interface labels exactly when known. Include alternatives only when they materially improve success.

For stateful or destructive actions, also state:

- preconditions
- affected data or output
- whether confirmation is required
- how to stop, undo, or recover

## 5. Make the map agent-usable

Write imperative, observable instructions. Replace vague phrases such as “configure correctly” with concrete fields, choices, and checks.

Teach distinctions that commonly cause failure—for example profile versus project, preview versus live output, save versus publish, or hidden versus deleted.

Prefer the smallest safe action. Require a pause before irreversible actions, public publishing, credential exposure, billing, deletion, or modification of existing user data.

## 6. Validate

Before delivery, confirm:

- all four required sections exist
- identity and scope are explicit
- every important claim has a source or confidence label
- capability leaves map to function cards
- every card has a success check
- untested procedures are marked as unverified
- risky actions have boundaries and recovery guidance
- terminology is consistent throughout
- relative links resolve
- the map does not contain secrets or private information

If direct testing is unavailable, deliver a documentation-based candidate and say exactly what remains to be verified.

## 7. Update incrementally

When feedback arrives, patch the affected identity field, branch, card, or platform note. Preserve validated content unless new evidence contradicts it. Record version-specific changes instead of silently rewriting them as universal behavior.

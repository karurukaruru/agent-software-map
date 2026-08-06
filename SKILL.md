---
name: agent-software-map
description: Create or update an Agent Software Map (ASM) that helps AI agents operate unfamiliar software safely and reliably. Use when a user asks to map a desktop app, CLI, web app, or API; document its capabilities and workflows; build function cards; or improve an existing ASM from documentation and observed behavior.
---

# Agent Software Map

## Goal

Create a concise software map that identifies evidence levels and can directly guide an agent's actions. Focus on successful execution, state awareness, and safe recovery rather than simply listing every feature.

## Standard Structure

Start from [asm-template.md](asm-template.md) and produce these sections in order:

1. Identity
2. Sources and confidence
3. Capability tree
4. Function cards

Name the result `ASM-<Software-Name>.md`.

## 1. Define the Scope

Record the software name, version or version range, platform, interface language when relevant, target workflows, and exclusions. Use information the user has already provided first. Ask a question only when a missing choice would materially change the result or create a safety risk.

## 2. Gather Information

Use this priority order:

1. Files, links, screenshots, recordings, and constraints provided by the user
2. Official documentation, source repositories, release notes, and help text
3. Direct observation or controlled testing
4. Reliable community sources used only to fill gaps

State what each source supports and distinguish among:

- `Verified`: directly observed on the specified version and platform
- `Documented`: supported by official material but not tested locally
- `Inferred`: reasonably deduced but still awaiting confirmation

Do not describe documented behavior as tested behavior. Do not invent menu names, keyboard shortcuts, default values, paths, or success states.

## 3. Build the Capability Tree

Organize capabilities around the software rather than mechanically copying every interface control. Common top-level branches include setup and identity, content or object management, input and output, runtime state, diagnostics and recovery, automation and integrations, and safety and permissions.

Stop expanding when a leaf can be expressed in one function card with one clear success condition. Merge duplicate paths that reach the same underlying operation.

## 4. Write Function Cards

Cover high-value leaves first. Every card must include:

- **Purpose**: the outcome the user wants
- **Entry point**: the menu, command, page, API, or prerequisite state
- **Procedure**: short ordered steps and necessary branches
- **Success check**: visible or machine-readable evidence of completion
- **Patches**: common mistakes, state traps, platform differences, recovery methods, and safety boundaries

For stateful or destructive operations, also state the prerequisites, affected data, whether confirmation is required, and how to stop, undo, or recover.

## 5. Make the Map Agent-Friendly

Use imperative language and observable conditions. Avoid vague directions such as “configure it correctly”; provide specific fields, choices, and checks.

Explain concepts that are easy to confuse, such as profile versus project, preview versus live output, save versus publish, and hide versus delete. Pause for confirmation before irreversible actions, public publishing, credential exposure, payment, deletion, or changes to existing user data.

## 6. Validate

Before delivery, confirm that:

- all four required sections are present
- identity and scope are clear
- important claims have a source or confidence label
- capability-tree leaves map to function cards
- every card has a success check
- untested procedures are labeled
- high-risk operations include boundaries and recovery guidance
- terminology is consistent and relative links work
- the map contains no private information

If direct testing is unavailable, deliver a documentation-based candidate and clearly list what still needs to be verified.

## 7. Update Incrementally

When feedback arrives, change only the affected identity field, branch, card, or platform note. Preserve verified content unless new evidence contradicts it. Record version differences explicitly instead of rewriting them as universal behavior.

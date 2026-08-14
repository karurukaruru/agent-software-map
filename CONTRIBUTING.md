# Contributing

Contributions are welcome, especially corrections based on direct use of a named software version and platform.

## Before opening a change

1. Run `python scripts/validate.py` from the repository root.
2. Keep `SKILL.md` concise and preserve its required YAML frontmatter.
3. Use `ASM-<Software-Name>.md` for generated maps.
4. Label claims as verified, documented, inferred, or unknown.
5. Give every high-value operational contract an observable success check, failure recovery, and retry-safety rule.
6. Preserve version and environment boundaries; documentation-only changes must not be described as live-tested.
7. Do not include credentials, private paths, personal information, or copyrighted manuals.

For software-map corrections, include the software version, platform, interface language, evidence source, and the exact object, state, capability, contract, or failure mode affected.

Use a focused pull request and explain how the change was validated. By contributing, you agree that your contribution is licensed under this repository's MIT License.

# Full list: implicit carrier decisions

## Scope

The source authority is `source/open-logic-config.sty`, pinned by SHA-256 in
the materialization receipt. Only the three declared carriers are admitted;
arbitrary macro expansion is deliberately excluded.

## Decisions

| Source carrier | Arguments | Decision | Review note |
|---|---:|---|---|
| `mTrue` | 1 | Enter the argument in math mode, then apply the typed Classical wrappers. | Confirm the finite contract if the upstream macro definition changes. |
| `mFalse` | 1 | Enter the argument in math mode with the source `\lnot` prefix, then apply typed wrappers. | Confirm notation and negation spacing against the target mathematical canon. |
| `TMtrans` | 3 | Type letters and numerals in all three arguments. | Literal `R`, `L`, and `N` in the third argument remain machine-direction symbols, not Arabic letters; review their presentation policy. |

The machine-readable findings list records every source location, argument,
disposition, authority hash, and reason:

`evidence/classical/repairs/implicit-math-intake-qualified-96175312/IMPLICIT_MATH_FINDINGS.json`

This source update is reversible and preserves the original formula indices;
the new carrier segments are appended rather than renumbering existing ones.

# Paired acceptance receipt — OLP-0021

Accepted 2026-08-14 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.

- Source: `content/sets-functions-relations/functions/function-basics.tex`.
- Canonical LF: 5,443 bytes, SHA-256
  `D1FA0923E303FC49A88D4E476C319D6E91A8088DE44C232DCFBA5878325FAEA3`.
- Declared CRLF: 5,583 bytes, SHA-256
  `F01A58D84A175F42D8C233EF0E7D41C23D406B54E8F11475C14514B64ECA3DC7`.
- Diagram asset `assets/diagrams/function.tikz`: SHA-256
  `CB994564115F1E1F2BE0E184ABB7614989FD9D89C94CE9B99FC74A614A58260D`.

Arabic target SHA-256
`A65EA58E8BDA3DAD299C8966FFFD7EA44D0B09FF7CDDE403F7A1A5D22539815D`,
commit `eeddc443d7d51fa78f2747fb715d1d835a66e04b`; Arabic ledger
SHA-256
`545F2AFD12CBE9D7F0F8B33852C1D111390D9C4E33BF0DA5C2CDA6959C61BEF7`.

Iranian-Persian target SHA-256
`D66599BDC39E09D80BCD3D02C257AEF308A2589E8B6F23C7791CB938E1F0EC83`,
commit `c7212ea7f10d444d71160c76a9f8d9c57191cb96`; Persian ledger
SHA-256
`069006FBB0C1B8254822299392245AB2EC87B37AE339E6D3DC413BAA9F6D73EF`.

Independent paired replay passed the exact 102-command sequence, 26
environment events, 66 math surfaces, eight glossary tokens, three structural
comments, two labels, one reference and asset binding. Semantic replay passed
the function definition; domain/codomain/range distinctions; figure direction;
all six examples; exact-one-value requirement; extensionality and its shared
domain/codomain proviso; and exhaustive, mutually exclusive cases. Unicode,
locale script, bidi and reader-facing leakage gates passed.

Both targets preserve rather than silently repair two source issues: the
`n`/`x` mismatch in `examplefunext`, and “positive square root” for a
function whose `Nat` domain includes zero (the principal root there is
nonnegative). The source claim that every positive integer has two real roots
`±√n` is valid and is not mislabeled as defective.

No build was run because the complete Functions driver still has missing
OLP-0022--0026 locale dependencies. Human/native and mathematical-specialist
review are absent. Cursor advances to OLP-0022, `function-kinds.tex`, declared
CRLF SHA-256
`6DFE2A70579F8E3521D8E2286E2360DD58A19FBEDA9718B62342105388AB4F93`.


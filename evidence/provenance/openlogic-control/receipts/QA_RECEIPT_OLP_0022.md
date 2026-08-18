# Paired acceptance receipt — OLP-0022

Accepted 2026-08-14 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.

- Source: `content/sets-functions-relations/functions/function-kinds.tex`.
- Canonical LF: 3,894 bytes, SHA-256
  `4D30902B7C66720AFABB8B079294106A685AEFBA0DC02CA10D9921BB554DB0AC`.
- Declared CRLF: 4,012 bytes, SHA-256
  `6DFE2A70579F8E3521D8E2286E2360DD58A19FBEDA9718B62342105388AB4F93`.
- Assets: `surjective.tikz` SHA-256
  `7083E6761874E930503FB0F9A4473A7177B65DA466B7AE5F443C86E53CD770A5`;
  `injective.tikz` SHA-256
  `6CB35D1950E2D1F34787EE0BDCC41FEE1678C8A9FC3DC910B10688C4EC2DCC21`;
  `bijective.tikz` SHA-256
  `38DACD080B28790B24B343F2F2DA36602792609481BC5AC4059D949904BE7F2D`.

Arabic target SHA-256
`6E4C12350566A5660C246B496A0F2A74E10BCE84B82977ED0D56FBA02FA049E8`,
commit `15aaed24e40bbfcaf73e260162f1ea6ef2c8cc2d`; Arabic locale config
SHA-256
`711563082DC943FB16351B16477C7FDB6DFD4262714BFBC2E93E262AA44EC7CA`;
Arabic ledger SHA-256
`325182A7139250A29E8319297A396CF06FEEC81FFCBFFEBDC347F750B5471A1F`.

Iranian-Persian target SHA-256
`335907D98A138C5062689AEAEC381AADE7BC3E1EE9CBD5371FB3A9C96F002180`,
commit `1dbea9a03604bab77ce0ea955302b091251eb544`; Persian locale config
SHA-256
`4661062C9D3709A61DC93D463BF70821BCE54D42E9CCCFBF3B897AFA3AB9B805`;
Persian ledger SHA-256
`10D5CE438DF08FF92976E64A683853D2A76FADF26E93EFE77C95172E29687A36`.

Independent paired replay passed the exact 97-command sequence, 28
environment events, 44 inline-math spans, two formal display bodies, 34
glossary-token surfaces, and all three references, labels, figure assets and
structural comments. All used glossary heads are locally defined, including
separate adjective and noun forms for injective/injection,
surjective/surjection and bijective/bijection; no English token fallback is
admitted.

Semantic replay passed the range/codomain distinction, existential and
at-most-one quantifiers, injective/surjective/bijective implications, all
examples, induced recodomain map, and one-to-one correspondence wording. The
source's malformed `\Setabs{f(x) \in B}{x \in A}` is preserved rather than
silently repaired and is recorded in both adverse ledgers. Independent QA
caused two exact corrections before acceptance: an Arabic plural-predicate
construction and the Persian term for successor function.

No build was run because the complete Functions driver still has missing
OLP-0023--0026 locale dependencies. Human/native and mathematical-specialist
review are absent. Cursor advances to OLP-0023,
`functions-relations.tex`, declared CRLF SHA-256
`0205F7168E0679F513E7C95EA7124CE364BCE36F9E04F06D519E90F6A5480A5C`.

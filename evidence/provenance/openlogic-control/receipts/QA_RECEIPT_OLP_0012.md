# Paired acceptance receipt — OLP-0012

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.

- Source: `content/sets-functions-relations/relations/relations-as-sets.tex`.
- Canonical LF Git blob: 5,251 bytes, SHA-256
  `2A67C6FB4846155E8E7CD8172FD1FB8214DB96D508CEAE5D70DEC95D5DFCC1FF`.
- Declared CRLF materialization: 5,376 bytes, SHA-256
  `412C6FA44EAD94F076DFEA7CD23F9E3CD748B08C1882DCB129B15F8EFCF5C29C`.
- Scope: scheduling unit 12 of 722; full unit, not a corpus checkpoint.

## Arabic (`ar`)

- Target SHA-256:
  `141BF3FF1EFD18E5180EB1183A9E0C2F2F103F2E1B1D5C8DD44C84C21CFBACE2`
  (6,951 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `48b60e3ec035c637c51b12d03ec8158dc0db248d`.
- Terminology/adverse ledger SHA-256:
  `F1A20AF608F2956150B1C34E611BD403E6868DF54EFBCA74C8D905F33D163111`.

## Iranian Persian (`fa-IR`)

- Target SHA-256:
  `500BD1C3E63E5F393715D55FC4E09D959FF6DAC961822912CE6FA37A8D934DE4`
  (7,380 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `4655c1cfb8e32155903d00fab3c488f7f86dcee2`.
- Terminology/adverse ledger SHA-256:
  `2EC144FC1B1C57606A5BE2C908F17BE2BD29A1B2E5FA6E52752284B89758C768`.

## Gate result and caveats

Independent read-only replay passed both complete targets. Each preserves all
83 source math segments, the 169-command multiset, the exact seven-environment
topology, identifiers, two references, one label, two glossary markers,
ordered tuples and matrix geometry. Manual semantic replay confirmed every
iff direction, quantifier, negation, relation polarity and final disjunction.
Unicode normalization, language-script separation, prohibited bidi controls
and reader-facing-English gates passed.

The source defines identity as `\Id{A}` and later uses an unexplained bare
`I` in `K=L\cup I` and `H=G\cup I`. Both translations preserve that exact
source ambiguity and record it in their own adverse ledgers; no silent repair
was made.

No build was run. OLP-0012 is import-free and references accepted units, but
the OLP-0011 chapter driver still lacks localized OLP-0013--0019 dependencies;
building it now could admit hidden English fallback. Human/native review is
absent for both locales.

The shared cursor advances to OLP-0013,
`content/sets-functions-relations/relations/reflections.tex`, declared CRLF
SHA-256 `1F94C1032EAEDB73B1DE69E6F010B8E0C7437FE240AB280583FF358896FA4B27`.

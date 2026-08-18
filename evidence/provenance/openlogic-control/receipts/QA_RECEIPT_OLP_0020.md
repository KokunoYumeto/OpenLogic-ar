# Paired acceptance receipt — OLP-0020

Accepted 2026-08-14 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
`f67757bb9305b173634082ab4cefd5601a707a34`.

- Source: `content/sets-functions-relations/functions/functions.tex`.
- Canonical LF Git blob: 399 bytes, SHA-256
  `D68BBA27E593DF2C17E2DC93B34256D829361B04134B4A962B997D5F4A230A59`.
- Declared CRLF materialization: 425 bytes, SHA-256
  `CE481E97A8F301C749D1461326B4EE3D0792B4ADC15A1FCEB7C6ED3B58CECA54`.
- Scope: complete scheduling unit 20 of 722, the Functions chapter driver;
  not a publication checkpoint.

## Arabic (`ar`)

- Target title: `الدوال`.
- Target SHA-256:
  `87007C764C936301137307BC9F64660D9380A171A7D72E60D0E775F017E9E635`.
- Branch/commit: `codex/openlogic-ar`,
  `23028b77bd0594e3ee9fb305fedd35b828922837`.
- Terminology ledger SHA-256:
  `F905AB3BA10360FA678628B08FDBC16725BE527FAB07749CD7CBA1451F1BABE0`.

## Iranian Persian (`fa-IR`)

- Target title: `توابع`.
- Target SHA-256:
  `D788EBF360B902A4EE9B4EE92E6EA1B59499EDB8AEB6DE00E88B0FDAD0144964`.
- Branch/commit: `codex/openlogic-fa-ir`,
  `96370559bb0b5d705a46bfe9e93c44503c0f3c74`.
- Terminology ledger unchanged, SHA-256:
  `646E81FB53721E7629B9C38C735DBB6F1136FB43CE60F210D42C8E01D4895429`.

## Gate result and caveats

Independent read-only replay passed. Each target is byte-identical to the
canonical LF source after replacing only the reader-facing title. The exact
12-command sequence, two environment events, source comments, six active
imports and their order are preserved. The `isomorphic-functions` import
remains exactly commented and was not silently admitted. UTF-8, NFC, script
separation and reader-facing leakage gates pass.

Build is correctly deferred: all six imported locale children OLP-0021--0026
are absent, and compiling the driver could admit hidden English fallback.
Human/native and mathematical-specialist review remain absent.

The paired cursor advances to OLP-0021,
`content/sets-functions-relations/functions/function-basics.tex`, declared
CRLF SHA-256
`F01A58D84A175F42D8C233EF0E7D41C23D406B54E8F11475C14514B64ECA3DC7`.


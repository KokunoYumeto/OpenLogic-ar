# Paired acceptance receipt — OLP-0011

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. The scheduling source is
`content/sets-functions-relations/relations/relations-complete.tex`.

- Declared CRLF materialization: 438 bytes, SHA-256
  `7E1363F3E757004246334478742E4199101DBB2551FAC272462454CD40161E23`.
- Canonical LF Git blob: 410 bytes, SHA-256
  `9720780FCF56A05F8F18C26234D7BEBC24024116BB6549A151E0905845B41EF5`.
- Scope: scheduling unit 11 of 722. This is a structural chapter driver, not a
  complete reader or corpus checkpoint.

## Arabic (`ar`)

- Target: `locale/ar/content/sets-functions-relations/relations/relations-complete.tex`.
- SHA-256: `9C8A89C1E7A5AE14A2E917C358920E5FB1FBEBB51488FA4CAE326E3DE50DD303`
  (426 bytes).
- Branch/commit: `codex/openlogic-ar`,
  `356f567d1638cf58ebff5afc230cfa7ccaffa28a`.
- Chapter title: `العلاقات`.

## Iranian Persian (`fa-IR`)

- Target: `locale/fa-IR/content/sets-functions-relations/relations/relations-complete.tex`.
- SHA-256: `3FE8611344F06A83F8CDADF3E96B4867F06511E551E9770602A14475FFA291E6`
  (411 bytes).
- Branch/commit: `codex/openlogic-fa-ir`,
  `190c6b9dfccbae2c65ef518a453bfca653153470`.
- Chapter title: `روابط`.

## Gate result and caveats

Independent read-only replay passed for both targets. Each preserves the exact
document class, `sfr`/`rel` identifiers, eight optionless imports in exact
source order, single chapter hook, environment sequence and document bounds.
Both pass NFC, script-separation, reader-facing-English, prohibited-bidi-control
and structural-equivalence checks.

Build is correctly withheld at this point: all eight locale dependencies
OLP-0012--0019 are absent, so a cumulative compile could silently import
English source. This is `BUILD_DEFERRED_FOR_DEPENDENCY_CLOSURE`, not a semantic
or structural target failure. Human/native review is absent for both locales.

The shared accepted cursor advances to OLP-0012,
`content/sets-functions-relations/relations/relations-as-sets.tex`, declared
CRLF SHA-256
`412C6FA44EAD94F076DFEA7CD23F9E3CD748B08C1882DCB129B15F8EFCF5C29C`.

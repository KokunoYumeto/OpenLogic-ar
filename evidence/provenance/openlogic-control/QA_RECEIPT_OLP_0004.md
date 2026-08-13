# Paired acceptance receipt — OLP-0004

Accepted 2026-08-13 against official Open Logic commit
`9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Source
`content/sets-functions-relations/sets/sets.tex` has SHA-256
`EEA34D38BB52811468A0025D348457A0F4D3F44AAE4B7CABB28551D6328E2785`.

- Arabic title `المجموعات`; target SHA-256
  `B1C50900475E2F94BF13435C7A5069F6BC6820C7F8D2D3B5C49321E521088ECF`;
  accepted commit `4ceee0dd4d1486d9932261658e3152da0a63136a`.
- Iranian-Persian title `مجموعه‌ها`; target SHA-256
  `DF9B514CCED39A35FA88B65A53659B7207D7E899F8B48CF08066E611752850C9`;
  accepted commit `a48b835c374a56fa722ef0b33391f029cca2f7c4`.

Both pass exact document class, `\olchapter{sfr}{set}`, six ordered imports,
chapter-end hook, NFC, brace, script-separation and independent-AI title checks.
No new terminology decision was needed; both ledgers remain unchanged.
`human_review=none`; no correction was required.

`build_not_run=dependency_closure`: this chapter driver imports six untranslated
reader units, so an immediate build would create hidden English fallback. No
PDF or publication checkpoint exists. The shared cursor advances to OLP-0005.


# OLP-0001 Arabic build and QA receipt

- Locale/register: `ar`, global formal Modern Standard Arabic.
- Unit: `OLP-0001`, `content/open-logic-about.tex`.
- Source authority: Open Logic commit `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`.
- Source SHA-256: `E4F2E2EC5D9957FA71DF41E9ED100641FE08230F63AF6065EAAFCB3D37346F4A`.
- Target SHA-256: `3DFDAB30491A82C494D48ED98D8D1D81F3778C831C934CD3EB9DC94FFAAF400D`.
- Locale SHA-256: `7F1B34A57BD396F63218DF69E6E879D5E931CB9D883B4A9C65B607D152D9FBAB`.
- Config SHA-256: `744C2E9590E24E91D22FF31E825CC3D9575FDEC307B95069FF6E86DCB6B90BC2`.
- Driver SHA-256: `0480F9696EC067E93732DA80FACBDDB20A205B2AE410B3B84A9AE4C7ED90EB82`.

## Checks completed

- Source/target semantic replay: all nine propositions in the source About text preserved, including the incomplete/draft caveat, planned features, six CC reuse verbs, attribution condition, and both destinations.
- Static parity: PASS. Source path/hash, ordered structural commands, two URLs, heading/outline text, 25 caption keys, 15 `cleveref` keys, nine boilerplate macro signatures/placeholders, balanced braces, NFC, and script-residual gates pass.
- Independent post-correction AI replay: PASS for all nine semantic propositions, exact structure/URLs, locale contract, build log, localized metadata/outline, link annotations, and full-page visual rendering.
- TeX source has no embedded bidi-format controls, presentation-form characters, Persian leakage, or unapproved English prose. `LaTeX`, URLs, domains, and named technical brands are intentionally invariant.
- Build: two serial passes of `lualatex -interaction=nonstopmode -halt-on-error about-ar.tex`; LuaHBTeX 1.25.7 / MiKTeX 26.5. No fatal error, undefined control sequence, missing character, overfull box, or underfull box was reported.
- Nonblocking build warnings retained in the log: repeated upstream `hyperref` option, two upstream file-provides-name warnings, font-language declarations, and deprecated memoir `\addtodef` use.
- A post-QA hygiene change replaced an intentional literal trailing TeX control-space with the equivalent `\space`; static checks and both build passes were replayed afterward.
- PDF metadata was subsequently moved from the locale-wide config into this
  unit's driver so later units cannot inherit the About title. Both build
  passes were replayed; extraction and the full-page render remained
  byte-identical to the accepted witnesses.
- PDF: one Letter page, 51,534 bytes, SHA-256 `A62B8FD0B5C4AFC94FE7F17E9B7BE46559AB818DCC9559B5A47D10D3547D5456`.
- PDF metadata and outline title are both `حول مشروع المنطق المفتوح`; author metadata is `مشروع المنطق المفتوح`.
- Link annotations: exact URIs `https://github.com/OpenLogicProject/OpenLogic/wiki/Contributing` and `http://openlogicproject.org/`.
- Current two-pass log SHA-256:
  `D6EE04F0E744FB04838B6898C590BB6F28E4E1D3E1FFE0666310B7E5813BA511`.
- Visual QA: PASS on the complete one-page PDF rendered at 144 dpi. No clipping, overlap, broken shaping, or Latin/RTL collision was seen. Render witness SHA-256 `50D729A544CC46B76D724091281D9D55927AF713ADC8996938BCD5C23F1BEF51`; temporary PNG deleted after inspection.
- Extraction witness: 1,482 characters; zero U+FFFD; zero Arabic Presentation Forms; U+202A/U+202B/U+202C counts 26/13/39. Extracted-text SHA-256 `A242EA1F98A47C17993D987575BF438D14026258C17FF1C5FA0A0A693AE39374`.

## Honest limits

- The PDF is not claimed to be tagged-PDF or accessibility certified. Babel/LuaTeX inserts directional controls in extraction, and adjacent punctuation around the displayed Latin domain is not guaranteed to copy in the same order in every extractor.
- `human_review=none`. The independent AI replay does not stand for native-community certification.
- This is one accepted scheduling unit in a 722-unit complete-edition closure, not a complete Open Logic Arabic edition and not a publication checkpoint.

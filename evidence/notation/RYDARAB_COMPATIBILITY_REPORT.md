# RyDArab and RamzArab compatibility report

## Result

The preserved packages are valuable design evidence, but they are not a safe production backend for the current 722-unit LuaLaTeX corpus. The release therefore reproduces their explicit east/west numeral choice through a narrow, modern presentation profile and retains the archives as provenance.

## Exact evidence

- `ramzarab-wayback-20060526001937.zip`: 520,455 bytes; SHA-256 `10BAC213CB217049C9557071400C6822E0B89A41CF643643977A270887B71F6E`; 13 extracted files; LPPL 1.2-or-later material; legacy 8-bit font encoding.
- `sys90334-wayback-20060620150906.zip`: 1,759,718 bytes; SHA-256 `ACF0F5BB003D0FFE54E9898A3B328A987F04C7D86C9F8FC1D73E706D5F3B7BA9`; 211 extracted files; `rydarab.sty` identifies version 1.4 dated 2003-03-03 and requires ArabTeX.
- W3C public-math message dated 2013-11-18: `w3c-2013-0017.html`, 15,033 bytes; SHA-256 `14DD89B245CF52F690EB318B4EF4ED840EED3955F14BEFF348C18DBBBF97F170`. It links a later v1.7 RAR on the vanished original host. One bounded original/Wayback retrieval established that those exact RAR bytes are unavailable.

## Incompatibilities

1. `\amarabmath` installs `\amrl` into every inline and display formula. `\amrl` recursively reverses the TeX token stream, which changes multi-digit numbers, function names, and structured expressions.
2. `amrename.tex` globally rebinds commands including `\sqrt`, `\lim`, `\frac`, delimiters, relations, arrows, scripts, and named functions. This conflicts with the modern Open Logic style stack and makes semantic equivalence difficult to prove.
3. The package depends on ArabTeX transliteration and METAFONT/8-bit symbol fonts rather than the repository's UTF-8, HarfBuzz, and Unicode Arabic source architecture.
4. The archived manual documents display-mode and argument-bracing restrictions that the frozen 722-file corpus does not satisfy.
5. The manual contains overlapping copyright prose, while its package headers specify LPPL. Reusing only the independently implemented numeral-profile idea avoids copying ambiguous implementation material.
6. RamzArab's bundled TrueType font declares OS/2 `fsType=8` (restricted embedding), so it must not be embedded in a public PDF.

## Modern digit-face provenance

- Upstream font: XITS Math 1.302, 548,096 bytes; SHA-256 `3025792ADB0B7072ACE08BF5726D341DE32F2254612DDEC6DD98271A8DD29689`; embedding `fsType=0`.
- Upstream license: SIL Open Font License 1.1, 4,998 bytes; SHA-256 `10C83ACB7BF240C6E263906E0905C8E419F3483C89141E83243465C221D322AD`.
- Reproducible derivative: `OpenLogicMachrekDigits-Regular.otf`, 535,528 bytes; SHA-256 `C4F290FB671B1EDF554BD57D31C6CD40CE88099FCA70B8B46B32B3F792A7D7AF`; embedding `fsType=0`; all primary names changed to avoid XITS/STIX reserved names.
- The derivative changes only the cmap entries for U+0030--U+0039: each ASCII slot draws the corresponding XITS Arabic-Indic outline from U+0660--U+0669. It retains the source character code, formula order, and machine-extracted ASCII digit semantics.
- A direct literal-U+0660 math-node probe triggered a reproducible luaotfload/HarfBuzz assertion inside Arabic paragraphs. The remapped ASCII slots avoid that engine defect and passed the same probe with the digit face embedded and ToUnicode enabled.

## Adopted compatibility model

- International profile: source math digits U+0030--U+0039 remain visually 0--9.
- Machrek profile: the same U+0030--U+0039 source math tokens render with Arabic-Indic U+0660--U+0669 outlines through style-aware math-active glyph boxes and a renamed OFL digit face.
- Both profiles keep LTR formula structure, Latin/Greek variables, Greek sigma, citations, identifiers, URLs, and all 722 translated files unchanged.
- Arabic decimal and thousands separators are available only as explicit macros for future author-audited loci; no blind punctuation substitution occurs.

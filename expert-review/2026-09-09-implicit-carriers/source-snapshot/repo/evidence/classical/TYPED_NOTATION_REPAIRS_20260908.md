# Classical Arabic notation: corrections and remaining visual problems

This is a technical supplement to the expert-review register. No Arabic wording
was changed in this pass. These decisions concern how the existing notation is
printed and how exact English/MSA/Classical source identities are preserved.
The complete Classical reader is not yet accepted or published.

| Place to check | Decision and reason | Evidence and current status |
| --- | --- | --- |
| Sets, basic notation: `sets-functions-relations/sets/basics.tex`, line 31 (`a_1, ..., a_n`) | Put each generated letter/numeral wrapper in one TeX group. Respect the original single-token argument boundary: `x_12` must not acquire the meaning of `x_{12}`. | Corrected in the materializer. Exact-inverse tests and actual control/RTL script positions pass. |
| Mathematical letters and digits in subscripts and nested subscripts | Preserve explicit spaces before the native font loader's `at` size keyword. Spaces written normally inside the expl3 syntax region were discarded, causing every requested size to load at the default size. | Installed `fontspec-luatex.sty`, lines 478 and 482, supplies the primary implementation pattern. The fresh PDF shows normal/script/nested-script sizes of 14.3462, 9.96264 and 6.97385 PDF points. |
| Graph examples: `sets-functions-relations/relations/graphs.tex`, lines 41–60 | Keep internal node names `(A)`, `(B)`, coordinates and dimensions such as `2cm` unchanged. Convert the explicitly printed node formulas, not the diagram's implementation data. | Corrected. Both source graph examples compile; exact source reconstruction passes. All 722 presentation units were regenerated and verified. A separate label-placement defect remains, below. |
| Same graph example, line 51 (`intertext`) and other text boxes containing explicit formulas | Re-enter mathematical conversion inside explicitly delimited formulas. Protect ordinary text, keys, international specimens and styled names independently. | Corrected in the same bounded parser repair. Six new regressions and the existing suites pass (61 tests total). No arbitrary macro expansion or implicit/generated math-label recognition is claimed. |
| RTL square roots and indexed roots | The radical face must be reflected without reflecting its radicand or degree. Moving the old left-facing root glyph to the right is insufficient. | Open defect, directly confirmed in PDF font/content streams. See [Unicode UTR 25 revision 15, §4.2, printed p. 37](https://www.unicode.org/reports/tr25/tr25-15.pdf). No claim of complete RTL typography is made. |
| RTL graph diagrams, nodes 2, 3 and 4 | Keep each printed number inside its corresponding node circle while preserving the source diagram geometry and RTL mathematics in labels. | Open runtime defect: the current source repair compiles, but the actual RTL PDF places labels outside their circles. The first isolated direction candidate failed the same containment check and was rejected. |

The notation occurrence ledger remains machine-readable at
`NOTATION_MATERIALIZATION_DECISIONS.json`: each source occurrence has its exact
location, original token(s), chosen presentation or explicit exemption, reason,
and reversible replacement. Its current SHA-256 is
`2aeb8fb72c1abfc1b7a9d44f69539b33175182171637455f998eb473a89318c8`.
It records 103,242 occurrences and 67,433 replacements across 722 units.
That coverage is a notation-transform inventory, not proof that every Arabic
translation choice has been justified against the canon.

Exact test/build/visual identities and failed predecessors are retained in the
source-bound receipts and the Arabic owner's continuation log. Findings remain
open to correction when stronger source or expert evidence becomes available;
expert participation is not required to continue production.

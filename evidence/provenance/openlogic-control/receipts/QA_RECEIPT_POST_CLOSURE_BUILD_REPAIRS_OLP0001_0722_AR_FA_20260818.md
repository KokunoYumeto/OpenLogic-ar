# QA receipt — post-closure Open Logic build repairs, Arabic and Persian

Date: 2026-08-18

Status: `PASS_POST_CLOSURE_TARGET_REPAIR_REPLAY_722`

## Authority and predecessor

- English authority: Open Logic commit
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`, tree
  `f67757bb9305b173634082ab4cefd5601a707a34`.
- The complete source binding remains
  `E5FBD3773FF80F2195E6EFA023EE51573E778BDF20629D3377B16FA09883FE51`.
- The historical complete-closure receipt is
  `QA_RECEIPT_COMPLETE_CLOSURE_OLP0001_0722_AR_FA_20260817.md`, SHA-256
  `8A0D50B4A9C58AD79A48AC85F2D0CA7BD4B58336C2F4ACFF531A0D28A2E4D069`.
  It correctly binds the earlier target bytes and is not rewritten.
- Its predecessor manifest SHA-256 was
  `3C9CE896A7FACE74BE840616ED9F46343079B300F0F72033DFF6DEA9026DFE53`;
  its predecessor complete paired target binding was
  `B6FEFA17CAA8B1BCDF891DC92B43CFDD9B3B2274830C1D024FE2AA0AB177B944`.

## Retained correction inventory

Each current edit was reconstructed against the historical hash. Reversing the
listed edit reproduces the predecessor target SHA-256 exactly, so the changes
below have byte-level provenance rather than merely plausible current content.

| Unit | Locale | Target path | Previous SHA-256 | Current SHA-256 | Bytes / LF | Rationale |
|---|---|---|---|---|---:|---|
| OLP-0040 | ar | `locale/ar/content/sets-functions-relations/size-of-sets/reduction-alt.tex` | `7DF9A4A307A810E394C64ADEEB709857F05C19BB4B41FC7E5717551780119AC3` | `83B410552D13D96039CA6801C980A065DFF71001B2FEDDB4FAB05CA0060766B0` | 6,515 / 133 | Give the alternative reduction problem its distinct `red-alt` label. |
| OLP-0040 | fa-IR | `locale/fa-IR/content/sets-functions-relations/size-of-sets/reduction-alt.tex` | `85E9046344BA21E68A36BB0B741872847BF08AE44D4B21CFBA38478C72824347` | `9C15BF0A9A05128C40C63D42D8323D9CC9F060FAFA7AEA9FCF568154EC02522A` | 7,255 / 138 | Apply the same duplicate-label repair independently in Persian. |
| OLP-0205 | fa-IR | `locale/fa-IR/content/model-theory/lindstrom/abstract-logics.tex` | `BA50D9DE92C4CAEEC915938E6C5294F8663E7FBB4C1FCC6DA62291FF079503FE` | `1B4FB6F802862BCC7F938CE41982B95583258E5B5493A4F4C36268A49E45013A` | 8,899 / 153 | Repair malformed `\notmodels_L` as `\not\models_L` once. |
| OLP-0206 | fa-IR | `locale/fa-IR/content/model-theory/lindstrom/ls-property.tex` | `6388BDC1AEA97EDC3C286049B9E2263F2EC8B1DACEA7EB5CDE27A5930D5A6326` | `21040A57FA83DF913783EF3A9E69825B1CE6F84E14E985199C886D073C7039D3` | 7,531 / 133 | Repair the malformed negated-models command at three loci. |
| OLP-0207 | fa-IR | `locale/fa-IR/content/model-theory/lindstrom/lindstrom-proof.tex` | `40C84157C7E2BCABF0E94F6EDC06003D26DD96D598990F2730F82946AAF7306F` | `3ECB1CC1AC3BF6FD8C6F5B8DD4C495E3FE49735F585B0BFF8F27E9FC0BC75749` | 8,853 / 148 | Repair the malformed negated-models command at three loci. |
| OLP-0326 | ar | `locale/ar/content/second-order-logic/syntax-and-semantics/satisfaction.tex` | `BAA97BE552D1F87BA8072E62617D0C6ECF41FE561A376C5164F5B66D5AF528B2` | `2E145D41AB40F5F31ABADF4A6BD7CED648AB653E440D30EAD4AA4AC9D57BDE6E` | 10,374 / 215 | Move Arabic punctuation into `\text{}` inside a mathematics case. |
| OLP-0368 | ar | `locale/ar/content/lambda-calculus/church-rosser/definitions-and-properties.tex` | `5C05544133FFCE85E35126C72CD8398DE9759CFB3C0F527686505DC8C81F92F9` | `3872A6ED8F0B3CB7171D252D447F862C982019417BAD13EA441C09F4C174E27E` | 4,375 / 80 | Contain an Arabic comma in text mode rather than the math font. |
| OLP-0379 | ar | `locale/ar/content/lambda-calculus/lambda-definability/fixpoints.tex` | `F068E4A0DAA43328C6A492DBB2BFCD4434E78977D04353DA87640546B0DF4F36` | `981675ED034DE19AAEA17B35F45D8BDFC8BE392F426D4ED25DAD9C1F292E2F2C` | 8,279 / 169 | Move the Arabic comma into the adjacent text group. |
| OLP-0416 | ar | `locale/ar/content/normal-modal-logic/syntax-and-semantics/tautological-instances.tex` | `01A3D69439398A1F4D42CFE1B4AC372799BC6C8DEF4CFBCE33D2865B00124263` | `56F7375BA5E4C7BF6F73A86A6717C5BE805F7BE63BB518D552ACBE3B184567AC` | 7,345 / 161 | Move two Arabic semicolons into text mode. |
| OLP-0427 | ar | `locale/ar/content/normal-modal-logic/axioms-systems/axioms-systems.tex` | `9B2F44E0B3F83BBF94B139C3D6E139BF45FDF9D502348774E03A7F31C843BB78` | `DC692BE256975B043CEBF4584DA333415D4EEDB12350009E156D6BCCB644B572` | 570 / 26 | Restore immutable `\usetoken{P}{derivation}` and remove a redundant terminal LF. |
| OLP-0429 | fa-IR | `locale/fa-IR/content/normal-modal-logic/axioms-systems/normal-logics.tex` | `83F54C01059D045A101DEFA3507F13C8D594116B5D2AA19EA8310D5F752874F1` | `6BB32BC7ECC9E8DDF99AD94A4E63541C691328522F9695EFCD94E0592E013395` | 6,082 / 122 | Move the Persian semicolon outside display mathematics. |
| OLP-0430 | ar | `locale/ar/content/normal-modal-logic/axioms-systems/logics-proofs.tex` | `E16F83BC55C1C47B6C98F89471C634FE382C6D90A5D80990EBA0EC07A438D199` | `1A45434F49B4A5C0FAAC515EE5F749563F63F16BB6E003AD4A57980DDA60126B` | 5,545 / 92 | Restore immutable `\usetoken{P}{derivation}`. |
| OLP-0434 | ar | `locale/ar/content/normal-modal-logic/axioms-systems/duals.tex` | `E4693B8A18A6175C41F410D0392521D7E848E4D12234E1FB0A5F3FD0BA53BC48` | `9ADE4688CA1340DBAE188F19FCFC34B028DF50510929F87E2F4EA1E6DA8CDF1C` | 1,375 / 41 | Restore immutable `\usetoken{P}{formula}`. |
| OLP-0438 | ar | `locale/ar/content/normal-modal-logic/axioms-systems/provability-from-set.tex` | `067AD4E2B2661EDD13527B87CFAF5E18D6E1EDA2766B1DD34730C761BD7CBC03` | `86D14EF6C0E2EDCCFE57BF59A45EA8487C550CE9EA17F181D0D44C114024FA8F` | 894 / 25 | Restore immutable `derivability` and `formula` token keys. |
| OLP-0619 | ar | `locale/ar/content/methods/induction/relations.tex` | `705148276FA10C1B1AF8D7ED38F0353CA7CC55ABC122E987A38ED02C14C7F973` | `8E1DA73B83054CDABAB24BD065FF90CF1F3A2CD9B9B75170FF1923F98B5A752D` | 9,696 / 187 | Restore three missing TeX row-terminator backslashes and contain the Arabic comma in text mode. |

## Complete bounded replay

The replay resolved only the 722 source paths and 1,444 target paths named by
the closure manifest. It found zero missing files, source-pin mismatches,
target-hash mismatches, ordering defects, strict-UTF-8 failures, CR bytes,
BOMs, NFC failures, forbidden bidi controls, or Arabic/Persian glyph-policy
violations.

- Source files: 722; bytes: 3,051,826; LF bytes: 75,457.
- Arabic targets: 722; bytes: 3,643,058; LF bytes: 73,206.
- Persian targets: 722; bytes: 3,948,090; LF bytes: 75,389.
- Updated closure-manifest SHA-256:
  `20BEA057CAD50409B1B228EFA1D430BFE19833400F706EF4F4CDD631C446737B`.
- Updated complete paired target binding, over stable-order Arabic-then-Persian
  rows `closure_id|locale|target_path|UPPER_SHA256|bytes|LF_count`, joined by
  LF with no final LF:
  `E356DA1C7D7AB7D61AA9CBFCC093EF567DC69D18839180C02352B234A1A3C6B3`.

## Limits

This is an append-only correction receipt. It does not rewrite or invalidate
the historical tranche receipts; it rebinds the current exact target bytes
after later build-facing repairs. No Git operation, publication, upload, or
native/human review occurred. A fresh complete dependency build, PDF
convergence, all-page render and extraction/accessibility replay remain
separate gates and are not claimed here.

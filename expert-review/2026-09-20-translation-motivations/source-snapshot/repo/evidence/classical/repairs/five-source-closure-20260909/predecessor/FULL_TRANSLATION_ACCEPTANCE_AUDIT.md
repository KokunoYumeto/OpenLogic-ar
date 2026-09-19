# Full translation acceptance audit

Status: **PASS**

This deterministic continuation accepts 722 units and 2166 live English/MSA/Classical bindings. It preserves the original v1 FAIL audit byte-for-byte and resolves each of its eight blockers through named continuation evidence; it does not rewrite the historical reviews as contemporaneous records.

## Acceptance counts

| Measure | Count |
|---|---:|
| `unit_count` | 722 |
| `live_source_bindings` | 2166 |
| `range_count` | 8 |
| `historical_blocker_count` | 8 |
| `resolved_historical_blocker_count` | 8 |
| `owner_followup_finding_count` | 4 |
| `blocking_finding_count` | 0 |

## Range acceptance

| Range | Units | Result | Continuations |
|---|---:|---|---|
| 0001-0100 | 100 | PASS | `FTA-COVERAGE-0044-0050`, `FTA-078-I1` |
| 0101-0200 | 100 | PASS | `FTA-0118-I1`, `C184-01`, `C185-01` |
| 0201-0300 | 100 | PASS | — |
| 0301-0400 | 100 | PASS | — |
| 0401-0500 | 100 | PASS | `FTA-0488-0490-M1`, `0452-I1`, `0452-I2`, `0452-I3` |
| 0501-0600 | 100 | PASS | `FTA-0588-N1` |
| 0601-0700 | 100 | PASS | `FTA-0643-WEAKGEN` |
| 0701-0722 | 22 | PASS | `FTA-0713-M1` |

## Historical blocker continuation chain

| Historical finding | Units | Resolution evidence |
|---|---|---|
| `FTA-COVERAGE-0044-0050` | OLP-0044, OLP-0045, OLP-0046, OLP-0047, OLP-0048, OLP-0049, OLP-0050 | `evidence/classical/reviews/0001-0050.json#/units/43-49`<br>`evidence/classical/repairs/0001-0100.json`<br>The formerly unreviewed seven-unit gap now has explicit non-pending unit verdicts, substantive review notes, and empty issue lists. |
| `FTA-078-I1` | OLP-0078 | `evidence/classical/repairs/0001-0100.json#/repairs/24`<br>The finite-support and monotonicity repair is recorded as continuation 078-I1 and is included in the current source preflight. |
| `FTA-0118-I1` | OLP-0118 | `evidence/classical/repairs/0101-0200.json#/finding_dispositions/7`<br>The self-contained support-reserve and freshening proof is recorded as repaired in both Arabic layers. |
| `FTA-0488-0490-M1` | OLP-0490 | `evidence/classical/repairs/0401-0500.json#/finding_dispositions/7`<br>The neighborhood/propositional-letter repair is recorded in both Arabic layers and rebound by the fresh preflight. |
| `FTA-0588-N1` | OLP-0588 | `evidence/classical/repairs/0501-0600.json#/finding_dispositions/11`<br>The formerly Classical-only omission is repaired in both Arabic layers and accepted in the continuation ledger. |
| `FTA-0643-WEAKGEN` | OLP-0643 | `evidence/classical/repairs/0601-0700.json#/finding_dispositions/14`<br>`evidence/classical/repairs/0601-0700.json#/validation/independent_formal_reviews/1`<br>The proof now uses freshened eigenconstants and a bijective constant swap covering Q1/Q2, identity, MP, and both QR forms. |
| `FTA-0713-M1` | OLP-0713 | `evidence/classical/reviews/0701-0722.json#/findings/0`<br>The modal-systems scope qualifier is explicitly resolved in both Arabic layers. |
| `FTA-OWNER-INTEGRATION-0101-0700` | OLP-0101-0700 | `evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json`<br>`build/finalize_classical_source_reconciliation.py#source_reconciliation_preflight`<br>A fresh independent preflight validates all 722 units and exact correction, formal, structural, semantic-review, and static-validation closure. |

## Owner follow-up decisions open to expert correction

These questions are review aids, not release blockers.

| Finding | Unit | Provisional choice | Why | Expert question |
|---|---|---|---|---|
| `C184-01` | OLP-0184 | محمول ذو n مواضع؛ علاقة ذات n مواضع | The descriptive construction says explicitly that the predicate or relation has n argument places. It avoids confusing arity with logical order (رتبة) or locality (محلية), while remaining reversible if an Arabic logic authority supplies a better canonical term. | ما المصطلح العربي المعجمي المعتمد لـ arity و n-place في نظرية النماذج، وكيف يطابق الاسم في التذكير والتأنيث؟ |
| `C185-01` | OLP-0185 | دالة ذات n مواضع؛ محمول ذو n مواضع | The descriptive construction preserves the arity condition in the definition of substructure and avoids overloading رتبة or محلية. | هل «ذو/ذات n مواضع» هو الأسلوب الأنسب في تعريف البنية الجزئية، أم يعتمد المعجم العربي مصطلحًا موجزًا لـ n-place؟ |
| `0452-I2` | OLP-0452 | يصدّق A إذا وفقط إذا صدّقها النموذج الأصلي، ويكذّبها إذا وفقط إذا كذّبها | Two separate biconditionals state the filtration invariant exactly and prevent a crossed reading between truth and falsity. | هل يبين التكافؤان المنفصلان بوضوح أن الترشيح يحفظ صدق A وكذبها كلًا في اتجاهه؟ |
| `0452-I3` | OLP-0452 | كل صيغة تصدق في نموذج تصدق أيضًا في نموذج منتهٍ؛ وإن كانت تكذب في نموذج تكذب أيضًا في نموذج منتهٍ | Splitting the true and false cases makes the source's paired parenthetical explicit and preserves the same truth value. The Classical layer already stated the two cases unambiguously. | هل تفصل الصياغة العربية حالتي الصدق والكذب بوضوح وتحفظ القيمة نفسها، من غير أن توهم إمكان تبدلها؟ |

## Deterministic identities

- Fresh preflight fingerprint: `7b39a2f1ec1d03e52e0af7f649d046d5f42e8f0e115d6a93b7df6c9fa0012759`
- Full source snapshot: `69ac33845eef27819f8a4f39b705c39dfd7ed0be2b56138f562d403512968d71`
- Frozen historical audit: `ea0733cfb04277d34fb999bbcaf6ea494ac015e904b040528a1b95963f828221`

| Input artifact | Bytes | SHA-256 |
|---|---:|---|
| `build/cardinality_repair_batch_20260908.py` | 23345 | `c5d435217cf43502186ab66f63225094c920d9231cd43952f8cd6c5be30a0b89` |
| `build/finalize_classical_source_reconciliation.py` | 86811 | `cc825aa509ebff8573ecfef3636c89fad219088715cb18369c102b18e3ce8959` |
| `build/generate_full_translation_acceptance_audit.py` | 29107 | `d13b6caa67f048e0fe31c1b64e410af969d13a10a98ad5fcc4cc1b2b2840ce98` |
| `build/validate_classical_overlay.py` | 84118 | `918f64e171585454b230c48280056ecda369b1bab4958a7efe486ba13f390690` |
| `evidence/classical/BASELINE.json` | 466996 | `c10a6321b79a210febba49b3fc216a7fb22b729a738af71d57dc1aea9e105beb` |
| `evidence/classical/BASELINE_CORRECTION_METADATA_SEED_20260906.json` | 159737 | `e5f0b85132ac052a446b7e7449e9d272cf5d941dbb908948e7a87c16e0b1057d` |
| `evidence/classical/FORMAL_REPAIR_DECLARATIONS_0001_0100_REBASED_20260905.json` | 20948 | `7b93452629123c6c5973eb5fcd1af56853c5c6ee8857e93b42c9012377cf339c` |
| `evidence/classical/SOURCE_PROPAGATION_PRE_QUALIFICATIONS_20260906.json` | 1105008 | `865eb48a37f5a50876dc5f406adf432a0360bf1e7c9a5fb5667caf41d27aa9ec` |
| `evidence/classical/SOURCE_RECONCILIATION_METADATA_20260905.json` | 74490 | `2464ac9546fb2dca1da69af9f1669fa563ad599f3ee364813668b0952d5873b2` |
| `evidence/classical/batches/0051-0100.corrections-OLP0067-20260906.json` | 1428 | `de2bf037dd0cf9348e502a45edb45a315bf68cc4a1d4a48919bbf318e1fd2148` |
| `evidence/classical/repairs/0001-0100.json` | 53170 | `6d29defdc78b870f6dc8a4c18b92a89e1437e09befb87782748116391f268326` |
| `evidence/classical/repairs/0001-0100.md` | 4312 | `6daf0c1157ea18e1072ef9f400034126f8448f7014c07dd0303d3012bb4b0c9a` |
| `evidence/classical/repairs/0101-0200.json` | 52537 | `b609a61216da695037f396bfab52200bb9f3a52f3d8dfe3b8bfd6e9796f7abe2` |
| `evidence/classical/repairs/0101-0200.md` | 9265 | `bd5dd32406c15335417208a3c0fdc7ff25e088da9a9c350576446bc9574a076c` |
| `evidence/classical/repairs/0201-0300.json` | 157418 | `ed6a4dad4b84d98f26236a357f443a6ebe09b851fce9266406b54645ba23a7ab` |
| `evidence/classical/repairs/0201-0300.md` | 17476 | `e44cd7f7360cddc65cb658bf620d0fb66732aaf8e9627d57e150ebd8881c75c1` |
| `evidence/classical/repairs/0301-0400.json` | 155251 | `4eaff0007717641c0d09848545c1277e06a47b619ea79fe27c0a69c2f6d25144` |
| `evidence/classical/repairs/0301-0400.md` | 15872 | `75bdc367772bfedc6481d51e9789e741dcb87ccef70c19029bc8e9b82e9c2526` |
| `evidence/classical/repairs/0401-0500.json` | 284309 | `520f152a60cb4e51a2c734bbe75944a3bf1e2b32de05320b2e340567512013aa` |
| `evidence/classical/repairs/0401-0500.md` | 7146 | `7a5e3b007d520a032b22a67163b3b247064fbf9eecb7ab513bd37b11684f18a0` |
| `evidence/classical/repairs/0501-0600.json` | 245258 | `52d9116196d5330049b4b12d4ce874a314e3495a7b5cabe9c872581fcdd8e068` |
| `evidence/classical/repairs/0501-0600.md` | 45634 | `a54f6c90f4534436f1a1d9872298b1c05ee48d8ce3d100e83180ea3e77d3f5e7` |
| `evidence/classical/repairs/0601-0700.json` | 262974 | `b0c9e7335b9074567926ed12c47f2c531a30338f520305092ceb46986e2f1a7c` |
| `evidence/classical/repairs/0601-0700.md` | 105432 | `2ad3d3854ae8be1bd0d8803db455a9ec47bd688151820bada11f77ba175fe7cb` |
| `evidence/classical/repairs/OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.json` | 27758 | `44587eeafb5a0564efd312b47d9d6c6be72a23fbad0a2449e76b66acea289827` |
| `evidence/classical/repairs/OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.md` | 7590 | `d1992b0fd0ec26d7447a1e24bd8acc538db0974cbdada972b53e7be9bd7cf56d` |
| `evidence/classical/repairs/OLP0008_CLASSICAL_PROSE_20260906.json` | 42407 | `99eda5ab0d7714c9fe274ce5a1fce4f058090cfff0474c8da749b80956f1f033` |
| `evidence/classical/repairs/OLP0008_CLASSICAL_PROSE_20260906.md` | 7129 | `6af4419381e3850c7bd8ed63042cc3ffcb96a1426cb7785b2ebbcde1c09a726f` |
| `evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json` | 137782 | `eb0e436d546c867a56d66767a24f66a2d687ea254ed83c9123aa0c2106a8e0c7` |
| `evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.md` | 8709 | `1688b82b31127a50c8e0d28307783340934cef62ef15673815d68cb1d8bbaa61` |
| `evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.json` | 5130 | `98b939cba500c9cbe8e591917709940ca0f685c61a0a4965535864e9aefd7120` |
| `evidence/classical/repairs/OLP0021_TWO_ROOTS_NOTE_20260907.md` | 1324 | `5669bebf86042ddca8eca2bde4824e1c2480cd34b8f7843219eb2ef7220cde1d` |
| `evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json` | 64402 | `90364663431ea9dad27fef1a427acf033498f1cd95f8cbea29cc665f41186c79` |
| `evidence/classical/repairs/OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.md` | 10610 | `3114d855ff63acbe40968e9f3e35c8055b2042b5d48828ede46ad32ebc500747` |
| `evidence/classical/repairs/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json` | 155011 | `86da173ac4083f2effe84cf60efe0e726e6caf79023aa8fa3ae6d852d73c8bc9` |
| `evidence/classical/repairs/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.md` | 17192 | `16c82b59d0e0474adffc80afcf5580e66e18918ff11dbcb083e4e6ea4e859ab7` |
| `evidence/classical/repairs/OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.json` | 42536 | `c7caca6897613149f74de25b08ebbe324699de79ec7531a7f4e6e5842d9683bd` |
| `evidence/classical/repairs/OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.md` | 9861 | `4dbda975e23cb69b574bad9a98206ff0a6b3d0fd767d5dc2a69a7b9ec8a5c05e` |
| `evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json` | 71615 | `13aa46d70ae164ca7b2be107503238027c2fadc3d0204a3bc0c68d9feb26aecc` |
| `evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.md` | 9516 | `f0569fd05c06adacd18c78237cb8e8f875e6dd8e5feab3fa145f7853a50d7918` |
| `evidence/classical/repairs/OLP0034_REDUCTION_CONSTRUCTIONS_20260907.json` | 19497 | `8addb4be1b7b8cc92f7044ab4ef357de6ea8105e134ac4ad921d9e5348580631` |
| `evidence/classical/repairs/OLP0034_REDUCTION_CONSTRUCTIONS_20260907.md` | 5194 | `0477e9a357f610a1ff5e4734b33a63a1082a268549f6a1697da77ad337a7827f` |
| `evidence/classical/repairs/OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.json` | 78958 | `4615dbc5636212dc0c9ca3c2244afef44f13a49d8a330ffd5dd6ce51415f68ed` |
| `evidence/classical/repairs/OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.md` | 12860 | `e30413fba4074349bd4a8e0d472cc4fbf42eeaedeaf065708c03b70e7326faa6` |
| `evidence/classical/repairs/OLP0051_0060_0068_SCOPE_PROPAGATION_20260906.json` | 71268 | `0c66dd4c3449c9aa8d92a0d904a813d9365942b0ef92d8327420a26b864d5c43` |
| `evidence/classical/repairs/OLP0051_0060_0068_SCOPE_PROPAGATION_20260906.md` | 12635 | `917bef2cb63753b5a001978c48d541221346ca06baacc2bbd177068cbffe73e1` |
| `evidence/classical/repairs/OLP0067_DUAL_GRAMMAR_20260906.json` | 80463 | `b6af652713edbecb4457d6725790cdc9de4f0ee4c446f3e3844d2760dde81ef1` |
| `evidence/classical/repairs/OLP0067_DUAL_GRAMMAR_20260906.md` | 19169 | `18e451a60bf43c1b5f39ab616c4e7fb998b5dfb3a7c920db27d1688bf8e700e7` |
| `evidence/classical/repairs/OLP0079_0093_MP_PROPAGATION_20260906.json` | 4312 | `7f463fe9b3848755accf7f7eb156893672bcd7b98bde5767b33e5b03a7a0368f` |
| `evidence/classical/repairs/OLP0079_0093_MP_PROPAGATION_20260906.md` | 1975 | `2e6a4b434760bbc1e34356fb309b61736513f1d03600e4e755d8f203ac1f9cc9` |
| `evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.json` | 57251 | `3cff7ba6901f09815be1ea4f42b2a29074639079fc21b09ae8cb4e6096e899da` |
| `evidence/classical/repairs/OLP0321_0326_0368_SEMANTIC_SCOPE_20260907.md` | 8883 | `c871f1c6fad2367f7ae1ac172d3aabbaff370ffb80171b073621a1aaafb98550` |
| `evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.json` | 33527 | `042822d86510960c3ae3fc9600ddf273f015bc00adc09e19c240a7071d265ff5` |
| `evidence/classical/repairs/OLP0375_0376_ARITHMETIC_SCOPE_20260907.md` | 4848 | `31c37879cc3959f675fcfc7018c9cbfb57e4e1eca9047df0ea4285eb5a0ffcbe` |
| `evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.json` | 98459 | `6d29d66c0db082e2c348cf8a30219e9d6ae11b80e14d0ecfdd2cbc2c79a6f4cd` |
| `evidence/classical/repairs/OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907.md` | 12850 | `af6578c5860299fa87972467dd2e890b64590b27457e804fee575896d181bb62` |
| `evidence/classical/repairs/OLP0497_MP_PROPAGATION_20260906.json` | 3744 | `31e05f4e4994e3bcb8abbad062f2e06cb6ada5ccb79f06eac8f7566bacfc61ca` |
| `evidence/classical/repairs/OLP0497_MP_PROPAGATION_20260906.md` | 2040 | `490a166f593fe3c9ec00107b814570153181038969c54d990a55adcd45d36e27` |
| `evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.json` | 11348 | `35006aeae8d7a83e7dd9cb3f9dbba4f5dc88cbcbb866d73c9cf42117347575a4` |
| `evidence/classical/repairs/OWNER_FOLLOWUP_REPAIRS_20260905.md` | 3148 | `94fde251a64c050174afff737fd6b871cf16cd24aad15702279b96c5ded49175` |
| `evidence/classical/repairs/history/pairing-before-applied-20260907/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json` | 154119 | `8ccc0f7f691271e37234d17812593df3748833efbd9578e4b01dfbbd217948af` |
| `evidence/classical/repairs/history/reduction-before-applied-20260907/classical-reduction.tex` | 7537 | `133d265118d6ffd9de895d0d908fd66c5f6a1b7fe1172b80a3c706dcf4a818b7` |
| `evidence/classical/repairs/history/reduction-before-applied-20260907/msa-reduction.tex` | 7671 | `0270446911d5ea3925e7c7505e88f658b903a52434430c4c3be36229c07c50e3` |
| `evidence/classical/reviews/0001-0050.json` | 89073 | `d404ce9f1f801b105397d5ad242c02047efb6881095b7a31220f9d223464190c` |
| `evidence/classical/reviews/0051-0100.json` | 212491 | `7311f9a9fc3f0b35dc58cde9a1013f8527ab3b3ae7e96fb1fafb0340542d8a69` |
| `evidence/classical/reviews/0101-0200.json` | 60127 | `93be2b852178b21ea252d5d7229219bda66e4ef5ea037b08c6baea5ec58ce795` |
| `evidence/classical/reviews/0201-0300.json` | 107523 | `9ec43fed5b2e10b86b35ba9a7640a8f5b1b3ab16e0e9fd4f57f882cd5e821ad4` |
| `evidence/classical/reviews/0301-0400.json` | 267745 | `03baeec71e1f67660c0883b2894e7408bfc6c0379ca09d8126bb5213a890cc3f` |
| `evidence/classical/reviews/0401-0500.json` | 293495 | `4e5ccd08318c232e612ad3d83eadf80a7c017e43b9322f3873c5495e609547cf` |
| `evidence/classical/reviews/0501-0600.json` | 295578 | `d490b5825ecb924c6ec63a254aa42f54644c8687c1b8150f3c866cc47bae3879` |
| `evidence/classical/reviews/0601-0700.json` | 96066 | `909c3e0877bc43d1b1c9a89aa7dc6ffdeda625a5fb434838301d00dfff8f5f0e` |
| `evidence/classical/reviews/0701-0722.json` | 80281 | `d89559f0656d3995a29ee5f42ed0d017680a88d3dcad501aa47f84f72bbe3979` |
| `evidence/classical/reviews/0701-0722.md` | 28991 | `5ddc6dc3b38339d3cdc2c8260bdade92bc54296fc363359dd1c26e8ce50b3ac0` |
| `evidence/classical/terminology/README.md` | 8277 | `71667fc1f7451c75f5a7de27142bc60ec6cb6f7b64fc3c521fd52aa05e9cbe11` |

## Blocking findings

None. All four expert-review questions remain explicitly non-blocking and open to correction.

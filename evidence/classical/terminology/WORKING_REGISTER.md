# Arabic translation decisions — working public register

Snapshot: 2026-09-04. Status: **partial and actively being backfilled**.

This register exposes the Arabic Open Logic terminology and difficult translation choices recorded so far so specialists can review them asynchronously. Translation continues when no official-dictionary entry or expert is available; reasoned choices stay provisional and explicitly open to correction. Expert feedback is welcome but is not a production or publication hold.

Retrospective entries record the present evidence-based reason for retaining or revising a choice. They do **not** claim to recover an earlier translator's private or contemporaneous thought process. A bounded unsuccessful lookup is never described as proof that a term is absent from all official dictionaries.

## Current coverage

- Frozen source inventory: 722 units.
- Decisions consolidated: 88.
- Contextually reviewed units with declared occurrence coverage: 4.
- Units with at least one recorded decision but incomplete contextual coverage: 30.
- Units still awaiting contextual decision review: 688.
- Classical target snapshots currently present: 472/722.
- Decisions explicitly queued for potentially useful expert input: 43.

These figures are deliberately not an exhaustive-completion claim. Machine-readable files preserve all source records, occurrence hashes and pending-unit states.

## How to review

Open EXPERT_REVIEW_QUEUE_WORKING.json for focused questions, DECISIONS_WORKING.json for the full current decision records, and COVERAGE_WORKING.json for every unit's reviewed/pending state. Corrections should cite a decision ID, mathematical sense, proposed wording and supporting source when available.

Public review surfaces: [GitHub terminology directory](https://github.com/KokunoYumeto/OpenLogic-ar/tree/main/evidence/classical/terminology), [GitHub issue form](https://github.com/KokunoYumeto/OpenLogic-ar/issues/new), and the stable [Zenodo concept DOI](https://doi.org/10.5281/zenodo.21921850). The DOI always resolves to the latest published snapshot in the existing Arabic-edition lineage.

## Recorded decisions

| Decision ID | English term / sense | Arabic in use | Basis | Confidence | Expert input |
| --- | --- | --- | --- | --- | --- |
| QA0051-0100-discharge-nominal | discharge of assumptions | إسقاط | inherited-unverified | high | not specifically requested |
| QA0051-0100-discharged-dual | both assumptions discharged | مسقطان | contextual-extension | high | not specifically requested |
| QA0051-0100-discharged-feminine | discharged assumptions or sentences | مسقطة | contextual-extension | high | not specifically requested |
| QA0051-0100-discharged-masculine | discharged assumption | مسقط | contextual-extension | high | not specifically requested |
| QA0051-0100-function-input | argument of a function | المدخل | ai-proposed | high | not specifically requested |
| QA0051-0100-modus-ponens | modus ponens | إثبات المقدَّم | contextual-extension | high | not specifically requested |
| QA0051-0100-undischarged-feminine | undischarged assumptions | غير المسقطة | contextual-extension | high | not specifically requested |
| QA0051-0100-undischarged-masculine | undischarged assumption | غير مسقط | contextual-extension | high | not specifically requested |
| ar-classical-0451-0500-accessibility-itaha | accessibility | إتاحة / علاقة الإتاحة | inherited-unverified | medium | useful |
| ar-classical-0451-0500-accessibility-nafadh | accessibility | نفاذ / علاقة النفاذ | inherited-unverified | medium | useful |
| ar-classical-0451-0500-branch | branch | فرع / شعبة | inherited-unverified | medium | useful |
| ar-classical-0451-0500-branching-nonbranching | branching/stacking rules | تشعيب / تفريع / مدّ الفرع من غير تشعيب | contextual-extension | high | not specifically requested |
| ar-classical-0451-0500-cardinality | cardinality/size | قوة / عدد / حجم | inherited-unverified | medium | useful |
| ar-classical-0451-0500-completeness | complete/completeness | تمام / تام | inherited-unverified | medium | useful |
| ar-classical-0451-0500-computability | computable procedure/enumeration | إجراء قابل للحساب / تعداد منتظم | contextual-extension | high | not specifically requested |
| ar-classical-0451-0500-contrapositive | contrapositive | عكس النقيض | ai-proposed | high | not specifically requested |
| ar-classical-0451-0500-countermodel | countermodel | نموذج مضاد | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-decidability | decidable/decidability | قابل للقرار / قابلية القرار | inherited-unverified | medium | useful |
| ar-classical-0451-0500-derivation-token | derivation/derivable | اشتقاق / قابل للاشتقاق؛ مع إبقاء رموز derivation وderivable | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-element-token | element | عنصر؛ مع إبقاء !!{element} | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-equivalence | equivalence relation | علاقة التكافؤ / يتكافأ | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-equivalence-class | equivalence class | فئة تكافؤ / فئة | inherited-unverified | medium | useful |
| ar-classical-0451-0500-euclidean | euclidean | إقليدي / إقليدية | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-filtration | filtration | ترشيح | inherited-unverified | medium | useful |
| ar-classical-0451-0500-finest-coarsest | finest/coarsest filtration | الأدق / الأخشن | inherited-unverified | medium | useful |
| ar-classical-0451-0500-finite-infinite | finite/infinite | منتهٍ / منتهية / لا نهائي | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-finite-model-property | finite model property | خاصية النموذج المنتهي | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-formula-token | formula | صيغة؛ مع إبقاء رموز !!{formula} وصيغها النحوية | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-fresh-used-prefix | new/used prefix | بادئة جديدة / مستعملة | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-hypothesis-assumption | assumption/hypothesis | فرض / افتراض | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-injection | injective | حقن؛ مع إبقاء الرمز !!a{injective} | inherited-unverified | medium | useful |
| ar-classical-0451-0500-interpretation | interpretation | تأويل | inherited-unverified | medium | useful |
| ar-classical-0451-0500-modal | modal | جهوي / موجهي | inherited-unverified | medium | useful |
| ar-classical-0451-0500-modal-closure | modally closed | مغلق جهويًا | inherited-unverified | medium | useful |
| ar-classical-0451-0500-model-world | model/world | نموذج / عالم | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-passage-OLP-0451 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0452 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0453 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0454 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0455 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | not specifically requested |
| ar-classical-0451-0500-passage-OLP-0456 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0457 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0458 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | not specifically requested |
| ar-classical-0451-0500-passage-OLP-0459 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0460 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0461 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0462 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0463 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | not specifically requested |
| ar-classical-0451-0500-passage-OLP-0464 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0465 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0466 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-passage-OLP-0467 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | not specifically requested |
| ar-classical-0451-0500-passage-OLP-0468 | passage-level exposition and semantic qualification | الصياغة العربية المثبتة في الموضع المحفوظ ببصمته | ai-proposed | medium | useful |
| ar-classical-0451-0500-prefix | prefix | بادئة | inherited-unverified | medium | useful |
| ar-classical-0451-0500-proof | proof | برهان / حجة | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-propositional-variable-token | propositional variable | متغير قضي؛ مع إبقاء !!{propositional variable} | inherited-unverified | medium | useful |
| ar-classical-0451-0500-reflexivity | reflexive | انعكاسي / انعكاسية | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-satisfiability | satisfiable/satisfaction | قابل للإرضاء / إرضاء / يرضي | inherited-unverified | medium | useful |
| ar-classical-0451-0500-semantic-entailment | entails/entailment | استلزام دلالي؛ مع بقاء Entails مستقلًا عن Proves | contextual-extension | high | not specifically requested |
| ar-classical-0451-0500-sentence-token | sentence | جملة؛ مع إبقاء !!a{sentence} | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-seriality | serial | متسلسل / تسلسلي | inherited-unverified | medium | useful |
| ar-classical-0451-0500-signed-formula-token | signed formula | صيغة موقعة؛ مع إبقاء !!{signed formula} | inherited-unverified | medium | useful |
| ar-classical-0451-0500-soundness | sound/soundness | سلامة / سليم | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-subformula-closure | closed under subformulas | مغلق تحت أخذ الصيغ الجزئية | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-symmetry | symmetric | متناظر / تناظر | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-tableau-token | tableau | جدول دلالي؛ مع إبقاء !!{tableau} وusetoken | inherited-unverified | medium | useful |
| ar-classical-0451-0500-transitivity | transitive | متعدٍ / تعدٍّ | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-truth-falsity | true/false | صادق / كاذب / صدق / كذب | inherited-unverified | high | not specifically requested |
| ar-classical-0451-0500-universal-model | universal model | نموذج كلي / نماذج كلية | inherited-unverified | medium | useful |
| ar-classical-0451-0500-validity | valid/validity | صالح / صالحة / الصلاحية | inherited-unverified | medium | useful |
| ar-classical-0451-0500-valuation | valuation | تقويم / إسناد | contextual-extension | medium | useful |
| retro-0001-0150:compilation | compiled | التجميع | inherited-unverified | medium | useful |
| retro-0001-0150:coverage-modality | may not yet be complete | لم يستوف الكتاب بعد بعض الموضوعات التي شرع فيها | contextual-extension | low | useful |
| retro-0001-0150:derived-textbook | derived textbooks | الكتب المشتقة من المشروع | contextual-extension | medium | not specifically requested |
| retro-0001-0150:driver-file | driver file | ملف التشغيل النموذجي | inherited-unverified | medium | useful |
| retro-0001-0150:formal-metalogic | formal meta-logic | المنطق الفوقي الصوري | inherited-unverified | medium | useful |
| retro-0001-0150:formal-methods | formal methods | المناهج الصورية | inherited-unverified | medium | not specifically requested |
| retro-0001-0150:glossary | a glossary | مسرد للمصطلحات | inherited-unverified | medium | not specifically requested |
| retro-0001-0150:infinity-prerequisite | which are not required for the logical parts of the OLP | ليس هذان البحثان شرطًا لدراسة الأجزاء المنطقية | contextual-extension | high | not specifically requested |
| retro-0001-0150:license-title | Creative Commons Attribution license | رخصة المشاع الإبداعي لنَسْب المُصنَّف | inherited-unverified | medium | not specifically requested |
| retro-0001-0150:naive-set-theory | Na\"ive Set Theory | نظرية المجموعات الساذجة | inherited-unverified | medium | useful |
| retro-0001-0150:number-systems | construction of number systems | بناء أنظمة الأعداد | inherited-unverified | medium | useful |
| retro-0001-0150:open-source-collaboration | open-source, collaborative textbook | اشترك في تأليفه جماعة وأتاحوا مصدره للناس | contextual-extension | medium | not specifically requested |
| retro-0001-0150:operator-primitives | logical operators primitives | جميع المؤثرات المنطقية أولية | inherited-unverified | medium | useful |
| retro-0001-0150:proof-cases | all cases for all operators in proofs | حالات كل مؤثر | inherited-unverified | medium | not specifically requested |
| retro-0001-0150:reading-vs-reuse | freely available | مباح الاطلاع | contextual-extension | medium | not specifically requested |
| retro-0001-0150:sets-heading | Sets | المجموعات | inherited-unverified | medium | not specifically requested |
| retro-0001-0150:textbook-rigour | it is rigorous | لا يخل بصرامته | inherited-unverified | medium | not specifically requested |

## Limits

- This is a working evidence publication, not expert endorsement, a completed lexicon, or full linguistic QA.
- Source-audit findings and inherited defects remain distinct from translation choices.
- The international and Machrek MSA readers share terminology; the classical edition can use different grammatical realization while preserving mathematical distinctions.
- Later snapshots preserve superseded decisions and identify replacements rather than rewriting history.

# OLP-0067 — three dual constructions in each Arabic register

Implemented in the source, 6 September 2026. Six local choices are listed below.
These are new assessments, not a reconstruction of an earlier translator’s intentions.
No official dictionary attestation is claimed. Every choice is provisional and open to correction.
The International and Machrek profiles share the MSA source; they are not separate wording registers.

## أين تراجع الاختيار؟ / Where to check

| Register | Exact source line | Chosen wording | Why |
|---|---|---|---|
| msa | [OLP-0067:26](../../../source/locale/ar/content/first-order-logic/proof-systems/tableaux.tex#L26) | الصيغتان الموقّعتان المضافتان | المقصود صيغتان اثنتان، وهما اسم تكون المرفوع؛ لذلك استعملنا المثنى ووافقناه بالوصفين. |
| msa | [OLP-0067:33](../../../source/locale/ar/content/first-order-logic/proof-systems/tableaux.tex#L33) | الصيغتين الموقّعتين | كلتا مضافة إلى المثنى في هذا السياق؛ فاستعملنا «الصيغتين الموقّعتين» مع إبقاء الصيغتين المعروضتين وقيد الفرع كما هما. |
| msa | [OLP-0067:38](../../../source/locale/ar/content/first-order-logic/proof-systems/tableaux.tex#L38) | صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً | يتطابق الطرفان في الصيغة نفسها ويختلفان في علامة الصدق، ولا يتطابقان بوصفهما صيغتين موقّعتين. صرّحنا بهذا الفرق مع تثنية الاسم والأوصاف بعد على. |
| classical | [OLP-0067:26](../../../source/locale/ar-classical/content/first-order-logic/proof-systems/tableaux.tex#L26) | الصيغتان الموقّعتان المضافتان | المقصود صيغتان اثنتان، وهما اسم تكون المرفوع؛ لذلك استعملنا المثنى ووافقناه بالوصفين. |
| classical | [OLP-0067:31](../../../source/locale/ar-classical/content/first-order-logic/proof-systems/tableaux.tex#L31) | الصيغتين الموقّعتين | كلتا مضافة إلى المثنى في هذا السياق؛ فاستعملنا «الصيغتين الموقّعتين» مع إبقاء الصيغتين المعروضتين وقيد الفرع كما هما. |
| classical | [OLP-0067:36](../../../source/locale/ar-classical/content/first-order-logic/proof-systems/tableaux.tex#L36) | صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً | يتطابق الطرفان في الصيغة نفسها ويختلفان في علامة الصدق، ولا يتطابقان بوصفهما صيغتين موقّعتين. صرّحنا بهذا الفرق مع تثنية الاسم والأوصاف بعد على. |

## ar-msa-OLP0067-signed-formula-added-nominative-20260906

**يرجى التحقق / Please double-check:** هل «الصيغتان الموقّعتان المضافتان» بيّن في وصف رأسي الفرعين، وهل لفظ «موقّعة» هو الأنسب للصيغة المقترنة بعلامة صدق هنا؟

English sense: Exactly two added signed formulas constitute the respective ends of the two new branches.

Chosen Arabic: الصيغتان الموقّعتان المضافتان

Literal English source (the readable term heading above is descriptive, not a verbatim TeX quote):

```tex
the two added !!{signed
  formula}s
```

Grammar: Definite feminine dual nominative noun with agreeing definite feminine dual nominative modifiers; it is the noun of تكون, whose predicate is نهايتيهما / رأسي الفرعين الجديدين.

Reason: The plural token expands to صيغ موقّعة, whereas المضافتان and the two-branch context require a dual. الصيغتان is nominative as the noun of تكون; الموقّعتان and المضافتان agree in number, case and definiteness. Only this complete local realization replaces the macro. The inherited technical stem موقّعة and the unchanged two branch endpoints are retained.

Before (`source/locale/ar/content/first-order-logic/proof-systems/tableaux.tex:26`):

```tex
تكون ال!!{signed formula}s
المضافتان
```

After:

```tex
تكون الصيغتان الموقّعتان
المضافتان
```

Alternatives:

- ال!!{signed formula}s المضافتان — rejected: Expands to a plural noun with a dual modifier; no dual slot exists in the inspected tokenizer.
- الصيغتان ذواتا العلامتين المضافتان — not selected: Introduces a different technical realization and can suggest that the signs rather than the signed formulas were added; the narrower inherited-stem repair is clearer.

Full-file SHA-256: `792ff7f33135257f884cd2ac9c03d30a3915009219b14c943b93b0615a784c2b` → `354e4fc8eafe5347ce15ea77cbcf46796e79723350bad5a497d28c9bfefc09c7`.
Exact occurrence excerpts, inverse patches, English locators and authority checks are in the paired JSON.

## ar-msa-OLP0067-signed-formula-both-genitive-20260906

**يرجى التحقق / Please double-check:** هل إضافة «كلتا» إلى «الصيغتين الموقّعتين» أوضح تعبيرًا عن وجوب إضافة الصيغتين معًا في قاعدة الاقتران ذات العلامة الصادقة؟

English sense: The True conjunction rule adds both specified signed formulas to the end of any branch containing the conjunction.

Chosen Arabic: الصيغتين الموقّعتين

Literal English source (the readable term heading above is descriptive, not a verbatim TeX quote):

```tex
both the two !!{signed formula}s
```

Grammar: Definite feminine dual genitive complement of كلتا, with an agreeing dual genitive adjective.

Reason: كلتا refers to both members of the stated pair and is followed here by its genitive complement. The plural token did not express that dual complement. الصيغتين الموقّعتين supplies the required dual while preserving كلتا, the two displayed True-signed formulas, and the any-containing-branch qualification. This changes grammatical realization, not the tableau rule.

Before (`source/locale/ar/content/first-order-logic/proof-systems/tableaux.tex:33`):

```tex
كلتا ال!!{signed formula}s،
```

After:

```tex
كلتا الصيغتين الموقّعتين،
```

Alternatives:

- كلتا ال!!{signed formula}s — rejected: The actual plural expansion is not the dual complement selected for exactly these two formulas.
- الصيغتين الموقّعتين معًا — not selected: Could express the same rule, but replacing كلتا is unnecessary; the narrow inflection repair retains the original emphasis on both.

Full-file SHA-256: `792ff7f33135257f884cd2ac9c03d30a3915009219b14c943b93b0615a784c2b` → `354e4fc8eafe5347ce15ea77cbcf46796e79723350bad5a497d28c9bfefc09c7`.
Exact occurrence excerpts, inverse patches, English locators and authority checks are in the paired JSON.

## ar-msa-OLP0067-signed-formula-closure-genitive-20260906

**يرجى التحقق / Please double-check:** هل «صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً» يوضح أن الصيغة واحدة وعلامتي الصدق متقابلتان، مع سلامة التثنية بعد «على»؟ هل صياغة «لهما الصيغة نفسها» أيسر للقارئ؟

English sense: A branch closes on two signed objects with exactly the same underlying syntactic formula and opposite truth-value signs; every branch must close for tableau closure.

Chosen Arabic: صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً

Literal English source (the readable term heading above is descriptive, not a verbatim TeX quote):

```tex
matching pair of !!{signed formula}s
```

Grammar: Indefinite feminine dual genitive after على, with agreeing dual modifiers; صيغةً and علامةً distinguish the aspects of identity and difference.

Reason: The MSA matching-pair phrase could obscure which part matches; Classical already distinguished the same formula from different signs, but attached dual modifiers to a plural macro. The explicit dual makes both editions agree grammatically and preserves that exact distinction. The complete signed objects are not identical: one is True A and the other False A. Every-branch quantification is unchanged. Neither True p with True p nor True p with False q meets this syntactic closure criterion.

Before (`source/locale/ar/content/first-order-logic/proof-systems/tableaux.tex:38`):

```tex
!!^a{tableau} مغلقًا إذا احتوى كل فرع من فروعه على زوج متطابق من
ال!!{signed formula}s،
```

After:

```tex
!!^a{tableau} مغلقًا إذا احتوى كل فرع من فروعه على
صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً،
```

Alternatives:

- ال!!{signed formula}s المتطابقتين صيغةً المختلفتين علامةً — rejected: The inherited Classical phrase expands to a plural noun followed by dual modifiers.
- صيغتين موقّعتين لهما الصيغة نفسها وعلامتان مختلفتان — acceptable-not-selected: Semantically equivalent, more explicit but longer; the chosen aspect construction preserves the prior Classical clarification.
- صيغتين متناقضتين — rejected: May suggest arbitrary contradictory formulas instead of an identical syntactic formula carrying opposite signs.

Full-file SHA-256: `792ff7f33135257f884cd2ac9c03d30a3915009219b14c943b93b0615a784c2b` → `354e4fc8eafe5347ce15ea77cbcf46796e79723350bad5a497d28c9bfefc09c7`.
Exact occurrence excerpts, inverse patches, English locators and authority checks are in the paired JSON.

## ar-classical-OLP0067-signed-formula-added-nominative-20260906

**يرجى التحقق / Please double-check:** هل «الصيغتان الموقّعتان المضافتان» بيّن في وصف رأسي الفرعين، وهل لفظ «موقّعة» هو الأنسب للصيغة المقترنة بعلامة صدق هنا؟

English sense: Exactly two added signed formulas constitute the respective ends of the two new branches.

Chosen Arabic: الصيغتان الموقّعتان المضافتان

Literal English source (the readable term heading above is descriptive, not a verbatim TeX quote):

```tex
the two added !!{signed
  formula}s
```

Grammar: Definite feminine dual nominative noun with agreeing definite feminine dual nominative modifiers; it is the noun of تكون, whose predicate is نهايتيهما / رأسي الفرعين الجديدين.

Reason: The plural token expands to صيغ موقّعة, whereas المضافتان and the two-branch context require a dual. الصيغتان is nominative as the noun of تكون; الموقّعتان and المضافتان agree in number, case and definiteness. Only this complete local realization replaces the macro. The inherited technical stem موقّعة and the unchanged two branch endpoints are retained.

Before (`source/locale/ar-classical/content/first-order-logic/proof-systems/tableaux.tex:26`):

```tex
تكون ال!!{signed formula}s المضافتان
```

After:

```tex
تكون الصيغتان الموقّعتان المضافتان
```

Alternatives:

- ال!!{signed formula}s المضافتان — rejected: Expands to a plural noun with a dual modifier; no dual slot exists in the inspected tokenizer.
- الصيغتان ذواتا العلامتين المضافتان — not selected: Introduces a different technical realization and can suggest that the signs rather than the signed formulas were added; the narrower inherited-stem repair is clearer.

Full-file SHA-256: `f5041be3f28e1a821382fcdeabbf8ea477288baca1b38ee321ac55bed8d9471c` → `772c2799ded3dff28788e317d7ea14747eabdf01da8a4d1343ee3cffc7f170b8`.
Exact occurrence excerpts, inverse patches, English locators and authority checks are in the paired JSON.

## ar-classical-OLP0067-signed-formula-both-genitive-20260906

**يرجى التحقق / Please double-check:** هل إضافة «كلتا» إلى «الصيغتين الموقّعتين» أوضح تعبيرًا عن وجوب إضافة الصيغتين معًا في قاعدة الاقتران ذات العلامة الصادقة؟

English sense: The True conjunction rule adds both specified signed formulas to the end of any branch containing the conjunction.

Chosen Arabic: الصيغتين الموقّعتين

Literal English source (the readable term heading above is descriptive, not a verbatim TeX quote):

```tex
both the two !!{signed formula}s
```

Grammar: Definite feminine dual genitive complement of كلتا, with an agreeing dual genitive adjective.

Reason: كلتا refers to both members of the stated pair and is followed here by its genitive complement. The plural token did not express that dual complement. الصيغتين الموقّعتين supplies the required dual while preserving كلتا, the two displayed True-signed formulas, and the any-containing-branch qualification. This changes grammatical realization, not the tableau rule.

Before (`source/locale/ar-classical/content/first-order-logic/proof-systems/tableaux.tex:31`):

```tex
كلتا ال!!{signed formula}s

```

After:

```tex
كلتا الصيغتين الموقّعتين

```

Alternatives:

- كلتا ال!!{signed formula}s — rejected: The actual plural expansion is not the dual complement selected for exactly these two formulas.
- الصيغتين الموقّعتين معًا — not selected: Could express the same rule, but replacing كلتا is unnecessary; the narrow inflection repair retains the original emphasis on both.

Full-file SHA-256: `f5041be3f28e1a821382fcdeabbf8ea477288baca1b38ee321ac55bed8d9471c` → `772c2799ded3dff28788e317d7ea14747eabdf01da8a4d1343ee3cffc7f170b8`.
Exact occurrence excerpts, inverse patches, English locators and authority checks are in the paired JSON.

## ar-classical-OLP0067-signed-formula-closure-genitive-20260906

**يرجى التحقق / Please double-check:** هل «صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً» يوضح أن الصيغة واحدة وعلامتي الصدق متقابلتان، مع سلامة التثنية بعد «على»؟ هل صياغة «لهما الصيغة نفسها» أيسر للقارئ؟

English sense: A branch closes on two signed objects with exactly the same underlying syntactic formula and opposite truth-value signs; every branch must close for tableau closure.

Chosen Arabic: صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً

Literal English source (the readable term heading above is descriptive, not a verbatim TeX quote):

```tex
matching pair of !!{signed formula}s
```

Grammar: Indefinite feminine dual genitive after على, with agreeing dual modifiers; صيغةً and علامةً distinguish the aspects of identity and difference.

Reason: The MSA matching-pair phrase could obscure which part matches; Classical already distinguished the same formula from different signs, but attached dual modifiers to a plural macro. The explicit dual makes both editions agree grammatically and preserves that exact distinction. The complete signed objects are not identical: one is True A and the other False A. Every-branch quantification is unchanged. Neither True p with True p nor True p with False q meets this syntactic closure criterion.

Before (`source/locale/ar-classical/content/first-order-logic/proof-systems/tableaux.tex:36`):

```tex
ويكون !!^a{tableau} مغلقًا متى اشتمل كل فرع على ال!!{signed formula}s المتطابقتين صيغةً المختلفتين علامةً:
```

After:

```tex
ويكون !!^a{tableau} مغلقًا متى اشتمل كل فرع على صيغتين موقّعتين متطابقتين صيغةً مختلفتين علامةً:
```

Alternatives:

- ال!!{signed formula}s المتطابقتين صيغةً المختلفتين علامةً — rejected: The inherited Classical phrase expands to a plural noun followed by dual modifiers.
- صيغتين موقّعتين لهما الصيغة نفسها وعلامتان مختلفتان — acceptable-not-selected: Semantically equivalent, more explicit but longer; the chosen aspect construction preserves the prior Classical clarification.
- صيغتين متناقضتين — rejected: May suggest arbitrary contradictory formulas instead of an identical syntactic formula carrying opposite signs.

Full-file SHA-256: `f5041be3f28e1a821382fcdeabbf8ea477288baca1b38ee321ac55bed8d9471c` → `772c2799ded3dff28788e317d7ea14747eabdf01da8a4d1343ee3cffc7f170b8`.
Exact occurrence excerpts, inverse patches, English locators and authority checks are in the paired JSON.

## Evidence and limits

- The inspected configuration defines the plural as صيغ موقّعة; the tokenizer dispatches the trailing s to that plural slot. This is software-source evidence, not dictionary attestation.
- All 21 formula segments and 101 named LaTeX control words per edition are byte/order-identical. Including 12 one-character controls/delimiters, the full ordered command inventory is 113, also unchanged. Exactly three plural token occurrences per edition become recorded explicit dual realizations; seven remain.
- Existing True/And and False/And rule-label corrections remain unchanged, as does the every-branch closure condition.
- The actual static checker passes both declared before/after comparisons and the MSA/Classical after comparison without a cross-edition exception. Static checks alone do not establish complete semantic or visual quality.
- The historical 0051–0100 batch and original closure proposal remain unchanged. The new exact one-unit companion supersedes only OLP-0067 identities; it does not certify all other batch units as current.
- Source finding aliases 0067-G1, 0067-G2 and 0067-G3 map respectively to added-nominative, both-genitive and closure-genitive in both registers. The JSON explicitly maps each alias to its two separate decision IDs.
- The original batch uses classical-batch-v1. The owner added narrowly pinned legacy support to the general batch auditor: it requires the original raw hash and parsed-data equality before all ordinary checks. This producer now passes those original bytes directly, with no schema-label adaptation or receipt rewrite. Other batch units are not silently marked current.
- No TeX was run. Presentation regeneration, central index binding, final-reader checks and actual PDF page evidence remain owner integration work. No page number has been guessed.

Companion: [0051–0100 / OLP-0067 only](../batches/0051-0100.corrections-OLP0067-20260906.json).
Lossless choices and exact locators: [JSON](OLP0067_DUAL_GRAMMAR_20260906.json).

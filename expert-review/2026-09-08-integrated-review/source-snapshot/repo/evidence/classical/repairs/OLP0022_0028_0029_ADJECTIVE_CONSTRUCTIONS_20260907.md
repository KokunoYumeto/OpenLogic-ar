# Four Classical Arabic construction repairs

This batch repairs four grammatical constructions in three Classical Arabic units. The English sources, MSA text, shared terminology, formulas and existing disclosed corrections are unchanged. These are contemporaneous, provisional decisions, open to correction—not claims of historical attestation or completed expert review.

Status: implemented; all nine focused tests passed in one run (0.085 seconds, exit code 0). No reader build, export or publication was performed.

## Where to review

Source lines below refer to this batch's exact after bytes, not PDF page numbers. The complete [machine-readable record](OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907.json) preserves before/after hashes, reversible literal patches, English/MSA anchors, reasons and unchanged passages.

## 1. OLP-0022: surjective functions

[Current passage, line 15](../../../source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L15) — `AR-OLP-0022-CLASSICAL-SURJECTIVE-OPENING-20260907`.
This is a newly recorded adjacent opening repair, separate from the prior six-function batch.

Before:

```latex
هذا الصنف
يسمى !!{surjective}، وصورته
```

After:

```latex
وتسمى هذه الدوال !!{surjective}، وصورتها
```

Meaning: Each function takes every codomain member as a value; the adjective describes the functions, not a category object.

Why: The old masculine subject هذا الصنف is followed by the shared feminine adjective شاملة. Replace it with the English referent هذه الدوال, a non-human plural with feminine-singular agreement. Also change وصورته to وصورتها so that the figure-reference pronoun agrees with the new subject. Keep the local surjective token and the codomain explanation unchanged.

English anchor (source lines 17–18, UTF-8 bytes [497, 538)):

```latex
Such
functions are called !!{surjective}
```

The MSA construction already reads `هذه الدوال !!{surjective}` (lines 18–18); neither MSA notation profile needs this repair.

Optional expert question: هل «وتسمى هذه الدوال شاملة، وصورتها في الشكل» أنسب، أم تفضلون الإفراد «وتسمى مثل هذه الدالة شاملة» مع إبقاء معنى شمول المجال المقابل؟

This remains open to correction; an answer is not a prerequisite for implementation or release.

Classical input: 4145 bytes, SHA-256 `8a73d76a7d09e54a6956468280c054ded5243f4f4a43ed05aee76de126dd9ca9`. Current batch output: 4151 bytes, SHA-256 `3a74dd4fc979afc520df1954cc09c78327ac63c6954852f77e0a8cb9b9a38922`. Literal source bytes [413, 469) become [413, 475).

## 2. OLP-0028: enumerable sets

[Current passage, line 22](../../../source/locale/ar-classical/content/sets-functions-relations/size-of-sets/introduction.tex#L22) — `AR-OLP-0028-CLASSICAL-ENUMERABLE-OPENING-20260907`.
Prior review choice: `AR-OLP0028-ar-classical-G11`.

Before:

```latex
وهذا الصنف
يسمى !!{enumerable}.
```

After:

```latex
وتسمى هذه المجموعات !!{enumerable}.
```

Meaning: The sets just described have enumerations; no effectiveness or computability restriction is added.

Why: The old expansion وهذا الصنف يسمى قابلة للتعداد attaches a feminine adjectival expression to masculine الصنف and risks treating the category rather than its sets as enumerable. Naming these sets supplies the English referent and a non-human plural compatible with the unchanged feminine-singular token. The finite/infinite-list explanation and Cantor conclusion are preserved.

English anchor (source lines 24–24, UTF-8 bytes [929, 965)):

```latex
Such sets are called !!{enumerable}.
```

The MSA construction already reads `وتسمى مثل هذه المجموعات !!{enumerable}.` (lines 24–24); neither MSA notation profile needs this repair.

Optional expert question: هل عبارة «وتسمى هذه المجموعات قابلة للتعداد» أوفق لأسلوب هذا الفصل، أم تفضلون «ويقال لهذه المجموعات إنها قابلة للتعداد»؟

This remains open to correction; an answer is not a prerequisite for implementation or release.

Classical input: 1347 bytes, SHA-256 `063721dc118acf308f1a3ec1b053ea5ee64b3ad6811f806a8e9e97e65266f498`. Current batch output: 1355 bytes, SHA-256 `e29d0e0ceec6b0306f9746f074a9159e7cac0a6d895faa2c8875a4b98b1c2d4a`. Literal source bytes [1104, 1148) become [1104, 1156).

## 3. OLP-0029: surjective functions f and g

[Current passage, line 150](../../../source/locale/ar-classical/content/sets-functions-relations/size-of-sets/enumerability.tex#L150) — `AR-OLP-0029-CLASSICAL-DUAL-SURJECTIVE-20260907`.
Prior review choice: `AR-OLP0029-ar-classical-G26`.

Before:

```latex
فافرض دالتين !!{surjective} هما
```

After:

```latex
فافرض دالتين، كل منهما !!{surjective}، هما
```

Meaning: Each of the two maps is onto its own codomain; the union exercise separately retains empty-component cases.

Why: دالتين شاملة places the singular shared adjective directly after a dual noun. The distributive clause كل منهما شاملة gives each function the property and preserves the dual هما introducing f and g. It neither changes the shared token into a dual form nor attributes surjectivity only to a combination of the maps. All domains, h, and the separate empty-set cases remain unchanged.

English anchor (source lines 166–167, UTF-8 bytes [6952, 7049)):

```latex
suppose there are !!{surjective} functions $f\colon \PosInt \to
  A$ and $g\colon \PosInt \to B$
```

The MSA construction already reads `افترض وجود دالتين، كل منهما !!{surjective}،` (lines 168–168); neither MSA notation profile needs this repair.

Optional expert question: هل التوزيع بعبارة «كل منهما شاملة» أوضح من تثنية الصفة هنا، مع بقاء الدالتين والحالتين الخاليتين على ما هما عليه؟

This remains open to correction; an answer is not a prerequisite for implementation or release.

Classical input: 12725 bytes, SHA-256 `3a73f26ac07a2a4299605ac1b9bbe62f06ce96863eb03d06e018fc71aed460e9`. Current batch output: 12754 bytes, SHA-256 `63d74fe9be63b8b0970562a13756c324944d37885d6421bc8e2af975450225a8`. Literal source bytes [7326, 7371) become [7326, 7391).

## 4. OLP-0029: zeroth, first, second elements of a list

[Current passage, line 171](../../../source/locale/ar-classical/content/sets-functions-relations/size-of-sets/enumerability.tex#L171) — `AR-OLP-0029-CLASSICAL-ZERO-INDEXED-ELEMENTS-20260907`.
Prior review choice: `AR-OLP0029-ar-classical-G29`.

Before:

```latex
فيسمون !!{element}s القائمة ذا الرتبة
```

After:

```latex
فيتحدثون عن !!{element}s القائمة ذات الرتب
```

Meaning: Refer to list elements at positions 0, 1, 2 and so on, retaining the equivalent zero-based enumeration definition.

Why: The old expansion فيسمون عناصر القائمة ذا الرتبة combines plural عناصر with singular masculine ذا and changes speaking of positions into naming. فيتحدثون عن restores the English relation, and ذات الرتب provides feminine-singular agreement with a non-human plural and plural ranks for the following sequence. Keep exactly the following 0, 1, 2, Nat domain, and shift proof. The possible attachment of ذات to القائمة remains an explicitly reviewable readability preference.

English anchor (source lines 189–189, UTF-8 bytes [8001, 8071)):

```latex
talk about the $0$th, $1$st, $2$nd, and so on, !!{element}s of a list.
```

The MSA construction already reads `فهم يتحدثون عن !!{element}s القائمة ذات الرتب $0$ و$1$ و$2$، وهكذا.` (lines 191–192); neither MSA notation profile needs this repair.

Optional expert question: هل «عناصر القائمة ذات الرتب» واضحة في السياق، أم تفضلون «عناصر القائمة التي رتبها» حتى لا تُحمل «ذات» على القائمة بدل العناصر؟

This remains open to correction; an answer is not a prerequisite for implementation or release.

Classical input: 12725 bytes, SHA-256 `3a73f26ac07a2a4299605ac1b9bbe62f06ce96863eb03d06e018fc71aed460e9`. Current batch output: 12754 bytes, SHA-256 `63d74fe9be63b8b0970562a13756c324944d37885d6421bc8e2af975450225a8`. Literal source bytes [8455, 8513) become [8475, 8542).

## Preserved mathematics and historical chain

The OLP-0022 input hash is the output of the earlier six-function repair transaction: `8a73d76a7d09e54a6956468280c054ded5243f4f4a43ed05aee76de126dd9ca9`. This batch changes only the opening and the referring pronoun. All five earlier changed literals in this file remain exact; their lines shift by minus one. The JSON embeds the predecessor transaction and records the predecessor ledger identity at capture. Central historical bindings still require owner integration; the earlier ledger is not rewritten to pretend its whole-file output is still current.

The OLP-0029 `-3` entry and OLSIZ-001 disclosure remain. The two enumeration maps, union map, separate empty-set cases, zero-inclusive natural numbers, indices 0/1/2 and index-shift equations remain. The corollary's finite endpoint `{0, …, n}` and the proof's `{0, …, n−1}` use differently quantified endpoint parameters and are not corrections to make.

The shared values remain `surjective` = شاملة, `enumerable` = قابلة للتعداد, and plural `element` = عناصر. These changes repair how the tokens are used in a sentence, not the dictionary entries.

## Verification and remaining work

Focused command: `python -X utf8 -B -m unittest build.tests.test_classical_adjective_constructions_0022_0028_0029 -v`. Result: all nine tests passed in the single run, 0.085 seconds, exit code 0. The checks cover ten exact complete input/output identities, four reversible replacements, twenty source/token witnesses, exact formal/math preservation in all three files without exceptions, thirteen preserved passages, the five-patch predecessor chain and these four current-source links. They do not establish full-corpus semantic acceptance, PDF layout or publication.

Next: owner integrates the source history and rebinds affected review locations together with the other substantive repairs. No central index or metadata was modified by this subtask.

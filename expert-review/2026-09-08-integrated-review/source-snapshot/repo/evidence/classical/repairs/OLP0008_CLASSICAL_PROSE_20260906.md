# OLP-0008: applied Classical prose clarifications

Four review decisions, five exact passage replacements, one Classical wording unit. All remain open to correction; expert response is not a gate.

Shared MSA is unchanged. This is not a claim that reader/presentation integration or publication is complete.

Before `8f7272540f2930ff7678b73f337d4669a38fac600f98a04b381d72a97f882c4f` (6884 bytes); current `44c0b9e062fb111b1547c8b7b5dc2afe6f4ac6c951e353aa6d8ba0f5473caac9` (6970 bytes).

All 72 mathematical containers retain exact bytes: four align* displays plus 68 dollar/bracket containers. No terminology token, environment, reference, nonempty-family condition or correction note changes.

## AR-OLP-0008-CLASSICAL-C005

[single-passage: current Classical source lines 43-43](../../../source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L43); English lines 47-47.

Before:
```tex
وإذا ضمت المجموعة إلى إحدى جزئياتها لم تزد عليها شيئًا، فالاتحاد
هو الكبرى: 
```

Now:
```tex
واتحاد المجموعة بإحدى مجموعاتها الجزئية هو المجموعة الأصلية نفسها: 
```

Why: Name the subset explicitly as مجموعاتها الجزئية and the result as المجموعة الأصلية نفسها. This removes an unclear pronoun in لم تزد عليها and does not misread the source's informal bigger as strictly greater cardinality. Union with any subset, including the equal-set case, returns the containing set.

Please double-check: هل يبيّن التعبير «المجموعة الأصلية نفسها» عودة الاتحاد إلى المجموعة المذكورة أولًا، بما يشمل حالة مساواة المجموعة الجزئية لها، من غير إيحاء بمقارنة العدد؟

## AR-OLP-0008-CLASSICAL-C009

[common-elements: current Classical source lines 79-80](../../../source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L79); English lines 85-86.

Before:
```tex
ومتى وجدت !!{element}s مشتركة، جمعها التقاطع كلها وحدها، نحو:
```

Now:
```tex
ومتى وجدت !!{element}s مشتركة بين مجموعتين، كان تقاطعهما المجموعة
التي تضمها جميعًا ولا تضم غيرها، نحو:
```

Why: Replace personified collection and stacked كلها وحدها with a direct nominal set definition. The antecedent of تضمها is the immediately stated common elements; جميعًا provides totality and ولا تضم غيرها provides exclusivity. The original element terminology token is retained exactly once.

Please double-check: هل مرجع الضمير في «تضمها جميعًا ولا تضم غيرها» واضح بما يكفي لبيان جميع العناصر المشتركة وحدها، أم تُفضّل إعادة الاسم صراحةً في مراجعة لاحقة مع تسجيل تحقيق رمز المصطلح؟

[subset-absorption: current Classical source lines 83-83](../../../source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L83); English lines 88-89.

Before:
```tex
وإذا كانت إحداهما جزئية من الأخرى فالتقاطع هو الصغرى:
```

Now:
```tex
وتقاطع المجموعة بإحدى مجموعاتها الجزئية هو تلك المجموعة الجزئية:
```

Why: Replace standalone جزئية with the precise noun phrase مجموعة جزئية and name the result by its inclusion role rather than the informal smaller-set metaphor. This retains equality cases and avoids an unintended strict-cardinality claim.

Please double-check: هل يوضح تكرار «المجموعة الجزئية» نتيجة التقاطع وعلاقة الاحتواء من غير الخلط بين المجموعة الجزئية والمجموعة الجزئية الفعلية؟

## AR-OLP-0008-CLASSICAL-C014

[single-passage: current Classical source lines 131-132](../../../source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L131); English lines 135-135.

Before:
```tex
	أثبت للمجموعة $A$ أنه متى كان $A \in B$ لزم
$A \subseteq \bigcup B$.
```

Now:
```tex
	أثبت أنه إذا كانت $A$ مجموعة وكان $A \in B$، فإن
$A \subseteq \bigcup B$.
```

Why: Use a direct proof imperative followed by both hypotheses and then the conclusion. The old dative للمجموعة makes the set appear the addressee or beneficiary of proof; the revised conditional makes its type assumption explicit. Membership and subset are not conflated and every math atom remains byte-identical.

Please double-check: هل يحفظ الأمر «أثبت أنه إذا كانت ... مجموعة وكان ...، فإن ...» فرضي المسألة كليهما بوضوح، ولا يوهم إضافة فرض غير وارد في الأصل؟

## AR-OLP-0008-CLASSICAL-C016

[single-passage: current Classical source lines 159-160](../../../source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L159); English lines 163-164.

Before:
```tex
\emph{فرق المجموعتين}~$A \setminus B$ ما اجتمع من !!{element}s
$A$ بعد استبعاد ما هو من !!{element}s~$B$، أي
```

Now:
```tex
\emph{فرق المجموعتين}~$A \setminus B$ هو مجموعة جميع !!{element}s
$A$ التي ليست من !!{element}s~$B$، أي
```

Why: Retain the attested name فرق المجموعتين but replace an apparent collection/removal procedure with a direct extensional definition. جميع makes all eligible elements explicit; التي ليست من preserves the conjunction of membership in A and nonmembership in B. Both element tokens and the defining display are untouched.

Please double-check: هل يعبّر «مجموعة جميع ... التي ليست من ...» عن فرق المجموعتين بدقة وسلاسة، مع إبقاء الفرق متميزًا من المتممة بالنسبة إلى مجموعة كلية مفترضة؟

## Authority and history

Directly inspected: Damascus subset (PDF 192 / printed 191), set difference (PDF 177 / printed 176), and KSU set operations (PDF/printed 14). The complete proposed sentences are contextual rewrites, not dictionary quotations. ENS extensionality and the Damascus proof entry were manager-reported only in this bounded subtask.

The prior wording and complete original proposal are preserved under history/olp0008-prose-20260906/. The dated witness companion preserves the original nonempty-family correction reason and question; only the complete Classical file identity changes for that unchanged selected passage. The disjointness witness moves one line earlier without a text or sense change.

No reader PDF page is inferred from source lines. Reconcile source closure, regenerate the notation presentation, and rebind the reviewer index before claiming those deliverables updated.

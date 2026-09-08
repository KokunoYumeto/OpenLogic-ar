# Four further Classical qualifications propagated to shared MSA

Status: implemented-in-shared-msa-source. New independent assessments, 6 September 2026.

Choices are provisional and open to correction. No official dictionary attestation or original-translator deliberation is claimed. International and Machrek share these MSA sources. Final PDF pages, rebuild and publication are not claimed.

Source/evidence validation: 24 tests passed. Exact inverse hashes, unchanged formulas/proofs, active literal phrase bindings and negative probes are checked; rendering and full-book semantic correctness are not claimed.

| Where to check | Chosen MSA wording | Why check this? |
|---|---|---|
| [OLP-0033, source line 25](../../../source/locale/ar/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L25) | فلكل مجموعة غير خالية | A surjection from positive integers exists for every nonempty enumerable set, not for the empty enumerable set. |
| [OLP-0039, source line 26](../../../source/locale/ar/content/sets-functions-relations/size-of-sets/non-enumerability-alt.tex#L26) | يقتضي | Nonenumerability implies absence of a Nat bijection and, more strongly, absence of a Nat surjection. Absence of a Nat bijection alone is not a definition of nonenumerability for arbitrary sets. |
| [OLP-0039, source line 27](../../../source/locale/ar/content/sets-functions-relations/size-of-sets/non-enumerability-alt.tex#L27) | بل لا توجد دالة | A stronger no-surjection consequence, not an equivalent paraphrase of no bijection |
| [OLP-0072, source line 81](../../../source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L81) | لا ترد أي قيود من جهة المتغير المميَّز على الحد | Existential-right and universal-left permit arbitrary closed terms without eigenvariable freshness restrictions; they do not permit open terms in this presentation. |
| [OLP-0081, source line 27](../../../source/locale/ar/content/first-order-logic/sequent-calculus/soundness.tex#L27) | فإذا تخلّفت واحدة على الأقل منها | Failure of at least one of the three required soundness properties is enough; it is not necessary for all three properties to fail. |

## OLP-0033: enumerable set / surjection

Literal English phrase: enumerable. Classical phrase: المجموعة غير الخالية.

Before: فلكل مجموعة. Chosen: فلكل مجموعة غير خالية.

English and MSA omit nonemptiness from the universal existence claim. Classical already adds it and a disclosed source-correction note. OLP-0029 explicitly includes the empty set among enumerable sets. No total function from the nonempty positive integers can have empty codomain. We propagate غير خالية and the existing Classical note, and repeat the nonempty qualification in the next paragraph's no-surjection criterion so that the same exception is not immediately lost. No diagonal proof or formula changes.

Mathematical reason: If f:PosInt→∅ were total, f(1) would have to be an element of ∅, impossible. Nonetheless ∅ has the empty enumeration and is enumerable under the book's definition.

Alternative considered: exclude the empty set from enumerable sets. Would contradict the explicit preceding definition. The local nonempty qualification preserves that definition and all results.

Expert question (open to correction): Does غير خالية plus the source-correction note make clear that the empty set remains enumerable, despite admitting no total map from positive integers? Does repeating the qualification in the following criterion prevent a false converse?

Exact changed source ranges: 25–25, 31–37.

## OLP-0039: nonenumerability / no bijection / no surjection

Literal English phrase: nonenumerable. Classical phrase: يقتضي.

Before: هو القول. Chosen: يقتضي.

The English equates nonenumerability with having no bijection from Nat, then equates that absence with having no surjection. MSA repeats these equivalences. Classical correctly uses implication and separates the stronger no-surjection assertion. A singleton is enumerable, has a constant surjection from Nat, but cannot have a Nat bijection. We replace هو القول with يقتضي and the explanatory أي with strengthening بل, retaining every existing formula, quantifier and later proof. This corrects an inherited source overstatement; it is not a claim that the English explicitly made the needed distinction.

Mathematical reason: A={0} has a finite enumeration and constant surjection f(n)=0 from Nat. Any function into {0} sends distinct 0 and 1 to the same value, so no such function is injective or bijective.

Alternative considered: restrict A explicitly to infinite sets before stating the equivalence. Mathematically sufficient, but the Classical implication wording is narrower textually and preserves the paragraph's arbitrary-set context without redefining enumerable.

Expert question (open to correction): Do يقتضي and بل clearly distinguish a necessary no-bijection consequence from the stronger no-surjection assertion? Please check that finite sets, including a singleton, are not labelled nonenumerable merely because they lack a Nat bijection.

Exact changed source ranges: 25–27.

Additional literal phrase choice: A stronger no-surjection consequence, not an equivalent paraphrase of no bijection.

English: that is. Before: أي لا توجد دالة. Chosen: بل لا توجد دالة. Classical: بل لا توجد دالة.

English that is and retained MSA أي introduce an allegedly equivalent paraphrase. No bijection and no surjection are not equivalent for a singleton. بل separately strengthens the consequence of nonenumerability, matching the actual Classical connective. The listed phrases are literal source text, not an ellipsis joining separate occurrences.

Expert question (open to correction): Does بل لا توجد دالة clearly strengthen the consequence rather than present no surjection as synonymous with no bijection?

## OLP-0072: no restrictions on t / eigenvariable condition

Literal English phrase: no restrictions. Classical phrase: من جهة المتغير المميَّز.

Before: لا ترد أي قيود على الحد. Chosen: لا ترد أي قيود من جهة المتغير المميَّز على الحد.

Both English and MSA first require t to be closed, then say there are no restrictions on t. Classical limits the latter statement to eigenvariable restrictions. We insert من جهة المتغير المميَّز, retaining MSA's existing spelling of eigenvariable. The earlier closedness requirements, the eigenconstant conditions for the other two rules, all rule schemas and the invalid derivation example stay exactly unchanged. This is an inherited expository scope clarification, not evidence that the formal calculus previously admitted open terms.

Mathematical reason: A variable x is a term but is not closed. The unrestricted literal reading would admit it, contrary to the explicit closed-term condition. A constant c is closed and may already occur in the surrounding sequent for existential-right/universal-left; the other quantifier rules impose their own freshness conditions.

Alternative considered: repeat the closed-term requirement instead of naming the missing restriction. Closedness is already stated twice. Naming the scope of the absent restriction directly resolves the apparent conflict and preserves the contrast with eigenvariable rules.

Expert question (open to correction): Does من جهة المتغير المميَّز make it clear that arbitrary choice among closed terms is allowed without removing closedness? Is المتغير المميَّز understood as the historical name for a constant/eigenparameter in these rules?

Exact changed source ranges: 81–81.

## OLP-0081: if any of the soundness properties do not hold

Literal English phrase: do not hold. Classical phrase: فإذا تخلف شيء منها.

Before: فإذا لم تتحقق أي منها. Chosen: فإذا تخلّفت واحدة على الأقل منها.

English says if any of the properties do not hold; Classical accurately says إذا تخلف شيء منها. The retained MSA فإذا لم تتحقق أي منها can naturally mean that none holds. We make the intended scope explicit with واحدة على الأقل, so one or more failed requirements suffice. This is a translation-level quantifier-scope ambiguity, not an inherited English error. The three properties themselves, the soundness theorem, all semantic arguments and prior source-correction notes are untouched.

Mathematical reason: For the Boolean valuation (true,true,false), at least one requirement fails, but it is false that none holds. This truth-assignment counterexample distinguishes the two readings of the sentence; it does not assert that a particular proof calculus realizes independently varying soundness properties.

Alternative considered: فإذا تخلّفت إحدى هذه الخصائص. Also expresses failure of one required property, but واحدة على الأقل makes explicit that the condition includes multiple failures and is not exactly-one.

Expert question (open to correction): Does فإذا تخلّفت واحدة على الأقل منها clearly express that any single failed requirement suffices, while including cases where more than one fails? Please preserve the distinction between السلامة of the calculus and الصلاحية of sequents.

Exact changed source ranges: 27–27.

[Exact-source, inverse-patch and decision evidence](OLP0033_0039_0072_0081_QUALIFICATION_PROPAGATION_20260906.json).

These source repairs do not claim that revised reader PDFs have been built or published.

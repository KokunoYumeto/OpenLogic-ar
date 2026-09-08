# Four missing qualifications carried into both MSA editions

New independent assessments, 6 September 2026. These are source clarifications
already present in Classical, not claims about the original translator’s reasoning.
Arabic choices remain provisional and open to correction; no official dictionary
attestation is claimed. Final printed/PDF pages are not yet bound.

| Where to check | Chosen MSA wording | Why check this? |
|---|---|---|
| [OLP-0005, source line 87](../../../source/locale/ar/content/sets-functions-relations/sets/basics.tex#L87) | إذا وُجدت مجموعة | Extensionality gives uniqueness of a set with specified members, conditional on existence; it does not imply unrestricted comprehension. |
| [OLP-0008, source line 120](../../../source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L120) | مجموعة غير خالية من المجموعات | An absolute intersection of a set-indexed family needs a nonempty family here; empty intersections require an explicitly fixed ambient universe. |
| [OLP-0016, source line 75](../../../source/locale/ar/content/sets-functions-relations/relations/orders.tex#L75) | لكنها ليست ترتيبًا خطيًا بوجه عام | The prefix order on finite words over an arbitrary alphabet is a partial order and is not linear in general; empty and singleton alphabets are exceptions. |
| [OLP-0018, source line 110](../../../source/locale/ar/content/sets-functions-relations/relations/trees.tex#L110) | كل مجموعة غير خالية | A prefix-closed subset of finite natural-number sequences is a rooted subtree only if it is nonempty under this book’s definition of tree. |

## OLP-0005: extensionality

Old wording: **تضمن الامتدادية أن هناك دائمًا**. Chosen wording: **إذا وُجدت مجموعة**.

The English and retained MSA wording could make extensionality itself guarantee a set for every property. Classical already made the uniqueness claim conditional. The same book explicitly distinguishes existence from uniqueness in OLP-0010 and gives the Russell predicate as a counterexample. We write إذا وُجدت مجموعة to expose the existence condition, and add a plain-language sentence distinguishing uniqueness from existence. This is a disclosed clarification of an inherited source overstatement, not a claim that the English explicitly stated the condition.

Mathematical reason: For the Russell predicate x not in x, assuming its extension is a set R gives R in R iff R not in R. Neither Boolean membership value satisfies this; extensionality cannot supply such existence.

Alternative: at most one set. Mathematically equivalent as a uniqueness claim; the selected conditional construction connects more clearly to the existing definite-description sentence.

**Expert question (open to correction):** Is إذا وُجدت مجموعة followed by the explicit uniqueness/existence distinction clear Arabic here? Would على الأكثر مجموعة واحدة express the qualification better without implying unrestricted set existence?

Exact changed source ranges: 87–88, 90–91.

## OLP-0008: intersection

Old wording: **مجموعة من المجموعات**. Chosen wording: **مجموعة غير خالية من المجموعات**.

Classical correctly adds nonemptiness to the family and index for intersection, and explains the source correction. The shared MSA omitted all three qualifications. With no fixed ambient set, the membership condition for an empty family is vacuously true for every object, so it does not specify a set by this definition. We carry the nonempty condition and its explanatory note into MSA and restrict only the intersection abbreviation. Empty unions and all displayed formulas are preserved.

Mathematical reason: For an empty family, the relative intersection inside {0} is {0}, but inside {0,1} is {0,1}. This demonstrates dependence on the ambient universe. For a nonempty family, choose one member as a bounding set.

Alternative: define empty intersection relative to a fixed universe. Valid in a relative-universe treatment, but no such universe is fixed here. Adding one would change the exposition more than propagating the existing Classical qualification.

**Expert question (open to correction):** Are عائلة التقاطع and مجموعة الفهرسة غير خالية clear and consistent terms for the nonempty intersection family and its index? Please check that the text cannot be read as forbidding empty unions.

Exact changed source ranges: 120–120, 125–131, 149–150.

## OLP-0016: extension relation

Old wording: **لكنها ليست ترتيبًا خطيًا**. Chosen wording: **لكنها ليست ترتيبًا خطيًا بوجه عام**.

The English and MSA statement lacked the generality qualification that Classical already supplies. Over a singleton alphabet, words are comparable by length; over the empty alphabet there is only the empty word. The given incomparable ab and ba require two distinct alphabet symbols. Adding بوجه عام retains the example and all formulas while avoiding an incorrect universal assertion. It matches an existing MSA use of the same qualifier for the subset-order example.

Mathematical reason: A singleton alphabet produces exactly a^n for n>=0, linearly ordered by prefix. The empty alphabet produces only the empty word. For two symbols, ab and ba are incomparable.

Alternative: state explicitly that the alphabet has at least two elements. Also correct for the non-linearity claim, but not necessary for the definition or partial-order claim. The existing conditional two-letter example and generality qualifier preserve the broader domain.

**Expert question (open to correction):** Does بوجه عام sufficiently mark the exception for empty and singleton alphabets? Would explicitly stating that a and b belong to the alphabet be clearer for beginning readers?

Exact changed source ranges: 75–75.

## OLP-0018: subtree

Old wording: **كل مجموعة**. Chosen wording: **كل مجموعة غير خالية**.

The definition requires an existing root. The empty set is vacuously prefix-closed but has no root, so the later unrestricted subtree assertion was too broad in English and MSA. Classical already adds غير خالية and an explicit source-correction note. We carry both into the shared MSA reader. A nonempty prefix-closed subset contains the empty sequence, which supplies the root; predecessor sequences of any node form a finite chain. Existing branch and other proof corrections are untouched.

Mathematical reason: The empty set is prefix-closed but has no element serving as root. Every nonempty prefix-closed set of finite words contains the empty word, the unique least word.

Alternative: allow empty trees by changing the earlier definition. Not selected: it would alter the stated rooted-tree convention and potentially later results. The narrow hypothesis is sufficient and already present in Classical.

**Expert question (open to correction):** Is شجرة جزئية with the explicit غير خالية qualification natural and unambiguous under this book’s rooted-tree convention? Please distinguish this convention from ones that allow an empty tree.

Exact changed source ranges: 110–110, 113–118.

[Full exact-source, inverse-patch and decision evidence](OLP0005_0008_0016_0018_QUALIFICATION_PROPAGATION_20260906.json).

These local source repairs do not claim that revised reader PDFs have been built or published.

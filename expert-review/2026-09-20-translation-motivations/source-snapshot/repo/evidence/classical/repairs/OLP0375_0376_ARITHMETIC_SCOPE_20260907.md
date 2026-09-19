# Arithmetic wording: places worth checking / مواضع للمراجعة

Applied 7 September 2026 in both Arabic wording registers. Provisional and
open to correction. These are newly recorded reasons, not a claim about the
original translator's thinking. The accompanying [JSON ledger](OLP0375_0376_ARITHMETIC_SCOPE_20260907.json)
preserves exact before/after words, source hashes, inverse patches and witnesses.

Printed and PDF pages are **not yet bound**. The following exact source lines
refer to the newly corrected local source; integration into the full reviewer
index and the next consolidated reader release remains pending.

## OLP-0375 — exponentiation, not the exponent / رفع العدد إلى قوة

Choice: **رفع العدد إلى قوة / دالة القوى** for the operation; **الأس** for
its second argument. Restrict the compact first term to a positive exponent;
use the already printed iterated-multiplication term for all natural inputs.

Where:

- MSA (International and Machrek): [arithmetical-functions.tex, line 121](../../../source/locale/ar/content/lambda-calculus/lambda-definability/arithmetical-functions.tex#L121), with the original-source clarification at lines 132–136.
- Classical: [arithmetical-functions.tex, line 124](../../../source/locale/ar-classical/content/lambda-calculus/lambda-definability/arithmetical-functions.tex#L124), with the clarification at lines 136–141.

Why: at exponent zero the compact term reduces to the identity, not Church
one. The preceding definition demands reduction to the numeral itself, not
merely equivalent behavior. The second term performs zero multiplications
starting at Church one and does give the required numeral. Its total-natural
interpretation uses the explicitly stated convention that a zero power is
one, including a zero base. No formula was replaced.

Please check: هل يوضح «رفع العدد إلى قوة» الفرق بين العملية والأس، وهل
يبين التنبيه شرط المخرج العددي وحال الأس الصفري؟ الاصطلاح قابل للتصحيح.

Official dictionary attestation was not checked or claimed. Stable decision:
`AR-OLP-0375-ZERO-EXPONENT-20260907`.

## OLP-0375 — pairs are the method used here / طريق التعريف هنا

Choice: **وسنعرّفهما هنا باستعمال ترميز الأزواج** (MSA) and
**وسبيلنا إلى تعريفهما هنا أن نستعمل ترميز الأزواج** (Classical).

Where: final prose paragraph, [MSA line 139](../../../source/locale/ar/content/lambda-calculus/lambda-definability/arithmetical-functions.tex#L139)
and [Classical line 144](../../../source/locale/ar-classical/content/lambda-calculus/lambda-definability/arithmetical-functions.tex#L144).

Why: the previous Classical phrase “لا يتم تعريفهما إلا” suggested that no
other method was possible. This section gives a construction, not a theorem
of that necessity. The qualification preserves the transition to the next
section without making the stronger claim.

Please check: هل تبين «هنا» أن الأزواج هي طريق التعريف المختار، من غير
أن توهم استحالة كل طريق آخر؟ الصياغة مفتوحة للتصحيح.

Stable decision: `AR-OLP-0375-PAIR-METHOD-20260907`.

## OLP-0376 — subtraction stops at zero / الوقوف عند الصفر

Choice: **الطرح على الأعداد الطبيعية مع الوقوف عند الصفر**.

Where: [MSA pairs.tex, line 46](../../../source/locale/ar/content/lambda-calculus/lambda-definability/pairs.tex#L46)
and [Classical pairs.tex, line 47](../../../source/locale/ar-classical/content/lambda-calculus/lambda-definability/pairs.tex#L47).

Why: repeated predecessor cannot pass below zero. Subtracting five from two
produces Church zero, not negative three or an undefined result. The new
prose states both cases explicitly and identifies the qualification of the
unrestricted English word “subtraction.” The defining term is unchanged.

Please check: هل هذه العبارة أوضح من «الطرح المبتور»؟ وهل تميز العملية
من الطرح على الأعداد الصحيحة أو الطرح الجزئي؟ الاختيار مفتوح للتصحيح.

The longer descriptive wording was preferred without claiming official
attestation. Stable decision: `AR-OLP-0376-TRUNCATED-SUBTRACTION-20260907`.

## Verified scope

Eight focused tests pass: four exact source inverses, all preserved
formula/reference/terminology structures, two unchanged English files, the
supporting definition, occurrence bindings, and 75 bounded beta-normalization
examples. Finite examples supplement the ledger's inductive explanation;
they do not certify the entire book or rendered readers.

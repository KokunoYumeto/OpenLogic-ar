# Expert-readable Arabic translation audit: OLP-0391–0410

مراجعة مواضع الترجمة الحساسة — القرارات مؤقتة ومفتوحة للتصحيح، ولا يتوقف العمل على مراجعة بشرية.

20 units fully read against frozen English, shared MSA and Classical Arabic (60 files). This is a separate read-only intake: no source edits, builds or publication; the frozen eight-decision batch is unchanged.

49 reviewed terminology choices; 141 exact Arabic occurrences. Four definite correction proposals and two wording ambiguities are listed below. Reasons are retrospective assessments, not recovered original translator motivations. No dictionary attestation or PDF page numbering is claimed.

## Check these six places first

| ID / unit | What to double-check | Where | Later-batch disposition |
|---|---|---|---|
| C391-0410-F01 / OLP-0394 | راجِع قيمة الصيغة في الفقرة الأخيرة: الناتج كاذب، لا غير محدد. | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:227>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:219>) | Definite correction proposal; not applied |
| C391-0410-F02 / OLP-0399 | تعريف المجموعة V_m يحتاج إلى الشرط m≥2 حتى لا يكون المقام صفرًا. | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>) | Definite correction proposal; not applied |
| C391-0410-F03 / OLP-0400 | راجِع قولنا «ويصح ... عكس هذا الحكم»: يلزم هنا تقييد مجموعة المقدمات بالتناهي. | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>) | Definite correction proposal; not applied |
| C391-0410-F04 / OLP-0404 | في تعريف المبرهنة، هل يتضح أن المواضع غير المميزة خالية؟ | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:43>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:43>) | Ambiguity to clarify; not applied |
| C391-0410-F05 / OLP-0409 | ميّزوا «من الضروري أن يكون من الممكن...» من «من الممكن أن يكون من الضروري...»؛ فالترتيب جزء من المعنى. | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:16>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:16>) | Ambiguity to clarify; not applied |
| C391-0410-F06 / OLP-0409 | انقلوا دقة «صدق عبارة الضرورة» من النسخة الكلاسيكية إلى النسختين ذواتي النص المشترك. | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:51>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:50>) | Definite correction proposal; not applied |

### C391-0410-F01: The final modal example evaluates to False, not Undef.

At v(p)=U, the displayed tables give ¬p=U, p∧¬p=U, ◇(p∧¬p)=True, and therefore ¬◇(p∧¬p)=False. All three sources print Undef as the last value. The objection that the formula is not a tautology survives, so only the exhibited value needs changing.

Why: Direct four-step calculation from this very unit; no terminology preference or external authority is involved.

Propagation: Both shared-MSA profiles and Classical require the same mathematical correction; frozen English should be cited as the inherited source, not silently rewritten by this audit.

Proposed wording (not current source):

- msa: $\pValue v(\lnot \Diamond(p \land \lnot p)) = \False$
- classical: $\pValue v(\lnot \Diamond(p \land \lnot p)) = \False$
- english_note: Replace the final RHS Undef with False; retain the tables and non-tautology conclusion.

Expert question, optional: Do you agree that only the final displayed value should be changed, preserving the intended counterexample?

Exact current source witnesses:

- [OLP-0394 english, lines 231–240](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:231>); SHA-256 `f4f46fab1263ab5437fc91964cf3e61a658ca18f5739c520a43f4e45f669f2ab`

```tex
However, the shortcomings of this proposed modal logic soon became
evident: However things turn out, $p \land \lnot p$ can never turn out
to be true. So even if it is not now settled (and therefore
undetermined), it should count as impossible, i.e., $\lnot \Diamond(p
\land \lnot p)$ should be a tautology. However, if $\pAssign v(p) =
\Undef$, then $\pValue v(\lnot \Diamond(p \land \lnot p)) =
\Undef$. Although \L ukasiewicz was correct that two truth
values will not be enough to accommodate modal distinctions such as
possiblity and necessity, introducing a third truth value is also not
enough.
```

- [OLP-0394 msa, lines 227–234](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:227>); SHA-256 `53eb87b345723bd978d1d82ed1f9caa19ad8857c7198e01da0e213afadd9c989`

```tex
غير أن أوجه قصور هذا المنطق الجهي المقترح سرعان ما ظهرت: كيفما آلت
الأمور، لا يمكن أن يتبين أبدًا أن~$p \land \lnot p$ صادق. ولذلك، حتى
إذا لم يكن متعينًا الآن (فكان غير محدد)، ينبغي أن يعد مستحيلًا؛ أي
ينبغي أن تكون~$\lnot \Diamond(p \land \lnot p)$ تحصيلًا منطقيًا.
لكن إذا كان~$\pAssign v(p) = \Undef$، فإن
$\pValue v(\lnot \Diamond(p \land \lnot p)) = \Undef$. ومع أن
\L ukasiewicz كان محقًا في أن قيمتي صدق لا تكفيان لاستيعاب تمييزات
جهية كالإمكان والضرورة، فإن إدخال قيمة صدق ثالثة لا يكفي أيضًا.
```

- [OLP-0394 classical, lines 219–225](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:219>); SHA-256 `5eeb1f6b952f6d8dee4cfe789ddec9adf2e661c1049de80db6a389314e50f8eb`

```tex
لكن قصور هذا المنطق الجهي المقترح يظهر سريعًا. فمهما آل الأمر، يمتنع
أن يتبين~$p \land \lnot p$ صادقًا؛ فهو مستحيل، وإن لم يتعين الآن
فكان غير محدد. فينبغي إذن أن تكون~$\lnot \Diamond(p \land \lnot p)$
تحصيلًا منطقيًا. غير أن~$\pAssign v(p) = \Undef$ يجعل
$\pValue v(\lnot \Diamond(p \land \lnot p)) = \Undef$.
فقد أصاب~\L ukasiewicz في أن قيمتي صدق لا تفيان بتمييزات الجهة،
كالإمكان والضرورة، لكن مجرد إضافة قيمة ثالثة لا يفي بها أيضًا.
```

- [OLP-0394 classical, lines 76–90](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:76>); SHA-256 `5eeb1f6b952f6d8dee4cfe789ddec9adf2e661c1049de80db6a389314e50f8eb`

```tex
    \begin{tabular}{c|c}
      $\tf{\lnot}$ & \\
      \hline
      $\True$ & $\False$ \\
      $\Undef$ & $\Undef$ \\
      $\False$ & $\True$
    \end{tabular}
    \quad
    \begin{tabular}{c|ccc}
      $\tf{\land}[\LogLuk[3]]$ & $\True$ & $\Undef$ & $\False$ \\
      \hline
      $\True$ & $\True$ & $\Undef$ & $\False$ \\
      $\Undef$ & $\Undef$ & $\Undef$ & $\False$\\
      $\False$ & $\False$ & $\False$ & $\False$
    \end{tabular}
```

- [OLP-0394 classical, lines 193–211](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:193>); SHA-256 `5eeb1f6b952f6d8dee4cfe789ddec9adf2e661c1049de80db6a389314e50f8eb`

```tex
\begin{center}
  \begin{tabular}{c|c}
    $\tf{\Diamond}$ & \\
    \hline
    $\True$ & $\True$ \\
    $\Undef$ & $\True$ \\
    $\False$ & $\False$
  \end{tabular}
  \quad
  \begin{tabular}{c|c}
    $\tf{\Box}$ & \\
    \hline
    $\True$ & $\True$ \\
    $\Undef$ & $\False$ \\
    $\False$ & $\False$
  \end{tabular}
\end{center}
فمؤدى الجدولين أن~$p$ ممكن إذا وفقط إذا لم يتعين كاذبًا بالفعل،
وأن~$p$ ضروري إذا وفقط إذا تعين صادقًا بالفعل.
```


### C391-0410-F02: Restrict the finite truth-value family V_m to natural m≥2.

Both Arabic files already repair V-infinity by adding m>0 and V_m by replacing n≤m with n<m. They still introduce V_m without restricting m. With m=1 and n=0, the fraction is 0/0. With the project's zero-inclusive naturals, m=0 also fails to describe the intended nonempty finite matrix. The later propositions quantify m≥2, identifying the intended domain.

Why: The m−1 denominator and m-element grid require m≥2; this is independent of notation profile and preserves zero-inclusive Nat.

Propagation: One shared definition repair in MSA and Classical. References to V_m in 0400/0401 inherit that domain; they are cross-locations, not separate newly counted defects.

Proposed wording (not current source):

- msa: النظر أيضًا، لكل عدد طبيعي~$m\ge2$، في المجموعات الجزئية
- classical: النظر أيضًا، لكل عدد طبيعي~$m\ge2$، في المجموعات الجزئية
- placement: Replace the intertext continuation at 0399 line 19; preserve the existing correct n<m and V-infinity m>0 restrictions.

Expert question, optional: Is the proposed introducing prose the clearest place to state m∈Nat and m≥2 for every subsequent use of V_m?

Exact current source witnesses:

- [OLP-0399 english, lines 13–24](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>); SHA-256 `affd39b02580135e472d159f31cbe2a5805f344a9eab515a4bce7fd18999889e`

```tex
The number of truth values of a matrix need not be finite.  An obvious
choice for a set of infinitely many truth values is the set of
rational numbers between $0$ and~$1$, $V_\infty = [0,1] \cap \Rat$,
i.e.,
\begin{align*}
    V_\infty & = \Setabs{\frac{n}{m}}{n,m \in \Nat \text{ and } n\le m}.
\intertext{When considering this infinite truth value set, it is often
useful to also consider the subsets}
V_m & = \Setabs{\frac{n}{m-1}}{n \in \Nat \text{ and } n\le m}
\intertext{For instance, $V_5$ is the set with $5$ evenly spaced truth values,}
V_5 & = \{0, \frac{1}{4}, \frac{1}{2}, \frac{3}{4}, 1\}.
\end{align*}
```

- [OLP-0399 msa, lines 13–23](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>); SHA-256 `e44d252e238bcad4d6532088ecff7ba7f9f0a3c09990d6ec77f8b7928ecf9dd7`

```tex
لا يلزم أن يكون عدد قيم الصدق في المصفوفة منتهيًا. ومن الخيارات
الواضحة لمجموعة غير منتهية من قيم الصدق مجموعة الأعداد النسبية بين
$0$ و$1$، أي~$V_\infty = [0,1] \cap \Rat$؛ وبعبارة أخرى،
\begin{align*}
    V_\infty & = \Setabs{\frac{n}{m}}{n,m \in \Nat \text{ و } m>0 \text{ و } n\le m}.
\intertext{وعند النظر في مجموعة قيم الصدق غير المنتهية هذه، يفيد غالبًا
النظر أيضًا في المجموعات الجزئية}
V_m & = \Setabs{\frac{n}{m-1}}{n \in \Nat \text{ و } n<m}
\intertext{فمثلًا، $V_5$ هي المجموعة ذات قيم الصدق الخمس المتساوية التباعد،}
V_5 & = \{0, \frac{1}{4}, \frac{1}{2}, \frac{3}{4}, 1\}.
\end{align*}
```

- [OLP-0399 classical, lines 13–23](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>); SHA-256 `0f5370d39be3c71fc1fb071977324bbefa1ce7f8d082bd5dfb480612ba2312fb`

```tex
ليس من شرط المصفوفة أن تكون قيم الصدق فيها متناهية. ومن أظهر
الخيارات لمجموعة لا متناهية مجموعة الأعداد النسبية المحصورة بين
$0$ و$1$، وهي~$V_\infty = [0,1] \cap \Rat$؛ أي
\begin{align*}
    V_\infty & = \Setabs{\frac{n}{m}}{n,m \in \Nat \text{ و } m>0 \text{ و } n\le m}.
\intertext{وعند النظر في مجموعة قيم الصدق غير المنتهية هذه، يفيد غالبًا
النظر أيضًا في المجموعات الجزئية}
V_m & = \Setabs{\frac{n}{m-1}}{n \in \Nat \text{ و } n<m}
\intertext{فمثلًا، $V_5$ هي المجموعة ذات قيم الصدق الخمس المتساوية التباعد،}
V_5 & = \{0, \frac{1}{4}, \frac{1}{2}, \frac{3}{4}, 1\}.
\end{align*}
```

- [OLP-0400 msa, lines 36–37](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:36>); SHA-256 `ff15f7a1eaeee1da4124ac5292c4fc8754a8a541f7cee1efae71e16a9362e084`

```tex
ويعرّف منطق~\L ukasiewicz ذو~$m$ من القيم بالطريقة نفسها، عدا أن
$V = V_m$.
```

- [OLP-0400 classical, lines 84–87](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>); SHA-256 `8cf51285f0f69c513fbbf95d4055e8a27f624de782588d2cb77a9598840a1ba2`

```tex
\begin{prop}\ollabel{prop:luk-infty-m}
  إذا كان~$\Gamma \Entails[\LogLuk[\infty]] !B$، كان
  $\Gamma \Entails[\LogLuk[m]] !B$ لكل~$m \ge 2$.
\end{prop}
```

- [OLP-0401 classical, lines 86–89](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:86>); SHA-256 `86daad125ae0dbfb36b06be473b6432cd4e551c069d006a873c664f398037561`

```tex
\begin{prop}\ollabel{prop:god-infty-m}
  إذا كان~$\Gamma \Entails[\LogGod[\infty]] !B$، فإن
  $\Gamma \Entails[\LogGod[m]] !B$ لكل~$m \ge 2$.
\end{prop}
```


### C391-0410-F03: The converse from all finite Łukasiewicz matrices requires a premise restriction.

The forward result Γ⊨L∞B ⇒ Γ⊨LmB for every m≥2 is valid. The following unqualified converse is false for arbitrary infinite Γ over the rational V-infinity defined in 0399.

Why: Finite common denominators justify the finite-premise statement; the explicit infinite counterexample rules out the unrestricted one. 0401 already states the analogous finite-premise restriction in both Arabic versions.

Propagation: Apply the finite-premise qualification to both MSA profiles and Classical in a later batch. Do not alter the correct forward proposition or duplicate 0401's already present repair.

Proposed wording (not current source):

- msa: وإذا كانت مجموعة المقدمات متناهية، صح العكس أيضًا.
- classical: وإذا كانت مجموعة المقدمات متناهية، صح عكس هذا الحكم أيضًا.

Evidence / counterexample:

definitions: E(A,B)=(A→B)∧(B→A), whose Łukasiewicz value is 1 iff the values of A and B agree. D(x)=¬x→x=min(1,2x). Γ contains E(p1,¬p1), and E(pi,D(p(i+1))) for every i≥1.

proof: The first designated constraint forces p1=1/2. If pi=2^(-i)<1, the next constraint forces pi=min(1,2p(i+1)), hence p(i+1)=pi/2. Thus every model of Γ must assign pi=2^(-i). These are all rational values in V-infinity, so Γ has an infinite-matrix model with a fresh q=0. No finite V_m contains every positive dyadic 2^(-i), so Γ has no V_m model for any m≥2. Consequently Γ⊨Lm q vacuously for every finite m but Γ⊭L∞ q.

finite_premise_remedy_proof: For finite Γ and one conclusion, only finitely many variables occur. A rational V-infinity countervaluation has a finite common denominator d on those variables; all values belong to V_(d+1), which is closed under the given complement/min/max/implication operations. Hence that countervaluation supplies a finite-matrix countermodel. For d=1 use V_2.


Expert question, optional: Does the finite-premise sentence, with the dyadic counterexample retained in the review log, express the intended consequence claim most clearly?

Exact current source witnesses:

- [OLP-0400 english, lines 83–96](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:83>); SHA-256 `3b6867d8660841a2e8ce81b27726e0848efb71629edd19aa77fd8cbc638ed543`

```tex
\begin{prop}\ollabel{prop:luk-infty-m}
  If $\Gamma \Entails[\LogLuk[\infty]] !B$ then $\Gamma
  \Entails[\LogLuk[m]] !B$ for all~$m \ge 2$.
\end{prop}

\begin{proof}
  Exercise.
\end{proof}

\begin{prob}
  Prove \olref[mvl][inf][luk]{prop:luk-infty-m}.
\end{prob}

In fact, the converse holds as well.
```

- [OLP-0400 msa, lines 84–97](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>); SHA-256 `ff15f7a1eaeee1da4124ac5292c4fc8754a8a541f7cee1efae71e16a9362e084`

```tex
\begin{prop}\ollabel{prop:luk-infty-m}
  إذا كان~$\Gamma \Entails[\LogLuk[\infty]] !B$، فإن
  $\Gamma \Entails[\LogLuk[m]] !B$ لكل~$m \ge 2$.
\end{prop}

\begin{proof}
  تمرين.
\end{proof}

\begin{prob}
  أثبت \olref[mvl][inf][luk]{prop:luk-infty-m}.
\end{prob}

وفي الواقع يصح العكس أيضًا.
```

- [OLP-0400 classical, lines 84–97](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>); SHA-256 `8cf51285f0f69c513fbbf95d4055e8a27f624de782588d2cb77a9598840a1ba2`

```tex
\begin{prop}\ollabel{prop:luk-infty-m}
  إذا كان~$\Gamma \Entails[\LogLuk[\infty]] !B$، كان
  $\Gamma \Entails[\LogLuk[m]] !B$ لكل~$m \ge 2$.
\end{prop}

\begin{proof}
  إثبات ذلك تمرين.
\end{proof}

\begin{prob}
  أثبت \olref[mvl][inf][luk]{prop:luk-infty-m}.
\end{prob}

ويصح في الحقيقة عكس هذا الحكم أيضًا.
```

- [OLP-0400 classical, lines 20–37](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:20>); SHA-256 `8cf51285f0f69c513fbbf95d4055e8a27f624de782588d2cb77a9598840a1ba2`

```tex
  \item الجزء الخالي من الثوابت~$\Lang L_0^{-}$ من لغة القضايا القياسية، ذو الروابط
  $\lnot$ و$\land$ و$\lor$ و$\lif$.
  % تصحيح مصدر مشترك (MVL-L0-I1): حُددت اللغة الخالية من lfalse التي تفسر المصفوفة جميع روابطها.
  \item مجموعة قيم الصدق~$V_\infty$.
  \item القيمة المميزة وحدها هي~$1$؛ أي~$V^+ = \{1\}$.
  \item دوال الصدق هي الدوال الآتية:
  \begin{align*}
    \tf{\lnot}[\LogLuk](x) & = 1 - x\\
    \tf{\land}[\LogLuk](x,y) & = \min(x,y)\\
    \tf{\lor}[\LogLuk](x,y) & = \max(x,y)\\
    \tf{\lif}[\LogLuk](x,y) & = \min(1,1-(x-y)) = \begin{cases}
      1 & \text{إذا كان } x \le y\\
      1-(x-y) & \text{في غير ذلك.}
    \end{cases}
    \end{align*}
\end{enumerate}
وأما منطق~\L ukasiewicz ذو~$m$ من القيم فيعرف على الوجه نفسه، إلا
أن~$V = V_m$.
```

- [OLP-0399 classical, lines 13–22](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>); SHA-256 `0f5370d39be3c71fc1fb071977324bbefa1ce7f8d082bd5dfb480612ba2312fb`

```tex
ليس من شرط المصفوفة أن تكون قيم الصدق فيها متناهية. ومن أظهر
الخيارات لمجموعة لا متناهية مجموعة الأعداد النسبية المحصورة بين
$0$ و$1$، وهي~$V_\infty = [0,1] \cap \Rat$؛ أي
\begin{align*}
    V_\infty & = \Setabs{\frac{n}{m}}{n,m \in \Nat \text{ و } m>0 \text{ و } n\le m}.
\intertext{وعند النظر في مجموعة قيم الصدق غير المنتهية هذه، يفيد غالبًا
النظر أيضًا في المجموعات الجزئية}
V_m & = \Setabs{\frac{n}{m-1}}{n \in \Nat \text{ و } n<m}
\intertext{فمثلًا، $V_5$ هي المجموعة ذات قيم الصدق الخمس المتساوية التباعد،}
V_5 & = \{0, \frac{1}{4}, \frac{1}{2}, \frac{3}{4}, 1\}.
```

- [OLP-0401 msa, lines 99–101](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:99>); SHA-256 `0529de2c1be492d463ca9af45feb88be41afee1dc8b588ea98f330640f1ca06c`

```tex
% تصحيح مصدر (0401-I1): لا يصح العكس المعلن هنا إلا مع مقدمات متناهية.
وإذا كانت مجموعة المقدمات متناهية، صح العكس أيضًا.

```

- [OLP-0401 classical, lines 99–101](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:99>); SHA-256 `86daad125ae0dbfb36b06be473b6432cd4e551c069d006a873c664f398037561`

```tex
% تصحيح مصدر (0401-I1): لا يصح العكس المعلن هنا إلا مع مقدمات متناهية.
وإذا كانت مجموعة المقدمات متناهية، فليس اللزوم مقصورًا على هذا الاتجاه؛
بل يصح عكسه أيضًا.
```


### C391-0410-F04: Make the empty undesignated positions explicit in the theorem sequent.

The definition says the n-sequent contains A in every designated position, without explicitly emptying the others. If 'contains' were read as allowing arbitrary additional entries, the initial A|...|A would satisfy it for every A. The intended specific sequent is recoverable from the adjacent derivability definition with Γ empty. This is an ambiguity, not a finding that the intended calculus really declares every sentence a theorem.

Why: The adjacent definition makes Γ0' occupy undesignated positions; with no premises that sequence is empty. Saying so prevents confusion with initial sequents.

Propagation: Optional precision repair shared by both MSA profiles and Classical; inherited from English.

Proposed wording (not current source):

- msa: تحتوي~$!A$ وحدها في كل موضع يقابل قيمة صدق مميّزة في~$\Log{L}$، وتخلو المواضع الأخرى.
- classical: تحتوي~$!A$ وحدها في كل موضع يقابل قيمة صدق مميّزة في~$\Log{L}$، وتخلو المواضع الأخرى.

Expert question, optional: Would explicitly stating 'A alone in designated slots, all other slots empty' avoid the initial-sequent ambiguity without overloading the definition?

Exact current source witnesses:

- [OLP-0404 english, lines 44–61](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:44>); SHA-256 `bc7f60e5e64ad1000db484141861723f90d7eee4316d1885263c3db652089972`

```tex
\begin{defn}[Theorems]
!!^a{sentence}~$!A$ is a \emph{theorem} of an $n$-valued
logic~$\Log{L}$ if there is !!a{derivation}
of the $n$-sequent containing $!A$ in each position corresponding to a
designated truth value of~$\Log{L}$.  We write $\Proves[\Log{L}]
!A$ if $!A$ is a theorem and $\Proves/[\Log{L}] !A$ if it is not.
\end{defn}

\begin{defn}[!!^{derivability}]
!!^a{sentence}~$!A$ is \emph{!!{derivable} from} a set of
!!{sentence}s~$\Gamma$ in an $n$-valued logic~$\Log{L}$, $\Gamma
\Proves[\Log{L}] !A$, iff there is a finite subset~$\Gamma_0 \subseteq
\Gamma$ and a sequence $\Gamma_0'$ of the !!{sentence}s in~$\Gamma_0$
such that the following sequent has  !!a{derivation}:
\[ \Lambda_1 \nSequent \dots \nSequent \Lambda_n \] where $\Lambda_i$
is $!A$ if position $i$ corresponds to a designated truth value, and
$\Gamma_0'$otherwise. If $!A$ is not !!{derivable} from $\Gamma$ we
write $\Gamma \Proves/ !A$.
```

- [OLP-0404 msa, lines 43–62](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:43>); SHA-256 `668a742d3d940e9f39237c3e189deab767cde72f4c1597347daf0f8141ae168f`

```tex
\begin{defn}[المبرهنات]
تكون !!^a{sentence}~$!A$ \emph{مبرهنة} في منطق ذي~$n$ من القيم
$\Log{L}$ إذا وُجد !!a{derivation} للتتابعية ذات الجوانب~$n$ التي
تحتوي~$!A$ في كل موضع يقابل قيمة صدق مميّزة في~$\Log{L}$. ونكتب
$\Proves[\Log{L}] !A$ إذا كانت~$!A$ مبرهنة، ونكتب
$\Proves/[\Log{L}] !A$ إذا لم تكن كذلك.
\end{defn}

\begin{defn}[!!^{derivability}]
تكون !!^a{sentence}~$!A$ \emph{!!{derivable} من} مجموعة
!!{sentence}s~$\Gamma$ في منطق ذي~$n$ من القيم~$\Log{L}$، أي
$\Gamma \Proves[\Log{L}] !A$، إذا وفقط إذا وُجدت مجموعة جزئية
منتهية~$\Gamma_0 \subseteq \Gamma$ ومتتالية~$\Gamma_0'$ من
ال!!{sentence}s في~$\Gamma_0$ بحيث يكون للتتابعية الآتية
!!a{derivation}:
\[ \Lambda_1 \nSequent \dots \nSequent \Lambda_n \]
حيث تكون~$\Lambda_i$ هي~$!A$ إذا كان الموضع~$i$ يقابل قيمة صدق
مميّزة، وتكون~$\Gamma_0'$ إذا كان يقابل قيمة صدق غير مميّزة. وإذا لم
تكن~$!A$ !!{derivable} من~$\Gamma$، كتبنا
$\Gamma \Proves/[\Log{L}] !A$.
```

- [OLP-0404 classical, lines 43–62](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:43>); SHA-256 `34d9abb8cd5e378c8e6269a89361676db1df1394eab7a7abe9fd1173dfcb070d`

```tex
\begin{defn}[المبرهنات]
تكون !!^a{sentence}~$!A$ \emph{مبرهنة} في منطق ذي~$n$ من القيم
$\Log{L}$ إذا وُجد !!a{derivation} للتتابعية ذات الجوانب~$n$ التي
تحتوي~$!A$ في كل موضع يقابل قيمة صدق مميّزة في~$\Log{L}$. ونكتب
$\Proves[\Log{L}] !A$ إذا كانت~$!A$ مبرهنة، ونكتب
$\Proves/[\Log{L}] !A$ إذا لم تكن كذلك.
\end{defn}

\begin{defn}[!!^{derivability}]
تكون !!^a{sentence}~$!A$ \emph{!!{derivable} من} مجموعة
!!{sentence}s~$\Gamma$ في منطق ذي~$n$ من القيم~$\Log{L}$، أي
$\Gamma \Proves[\Log{L}] !A$، إذا وفقط إذا وُجدت مجموعة جزئية
منتهية~$\Gamma_0 \subseteq \Gamma$ ومتتالية~$\Gamma_0'$ من
ال!!{sentence}s في~$\Gamma_0$ بحيث يكون للتتابعية الآتية
!!a{derivation}:
\[ \Lambda_1 \nSequent \dots \nSequent \Lambda_n \]
حيث تكون~$\Lambda_i$ هي~$!A$ إذا كان الموضع~$i$ يقابل قيمة صدق
مميّزة، وتكون~$\Gamma_0'$ إذا كان يقابل قيمة صدق غير مميّزة. وإذا لم
تكن~$!A$ !!{derivable} من~$\Gamma$، كتبنا
$\Gamma \Proves/[\Log{L}] !A$.
```

- [OLP-0404 classical, lines 25–33](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:25>); SHA-256 `34d9abb8cd5e378c8e6269a89361676db1df1394eab7a7abe9fd1173dfcb070d`

```tex
\begin{defn}[التتابعية الابتدائية]
\emph{التتابعية الابتدائية ذات الجوانب~$n$} تتابعية ذات جوانب~$n$ من
الصورة~$!A \nSequent \dots \nSequent !A$ لأي !!{sentence}~$!A$ في
اللغة.

وقد تشتمل اللغة على رابط صفري الرتبة~$\star$، وهو ثابت من ثوابت
القضايا. وحينئذ نعدّ التتابعية~$\dots \nSequent \star \nSequent \dots$
ابتدائية أيضًا، على أن يوضع~$\star$ وحده في الموضع الموافق لقيمة
الصدق~$\tf{\star} \in V$، وتخلو سائر المواضع.
```


### C391-0410-F05: Do not use the same compressed Arabic phrase for □◇ and ◇□.

English's initial examples say 'necessarily possible' (□◇). Its later iterated example begins 'Possibly necessarily' (◇□). Both Arabic versions use the same initial words 'من الممكن بالضرورة' in both places. That compressed phrase may be read as necessity applying to possibility or as an adverb modifying possible necessity; it does not display the distinct nesting carried by the English text. This report identifies a scope ambiguity rather than claiming every Arabic reader must choose the wrong reading.

Why: Possibility and necessity do not commute in general. Distinct nested clauses preserve the source operator order and remain ordinary scholarly Arabic.

Propagation: Both MSA profiles and Classical. This is an Arabic rendering issue, not the separate shared English world-independence issue.

Proposed wording (not current source):

- examples_2: \item من الضروري أن يكون من الممكن أن تمطر غدًا.
- examples_3: \item إذا كان من الضروري أن يكون من الممكن أن تصدق~$!A$، فمن الممكن أن تصدق~$!A$.
- iterated_example: «من الممكن أن يكون من الضروري \ldots أن يكون من الممكن أن تصدق~$!A$»
- editions: Use equivalent explicit nesting in both MSA and Classical.

Expert question, optional: Are the proposed nested أن clauses the most natural way to preserve □◇ versus ◇□ without relying on an English-like adverb order?

Exact current source witnesses:

- [OLP-0409 english, lines 17–20](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:17>); SHA-256 `42c2f00e8f81aab33744c17ecd192e38262a12cffa935cabb079a56e541618e2`

```tex
\item It is necessary that $2+2=4$.
\item It is necessarily possible that it will rain tomorrow.
\item If it is necessarily possible that~$!A$ then it is possible
  that~$!A$.
```

- [OLP-0409 english, lines 55–57](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:55>); SHA-256 `42c2f00e8f81aab33744c17ecd192e38262a12cffa935cabb079a56e541618e2`

```tex
descriptions. Carnap's approach could not handle \emph{iterated}
modalities, in that sentences of the form ``Possibly necessarily
\ldots possibly $!A$'' always reduce to the innermost modality.
```

- [OLP-0409 msa, lines 16–18](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:16>); SHA-256 `dec0f1a2cefc853af7abfa606d7ddfea555a3da30ad3c686cb54c1af2cfbe130`

```tex
\item من الضروري أن~$2+2=4$.
\item من الممكن بالضرورة أن تمطر غدًا.
\item إذا كان من الممكن بالضرورة أن~$!A$، فمن الممكن أن~$!A$.
```

- [OLP-0409 msa, lines 46–49](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:46>); SHA-256 `dec0f1a2cefc853af7abfa606d7ddfea555a3da30ad3c686cb54c1af2cfbe130`

```tex
\emph{صادقة بالضرورة} إذا كانت صادقة في جميع أوصاف الحالات. ولم يستطع
نهج كارناب معالجة الجهات \emph{المكررة}، إذ تختزل الجمل من الصورة
``من الممكن بالضرورة \ldots من الممكن أن~$!A$'' دائمًا إلى الجهة
الأعمق.
```

- [OLP-0409 classical, lines 16–18](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:16>); SHA-256 `dd5adbd70179dc2666ebdf5db3526540617073362199be13fabc52674ce38426`

```tex
\item من الضروري أن~$2+2=4$.
\item من الممكن بالضرورة أن تمطر غدًا.
\item إذا كان من الممكن بالضرورة أن~$!A$، فمن الممكن أن~$!A$.
```

- [OLP-0409 classical, lines 45–48](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:45>); SHA-256 `dd5adbd70179dc2666ebdf5db3526540617073362199be13fabc52674ce38426`

```tex
الاعتباطية~$!A$، جعل~$!A$ \emph{صادقة بالضرورة} إذا صدقت في كل
وصف للحالة. غير أن هذا البناء لا يميّز أثر الجهات \emph{المكررة}:
فالجملة من نحو «من الممكن بالضرورة \ldots من الممكن أن~$!A$»
تؤول فيه دائمًا إلى الجهة الأعمق.
```


### C391-0410-F06: Propagate 'truth of the necessity statement', not truth of any statement.

English says that truth of a statement at a world does not depend on that world in the global all-worlds approach. MSA follows that overbroad statement. Classical correctly says 'صدق عبارة الضرورة'. An atomic p can differ between worlds even when the universal necessity operator is world-independent.

Why: This propagates a mathematical clarification already present in the Classical text and is verified by an explicit two-world model.

Propagation: Shared MSA only (International and Machrek); Classical already contains the required precision. Cite frozen English as origin, without editing it.

Proposed wording (not current source):

- msa: إذ لا يعتمد صدق عبارة الضرورة في عالم~$w$ (أو وصف حالة~$s$) على~$w$ أصلًا.
- classical: Retain the existing precise wording at lines 53–54.

Evidence / counterexample:

Take two worlds with universal accessibility. Let p be true at w0 and false at w1. The value of p depends on the current world, while □p is false at both because p is not true in every world. Thus only the global necessity statement, not an arbitrary statement, has the claimed independence.

Expert question, optional: Does 'صدق عبارة الضرورة' adequately distinguish the world-invariant global modal assertion from the world-sensitive embedded formula?

Exact current source witnesses:

- [OLP-0409 english, lines 59–69](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:59>); SHA-256 `42c2f00e8f81aab33744c17ecd192e38262a12cffa935cabb079a56e541618e2`

```tex
The major breakthrough in modal semantics came with Saul Kripke's
article ``A Completeness Theorem in Modal Logic'' (JSL 1959). Kripke
based his work on Leibniz's idea that a statement is necessarily true
if it is true ``at all possible worlds.'' This idea, though, suffers
from the same drawbacks as Carnap's, in that the truth of statement at
a world $w$ (or a state description $s$) does not depend on $w$ at
all. So Kripke assumed that worlds are related by an
\emph{accessibility relation} $R$, and that a statement of the form
``Necessarily $!A$'' is true at a world $w$ if and only if
$!A$ is true at all worlds $w'$ \emph{accessible from}
$w$. Semantics that provide some version of this approach are called
```

- [OLP-0409 msa, lines 51–60](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:51>); SHA-256 `dec0f1a2cefc853af7abfa606d7ddfea555a3da30ad3c686cb54c1af2cfbe130`

```tex
جاء الاختراق الأهم في الدلالة الموجهية مع مقالة سول كريبكي ``مبرهنة
اكتمال في المنطق الموجهي'' (JSL 1959). بنى كريبكي عمله على فكرة
لايبنتس القائلة إن العبارة تكون صادقة بالضرورة إذا كانت صادقة ``في
جميع العوالم الممكنة''. غير أن هذه الفكرة تعاني المآخذ نفسها التي
يعانيها نهج كارناب، إذ لا يعتمد صدق العبارة في عالم~$w$ (أو وصف
حالة~$s$) على~$w$ أصلًا. لذلك افترض كريبكي أن العوالم ترتبط بعلاقة
\emph{وصول}~$R$، وأن عبارة من الصورة ``بالضرورة~$!A$'' تكون صادقة في
عالم~$w$ إذا وفقط إذا كانت~$!A$ صادقة في جميع العوالم~$w'$ التي
\emph{يمكن الوصول إليها من}~$w$. وتسمى الدلالات التي تقدم صورة ما من
هذا النهج دلالات كريبكي، وقد أتاحت التطور المتسارع للمنطقات الموجهية
```

- [OLP-0409 classical, lines 50–58](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:50>); SHA-256 `dd5adbd70179dc2666ebdf5db3526540617073362199be13fabc52674ce38426`

```tex
ثم كان التحول الكبير بمقالة سول كريبكي «مبرهنة اكتمال في المنطق
الموجهي» (JSL 1959). وأصل الفكرة عند لايبنتس: الضروري ما يصدق
«في جميع العوالم الممكنة». لكن الإطلاق في جميع العوالم يعيد إشكال
كارناب؛ إذ إن صدق عبارة الضرورة في عالم~$w$، أو في وصف حالة~$s$،
لا يتغير بتغير~$w$. فجعل كريبكي بين العوالم علاقة \emph{وصول}~$R$.
وعندئذ تكون عبارة «بالضرورة~$!A$» صادقة في العالم~$w$ متى وفقط
متى صدقت~$!A$ في جميع العوالم~$w'$ التي \emph{يمكن الوصول إليها
من}~$w$. وكل دلالة تأخذ بصورة من هذا البناء تسمى دلالة كريبكي.
وبه اتسع البحث اتساعًا عظيمًا، فصار الكلام على منطقات موجهية متعددة.
```

## Word-and-location index

Each heading is a display label. Arabic forms below are literal source substrings; ↵ marks a literal source line break, not an invented combined quote. Every listed choice is provisional and open to correction. MSA is shared by the International and Machrek profiles.

| Decision / unit | English sense label | MSA form | Classical form | First exact location |
|---|---|---|---|---|
| C391-0410-T01 / OLP-0391 | sublogics | منطقات جزئية | منطقات جزئية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:11>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:11>) |
| C391-0410-T02 / OLP-0391 | contrapositive | المعاكس النقيض | المعاكس النقيض | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:81>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:81>) |
| C391-0410-T03 / OLP-0392 | three-valued logics | المنطقات الثلاثية القيم | المنطقات الثلاثية القيم | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>) |
| C391-0410-T04 / OLP-0393 | designated value | مميزة | مميزة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/introduction.tex:17>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/introduction.tex:17>) |
| C391-0410-T05 / OLP-0394 | future contingent | المستقبلية العرضية | المستقبلية العرضية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:19>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:17>) |
| C391-0410-T06 / OLP-0394 | possible but not necessary | الممكن غير الضروري | الممكن الذي ليس بضروري | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:36>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:32>) |
| C391-0410-T07 / OLP-0395 | undefined | غير معرّف | غير معرف | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:25>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:15>) |
| C391-0410-T08 / OLP-0395 | unknown | مجهول | مجهول | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:35>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:32>) |
| C391-0410-T09 / OLP-0395 | strong Kleene logic | منطق كليني القوي | منطق كليني القوي | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:37>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:35>) |
| C391-0410-T10 / OLP-0395 | weak Kleene logic | منطق كليني الضعيف | منطق كليني الضعيف | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:85>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:83>) |
| C391-0410-T11 / OLP-0395 | meaningless | عديم المعنى | عديم المعنى | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:160>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:158>) |
| C391-0410-T12 / OLP-0395 | external negation | النفي الخارجي | النفي الخارجي | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:163>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:161>) |
| C391-0410-T13 / OLP-0396 | intuitionistic validity | المنطق الحدسي | الصحيحة حدسيًا | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:14>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/goedel.tex:14>) |
| C391-0410-T14 / OLP-0397 | logic of paradox | منطق المفارقة | منطق المفارقة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:20>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:20>) |
| C391-0410-T15 / OLP-0397 | logic of nonsense | منطق اللامعنى | منطق اللامعنى | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:31>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:32>) |
| C391-0410-T16 / OLP-0397 | paraconsistent | متسامح مع التناقض | متسامح مع ↵ التناقض | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:151>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:152>) |
| C391-0410-T17 / OLP-0397 | principle of explosion | مبدأ الانفجار | مبدأ الانفجار | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:152>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:153>) |
| C391-0410-T18 / OLP-0397 | 3-valued R-Mingle | منطق R-Mingle الثلاثي القيم | منطق R-Mingle الثلاثي القيم | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:171>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:173>) |
| C391-0410-T19 / OLP-0398 | infinite-valued logics | المنطقات اللانهائية القيم | المنطقات اللانهائية القيم | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>) |
| C391-0410-T20 / OLP-0399 | rational numbers | الأعداد النسبية | الأعداد النسبية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:14>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:14>) |
| C391-0410-T21 / OLP-0399 | fuzzy | ضبابية | ضبابية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:32>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:32>) |
| C391-0410-T22 / OLP-0400 | editorial stub | بذرة | بذرة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:14>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:14>) |
| C391-0410-T23 / OLP-0401 | editorial stub | بذرة | نواة موجزة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:14>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:14>) |
| C391-0410-T24 / OLP-0401 | converse with finite premises | مجموعة المقدمات متناهية | مجموعة المقدمات متناهية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:100>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:100>) |
| C391-0410-T25 / OLP-0402 | sequent calculus | حساب التتابع | حساب التتابع | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>) |
| C391-0410-T26 / OLP-0403 | side formulas | الصيغ الجانبية | الصيغ الجانبية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/introduction.tex:33>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/introduction.tex:34>) |
| C391-0410-T27 / OLP-0404 | n-sided sequent | التتابعية ذات الجوانب | التتابعية ذات الجوانب | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:17>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:17>) |
| C391-0410-T28 / OLP-0404 | nullary connective | رابط صفري الرتبة | رابط صفري الرتبة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:30>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:30>) |
| C391-0410-T29 / OLP-0404 | theorem | مبرهنة | مبرهنة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:44>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:44>) |
| C391-0410-T30 / OLP-0405 | structural rules | القواعد البنيوية | القواعد البنيوية | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:11>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:11>) |
| C391-0410-T31 / OLP-0405 | weakening | الإضعاف | الإضعاف | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) |
| C391-0410-T32 / OLP-0405 | contraction | الانكماش | الانكماش | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) |
| C391-0410-T33 / OLP-0405 | exchange | التبادل | التبادل | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) |
| C391-0410-T34 / OLP-0406 | characteristic truth function | دالة الصدق المميزة | دالة الصدق المميزة | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:14>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:14>) |
| C391-0410-T35 / OLP-0406 | Kleene transliteration | كلايني | كلايني | [MSA](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:20>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:20>) |
| C391-0410-T36 / OLP-0407 | normal modal logics | المنطقات الجهية النظامية | المنطقات الجهية النظامية | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:8>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:8>) |
| C391-0410-T37 / OLP-0407 | metatheory | الميتانظرية | ميتانظرية | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:11>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:11>) |
| C391-0410-T38 / OLP-0408 | syntax and semantics | التركيب والدلالة | التركيب والدلالة | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>) |
| C391-0410-T39 / OLP-0409 | modal propositions | القضايا الموجهية | القضايا الموجهية | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>) |
| C391-0410-T40 / OLP-0409 | necessarily possible | من الممكن بالضرورة | من الممكن بالضرورة | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:17>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:17>) |
| C391-0410-T41 / OLP-0409 | state description | وصف الحالة | وصف الحالة | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:43>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:43>) |
| C391-0410-T42 / OLP-0409 | accessibility relation | وصول | وصول | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:57>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:54>) |
| C391-0410-T43 / OLP-0409 | alethic | منطق جهات ↵ الصدق | منطق جهات الصدق | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:70>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:67>) |
| C391-0410-T44 / OLP-0409 | epistemic agent | لعامل | عامل | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:68>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:64>) |
| C391-0410-T45 / OLP-0409 | correspondence theory | نظرية ↵ المطابقة | نظرية المطابقة | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:73>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:70>) |
| C391-0410-T46 / OLP-0409 | material conditional | الشرط المادي | الشرط المادي | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:33>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:33>) |
| C391-0410-T47 / OLP-0410 | modal operator | المؤثر الموجهي | المؤثر الموجهي | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:26>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:26>) |
| C391-0410-T48 / OLP-0410 | modal-free | خالية من الجهات | خالية من الجهات | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:104>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:104>) |
| C391-0410-T49 / OLP-0410 | inductive definition | استقرائيًا | التعريف الاستقرائي | [MSA](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:32>) · [Classical](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:32>) |

### C391-0410-T01 — sublogics

Meaning: Inclusion of consequence relations on the shared fragment, not inclusion of the truth-value sets.

Retrospective reason: Retain the compact plural because the corollary explicitly states the entailment inclusion; it must not suggest fewer truth values.

Alternative, not applied: منطقات أضعف. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does جزئية make consequence inclusion clear without being confused with a partial semantics?

English anchor: [OLP-0391, lines 71–75](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:71>).

All recorded literal occurrences in this unit:

- [msa, lines 11–11](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:11>) — منطقات جزئية
- [classical, lines 11–11](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:11>) — منطقات جزئية

### C391-0410-T02 — contrapositive

Meaning: Contraposition of the meta-level entailment implication.

Retrospective reason: The proof starts with a classical countermodel and yields a many-valued countermodel, so this names contraposition rather than reversal of the implication.

Alternative, not applied: المقابل بالنقيض. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Which established Arabic expression best distinguishes contraposition from the plain converse in this book?

English anchor: [OLP-0391, lines 79–88](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:79>).

All recorded literal occurrences in this unit:

- [msa, lines 81–81](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:81>) — المعاكس النقيض
- [classical, lines 81–81](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:81>) — المعاكس النقيض

### C391-0410-T03 — three-valued logics

Meaning: Exactly three truth values in each semantic matrix.

Retrospective reason: The heading counts values, not propositions, and the following introduction explicitly names True, Undef and False.

Alternative, not applied: منطقات ذات ثلاث قيم. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Is الثلاثية القيم the clearest concise title for this audience?

English anchor: [OLP-0392, lines 8–8](<source-snapshot/english/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>).

All recorded literal occurrences in this unit:

- [msa, lines 8–8](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>) — المنطقات الثلاثية القيم
- [classical, lines 8–8](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>) — المنطقات الثلاثية القيم

### C391-0410-T04 — designated value

Meaning: Membership in V-plus used for satisfaction/consequence, not merely having a notable numerical value.

Retrospective reason: The passage separately chooses truth functions and designated values; keeping مميزة preserves that independent parameter.

Alternative, not applied: معيّنة للقبول. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would a short first-use gloss prevent مميزة from being confused with the defining truth function?

English anchor: [OLP-0393, lines 13–18](<source-snapshot/english/content/many-valued-logic/three-valued-logics/introduction.tex:13>).

All recorded literal occurrences in this unit:

- [msa, lines 17–17](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/introduction.tex:17>) — مميزة
- [classical, lines 17–17](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/introduction.tex:17>) — مميزة

### C391-0410-T05 — future contingent

Meaning: A future proposition whose truth is not yet settled, interpreted here as possible but not necessary.

Retrospective reason: The sea-battle and Warsaw arguments supply the sense; عرضية must not be read as chance, accidental wording, or an incidental aside.

Alternative, not applied: المستقبلية الممكنة غير الضرورية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does العرضية carry the intended modal contingency for readers without specialist philosophical training?

English anchor: [OLP-0394, lines 13–19](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:13>).

All recorded literal occurrences in this unit:

- [msa, lines 19–19](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:19>) — المستقبلية العرضية
- [classical, lines 17–17](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:17>) — المستقبلية العرضية
- [classical, lines 35–35](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:35>) — المستقبلية العرضية

### C391-0410-T06 — possible but not necessary

Meaning: The source's explicitly qualified historical use of possible.

Retrospective reason: Retain the footnote's qualification; removing it would collapse the source's contingent third value into unrestricted modern possibility.

Alternative, not applied: ممكن غير واجب. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would واجب suggest an unintended deontic sense here, making ضروري preferable?

English anchor: [OLP-0394, lines 37–39](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:37>).

All recorded literal occurrences in this unit:

- [msa, lines 36–36](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:36>) — الممكن غير الضروري
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:32>) — الممكن الذي ليس بضروري

### C391-0410-T07 — undefined

Meaning: The computational truth-value interpretation associated with nontermination.

Retrospective reason: The sequential computation explanation distinguishes failure to produce a value from a determinate false value; the unvocalized Classical form remains the same term.

Alternative, not applied: غير محدد. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does غير معرّف best preserve partial computation rather than merely unsettled future truth?

English anchor: [OLP-0395, lines 13–17](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:13>).

All recorded literal occurrences in this unit:

- [msa, lines 25–25](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:25>) — غير معرّف
- [msa, lines 26–26](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:26>) — غير معرّف
- [msa, lines 31–31](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:31>) — غير معرّف
- [msa, lines 34–34](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:34>) — غير معرّف
- [msa, lines 35–35](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:35>) — غير معرّف
- [msa, lines 163–163](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:163>) — غير معرّف
- [classical, lines 15–15](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:15>) — غير معرف
- [classical, lines 25–25](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:25>) — غير معرف
- [classical, lines 29–29](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:29>) — غير معرف
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:32>) — غير معرف
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:32>) — غير معرف
- [classical, lines 161–161](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:161>) — غير معرف

### C391-0410-T08 — unknown

Meaning: An epistemic reading of U under parallel evaluation, distinct from undefined.

Retrospective reason: The parallel cases may determine a compound before both components are known; the chosen term explicitly contrasts with غير معرف.

Alternative, not applied: غير معلوم. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Which of مجهول and غير معلوم makes the contrast clearest without implying a fourth truth value?

English anchor: [OLP-0395, lines 31–40](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:31>).

All recorded literal occurrences in this unit:

- [msa, lines 35–35](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:35>) — مجهول
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:32>) — مجهول

### C391-0410-T09 — strong Kleene logic

Meaning: The specific three-valued Kleene matrix with determinate short-circuit conjunction/disjunction cases.

Retrospective reason: Strong is a technical family label tied to these tables, not a claim that every consequence is stronger than in other matrices.

Alternative, not applied: منطق كليني الشديد. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Is القوي preferable to الشديد as the stable family label?

English anchor: [OLP-0395, lines 46–87](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:46>).

All recorded literal occurrences in this unit:

- [msa, lines 37–37](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:37>) — منطق كليني القوي
- [msa, lines 41–41](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:41>) — منطق كليني القوي
- [msa, lines 149–149](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:149>) — منطق كليني القوي
- [classical, lines 35–35](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:35>) — منطق كليني القوي
- [classical, lines 39–39](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:39>) — منطق كليني القوي
- [classical, lines 147–147](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:147>) — منطق كليني القوي

### C391-0410-T10 — weak Kleene logic

Meaning: The Kleene matrix whose compound truth functions propagate U.

Retrospective reason: Weak is retained in explicit contrast with the strong tables and computational interpretations; it should not be reinterpreted as poor validity.

Alternative, not applied: منطق كليني الواهن. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would الضعيف remain the least misleading family label when the consequence relation is discussed?

English anchor: [OLP-0395, lines 90–131](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:90>).

All recorded literal occurrences in this unit:

- [msa, lines 85–85](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:85>) — منطق كليني الضعيف
- [msa, lines 145–145](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:145>) — منطق كليني الضعيف
- [msa, lines 162–162](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:162>) — منطق كليني الضعيف
- [classical, lines 83–83](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:83>) — منطق كليني الضعيف
- [classical, lines 160–160](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:160>) — منطق كليني الضعيف

### C391-0410-T11 — meaningless

Meaning: Bochvar's proposed interpretation of U, including paradoxical sentences.

Retrospective reason: This is an attributed semantic interpretation, not a claim that the displayed formula is syntactically malformed.

Alternative, not applied: غير ذي معنى. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does عديم المعنى need an explicit distinction from an ill-formed formula at first use?

English anchor: [OLP-0395, lines 164–169](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:164>).

All recorded literal occurrences in this unit:

- [msa, lines 160–160](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:160>) — عديم المعنى
- [classical, lines 158–158](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:158>) — عديم المعنى

### C391-0410-T12 — external negation

Meaning: The unary operator whose table maps U to True, unlike the original negation.

Retrospective reason: External names a specific connective/table, not a negation outside quotation marks or outside the formal language.

Alternative, not applied: النفي الخارجي المضاف. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does الخارجي communicate the contrast with the original negation without suggesting metalinguistic negation only?

English anchor: [OLP-0395, lines 167–177](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:167>).

All recorded literal occurrences in this unit:

- [msa, lines 163–163](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:163>) — النفي الخارجي
- [classical, lines 161–161](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:161>) — النفي الخارجي

### C391-0410-T13 — intuitionistic validity

Meaning: Formal intuitionistic validity and its relation to Gödel tautologies.

Retrospective reason: The existing Arabic realizes the same logic as a noun phrase in MSA and an adverbial qualification in Classical; neither means personal intuitive plausibility.

Alternative, not applied: الصحيحة في المنطق الحدسي. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would the expanded Classical phrase prevent a nontechnical reading of حدسيًا?

English anchor: [OLP-0396, lines 71–83](<source-snapshot/english/content/many-valued-logic/three-valued-logics/goedel.tex:71>).

All recorded literal occurrences in this unit:

- [msa, lines 14–14](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:14>) — المنطق الحدسي
- [msa, lines 70–70](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:70>) — المنطق الحدسي
- [msa, lines 71–71](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:71>) — المنطق الحدسي
- [classical, lines 14–14](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/goedel.tex:14>) — الصحيحة حدسيًا

### C391-0410-T14 — logic of paradox

Meaning: The named LP matrix based on strong Kleene truth functions with two designated values.

Retrospective reason: The title is retained as a proper system label, anchored by its definition rather than by the ordinary literary sense of paradox.

Alternative, not applied: منطق المفارقات. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Is singular المفارقة preferable as a stable rendering of the system name LP?

English anchor: [OLP-0397, lines 20–28](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:20>).

All recorded literal occurrences in this unit:

- [msa, lines 20–20](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:20>) — منطق المفارقة
- [classical, lines 20–20](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:20>) — منطق المفارقة

### C391-0410-T15 — logic of nonsense

Meaning: Halldén's named matrix with weak Kleene functions and an added unary operator.

Retrospective reason: This system label stays distinct from the predicate عديم المعنى used for its unary operation; the label alone is not a claim of malformed syntax.

Alternative, not applied: منطق عديم المعنى. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Is اللامعنى natural as a system title while عديم المعنى remains the predicate in its definition?

English anchor: [OLP-0397, lines 31–49](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:31>).

All recorded literal occurrences in this unit:

- [msa, lines 31–31](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:31>) — منطق اللامعنى
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:32>) — منطق اللامعنى

### C391-0410-T16 — paraconsistent

Meaning: Failure of unrestricted explosion, without saying all contradictions are accepted.

Retrospective reason: The adjacent non-entailment and explicit exceptional cases constrain the metaphor متسامح. The Classical observed form crosses a literal source newline.

Alternative, not applied: غير انفجاري. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would غير انفجاري serve as a useful explanatory gloss without erasing the broader established family term?

English anchor: [OLP-0397, lines 139–144](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:139>).

All recorded literal occurrences in this unit:

- [msa, lines 151–151](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:151>) — متسامح مع التناقض
- [classical, lines 152–153](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:152>) — متسامح مع ↵ التناقض

### C391-0410-T17 — principle of explosion

Meaning: The schema allowing arbitrary conclusions from a contradiction.

Retrospective reason: The full A,¬A entails B pattern anchors the metaphor; the source says it does not hold generally, not that every instance fails.

Alternative, not applied: مبدأ لزوم كل شيء عن التناقض. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Should the literal explanatory phrase accompany the compact metaphor at first mention?

English anchor: [OLP-0397, lines 141–144](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:141>).

All recorded literal occurrences in this unit:

- [msa, lines 152–152](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:152>) — مبدأ الانفجار
- [classical, lines 153–153](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:153>) — مبدأ الانفجار

### C391-0410-T18 — 3-valued R-Mingle

Meaning: The inherited name of the matrix specified at this exact definition.

Retrospective reason: Retaining the Latin system label preserves discoverability and avoids inventing an Arabic technical name. The correspondence of this name to external literature has not been independently checked.

Alternative, not applied: منطق المزج R الثلاثي القيم. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does the matrix supplied here match the intended R-Mingle convention, and should the Latin label be retained?

English anchor: [OLP-0397, lines 162–170](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:162>).

All recorded literal occurrences in this unit:

- [msa, lines 171–171](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:171>) — منطق R-Mingle الثلاثي القيم
- [classical, lines 173–173](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:173>) — منطق R-Mingle الثلاثي القيم

### C391-0410-T19 — infinite-valued logics

Meaning: Infinitely many available truth values, not individual truth values of infinite magnitude.

Retrospective reason: The next section bounds the values between 0 and 1; the title refers to cardinality.

Alternative, not applied: منطقات ذات قيم صدق لا متناهية العدد. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would the longer title prevent confusion between infinitely many values and infinite numerical values?

English anchor: [OLP-0398, lines 8–8](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>).

All recorded literal occurrences in this unit:

- [msa, lines 8–8](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>) — المنطقات اللانهائية القيم
- [classical, lines 8–8](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>) — المنطقات اللانهائية القيم

### C391-0410-T20 — rational numbers

Meaning: Rationals in [0,1], distinct from the subsequent real-valued alternative.

Retrospective reason: The explicit intersection with Rat fixes the mathematical sense; نسبية does not refer to relativity of truth.

Alternative, not applied: الأعداد الكسرية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would الكسرية risk conflating rational numbers with a chosen fractional notation?

English anchor: [OLP-0399, lines 13–16](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>).

All recorded literal occurrences in this unit:

- [msa, lines 14–14](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:14>) — الأعداد النسبية
- [classical, lines 14–14](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:14>) — الأعداد النسبية

### C391-0410-T21 — fuzzy

Meaning: The source's name for the family with real or other infinite subsets of [0,1] as truth values.

Retrospective reason: The term labels semantics with intermediate truth values; it should not mean informal imprecision or an unverified argument.

Alternative, not applied: تمويهية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Is ضبابية the best established reader-facing term for this family?

English anchor: [OLP-0399, lines 30–32](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:30>).

All recorded literal occurrences in this unit:

- [msa, lines 32–32](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:32>) — ضبابية
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:32>) — ضبابية

### C391-0410-T22 — editorial stub

Meaning: An editorial notice that this source section is only a short beginning.

Retrospective reason: Keeping the explicit metaphor preserves the source's incompleteness warning and avoids pretending a completed comprehensive section.

Alternative, not applied: نواة موجزة. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would نواة موجزة be more natural, as in the next section, while preserving the warning?

English anchor: [OLP-0400, lines 14–15](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:14>).

All recorded literal occurrences in this unit:

- [msa, lines 14–14](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:14>) — بذرة
- [classical, lines 14–14](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:14>) — بذرة

### C391-0410-T23 — editorial stub

Meaning: The same editorial incompleteness notice in the Gödel section.

Retrospective reason: The Classical noun phrase is an idiomatic recasting of the source's stub, not a new claim about axiomatic cores.

Alternative, not applied: قسم تمهيدي غير مستوفى. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does نواة need a qualifier to prevent confusion with a technical logical kernel?

English anchor: [OLP-0401, lines 14–14](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/goedel.tex:14>).

All recorded literal occurrences in this unit:

- [msa, lines 14–14](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:14>) — بذرة
- [classical, lines 14–14](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:14>) — نواة موجزة

### C391-0410-T24 — converse with finite premises

Meaning: The corrected Arabic qualification of the finite/infinite consequence converse.

Retrospective reason: The finite-premise wording already present is retained as a semantic scope repair, not alleged to have been literally stated in the frozen English sentence.

Alternative, not applied: إذا كانت المقدمات معدودة. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does متناهية clearly avoid the weaker and inadequate condition معدودة?

English anchor: [OLP-0401, lines 87–99](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/goedel.tex:87>).

All recorded literal occurrences in this unit:

- [msa, lines 100–100](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:100>) — مجموعة المقدمات متناهية
- [classical, lines 100–100](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:100>) — مجموعة المقدمات متناهية

### C391-0410-T25 — sequent calculus

Meaning: A proof calculus on sequents, not a calculus of ordinary numeric sequences.

Retrospective reason: The heading is linked to the following multiset/sequence-slot definitions and inference rules; the morphology differs legitimately from التتابعية in running prose.

Alternative, not applied: حساب التتابعيات. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would the plural title better distinguish sequents from sequential order?

English anchor: [OLP-0402, lines 8–8](<source-snapshot/english/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>).

All recorded literal occurrences in this unit:

- [msa, lines 8–8](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>) — حساب التتابع
- [classical, lines 8–8](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>) — حساب التتابع

### C391-0410-T26 — side formulas

Meaning: Unchanged context formulas omitted when displaying the principal connective rule.

Retrospective reason: Side means structural context, not logically optional premises that may be discarded.

Alternative, not applied: صيغ السياق. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would صيغ السياق help explain why these formulas return in full proof trees?

English anchor: [OLP-0403, lines 27–48](<source-snapshot/english/content/many-valued-logic/sequent-calculus/introduction.tex:27>).

All recorded literal occurrences in this unit:

- [msa, lines 33–33](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/introduction.tex:33>) — الصيغ الجانبية
- [classical, lines 34–34](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/introduction.tex:34>) — الصيغ الجانبية

### C391-0410-T27 — n-sided sequent

Meaning: An ordered n-slot expression with one finite possibly empty sequence in each truth-value position.

Retrospective reason: The term describes syntactic slots, not n premises of an inference; the displayed Γ1|...|Γn fixes their order.

Alternative, not applied: تتابعية ذات مواضع. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would مواضع be clearer than جوانب when n exceeds two?

English anchor: [OLP-0404, lines 17–23](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:17>).

All recorded literal occurrences in this unit:

- [msa, lines 17–17](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:17>) — التتابعية ذات الجوانب
- [classical, lines 17–17](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:17>) — التتابعية ذات الجوانب

### C391-0410-T28 — nullary connective

Meaning: A zero-argument propositional constant with an assigned truth value.

Retrospective reason: The explanatory constant clause makes the arity meaning precise and distinguishes rank from proof-theoretic complexity.

Alternative, not applied: رابط بلا وسائط. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would بلا وسائط be a clearer first-use gloss for صفري الرتبة?

English anchor: [OLP-0404, lines 30–33](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:30>).

All recorded literal occurrences in this unit:

- [msa, lines 30–30](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:30>) — رابط صفري الرتبة
- [classical, lines 30–30](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:30>) — رابط صفري الرتبة

### C391-0410-T29 — theorem

Meaning: A sentence derivable without premises via the designated-slot sequent.

Retrospective reason: Retain the proof-theoretic noun and avoid replacing it with a semantic tautology; the separate empty-slot issue is recorded as F04.

Alternative, not applied: قضية مبرهنة. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does the definition adequately distinguish theorem from semantic validity once the empty slots are explicit?

English anchor: [OLP-0404, lines 45–61](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:45>).

All recorded literal occurrences in this unit:

- [msa, lines 44–44](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:44>) — مبرهنة
- [msa, lines 47–47](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:47>) — مبرهنة
- [classical, lines 44–44](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:44>) — مبرهنة
- [classical, lines 47–47](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:47>) — مبرهنة

### C391-0410-T30 — structural rules

Meaning: Rules changing contexts rather than introducing a principal logical connective.

Retrospective reason: The rules add, merge or reorder occurrences and operate independently in truth-value slots.

Alternative, not applied: القواعد الهيكلية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Which label best contrasts with the following propositional rules for this audience?

English anchor: [OLP-0405, lines 11–35](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:11>).

All recorded literal occurrences in this unit:

- [msa, lines 11–11](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:11>) — القواعد البنيوية
- [msa, lines 13–13](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:13>) — القواعد البنيوية
- [classical, lines 11–11](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:11>) — القواعد البنيوية
- [classical, lines 13–13](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:13>) — القواعد البنيوية

### C391-0410-T31 — weakening

Meaning: Adding a formula occurrence in one sequent position.

Retrospective reason: The operation weakens the sequent's satisfaction requirement; it is not a less rigorous inference.

Alternative, not applied: التوسيع. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would an explanatory note about adding context resolve the apparent paradox in the name الإضعاف?

English anchor: [OLP-0405, lines 18–21](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:18>).

All recorded literal occurrences in this unit:

- [msa, lines 37–37](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) — الإضعاف
- [classical, lines 37–37](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) — الإضعاف

### C391-0410-T32 — contraction

Meaning: Merging two identical adjacent formula occurrences in one position.

Retrospective reason: The displayed rule fixes the sense as duplicate removal, not abbreviation of a formula or a semantic collapse.

Alternative, not applied: التقليص. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Which term better distinguishes contraction from formula simplification?

English anchor: [OLP-0405, lines 23–27](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:23>).

All recorded literal occurrences in this unit:

- [msa, lines 37–37](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) — الانكماش
- [classical, lines 37–37](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) — الانكماش

### C391-0410-T33 — exchange

Meaning: Permuting neighboring formula occurrences in a sequent position.

Retrospective reason: This is a context permutation, not substituting one formula for another or exchanging premise and conclusion.

Alternative, not applied: التبديل. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Is التبادل sufficiently distinct from substitution in the wider reader?

English anchor: [OLP-0405, lines 29–33](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:29>).

All recorded literal occurrences in this unit:

- [msa, lines 37–37](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) — التبادل
- [classical, lines 37–37](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:37>) — التبادل

### C391-0410-T34 — characteristic truth function

Meaning: The function defining a connective's output values, not membership in V-plus.

Retrospective reason: The surrounding explanation says identical truth functions yield identical rules; the shared adjective مميزة may otherwise be confused with designated values.

Alternative, not applied: دالة الصدق المعرِّفة. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would المعرِّفة or الموصِّفة reduce confusion with قيم مميزة without imposing a new unsupported canonical term?

English anchor: [OLP-0406, lines 13–17](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:13>).

All recorded literal occurrences in this unit:

- [msa, lines 14–14](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:14>) — دالة الصدق المميزة
- [classical, lines 14–14](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:14>) — دالة الصدق المميزة

### C391-0410-T35 — Kleene transliteration

Meaning: The same person/system called كليني in unit 0395.

Retrospective reason: Both are observed Arabic spellings; a later consistency pass can prefer the chapter's كليني while leaving formal labels untouched. No official transliteration is claimed.

Alternative, not applied: كليني. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Should the reader use the earlier chapter's spelling كليني consistently?

English anchor: [OLP-0406, lines 21–22](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:21>).

All recorded literal occurrences in this unit:

- [msa, lines 20–20](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:20>) — كلايني
- [msa, lines 62–62](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:62>) — كلايني
- [msa, lines 89–89](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:89>) — كلايني
- [msa, lines 140–140](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:140>) — كلايني
- [classical, lines 20–20](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:20>) — كلايني
- [classical, lines 62–62](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:62>) — كلايني
- [classical, lines 89–89](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:89>) — كلايني
- [classical, lines 140–140](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:140>) — كلايني

### C391-0410-T36 — normal modal logics

Meaning: The technical family named by the source, not merely ordinary or familiar modal reasoning.

Retrospective reason: The literal printed heading is recorded separately from the different singular spelling in the source comment. نظامية should remain linked to the formal family rather than an everyday normality claim.

Alternative, not applied: المنطقات الموجهية النظامية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Which of الجهية and الموجهية should be the reader-facing family term, and does النظامية convey the technical normality?

English anchor: [OLP-0407, lines 7–12](<source-snapshot/english/content/normal-modal-logic/normal-modal-logic.tex:7>).

All recorded literal occurrences in this unit:

- [msa, lines 8–8](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:8>) — المنطقات الجهية النظامية
- [msa, lines 11–11](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:11>) — المنطقات الجهية النظامية
- [classical, lines 8–8](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:8>) — المنطقات الجهية النظامية
- [classical, lines 11–11](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:11>) — المنطقات الجهية النظامية

### C391-0410-T37 — metatheory

Meaning: Theory about the formal modal systems themselves.

Retrospective reason: The distinction between object language and mathematical study of it must remain; Classical simply drops the definite article in a nominal construction.

Alternative, not applied: ما وراء النظرية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does ميتانظرية remain clearer than an Arabic phrase that might sound metaphysical?

English anchor: [OLP-0407, lines 10–12](<source-snapshot/english/content/normal-modal-logic/normal-modal-logic.tex:10>).

All recorded literal occurrences in this unit:

- [msa, lines 11–11](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:11>) — الميتانظرية
- [classical, lines 11–11](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:11>) — ميتانظرية

### C391-0410-T38 — syntax and semantics

Meaning: Formation rules contrasted with interpretation and truth.

Retrospective reason: The paired title correctly separates well-formed expressions from their semantic evaluation; it is not a claim that syntax is a single formula composition.

Alternative, not applied: البنية الصورية والدلالة. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would the established compact pairing be clearer than the longer alternative?

English anchor: [OLP-0408, lines 8–8](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>).

All recorded literal occurrences in this unit:

- [msa, lines 8–8](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>) — التركيب والدلالة
- [classical, lines 8–8](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>) — التركيب والدلالة

### C391-0410-T39 — modal propositions

Meaning: Propositions involving modalities, including but not limited to possibility and necessity.

Retrospective reason: The subsequent deontic, temporal and epistemic examples prevent a restriction to alethic modality only.

Alternative, not applied: القضايا الجهية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Should this match the الجهية form in the part title or retain الموجهية consistently in prose?

English anchor: [OLP-0409, lines 13–25](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>).

All recorded literal occurrences in this unit:

- [msa, lines 13–13](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>) — القضايا الموجهية
- [classical, lines 13–13](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>) — القضايا الموجهية

### C391-0410-T40 — necessarily possible

Meaning: Necessity taking scope over possibility in the opening examples.

Retrospective reason: This literal in-use phrase is being flagged, not endorsed as unambiguous: the later reversed English nesting receives the same Arabic words. See F05.

Alternative, not applied: من الضروري أن يكون من الممكن. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Do explicit nested clauses best preserve the operator scope and natural Arabic flow?

English anchor: [OLP-0409, lines 18–20](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:18>).

All recorded literal occurrences in this unit:

- [msa, lines 17–17](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:17>) — من الممكن بالضرورة
- [msa, lines 18–18](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:18>) — من الممكن بالضرورة
- [msa, lines 48–48](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:48>) — من الممكن بالضرورة
- [classical, lines 17–17](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:17>) — من الممكن بالضرورة
- [classical, lines 18–18](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:18>) — من الممكن بالضرورة
- [classical, lines 47–47](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:47>) — من الممكن بالضرورة

### C391-0410-T41 — state description

Meaning: Carnap's specified collection of atomic sentences used to define truth.

Retrospective reason: The word وصف refers to a technical semantic object, not merely a prose account of circumstances.

Alternative, not applied: وصف لحالة. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does the definite compound adequately signal the technical object at first mention?

English anchor: [OLP-0409, lines 46–57](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:46>).

All recorded literal occurrences in this unit:

- [msa, lines 43–43](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:43>) — وصف الحالة
- [msa, lines 44–44](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:44>) — وصف الحالة
- [classical, lines 43–43](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:43>) — وصف الحالة

### C391-0410-T42 — accessibility relation

Meaning: The binary relation selecting the worlds quantified over by a necessity statement.

Retrospective reason: The following directed from-clause preserves orientation; arrival or physical reachability should not be inferred.

Alternative, not applied: إمكان الوصول. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would علاقة إمكان الوصول be a clearer full technical term than علاقة وصول?

English anchor: [OLP-0409, lines 65–71](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:65>).

All recorded literal occurrences in this unit:

- [msa, lines 57–57](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:57>) — وصول
- [msa, lines 59–59](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:59>) — وصول
- [msa, lines 75–75](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:75>) — وصول
- [classical, lines 54–54](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:54>) — وصول
- [classical, lines 56–56](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:56>) — وصول
- [classical, lines 71–71](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:71>) — وصول

### C391-0410-T43 — alethic

Meaning: Truth-related modalities contrasted with epistemic and dynamic modalities.

Retrospective reason: The gloss avoids opaque transliteration and distinguishes this family from epistemic and dynamic modalities. The exact MSA phrase crosses a literal newline, preserved in the observed-form field.

Alternative, not applied: المنطق الأليثي. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does جهات الصدق convey the family without confusion with truth values?

English anchor: [OLP-0409, lines 73–83](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:73>).

All recorded literal occurrences in this unit:

- [msa, lines 70–71](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:70>) — منطق جهات ↵ الصدق
- [classical, lines 67–67](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:67>) — منطق جهات الصدق

### C391-0410-T44 — epistemic agent

Meaning: The bearer of knowledge or an epistemic state, not a numerical factor.

Retrospective reason: The context supplies the epistemic sense, but عامل has a common mathematical factor reading worth avoiding when the reader moves between algebra and epistemology.

Alternative, not applied: فاعل معرفي. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would فاعل معرفي be more natural and less ambiguous than عامل in this context?

English anchor: [OLP-0409, lines 78–83](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:78>).

All recorded literal occurrences in this unit:

- [msa, lines 68–68](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:68>) — لعامل
- [classical, lines 64–64](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:64>) — عامل

### C391-0410-T45 — correspondence theory

Meaning: The correspondence between relational frame properties and modal schemas.

Retrospective reason: The MSA compound crosses a literal newline while the Classical compound is contiguous. Both name characterization of frame properties by modal schemas, not literal identity between a relation and a formula.

Alternative, not applied: نظرية التقابل. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would المطابقة be confused with identity of formulas rather than characterization of frame properties?

English anchor: [OLP-0409, lines 85–95](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:85>).

All recorded literal occurrences in this unit:

- [msa, lines 73–74](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:73>) — نظرية ↵ المطابقة
- [classical, lines 70–70](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:70>) — نظرية المطابقة

### C391-0410-T46 — material conditional

Meaning: The truth-functional conditional contrasted with strict implication.

Retrospective reason: Preserving المادي distinguishes the connective from the necessary conditional; it is not a physical-material claim.

Alternative, not applied: الاستلزام المادي. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Does الشرط better avoid conflating object-language connective and consequence relation?

English anchor: [OLP-0409, lines 35–44](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:35>).

All recorded literal occurrences in this unit:

- [msa, lines 33–33](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:33>) — الشرط المادي
- [classical, lines 33–33](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:33>) — الشرط المادي

### C391-0410-T47 — modal operator

Meaning: The unary Box or Diamond symbol in the alphabet and formation clauses.

Retrospective reason: The term marks an operation on formulas, not a quantifier over the object language's individual variables.

Alternative, not applied: الرابط الجهي. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Should operator المؤثر be kept distinct from connective الرابط in the surrounding exposition?

English anchor: [OLP-0410, lines 26–27](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:26>).

All recorded literal occurrences in this unit:

- [msa, lines 26–26](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:26>) — المؤثر الموجهي
- [msa, lines 27–27](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:27>) — المؤثر الموجهي
- [classical, lines 26–26](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:26>) — المؤثر الموجهي
- [classical, lines 27–27](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:27>) — المؤثر الموجهي

### C391-0410-T48 — modal-free

Meaning: A formula containing neither Box nor Diamond.

Retrospective reason: The definition is syntactic absence of modal operators, not semantic impossibility or absence of directional meaning.

Alternative, not applied: خالية من المؤثرات الموجهية. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would the longer phrase reduce ambiguity while keeping the exact no-Box/no-Diamond condition?

English anchor: [OLP-0410, lines 104–105](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:104>).

All recorded literal occurrences in this unit:

- [msa, lines 104–104](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:104>) — خالية من الجهات
- [classical, lines 104–104](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:104>) — خالية من الجهات

### C391-0410-T49 — inductive definition

Meaning: Recursive generation from atomic formulas with explicit closure and limit clauses.

Retrospective reason: The term describes structural induction/formation, not empirical generalization from examples; Classical explicitly starts with atoms then composition.

Alternative, not applied: تعريف توليدي. Candidate for the stated expert question; not asserted to be dictionary-attested.

Please double-check: Would a first-use gloss distinguish this exact formation rule from empirical induction?

English anchor: [OLP-0410, lines 32–64](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:32>).

All recorded literal occurrences in this unit:

- [msa, lines 32–32](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:32>) — استقرائيًا
- [classical, lines 32–32](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:32>) — التعريف الاستقرائي

## Unit coverage and no-change evidence

Structural-only units are not counted as rephrased exposition. Each full three-source identity is in the companion JSON. No PDF page has been estimated.

### OLP-0391 — prose

All four classical restrictions are retained; the induction covers atom, negation, conjunction and the two analogous binary cases. The corrected Arabic statement restricts the claim and consequence corollary to the constant-free four-connective fragment and correctly uses satisfaction, not entailment, for a valuation.

Classical discourse: The opening identifies the common property and then details it; the proof proceeds by explicit cases and a contrapositive. This is substantive discourse reconstruction, not a synonym swap.

Already corrected / false-positive control: Already shared in both Arabic files: fragment scope, quantification over variables occurring in the formula, and the satisfaction notation. Do not report these corrected defects as new.

Full source reads:

- [english: lines 1–90](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:1>), 4122 bytes, SHA-256 `e831e5ce1375c0ea5b2743d8c8c45cf0d8299dde538cdf46284e34a968c665a1`.
- [msa: lines 1–94](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:1>), 5021 bytes, SHA-256 `ffb57f53c53d724941dc160091698d6ecb590da0f79c54eae197f3cbc773c3f5`.
- [classical: lines 1–94](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:1>), 5057 bytes, SHA-256 `1d75fd563f024a2136bfaab049978a7f950234b1bd7f8b153b30274015749f72`.

Representative exact-evidence ranges: [english 23–38](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:23>); [msa 35–39](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:35>); [classical 35–39](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:35>); [english 78–90](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:78>); [msa 80–94](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/syntax-and-semantics/sublogics.tex:80>); [classical 80–94](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/sublogics.tex:80>).

### OLP-0392 — structural

Five import targets, their order, the chapter identity and end hook are unchanged.

Classical discourse: Title-only driver; no continuous prose exists to rephrase. Structural review is not counted as translated exposition.

Already corrected / false-positive control: Only harmless trailing blank-line differences.

Full source reads:

- [english: lines 1–22](<source-snapshot/english/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:1>), 358 bytes, SHA-256 `8015ad7f225f913aa068bd9e9cba20b78b35e0b3844c60fe8a3989f6c2d9ac74`.
- [msa: lines 1–23](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:1>), 362 bytes, SHA-256 `ef09f12ae810a0fca04443e507fa8e40f01f44fbcaf83935ec086f89c84e4f18`.
- [classical: lines 1–24](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:1>), 363 bytes, SHA-256 `95f47a6db0a848ee29fcc0c9d5fe513b5df0f4b4dcdca2b6dcbd59b1d0a6181a`.

Representative exact-evidence ranges: [english 8–20](<source-snapshot/english/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>); [msa 8–20](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>); [classical 8–20](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>).

### OLP-0393 — prose

Adding U, the freedom in truth-function selection, both designated-value choices and the promised selective survey all remain.

Classical discourse: The contrast between one extra value and many possible truth functions is rebuilt as a condition/concession. 'كثيرة جدًا' makes clear that the sentence is about many choices, not infinitely many functions on a finite set.

Already corrected / false-positive control: No new semantic correction identified.

Full source reads:

- [english: lines 1–23](<source-snapshot/english/content/many-valued-logic/three-valued-logics/introduction.tex:1>), 786 bytes, SHA-256 `3c037aaf7bcd3d7986c15ccff60ecf1763afabbaf0e2be4c5a8961de46382eef`.
- [msa: lines 1–23](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/introduction.tex:1>), 924 bytes, SHA-256 `b2a2f24834e71ddc55a8799f6931b98454655c28a5a27bf64793944f672ad93b`.
- [classical: lines 1–22](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/introduction.tex:1>), 916 bytes, SHA-256 `f3c48515a61e48ff17b53e9d47e8837358af8938f9d2b21d1df127016addb209`.

Representative exact-evidence ranges: [english 13–21](<source-snapshot/english/content/many-valued-logic/three-valued-logics/introduction.tex:13>); [msa 13–21](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/introduction.tex:13>); [classical 13–20](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/introduction.tex:13>).

### OLP-0394 — prose

Sea-battle motivation, Warsaw noon/date example, possible-but-not-necessary footnote, four tables, conditional motivation, matrix tuple, every exercise, modal tables and final objection are present. One final evaluated value is wrong in all three files, though the non-tautology conclusion remains true.

Classical discourse: The argument is genuinely reconstructed through the determinate/indeterminate cases, with explicit reasons for each conditional entry. The extended quoted passage keeps its hypothetical force and attribution; no independent verification of historical claims is implied.

Already corrected / false-positive control: Both Arabic sources already have the constant-free language, the False/U conjunction symmetry, the corrected matrix tuple and exercise parenthesis. Preserve these.

Full source reads:

- [english: lines 1–242](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:1>), 10307 bytes, SHA-256 `f4f46fab1263ab5437fc91964cf3e61a658ca18f5739c520a43f4e45f669f2ab`.
- [msa: lines 1–236](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:1>), 12238 bytes, SHA-256 `53eb87b345723bd978d1d82ed1f9caa19ad8857c7198e01da0e213afadd9c989`.
- [classical: lines 1–227](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:1>), 11339 bytes, SHA-256 `5eeb1f6b952f6d8dee4cfe789ddec9adf2e661c1049de80db6a389314e50f8eb`.

Representative exact-evidence ranges: [english 13–39](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:13>); [msa 13–36](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:13>); [classical 13–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:13>); [english 231–240](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:231>); [msa 227–234](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:227>); [classical 219–225](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:219>).

### OLP-0395 — prose

Sequential and parallel computation remain distinct; strong/weak truth tables, absence-of-tautologies proof, nontrivial consequence exercise, Bochvar operators and definability question are preserved. No-tautology result is legitimate for the explicitly constant-free language.

Classical discourse: The Classical version explains how stopping one parallel computation suffices and then distinguishes unknown from undefined. This preserves the epistemic/computational distinction rather than using U as a single vague term.

Already corrected / false-positive control: Both Arabic files already restrict the primitive fragment; the Classical grammatical repair of أحد جزأيها is present. The final exercise asks whether an operator is definable; it does not assert that it is.

Full source reads:

- [english: lines 1–197](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:1>), 7075 bytes, SHA-256 `5630d9cb5c6a43dde8e85791827e95326ea0258b9be9aecbef3e89ee098cb376`.
- [msa: lines 1–190](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:1>), 8182 bytes, SHA-256 `35eb5b9c777d76b66e9126bc50b1344c2fd81ca1143ec6ee46d987811fa7a746`.
- [classical: lines 1–188](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:1>), 7775 bytes, SHA-256 `f5142a63b9a3624b54ceb675031f555f01230fdca054003e90e80f6a99d76071`.

Representative exact-evidence ranges: [english 13–43](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:13>); [msa 13–38](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:13>); [classical 13–36](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:13>); [english 133–169](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:133>); [msa 129–163](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/kleene.tex:129>); [classical 127–161](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/kleene.tex:127>).

### OLP-0396 — prose

The Gödel truth tables retain false negation at U and the conditional's distinctive U/False and U/U cases. Intuitionistic containment, nonclassical counterexamples and all exercises are preserved.

Classical discourse: The exposition separates the shared conjunction/disjunction tables from the contrasting negation/conditional tables and then explains the relation to intuitionistic logic.

Already corrected / false-positive control: The constant has an explicit False interpretation in both current Arabic sources; no missing interpretation is alleged.

Full source reads:

- [english: lines 1–118](<source-snapshot/english/content/many-valued-logic/three-valued-logics/goedel.tex:1>), 4223 bytes, SHA-256 `de6e29f7cf74c9ee8288354943e960df3ccb3f50ebaa2921442b20c9adac13bf`.
- [msa: lines 1–115](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:1>), 4620 bytes, SHA-256 `57fffe02fed67171bd5b85f5e7cd4d596cdf9f3f1187a5799b48f1af48da7bae`.
- [classical: lines 1–113](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/goedel.tex:1>), 4511 bytes, SHA-256 `7d27d1c96abfdd364641a77e3437e37aedf97e2a6ae56b5e1c11e7398a54d178`.

Representative exact-evidence ranges: [english 13–25](<source-snapshot/english/content/many-valued-logic/three-valued-logics/goedel.tex:13>); [msa 13–25](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:13>); [classical 13–25](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/goedel.tex:13>); [english 71–118](<source-snapshot/english/content/many-valued-logic/three-valued-logics/goedel.tex:71>); [msa 70–115](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/goedel.tex:70>); [classical 70–113](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/goedel.tex:70>).

### OLP-0397 — prose

LP/Hal/R-Mingle designated sets and truth functions remain as stated in English; the two-part refinement induction and every exercise are retained. Failure of explosion is stated as non-universal, with the tautological-conclusion exception retained.

Classical discourse: The Classical discourse contrasts truth functions with designated values, then separates tautologies from consequence. Its transition to paraconsistency is explanatory and does not say every contradiction is true.

Already corrected / false-positive control: Both Arabic sources already repair the U base case and repeated B/C conjunction variable in the refinement proof. The R-Mingle label is retained as an unverified source name, not independently certified as a standard matrix.

Full source reads:

- [english: lines 1–209](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:1>), 8529 bytes, SHA-256 `105d956c622e310bf3039faa57d0fb5604531a143cc8c7bcf3c48d26ee038a09`.
- [msa: lines 1–219](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:1>), 10406 bytes, SHA-256 `e23ef2a7ec9cb5c57b0bbcc6e6ff6bcaf44dae5afc7b927e7f2347b4205ac7a1`.
- [classical: lines 1–222](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:1>), 10261 bytes, SHA-256 `9c7cbf005239e866307fbc094e7a088322ab7b6d166d29cc67112b16714ee8c2`.

Representative exact-evidence ranges: [english 54–88](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:54>); [msa 54–95](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:54>); [classical 56–97](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:56>); [english 139–145](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:139>); [msa 149–154](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/three-valued-logics/multiple-designation.tex:149>); [classical 151–155](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/multiple-designation.tex:151>).

### OLP-0398 — structural

Three import targets, order, chapter identity and end hook are preserved.

Classical discourse: Title-only chapter driver; structural, not prose translation.

Already corrected / false-positive control: Both Arabic comments correctly identify the infinite-valued chapter; English's comment says three-valued.

Full source reads:

- [english: lines 1–18](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:1>), 305 bytes, SHA-256 `fb04e81a62757c4d33472613879b832aaab480e9be4f9e8b7396299017352921`.
- [msa: lines 1–19](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:1>), 317 bytes, SHA-256 `95c35f13689412619d8b96d42627a986d267ffb674530dd829022fd9d408deab`.
- [classical: lines 1–20](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:1>), 318 bytes, SHA-256 `572791d7861f6cf11309214e428ddfe73d4f034ef0c4fddd0f0d2db392810b35`.

Representative exact-evidence ranges: [english 8–16](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>); [msa 8–16](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>); [classical 8–16](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>).

### OLP-0399 — prose

Rational V-infinity, finite uniform grids, designated 1, intermediate values and the separate real-valued alternative all remain. V_m still requires m≥2.

Classical discourse: The Classical opening first denies finiteness as a requirement, identifies the rational example, then contrasts it with real-valued alternatives. No natural-number zero convention was changed.

Already corrected / false-positive control: Both Arabic texts already have m>0 for V-infinity and n<m for V_m. Those repairs are real; only the remaining finite-grid denominator condition is newly flagged.

Full source reads:

- [english: lines 1–35](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:1>), 1338 bytes, SHA-256 `affd39b02580135e472d159f31cbe2a5805f344a9eab515a4bce7fd18999889e`.
- [msa: lines 1–36](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:1>), 1771 bytes, SHA-256 `e44d252e238bcad4d6532088ecff7ba7f9f0a3c09990d6ec77f8b7928ecf9dd7`.
- [classical: lines 1–36](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:1>), 1767 bytes, SHA-256 `0f5370d39be3c71fc1fb071977324bbefa1ce7f8d082bd5dfb480612ba2312fb`.

Representative exact-evidence ranges: [english 13–32](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>); [msa 13–32](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>); [classical 13–32](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>).

### OLP-0400 — prose

The complement/min/max/Łukasiewicz implication operations and the numeric three-valued comparison tables are preserved. The forward implication from infinite to each finite matrix is correct; the unqualified converse is not correct for arbitrary infinite premises.

Classical discourse: The editorial stub warning remains explicit. The Classical wording moves from the matrix to finite variants, then the consequence result and fuzzy-logic usage without manufacturing a longer completed theory.

Already corrected / false-positive control: The constant-free repair is already shared. The missing m≥2 family restriction is tracked once at 0399, not counted as a duplicate defect here.

Full source reads:

- [english: lines 1–108](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:1>), 3129 bytes, SHA-256 `3b6867d8660841a2e8ce81b27726e0848efb71629edd19aa77fd8cbc638ed543`.
- [msa: lines 1–108](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:1>), 3538 bytes, SHA-256 `ff15f7a1eaeee1da4124ac5292c4fc8754a8a541f7cee1efae71e16a9362e084`.
- [classical: lines 1–108](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:1>), 3552 bytes, SHA-256 `8cf51285f0f69c513fbbf95d4055e8a27f624de782588d2cb77a9598840a1ba2`.

Representative exact-evidence ranges: [english 13–37](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:13>); [msa 13–37](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:13>); [classical 13–37](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:13>); [english 83–106](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:83>); [msa 84–106](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>); [classical 84–106](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:84>).

### OLP-0401 — prose

Gödel's numeric operations and all comparison tables, intuitionistic inclusions, linearity schema and the final finite/infinite exercise remain. Unlike 0400, both Arabic files already explicitly restrict the converse to finite premises.

Classical discourse: The Classical text honestly calls the section a nucleus and organizes the comparison with intuitionistic logic as previously established facts, examples and an alternative characterization.

Already corrected / false-positive control: Both Arabic sources already remove erroneous nested math delimiters in the cases table and restrict the converse to finite premises. This provides a nearby wording model for 0400.

Full source reads:

- [english: lines 1–127](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/goedel.tex:1>), 3992 bytes, SHA-256 `e763954137e0c3ed9e2ce32d0ed248bd50e922f7f147fc0506e482878932314b`.
- [msa: lines 1–127](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:1>), 4447 bytes, SHA-256 `0529de2c1be492d463ca9af45feb88be41afee1dc8b588ea98f330640f1ca06c`.
- [classical: lines 1–128](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:1>), 4632 bytes, SHA-256 `86daad125ae0dbfb36b06be473b6432cd4e551c069d006a873c664f398037561`.

Representative exact-evidence ranges: [english 83–114](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/goedel.tex:83>); [msa 84–115](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/infinite-valued-logics/goedel.tex:84>); [classical 86–116](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/infinite-valued-logics/goedel.tex:86>).

### OLP-0402 — structural

Four import targets and end hook are preserved.

Classical discourse: Identical Arabic title-only driver; no claim of newly rephrased continuous prose.

Already corrected / false-positive control: Arabic comments fix the inherited incorrect chapter comment.

Full source reads:

- [english: lines 1–20](<source-snapshot/english/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:1>), 348 bytes, SHA-256 `def8a764c8cb783a86a6704d96ae02529921a0bb30d118b4fe4cff4ac667cf19`.
- [msa: lines 1–20](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:1>), 332 bytes, SHA-256 `6f15e0cb1f59cdf496259462c6288685ee4e47214d1d5c03b438e6fead62a7a5`.
- [classical: lines 1–20](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:1>), 332 bytes, SHA-256 `6f15e0cb1f59cdf496259462c6288685ee4e47214d1d5c03b438e6fead62a7a5`.

Representative exact-evidence ranges: [english 8–18](<source-snapshot/english/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>); [msa 8–18](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>); [classical 8–18](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>).

### OLP-0403 — prose

Classical two-sided sequent semantics, falsity/truth alternatives, iff directions, side-formula omission, n-sided generalization and A|A|A initial sequent all remain.

Classical discourse: The Classical version explains the route from the familiar classical case to the finite many-valued case, with explicit 'متى وفقط متى' and separate alternatives.

Already corrected / false-positive control: Both Arabic files already repair the m/n antecedent length and missing valuation argument; do not reopen these.

Full source reads:

- [english: lines 1–83](<source-snapshot/english/content/many-valued-logic/sequent-calculus/introduction.tex:1>), 3193 bytes, SHA-256 `4077eee65fb505ab3b97ebfc37616593b555252fafbbbebe0413981e0988bbe3`.
- [msa: lines 1–80](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/introduction.tex:1>), 3723 bytes, SHA-256 `eba024907eca2e264b472d8b9ae0ba4f486ed8481d9cb2a27b51523b906be7f7`.
- [classical: lines 1–80](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/introduction.tex:1>), 3749 bytes, SHA-256 `eb53c6420a615e60ddb41c8504156a57749e6b34c24f257cbfe0c195ce4f1f0d`.

Representative exact-evidence ranges: [english 13–38](<source-snapshot/english/content/many-valued-logic/sequent-calculus/introduction.tex:13>); [msa 13–36](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/introduction.tex:13>); [classical 13–37](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/introduction.tex:13>); [english 61–83](<source-snapshot/english/content/many-valued-logic/sequent-calculus/introduction.tex:61>); [msa 58–80](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/introduction.tex:58>); [classical 58–80](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/introduction.tex:58>).

### OLP-0404 — prose

Finite possibly empty sequences, general n-slot sequents, constant initial sequents, derivation trees, finite-premise derivability and the three-value example remain. The theorem definition leaves undesignated slots implicit, an ambiguity worth tightening.

Classical discourse: The Classical version makes the empty-sequence convention and the derivation-tree condition explicit before the definitions, then works through the three-value example.

Already corrected / false-positive control: The general Γ_i repair, nullary-constant empty-slot condition and indexed nonderivability notation are already shared. The separate theorem-slot ambiguity is not a proof that the intended calculus is trivial.

Full source reads:

- [english: lines 1–73](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:1>), 3007 bytes, SHA-256 `bc7f60e5e64ad1000db484141861723f90d7eee4316d1885263c3db652089972`.
- [msa: lines 1–76](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:1>), 3957 bytes, SHA-256 `668a742d3d940e9f39237c3e189deab767cde72f4c1597347daf0f8141ae168f`.
- [classical: lines 1–75](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:1>), 3970 bytes, SHA-256 `34d9abb8cd5e378c8e6269a89361676db1df1394eab7a7abe9fd1173dfcb070d`.

Representative exact-evidence ranges: [english 13–34](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:13>); [msa 13–34](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:13>); [classical 13–34](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:13>); [english 44–69](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:44>); [msa 43–74](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:43>); [classical 43–73](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:43>).

### OLP-0405 — prose

Weakening, contraction, exchange and the two-distinct-position cut rule retain the same premise/conclusion formulas and i≠j condition.

Classical discourse: A concise conditional explanation replaces the English sentence about applying structural rules at each position; the double line is explained as compressed repeated structural steps.

Already corrected / false-positive control: No source correction identified. No macro expansion or rendered label was assumed from the raw source.

Full source reads:

- [english: lines 1–52](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:1>), 1834 bytes, SHA-256 `56cff0e33dcc908b72e501cd49a7dd69f0a70e4b74dcd2b84e9a18494848af14`.
- [msa: lines 1–52](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:1>), 1925 bytes, SHA-256 `d6c26a4389b601c973f84b9df551364a323f38d94d6ee0c40d9650cb6be4602e`.
- [classical: lines 1–52](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:1>), 2014 bytes, SHA-256 `258e16004f5aebec529e0658b0d15cc6b72f5118ba0594e297189d3190e79882`.

Representative exact-evidence ranges: [english 13–50](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:13>); [msa 13–50](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/structural-rules.tex:13>); [classical 13–50](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/structural-rules.tex:13>).

### OLP-0406 — prose

The common negation rules, two Gödel negation rules, conjunction/disjunction rules, three sets of conditional rules and full sideways proof tree were read and compared. The formula/proof-tree tokens are retained; no weakened hypotheses or omitted case found.

Classical discourse: The opening explains dependence on the characteristic truth function and distinguishes shared rules from other differences. Most remaining text is necessarily formula captions, not freely rewritable exposition.

Already corrected / false-positive control: Both Arabic files spell Kleene كلايني here but كليني in 0395. This is a reversible naming-consistency preference, not mathematical damage.

Full source reads:

- [english: lines 1–235](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:1>), 8173 bytes, SHA-256 `0d74a6c4ba24d5178d205fd05971dd4684e3d8fcdae367878ab857e3a54513b6`.
- [msa: lines 1–234](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:1>), 8251 bytes, SHA-256 `e7ba97db83b879e9d778c1199bba92069a6e90dffe7bd1c1c61e2a36196c3ceb`.
- [classical: lines 1–234](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:1>), 8240 bytes, SHA-256 `cb676762f6a0e4cc3854b275b692f9553597e8aa8510baa7322586782ccb2839`.

Representative exact-evidence ranges: [english 13–22](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:13>); [msa 13–21](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:13>); [classical 13–21](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:13>); [english 194–235](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:194>); [msa 193–234](<source-snapshot/repo/source/locale/ar/content/many-valued-logic/sequent-calculus/propositional-rules.tex:193>); [classical 193–234](<source-snapshot/repo/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/propositional-rules.tex:193>).

### OLP-0407 — prose-bearing-part-driver

Editorial scope, Aldo Antonelli attribution, seven imports and end hook remain.

Classical discourse: The short Classical editorial is rephrased as subject matter and present contents; unlike the pure drivers, this unit does contain audited prose.

Already corrected / false-positive control: Printed title says الجهية while the comment claims الجهوي and the prose also uses الموجهي. Log actual strings separately, not a combined invented heading.

Full source reads:

- [english: lines 1–31](<source-snapshot/english/content/normal-modal-logic/normal-modal-logic.tex:1>), 706 bytes, SHA-256 `e388c5bd59b5f2ac9fee081e6645262cfd0361cdc72d3e1d6f51f07788f87077`.
- [msa: lines 1–32](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:1>), 1030 bytes, SHA-256 `3a1c4b7e8cfe0721387618d87e8bf48df5553fb92df13cb10eb30d14c50ed45f`.
- [classical: lines 1–32](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:1>), 1017 bytes, SHA-256 `fdd7953c0312f61ec4a5c6c6532c231ed7a817e46c374a5afd65fe073be7013a`.

Representative exact-evidence ranges: [english 7–29](<source-snapshot/english/content/normal-modal-logic/normal-modal-logic.tex:7>); [msa 8–30](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/normal-modal-logic.tex:8>); [classical 8–30](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/normal-modal-logic.tex:8>).

### OLP-0408 — structural

All ten import targets and chapter/end identities remain.

Classical discourse: Title-only syntax/semantics chapter driver, not a prose translation.

Already corrected / false-positive control: No new correction identified.

Full source reads:

- [english: lines 1–24](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:1>), 503 bytes, SHA-256 `5e8e509437c77846b7ec17bdc55a8c960fcd45cffc363a55830ebc76ac6b03fe`.
- [msa: lines 1–23](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:1>), 489 bytes, SHA-256 `8f31dbfc1bcc84458cab71e47561a0ee485d5134d75ecc9cd703165da2532eb1`.
- [classical: lines 1–23](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:1>), 489 bytes, SHA-256 `8f31dbfc1bcc84458cab71e47561a0ee485d5134d75ecc9cd703165da2532eb1`.

Representative exact-evidence ranges: [english 8–21](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>); [msa 8–21](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>); [classical 8–21](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>).

### OLP-0409 — prose

Examples, Aristotle discussion, Lewis strict implication, Carnap iteration, Kripke accessibility, relational applications and correspondence schemas remain. The repeated Arabic scope phrase can obscure two opposite modality orders. Classical correctly restricts a world-independence statement that is overbroad in EN/MSA. The opening conditional is an example of a modal proposition, not an assertion that it is valid in every frame.

Classical discourse: The Classical version develops the historical argument in stages, makes the reason for accessibility explicit, and recasts relational applications and correspondence coherently. 'في العرض التاريخي هنا' signals the source's presentation, not independent historical validation.

Already corrected / false-positive control: Classical 'صدق عبارة الضرورة' is an evidenced semantic clarification needing propagation to the shared MSA; do not replace it with the less precise English/MSA phrase.

Full source reads:

- [english: lines 1–97](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:1>), 4962 bytes, SHA-256 `42c2f00e8f81aab33744c17ecd192e38262a12cffa935cabb079a56e541618e2`.
- [msa: lines 1–83](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:1>), 6555 bytes, SHA-256 `dec0f1a2cefc853af7abfa606d7ddfea555a3da30ad3c686cb54c1af2cfbe130`.
- [classical: lines 1–78](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:1>), 5949 bytes, SHA-256 `dd5adbd70179dc2666ebdf5db3526540617073362199be13fabc52674ce38426`.

Representative exact-evidence ranges: [english 13–33](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>); [msa 13–29](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>); [classical 13–29](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>); [english 46–95](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:46>); [msa 40–81](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/introduction.tex:40>); [classical 40–76](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/introduction.tex:40>).

### OLP-0410 — prose

All tagged alphabet items, constants, variable sequence starting at 0, connective/modal formation clauses, limit clause, conditional abbreviation alternatives and dual modal abbreviations remain. The Arabic material-conditional abbreviation already repairs English's unmatched parenthesis.

Classical discourse: The few freely written sentences organize alphabet, induction from atoms, defined abbreviations and modal-free formulas. Retaining the recursive clauses avoids perturbing their mathematical force.

Already corrected / false-positive control: No rendered Arabic is guessed for !! terminology macros; these are recorded as source macros only. Both Arabic defIf branches are balanced.

Full source reads:

- [english: lines 1–107](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:1>), 3526 bytes, SHA-256 `adacd15035d83e6b193aef874044156015bf168e67966833d5cdb5c064bdce1d`.
- [msa: lines 1–106](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:1>), 3725 bytes, SHA-256 `ba41d7d48e5d1df74f4cf52b04425e79ab726fdedd9d79fbea4bf3db794bd6c0`.
- [classical: lines 1–107](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:1>), 3857 bytes, SHA-256 `f4b2f8427ce751362ee4f530d075bcdd89c61afb8df7d4122f7c909cdd57e833`.

Representative exact-evidence ranges: [english 14–33](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:14>); [msa 14–33](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:14>); [classical 14–33](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:14>); [english 66–105](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:66>); [msa 66–104](<source-snapshot/repo/source/locale/ar/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:66>); [classical 66–105](<source-snapshot/repo/source/locale/ar-classical/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:66>).

## English-anchor correction history

All 49 English terminology anchors were reviewed for active semantic context. T01’s old lines 2–5 were a section comment and preamble: they were **not valid semantic evidence**, despite matching the source bytes. Its replacement is the active consequence-inclusion corollary, lines 71–75.

47 anchors were replaced or context-adjusted; T17 and T31 were retained after review. T31 already contains the actual weakening premise and conclusion, not merely a command name. Arabic occurrences, source identities, findings, dates, retrospective reasons and all prior limitations are unchanged.

Old intake JSON: 624,677 bytes; SHA-256 `a9ac5d24d792eea03907f092b28198931a6d99afc5d36d9769306a041a6f6788`. The companion JSON retains every old and new witness and an individual assessment for all 49 records.

| Decision | English unit | Old lines | Current lines | Disposition |
|---|---|---|---|---|
| C391-0410-T01 | OLP-0391 | 2–5 | [71–75](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:71>) | Changed |
| C391-0410-T02 | OLP-0391 | 78–81 | [79–88](<source-snapshot/english/content/many-valued-logic/syntax-and-semantics/sublogics.tex:79>) | Changed |
| C391-0410-T03 | OLP-0392 | 7–10 | [8–8](<source-snapshot/english/content/many-valued-logic/three-valued-logics/three-valued-logics.tex:8>) | Changed |
| C391-0410-T04 | OLP-0393 | 17–20 | [13–18](<source-snapshot/english/content/many-valued-logic/three-valued-logics/introduction.tex:13>) | Changed |
| C391-0410-T05 | OLP-0394 | 18–21 | [13–19](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:13>) | Changed |
| C391-0410-T06 | OLP-0394 | 38–41 | [37–39](<source-snapshot/english/content/many-valued-logic/three-valued-logics/lukasiewicz.tex:37>) | Changed |
| C391-0410-T07 | OLP-0395 | 16–19 | [13–17](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:13>) | Changed |
| C391-0410-T08 | OLP-0395 | 38–41 | [31–40](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:31>) | Changed |
| C391-0410-T09 | OLP-0395 | 45–48 | [46–87](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:46>) | Changed |
| C391-0410-T10 | OLP-0395 | 89–92 | [90–131](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:90>) | Changed |
| C391-0410-T11 | OLP-0395 | 163–166 | [164–169](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:164>) | Changed |
| C391-0410-T12 | OLP-0395 | 167–170 | [167–177](<source-snapshot/english/content/many-valued-logic/three-valued-logics/kleene.tex:167>) | Changed |
| C391-0410-T13 | OLP-0396 | 13–16 | [71–83](<source-snapshot/english/content/many-valued-logic/three-valued-logics/goedel.tex:71>) | Changed |
| C391-0410-T14 | OLP-0397 | 19–22 | [20–28](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:20>) | Changed |
| C391-0410-T15 | OLP-0397 | 30–33 | [31–49](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:31>) | Changed |
| C391-0410-T16 | OLP-0397 | 140–143 | [139–144](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:139>) | Changed |
| C391-0410-T17 | OLP-0397 | 141–144 | [141–144](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:141>) | Retained after semantic review |
| C391-0410-T18 | OLP-0397 | 161–164 | [162–170](<source-snapshot/english/content/many-valued-logic/three-valued-logics/multiple-designation.tex:162>) | Changed |
| C391-0410-T19 | OLP-0398 | 7–10 | [8–8](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/infinite-valued-logics.tex:8>) | Changed |
| C391-0410-T20 | OLP-0399 | 14–17 | [13–16](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:13>) | Changed |
| C391-0410-T21 | OLP-0399 | 31–34 | [30–32](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/introduction.tex:30>) | Changed |
| C391-0410-T22 | OLP-0400 | 13–16 | [14–15](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/lukasiewicz.tex:14>) | Changed |
| C391-0410-T23 | OLP-0401 | 13–16 | [14–14](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/goedel.tex:14>) | Changed |
| C391-0410-T24 | OLP-0401 | 98–101 | [87–99](<source-snapshot/english/content/many-valued-logic/infinite-valued-logics/goedel.tex:87>) | Changed |
| C391-0410-T25 | OLP-0402 | 7–10 | [8–8](<source-snapshot/english/content/many-valued-logic/sequent-calculus/sequent-calculus.tex:8>) | Changed |
| C391-0410-T26 | OLP-0403 | 34–37 | [27–48](<source-snapshot/english/content/many-valued-logic/sequent-calculus/introduction.tex:27>) | Changed |
| C391-0410-T27 | OLP-0404 | 16–19 | [17–23](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:17>) | Changed |
| C391-0410-T28 | OLP-0404 | 29–32 | [30–33](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:30>) | Changed |
| C391-0410-T29 | OLP-0404 | 43–46 | [45–61](<source-snapshot/english/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex:45>) | Changed |
| C391-0410-T30 | OLP-0405 | 10–13 | [11–35](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:11>) | Changed |
| C391-0410-T31 | OLP-0405 | 18–21 | [18–21](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:18>) | Retained after semantic review |
| C391-0410-T32 | OLP-0405 | 23–26 | [23–27](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:23>) | Changed |
| C391-0410-T33 | OLP-0405 | 29–32 | [29–33](<source-snapshot/english/content/many-valued-logic/sequent-calculus/structural-rules.tex:29>) | Changed |
| C391-0410-T34 | OLP-0406 | 13–16 | [13–17](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:13>) | Changed |
| C391-0410-T35 | OLP-0406 | 20–23 | [21–22](<source-snapshot/english/content/many-valued-logic/sequent-calculus/propositional-rules.tex:21>) | Changed |
| C391-0410-T36 | OLP-0407 | 6–9 | [7–12](<source-snapshot/english/content/normal-modal-logic/normal-modal-logic.tex:7>) | Changed |
| C391-0410-T37 | OLP-0407 | 9–12 | [10–12](<source-snapshot/english/content/normal-modal-logic/normal-modal-logic.tex:10>) | Changed |
| C391-0410-T38 | OLP-0408 | 7–10 | [8–8](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/syntax-and-semantics.tex:8>) | Changed |
| C391-0410-T39 | OLP-0409 | 12–15 | [13–25](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:13>) | Changed |
| C391-0410-T40 | OLP-0409 | 17–20 | [18–20](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:18>) | Changed |
| C391-0410-T41 | OLP-0409 | 50–53 | [46–57](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:46>) | Changed |
| C391-0410-T42 | OLP-0409 | 65–68 | [65–71](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:65>) | Changed |
| C391-0410-T43 | OLP-0409 | 81–84 | [73–83](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:73>) | Changed |
| C391-0410-T44 | OLP-0409 | 79–82 | [78–83](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:78>) | Changed |
| C391-0410-T45 | OLP-0409 | 85–88 | [85–95](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:85>) | Changed |
| C391-0410-T46 | OLP-0409 | 37–40 | [35–44](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/introduction.tex:35>) | Changed |
| C391-0410-T47 | OLP-0410 | 25–28 | [26–27](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:26>) | Changed |
| C391-0410-T48 | OLP-0410 | 104–107 | [104–105](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:104>) | Changed |
| C391-0410-T49 | OLP-0410 | 31–34 | [32–64](<source-snapshot/english/content/normal-modal-logic/syntax-and-semantics/language-modal-logic.tex:32>) | Changed |

Post-correction readback: PASS in one bounded run for 60 source identities, 20 units, 49 decisions, 314 current quotations, 141 Arabic occurrences, six findings and all Markdown anchors. Reverting only the permitted witness/binding-metadata changes and restoring the original extra terminal LF reconstructs the exact old JSON hash above. The initial preservation-only comparison exposed that one-byte newline normalization; its bounded follow-up confirmed the match without rerunning counts or quotes.

## Validation and remaining limits

PASS: 60 current identities rechecked; 20 English baseline hashes match; 314 exact quoted witnesses and 141 literal occurrences validate.

Across each edition: 30 matching table blocks, 159 matching proof-tree command lines, 20 matching exercise blocks, and matching import/section identity tokens. Whitespace normalization only; not a TeX build or universal semantic proof.

The modal arithmetic and dyadic counterexample were checked in a small bounded JavaScript lane. The infinite counterexample is justified by the algebraic proof, not by a finite test alone.

- No PDF, AUX or SyncTeX evidence was used. Printed/PDF page fields are deliberately null; source-line locators are exact for the recorded bytes.
- No official dictionary, medieval-original, Unicode rendering, external historical attribution or external R-Mingle naming attestation was performed or claimed in this bounded audit.
- All 20 primary-source triples were read. The 49 recorded choices enumerate all exact literal matches of their recorded forms in their listed unit, not every morphological variant or synonym and not rendered !! macro expansions.
- The 30 tables per edition, 159 proof-tree command lines per edition, 20 exercise blocks per edition and import/identity comparisons are bounded structural checks; they do not prove arbitrary TeX rendering or the soundness of every mathematical source claim.
- No corrections were applied. Four definite correction proposals and two ambiguities remain for a later consolidated source batch. Optional human expert input does not prevent a provisional evidence-based decision.
- This report is local intake, not a change to the root goal's completion, central decision coverage, source batch, release inventory or published bytes.

Machine-readable companion: [units-0391-0410-continuation.json](<source-snapshot/repo/tmp/redo-20260906-propagation/units-0391-0410-continuation.json>).

Next action: reconcile this later-batch intake without reopening or delaying the frozen current batch.

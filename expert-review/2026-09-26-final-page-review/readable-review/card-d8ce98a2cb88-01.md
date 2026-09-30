# صفحة ١ من بطاقة المراجعة

[فهرس هذه البطاقة](card-d8ce98a2cb88.md) · [الدليل الكامل](../DIRECTORY_READABLE_AR.md) · [التالي](card-d8ce98a2cb88-02.md)


عرض القراءة وتقسيم الصفحات: OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. لم تُعد صياغة التعليلات بهذا التقسيم، ولا يثبت سلامتها الدلالية أو المعجمية؛ لم تقع مراجعة بشرية شاملة، وكل اختيار قابل للتصحيح.


<!-- BEGIN PRESERVED REVIEW TEXT -->
# القرارات العربية الحالية — الجزء ٩ من ١١

[الرجوع إلى فهرس الأجزاء](../arabic-existing/README.md)

السياقات والتعليلات أدناه من السجل القائم؛ لم تُراجع جميعها مراجعة معجمية جديدة في هذا الإخراج. يعني تحذير الموضع غير المحسوم أن الملف معروف لكن السطر الحالي لم يثبت، ويعني رابط بدء الوحدة أن صفحة اللفظ ليست معلومة بالدقة.

## الترتيب المسبق

الأصل الإنجليزي: `Preorder`. معرّف القرار: `retro-0005-0050:named-defn:cf711a0bd98782c1`.

**المعنى المقصود:** علاقة ثنائية انعكاسية ومتعدية؛ لا يشترط فيها ضد التناظر ولا الاتصال.

**سبب الاختيار:** التعريف المحلي يذكر الشرطين فقط، فتدل «مسبق» على رتبة أضعف من partial order. DAM يثبت عائلة «ترتيب جزئي/علاقة ترتيب» ولا يقدم مدخلًا مباشرًا لـ preorder.

**سؤال مفتوح:** هل «الترتيب المسبق» الأنسب لـ preorder أم يفضل «شبه ترتيب»؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٢٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L22). الشاهد المسجل: «\begin{defn}[Preorder]».
  - **العربية المعيارية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L21)؛ الطبعة الدولية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=45) (ترقيم المتن: ٤٤)، [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=45) (ترقيم المتن: ٤٤)، [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الترتيب المسبق]».
  - **العربية التراثية:** [السطر ٢٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L20)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الترتيب المسبق]».

## العودية البدائية / التركيب / الإسقاط / الرتبة / التصغير المحدود / عودية مسار القيم

الأصل الإنجليزي: `primitive recursion / composition / projection / arity / bounded minimization / course-of-values recursion`. معرّف القرار: `locale-ar-chosen-bb60e2079ebf828e`.

**المعنى المقصود:** مصطلحات مستقلة في نظرية الدوال العودية: مخطط العودية البدائية؛ تركيب الدوال؛ دوال الإسقاط؛ عدد حجج الدالة؛ أصغر شاهد دون حد معطى؛ والعودية التي يجوز لخطوتها استعمال متتالية جميع القيم السابقة.

**سبب الاختيار:** قورنت الوحدات OLP-0211–0222 كاملة في الأصل الإنجليزي والعربية المعيارية والعربية الكلاسيكية. تتطابق الصيغ والتعريفات في «العودية البدائية» و«التركيب» و«دوال الإسقاط» و«رتبة الدالة» و«التصغير المحدود» و«عودية مسار القيم»، ولا يُسقط أي لفظ منها قيدًا أو وسيطًا أو اتجاهًا. يشهد معجم دمشق مباشرة لـ composition of functions/تركيب دوال، ويشهد للجذر minimization/تصغير في معنى بولي مختلف فقط؛ أما بقية رؤوس الحزمة، وخصوصًا primitive recursion وarity وbounded minimization وcourse-of-values recursion، فلم توجد لها رؤوس إنجليزية مطابقة في البحث الحرفي المحدود في المعجم. لذلك لا يجوز وصف الحزمة كلها بأنها موثقة معجميًا، ويبقى السؤال الخبروي مطلوبًا لكل مكوّن.

**سؤال مفتوح:** هل الأنسب، في سياق الدوال العودية الوارد في OLP-0211–0222، اعتماد الأزواج الستة الآتية كما هي: primitive recursion = «العودية البدائية»، composition = «التركيب»، projection = «الإسقاط»، arity = «الرتبة»، bounded minimization = «التصغير المحدود»، وcourse-of-values recursion = «عودية مسار القيم»؟ أم تفضّلون، لأي مكوّن بعينه، «الاستدعاء الأولي» أو «التأليف» أو «المسقط» أو «عدد المواضع/عدد الحجج» أو «التقليل المقيد» أو «العودية بالقيم السابقة»؟ يرجى تعيين المكوّن الذي تقترحون تغييره وسبب الملاءمة الاصطلاحية في هذا المعنى الصوري، مع العلم أن «تصغير» المعجم مشهود في معنى بولي غير معنى البحث المحدود؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0211 — العودية البدائية، وقوع ١:**

## قاسم فعلي

الأصل الإنجليزي: `proper divisor`. معرّف القرار: `locale-ar-chosen-6597be6f8345b43e`.

**المعنى المقصود:** قاسم صحيح لعدد يقسمه بلا باق ولا يساويه؛ أي proper divisor في سياق العدد التام.

**سبب الاختيار:** تعريف OLP-0005 في اللغات الثلاث يحفظ شرطي القسمة بلا باق وعدم مساواة العدد نفسه. ويطابقه معجم دمشق لفظًا وتعريفًا في رأس proper divisor = «قاسم فعلي»، مع مثال قواسم 12 الفعلية. لذلك يؤيد الكانون الاختيار مباشرة، ويبقى «قاسم حقيقي» بديلًا إقليميًا يحتاج موازنة استعمالية لا تصحيحًا دلاليًا.

**سؤال مفتوح:** هل «قاسم فعلي» هو الرأس العربي الأنسب لـ proper divisor في نظرية الأعداد، بالنظر إلى أنه يقسم العدد بلا باق ولا يساويه، أم تفضّلون «قاسم حقيقي» في هذا السجل؟ وهل ترون فرقًا إقليميًا أو تعليميًا يبرر ذكر المرادف مع إبقاء «قاسم فعلي» رأسًا؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0005 — الامتدادية، وقوع ١:**
  - **الأصل:** [السطر ٧٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L75). الشاهد المسجل: «A number is called \emph{perfect} iff it is equal to the sum of its proper divisors (i.e., numbers that evenly divide it but aren't identical to the number). For instance, $6$ is perfect because its proper divisors are $1$, $2$, and~$3$, and $6 = 1 + 2 + 3$…».
  - **العربية المعيارية:** [السطر ٧٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/basics.tex#L75)؛ الطبعة الدولية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «يُسمى العدد \emph{تامًا} إذا وفقط إذا كان مساويًا لمجموع قواسمه الفعلية (أي الأعداد التي تقسمه من دون باق، ولا تساوي العدد نفسه). فمثلًا، العدد $6$ تام لأن قواسمه الفعلية هي $1$ و$2$ و~$3$، ولأن $6 = 1 + 2 + 3$. والواقع أن».
  - **العربية التراثية:** [السطر ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/basics.tex#L68)؛ الطبعة التراثية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «العدد \emph{التام} هو المساوي لمجموع قواسمه الفعلية، وهي الأعداد التي تقسمه بلا باق ولا تساويه هو نفسه. فالعدد $6$ تام؛ إذ قواسمه الفعلية $1$ و$2$ و~$3$، و$6 = 1 + 2 + 3$. وهو $6$ وحده التام».

## مجموعة جزئية فعلية

الأصل الإنجليزي: `proper subset`. معرّف القرار: `locale-ar-chosen-be996e3ce6febd34`.

**المعنى المقصود:** مجموعة A محتواة في B مع A≠B، ويرمز إليها A⊊B؛ أي proper subset لا مجرد subset.

**سبب الاختيار:** تعريف OLP-0006 متطابق في اللغات الثلاث، ويقرن اللفظ صراحة بشرطي الاحتواء وعدم المساواة. ويسجل معجم دمشق الرأس نفسه proper subset = «مجموعة جزئية فعلية» ويعرّفه بالاحتواء التام. لذلك لا يختلط الرمز الصارم بالاحتواء غير الصارم.

**سؤال مفتوح:** هل «مجموعة جزئية فعلية» هو الرأس العربي الأنسب لـ proper subset بمعنى A⊆B وA≠B (أي A⊊B)، أم تفضّلون «مجموعة جزئية حقيقية»؟ وهل ينبغي تجنب «مناسبة» و«صحيحة» لضعف دلالتهما على صرامة الاحتواء؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0006 — المجموعات الجزئية ومجموعات القوى، وقوع ١:**
  - **الأصل:** [السطر ٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/subsets.tex#L24). الشاهد المسجل: «that $A$ is a \emph{proper subset} of $B$.».
  - **العربية المعيارية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/subsets.tex#L24)؛ الطبعة الدولية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن $A$ \emph{مجموعة جزئية فعلية} من $B$.».
  - **العربية التراثية:** [السطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/subsets.tex#L23)؛ الطبعة التراثية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وتسمى $A$ حينئذ \emph{مجموعة جزئية فعلية} من $B$.».

## قضية

الأصل الإنجليزي: `proposition`. معرّف القرار: `locale-ar-chosen-c30b707a94517abd`.

**المعنى المقصود:** proposition في استعمالين ظاهرين في الشواهد: عبارة خبرية تقبل الصدق والكذب، ونتيجة رياضية مصوغة داخل بيئة prop أو محال إليها بقول «القضية الآتية».

**سبب الاختيار:** تستعمل النسختان العربيتان «قضية» في مواضع العبارة الصدقية وفي مواضع النتيجة الرياضية، ويشهد معجم دمشق لـ proposition بالمقابلين «قضية، دعوى». الاختيار الحالي ممكن في الاستعمالين، لكن الكانون لا يلغي «دعوى». أصلحت هذه المرحلة محاذاة OLP-0430 فقط: proposition في السطر الإنجليزي 35 يقابله «القضية الآتية» في السطر العربي 33، لا موضع tautology في السطرين 68/70. بقية المواضع الأربعة محفوظة بمقاطعها الدقيقة.

**سؤال مفتوح:** هل ينبغي إبقاء «قضية» ترجمةً موحدة لـ proposition في مواضع العبارة الصدقية والنتيجة الرياضية المبرهنة، أم تفضّلون التفريق باستعمال «دعوى» للنتيجة الرياضية و«قضية» للعبارة التي تقبل الصدق والكذب؟ وكيف توزعون هذين اللفظين على الشواهد الخمسة، علمًا بأن معجم دمشق يثبت كليهما؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0430 — Derivations والنظم الجهية، وقوع ١:**
  - **الأصل:** [السطر ٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/normal-modal-logic/axioms-systems/logics-proofs.tex#L35). الشاهد المسجل: «The following proposition allows us to show that $!B \in \Sigma$».
  - **العربية المعيارية:** [السطر ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/normal-modal-logic/axioms-systems/logics-proofs.tex#L68)؛ الطبعة الدولية: [ص ٧٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=738) (ترقيم المتن: ٧٣٧)، [ص ٧٣٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=739) (ترقيم المتن: ٧٣٨) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٣٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=739) (ترقيم المتن: ٧٣٨)، [ص ٧٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=740) (ترقيم المتن: ٧٣٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item كل قضية صادقة صدقا تحليليا~$!B$ مثال لمثل هذه القضية، ولذلك».
  - **العربية التراثية:** [السطر ٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/normal-modal-logic/axioms-systems/logics-proofs.tex#L70)؛ الطبعة التراثية: [ص ٧٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=724) (ترقيم المتن: ٧٢٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item كل قضية صادقة صدقا تحليليا~$!B$ مثال لمثل هذه القضية، ولذلك».
- **OLP-0057 — مقدمة، وقوع ٢:**
  - **الأصل:** [السطر ١٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/propositional-logic/syntax-and-semantics/introduction.tex#L16). الشاهد المسجل: «!!a{propositional variable}~$p$ stands for a sentence or proposition».
  - **العربية المعيارية:** [السطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/propositional-logic/syntax-and-semantics/introduction.tex#L16)؛ الطبعة الدولية: [ص ١١٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=113) (ترقيم المتن: ١١٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=113) (ترقيم المتن: ١١٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «!!a{propositional variable}~$p$ جملةً أو قضيةً تكون صادقة أو كاذبة.».
  - **العربية التراثية:** [السطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/propositional-logic/syntax-and-semantics/introduction.tex#L16)؛ الطبعة التراثية: [ص ١٠٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=108) (ترقيم المتن: ١٠٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «!!a{propositional variable}~$p$ في التصور الأول أنه يقوم مقام جملة أو قضية تقبل الصدق والكذب.».
- **OLP-0013 — تأملات فلسفية، وقوع ٣:**
  - **الأصل:** [السطر ٦٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/reflections.tex#L64). الشاهد المسجل: «expressing a proposition than the nonsense string: ``the cup penholder».
  - **العربية المعيارية:** [السطر ٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/reflections.tex#L58)؛ الطبعة الدولية: [ص ٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=43) (ترقيم المتن: ٤٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=43) (ترقيم المتن: ٤٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وليست قائمة كهذه من الأسماء أقدر على التعبير عن قضية من السلسلة عديمة».
  - **العربية التراثية:** [السطر ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/reflections.tex#L52)؛ الطبعة التراثية: [ص ٤٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=42) (ترقيم المتن: ٤١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: ««$\tuple{x,y}$» و«$\in$» و«$R$». ومجرد سرد الأسماء لا يعبر عن قضية،».
- **OLP-0617 — التعريفات الاستقرائية، وقوع ٤:**
  - **الأصل:** [السطر ١٣٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/methods/induction/inductive-definitions.tex#L137). الشاهد المسجل: «proposition follows.».
  - **العربية المعيارية:** [السطر ٨٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/methods/induction/inductive-definitions.tex#L83)؛ الطبعة الدولية: [ص ٩٨١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=981) (ترقيم المتن: ٩٨٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٨٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=982) (ترقيم المتن: ٩٨١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «بوصفه قضية عن جميع~$n$: لكل $n$، عدد الرموز $[$ في أي حد سليم».
  - **العربية التراثية:** [السطر ٧٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/methods/induction/inductive-definitions.tex#L77)؛ الطبعة التراثية: [ص ٩٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=960) (ترقيم المتن: ٩٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «سليم طوله~$n$ هو~$< n/2$، أمكن أن نجعله قضية في جميع~$n$: لكل $n$،».
- **OLP-0495 — تأويل براور--هايتنغ--كولموغوروف، وقوع ٥:**
  - **الأصل:** [السطر ٥٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/intuitionistic-logic/introduction/bhk-interpretation.tex#L55). الشاهد المسجل: «Let us prove $!A \lif \lnot \lnot !A$ for any proposition~$!A$, which».
  - **العربية المعيارية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/intuitionistic-logic/introduction/bhk-interpretation.tex#L46)؛ الطبعة الدولية: [ص ٨٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=825) (ترقيم المتن: ٨٢٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٨٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=826) (ترقيم المتن: ٨٢٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لنبرهن $!A \lif \lnot \lnot !A$ لأي قضية~$!A$، أي».
  - **العربية التراثية:** [السطر ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/intuitionistic-logic/introduction/bhk-interpretation.tex#L45)؛ الطبعة التراثية: [ص ٨١٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=810) (ترقيم المتن: ٨٠٩)، [ص ٨١١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=811) (ترقيم المتن: ٨١٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نريد بناء~$!A \lif \lnot \lnot !A$ لكل قضية~$!A$، أي بناء».

## إثبات

الأصل الإنجليزي: `prove`. معرّف القرار: `retro-0005-0050:emphasis:e35f43faf7664a84`.

**المعنى المقصود:** تحصيل برهان لمبرهنة شرودر–برنشتاين؛ حُوّل الفعل prove إلى مصدر في «وسائل إثبات مبرهنة».

**سبب الاختيار:** العربية تحتاج اسمًا بعد «وسائل»، فـ«إثبات» تحويل نحوي لا تغيير منطقي. ويستعمل تعريف DAM لمدخل «direct proof — برهان مباشر» لفظ «إثبات» نفسه في عبارة «إثبات صحة قضية...»، فيؤيد المصدر دلالة اللفظ وإن لم يجعله رأس المدخل.

**سؤال مفتوح:** هل «وسائل إثبات مبرهنة» أسلس من «وسائل البرهنة على مبرهنة»؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0037 — مفهوم الحجم ومبرهنة شرودر–برنشتاين، وقوع ١:**
  - **الأصل:** [السطر ٣٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/schroder-bernstein.tex#L39). الشاهد المسجل: «a position to \emph{prove} Schr\"oder-Bernstein in».
  - **العربية المعيارية:** [السطر ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/schroder-bernstein.tex#L36)؛ الطبعة الدولية: [ص ٧٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=77) (ترقيم المتن: ٧٦) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٧٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=77) (ترقيم المتن: ٧٦) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{إثبات} مبرهنة شرودر–برنشتاين إلا في».
  - **العربية التراثية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/schroder-bernstein.tex#L26)؛ الطبعة التراثية: [ص ٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=74) (ترقيم المتن: ٧٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\oliflabeldef{sfr:cardinals:card-sb:sec}{ولن تتهيأ لنا وسائل \emph{إثبات} مبرهنة شرودر–برنشتاين حتى نبلغ \olref[sfr][cardinals][card-sb]{sec}.}{}%».

## الرباعيات

الأصل الإنجليزي: `quadruples`. معرّف القرار: `retro-0005-0050:emphasis:fc6fc052e3bdb157`.

**المعنى المقصود:** الصفوف المرتبة ذات أربعة مكونات ⟨x,y,z,u⟩ ضمن بناء tuples تكراريًا.

**سبب الاختيار:** قربها من triples وtuples يجعل «الرباعيات» مفهومة بوصفها مرتبة، لكن DAM يصرح «رباعية مرتبة». حذف الصفة اقتصاد سياقي قد يفتح لبسًا مع مجموعة من أربعة عناصر.

**سؤال مفتوح:** هل يكفي سياق tuples لحذف «المرتبة»، أم ينبغي «الرباعيات المرتبة»؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0009 — الأزواج والصفوف المرتبة والضروب الديكارتية، وقوع ١:**
  - **الأصل:** [السطر ٤٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/pairs-and-products.tex#L42). الشاهد المسجل: «\emph{quadruples} $\tuple{x, y, z, u}$, and so on. We can think of».
  - **العربية المعيارية:** [السطر ٤١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/pairs-and-products.tex#L41)؛ الطبعة الدولية: [ص ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=37) (ترقيم المتن: ٣٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=37) (ترقيم المتن: ٣٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الثلاثيات} $\tuple{x, y, z}$ و\emph{الرباعيات}».
  - **العربية التراثية:** [السطر ٣٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/pairs-and-products.tex#L39)؛ الطبعة التراثية: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «و\emph{الرباعيات} $\tuple{x, y, z, u}$، ثم ما بعدها.».

## المكمّمات

الأصل الإنجليزي: `quantifier`. معرّف القرار: `repair-compact-0101-0200:QNT-01`.

**المعنى المقصود:** عامل الربط المتغيري ∀ أو ∃ وقواعده وصوره في منطق الرتبة الأولى؛ استعمل الجمع «المكمّمات» في العناوين والكلام العام، والمفرد «المكمّم» عند تعيين العامل.

**سبب الاختيار:** قورنت المواضع المسماة في OLP-0104 و0108 و0112 و0115 و0117 و0120 و0123 و0128 بالإنجليزية والعربية المعيارية والكلاسيكية. تحافظ «المكمّمات» و«المكمّم» على معنى quantifiers/quantifier وعلى الفرق العددي، ولا تمس رمزي ∀ و∃ أو شروط المتغير المميز. أزيلت من التمثيل المرشح ست مجموعات فارغة مكررة كانت تكرر الوحدات من غير موضع. لم يوجد رأس quantifier إنجليزي مطابق في معجم دمشق المستعمل، ولذلك لا توجد دعوى توثيق رسمي لهذا الاختيار، ويبقى «السور/الأسوار» منافسًا عربيًا معروفًا يحتاج حكمًا خبيرًا.

**سؤال مفتوح:** في منطق الرتبة الأولى، هل تفضّلون quantifier = «مكمّم» وجمعه «مكمّمات» كما في المواضع الثمانية، أم «سور/أسوار» أو «أداة/أدوات تكميم»؟ وهل ينبغي توحيد العناوين والقواعد على صيغة واحدة مع إبقاء المفرد حين يشار إلى ∀ أو ∃ بعينه؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0104 — Tableaux مع المكمّمات، وقوع ١:**
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/tableaux/proving-things-quant.tex)؛ الطبعة الدولية: [ص ٣٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=326) (ترقيم المتن: ٣٢٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=326) (ترقيم المتن: ٣٢٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/tableaux/proving-things-quant.tex)؛ الطبعة الدولية: [ص ٣٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=326) (ترقيم المتن: ٣٢٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=326) (ترقيم المتن: ٣٢٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/tableaux/proving-things-quant.tex)؛ الطبعة الدولية: [ص ٣٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=326) (ترقيم المتن: ٣٢٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=326) (ترقيم المتن: ٣٢٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/tableaux/proving-things-quant.tex)؛ الطبعة التراثية: [ص ٣١٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=319) (ترقيم المتن: ٣١٨) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
- **OLP-0108 — Derivability والمكمّمات، وقوع ٢:**
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/tableaux/provability-quantifiers.tex)؛ الطبعة الدولية: [ص ٣٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=337) (ترقيم المتن: ٣٣٦) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=337) (ترقيم المتن: ٣٣٦) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/tableaux/provability-quantifiers.tex#L10)؛ الطبعة التراثية: [ص ٣٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=330) (ترقيم المتن: ٣٢٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{\usetoken{S}{derivability} والمكمّمات}».
- **OLP-0112 — Derivations البديهي، وقوع ٤:**
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/axiomatic-deduction.tex)؛ الطبعة الدولية: [ص ٣٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=346) (ترقيم المتن: ٣٤٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=346) (ترقيم المتن: ٣٤٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/axiomatic-deduction.tex)؛ الطبعة الدولية: [ص ٣٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=346) (ترقيم المتن: ٣٤٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=346) (ترقيم المتن: ٣٤٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [السطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/axiomatic-deduction.tex#L16)؛ الطبعة التراثية: [ص ١٨١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=181) (ترقيم المتن: ١٨٠)، [ص ٣٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=338) (ترقيم المتن: ٣٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «على المكمّمات، وإلا ظهرت نسخة تخلو منها.».
- **OLP-0115 — بديهيات المكمّمات وقواعدها، وقوع ٥:**
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/axioms-rules-quantifiers.tex)؛ الطبعة الدولية: [ص ٣٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=348) (ترقيم المتن: ٣٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=348) (ترقيم المتن: ٣٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/axioms-rules-quantifiers.tex)؛ الطبعة الدولية: [ص ٣٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=348) (ترقيم المتن: ٣٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=348) (ترقيم المتن: ٣٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/axioms-rules-quantifiers.tex)؛ الطبعة الدولية: [ص ٣٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=348) (ترقيم المتن: ٣٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=348) (ترقيم المتن: ٣٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/axioms-rules-quantifiers.tex#L11)؛ الطبعة التراثية: [ص ٣٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=340) (ترقيم المتن: ٣٣٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{بديهيات المكمّمات وقواعدها}».
  - **العربية التراثية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/axioms-rules-quantifiers.tex#L13)؛ الطبعة التراثية: [ص ٣٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=340) (ترقيم المتن: ٣٣٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[بديهيات المكمّمات]».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/axioms-rules-quantifiers.tex#L29)؛ الطبعة التراثية: [ص ٣٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=340) (ترقيم المتن: ٣٣٩)، [ص ٣٤١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=341) (ترقيم المتن: ٣٤٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[قواعد المكمّمات]».
- **OLP-0117 — Derivations مع المكمّمات، وقوع ٧:**
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/proving-things-quant.tex)؛ الطبعة الدولية: [ص ٣٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=351) (ترقيم المتن: ٣٥٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=351) (ترقيم المتن: ٣٥٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/proving-things-quant.tex#L11)؛ الطبعة التراثية: [ص ٣٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=343) (ترقيم المتن: ٣٤٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{\usetoken{P}{derivation} مع المكمّمات}».
- **OLP-0120 — مبرهنة الاستنباط مع المكمّمات، وقوع ٩:**
  - **العربية المعيارية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/deduction-theorem-quantifiers.tex#L11)؛ الطبعة الدولية: [ص ٣٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=355) (ترقيم المتن: ٣٥٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=355) (ترقيم المتن: ٣٥٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{مبرهنة الاستنباط مع المكمّمات}».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/deduction-theorem-quantifiers.tex#L11)؛ الطبعة التراثية: [ص ٣٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=347) (ترقيم المتن: ٣٤٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{مبرهنة الاستنباط مع المكمّمات}».
- **OLP-0123 — Derivability والمكمّمات، وقوع ١١:**
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/axiomatic-deduction/provability-quantifiers.tex)؛ الطبعة الدولية: [ص ٣٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=358) (ترقيم المتن: ٣٥٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=358) (ترقيم المتن: ٣٥٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [السطر ١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/axiomatic-deduction/provability-quantifiers.tex#L14)؛ الطبعة التراثية: [ص ٣٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=350) (ترقيم المتن: ٣٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{\usetoken{S}{derivability} والمكمّمات}».
- **OLP-0128 — مخطط البرهان، وقوع ١٣:**
  - **العربية المعيارية:** [السطر ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/first-order-logic/completeness/outline.tex#L91)؛ الطبعة الدولية: [ص ٣٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=363) (ترقيم المتن: ٣٦٢) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=363) (ترقيم المتن: ٣٦٢) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «الرموز الثابتة، ومعها جملًا تصل بينها وبين المكمّمات على الوجه الصحيح.».
  - **العربية التراثية:** [السطر ٧٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/completeness/outline.tex#L77)؛ الطبعة التراثية: [ص ٣٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=355) (ترقيم المتن: ٣٥٤) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «غير أن المكمّمات تعرض لنا عقبة. فإذا كان $\lexists[x][!A(x)] \in \Gamma$،».
  - **العربية التراثية:** [السطر ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/completeness/outline.tex#L87)؛ الطبعة التراثية: [ص ٣٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=355) (ترقيم المتن: ٣٥٤) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «جملًا تصلها بالمكمّمات على الوجه اللازم. ويبقى علينا، بالطبع، أن نثبت».

## مجموعة قسمة

الأصل الإنجليزي: `quotient`. معرّف القرار: `retro-0005-0050:emphasis:67faf5f0c6d22ba3`.

**المعنى المقصود:** المجموعة A/R المؤلفة من جميع أصناف التكافؤ لعلاقة التكافؤ R على A.

**سبب الاختيار:** السطر يأتي بعد تعريف الصنف ويجمع الأصناف في كائن واحد. «مجموعة قسمة» تحفظ فكرة quotient، لكن DAM يعرّف الكائن نفسه تحت «مجموعة خوارج القسمة»، وهو تعارض مباشر.

**سؤال مفتوح:** هل تُبقى «مجموعة قسمة» أم تراجع إلى «مجموعة خوارج القسمة» المثبتة؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0015 — علاقات التكافؤ، وقوع ١:**
  - **الأصل:** [السطر ٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/equivalence-relations.tex#L34). الشاهد المسجل: «= \Setabs{y \in A}{Rxy}$. The \emph{quotient} of $A$ under~$R$ is».
  - **العربية المعيارية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/equivalence-relations.tex#L30)؛ الطبعة الدولية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «= \Setabs{y \in A}{Rxy}$. وتكون \emph{مجموعة قسمة} $A$ بالنسبة إلى~$R$ هي».
  - **العربية التراثية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/equivalence-relations.tex#L30)؛ الطبعة التراثية: [ص ٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=43) (ترقيم المتن: ٤٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «= \Setabs{y \in A}{Rxy}$. وأما \emph{مجموعة قسمة} $A$ بالنسبة».

## مجموعة قسمة A بالنسبة إلى R؛ مجموعة القسمة

الأصل الإنجليزي: `quotient of A under R; quotient set`. معرّف القرار: `locale-ar-chosen-e05cc60778d13cd6`.

**المعنى المقصود:** مجموعة جميع فئات التكافؤ للعلاقة R على A، أي A/R؛ quotient of A under R وquotient set في نظرية العلاقات.

**سبب الاختيار:** تعريف OLP-0015 متطابق في اللغات الثلاث: A/R هي المجموعة الجامعة لفئات التكافؤ. الصياغة الحالية «مجموعة قسمة A بالنسبة إلى R» سليمة دلاليًا ومتسقة مع نص الطبعة، لكن معجم دمشق يسجل للمفهوم نفسه «مجموعة خوارج القسمة». لذلك لا يجوز تقديم الاختيار الحالي بوصفه الوحيد الموثق؛ السؤال يجب أن يعرض التعارض مباشرة. أضيف شاهد العربية الكلاسيكية الذي كان غير مسجل في القرار السابق.

**سؤال مفتوح:** أي الرأسين أدق وأشيع لـ quotient set = A/R، أي مجموعة فئات تكافؤ R على A: «مجموعة قسمة A بالنسبة إلى R» أم «مجموعة خوارج القسمة لـ A بالنسبة إلى R» كما في معجم دمشق؟ وهل ترون أن «مجموعة القسمة» المختصرة كافية بعد التعريف؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0015 — علاقات التكافؤ، وقوع ١:**
  - **الأصل:** [السطر ٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/equivalence-relations.tex#L31). الشاهد المسجل: «\begin{defn}\ollabel{def:equivalenceclass} Let $R \subseteq A^2$ be an equivalence relation. For each $x \in A$, the \emph{equivalence class} of $x$ in~$A$ is the set $\equivrep{x}{R} = \Setabs{y \in A}{Rxy}$. The \emph{quotient} of $A$ under~$R$ is $\equiv…».
  - **العربية المعيارية:** [السطر ٢٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/equivalence-relations.tex#L27)؛ الطبعة الدولية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}\ollabel{def:equivalenceclass} لتكن $R \subseteq A^2$ علاقة تكافؤ. لكل $x \in A$، تكون \emph{فئة التكافؤ} للعنصر $x$ في~$A$ هي المجموعة $\equivrep{x}{R} = \Setabs{y \in A}{Rxy}$. وتكون \emph{مجموعة قسمة} $A$ بالنسبة إلى~$R$ هي $\equivclass{A}{R}…».

## بناء الأعداد النسبية فئات تكافؤ لأزواج الأعداد الصحيحة ذات المقام غير الصفري

الأصل الإنجليزي: `rational construction as integer pairs modulo Ratequiv`. معرّف القرار: `locale-ar-chosen-f2e0521fa52bd1c8`.

**المعنى المقصود:** بناء ℚ بوصفه خارج قسمة ℤ×(ℤ∖{0}) بعلاقة (a,b)∼(c,d) iff ad=bc، ثم تعريف الجمع والضرب والترتيب على الفئات وتضمين ℤ بالمقام 1.

**سبب الاختيار:** قُرئ OLP-0043 كاملًا في اللغات الثلاث. ترفض الصياغة مساواة العدد النسبي بالزوج الممثل وحده، وتمنع المقام الصفري، وتحفظ علاقة Ratequiv والضرب التبادلي والفئات والعمليات وتضمين الصحيح. وهي لذلك وصف بناء صحيح لا رأس معجمي بسيط. مدخلا quotient set وrational number في معجم دمشق يثبتان مفهومين مجاورين فقط؛ أولهما يسمي الخارج «مجموعة خوارج القسمة»، والثاني يختار «عدد منطق»، ولا يعرض أي منهما هذا البناء الكامل. أضيف شاهد العربية الكلاسيكية الكامل.

**سؤال مفتوح:** هل الصياغة «بناء الأعداد النسبية فئات تكافؤ لأزواج الأعداد الصحيحة ذات المقام غير الصفري» واضحة ودقيقة بوصفها وصفًا للبناء ℤ×(ℤ∖{0})/Ratequiv، أم تفضّلون «بناء ℚ خارجَ قسمة أزواج صحيحة ذات حد ثان غير صفري» أو صياغة أخرى؟ يرجى مراعاة ألا توحي الصياغة بأن الزوج نفسه هو العدد النسبي أو بأن لكل فئة ممثلًا مختزلًا وحيدًا؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0043 — من ℤ إلى ℚ، وقوع ١:**
  - **الأصل:** [السطر ٢٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/rationals.tex#L22). الشاهد المسجل: «The obvious approach would be to think of the rationals \emph{as} ordered pairs drawn from $\Int \times (\Int \setminus \{0_\Int\})$. As before, though, that would be a bit too na\"ive, since we want $\nicefrac{3}{2} = \nicefrac{6}{4}$, but $\tuple{ 3, 2}\n…».
  - **الأصل:** [السطر ٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/rationals.tex#L47). الشاهد المسجل: «As with the integers, we also want to define some basic operations. Where $\equivrep{i,j}{\Ratequiv}$ is the equivalence class under $\Ratequiv$ with $\tuple{i, j}$ as !!a{element}, we say: \begin{align*} \equivrep{a, b}{\Ratequiv} + \equivrep{c, d}{\Ratequ…».
  - **العربية المعيارية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/rationals.tex#L21)؛ الطبعة الدولية: [ص ٨٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=89) (ترقيم المتن: ٨٨) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٨٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=89) (ترقيم المتن: ٨٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «قد يبدو النهج الواضح أن نفكر في الأعداد النسبية \emph{على أنها} أزواج مرتبة مأخوذة من $\Int \times (\Int \setminus \{0_\Int\})$. لكن هذا، كما من قبل، سيكون ساذجًا أكثر مما ينبغي؛ إذ نريد $\nicefrac{3}{2} = \nicefrac{6}{4}$، لكن $\tuple{ 3, 2}\neq \tuple{ 6,…».
  - **العربية المعيارية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/rationals.tex#L46)؛ الطبعة الدولية: [ص ٨٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=89) (ترقيم المتن: ٨٨)، [ص ٩٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=90) (ترقيم المتن: ٨٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٨٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=89) (ترقيم المتن: ٨٨)، [ص ٩٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=90) (ترقيم المتن: ٨٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وكما في الأعداد الصحيحة، نريد أيضًا تعريف بعض العمليات الأساسية. وحيث إن $\equivrep{i,j}{\Ratequiv}$ هي فئة التكافؤ بالنسبة إلى $\Ratequiv$ التي يكون $\tuple{i, j}$ !!a{element} فيها، نقول: \begin{align*} \equivrep{a, b}{\Ratequiv} + \equivrep{c, d}{\Ratequ…».

## عدد نسبي

الأصل الإنجليزي: `rational number`. معرّف القرار: `locale-ar-chosen-43722a16d72ec469`.

**المعنى المقصود:** عدد يمكن كتابته m/n حيث m,n صحيحان وn≠0؛ عنصر ℚ، في مقابل الصحيح والحقيقي وغير النسبي.

**سبب الاختيار:** مواضع OLP-0007 في اللغات الثلاث تربط ℚ بصيغة m/n ذات المقام غير الصفري وتستعمل المفرد والجمع «نسبي/نسبية» باتساق. لكن معجم دمشق يسجل rational number = «عدد منطق» لا «عدد نسبي». هذا تعارض اصطلاحي مباشر، لا خلل دلالي في الطبعة. أضيف شاهد العربية الكلاسيكية الذي كان غير مسجل.

**سؤال مفتوح:** أي المصطلحين ينبغي أن يكون الرأس لـ rational number في هذه الطبعة: «عدد نسبي» المتسق مع الاستعمال العربي الداخلي و«الأعداد النسبية»، أم «عدد منطق» المسجل في معجم دمشق؟ وإذا أبقينا «عدد نسبي»، فهل ينبغي ذكر «عدد منطق» مرادفًا تاريخيًا أو إقليميًا؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0007 — بعض المجموعات المهمة، وقوع ١:**
  - **الأصل:** [السطر ٢١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L21). الشاهد المسجل: «\shoveleft{\Rat = \Setabs{\nicefrac{m}{n}}{m, n \in \Int\text{ and }n \neq 0}}\\ \shoveright{\text{the set of rationals}}\\».
  - **الأصل:** [السطر ٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L29). الشاهد المسجل: «As we move through these sets, we are adding \emph{more} numbers to our stock. Indeed, it should be clear that $\Nat \subseteq \Int \subseteq \Rat \subseteq \Real$: after all, every natural number is an integer; every integer is a rational; and every ration…».
  - **العربية المعيارية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/important-sets.tex#L21)؛ الطبعة الدولية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=33) (ترقيم المتن: ٣٢) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=33) (ترقيم المتن: ٣٢) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\shoveleft{\Rat = \Setabs{\nicefrac{m}{n}}{m, n \in \Int\text{ و }n \neq 0}}\\ \shoveright{\text{مجموعة الأعداد النسبية}}\\».
  - **العربية المعيارية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/important-sets.tex#L29)؛ الطبعة الدولية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وعندما ننتقل من مجموعة إلى التي تليها في هذه القائمة، نضيف \emph{مزيدًا} من الأعداد إلى ما لدينا. وبالفعل، من الواضح أن $\Nat \subseteq \Int \subseteq \Rat \subseteq \Real$؛ فكل عدد طبيعي عدد صحيح، وكل عدد صحيح عدد نسبي، وكل عدد نسبي عدد حقيقي. ومن الواضح ب…».

## اختزال

الأصل الإنجليزي: `reducing`. معرّف القرار: `retro-0005-0050:emphasis:0abddf12718e685c`.

**المعنى المقصود:** تحويل حل مسألة تعداد إلى حل أخرى: من معدِّد لكائنات A يُبنى معدِّد لكائنات B، أي reduction بين مشكلتين.

**سبب الاختيار:** الموضعان يشرحان اتجاه الاختزال صراحة، فلا يراد تبسيط كسر. DAM يثبت «اختزال» لكنه يعرّفه لمعنى كسري مختلف؛ الدلالة هنا من شرح المصدر.

**سؤال مفتوح:** هل «اختزال مسألة» هو الاصطلاح المفضل في القابلية للعد، أم «ردّ/تحويل»؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0040 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ٢٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction-alt.tex#L28). الشاهد المسجل: «This is called \emph{reducing} one problem to another. In this case,».
  - **العربية المعيارية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/reduction-alt.tex#L28)؛ الطبعة الدولية: [ص ٨٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=82) (ترقيم المتن: ٨١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٨٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=82) (ترقيم المتن: ٨١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «يسمى هذا \emph{اختزال} مسألة إلى أخرى. وفي هذه الحالة نختزل مسألة».
  - **العربية التراثية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction-alt.tex#L19)؛ الطبعة التراثية: [ص ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=78) (ترقيم المتن: ٧٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وهذا \emph{اختزال} مسألة إلى أخرى؛ فقد رددنا تعداد $\Bin^\omega$ إلى تعداد $\Pow{\Nat}$. فحل المسألة الأخيرة، أعني تعداد $\Pow{\Nat}$، لو وجد لأمكن أن نستخرج منه حل الأولى، أعني تعداد $\Bin^\omega$.».
- **OLP-0034 — الاختزال، وقوع ٢:**
  - **الأصل:** [السطر ٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L27). الشاهد المسجل: «\emph{reducing} one problem to another---in this case, we reduce the».
  - **العربية المعيارية:** [السطر ٢٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/reduction.tex#L27)؛ الطبعة الدولية: [ص ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=73) (ترقيم المتن: ٧٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=73) (ترقيم المتن: ٧٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{اختزال} مسألة إلى أخرى---وفي هذه الحالة نختزل مسألة تعداد».
  - **العربية التراثية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction.tex#L17)؛ الطبعة التراثية: [ص ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=69) (ترقيم المتن: ٦٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «قد ثبت بالحجة القطرية أن $\Pow{\PosInt}$ !!{nonenumerable}، وكان قد سبق ثبوت ذلك لـ$\Bin^\omega$، أي مجموعة المتتاليات اللانهائية من~$0$ و~$1$، فهي !!{nonenumerable}. ويمكن أن نجعل النتيجة الثانية سبيلًا آخر إلى إثبات أن $\Pow{\PosInt}$ !!{nonenumerable}: ف…».

## الاختزال

الأصل الإنجليزي: `Reduction`. معرّف القرار: `retro-0005-0050:section:7e104384ad9ac4c1`.

**المعنى المقصود:** عنوان لقسم يعرض reduction بين مسألتي تعداد وكيف يولد حل إحداهما حل الأخرى.

**سبب الاختيار:** العنوان يلخص آلية نقل مشكلة إلى أخرى باتجاه محدد. DAM يثبت «اختزال» لفظًا لمعنى اختزال كسر؛ فهو سند لفظي لا شاهد للمعنى التخصصي.

**سؤال مفتوح:** هل يحتاج العنوان إلى «اختزال المسائل» لتجنب معنى الكسور؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0040 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ١١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction-alt.tex#L11). الشاهد المسجل: «\olsection{Reduction}».
  - **العربية المعيارية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/reduction-alt.tex#L11)؛ الطبعة الدولية: [ص ٨٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=82) (ترقيم المتن: ٨١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٨٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=82) (ترقيم المتن: ٨١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الاختزال}».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction-alt.tex#L11)؛ الطبعة التراثية: [ص ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=78) (ترقيم المتن: ٧٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الاختزال}».
- **OLP-0034 — الاختزال، وقوع ٢:**
  - **الأصل:** [السطر ١١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L11). الشاهد المسجل: «\olsection{Reduction}».
  - **العربية المعيارية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/reduction.tex#L11)؛ الطبعة الدولية: [ص ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=73) (ترقيم المتن: ٧٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=73) (ترقيم المتن: ٧٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الاختزال}».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction.tex#L11)؛ الطبعة التراثية: [ص ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=69) (ترقيم المتن: ٦٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الاختزال}».

## اختزال؛ اختزال تعداد B إلى تعداد A

الأصل الإنجليزي: `reduction; reduce enumeration of B to enumeration of A`. معرّف القرار: `locale-ar-chosen-b6f7133d8faecabf`.

**المعنى المقصود:** اختزال مسألة تعداد B إلى مسألة تعداد A: تحويل أي تعداد لـ A إلى تعداد لـ B بواسطة دالة شاملة A→B؛ ويكفي بصورة مكافئة حقن B→A لاستخراج تعداد B من تعداد A، فينتقل عدم قابلية B للتعداد إلى A.

**سبب الاختيار:** استُعيد الموضع الدلالي الصحيح في OLP-0034 وقُرئ كاملًا في اللغات الثلاث؛ وهو يصرح باتجاه المسألتين والدالة الشاملة A→B والحقن B→A والاستدلال العكسي من عدم قابلية B إلى عدم قابلية A. أما OLP-0679 فيستعمل reduction لاختزال صيغة في بحث البرهان، وOLP-0247 يستعمله لاختزال حسابي K→Tot؛ كلاهما شاهد صالح على اللفظ «اختزال» لكنه لا يسند تعليل اختزال التعداد. معجم دمشق يسجل reduction = «اختزال (اختصار)» في معنى رد الكسر، فيؤيد المقابل اللفظي العام فقط ولا يثبت معنى التعداد.

**سؤال مفتوح:** هل «اختزال مسألة تعداد B إلى مسألة تعداد A» هو التعبير العربي الأدق حين يكون المطلوب تحويل كل تعداد لـ A إلى تعداد لـ B بدالة شاملة A→B (أو استعمال حقن B→A)، أم تفضّلون «ردّ مسألة تعداد B إلى مسألة تعداد A» أو «تحويلها»؟ وهل اتجاه العبارة واضح بما يكفي لمنع قلب A وB؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0679 — في الاكتمال، وقوع ١:**
  - **الأصل:** [السطر ١٥٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/proof-search/completeness.tex#L153). الشاهد المسجل: «in~$C_n$ not already used in a reduction of $\lexists[x][!B(x)]$ on».
  - **العربية المعيارية:** [السطر ١٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/proof-theory/proof-search/completeness.tex#L144)؛ الطبعة الدولية: [ص ١١٠١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1101) (ترقيم المتن: ٨١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٠٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1102) (ترقيم المتن: ٨١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ثوابت في~$C_n$ ولم يُستعمل من قبل في اختزال~$\lexists[x][!B(x)]$ على».
  - **العربية التراثية:** [السطر ١٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/proof-search/completeness.tex#L143)؛ الطبعة التراثية: [ص ١٠٨٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1080) (ترقيم المتن: ٧٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ثوابت في~$C_n$ ولم يُستعمل من قبل في اختزال~$\lexists[x][!B(x)]$ على».
- **OLP-0247 — عدم قابلية تقرير الكلية، وقوع ٢:**
  - **الأصل:** [السطر ٥١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/computability/computability-theory/total.tex#L51). الشاهد المسجل: «$k$ is a reduction of $K$ to~$\fn{Tot}$.».
  - **العربية المعيارية:** [السطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/computability/computability-theory/total.tex#L50)؛ الطبعة الدولية: [ص ٤٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=473) (ترقيم المتن: ٤٧٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=474) (ترقيم المتن: ٤٧٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «خلاف ذلك. وبذلك تكون $k$ اختزالًا من $K$ إلى~$\fn{Tot}$.».
  - **العربية التراثية:** [السطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/computability/computability-theory/total.tex#L50)؛ الطبعة التراثية: [ص ٤٦٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=465) (ترقيم المتن: ٤٦٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن لم يكن. فهذه $k$ اختزال من $K$ إلى~$\fn{Tot}$.».

## الإغلاق الانعكاسي

الأصل الإنجليزي: `reflexive closure`. معرّف القرار: `retro-0005-0050:emphasis:85f7a2a303f7bb63`.

**المعنى المقصود:** العلاقة R∪Id_A الناتجة من ترتيب صارم بإضافة كل (x,x)، أي أصغر علاقة انعكاسية تحتوي R هنا.

**سبب الاختيار:** «الإغلاق الانعكاسي» يصف العملية بدقة. لكن DAM يستعمل «لصاقة» في transitive closure ولم يظهر reflexive closure؛ لذلك «اللصاقة الانعكاسية» منافس عائلي غير مثبت.

**سؤال مفتوح:** هل توحّد عائلة closure على «إغلاق» أم تتبع DAM في «لصاقة»؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L100). الشاهد المسجل: «x}$. (This is called the \emph{reflexive closure} of~$R$.)».
  - **العربية المعيارية:** [السطر ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L95)؛ الطبعة الدولية: [ص ٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=47) (ترقيم المتن: ٤٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=47) (ترقيم المتن: ٤٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الإغلاق الانعكاسي} لـ~$R$.) وبالعكس، يمكن البدء بترتيب جزئي والحصول».
  - **العربية التراثية:** [السطر ٨٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L88)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الإغلاق الانعكاسي} لـ~$R$. وبالعكس، حذف~$\Id{A}$ من ترتيب».

## الإغلاق الانعكاسي؛ إضافة قطر الهوية أو حذفه

الأصل الإنجليزي: `reflexive closure; add/remove identity diagonal`. معرّف القرار: `locale-ar-chosen-e5c3c39aeb9ff181`.

**المعنى المقصود:** تحويل ترتيب صارم R على A إلى ترتيب جزئي R⁺=R∪Id(A) بإضافة أزواج القطر، وبالعكس تحويل ترتيب جزئي إلى صارم بـ R⁻=R∖Id(A)، مع حفظ الخطية في الحالتين.

**سبب الاختيار:** قُرئ OLP-0016 كاملًا في اللغات الثلاث. لا يقتصر الشاهد على عبارة reflexive closure، بل يثبت الإضافة والحذف وصيغتي R⁺ وR⁻ وحفظ الخطية؛ لذلك وُسع الربط ليشمل الآلية كلها. لم يوجد reflexive closure رأسًا مطابقًا في معجم دمشق. وجد فقط transitive closure = «لصاقة متعدية»، وهو يفتح قياس «لصاقة انعكاسية» لكنه لا يشهده مباشرة. لذا تبقى «الإغلاق الانعكاسي» سليمة داخليًا لكن غير مثبتة من هذا الكانون.

**سؤال مفتوح:** ما الرأس الأنسب لـ reflexive closure في سياق العلاقات: «الإغلاق الانعكاسي» المستعمل في الطبعة، أم «اللصاقة الانعكاسية» قياسًا على transitive closure = «لصاقة متعدية» في معجم دمشق، أم «الغلق/الإقفال الانعكاسي»؟ وهل صياغة «إضافة قطر الهوية أو حذفه» واضحة في التعبير عن R⁺=R∪Id(A) وR⁻=R∖Id(A) مع حفظ الخطية؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L100). الشاهد المسجل: «x}$. (This is called the \emph{reflexive closure} of~$R$.)».
  - **العربية المعيارية:** [السطر ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L95)؛ الطبعة الدولية: [ص ٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=47) (ترقيم المتن: ٤٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=47) (ترقيم المتن: ٤٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الإغلاق الانعكاسي} لـ~$R$.) وبالعكس، يمكن البدء بترتيب جزئي والحصول».
  - **العربية التراثية:** [السطر ٨٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L88)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الإغلاق الانعكاسي} لـ~$R$. وبالعكس، حذف~$\Id{A}$ من ترتيب».

## الإغلاق الانعكاسي المتعدي

الأصل الإنجليزي: `reflexive transitive closure`. معرّف القرار: `retro-0005-0050:emphasis:cdf603600e974694`.

**المعنى المقصود:** العلاقة R*=R+∪Id_A: أصغر علاقة انعكاسية ومتعدية تحتوي R، أي مسارات بطول صفر أو أكثر.

**سبب الاختيار:** ترتيب الصفات في «الإغلاق الانعكاسي المتعدي» يحفظ الخاصيتين، والصيغة الرمزية تمنع الالتباس. لكن DAM يسمي transitive closure «لصاقة متعدية» ولا يقدم مدخلًا للعبارة المركبة.

**سؤال مفتوح:** هل «الإغلاق الانعكاسي المتعدي» مقبول رغم «لصاقة متعدية» في DAM؟

**كل وقوع مسجل لهذا القرار:**

- **OLP-0019 — عمليات على العلاقات، وقوع ١:**
  - **الأصل:** [السطر ٥٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L56). الشاهد المسجل: «The \emph{reflexive transitive closure} of $R$ is $R^* = R^+ \cup».
  - **العربية المعيارية:** [السطر ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/operations.tex#L56)؛ الطبعة الدولية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الإغلاق الانعكاسي المتعدي} لـ $R$ هو $R^* = R^+ \cup».
  - **العربية التراثية:** [السطر ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/operations.tex#L56)؛ الطبعة التراثية: [ص ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=49) (ترقيم المتن: ٤٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وأما \emph{الإغلاق الانعكاسي المتعدي} لـ$R$ فتعريفه $R^* = R^+ \cup».

## علاقة؛ علاقة ثنائية

الأصل الإنجليزي: `relation; binary relation`. معرّف القرار: `locale-ar-chosen-d851298d00cf65f2`.

**المعنى المقصود:** relation رأس عام؛ binary relation مجموعة من أزواج مرتبة محتواة في A×B مع ترميز Rxy أو xRy.

**سبب الاختيار:** فُحصت مجموعات الوقوع الست والثلاثون في النصوص الثلاثة. يحفظ «علاقة/علاقة ثنائية» الأزواج والترميز، ويثبت معجم دمشق binary relation = «علاقة ثنائية» بالتعريف نفسه. يبقى سؤال متى يجوز حذف «ثنائية» بعد تثبيت السياق.

**سؤال مفتوح:** هل تعتمدون relation = «علاقة» وbinary relation = «علاقة ثنائية»، مع جواز اختصار الثاني إلى «علاقة» بعد تعريف أن جميع العلاقات في الباب ثنائية؟ أم تفضّلون إبقاء «ثنائية» في كل موضع يمنع التباسها بعلاقات n-ية؟

**كل وقوع مسجل لهذا القرار:**


<!-- END PRESERVED REVIEW TEXT -->

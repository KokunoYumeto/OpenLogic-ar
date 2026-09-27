# بطاقات الاتحادات والتقاطعات — القرارات ١٠٠–١٠٧

[الرجوع إلى مقدمة الدفعة](README.md)

## الفرق

الأصل الإنجليزي: `Difference`. معرّف القرار: `retro-0005-0050:named-defn:5aa1d25a1ba73e95`.

**المعنى المقصود:** عنوان عملية فرق مجموعتين بالترتيب A\B: ما في A وليس في B، لا الفرق الحسابي ولا الفرق التناظري.

**سبب الاختيار:** يوثق المعجم مدخل «فرق مجموعتين» مباشرة ويظلل في الرسم منطقة A الخالية من B. أما عنوان «الفرق» فيعتمد على سياق المجموعات والرمز A\B لتخصيص المعنى؛ لا يدل لفظه وحده على جهة العملية. التعريف في الطبعات يحفظ شرط الانتماء إلى A وعدم الانتماء إلى B، فلا تُضاف عناصر B وحدها. مراجعة لاحقة لعنوان مختصر لا نقل حرفي لمدخل set difference.

**سؤال مفتوح:** هل يكفي عنوان «الفرق» عند تعريف A\B لتمييز فرق المجموعتين الموجَّه من الفرق الحسابي أو التناظري؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٥٥-١٦٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L155-L168) — يعرف A\B بما في A وليس في B وتبين الصورة الجهة.

**مواضع المعجم المعاينة:** [ص ٦٤٤ من PDF (المطبوعة ٦٣٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=644)

**حدود الشاهد المعجمي:** PDF ص ٦٤٤، المطبوعة ٦٣٢: set difference = «فرق مجموعتين»، مع تعريف ورسم لمنطقة A وحدها.

**بديل جدير بالمقارنة:** فرق المجموعتين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لصحة المعنى في التعريف، ومتوسطة لكفاية العنوان المختصر.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ١٦٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L162). الشاهد المسجل: «\begin{defn}[Difference]».
  - **العربية المعيارية:** [السطر ١٦٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L166)؛ الطبعة الدولية: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الفرق]».
  - **العربية التراثية:** [السطر ١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L158)؛ الطبعة التراثية: [ص ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=35) (ترقيم المتن: ٣٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الفرق]».

## متباينتين

الأصل الإنجليزي: `disjoint`. معرّف القرار: `retro-0005-0050:emphasis:050b9f86fe2fdeb3`.

**المعنى المقصود:** مجموعتان لا عناصر مشتركة بينهما، أي تقاطعهما خال؛ لا يكفي مجرد عدم تساويهما.

**سبب الاختيار:** النص الحالي «متباينتين» مربوط فورًا بشرط خلو التقاطع وبشرح عدم وجود عناصر مشتركة، ولذلك لم يظهر خلل في القضية الرياضية نفسها. لكن المعجم يثبت disjoint sets = «مجموعات منفصلة» بالمعنى نفسه، ولا يشهد في هذا المدخل لـ«متباينتين». أُبقي اللفظ المنشور قابلًا للعكس مع توصية لغوية مؤقتة بمقارنته بـ«منفصلتين» في دفعة تصحيح مصدر لاحقة؛ فكلا اللفظين إذا عُزل عن التعريف قد يوهم بمعنى أوسع.

**سؤال مفتوح:** في OLP-0008، أيهما أدق بجوار شرط التقاطع الخالي: «متباينتين» الحالية أم «منفصلتين» التي يسندها المعجم، من غير إيهام بالمغايرة فقط أو بالفصل الطوبولوجي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧١-٨٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L71-L83) — يضبط الأصل التباعد هنا بخلو التقاطع وعدم الاشتراك في أي عنصر.

**مواضع المعجم المعاينة:** [ص ١٩٦ من PDF (المطبوعة ١٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=196)

**حدود الشاهد المعجمي:** PDF ص ١٩٦، المطبوعة ١٨٤: disjoint sets = «مجموعات منفصلة»، وشرحها بأنها لا تحوي عناصر مشتركة؛ لم يرد «متباينتين» في هذا المدخل.

**بديل جدير بالمقارنة:** منفصلتين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لصحة الشرط الرياضي، ومنخفضة نسبيًا لاختيار الصفة الحالية أمام شاهد معجمي مخالف.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ٧٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L77). الشاهد المسجل: «Two sets are called \emph{disjoint} if their intersection is».
  - **العربية المعيارية:** [السطر ٧٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L76)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وتُسمّى مجموعتان \emph{متباينتين} إذا كان تقاطعهما».
  - **العربية التراثية:** [السطر ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L71)؛ الطبعة التراثية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فإن خلا التقاطع سميت المجموعتان \emph{متباينتين}؛ أي لا !!{element}s».

## تقاطع

الأصل الإنجليزي: `intersection`. معرّف القرار: `retro-0005-0050:emphasis:37ef90d155536e42`.

**المعنى المقصود:** تقاطع A وB هو مجموعة العناصر المشتركة فيهما؛ استعمال الاسم هنا نكرة في صدر التعريف.

**سبب الاختيار:** يثبت المعجم intersection = «تقاطع»، وفي معنى المجموعات يعرفه بجميع العناصر المشتركة. يرد في هذا الموضع «تقاطع» نكرة قبل تسمية A وB ثم تثبته صيغة x∈A ∧ x∈B؛ تنكير الاسم مقتضى السياق لا نص المعجم. لا يستعار هنا معنى تقاطع الخطوط الهندسي.

**سؤال مفتوح:** هل تنكير «تقاطع» في صدر التعريف طبيعي وواضح مع تثبيت الاسم المعجمي والمعنى المجموعاتي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧١-٧٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L71-L79) — يحدد التقاطع بانتماء العنصر إلى A وB معًا.

**مواضع المعجم المعاينة:** [ص ٣٧٠ من PDF (المطبوعة ٣٥٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=370)

**حدود الشاهد المعجمي:** PDF ص ٣٧٠، المطبوعة ٣٥٨: intersection = «تقاطع»، والمعنى الثاني تقاطع مجموعتين وعناصرهما المشتركة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للمعنى والمصطلح؛ أداة التعريف مسألة سياق.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ٧٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L72). الشاهد المسجل: «The \emph{intersection} of two sets $A$ and $B$, written $A \cap B$, is».
  - **العربية المعيارية:** [السطر ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L71)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تقاطع} مجموعتين $A$ و$B$، ويكتب $A \cap B$، هو مجموعة».
  - **العربية التراثية:** [السطر ٦٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L66)؛ الطبعة التراثية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تقاطع} $A$ و$B$، ورمزه $A \cap B$، مجموعة الأشياء التي هي من».

## التقاطع

الأصل الإنجليزي: `intersection`. معرّف القرار: `retro-0005-0050:emphasis:95aec41f60ae35ca`.

**المعنى المقصود:** العملية التي تعيد مجموعة العناصر المشتركة لمجموعتين؛ التعريف هنا إحالة إلى العملية الممهد لها.

**سبب الاختيار:** سبق شرح العملية ثم عاد النص إلى «التقاطع» معرفًا عند تصويرها. يثبت المعجم أصل اللفظ «تقاطع» في معنى المجموعات، ولا يقرر أداة التعريف في هذا السياق. يحتفظ الشرح بصورة العناصر المشتركة بدل تصور هندسي محض لنقطة التقاء مستقيمين.

**سؤال مفتوح:** هل التعريف في «التقاطع» مناسب للإحالة إلى العملية المذكورة قبل الرسم، وهل تبقى صورة العناصر المشتركة واضحة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٥٨-٦٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L58-L68) — يسمي العملية ويصف رسم منطقة اشتراك المجموعتين.

**مواضع المعجم المعاينة:** [ص ٣٧٠ من PDF (المطبوعة ٣٥٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=370)

**حدود الشاهد المعجمي:** PDF ص ٣٧٠، المطبوعة ٣٥٨، يثبت الاسم ومعنى العناصر المشتركة، لا صيغة التعريف السياقية.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المصطلح، ومتوسطة في التفضيل الأسلوبي بين المعرفة والنكرة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ٦٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L62). الشاهد المسجل: «\emph{intersection}, and can be depicted as in \olref{fig:intersection}.».
  - **العربية المعيارية:** [السطر ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L60)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «أيضًا. وتسمى هذه العملية \emph{التقاطع}، ويمكن تمثيلها كما في».
  - **العربية التراثية:** [السطر ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L57)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{التقاطع}، وصورتها في \olref{fig:intersection}.».

## التقاطع

الأصل الإنجليزي: `Intersection`. معرّف القرار: `retro-0005-0050:named-defn:f127e60a4c6019a6`.

**المعنى المقصود:** تقاطع A وB جميع ما ينتمي إليهما معًا: x∈A ∧ x∈B، ويجوز أن يكون خاليًا.

**سبب الاختيار:** العنوان «التقاطع» يوافق مدخل المعجم في معناه المجموعاتي، لا التقاطع الهندسي وحده. يحفظ تعريف العربية المعيارية «كل من» والتراثية «معًا» قيد الانتماء المزدوج، وتؤكده الصيغة الرمزية بعاطف الاقتران. يوضح المثال اللاحق إمكان خلو التقاطع. هذا تسويغ لاحق بمقابلة الأصل والمعجم، لا شهادة على استعمال تاريخي مخصوص.

**سؤال مفتوح:** هل تمنع عبارة «معًا» وشرط x∈A ∧ x∈B اللبس بين الاشتراك المجموعاتي والتقاطع الهندسي، مع قبول التقاطع الخالي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧١-٨٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L71-L83) — يعرّف التقاطع بالاشتراك في العضوية ويذكر خلوه عند الانفصال.

**مواضع المعجم المعاينة:** [ص ٣٧٠ من PDF (المطبوعة ٣٥٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=370)

**حدود الشاهد المعجمي:** PDF ص ٣٧٠، المطبوعة ٣٥٨، المعنى الثاني: تقاطع مجموعتين وعناصرهما المشتركة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية؛ المدخل والصيغة التعريفية متفقان.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ٧١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L71). الشاهد المسجل: «\begin{defn}[Intersection]».
  - **العربية المعيارية:** [السطر ٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L70)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[التقاطع]».
  - **العربية التراثية:** [السطر ٦٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L65)؛ الطبعة التراثية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[التقاطع]».

## فرق المجموعتين

الأصل الإنجليزي: `set difference`. معرّف القرار: `retro-0005-0050:emphasis:1a96d33e0bf888f1`.

**المعنى المقصود:** فرق A عن B مجموعة عناصر A غير المنتمية إلى B؛ يختلف عن B\A وعن الفرق التناظري.

**سبب الاختيار:** يستعمل المعجم «فرق مجموعتين» لـ set difference ويشرح الجهة بمنطقة A وحدها. «فرق المجموعتين» تعريف نحوي للمضاف إليه حين تكون A وB معلومتين. يحفظ المتن الرمز A\B وشرط x∈A وx∉B؛ ومن ثم لا تتبادل جهة الفرق بتبادل المجموعتين. ليس هذا فرقًا حسابيًا بين عددين.

**سؤال مفتوح:** هل تعين عبارة «فرق المجموعتين» والرمز A\B جهة الفرق، أم يحتاج أول ذكر إلى التصريح «ما في A دون B»؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٦٢-١٦٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L162-L168) — يذكر الجهة A\B وشرطي العضوية وعدمها.

**مواضع المعجم المعاينة:** [ص ٦٤٤ من PDF (المطبوعة ٦٣٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=644)

**حدود الشاهد المعجمي:** PDF ص ٦٤٤، المطبوعة ٦٣٢: set difference = «فرق مجموعتين» ورسم يظلل A غير المشتركة مع B.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للمعنى، ومتوسطة لوضوح الإضافة العربية وحدها من غير الرمز.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ١٦٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L163). الشاهد المسجل: «The \emph{set difference}~$A \setminus B$ is the set of all !!{element}s of».
  - **العربية المعيارية:** [السطر ١٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L167)؛ الطبعة الدولية: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{فرق المجموعتين}~$A \setminus B$ هو مجموعة جميع !!{element}s».
  - **العربية التراثية:** [السطر ١٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L159)؛ الطبعة التراثية: [ص ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=35) (ترقيم المتن: ٣٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{فرق المجموعتين}~$A \setminus B$ هو مجموعة جميع !!{element}s».

## الاتحاد

الأصل الإنجليزي: `Union`. معرّف القرار: `retro-0005-0050:named-defn:869825be5d192a42`.

**المعنى المقصود:** اتحاد A وB جميع ما ينتمي إلى A أو B أو إليهما معًا؛ لا يكرر العنصر المشترك.

**سبب الاختيار:** يوثق المعجم union = «اتحاد» ويضم في الرسم المنطقة المشتركة وغير المشتركة. يصرح تعريف الأصل والعربيتين بإدخال عناصر A وB أو كلتيهما، وتحفظ الصيغة x∈A ∨ x∈B عاطف «أو» الشامل. المثال المجاور لا يعد العنصر المشترك مرتين؛ فلا تُفهم عبارة الجمع في الشرح على أنها جمع عددي أو اتحاد متعدد النسخ. أداة التعريف في العنوان محلية لا منقولة حرفيًا عن المعجم.

**سؤال مفتوح:** هل يقرأ «الاتحاد» هنا بمعنى «أو» الشامل لكلتا المجموعتين، مع عدم تكرار العنصر المشترك، رغم استعمال «جمع» في الشرح؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٠-٥١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L30-L51) — يعرّف الاتحاد بعضوية A أو B أو كليهما ويعرض مثالًا للمجموعتين.

**مواضع المعجم المعاينة:** [ص ٧٥٤ من PDF (المطبوعة ٧٤٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=754)

**حدود الشاهد المعجمي:** PDF ص ٧٥٤، المطبوعة ٧٤٢: union = «اتحاد (اجتماع)» مع رسم يشمل منطقتي المجموعتين والتداخل.

**بديل جدير بالمقارنة:** اجتماع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية؛ المعجم والأصل يثبتان المعنى الشامل.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L34). الشاهد المسجل: «\begin{defn}[Union]».
  - **العربية المعيارية:** [السطر ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L33)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الاتحاد]».
  - **العربية التراثية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L30)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الاتحاد]».

## الاتحادات والتقاطعات

الأصل الإنجليزي: `Unions and Intersections`. معرّف القرار: `retro-0005-0050:section:2bafe98ac3a68350`.

**المعنى المقصود:** عنوان يجمع عمليتي الاتحاد والتقاطع على المجموعات.

**سبب الاختيار:** يسمي الأصل القسم Unions and Intersections ويعرّف العمليتين في الوحدة نفسها. يسجل المعجم union «اتحاد (اجتماع)» وintersection «تقاطع» في معنى المجموعات. «الاتحادات والتقاطعات» جمع معرف لهذين الاسمين، لا عبارة منقولة حرفيًا من مدخلي المعجم، ولا يحصر القسم في حالتي الاجتماع الهندسي للدوائر.

**سؤال مفتوح:** هل جمع الاسمين في «الاتحادات والتقاطعات» هو الأبين عنوانًا للعمليتين كما عرّفهما الأصل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٠-٤٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L10-L40)، [الأسطر ٥٨-٧٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L58-L79) — يمهد العنوان لتعريف الاتحاد والتقاطع بوصفهما عمليتين مجموعاتيتين.

**مواضع المعجم المعاينة:** [ص ٣٧٠ من PDF (المطبوعة ٣٥٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=370)، [ص ٧٥٤ من PDF (المطبوعة ٧٤٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=754)

**حدود الشاهد المعجمي:** PDF ص ٣٧٠ و٧٥٤، المطبوعتان ٣٥٨ و٧٤٢، تثبتان الاسمين المفردين في معنى المجموعات.

**بديل جدير بالمقارنة:** الاجتماعات والتقاطعات

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للأصل الاصطلاحي، ومتوسطة لصيغة الجمع الأسلوبية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحادات والتقاطعات، وقوع ١:**
  - **الأصل:** [السطر ١٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L10). الشاهد المسجل: «\olsection{Unions and Intersections}».
  - **العربية المعيارية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L10)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الاتحادات والتقاطعات}».
  - **العربية التراثية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L10)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الاتحادات والتقاطعات}».

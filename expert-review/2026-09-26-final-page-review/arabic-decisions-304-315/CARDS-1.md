# بطاقات التكميم والسلسلة الفارغة — القرارات ٣٠٤–٣٠٧

[الرجوع إلى مقدمة الدفعة](README.md)

## المكممان الكلي والوجودي المقيّدان

الأصل الإنجليزي: `bounded universal and existential quantifiers`. معرّف القرار: `locale-ar-chosen-33584af1745401ed`.

**المعنى المقصود:** المكممان الكلي والوجودي حين يقيّد المتغير x بالانتماء إلى A؛ لا يعني القيد أن A منتهية.

**سبب الاختيار:** يعطي الأصل التوسيعين: الكلي على A يستلزم الخاصية عند انتماء x إلى A، والوجودي على A يجمع الانتماء والخاصية. تحتفظ الطبعتان بالرمزين والصيغتين، فيصح وصفهما بالمقيّدين؛ القيد مجال المتغير لا حدّ عددي لحجم A. لم يخرج البحث المحدود في المعجم مدخلًا مباشرًا لـ restricted quantifier، فالتقرير رياضي سياقي لا توثيق اصطلاحي رسمي.

**سؤال مفتوح:** هل «المكممان الكلي والوجودي المقيّدان» أوضح من «المحصوران في A» لهذا التوسيع، مع عدم الإيحاء بأن A منتهية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٣-٦٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/subsets.tex#L63-L66) — تثبت الصيغتان في التعريف الفرق بين الشرط في الكلي والاقتران في الوجودي.

**نتيجة البحث المعجمي المحدود:** بحثنا في OCR هذا المعجم عن bounded/restricted quantifier وعن universal/existential quantifier ولم يظهر مدخل مباشر؛ لا يعني ذلك استقصاء كل المعاجم أو نفي وجود اصطلاح آخر. الصيغ الأصلية نفسها تثبت معنى التقييد.

**بديل جدير بالمقارنة:** المكممان المحصوران؛ قد يكون أبين لكنه يحتاج تحققًا من استعماله عند المختصين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى الصيغتين، متوسطة في اسم المصطلح غير المشهود مباشرة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0006 — المجموعات الجزئية والتكميم المقيد، وقوع ١:**
  - **الأصل:** [السطر ٦٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/subsets.tex#L63). الشاهد المسجل: «\begin{defn}\ollabel{forallxina} $(\forall x \in A)\phi$ abbreviates $\forall x(x \in A \lif \phi)$. Similarly, $(\exists x \in A)\phi$ abbreviates $\exists x(x \in A \land \phi)$.».
  - **العربية المعيارية:** [السطر ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/subsets.tex#L63)؛ الطبعة الدولية: [ص ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=32) (ترقيم المتن: ٣١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=32) (ترقيم المتن: ٣١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}\ollabel{forallxina} تختصر $(\forall x \in A)\phi$ العبارة $\forall x(x \in A \lif \phi)$. وبالمثل، تختصر $(\exists x \in A)\phi$ العبارة $\exists x(x \in A \land \phi)$.».
  - **العربية التراثية:** [السطر ٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/subsets.tex#L59)؛ الطبعة التراثية: [ص ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=32) (ترقيم المتن: ٣١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}\ollabel{forallxina} الرمز $(\forall x \in A)\phi$ اختصار لـ$\forall x(x \in A \lif \phi)$، وكذلك $(\exists x \in A)\phi$ اختصار لـ$\exists x(x \in A \land \phi)$.».

## كلا الأمرين

الأصل الإنجليزي: `both`. معرّف القرار: `retro-0005-0050:emphasis:319c70db8bf351e4`.

**المعنى المقصود:** قد تكون المجموعة نفسها عنصرًا في مجموعة أخرى ومجموعة جزئية منها في آن واحد؛ العلاقتان مستقلتان.

**سبب الاختيار:** أكد الأصل both ثم أعطى مثال {0}∈{0,{0}} و{0}⊆{0,{0}}. نقل «كلا الأمرين» التنسيق بين محمولَي العضوية والاحتواء ولم يحولهما إلى علاقة واحدة. المعجم يشرح عنصر المجموعة ومجموعة جزئية في مدخلين مختلفين؛ التوكيد البلاغي مستند إلى المثال لا إلى رأس معجمي.

**سؤال مفتوح:** هل «كلا الأمرين» طبيعي مع المحمولين اللاحقين، أم «الوصفان معًا» أدق في هذا السياق؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٥-٣٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/subsets.tex#L35-L39) — المثال اللاحق يثبت انتماء المجموعة واحتواءها معًا دون خلط.

**مواضع المعجم المعاينة:** [ص ٢١٤ من PDF (المطبوعة ٢٠٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=214)، [ص ٦٩٦ من PDF (المطبوعة ٦٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=696)

**حدود الشاهد المعجمي:** PDF ص ٢١٤ (المطبوعة ٢٠٢) يشرح العضوية x∈A، وص ٦٩٦ (المطبوعة ٦٨٤) يشرح subset بوصف احتواء جميع عناصر المجموعة الجزئية؛ لا يمليان لفظ «كلا الأمرين».

**بديل جدير بالمقارنة:** الوصفان معًا؛ أوضح حسابيًا لكنه أقل محافظة على بنية الأصل التعليمية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تمييز العلاقتين وصدق المثال، متوسطة في التوكيد الأسلوبي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0006 — المجموعات الجزئية والتكميم المقيد، وقوع ١:**
  - **الأصل:** [السطر ٣٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/subsets.tex#L37). الشاهد المسجل: «may happen to \emph{both} be !!a{element} and a subset of some other».
  - **العربية المعيارية:** [السطر ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/subsets.tex#L37)؛ الطبعة الدولية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «يحدث \emph{كلا الأمرين} لمجموعة ما: أن تكون !!a{element} وأن تكون مجموعة جزئية من».
  - **العربية التراثية:** [السطر ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/subsets.tex#L37)؛ الطبعة التراثية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الوصفان لمجموعة بالنسبة إلى أخرى، فيصدق عليها \emph{كلا الأمرين}: كونها».

## السلسلة الفارغة

الأصل الإنجليزي: `empty string`. معرّف القرار: `locale-ar-chosen-3785ffb8e8bf0b55`.

**المعنى المقصود:** السلسلة الفارغة Λ هي الكلمة الوحيدة التي طولها صفر، وتدخل في A* لكل أبجدية A؛ ليست الرمز 0 ولا السلسلة المكونة من أصفار.

**سبب الاختيار:** يعرض الأصل السلاسل على أبجدية A ثم يدرج Λ قبل 0 و00 في مثال الأبجدية الثنائية، وتفعل الطبعتان ذلك. لذا تحفظ «السلسلة الفارغة» اختلافها عن سلسلة رموز الصفر. لم يعثر البحث المعجمي المحدود عن empty string أو string على مدخل مباشر في المصدر المصور؛ إبقاء اللفظ قرار من التعريف والتمثيل مع سؤال خبير.

**سؤال مفتوح:** هل «السلسلة الفارغة» هو الأشيع في لغة الحوسبة العربية، أم «الكلمة الفارغة» أو «السلسلة الخالية» أوضح لهذا الرمز؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٧-٥٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L47-L54) — إدراج Λ منفصلة من 0 و00 يحدد معناها العددي البنيوي.

**نتيجة البحث المعجمي المحدود:** لم ينتج البحث في OCR معجم دمشق عن empty string أو string؛ لا نعمم الغياب على المعاجم الأخرى. يعتمد تمييز الصفر من السلسلة الخالية على مثال الأصل نفسه.

**بديل جدير بالمقارنة:** الكلمة الفارغة؛ قد تكون مألوفة في نظرية اللغات الشكلية؛ السلسلة الصفرية؛ مرفوضة لأنها قد تعني سلسلة أصفار

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تمييز Λ من 0، متوسطة في المفاضلة الاصطلاحية بين سلسلة وكلمة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0007 — المجموعات المهمة والسلاسل، وقوع ١:**
  - **الأصل:** [السطر ٤٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L49). الشاهد المسجل: «is a string over $A$. We include the \emph{empty string $\Lambda$}».
  - **العربية المعيارية:** [السطر ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/important-sets.tex#L49)؛ الطبعة الدولية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وندرج \emph{السلسلة الفارغة $\Lambda$} ضمن السلاسل على~$A$ لكل».
  - **العربية التراثية:** [السطر ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/important-sets.tex#L45)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{السلسلة الفارغة $\Lambda$} ضمن السلاسل على~$A$ لكل أبجدية~$A$. فمثلًا:».

## لا نهائية

الأصل الإنجليزي: `infinite`. معرّف القرار: `retro-0005-0050:emphasis:3a60d8ab3bab6856`.

**المعنى المقصود:** مجموعات لها عدد غير منته من العناصر؛ تشمل في المثال الطبيعية والصحيحة والنسبية والحقيقية.

**سبب الاختيار:** العبارة الإنجليزية glosses infinite بوجود عناصر بلا نهاية، وتعيد التراثية هذا الشرط في الجملة التالية. المعجم المصور يطبع «مجموعة غير منتهية (مجموعة لانهائية)»؛ «لا نهائية» في النص صورة مفصولة من الاسم الثاني وتوافق «مجموعات» في التأنيث.

**سؤال مفتوح:** هل تُبقى «لا نهائية» المفصولة، أم يوحّد الاصطلاح على «غير منتهية» أو الرسم المتصل في المعجم؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٦-٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L26-L27) — الأصل يشرح الصفة مباشرة بأنها كثرة عناصر لا تنتهي.

**مواضع المعجم المعاينة:** [ص ٣٥٩ من PDF (المطبوعة ٣٤٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=359)

**حدود الشاهد المعجمي:** PDF ص ٣٥٩ (المطبوعة ٣٤٧) يعرض infinite set = «مجموعة غير منتهية (مجموعة لانهائية)»؛ شاهد للمعنيين، لا للرسم المفصول الذي اختارته الطبعة.

**بديل جدير بالمقارنة:** غير منتهية؛ أول ما يورده المدخل وقد يكون أقل اختلافًا في الرسم

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى اللانهاية، متوسطة في رسم المركب الكتابي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0007 — المجموعات المهمة والسلاسل، وقوع ١:**
  - **الأصل:** [السطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L26). الشاهد المسجل: «These are all \emph{infinite} sets, that is, they each have».
  - **العربية المعيارية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/important-sets.tex#L26)؛ الطبعة الدولية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وهذه كلها مجموعات \emph{لا نهائية}، أي إن لكل منها عددًا».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/important-sets.tex#L25)؛ الطبعة التراثية: [ص ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=32) (ترقيم المتن: ٣١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وكل واحدة منها \emph{لا نهائية}؛ أي إن عدد !!{element}sها لا يتناهى.».

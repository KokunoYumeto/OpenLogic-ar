# بطاقات عمليات العلاقات — القرارات ١٦١–١٦٢

[الرجوع إلى مقدمة الدفعة](README.md)

## معكوس

الأصل الإنجليزي: `inverse`. معرّف القرار: `retro-0005-0050:emphasis:b5408b514dbf111e`.

**المعنى المقصود:** معكوس العلاقة R علاقة تقلب ترتيب كل زوج: يدخل الزوج (y,x) فيه إذا دخل (x,y) في R.

**سبب الاختيار:** تحدد صيغة الأصل R مرفوعة إلى الأس سالب واحد بتبديل موضعي عنصري الزوج، لا بقلب دالة عددية ولا بمعكوس ضرب. في التراثية اختصر الاسم إلى «معكوس» لاتصال الكلام بـR، وفي المعيارية «معكوس العلاقة» لرفع اللبس. المعجم يطبع inverse relation «علاقة عكسية» ويشرح تبديل الزوجين؛ فهو شاهد مباشر للمعنى لكنه لا يثبت لفظ «معكوس» بوصفه عنوان المدخل نفسه.

**سؤال مفتوح:** هل «معكوس» وحده في التراثية واضح بعد تسمية R علاقة، أم «العلاقة العكسية» أو «معكوس العلاقة» أوضح وأوثق؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٩-٢٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L19-L23) — يعرف العلاقة المعكوسة بتبديل الزوجين في صيغة مجموعة الأزواج.

**مواضع المعجم المعاينة:** [ص ٣٧٥ من PDF (المطبوعة ٣٦٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=375)

**حدود الشاهد المعجمي:** PDF ص ٣٧٥، المطبوعة ٣٦٣: inverse relation = «علاقة عكسية» مع تعريف انقلاب (x,y) إلى (y,x)؛ «معكوس» اسم منشور في الطبعتين لا نص المدخل المعجمي.

**بديل جدير بالمقارنة:** علاقة عكسية كما في المعجم؛ معكوس العلاقة كما في الصياغة المعيارية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لتطابق الصيغة والمعنى، ومتوسطة لاختيار الاسم العربي المختصر.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0019 — عمليات على العلاقات، وقوع ١:**
  - **الأصل:** [السطر ٢٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L22). الشاهد المسجل: «The \emph{inverse} of $R$ is $R^{-1} = \Setabs{\tuple{y, x}}{\tuple{x,».
  - **العربية المعيارية:** [السطر ٢٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/operations.tex#L22)؛ الطبعة الدولية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{معكوس العلاقة} $R$ هو $R^{-1} = \Setabs{\tuple{y, x}}{\tuple{x,».
  - **العربية التراثية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/operations.tex#L21)؛ الطبعة التراثية: [ص ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=49) (ترقيم المتن: ٤٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نسمّي \emph{معكوس} $R$ المجموعة $R^{-1} = \Setabs{\tuple{y, x}}{\tuple{x,».

## الإغلاق المتعدي

الأصل الإنجليزي: `Transitive closure`. معرّف القرار: `retro-0005-0050:named-defn:92fd4d95fc259dd1`.

**المعنى المقصود:** الإغلاق المتعدي R الموجب اتحاد قوى العلاقة من القوة الأولى فما فوق؛ يضم كل زوج تصله سلسلة غير خالية من خطوات R.

**سبب الاختيار:** يحفظ عنوان «الإغلاق المتعدي» صلة الاسم بالبناء R+ في الأصل، وهو اتحاد R للقوى الموجبة، ويتميز من الإغلاق الانعكاسي المتعدي R* الذي يضيف القطر. لكن المعجم المعاين يطبع transitive closure «لصاقة متعدية» لا «إغلاق متعدي»؛ فاسم الطبعة قرار اصطلاحي مؤقت لا شاهد معجمي مطابق. يبقى السؤال عن اللفظ الأفضل مفتوحًا مع الحفاظ على الصيغتين المختلفتين.

**سؤال مفتوح:** هل «إغلاق متعدي» هو الاصطلاح الأوضح والمتداول لهذا البناء، أم ينبغي اتباع «لصاقة متعدية» المعجمية أو توضيح العلاقة بين الاسمين؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٥٠-٥٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L50-L58) — يعرض العنوان وصيغة R+ ثم يميز R* بإضافة علاقة الهوية.

**مواضع المعجم المعاينة:** [ص ٧٣١ من PDF (المطبوعة ٧١٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=731)

**حدود الشاهد المعجمي:** PDF ص ٧٣١، المطبوعة ٧١٩: transitive closure = «لصاقة متعدية» مع شرح يضم R داخل العلاقة المتعدية الأصغر؛ لا يطبع المدخل «إغلاق متعدي».

**بديل جدير بالمقارنة:** لصاقة متعدية كما في معجم دمشق

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لحفظ الصيغة الرياضية، ومتوسطة للاسم المنشور المخالف للمدخل.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0019 — عمليات على العلاقات، وقوع ١:**
  - **الأصل:** [السطر ٥٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L50). الشاهد المسجل: «\begin{defn}[Transitive closure]Let $R \subseteq A^2$ be a binary relation.».
  - **العربية المعيارية:** [السطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/operations.tex#L50)؛ الطبعة الدولية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الإغلاق المتعدي]لتكن $R \subseteq A^2$ علاقة ثنائية.».
  - **العربية التراثية:** [السطر ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/operations.tex#L49)؛ الطبعة التراثية: [ص ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=49) (ترقيم المتن: ٤٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الإغلاق المتعدي]».

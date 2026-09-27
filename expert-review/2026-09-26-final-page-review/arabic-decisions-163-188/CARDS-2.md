# بطاقات تعريف الدالة وحدودها — القرارات ١٦٤–١٨٠

[الرجوع إلى مقدمة الدفعة](README.md)

## الدالة

الأصل الإنجليزي: `Function`. معرّف القرار: `retro-0005-0050:named-defn:71d030c0e3d552c0`.

**المعنى المقصود:** اسم حد الدالة الذي يسبق شرط إسناد قيمة واحدة في المجموعة المقابلة لكل عنصر من المجال.

**سبب الاختيار:** عنوان التعريف في الأصل Function، ويعقب العنوان مباشرة النص الرياضي الذي يقرن كل عنصر من A بعنصر من B. يعرض المعجم «دالة (تابع)» مع شرط التفرد، فاختيار الاسم المفرد «الدالة» يطابق وظيفة العنوان ولا يغير التعريف.

**سؤال مفتوح:** هل الأفضل إبقاء عنوان الحد «الدالة» وحده، مع ذكر «تابع» المعجمي في الشرح لا في رأس التعريف؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٨-٣٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L28-L36) — موضع التعريف الأصلي يحدد اسم الحد ونطاق شرط الإسناد الواحد.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** في PDF ص ٢٧٦، المطبوعة ٢٦٤، ورد المدخل function «دالة (تابع)»؛ أما تركيب عنوان الحد هنا فمن الأصل.

**بديل جدير بالمقارنة:** تابع؛ مرادف يذكره المعجم مع دالة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تسمية المفهوم، ومتوسطة في حذف المرادف من رأس الحد.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٢٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L28). الشاهد المسجل: «\begin{defn}[Function]».
  - **العربية المعيارية:** [السطر ٢٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L27)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الدالة]».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L25)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الدالة]».

## الدالة

الأصل الإنجليزي: `function`. معرّف القرار: `retro-0005-0050:emphasis:0a90740cea2155d1`.

**المعنى المقصود:** الدالة تعيين يحدد لكل عنصر من المجموعة الأولى عنصرًا واحدًا في الثانية، لا طريقة مخصوصة للحساب.

**سبب الاختيار:** يبدأ الأصل بوصف وظيفة الدالة ثم يثبت تعريفها بين A وB؛ والنصان العربيان يستعملان «الدالة» في الموضعين. يشرح المدخل المعجمي دالة بقانون الاقتران، ويجعل «تطبيق» اسمًا لعملية الإرسال، فلا يحول الفرق بين اللفظين الدالة إلى خوارزمية حسابية.

**سؤال مفتوح:** هل ينبغي إضافة «تابع» المعجمي عند أول ذكر، أم أن إبقاء «الدالة» يفصل بوضوح بين الكائن الرياضي و«التطبيق»؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٣-١٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L13-L16)، [الأسطر ٢٨-٣٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L28-L30) — يجمع موضعي الشرح والتعريف ليمنع قراءة الدالة على أنها طريقة حساب فحسب.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)، [ص ٤٤٤ من PDF (المطبوعة ٤٣٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=444)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يعرف function باسم «دالة (تابع)»، وص ٤٤٤ يطبع map وmapping باسم «تطبيق»؛ ولا يفرض ذلك مساواة المعنيين في كل سياق.

**بديل جدير بالمقارنة:** تابع؛ مرادف معجمي للدالة؛ تطبيق؛ أقرب إلى فعل التعيين لا اسم الدالة في هذا الحد

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في شرط القيمة الواحدة، ومتوسطة في المفاضلة بين الألفاظ المرادفة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ١٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L13). الشاهد المسجل: «A \emph{function} is a map which sends each !!{element} of a given set».
  - **العربية المعيارية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L13)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الدالة} تعيينٌ يرسل كل !!{element} من مجموعة معطاة».
  - **العربية التراثية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L13)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الدالة} تعيين يجعل لكل !!{element} من مجموعة معطاة».
- **OLP-0021 — أساسيات الدوال، وقوع ٢:**
  - **الأصل:** [السطر ٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L29). الشاهد المسجل: «A \emph{function} $f \colon A \to B$ is a mapping of each !!{element}».
  - **العربية المعيارية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L28)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الدالة} $f \colon A \to B$ تعيين يرسل كل !!{element}».
  - **العربية التراثية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L26)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الدالة} $f \colon A \to B$ تعيين يقابل كل !!{element}».

## صندوق أسود

الأصل الإنجليزي: `black box`. معرّف القرار: `retro-0005-0050:emphasis:408781f8c3650d9f`.

**المعنى المقصود:** الصندوق الأسود تشبيه للدالة حين لا يعتد إلا بقرن المدخل بالمخرج، بصرف النظر عن كيفية حسابه.

**سبب الاختيار:** يفسر الأصل تشبيه black box صراحة بأن المهم علاقة المدخل بالمخرج لا خوارزمية إنتاجه؛ وحفظت العربيتان الصورة البلاغية مع شرحها. مدخل function المعجمي يضبط الاقتران ولا يثبت هذا المجاز، فلم ننسب «صندوق أسود» إليه أو نجعل البحث المحدود برهانًا على غيابه من العربية.

**سؤال مفتوح:** هل يسهل «صندوق أسود» فهم المقصود في النثر التراثي، أم يستحسن شرح الاقتران أولًا وإبقاء التشبيه بعده؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٣-٢٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L23-L25) — الجملة الإنجليزية نفسها تحدد حدود التشبيه وتمنع توهم آلة مادية لازمة.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يشرح الدالة بالاقتران؛ لم يظهر black box في بحث OCR المحدود، ولا يثبت المدخل مجاز الصندوق.

**بديل جدير بالمقارنة:** تعيين مجرد؛ شرح للمعنى لكنه يحذف صورة الأصل البلاغية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى التجريد، ومتوسطة في مناسبة المجاز لسجل النثر التراثي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٢٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L23). الشاهد المسجل: «In this mathematical, abstract sense, a function is a \emph{black box}: what matters is only what output is paired with what input, not».
  - **العربية المعيارية:** [السطر ٢٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L22)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وفي هذا المعنى الرياضي المجرد، تكون الدالة \emph{صندوقًا أسود}: فلا يهم إلا أي مخرج يقترن بأي مدخل، لا الطريقة».
  - **العربية التراثية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L21)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فالدالة بهذا المعنى الرياضي المجرد \emph{صندوق أسود}:».

## مجال

الأصل الإنجليزي: `domain`. معرّف القرار: `retro-0005-0050:emphasis:496401a91343df20`.

**المعنى المقصود:** مجال الدالة التامة هو مجموعة المدخلات A، أما مجال الدالة الجزئية فهو الجزء من A الذي تكون قيمتها معرفة عليه.

**سبب الاختيار:** يستعمل الأصل domain في موضع الدالة التامة لمجموعة A كلها، ثم يعيد تحديده في الجزئية بمجموعة مواضع التعريف. أبقت العربيتان «مجال» في الحالين مع قيد الجزئية، فلا يسقط تغير النطاق. يسمي المعجم مدخل domain «ساحة، نطاق، منطقة، منطلق» في معان عدة، بينما يسمي codomain «مجالًا مقابلًا لدالة»؛ لذلك لا نقدم «مجال» بوصفه عنوان المدخل المعجمي الحرفي.

**سؤال مفتوح:** هل يظل «مجال» مناسبًا للدالة التامة والجزئية معًا، أم أن «ساحة التعريف» أدق في الجزئية عند مقابلة المصطلح المعجمي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢-٤٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L32-L44) — يحدد مجال الدالة التامة بأنه A في التعريف والرسم.؛ [الأسطر ٢٠-٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L20-L27) — يقصر مجال الدالة الجزئية على عناصر A التي تعرف عندها القيمة.

**وجه جمع المواضع:** موضعا الأصل يميزان بين مجموعة المدخلات كلها ومجموعة مواضع التعريف الفعلية.

**مواضع المعجم المعاينة:** [ص ٢٠٢ من PDF (المطبوعة ١٩٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=202)، [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)

**حدود الشاهد المعجمي:** PDF ص ٢٠٢، المطبوعة ١٩٠، يعطي domain وجوهًا منها «ساحة» في سياق الدالة؛ وص ١١٢، المطبوعة ١٠٠، يعطي codomain «مجالًا مقابلًا لدالة». الفرق بين المجال التام والجزئي مأخوذ من الأصل.

**بديل جدير بالمقارنة:** ساحة الدالة؛ مذكورة في شرح المعجم للمعنى الوظيفي؛ ساحة التعريف؛ توضح الجزئية لكنها ليست عنوان المدخل المعاين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في اختلاف المجالين رياضيًا، ومتوسطة في توحيد لفظ «مجال» عربيًا.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L26). الشاهد المسجل: «\emph{domain} of a partial function~$f$ is the subset of~$A$ where it».
  - **العربية المعيارية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L26)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مجال} الدالة الجزئية~$f$ فهو المجموعة الجزئية من~$A$ المؤلفة».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/partial-functions.tex#L25)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «و\emph{مجال} الجزئية~$f$ ما عُرّفت عليه من~$A$، أي».
- **OLP-0021 — أساسيات الدوال، وقوع ٢:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L32). الشاهد المسجل: «We call $A$ the \emph{domain} of~$f$ and $B$ the \emph{codomain}».
  - **العربية المعيارية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L31)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نسمي $A$ \emph{مجال}~$f$، ونسمي $B$ \emph{المجال المقابل}».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L29)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نسمي $A$ \emph{مجال}~$f$، و$B$ \emph{المجال المقابل} لـ~$f$.».
- **OLP-0021 — أساسيات الدوال، وقوع ٣:**
  - **الأصل:** [السطر ٤٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L44). الشاهد المسجل: «on the left represents the function's \emph{domain}; the ellipse on».
  - **العربية المعيارية:** [السطر ٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L43)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «على اليسار يمثل \emph{مجال} الدالة، والقطع الناقص على».
  - **العربية التراثية:** [السطر ٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L40)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مجال} الدالة، والأيمن \emph{مجالها المقابل}؛ والسهم ينتقل من».

## المجال المقابل

الأصل الإنجليزي: `codomain`. معرّف القرار: `retro-0005-0050:emphasis:6cb5cd42923c87f0`.

**المعنى المقصود:** المجال المقابل B هو المجموعة المصرح بأن قيم الدالة تقع فيها، وقد يكون أوسع من مداها الفعلي.

**سبب الاختيار:** يعين الأصل A مجالًا وB codomain ثم يعرف المدى جزءًا من B؛ فاختيار «المجال المقابل» يحفظ الفرق بين المجموعة المعلنة وصورة الدالة. يطبع المعجم codomain «مجالًا مقابلًا لدالة» بهذا المعنى، فلا تساوي الترجمة بين B والمدى.

**سؤال مفتوح:** هل «المجال المقابل» كافٍ لتمييز B من المدى عند القارئ، أم ينبغي إعادة كلمة «لدالة» عند أول حد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢-٤٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L32-L40) — التعريف الأصلي يضع المجال المقابل قبل تعريف المدى جزءًا منه.

**مواضع المعجم المعاينة:** [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)، [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ١١٢، المطبوعة ١٠٠، يطبع codomain «مجالًا مقابلًا لدالة»؛ وص ٥٩١ يميز المدى بمجموعة القيم المصابة.

**بديل جدير بالمقارنة:** مجال مقابل لدالة؛ صيغة المعجم الأطول عند أول تعريف

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المعنى والمقابلة الاصطلاحية؛ الاختصار الأسلوبي قابل للمراجعة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L32). الشاهد المسجل: «We call $A$ the \emph{domain} of~$f$ and $B$ the \emph{codomain}».
  - **العربية المعيارية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L31)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نسمي $A$ \emph{مجال}~$f$، ونسمي $B$ \emph{المجال المقابل}».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L29)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نسمي $A$ \emph{مجال}~$f$، و$B$ \emph{المجال المقابل} لـ~$f$.».

## وسائطها

الأصل الإنجليزي: `arguments`. معرّف القرار: `retro-0005-0050:emphasis:8ca3be8dd7f40b47`.

**المعنى المقصود:** وسائط الدالة هي عناصر مجالها التي تدخل في التعيين فتقابل كل واحدة منها قيمة محددة.

**سبب الاختيار:** يسمي الأصل عناصر A inputs أو arguments؛ وحفظت العربيتان لفظ المدخل ثم استعملتا «وسائطها» للمصطلح الثاني. لكن مدخل argument في صفحة المعجم المعاينة هو «سعة» في سياق العدد المركب، لا وسيطة الدالة؛ وصفحة function تتحدث عن متغير مستقل. لذلك تبقى «وسيطة» اختيارًا سياقيًا يحتاج شاهدًا رياضيًا عربيًا أوثق.

**سؤال مفتوح:** أيثبت استعمال «وسيطة الدالة» في كتب عربية معتمدة بهذا المعنى، أم أن «مدخل» أو «متغير مستقل» أوضح هنا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢-٣٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L32-L36) — الأصل يذكر المدخلات والوسائط معًا لعناصر المجال، فلا يجوز نقل الوسيطة إلى المجال المقابل.

**مواضع المعجم المعاينة:** [ص ٤٩ من PDF (المطبوعة ٣٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=49)، [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٤٩، المطبوعة ٣٧، يعطي argument «سعة» ويحيل إلى amplitude في معنى آخر؛ وص ٢٧٦ يسمي x متغيرًا مستقلًا. لا يشهد أيهما وحده للفظ «وسيطة» في هذا الحد.

**بديل جدير بالمقارنة:** مدخلات؛ مذكورة أصلًا مرادفًا سياقيًا؛ متغيرات مستقلة؛ وصف يرد في شرح المعجم للدالة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في دور عناصر A، ومنخفضة نسبيًا في إثبات لفظ «وسيطة» من المعجم المعاين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L33). الشاهد المسجل: «of~$f$. The !!{element}s of~$A$ are called inputs or \emph{arguments}».
  - **العربية المعيارية:** [السطر ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L32)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لـ~$f$. وتسمى !!{element}s~$A$ مدخلات~$f$ أو \emph{وسائطها}،».
  - **العربية التراثية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L30)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «و!!{element}s~$A$ مدخلات~$f$، أو \emph{وسائطها}. أما !!{element}».

## قيمة~$f$

الأصل الإنجليزي: `value of $f$`. معرّف القرار: `retro-0005-0050:emphasis:4d940209518dc882`.

**المعنى المقصود:** قيمة الدالة f عند الوسيطة x هي عنصر B الذي تقرنه به، ويرمز إليه بالتعبير f(x).

**سبب الاختيار:** يعرف الأصل value of f for argument x ويثبت الرمز f(x)، فأبقت العربيتان الإضافة «قيمة f» بدل تعميمها إلى مدى الدالة كله. يميز المعجم في تعريف function بين ساحة الدالة ومجموعة قيمها، وفي مدخل image بين صورة عنصر وصورة مجموعة؛ فالقيمة المفردة هنا ليست مجموعة الصور.

**سؤال مفتوح:** هل يكفي «قيمة f عند x» للقارئ من غير تكرار «الدالة»، وهل ينبغي وصلها صراحة بلفظ «صورة x» المعجمي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٣-٤٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L33-L40) — النص يثبت الوسيطة وقيمتها المفردة ورمزها، ثم يميز المدى بوصفه مجموعة القيم.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)، [ص ٣٤٧ من PDF (المطبوعة ٣٣٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=347)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يصف قيم الدالة، وص ٣٤٧، المطبوعة ٣٣٥، يسمي image «صورة» للعنصر وللمجموعة؛ لا يسوي ذلك بين القيمة المفردة والمدى.

**بديل جدير بالمقارنة:** صورة x؛ اصطلاح معجمي قريب لكنه يحتاج ضبطًا عند الانتقال إلى صورة مجموعة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المعنى والرمز، ومتوسطة في المفاضلة بين قيمة وصورة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L35). الشاهد المسجل: «by~$f$ is called the \emph{value of~$f$} for argument~$x$,».
  - **العربية المعيارية:** [السطر ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L34)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{قيمة~$f$} عند الوسيطة~$x$،».
  - **العربية التراثية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L31)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «من~$B$ المقابل للوسيطة~$x$ بواسطة~$f$ فهو \emph{قيمة~$f$} عند~$x$،».

## المدى

الأصل الإنجليزي: `range`. معرّف القرار: `retro-0005-0050:emphasis:6702c5a0d4f531d2`.

**المعنى المقصود:** مدى الدالة هو مجموعة قيمها المتحققة، أي صورة مجالها، وهو جزء من مجالها المقابل.

**سبب الاختيار:** يفصل الأصل range عن codomain ويكتبه مجموعة القيم f(x) حيث x في A. صفحة المعجم تسمي range «مدى» وتعطي المعنى نفسه للدالة؛ لذلك يحفظ اختيار «المدى» الفرق اللازم لمسائل الشمول في القسم التالي.

**سؤال مفتوح:** هل يلزم عند أول تعريف التصريح بأن المدى هو «صورة المجال» أيضًا لتجنب مساواته بالمجال المقابل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٨-٤٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L38-L40) — معادلة المدى في الأصل تحدد المجموعة التي ستقارن لاحقًا بالمجال المقابل.

**مواضع المعجم المعاينة:** [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)، [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)

**حدود الشاهد المعجمي:** PDF ص ٥٩١، المطبوعة ٥٧٩، يطبع range «مدى» ويصف قيم الدالة المتحققة؛ وص ١١٢ يحدد codomain مجموعة قد تتسع لها.

**بديل جدير بالمقارنة:** صورة الدالة؛ شرح ممكن لا يحل محل «المدى» في عنوان الحد

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في مطابقة المصطلح والمعنى الرياضي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L38). الشاهد المسجل: «The \emph{range} $\ran{f}$ of~$f$ is the subset of the codomain».
  - **العربية المعيارية:** [السطر ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L37)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن \emph{المدى} $\ran{f}$ للدالة~$f$ هو المجموعة الجزئية من المجال المقابل».
  - **العربية التراثية:** [السطر ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L34)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «و\emph{المدى} $\ran{f}$ للدالة~$f$ جزئية المجال المقابل».

## مجالها المقابل

الأصل الإنجليزي: `codomain`. معرّف القرار: `retro-0005-0050:emphasis:afafeb4db9c2724e`.

**المعنى المقصود:** في الرسم التوضيحي يمثل القطع الناقص الأيمن المجال المقابل للدالة، وليس بالضرورة مدى قيمها.

**سبب الاختيار:** يعين الأصل الشكل الأيسر مجالًا والأيمن codomain، ثم يسير السهم من وسيطة إلى قيمة؛ فحفظت الطبعة التراثية الإضافة «مجالها المقابل» لتربط الرسم بالدالة المعينة. يؤيد المعجم اسم المجال المقابل ويبين أن مجموعة القيم قد تكون أصغر، فلا تصح تسمية الشكل الأيمن مدى بلا قيد.

**سؤال مفتوح:** هل «مجالها المقابل» أوضح من «المجال المقابل» في وصف الشكل، أم يشتت الضمير عن اسم المصطلح؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٣-٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L43-L47) — وصف الرسم الإنجليزي يحدد وظيفة الشكل الأيمن مستقلة عن السهم الذي يحدد القيمة.

**مواضع المعجم المعاينة:** [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)

**حدود الشاهد المعجمي:** PDF ص ١١٢، المطبوعة ١٠٠، يسمي codomain «مجالًا مقابلًا لدالة» ويصف اشتماله على القيم، وربما زيادته عليها.

**بديل جدير بالمقارنة:** المجال المقابل؛ الصيغة الاصطلاحية المجردة في التعريف

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تمييز الشكل عن المدى، ومتوسطة في اختيار الضمير.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٤٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L45). الشاهد المسجل: «the right represents the function's \emph{codomain}; and an arrow».
  - **العربية المعيارية:** [السطر ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L44)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «اليمين يمثل \emph{مجالها المقابل}، ويشير السهم».
  - **العربية التراثية:** [السطر ٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L40)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مجال} الدالة، والأيمن \emph{مجالها المقابل}؛ والسهم ينتقل من».

## وسيطة

الأصل الإنجليزي: `argument`. معرّف القرار: `retro-0005-0050:emphasis:b208dbdb9ef39f91`.

**المعنى المقصود:** الوسيطة في الرسم عنصر من مجال الدالة ينطلق منه السهم إلى قيمته في المجال المقابل.

**سبب الاختيار:** موضع argument في الأصل هو مبتدأ السهم لا غايته، وعبارة الطبعة «وسيطة في المجال» تحفظ هذا الاتجاه. صفحة المعجم تعطي argument معنى «سعة» غير المطابق لهذا الرسم، وصفحة function تستعمل المتغير المستقل؛ لذا فالتعليل الرياضي ثابت من الأصل، أما اللفظ فيظل للمراجعة الاصطلاحية.

**سؤال مفتوح:** هل يفضل في شرح الرسم «مدخل» لتكون جهة السهم بديهية، أم «وسيطة» مع التعريف السابق؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٣-٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L43-L47) — الجملة الأصلية تنقل السهم من argument في المجال إلى value في المقابل.

**مواضع المعجم المعاينة:** [ص ٤٩ من PDF (المطبوعة ٣٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=49)، [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٤٩ لا يشهد لمدخل الدالة بل لسعة العدد، وص ٢٧٦ يشرح المتغير المستقل؛ ولا نزعم أن المعجم يطبع «وسيطة» هنا.

**بديل جدير بالمقارنة:** مدخل؛ يظهر مرادفًا في الأصل نفسه وفي التعريف العربي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في اتجاه السهم، ومتوسطة في لفظ الوسيطة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٤٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L46). الشاهد المسجل: «points from an \emph{argument} in the domain to the corresponding».
  - **العربية المعيارية:** [السطر ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L45)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «من \emph{وسيطة} في المجال إلى».
  - **العربية التراثية:** [السطر ٤١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L41)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{وسيطة} في المجال إلى \emph{قيمتها} الموافقة في المجال المقابل.».

## قيمتها

الأصل الإنجليزي: `value`. معرّف القرار: `retro-0005-0050:emphasis:1bfd961390745b0f`.

**المعنى المقصود:** القيمة المصورة هي مخرج واحد تقابله وسيطة بعينها، لا مجموعة القيم كلها.

**سبب الاختيار:** يقابل الأصل argument بـvalue في شرح السهم الواحد، فاستعملت التراثية «قيمتها» مع ضمير يعود إلى الوسيطة. يشرح المعجم صورة العنصر في مدخل image، ويفصل مدخل range مجموعة القيم؛ ومن ثم لا تختلط القيمة المفردة بالمدى.

**سؤال مفتوح:** هل «قيمتها» ذات الضمير أوضح في الشكل من «القيمة المناظرة»، أم يحتاج المرجع إلى تسمية الوسيطة مجددًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٣-٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L43-L47) — السهم في الأصل يربط مدخلًا مفردًا بقيمة مفردة في المجال المقابل.

**مواضع المعجم المعاينة:** [ص ٣٤٧ من PDF (المطبوعة ٣٣٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=347)، [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ٣٤٧ يفرق صورة العنصر وصورة المجموعة، وص ٥٩١ يعطي المدى مجموعة قيم الدالة؛ وهذا يدعم التفريق لا اختيار الضمير الأسلوبي.

**بديل جدير بالمقارنة:** القيمة المناظرة؛ صيغة الطبعة المعيارية من غير ضمير

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المعنى، ومتوسطة في الصياغة التراثية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L47). الشاهد المسجل: «\emph{value} in the codomain.».
  - **العربية المعيارية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L46)؛ الطبعة الدولية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{القيمة} المناظرة في المجال المقابل.».
  - **العربية التراثية:** [السطر ٤١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L41)؛ الطبعة التراثية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{وسيطة} في المجال إلى \emph{قيمتها} الموافقة في المجال المقابل.».

## بأن للعدد الصحيح الموجب جذرين

الأصل الإنجليزي: `each positive integer has two square roots`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0021-TWO-ROOTS-NOTE-20260907`.

**المعنى المقصود:** لكل عدد صحيح موجب جذران حقيقيان متضادان؛ لكن اختيار الجذر الرئيسي دالة على الطبيعيّات تشمل الصفر، فيلزم وصفه بغير السالب.

**سبب الاختيار:** النص الإنجليزي يقول بحق إن للموجب جذرين، ثم يسمي اختيار الجذر الموجب دالة من الطبيعيّات إلى الحقيقيّات، مع أن الجذر عند الصفر صفر لا موجب. حفظت العربيتان دعوى الجذرين للموجب وصححتا وصف الاختيار إلى «غير السالب»، وصرحت التراثية بالعلة في تنبيه. لا يقدم مدخل الدالة المعجمي هذا التصويب؛ دليله تعريف الأصل للمدخل واحتواؤه الصفر.

**سؤال مفتوح:** هل التنبيه العربي المضاف واضح في فصل تصويب الجذر الرئيسي عند الصفر عن العبارة الصحيحة الخاصة بالجذرين لكل موجب؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٤-٧٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L64-L72) — المثال الأصلي يذكر الطبيعيّات والجذرين للموجب والاختيار الموجب، فتظهر عند الصفر علة التصويب.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يثبت أن الدالة تعطي لكل مدخل قيمة وحيدة؛ ولا يحسم المدخل لفظ الجذر الرئيسي. التصويب الرياضي مأخوذ من المثال الأصلي وصفر الطبيعيّات في العمل.

**بديل جدير بالمقارنة:** الجذر الرئيسي؛ اسم يرد مع وصف غير السالب في الطبعة المعيارية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في ضرورة غير السالب عند الصفر، ومتوسطة في طول التنبيه التحريري.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ٦٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L68). الشاهد المسجل: «that $x^2 = n$ is not functional, since each positive integer~$n$ has two square roots: $\sqrt{n}$ and~$-\sqrt{n}$. We can make it functional by».
  - **العربية المعيارية:** [السطر ٧٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L76)؛ الطبعة الدولية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: ««الجذر غير السالب (الرئيسي)»؛ ولا يمس هذا التصويب القول السابق بأن للعدد الصحيح الموجب جذرين.».
  - **العربية التراثية:** [السطر ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L68)؛ الطبعة التراثية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الرئيسي. وأما كون العدد الصحيح الموجب ذا جذرين فباق على حاله.».

## تحسب g العدد السابق للعدد اللاحق للعدد اللاحق لـ x،

الأصل الإنجليزي: `predecessor of the successor of the successor`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0021-CLASSICAL-SUCCESSOR-CONSTRUCTION-20260907`.

**المعنى المقصود:** الدالة g(x)=x+2-1 تأخذ لاحق لاحق x ثم سابقه، فيكون الناتج x+1 كالدالة f.

**سبب الاختيار:** يسمي الأصل أولًا الوسيطة n ثم يرجع إلى x وهو اسمها في التعريف؛ وحدت الطبعة التراثية الاسم على x وأبقت ثلاث خطوات اللاحق واللاحق والسابق، لا مجرد النتيجة الجبرية. مدخل predecessor المعجمي «سابق» ويورد «لاحق» مقابله، لكن ترتيب الخطوات وحفظ القيمة مأخوذان من الأصل.

**سؤال مفتوح:** هل الصياغة التراثية «السابق لللاحق لللاحق» تبين تركيب الخطوات بالترتيب المقصود، أم يلزم تقديم شرح حسابي قصير قبلها؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٠٢-١٠٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L102-L108) — المثال الأصلي يصرح بخطوات الحساب ويحتوي تبديل الاسم n إلى x الذي أصلحته الطبعة.

**مواضع المعجم المعاينة:** [ص ٥٥٨ من PDF (المطبوعة ٥٤٦)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=558)

**حدود الشاهد المعجمي:** PDF ص ٥٥٨، المطبوعة ٥٤٦، يطبع predecessor «سابق» ويذكر successor «لاحق» في شرحه؛ لا يقرر ترتيب هذه الدالة المركبة.

**بديل جدير بالمقارنة:** تبسيط التعبير إلى x+1 فقط؛ يضيع غرض المثال في اختلاف طريقتي التعريف

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الحساب وتوحيد الاسم، ومتوسطة في سلاسة العبارة العربية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ١٠٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L103). الشاهد المسجل: «Let $g \colon \Nat \to \Nat$ be defined such that $g(x) = x+2-1$. This tells us that $g$ is a function which takes in natural numbers and outputs natural numbers. Given a natural number~$n$, $g$ will output the predecessor of the successor of the successor…».
  - **العربية التراثية:** [السطر ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L94)؛ الطبعة التراثية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «تحسب~$g$ العدد السابق للعدد اللاحق للعدد اللاحق لـ~$x$،».

## التعريف

الأصل الإنجليزي: `definitions`. معرّف القرار: `retro-0005-0050:emphasis:89f5e07df8194bf8`.

**المعنى المقصود:** التعريفان معادلتان مختلفتان تحددان التعيين نفسه للدالتين f وg على المجال والمجال المقابل نفسيهما.

**سبب الاختيار:** يوضح الأصل الفرق بين وسيلتي التعريف ومساواة الدالتين إذا تساوت قيمهما لكل وسيطة مع اتحاد المجال والمجال المقابل. اختارت التراثية المفرد «التعريف» للجنس حيث تستعمل المعيارية المثنى، وأبقت بعدها شرط الاتحاد؛ مدخل function المعجمي يحدد الدالة بالاقتران لكنه لا يحكم المفرد والمثنى في هذا السياق.

**سؤال مفتوح:** هل قول «مختلفتان في التعريف» أفصح هنا من «لهما تعريفان مختلفان»، أم يوهم أن لكل منهما تعريفًا واحدًا مشتركًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١١٠-١٢٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L110-L120) — المقطع الأصلي يجمع اختلاف صيغتي التعريف مع مبدأ مساواة الدوال امتداديًا.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يعرف function بقانون الإقران، ولا يتناول المفاضلة الأسلوبية بين مفرد التعريف ومثناه.

**بديل جدير بالمقارنة:** تعريفان مختلفان؛ عبارة الطبعة المعيارية وأقرب إلى جمع الأصل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المعنى، ومتوسطة في اختيار الصيغة المفردة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ١١٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L112). الشاهد المسجل: «\emph{definitions}. However, these are the \emph{same function}. After».
  - **العربية المعيارية:** [السطر ١٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L121)؛ الطبعة الدولية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تعريفان} مختلفان. غير أنهما \emph{الدالة نفسها}. ففي».
  - **العربية التراثية:** [السطر ١٠٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L104)؛ الطبعة التراثية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فـ$f$ و$g$ مختلفتان في \emph{التعريف}، ولكنهما \emph{دالة واحدة}.».

## دالة واحدة

الأصل الإنجليزي: `same function`. معرّف القرار: `retro-0005-0050:emphasis:5f1fba20046eccaa`.

**المعنى المقصود:** الدالتان f وg دالة واحدة في المعنى الامتدادي إذا اتحد المجال والمجال المقابل وتساوت القيمة عند كل مدخل.

**سبب الاختيار:** رغم اختلاف المعادلتين يثبت الأصل f(n)=g(n) لكل طبيعي ثم يشترط المجالين نفسيهما؛ لذا تقول التراثية «دالة واحدة» ولا تجعل اختلاف وصف الحساب اختلافًا في الكائن الرياضي. مدخل function المعجمي يركز الاقتران نفسه، لكن شرط المساواة التفصيلي ثابت من الأصل لا من مجرد المدخل.

**سؤال مفتوح:** هل تكفي عبارة «دالة واحدة» بعد بيان تساوي القيم والمجالين، أم الأوضح «الدالة نفسها» كما في المعيارية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١١٠-١٢٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L110-L120) — البرهان الأصلي لا يكتفي بالمساواة العددية بل يذكر اتحاد المجال والمجال المقابل.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)، [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يعرف الدالة بربط مدخل بقيمة، وص ١١٢ يبين المجال المقابل؛ مساواة دالتين من الشروط المنصوصة في الأصل.

**بديل جدير بالمقارنة:** الدالة نفسها؛ صياغة المعيارية مع حفظ المعنى

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية رياضيًا، ومتوسطة في وقع التركيب التراثي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ١١٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L112). الشاهد المسجل: «\emph{definitions}. However, these are the \emph{same function}. After».
  - **العربية المعيارية:** [السطر ١٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L121)؛ الطبعة الدولية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تعريفان} مختلفان. غير أنهما \emph{الدالة نفسها}. ففي».
  - **العربية التراثية:** [السطر ١٠٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L104)؛ الطبعة التراثية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=51) (ترقيم المتن: ٥٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فـ$f$ و$g$ مختلفتان في \emph{التعريف}، ولكنهما \emph{دالة واحدة}.».

## امتدادية الدوال

الأصل الإنجليزي: `extensionality for functions`. معرّف القرار: `locale-ar-chosen-170be3a705ec13f3`.

**المعنى المقصود:** امتدادية الدوال مبدأ يجعل تساوي قيم دالتين عند كل مدخل كافيًا لمساواتهما إذا اتحد مجالهما ومجالهما المقابل.

**سبب الاختيار:** يسمي الأصل principle of extensionality for functions ثم يعرض الشرط الرمزي ويقيده باتحاد المجال والمجال المقابل؛ فحفظت العربيتان «امتدادية» والقيد، ولم تختزلا المبدأ إلى تشابه الصيغ. لم يعثر بحث OCR المحدود في المعجم على extensionality، ومدخل function العام لا يثبت اللفظ؛ لذلك يعد الاسم هنا اختيارًا مؤقتًا مستمد المعنى من الأصل.

**سؤال مفتوح:** ما المصطلح العربي الموثق الأنسب لامتدادية الدوال، وهل تحتاج العبارة توضيح الفرق بين تساوي القيم واتحاد المجال المقابل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١١٠-١٢٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L110-L120) — الجملة والرمز وشرط المجالين في الأصل هي حدود المبدأ الذي سمي بالعربية.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)، [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يشرح الدالة، وص ١١٢ يحدد المجال المقابل؛ لا يثبت هذان المدخلان لفظ امتدادية، ولم يظهر extensionality في البحث المحدود بهذا المعجم.

**بديل جدير بالمقارنة:** مبدأ تساوي الدوال بالقيم؛ شرح رياضي لا اسم اصطلاحي موثق في الشاهد المعاين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في مضمون الشرط، ومنخفضة نسبيًا في توثيق اسم المبدأ العربي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ١١٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L110). الشاهد المسجل: «\begin{explain} We just considered two functions, $f$ and $g$, with different \emph{definitions}. However, these are the \emph{same function}. After all, for any natural number~$n$, we have that $f(n) = n+1 = n+2-1 = g(n)$. Otherwise put: our definitions fo…».
  - **العربية المعيارية:** [السطر ١١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L119)؛ الطبعة الدولية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=53) (ترقيم المتن: ٥٢)، [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=53) (ترقيم المتن: ٥٢)، [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{explain} نظرنا للتو في دالتين، $f$ و$g$، لهما \emph{تعريفان} مختلفان. غير أنهما \emph{الدالة نفسها}. ففي النهاية، لكل عدد طبيعي~$n$، لدينا $f(n) = n+1 = n+2-1 = g(n)$. وبعبارة أخرى: يحدد تعريفانا للدالتين~$f$ و~$g$ التعيين نفسه بواسطة معادلتين مختلفت…».

## تعريف بحسب الحالات؛ حالات مستنفدة ومتنافية

الأصل الإنجليزي: `definition by cases; exhaustive and exclusive cases`. معرّف القرار: `locale-ar-chosen-1fbb1a665996d399`.

**المعنى المقصود:** تعريف الدالة بحسب الحالات يحدد لكل مدخل حالة واحدة بالضبط؛ فيجب أن تستوعب الحالات جميع المدخلات وألا تتداخل.

**سبب الاختيار:** يعطي الأصل مثال الزوجي والفردي ويطالب ببرهان الاستيفاء والتنافي عند الحاجة. صاغت التراثية «التفصيل بحسب الحالات» وأبقت الشرطين، فلا يكفي أن تعطي كل حالة قيمة صحيحة من غير إثبات أن كل مدخل يقع في واحدة فقط. مدخل function المعجمي يثبت شرط القيمة الواحدة ولا يشرح طريقة الحالات، فلا ننسب إليه اسم هذه الطريقة.

**سؤال مفتوح:** هل «التفصيل بحسب الحالات» أليق بالسجل التراثي من «تعريف بحسب الحالات»، وهل يظهر للقارئ لزوم الاستيفاء والتنافي معًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٢٣-١٣٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L123-L137) — الفقرة الأصلية تعرض المثال ثم تذكر الشرطين والبرهان المطلوب لهما صراحة.

**مواضع المعجم المعاينة:** [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٢٧٦ يشرح تفرد قيمة الدالة فقط؛ لم يظهر في البحث المحدود مدخل مطابق لعبارة تعريف الدالة بحسب الحالات.

**بديل جدير بالمقارنة:** تعريف بحسب الحالات؛ صيغة المعيارية الأقرب إلى لفظ الأصل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الشرطين الرياضيين، ومتوسطة في الصياغة التراثية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0021 — أساسيات الدوال، وقوع ١:**
  - **الأصل:** [السطر ١٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-basics.tex#L124). الشاهد المسجل: «We can also define functions by cases. For instance, we could define $h \colon \Nat \to \Nat$ by \[ h(x) = \begin{cases} \frac{x}{2} & \text{if $x$ is even} \\ \frac{x+1}{2} & \text{if $x$ is odd.} \end{cases} \] Since every natural number is either even or…».
  - **العربية المعيارية:** [السطر ١٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-basics.tex#L132)؛ الطبعة الدولية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=53) (ترقيم المتن: ٥٢)، [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=53) (ترقيم المتن: ٥٢)، [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{ex} يمكننا أيضًا تعريف الدوال بحسب الحالات. فمثلًا، يمكننا تعريف $h \colon \Nat \to \Nat$ كما يأتي: \[ h(x) = \begin{cases} \frac{x}{2} & \text{إذا كان $x$ زوجيًا} \\ \frac{x+1}{2} & \text{إذا كان $x$ فرديًا.} \end{cases} \] ولأن كل عدد طبيعي إما زوج…».
  - **العربية التراثية:** [السطر ١١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-basics.tex#L114)؛ الطبعة التراثية: [ص ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=51) (ترقيم المتن: ٥٠)، [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{ex} ومن طرق التعريف التفصيل بحسب الحالات. فالدالة $h \colon \Nat \to \Nat$ يمكن وضعها هكذا: \[ h(x) = \begin{cases} \frac{x}{2} & \text{إذا كان $x$ زوجيًا} \\ \frac{x+1}{2} & \text{إذا كان $x$ فرديًا.} \end{cases} \] وكل طبيعي إما زوجي وإما فردي، فتك…».

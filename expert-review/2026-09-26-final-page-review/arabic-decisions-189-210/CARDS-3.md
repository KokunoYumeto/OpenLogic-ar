# بطاقات التركيب — القرارات ٢٠٣–٢٠٥

[الرجوع إلى مقدمة الدفعة](README.md)

## تركيب الدوال

الأصل الإنجليزي: `Composition of Functions`. معرّف القرار: `retro-0005-0050:section:a42462ceefdb80e8`.

**المعنى المقصود:** تركيب الدوال تكوين دالة جديدة بتطبيق f أولًا ثم g، متى سمح توافق المدى والمجال بذلك.

**سبب الاختيار:** عنوان الأصل Composition of Functions يتبعه وصف عملي يبدأ من x، فيطبق f ثم g، وتنتهي الصيغة إلى g(f(x)). عنوان التراثية «تركيب الدوال» يحفظ ترتيب العمل والمعنى دون ترجمة حرفية توهم أن مجرد جمع الدالتين يكفي. مدخل المعجم يطبع composition of functions «تركيب دوال» ويعرض الحالة نفسها.

**سؤال مفتوح:** هل يستحسن أن يذكر عنوان الفصل أو أول سطر فيه ترتيب التطبيق f ثم g قبل الرسم لتجنب التباس اتجاه رمز التركيب؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٠-٢١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/composition.tex#L10-L21) — عنوان الأصل ومقدمته والرسم اللاحق يحددان العملية وترتيب إجرائها.

**مواضع المعجم المعاينة:** [ص ١٢٥ من PDF (المطبوعة ١١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=125)

**حدود الشاهد المعجمي:** PDF ص ١٢٥، المطبوعة ١١٣، يطبع composition of functions «تركيب دوال» مع مثال يبين تركيب التطبيقين.

**بديل جدير بالمقارنة:** تأليف الدوال؛ محتمل في بعض المراجع لكنه ليس المدخل المعجمي المعاين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المصطلح العام وترتيب العمل.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0025 — تركيب الدوال، وقوع ١:**
  - **الأصل:** [السطر ١٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/composition.tex#L10). الشاهد المسجل: «\olsection{Composition of Functions}».
  - **العربية المعيارية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/composition.tex#L10)؛ الطبعة الدولية: [ص ٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=59) (ترقيم المتن: ٥٨) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=59) (ترقيم المتن: ٥٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{تركيب الدوال}».
  - **العربية التراثية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/composition.tex#L10)؛ الطبعة التراثية: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{تركيب الدوال}».

## التركيب

الأصل الإنجليزي: `Composition`. معرّف القرار: `retro-0005-0050:named-defn:8b9d9607e776a186`.

**المعنى المقصود:** التركيب اسم العملية المعرفة على دالتين متوافقتين، وناتجه دالة من A إلى C قيمتها عند x هي g(f(x)).

**سبب الاختيار:** تعريف الأصل يسمي composition صراحة ثم يثبت مجال الناتج والمجال المقابل ومعادلة القيم. أبقت التراثية اسم «التركيب» والتساوي الرياضي، مع المحافظة على أن الرمز comp(f,g) يطبق f قبل g ولو خالف توقع قارئ يستحضر الرمز الدائري من اليسار. مدخل المعجم شاهد للمصطلح العام، أما جهة الرمز فتحكمها صيغة الأصل.

**سؤال مفتوح:** هل شرح التعريف حول الرمز comp(f,g) كاف لمنع قراءته بترتيب معاكس، أم يحتاج تنبيهًا وجيزًا عند أول ورود له؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٩-٤٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/composition.tex#L39-L42) — عنوان التعريف وصيغته يربطان اسم العملية بالمجال وبالمعادلة g(f(x)).

**مواضع المعجم المعاينة:** [ص ١٢٥ من PDF (المطبوعة ١١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=125)

**حدود الشاهد المعجمي:** PDF ص ١٢٥ يسمي تركيب الدوال ويعطي مثالًا، لكنه لا يفسر الرمز comp(f,g) في الطبعة؛ ترتيب هذا الرمز مقيد بتعريف الأصل.

**بديل جدير بالمقارنة:** تأليف؛ بديل لغوي لا تدعمه الصفحة المعجمية المعاينة لهذا المدخل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المعادلة والاسم المعجمي، ومتوسطة في كفاية شرح الرمز للقارئ.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0025 — تركيب الدوال، وقوع ١:**
  - **الأصل:** [السطر ٣٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/composition.tex#L39). الشاهد المسجل: «\begin{defn}[Composition]».
  - **العربية المعيارية:** [السطر ٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/composition.tex#L38)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[التركيب]».
  - **العربية التراثية:** [السطر ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/composition.tex#L35)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[التركيب]».

## تركيب

الأصل الإنجليزي: `composition`. معرّف القرار: `retro-0005-0050:emphasis:391bb56ce5a4e7d8`.

**المعنى المقصود:** تركيب f مع g في هذا الكتاب هو الدالة x↦g(f(x)) من A إلى C، لا x↦f(g(x)).

**سبب الاختيار:** موضع الإبراز في تعريف الأصل يدل على العملية نفسها، ويعطي على الفور المعادلة التي ترفع أي احتمال لعكس الترتيب. أبقت التراثية «تركيب» ولم تستبدل الصيغة بإعادة ترتيب الوسيطتين داخل الماكرو؛ فالمدخل المعجمي يسند اسم العملية، والصيغة الأصلية تسند ترتيبها الخاص في الكتاب.

**سؤال مفتوح:** هل يحتاج إبراز كلمة «تركيب» إلى ربط لفظي أوضح بعبارة «نطبق f ثم g» حتى يفهم ترتيب المعادلة من غير الرجوع إلى الرسم؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٩-٤٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/composition.tex#L39-L42) — الاسم المبرز والمعادلة في الأصل متجاوران، ويجب ألا تنفصل دلالة المصطلح عن جهة التطبيق.

**مواضع المعجم المعاينة:** [ص ١٢٥ من PDF (المطبوعة ١١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=125)

**حدود الشاهد المعجمي:** PDF ص ١٢٥ يطبع composition of functions «تركيب دوال»؛ جهة تركيب دالتي هذا الكتاب تؤخذ من معادلة الأصل المصاحبة.

**بديل جدير بالمقارنة:** تأليف الدالتين؛ لا يزيد وضوح جهة التطبيق

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى العملية وترتيبها، ومتوسطة في سلاسة العبارة المنشورة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0025 — تركيب الدوال، وقوع ١:**
  - **الأصل:** [السطر ٤١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/composition.tex#L41). الشاهد المسجل: «\emph{composition} of $f$ with~$g$ is $\comp{f}{g} \colon A \to C$,».
  - **العربية المعيارية:** [السطر ٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/composition.tex#L40)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تركيب} $f$ مع~$g$ هو $\comp{f}{g} \colon A \to C$،».
  - **العربية التراثية:** [السطر ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/composition.tex#L37)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تركيب} $f$ مع~$g$ هو $\comp{f}{g} \colon A \to C$،».

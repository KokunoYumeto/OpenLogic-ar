# بطاقات تصويبا مثال الأزواج — القرارات ٢٢٩–٢٣٠

[الرجوع إلى مقدمة الدفعة](README.md)

## سمّى الأصل الزوج الثاني ⟨0,2⟩، فأثبتناه ⟨0,1⟩؛ فهو الذي يقع في الموضع الثالث من جدول بداية التعداد الأول. وكرر الأصل أسرة الأزواج ⟨2,m⟩، وصواب الثانية ⟨3,m⟩؛ ويشهد له الزوج ⟨3,0⟩ في الموضع الثامن من بداية التعداد المكتمل أعلاه.

الأصل الإنجليزي: `distinct source corrections with exact table witnesses`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0032-CLASSICAL-SOURCE-CORRECTION-DISCLOSURE-20260907`.

**المعنى المقصود:** يوجد خطآن منفصلان في مثال الأصل: سمى الزوج الثاني من سلسلة الصف الصفري (0,2) والصواب (0,1)، وكرر أسرة (2,m) حيث ينبغي (3,m).

**سبب الاختيار:** تضع قائمة الأصل المعروضة (0,1) في الموضع الثالث بعد ترك خانة، بينما نثره يسميه (0,2)؛ ويضع جدول البداية المكتملة (3,0) في الموضع الثامن بينما نثره يكرر أسرة (2,m). أفصحت التراثية عن التصويبين كل على حدة وربطتهما بموضعي الجدولين، فلا تبدو الأعداد الجديدة تغييرًا صامتًا للترجمة. مدخل الزوج المرتب في المعجم يثبت طبيعة الكائن فقط ولا يشهد للموضع الثالث أو الثامن؛ هذان من جدول الأصل.

**سؤال مفتوح:** هل تعرض الحاشية التراثية شهادتي الموضع الثالث والثامن بحيث يستطيع القارئ التحقق من كل تصويب من جدول الأصل دون خلط الخطأين؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٩-٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L19-L27) — النثر يسمي الزوج الثاني خطأ وجدول البداية يضع الزوج الصحيح في الخانة الثالثة.؛ [الأسطر ٣٩-٤٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L39-L45) — النثر يكرر أسرة الصف الثالث وجدول التعداد يضع الزوج (3,0) في الخانة الثامنة.

**وجه جمع المواضع:** الموضعان النثريان في الأصل يقابل كل منهما جدولًا مجاورًا يثبت الزوج الصحيح، ولا يجوز جمعهما في دعوى تصويب مبهمة.

**مواضع المعجم المعاينة:** [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)

**حدود الشاهد المعجمي:** PDF ص ٥٠٦ يبين معنى ordered pair «زوج مرتب»، لكنه لا يقدم شاهدًا على ترتيب خانات المثال؛ تصويب الخانتين من نص الأصل وجدوليه.

**بديل جدير بالمقارنة:** ترك تصحيح الزوج الثاني صامتًا؛ يحجب فرقًا بين الشاهد والترجمة؛ حصر التنبيه في الأسرة المكررة؛ يفوت الخطأ المستقل الأول

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التصويبين لأن جدولَي الأصل يحددان الموضعين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0032 — دالة مزاوجة بديلة، وقوع ١:**
  - **الأصل:** [السطر ١٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L19). الشاهد المسجل: «Starting with the pairs that have~$0$ in the first place (i.e., pairs $\tuple{0,m}$), put the first (i.e., $\tuple{0,0}$) in the first empty place, then skip an empty space, put the second (i.e., $\tuple{0,2}$) in the next empty place, skip one again, and s…».
  - **الأصل:** [السطر ٣٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L39). الشاهد المسجل: «Enter pairs $\tuple{2,m}$, $\tuple{2,m}$, etc., in the same way. Our completed enumeration thus starts like this:».
  - **العربية التراثية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L46)؛ الطبعة التراثية: [ص ٦٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=65) (ترقيم المتن: ٦٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «سمّى الأصل الزوج الثاني $\tuple{0,2}$، فأثبتناه $\tuple{0,1}$؛ فهو الذي يقع في الموضع الثالث من جدول بداية التعداد الأول. وكرر الأصل أسرة الأزواج $\tuple{2,m}$، وصواب الثانية $\tuple{3,m}$؛ ويشهد له الزوج $\tuple{3,0}$ في الموضع الثامن من بداية التعداد المك…».

## ورد الزوج الثاني في النص الإنجليزي على صورة ⟨0,2⟩؛ وأُثبت هنا ⟨0,1⟩، كما يبيّنه الموضع الثالث من جدول بداية التعداد الأول. وكرر النص الإنجليزي أسرة الأزواج ⟨2,m⟩؛ والصواب ⟨3,m⟩ في المرة الثانية، كما يبيّنه الزوج ⟨3,0⟩ في الموضع الثامن من بداية التعداد المكتمل أعلاه.

الأصل الإنجليزي: `distinct source corrections to the second pair and repeated family`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0032-MSA-SOURCE-CORRECTION-DISCLOSURE-20260907`.

**المعنى المقصود:** التنبيه في الطبعة المعيارية يفرق بين إصلاح (0,2) إلى (0,1) في بداية السرد وإصلاح الأسرة الثانية (2,m) إلى (3,m) في متابعة السرد.

**سبب الاختيار:** كانت صيغة عربية أقدم تفصح عن الأسرة المكررة وحدها. فأضاف التصويب المعياري شاهد الخانة الثالثة للزوج (0,1)، وأبقى شاهد الخانة الثامنة للزوج (3,0)، على وفق جدولي الأصل المثبتين. هذا إيضاح تصحيحي للنسخة المنشورة، لا نسبة الأعداد المصححة إلى نثر الأصل الإنجليزي. مدخل الزوج المرتب المعجمي لا يحسم القيم الموضعية في الجدول.

**سؤال مفتوح:** هل يميز النص المعياري بوضوح بين ما طبع في نثر الأصل وما أثبته جدول الأصل عند كل من التصويبين؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٩-٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L19-L27) — يظهر اسم الزوج الخاطئ ثم يقابله زوج الخانة الثالثة الصحيح.؛ [الأسطر ٣٩-٤٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L39-L45) — تظهر الأسرة المكررة خطأ ثم زوج الخانة الثامنة الصحيح.

**وجه جمع المواضع:** المقطعان الإنجليزيان وجدولاهما يثبتان اختلافين مستقلين يجب الإفصاح عنهما في حاشية الترجمة.

**مواضع المعجم المعاينة:** [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)

**حدود الشاهد المعجمي:** PDF ص ٥٠٦ يشرح الزوج المرتب دون ترتيب المثال الخاص؛ القيمتان المصححتان تستندان إلى جدولي الأصل الإنجليزي.

**بديل جدير بالمقارنة:** إبقاء التنبيه القديم عن الأسرة الثانية فقط؛ لا يفصح عن التصويب المستقل للزوج الثاني

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في حدود النص الأصلي والتصويبين والإفصاح عنهما.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0032 — دالة مزاوجة بديلة، وقوع ١:**
  - **الأصل:** [السطر ١٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L19). الشاهد المسجل: «Starting with the pairs that have~$0$ in the first place (i.e., pairs $\tuple{0,m}$), put the first (i.e., $\tuple{0,0}$) in the first empty place, then skip an empty space, put the second (i.e., $\tuple{0,2}$) in the next empty place, skip one again, and s…».
  - **الأصل:** [السطر ٣٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L39). الشاهد المسجل: «Enter pairs $\tuple{2,m}$, $\tuple{2,m}$, etc., in the same way. Our completed enumeration thus starts like this:».
  - **العربية المعيارية:** [السطر ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/pairing-alt.tex#L49)؛ الطبعة الدولية: [ص ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=69) (ترقيم المتن: ٦٨) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=69) (ترقيم المتن: ٦٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ورد الزوج الثاني في النص الإنجليزي على صورة $\tuple{0,2}$؛ وأُثبت هنا $\tuple{0,1}$، كما يبيّنه الموضع الثالث من جدول بداية التعداد الأول. وكرر النص الإنجليزي أسرة الأزواج $\tuple{2,m}$؛ والصواب $\tuple{3,m}$ في المرة الثانية، كما يبيّنه الزوج $\tuple{3,0}$…».

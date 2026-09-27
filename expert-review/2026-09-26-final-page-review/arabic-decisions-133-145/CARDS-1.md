# بطاقات الترتيبات — القرارات ١٣٣–١٤٥

[الرجوع إلى مقدمة الدفعة](README.md)

## لكنها ليست ترتيبًا خطيًا بوجه عام

الأصل الإنجليزي: `extension relation`. معرّف القرار: `semantic-propagation-20260906:0016-P1`.

**المعنى المقصود:** علاقة البادئة على المتتاليات المنتهية ترتيب جزئي؛ وليست خطية عمومًا إذا احتوت الأبجدية عنصرين مختلفين، لكنها خطية إذا لم تحتو إلا عنصرًا واحدًا أو كانت خالية.

**سبب الاختيار:** ينفي الأصل الخطية بلا قيد في الجملة ثم يبرهن بمثال يفرض a≠b. وهذا الشاهد لا يوجد إذا كانت الأبجدية خالية أو أحادية، إذ تقارن حينئذ كل متتاليتين بالبادئة. لذا أضافت الصياغة العربية «بوجه عام» إلى النفي، محافظة على برهان الأصل ومانعة تعميمه خطأً. يحدد المعجم الترتيب الخطي بإمكان مقارنة كل عنصرين؛ وهو شاهد على معيار الخطية لا على تصحيح هذه الجملة بعينه.

**سؤال مفتوح:** هل «ليست ترتيبًا خطيًا بوجه عام» تبين الاستثناء بما يكفي، أم يحسن التصريح بأن المثال المضاد يفترض حرفين مختلفين من A؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧٢-٧٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L72-L79) — يعرض تعريف علاقة البادئة ثم ينفي الخطية ويسوق شاهدًا مشروطًا باختلاف حرفين.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣: linear order = «ترتيب خطي»، ويعني مقارنة كل عنصرين؛ استثناء الأبجدية الأحادية مستنبط من تعريف الأصل لا مذكور في المعجم.

**بديل جدير بالمقارنة:** ليست خطية إذا ضمت A حرفين مختلفين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للتصحيح المنطقي، ومتوسطة لكفاية العبارة الموجزة للقارئ.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٧٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L78). الشاهد المسجل: «extension relation on $A^*$ is a partial order but not a linear order,».
  - **العربية المعيارية:** [السطر ٧٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L75)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وعلاقة الامتداد على $A^*$ ترتيب جزئي، لكنها ليست ترتيبًا خطيًا بوجه عام؛ فمثلًا،».
  - **العربية التراثية:** [السطر ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L69)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وهي على $A^*$ ترتيب جزئي، لا خطي عمومًا؛ فإذا كان $a \neq b$ كان».

## مقطعًا ابتدائيًا

الأصل الإنجليزي: `initial segment`. معرّف القرار: `retro-0005-0050:emphasis:e8e288ef2a21ec3c`.

**المعنى المقصود:** المتتالية s مقطع ابتدائي من s′ إذا طابقت أول عناصر s′ جميعًا، بما في ذلك حالة المتتالية الخالية.

**سبب الاختيار:** يسمي الأصل s بادئةً أو initial segment لـs′ بعد تعريف العلاقة على A*. صاغت التراثية الاسم «مقطعًا ابتدائيًا» في موقع نصب بعد «سمينا»، مقابل «مقطع ابتدائي» في المعيارية. يطبع المعجم «قطعة ابتدائية» للجزء الأول من متتالية، وهو شاهد قريب لكنه لا يثبت لفظ «مقطع». أبقي اللفظ المنشور مؤقتًا وسجل اختلافه الصريح من المدخل.

**سؤال مفتوح:** هل «مقطع ابتدائي» أم «قطعة ابتدائية» أنسب في متتاليات A*، وهل يوضح السياق شمول المتتالية الخالية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧٢-٧٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L72-L79) — يربط الاسم بتعريف علاقة البادئة وبحالة المتتالية الخالية.

**مواضع المعجم المعاينة:** [ص ٣٦١ من PDF (المطبوعة ٣٤٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=361)

**حدود الشاهد المعجمي:** PDF ص ٣٦١، المطبوعة ٣٤٩: initial segment = «قطعة ابتدائية»؛ يذكر معنى قطعة المتتالية من أولها ومعنى القطعة الابتدائية في مجموعة مرتبة، ولا يطبع «مقطع».

**بديل جدير بالمقارنة:** قطعة ابتدائية كما في المعجم

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للمعنى، ومتوسطة للاسم المنشور المخالف للمدخل.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٧٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L77). الشاهد المسجل: «we also say that $s$ is an \emph{initial segment} of~$s'$. The».
  - **العربية المعيارية:** [السطر ٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L74)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$s \sqsubseteq s'$ قلنا أيضًا إن $s$ \emph{مقطع ابتدائي} من~$s'$.».
  - **العربية التراثية:** [السطر ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L68)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فمتى كان $s \sqsubseteq s'$ سمينا $s$ \emph{مقطعًا ابتدائيًا} من~$s'$.».

## الترتيب الخطي

الأصل الإنجليزي: `Linear order`. معرّف القرار: `retro-0005-0050:named-defn:7aedf753e1655eb8`.

**المعنى المقصود:** عنوان الترتيب الخطي: ترتيب جزئي يمكن فيه مقارنة كل عنصرين مختلفين بأحد الاتجاهين.

**سبب الاختيار:** يعرّف الأصل الترتيب الخطي بإضافة الاتصالية إلى الترتيب الجزئي؛ أي لا يبقى زوج مختلف غير قابل للمقارنة. يطبع المعجم «ترتيب خطي» مع شرط المقارنة نفسه، ويورد «ترتيب كلي» في الأسماء المرادفة الإنجليزية. أداة التعريف في العنوان صياغة عربية موضعية لا اختلاف في الحد الرياضي.

**سؤال مفتوح:** هل عنوان «الترتيب الخطي» يبيّن أنه أخص من الجزئي، وأن الاتصالية هنا مقارنة كل زوج لا اتصال رسم بياني؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢-٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L32-L35) — يعرّف العنوان بإضافة connected إلى partial order ويسرد اسم total order أيضًا.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣: linear order = «ترتيب خطي» مع شرط المقارنة بين كل عنصرين.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية؛ الاسم والشرط موافقان للمدخل المعجمي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L32). الشاهد المسجل: «\begin{defn}[Linear order]\ollabel{def:linearorder}».
  - **العربية المعيارية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L31)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الترتيب الخطي]\ollabel{def:linearorder}».
  - **العربية التراثية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L28)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الترتيب الخطي]\ollabel{def:linearorder}».

## الترتيب الخطي

الأصل الإنجليزي: `linear order.`. معرّف القرار: `retro-0005-0050:emphasis:51c0c107c25bdd3e`.

**المعنى المقصود:** الترتيب الخطي اسم ثان للترتيب الكلي في التعريف نفسه؛ هو ترتيب جزئي يقارن كل زوج مختلف.

**سبب الاختيار:** يقرن الأصل total order وlinear order في تعريف واحد. في التراثية جاء الثاني معرفةً بعد «ويسمى أيضًا» انسجامًا مع الأول، بينما صيغ في المعيارية نكرة منصوبة بعد «يسمى». يثبت المعجم «ترتيب خطي» بمعنى المقارنة الشاملة، فلا ينتج عن اختلاف التركيب النحوي شرط جديد ولا تُحذف مضادّة التناظر الموروثة من الجزئي.

**سؤال مفتوح:** هل التماثل بين «الترتيب الكلي» و«الترتيب الخطي» واضح للقارئ، مع بقاء شرط الجزئي والمقارنة معًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢-٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L32-L35) — يسمي الترتيب الجزئي المتصل باسمين مترادفين في التعريف نفسه.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣، يثبت «ترتيب خطي» ويذكر total order اسمًا آخر للمدخل.

**بديل جدير بالمقارنة:** ترتيبًا خطيًا في أسلوب المعيارية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للحد والمصطلح، ومتوسطة لتفضيل التعريف أو التنكير النحوي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L34). الشاهد المسجل: «\emph{total order} or \emph{linear order.}».
  - **العربية المعيارية:** [السطر ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L33)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{ترتيبًا كليًا} أو \emph{ترتيبًا خطيًا.}».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L29)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب الكلي}، ويسمى أيضًا \emph{الترتيب الخطي}، ترتيب جزئي متصل.».

## لا يزيد طولًا على

الأصل الإنجليزي: `no longer than`. معرّف القرار: `retro-0005-0050:emphasis:2f796191d0cf12b2`.

**المعنى المقصود:** العلاقة على الكلمات الثنائية التي فيها x لا يزيد طولًا على y بالضبط حين يكون طول x أصغر من طول y أو مساويًا له.

**سبب الاختيار:** يضع الأصل اسم no longer than ثم يثبته بالصيغة len(x)≤len(y). تحفظ العربيتان اتجاه المقارنة: «لا يزيد طولًا على» لا تعني أن x بادئة y، وقد يتساوى الطول لكلمتين مختلفتين مثل 01 و10. المعجم المعاين يشهد لفكرة الترتيب والمقارنة، ولا يطبع هذه العبارة المركبة؛ فهي صياغة وصفية من شرط الأصل لا مدخل منقول عنه.

**سؤال مفتوح:** أفي «لا يزيد طولًا على» إيجاز طبيعي لشرط الطول ≤، أم «ليس أطول من» أبين مع تجنب الخلط بعلاقة البادئة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٥-٥٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L45-L50) — يعرّف العلاقة بمتباينة الطولين ويقدم 01 و10 شاهدًا على عدم مضادّة التناظر.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣، شاهد على معنى الترتيب بالمقارنة؛ لا يرد فيه الاسم الوصفي no longer than أو ترجمة مطابقة له.

**بديل جدير بالمقارنة:** ليس أطول من

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لاتجاه المتباينة، ومتوسطة للأفصح بين العبارتين الوصفيتين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٤٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L46). الشاهد المسجل: «Consider the \emph{no longer than} relation $\preccurlyeq$».
  - **العربية المعيارية:** [السطر ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L44)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «اعتبر علاقة \emph{لا يزيد طولًا على} $\preccurlyeq$».
  - **العربية التراثية:** [السطر ٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L40)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ولننظر في علاقة \emph{لا يزيد طولًا على} $\preccurlyeq$ على~$\Bin^*$:».

## ترتيب

الأصل الإنجليزي: `order`. معرّف القرار: `retro-0005-0050:emphasis:a8bcc2306544da54`.

**المعنى المقصود:** الترتيب هنا علاقة مقارنة بين عناصر مجال، لا ترتيب عرض الكلمات في الصفحة ولا رتبة عدد منفرد.

**سبب الاختيار:** يفتتح الأصل أنواع order relations بأمثلة الأصغر والمساوي والأكبر. في التراثية يجيء «ترتيب» مضافًا إليه بعد «علاقات»، وفي المعيارية «الترتيب» معرفةً؛ وكلاهما يؤدي الاسم الاصطلاحي. يطبع المعجم «علاقة ترتيب» في موضعي ordering وorder relation المتجاورين، ويشرح شروط علاقة الترتيب؛ لذلك لا يستند الاختيار إلى معنى order بوصفه درجة أو مرتبة.

**سؤال مفتوح:** هل «علاقات ترتيب» سليمة وأفصح هنا من «علاقات الترتيب»، مع وضوح المعنى الرياضي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٢-١٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L12-L19) — يمهد لتصنيف العلاقات التي تعبر عن الأصغر والمساوي والأكبر.

**مواضع المعجم المعاينة:** [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)، [ص ٥٠٧ من PDF (المطبوعة ٤٩٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=507)

**حدود الشاهد المعجمي:** PDF ص ٥٠٦-٥٠٧، المطبوعتان ٤٩٤-٤٩٥: ordering/order relation = «علاقة ترتيب»؛ تختلف هذه عن مداخل order بمعنى المرتبة أو الدرجة.

**بديل جدير بالمقارنة:** علاقات الترتيب كما في المعيارية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للمعنى الاصطلاحي، ومتوسطة للفارق الأسلوبي في الإضافة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ١٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L15). الشاهد المسجل: «certain respect. These involve \emph{order} relations. But there are».
  - **العربية المعيارية:** [السطر ١٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L15)؛ الطبعة الدولية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب}. لكن علاقات الترتيب أنواع مختلفة؛ فمنها مثلًا ما يشترط أن».
  - **العربية التراثية:** [السطر ١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L14)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «أو «أكبر منه» من جهة ما؛ وتلك علاقات \emph{ترتيب}. وليس الترتيب».

## الترتيب الجزئي

الأصل الإنجليزي: `partial order`. معرّف القرار: `retro-0005-0050:emphasis:f7017a0b5551eebc`.

**المعنى المقصود:** الترتيب الجزئي ترتيب مسبق مضادّ للتناظر؛ أي علاقة انعكاسية ومتعدية لا يتبادل فيها عنصران مختلفان الاتجاهين معًا.

**سبب الاختيار:** يضيف الأصل anti-symmetric إلى preorder، فتجتمع الانعكاسية والتعدية ومضادّة التناظر. الاسم «ترتيب جزئي» مطبوع في المعجم؛ وفي التراثية جاء معرفةً بعد تعريف «الترتيب المسبق»، وفي المعيارية نكرةً منصوبة بعد «يسمى». اختلاف الإعراب لا يضيف قابلية المقارنة لكل زوج؛ فتلك خاصة بالخطي.

**سؤال مفتوح:** هل يتبين من اللفظ والحد أن «جزئي» لا يعني بعض العناصر فقط، وأن زوجًا غير قابل للمقارنة جائز؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٧-٣٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L27-L30) — يسمي الترتيب المسبق المضاد للتناظر ترتيبًا جزئيًا.

**مواضع المعجم المعاينة:** [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)

**حدود الشاهد المعجمي:** PDF ص ٥٢٣، المطبوعة ٥١١: partial order = «ترتيب جزئي»، مع مدخل للمجموعة المرتبة جزئيًا.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية؛ المصطلح مباشر وحدّه محفوظ.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L29). الشاهد المسجل: «\emph{partial order}.».
  - **العربية المعيارية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L28)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{ترتيبًا جزئيًا}.».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L25)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب الجزئي} ترتيب مسبق يضاف إلى خصائصه مضادّة التناظر.».

## الترتيب الجزئي

الأصل الإنجليزي: `Partial order`. معرّف القرار: `retro-0005-0050:named-defn:9e9c3336e3d57c48`.

**المعنى المقصود:** عنوان تعريف الترتيب الجزئي، وهو ترتيب مسبق يضاف إليه شرط مضادّة التناظر.

**سبب الاختيار:** العنوان معرف في العربيتين لاسم partial order. يطبع المعجم «ترتيب جزئي» دون أداة التعريف، ويشرح أن المجموعة المرتبة جزئيًا مزودة بعلاقة من هذا النوع. لا تُستنتج الخطية من «جزئي»؛ إذ يسرد الأصل الترتيب الخطي تعريفًا تالياً أخص منه. تحفظ صيغة العنوان هذا التسلسل في التصنيف.

**سؤال مفتوح:** هل عنوان «الترتيب الجزئي» واضح بوصفه اسم علاقة لا مجرد ترتيب جزء من المجموعة، مع إحالته إلى الشروط الثلاثة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٧-٣٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L27-L30) — يقرن العنوان بالترتيب المسبق المضاد للتناظر.

**مواضع المعجم المعاينة:** [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)

**حدود الشاهد المعجمي:** PDF ص ٥٢٣، المطبوعة ٥١١، يثبت «ترتيب جزئي»؛ التعريف في عنوان الطبعة تصريف سياقي.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للاسم والمعنى؛ أداة التعريف نحوية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L27). الشاهد المسجل: «\begin{defn}[Partial order]».
  - **العربية المعيارية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L26)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الترتيب الجزئي]».
  - **العربية التراثية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L24)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الترتيب الجزئي]».

## الترتيب المسبق

الأصل الإنجليزي: `preorder.`. معرّف القرار: `retro-0005-0050:emphasis:c945851ea2de2d06`.

**المعنى المقصود:** الترتيب المسبق علاقة انعكاسية ومتعدية، ولا يشترط مضادّة التناظر أو قابلية مقارنة كل زوج.

**سبب الاختيار:** يعرف الأصل preorder بالانعكاسية والتعدية وحدهما. التراثية تصوغ «الترتيب المسبق» معرفًا بعد المبتدأ، والمعيارية «ترتيبًا مسبقًا» منصوبًا بعد «تسمى»؛ ولا يتغير الحد. مدخل ordering المعاين يسرد التعدي ومضادّة التناظر دون أن يطبع هنا شرط الانعكاسية، ومدخل partial order يثبت الاسم العربي «ترتيب جزئي». ولم يظهر في البحث OCR المحدود أو الصفحات المعاينة مدخل مباشر لـpreorder؛ لذلك لا ننسب «المسبق» إليهما، ونبقي المصطلح المنشور مؤقتًا.

**سؤال مفتوح:** هل «ترتيب مسبق» مستعمل اصطلاحًا لهذا الشرط الأضعف في المصادر العربية الرياضية، أم يلزم بديل موثق مع إبقاء الانعكاسية والتعدية فقط؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٢-٢٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L22-L25) — يعرف العلاقة بشرطي الانعكاسية والتعدية دون شرط ثالث.

**مواضع المعجم المعاينة:** [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)، [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)

**حدود الشاهد المعجمي:** PDF ص ٥٠٦ و٥٢٣، المطبوعتان ٤٩٤ و٥١١، يثبتان علاقة الترتيب والترتيب الجزئي؛ لم تثبت فيهما تسمية preorder نفسها، وغيابها من OCR المحدود ليس حجة غياب شامل.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للحد الرياضي، ومنخفضة نسبيًا لتوثيق اللفظ العربي في الشواهد المعاينة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L24). الشاهد المسجل: «\emph{preorder.}».
  - **العربية المعيارية:** [السطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L23)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{ترتيبًا مسبقًا.}».
  - **العربية التراثية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L21)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب المسبق} العلاقة الجامعة للانعكاسية والتعدية.».

## الخطي الصارم

الأصل الإنجليزي: `strict linear order.`. معرّف القرار: `retro-0005-0050:emphasis:6967c7a81fd59b5f`.

**المعنى المقصود:** الخطي الصارم في هذا السياق ترتيب صارم يقارن كل عنصرين مختلفين، فيساوي معنى «الترتيب الكلي الصارم» في التعريف.

**سبب الاختيار:** يسرد الأصل strict total order وstrict linear order اسمين لعلاقة صارمة متصلة واحدة. التراثية تختصر الاسم الثاني إلى «الخطي الصارم» اعتمادًا على «الترتيب» المصرح به قبله مباشرة، بينما تبسطه المعيارية. المعجم يثبت «ترتيب خطي» غير الصارم وشرط المقارنة، ولا يطبع في الصفحة صيغة strict linear order المركبة؛ فالجزء الصارم مأخوذ من حد الأصل.

**سؤال مفتوح:** هل حذف «الترتيب» من الاسم الثاني مفهوم في الجملة نفسها، أم يفضل «الترتيب الخطي الصارم» لئلا ينفصل عن اسم العلاقة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٧-٩٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L87-L90) — يسمي الترتيب الصارم المتصل باسمين مترادفين.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣: linear order = «ترتيب خطي»؛ لا يثبت المدخل وصف strict أو العنوان المركب الصارم.

**بديل جدير بالمقارنة:** الترتيب الخطي الصارم كما في الصياغة المعيارية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للمعنى، ومتوسطة لبلاغة الحذف الاصطلاحي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٨٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L89). الشاهد المسجل: «\emph{strict total order} or \emph{strict linear order.}».
  - **العربية المعيارية:** [السطر ٨٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L85)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{ترتيبًا كليًا صارمًا} أو \emph{ترتيبًا خطيًا صارمًا.}».
  - **العربية التراثية:** [السطر ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L78)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب الكلي الصارم}، أو \emph{الخطي الصارم}، ترتيب صارم متصل.».

## ترتيب صارم

الأصل الإنجليزي: `strict order`. معرّف القرار: `retro-0005-0050:emphasis:35ab10fec89ca3c9`.

**المعنى المقصود:** الترتيب الصارم علاقة لا انعكاسية ولا تناظرية ومتعدية؛ فلا زوج ذاتيًا فيها، ويمنع اجتماع الاتجاهين لأي زوج.

**سبب الاختيار:** يعد الأصل الشروط الثلاثة صراحةً وإن كان اللاتناظر يقتضي اللاانعكاسية منطقيًا؛ أبقت العربيتان هذا التعداد ولم تختزلاه. صفحة المعجم عن ordering تعرض علاقة بالرمز ≤ وتسرد التعدي ومضادّة التناظر، لكنها لا تطبع strict order؛ فلا يُنسب «صارم» إليها ولا تُستكمل منها وحدها شروط الترتيب غير الصارم. التراثية تختار النكرة «ترتيب صارم» بعد الجملة التعريفية، والمعيارية تعرف الاسم في الموضع المناظر.

**سؤال مفتوح:** هل «ترتيب صارم» واضح في مقابلة الترتيب الجزئي غير الصارم، وهل يجدر إبقاء الشروط الثلاثة كما في الأصل رغم تضمن أحدها لآخر؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٢-٨٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L82-L85) — يعدد اللاانعكاسية واللاتناظرية والتعدية في تعريف strict order.

**مواضع المعجم المعاينة:** [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)

**حدود الشاهد المعجمي:** PDF ص ٥٠٦، المطبوعة ٤٩٤، يورد ordering بعلاقة رمزها ≤، ويذكر التعدي ومضادّة التناظر دون أن يطبع شرط الانعكاسية أو اسم strict order المركب.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للحد والشروط، ومتوسطة لتوثيق الاسم المركب في الشاهد المعاين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٨٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L83). الشاهد المسجل: «A \emph{strict order} is a relation which is irreflexive, asymmetric,».
  - **العربية المعيارية:** [السطر ٨٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L80)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب الصارم} علاقة تتصف باللاانعكاسية واللاتناظرية والتعدية.».
  - **العربية التراثية:** [السطر ٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L74)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «كل علاقة تجمع اللاانعكاسية واللاتناظرية والتعدية \emph{ترتيب صارم}.».

## الترتيب الكلي الصارم

الأصل الإنجليزي: `strict total order`. معرّف القرار: `retro-0005-0050:emphasis:75f58cfddd571dac`.

**المعنى المقصود:** الترتيب الكلي الصارم ترتيب صارم متصل، أي يقارن كل عنصرين مختلفين بأحد الاتجاهين، من غير الأزواج الذاتية.

**سبب الاختيار:** يؤدي «الكلي» هنا اشتراط المقارنة بين كل زوج مختلف، لا صدق العلاقة في الاتجاهين ولا شمول الأزواج الذاتية. يذكر المعجم total order اسمًا آخر للترتيب الخطي غير الصارم؛ أما قيد الصرامة والاسم المركب فمستندان إلى تعريف الأصل لا إلى مدخل مطابق في الصفحة. تراعي التراثية عطف الاسمين المعرفين، فيما تستعمل المعيارية النكرة المنصوبة بعد «يسمى».

**سؤال مفتوح:** هل «الترتيب الكلي الصارم» يوصل شرط الاتصال مع منع الأزواج الذاتية بلا إيحاء بأن «كلي» يعني صدق R على جميع الأزواج؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٧-٩٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L87-L90) — يسمي الترتيب الصارم المتصل ترتيبًا كليًا صارمًا أو خطيًا صارمًا.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣، يذكر total order مرادفًا لـlinear order؛ لا يطبع strict total order مستقلًا.

**بديل جدير بالمقارنة:** الترتيب الخطي الصارم، الاسم الثاني في الأصل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لشرط المقارنة، ومتوسطة لتوثيق المركب الاصطلاحي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٨٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L89). الشاهد المسجل: «\emph{strict total order} or \emph{strict linear order.}».
  - **العربية المعيارية:** [السطر ٨٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L85)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{ترتيبًا كليًا صارمًا} أو \emph{ترتيبًا خطيًا صارمًا.}».
  - **العربية التراثية:** [السطر ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L78)؛ الطبعة التراثية: [ص ٤٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=45) (ترقيم المتن: ٤٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب الكلي الصارم}، أو \emph{الخطي الصارم}، ترتيب صارم متصل.».

## الترتيب الكلي

الأصل الإنجليزي: `total order`. معرّف القرار: `retro-0005-0050:emphasis:480ad08720965a39`.

**المعنى المقصود:** الترتيب الكلي هو ترتيب جزئي متصل، أو بعبارة مكافئة ترتيب خطي يقارن كل زوج مختلف.

**سبب الاختيار:** يقدم الأصل total order وlinear order اسمين للتعريف نفسه. يذكر المعجم total order بين أسماء linear order ويحده بمقارنة كل عنصرين؛ لذا يعضد اختيار «الترتيب الكلي» مع «الخطي». في التراثية الاسم معرفة بعد سياق تعريف، وفي المعيارية جاء نكرة منصوبة؛ ليس هذا اختلافًا في قوة الخاصية.

**سؤال مفتوح:** هل يقرأ «الكلي» على معنى قابلية مقارنة كل زوج، لا على معنى أن كل زوج في العلاقة أو أن المجال كله مرتب فحسب؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢-٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L32-L35) — يعطي total order وlinear order بوصفهما اسمين للترتيب الجزئي المتصل.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣، يورد total order ضمن المرادفات الإنجليزية لـlinear order = «ترتيب خطي»؛ صيغة «ترتيب كلي» ترجمة متسقة لا مدخل عربي مستقل هنا.

**بديل جدير بالمقارنة:** الترتيب الخطي، الاسم المعجمي المثبت للمفهوم نفسه

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية للتكافؤ الرياضي، ومتوسطة لتوثيق الاسم العربي «الكلي» مباشرة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0016 — الترتيبات، وقوع ١:**
  - **الأصل:** [السطر ٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/orders.tex#L34). الشاهد المسجل: «\emph{total order} or \emph{linear order.}».
  - **العربية المعيارية:** [السطر ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/orders.tex#L33)؛ الطبعة الدولية: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=46) (ترقيم المتن: ٤٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{ترتيبًا كليًا} أو \emph{ترتيبًا خطيًا.}».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/orders.tex#L29)؛ الطبعة التراثية: [ص ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=44) (ترقيم المتن: ٤٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الترتيب الكلي}، ويسمى أيضًا \emph{الترتيب الخطي}، ترتيب جزئي متصل.».

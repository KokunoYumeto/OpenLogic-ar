# بطاقات الطول والفهرسة والتقاطع — القرارات ٣٠٨–٣١١

[الرجوع إلى مقدمة الدفعة](README.md)

## أعدادًا أخرى

الأصل الإنجليزي: `more`. معرّف القرار: `retro-0005-0050:emphasis:4cd1d693c68ebbda`.

**المعنى المقصود:** بالانتقال من الطبيعية إلى الصحيحة ثم النسبية والحقيقية تضاف أعداد إلى النطاق المدروس، ولا يقتضي ذلك مساواة أحجام تلك المجموعات.

**سبب الاختيار:** جاءت «أعدادًا أخرى» بدل «مزيدًا» لبيان المفعول الذي يزيد في السلسلة Nat⊆Int⊆Rat⊆Real. الجملة عن اتساع الاحتواء وتنوع الأعداد الممثلة، لا عن مقارنة الكارديناليات؛ فوجود حقنات أو احتواءات لا يجعل all cardinalities strictly larger، كما يتبين لاحقًا.

**سؤال مفتوح:** هل «أعدادًا أخرى» تحافظ على المراد من more دون أن توهم أن كل انتقال يزيد العدد الكاردينالي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٩-٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L29-L34) — سلسلة الاحتواء اللاحقة تعين معنى الزيادة بأنها إضافة عناصر وتمثيلات لا حكم على الحجم اللانهائي.

**انطباق المعجم الرياضي:** more هنا رابط تفسيري غير اصطلاحي؛ تفسره سلسلة الاحتواء والأمثلة التالية في الأصل.

**بديل جدير بالمقارنة:** مزيدًا من الأعداد؛ أوضح مفعولًا وأقرب إلى صياغة الطبعة المعاصرة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى الاتساع، متوسطة في تفضيل النظم التراثي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0007 — المجموعات المهمة والسلاسل، وقوع ١:**
  - **الأصل:** [السطر ٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L29). الشاهد المسجل: «As we move through these sets, we are adding \emph{more} numbers to».
  - **العربية المعيارية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/important-sets.tex#L30)؛ الطبعة الدولية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مزيدًا} من الأعداد إلى ما لدينا. وبالفعل، من الواضح أن».
  - **العربية التراثية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/important-sets.tex#L28)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وكلما انتقلنا في هذه المجموعات إلى التالية ضممنا \emph{أعدادًا أخرى}».

## طولها

الأصل الإنجليزي: `length`. معرّف القرار: `retro-0005-0050:emphasis:f85f97d998311146`.

**المعنى المقصود:** طول السلسلة x=x₁…xₙ هو عدد رموزها n، لا القيمة العددية للكلمة أو طول أبجديتها.

**سبب الاختيار:** ألحقت التراثية ضمير «ها» بـ«طول» ليعود إلى السلسلة الموصوفة، ثم تحفظ الصيغة len(x)=n. لا يعطي البحث المحدود في المعجم مدخلًا مباشرًا لـ length of a string، فلا نعامل هذا الضمير شهادة اصطلاحية؛ يثبت معناه التعريف الرمزي في الأصل.

**سؤال مفتوح:** هل مرجع الضمير في «طولها» واضح عند الانتقال بين السلسلة والأبجدية A، أم ينبغي تكرار «طول السلسلة»؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٥٦-٥٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L56-L58) — تحدد معادلة len(x)=n أن الطول عدد الحروف في السلسلة x.

**نتيجة البحث المعجمي المحدود:** لم يظهر length of a string في بحث OCR المحدود في المعجم المصور؛ التعريف x₁…xₙ وlen(x)=n هو السند الرياضي، ولا نستنتج غياب المصطلح عن سائر المصادر.

**بديل جدير بالمقارنة:** طول السلسلة؛ أكثر صراحة إذا اتسع الفاصل بين الاسم والضمير

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التعريف، متوسطة في وضوح الإحالة الضميرية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0007 — المجموعات المهمة والسلاسل، وقوع ١:**
  - **الأصل:** [السطر ٥٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/important-sets.tex#L57). الشاهد المسجل: «``letters'' from $A$, then we say \emph{length} of the string is~$n$».
  - **العربية المعيارية:** [السطر ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/important-sets.tex#L57)؛ الطبعة الدولية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: ««حروف» من $A$، فإننا نقول إن \emph{طول} السلسلة هو~$n$،».
  - **العربية التراثية:** [السطر ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/important-sets.tex#L52)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «من $A$، كان \emph{طولها}~$n$، وكتبنا $\len{x}=n$.».

## مجموعة فهرسة

الأصل الإنجليزي: `index set`. معرّف القرار: `locale-ar-chosen-3a785fb961dfc5fb`.

**المعنى المقصود:** المجموعة I التي تتخذ عناصرها أدلة i لعائلة المجموعات Aᵢ في الاتحاد والتقاطع المفهرسين، وليست دليلًا واحدًا أو مجموعة منتهية بالضرورة.

**سبب الاختيار:** تعطي صيغة الأصل Aᵢ لكل i∈I، فتفصل مجموعة الفهرسة I عن الدليل الفرد i. أبقت الطبعة «مجموعة فهرسة» على هذه الوظيفة، لكن المعجم المصور يطبع index set = «مجموعة أدلة»، ويشرح المثال نفسه A=⋃Aₖ؛ فهو شاهد مباشر لمفهوم I لا للفظ المختار. مع التقاطع المطلق أضاف النص العربي شرط عدم خلو I كي لا يصبح التقاطع بلا مجموعة كلية محددة.

**سؤال مفتوح:** هل يُفضّل «مجموعة أدلة» الموافقة للمعجم أم «مجموعة فهرسة» الأبْين لقارئ الحوسبة، مع حفظ الفرق بين I وi وشرط عدم خلو التقاطع؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٣٨-١٥٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L138-L150) — الأصل يعرف I بوصفها حاملة جميع الأدلة المستخدمة في Aᵢ ويميز الاتحاد من التقاطع.

**مواضع المعجم المعاينة:** [ص ٣٥٦ من PDF (المطبوعة ٣٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=356)

**حدود الشاهد المعجمي:** PDF ص ٣٥٦ (المطبوعة ٣٤٤) يطبع index set = «مجموعة أدلة» ويعرض عائلة Aₖ، لا يطبع «مجموعة فهرسة». هذا خلاف لفظي صريح لا شهادة على اللفظ الحالي.

**بديل جدير بالمقارنة:** مجموعة أدلة؛ المدخل المعجمي المباشر؛ مجموعة المؤشرات؛ قد توضح وظيفة i لكنها تحتاج بحث استعمال مستقل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تحديد I ومداها، متوسطة في اختيار اللفظ المخالف للمعجم.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ١:**
  - **الأصل:** [السطر ١٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L138). الشاهد المسجل: «We could also do the same for a sequence of sets $A_1$, $A_2$, \dots \begin{align*} \bigcup_i A_i & = \Setabs{x}{x \text{ belongs to one of the } A_i}\\ \bigcap_i A_i & = \Setabs{x}{x \text{ belongs to every } A_i}. \end{align*} When we have an \emph{index}…».
  - **العربية المعيارية:** [السطر ١٤٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L142)؛ الطبعة الدولية: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=36) (ترقيم المتن: ٣٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ويمكننا فعل الأمر نفسه لمتتالية من المجموعات $A_1$، $A_2$، \dots \begin{align*} \bigcup_i A_i & = \Setabs{x}{x \text{ ينتمي إلى إحدى المجموعات } A_i}\\ \bigcap_i A_i & = \Setabs{x}{x \text{ ينتمي إلى كل } A_i}. \end{align*} وعندما تكون لدينا \emph{مجموعة فه…».

## مجموعة غير خالية من المجموعات

الأصل الإنجليزي: `intersection`. معرّف القرار: `semantic-propagation-20260906:0008-P1`.

**المعنى المقصود:** يمكن اتحاد عائلة مجموعات خالية أو غير خالية، أما تقاطعها المطلق في هذا السياق فيحتاج عائلة غير خالية ما لم تُحدد مجموعة كلية حاضنة.

**سبب الاختيار:** يقول الأصل إن التقاطع يحوي كل ما ينتمي إلى جميع عناصر عائلة A من غير أن يقيد A بعدم الخلو. إذا كانت A خالية صدق الشرط لكل شيء، فلا يعيّن مجموعة من غير كليّ حاضن. أضافت التراثية والطبعة المعاصرة شرط عدم الخلو عند تعريف التقاطع والمجموعة المفهرسة، وأبقتا اتحاد الخالية ممكنًا؛ وهذا تصحيح نطاق رياضي لا مجرد مفردة بديلة.

**سؤال مفتوح:** هل التنبيه على العائلة غير الخالية واضح في التعريفين، ولا يوهم بمنع اتحاد العائلة الخالية أو تقاطعها النسبي إلى كليّ محدد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٠٠-١٠٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L100-L106) — جملة تقديم الاتحاد والتقاطع لجميع عناصر العائلة هي موضع التعميم الذي يحتاج قيدًا.

**مواضع المعجم المعاينة:** [ص ٣٧٠ من PDF (المطبوعة ٣٥٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=370)، [ص ٧٥٤ من PDF (المطبوعة ٧٤٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=754)

**حدود الشاهد المعجمي:** PDF ص ٣٧٠ (المطبوعة ٣٥٨) يعرف intersection للمجموعات، وص ٧٥٤ (المطبوعة ٧٤٢) الاتحاد حتى في عائلة مجموعات؛ لا يحسم المدخلان وحدهما تقاطع العائلة الخالية من دون كليّ. القيد مستند إلى تحليل الصيغة الأصلية.

**بديل جدير بالمقارنة:** تعريف تقاطع الخالية بالنسبة إلى مجموعة كلية محددة؛ جائز في سياق آخر لكنه غير معطى هنا

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في لزوم القيد وترك الاتحاد بلا تضييق.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ١:**
  - **الأصل:** [السطر ١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L100). الشاهد المسجل: «We can also form the union or intersection of more than two».
  - **الأصل:** [السطر ١٠٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L103). الشاهد المسجل: «(or intersection) of into a single set. Then we can define the union».
  - **الأصل:** [السطر ١٠٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L105). الشاهد المسجل: «least one !!{element} of the set, and the intersection as the set of».
  - **العربية المعيارية:** [السطر ١٢٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L120)؛ الطبعة الدولية: [ص ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=35) (ترقيم المتن: ٣٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=35) (ترقيم المتن: ٣٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إذا كانت $A$ مجموعة غير خالية من المجموعات، فإن $\bigcap A$ هي مجموعة الكائنات».
  - **العربية التراثية:** [السطر ١١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L113)؛ الطبعة التراثية: [ص ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=35) (ترقيم المتن: ٣٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لتكن $A$ مجموعة غير خالية من المجموعات. فتقاطعها $\bigcap A$ يجمع ما تشترك».

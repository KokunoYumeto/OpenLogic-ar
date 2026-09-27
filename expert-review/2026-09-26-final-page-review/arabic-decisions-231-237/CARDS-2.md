# بطاقات القطر والصفوف والضبط الكتابي — القرارات ٢٣٤–٢٣٧

[الرجوع إلى مقدمة الدفعة](README.md)

## بقراءة عناصر قطر المصفوفة أعلاه على التوالي

الأصل الإنجليزي: `Read down an infinite diagonal at every positive index`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0033-REPAIR-G13-20260907`.

**المعنى المقصود:** تقرأ القيم s_n(n) على القطر لكل رتبة موجبة n، ثم تقلب كل صفر وواحد لتنشئ متتالية خارجة عن كل قائمة مفترضة.

**سبب الاختيار:** تعريف الأصل يعطي قيمة المتتالية الجديدة لكل n في PosInt، لا نهاية أخيرة لقراءة القطر. استعملت التراثية «بقراءة عناصر قطر المصفوفة أعلاه على التوالي» لتدل على السير بحسب الرتب، مع إبقاء حالتي قلب الصفر والواحد والصيغة 1−s_n(n). يسمي المعجم Cantor’s diagonal process «إجرائية كانتور القطرية» ويشرح تغيير حد كل رتبة، شاهدًا مطابقًا لآلية البرهان ولو اختلف لفظ العملية.

**سؤال مفتوح:** هل «على التوالي» كافية ليفهم أن تعريف العنصر القطري يجري لكل n بلا مرحلة انتهاء، أم يحتاج النص إلى تصريح «في كل رتبة»؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٧-٩٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L87-L93) — المقطع الأصلي يربط التعريف الكلي بالقطر ويحدد قلب القيم عند كل رتبة.

**مواضع المعجم المعاينة:** [ص ٨٧ من PDF (المطبوعة ٧٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=87)، [ص ٥٠ من PDF (المطبوعة ٣٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=50)

**حدود الشاهد المعجمي:** PDF ص ٨٧، المطبوعة ٧٥، يطبع «إجرائية كانتور القطرية» ويشرح تغيير حد كل رتبة؛ وص ٥٠ يعرف الصفيفة ذات الصفوف والأعمدة.

**بديل جدير بالمقارنة:** إجرائية كانتور القطرية؛ لفظ المعجم المعاين بدل «طريقة» المنشورة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في آلية كل رتبة، ومتوسطة في الاسم المختار للطريقة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٨٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L87). الشاهد المسجل: «To define $\overline{s}$, we specify what all its !!{element}s are, i.e., we specify $\overline{s}(n)$ for all $n \in \PosInt$. We do this by reading down the diagonal of the array above (hence the name ``diagonal method'') and then changing every $1$ to a…».
  - **العربية المعيارية:** [السطر ٩٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L90)؛ الطبعة الدولية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=71) (ترقيم المتن: ٧٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=71) (ترقيم المتن: ٧٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$\overline{s}(n)$ لكل $n \in \PosInt$. ونفعل ذلك بقراءة عناصر قطر المصفوفة أعلاه على التوالي (ومن هنا اسم «الطريقة القطرية»)، ثم نغير كل».

## أيًّا

الأصل الإنجليزي: `any function`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0033-REPAIR-NFC1-20260907`.

**المعنى المقصود:** الكتابة المعيارية لكلمة «أيًّا» تحفظ معنى العموم: لا تكون الدالة المفترضة شاملة أيًّا كانت.

**سبب الاختيار:** سجل التصويب تغيير ترتيب الشدة والتنوين في الموضع العربي إلى صيغة NFC فحسب، دون استبدال الكلمة أو المجال الكمي للعبارة «أيًّا كانت». الأصل يطلب نفي وجود أي دالة شاملة من PosInt إلى A غير الخالية؛ فالتطبيع الكتابي لا يغير هذا الشرط. صفحة المجموعة العدودة في المعجم سياق للمصطلح لا شاهد على ترتيب علامات التشكيل.

**سؤال مفتوح:** هل حفظت الطبعة عند عرضها «أيًّا» مع علامة التنوين والشدة من غير أن تختل القراءة أو نطاق الكم؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٣-٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L33-L38) — نفي وجود الدالة في الأصل هو الكم الذي لا يجوز لتطبيع العلامات أن يغيره.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يعرّف المجموعة العدودة؛ لا يقرر قاعدة NFC، ولذلك تؤخذ سلامة التطبيع من مقارنة البايتات والعبارة العربية.

**بديل جدير بالمقارنة:** إزالة التشكيل كله؛ تغير عرض الكلمة بلا حاجة ولا تستند إلى الأصل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في عدم تغير اللفظ والمعنى، ومتوسطة في العرض الطباعي على كل جهاز.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L33). الشاهد المسجل: «How would one prove that a set is !!{nonenumerable}? You have to show that no such surjective function can exist. Equivalently, you have to show that the elements of~$A$ cannot be enumerated in a one way infinite list. The best way to do this is to show tha…».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L25)؛ الطبعة التراثية: [ص ٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=67) (ترقيم المتن: ٦٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وطريق إثبات أن المجموعة غير الخالية !!{nonenumerable} أن ننفي إمكان تلك الدالة الشاملة؛ ومعناه أن عناصر~$A$ لا تستوعبها قائمة لا نهائية تمتد في جهة واحدة. ويكفينا لذلك أن نبين أن كل قائمة من !!{element}s~$A$ يفوتها عنصر على الأقل، أي إن الدالة $f\colon \Pos…».

## صفًّا

الأصل الإنجليزي: `row`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0033-REPAIR-NFC2-20260907`.

**المعنى المقصود:** ترتيب المتتاليات يجعل لكل متتالية صفًّا واحدًا في الجدول، وتوضع عناصرها في أعمدته بحسب الرتبة.

**سبب الاختيار:** الأصل يرتب قائمة المتتاليات في array بحيث تمثل كل واحدة صفًا، والتحويل المسجل يطبع «صفًّا» بترتيب علامات معيارية فقط دون مساس بموضع s_i(j). مدخل المعجم array «صفيفة» يشرح صفوفًا وأعمدة، بينما مدخل row يطبع «سطرًا»؛ «صف» لفظ الطبعة وفرق بين الشاهد المعجمي والاستخدام المنشور لا يجوز إخفاؤه.

**سؤال مفتوح:** هل «صف» في هذا الرسم أوضح من «سطر» المعجمي، وهل يظهر التنوين والشدة فيه ترتيبًا صحيحًا في PDF وEPUB؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٢-٦٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L62-L63) — جملة الأصل تعرض جدول المتتاليات الذي يحدد وظيفة كل صف وكل عمود.

**مواضع المعجم المعاينة:** [ص ٥٠ من PDF (المطبوعة ٣٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=50)، [ص ٦٢٢ من PDF (المطبوعة ٦١٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=622)

**حدود الشاهد المعجمي:** PDF ص ٥٠، المطبوعة ٣٨، يشرح array «صفيفة» ذات صفوف وأعمدة؛ وص ٦٢٢، المطبوعة ٦١٠، يسمي row «سطرًا» في الصفيفة.

**بديل جدير بالمقارنة:** سطرًا؛ اللفظ المعجمي، وقد يكون أقل مألوفية في وصف صفوف هذا الجدول

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في بنية الجدول وثبات الرمز، ومتوسطة في المفاضلة بين صف وسطر.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٦٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L62). الشاهد المسجل: «We may arrange this list, and the elements of each sequence $s_i$ in it, in an array:».
  - **العربية التراثية:** [السطر ٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L40)؛ الطبعة التراثية: [ص ٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=67) (ترقيم المتن: ٦٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ونعرض القائمة في مصفوفة، نجعل لكل متتالية~$s_i$ صفًّا ترتب فيه عناصرها:».

## قطريًّا

الأصل الإنجليزي: `diagonalization`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0033-REPAIR-NFC3-20260907`.

**المعنى المقصود:** البرهان القطري يستعمل قطر ترتيب القيم لتكوين متتالية جديدة، وقد يطبق المعنى نفسه من غير رسم قطر ظاهر.

**سبب الاختيار:** التغيير الموثق في التراثية لا يزيد على توحيد ترتيب الشدة والتنوين في «قطريًّا»، لا استبدال الحجة أو الصيغة. يشرح الأصل مباشرة أن diagonalization قد تستعمل بلا صفيفة مرسومة. مدخل المعجم لطريقة كانتور القطرية يشرح مثال تغيير حدود متتالية، لكنه لا يقيد كل تطبيق بوجود رسم هندسي.

**سؤال مفتوح:** هل يظل الفرق بين مبدأ الحجة القطرية والرسم الجدولي ظاهرًا للقارئ، مع سلامة ضبط «قطريًّا» في الملفات المعروضة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٤٠-١٤٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L140-L144) — الجملة الأصلية تفصل الاسم المستمد من القطر عن إمكان تطبيق الطريقة بلا صفيفة مرسومة.

**مواضع المعجم المعاينة:** [ص ٨٧ من PDF (المطبوعة ٧٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=87)

**حدود الشاهد المعجمي:** PDF ص ٨٧ يطبع «إجرائية كانتور القطرية» ويصف تغيير الحدود؛ لا يجعل الرسم المصفوفي لازمًا لكل برهان قطري.

**بديل جدير بالمقارنة:** طريقة قطرية؛ صحيح للآلية العامة لكنه أقل تحديدًا لاسم العملية في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في ثبات المعنى والبرهان، ومتوسطة في العرض الطباعي للعلامات.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ١٤٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L140). الشاهد المسجل: «This proof method is called ``diagonalization'' because it uses the diagonal of the array to define~$\overline{s}$. Diagonalization need not involve the presence of an array: we can show that sets are not !!{enumerable} by using a similar idea even when no…».
  - **العربية التراثية:** [السطر ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L78)؛ الطبعة التراثية: [ص ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=68) (ترقيم المتن: ٦٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إنما سمي هذا الاستدلال قطريًّا لأخذ تعريف~$\overline{s}$ من قطر المصفوفة. وليس وجود المصفوفة شرطًا في الاستدلال القطري؛ فقد نستعمل معناه لإثبات أن مجموعات ليست !!{enumerable}، من غير أن نرسم مصفوفة أو نعين قطرًا ظاهرًا.».

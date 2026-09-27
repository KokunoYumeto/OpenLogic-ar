# بطاقات كوشي وعنوان اللانهائية — القرارات ٤١٢–٤١٥

[الرجوع إلى مقدمة الدفعة](README.md)

## متتالية كوشي

الأصل الإنجليزي: `Cauchy sequence`. معرّف القرار: `retro-0005-0050:emphasis:7ad1261c86e82443`.

**المعنى المقصود:** متتالية قيمها نسبية وتحقق شرط كوشي: تصير المسافة بين أي حدين متأخرين أصغر من كل مقدار موجب معطى.

**سبب الاختيار:** يستعمل الملحق شرط كوشي لبناء الأعداد الحقيقية من متتاليات النسبية، لا مجرد تقارب مفترض سلفًا. أبقت الطبعتان «متتالية كوشي»؛ يطبع المعجم المدخل الكامل نفسه ويشرحه بعبارة تقارب حدود المتتالية وفق الشرط القياسي. لا نساوي بين موضوع البناء في الكتاب وبين افتراض وجود النهاية داخله.

**سؤال مفتوح:** هل تبقى «متتالية كوشي» رأسًا مشتركًا للطبعات، مع فهرسة «متتابعة كوشي» بوصفها مرادفًا إقليميًا إن ثبت استعماله؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cauchy.tex#L84) — يعطي موضع الملحق شرط المتتالية المستعمل في بناء الحقيقية.

**وجه جمع المواضع:** يعطي موضع الملحق شرط المتتالية المستعمل في بناء الحقيقية.

**مواضع المعجم المعاينة:** [ص ٩٦ من PDF (المطبوعة ٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=96)

**حدود الشاهد المعجمي:** PDF ص ٩٦، المطبوعة ٨٤، يطبع Cauchy’s sequence = «متتالية كوشي» ويذكر شرط كوشي. يشهد للمصطلح نفسه، لا لكل تفصيل في بناء الكتاب.

**بديل جدير بالمقارنة:** متتابعة كوشي؛ مرادف محتمل غير مثبت في الصفحة المفحوصة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في مطابقة الرأس المعجمي، ومتوسطة في حصر المرادفات الإقليمية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0048 — بناء الحقيقية بمتتاليات كوشي، وقوع ١:**
  - **الأصل:** [السطر ٨٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cauchy.tex#L84). الشاهد المسجل: «A function $f: \Nat \to \Rat$ is a \emph{Cauchy sequence} iff for».
  - **العربية المعيارية:** [السطر ٧٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cauchy.tex#L79)؛ الطبعة الدولية: [ص ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=99) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=99) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الدالة $f: \Nat \to \Rat$ \emph{متتالية كوشي} إذا وفقط إذا كان لكل».
  - **العربية التراثية:** [السطر ٤٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cauchy.tex#L42)؛ الطبعة التراثية: [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الدالة $f: \Nat \to \Rat$ \emph{متتالية كوشي} إذا وفقط إذا تحقق، لكل $\epsilon \in \Rat$ موجب، أن $(\exists \ell \in».

## ملحق: بناء الحقيقية بمتتاليات كوشي

الأصل الإنجليزي: `Appendix: the Reals as Cauchy Sequences`. معرّف القرار: `retro-0005-0050:section:d2571fc259657b3e`.

**المعنى المقصود:** عنوان ملحق يبين طريقة إنشاء الأعداد الحقيقية باستعمال متتاليات كوشي.

**سبب الاختيار:** يقول الأصل «الحقيقية بوصفها متتاليات كوشي» في العنوان؛ نقلت التراثية معنى التمثيل البنائي إلى «بناء الحقيقية بمتتاليات كوشي». هذا أدق للقارئ حين لا يراد مساواة العدد والمتتالية الخام دون علاقة التكافؤ. تحفظ المعيارية عبارة «بوصفها» بوصفها مقابلة صالحة للمراجعة.

**سؤال مفتوح:** هل يوضح عنوان «بناء الحقيقية بمتتاليات كوشي» مقصد الملحق من غير أن يبتعد أكثر مما يلزم عن عنوان الأصل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cauchy.tex#L11) — عنوان الأصل والمدخل اللاحق يحددان أن الكلام عن طريقة التمثيل والبناء.

**وجه جمع المواضع:** عنوان الأصل والمدخل اللاحق يحددان أن الكلام عن طريقة التمثيل والبناء.

**مواضع المعجم المعاينة:** [ص ٩٦ من PDF (المطبوعة ٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=96)

**حدود الشاهد المعجمي:** PDF ص ٩٦، المطبوعة ٨٤، يثبت «متتالية كوشي» فقط؛ لا يملي اختيار حرف الجر أو تركيب عنوان الملحق.

**بديل جدير بالمقارنة:** الأعداد الحقيقية بوصفها متتاليات كوشي؛ صيغة المعيارية الأقرب إلى بنية العنوان الإنجليزي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: موضع الأصل والنص الجاري مثبتان، ويبقى الحكم الاصطلاحي أو الأسلوبي مفتوحًا للتصحيح.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0048 — بناء الحقيقية بمتتاليات كوشي، وقوع ١:**
  - **الأصل:** [السطر ١١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cauchy.tex#L11). الشاهد المسجل: «\olsection{Appendix: the Reals as Cauchy Sequences}».
  - **العربية المعيارية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cauchy.tex#L11)؛ الطبعة الدولية: [ص ٩٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=98) (ترقيم المتن: ٩٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=98) (ترقيم المتن: ٩٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{ملحق: الأعداد الحقيقية بوصفها متتاليات كوشي}».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cauchy.tex#L11)؛ الطبعة التراثية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=94) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{ملحق: بناء الحقيقية بمتتاليات كوشي}».

## المجموعات اللانهائية

الأصل الإنجليزي: `Infinite Sets`. معرّف القرار: `retro-0005-0050:chapter:6c3c94b578a548de`.

**المعنى المقصود:** عنوان فصل المجموعات التي لا ينتهي عدد عناصرها.

**سبب الاختيار:** المعجم يجيز «مجموعة لانهائية» إلى جانب «مجموعة غير منتهية» لرأس infinite set؛ لذلك جاء جمعها «المجموعات اللانهائية» مطابقًا لنطاق عنوان الفصل. لا يدل العنوان بمفرده على أي تعريف خاص، كاللانهائية بحسب ديديكند، قبل تقريره في المتن.

**سؤال مفتوح:** هل يفضل إبقاء العنوان «المجموعات اللانهائية»، وفصل تعريف ديديكند الخاص في موضعه من الفصل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/infinite/infinite.tex#L8) — عنوان الأصل جمع عام للمجموعات اللانهائية قبل تفصيل التعريفات.

**وجه جمع المواضع:** عنوان الأصل جمع عام للمجموعات اللانهائية قبل تفصيل التعريفات.

**مواضع المعجم المعاينة:** [ص ٣٥٩ من PDF (المطبوعة ٣٤٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=359)

**حدود الشاهد المعجمي:** PDF ص ٣٥٩، المطبوعة ٣٤٧، يطبع infinite set «مجموعة غير منتهية (مجموعة لانهائية)»؛ صيغة العنوان جمع للمرادف الثاني.

**بديل جدير بالمقارنة:** المجموعات غير المنتهية؛ المرادف الأول في المدخل المعجمي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: موضع الأصل والنص الجاري مثبتان، ويبقى الحكم الاصطلاحي أو الأسلوبي مفتوحًا للتصحيح.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0049 — المجموعات اللانهائية، وقوع ١:**
  - **الأصل:** [السطر ٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/infinite/infinite.tex#L8). الشاهد المسجل: «\olchapter{sfr}{infinite}{Infinite Sets}».
  - **العربية المعيارية:** [السطر ٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/infinite/infinite.tex#L8)؛ الطبعة الدولية: [ص ١٠٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=102) (ترقيم المتن: ١٠١)، [ص ١٠٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=103) (ترقيم المتن: ١٠٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١٠٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=102) (ترقيم المتن: ١٠١)، [ص ١٠٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=103) (ترقيم المتن: ١٠٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olchapter{sfr}{infinite}{المجموعات اللانهائية}».
  - **العربية التراثية:** [السطر ٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/infinite/infinite.tex#L8)؛ الطبعة التراثية: [ص ٩٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=98) (ترقيم المتن: ٩٧)، [ص ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=99) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olchapter{sfr}{infinite}{المجموعات اللانهائية}».

## نأخذ

الأصل الإنجليزي: `help ourselves`. معرّف القرار: `retro-0005-0050:emphasis:947f3291cb4df666`.

**المعنى المقصود:** أخذ مجموعة لانهائية معطاة على سبيل الفرض في مدخل الفصل، لا تقرير إنشائها أو إثبات وجودها.

**سبب الاختيار:** تؤدي «نأخذ» فعل الاستعانة بكائن مفروض في البرهان دون أن تجعله نتيجة مستنبطة. صيغة المعيارية «نفترض» أدل على الشرط المنطقي الصريح؛ وفي التراثية ينتج معنى الفرض من السياق المحيط بالمجموعة التي نختارها.

**سؤال مفتوح:** هل يفهم القارئ «نأخذ» على أنه فرض العمل في هذا الموضع، أم تحتاج العبارة إلى تصريح بالافتراض؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/infinite/hilberts-hotel.tex#L13) — العبارة الأصلية تمهد لاختيار مجموعة لأجل الحجة التالية، لا لبرهان وجودها.

**وجه جمع المواضع:** العبارة الأصلية تمهد لاختيار مجموعة لأجل الحجة التالية، لا لبرهان وجودها.

**انطباق المعجم الرياضي:** يتعلق القرار بسبك الجملة أو بنطاق القضية؛ لا يقرر مدخل المعجم الرياضي سلامة هذا الربط البرهاني.

**بديل جدير بالمقارنة:** نفترض؛ صيغة المعيارية الأصرح في الإشارة إلى الفرض

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: موضع الأصل والنص الجاري مثبتان، ويبقى الحكم الاصطلاحي أو الأسلوبي مفتوحًا للتصحيح.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0050 — المجموعات اللانهائية، وقوع ١:**
  - **الأصل:** [السطر ١٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/infinite/hilberts-hotel.tex#L13). الشاهد المسجل: «want to \emph{help ourselves} to the natural numbers, our first step».
  - **العربية المعيارية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/infinite/hilberts-hotel.tex#L13)؛ الطبعة الدولية: [ص ١٠٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=103) (ترقيم المتن: ١٠٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١٠٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=103) (ترقيم المتن: ١٠٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{نفترض} الأعداد الطبيعية معطاة لنا، وجب أن تكون خطوتنا الأولى».
  - **العربية التراثية:** [السطر ١٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/infinite/hilberts-hotel.tex#L12)؛ الطبعة التراثية: [ص ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=99) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لا ريب في أن مجموعة الأعداد الطبيعية لا نهائية. فإذا لم نرد أن \emph{نأخذ} الطبيعية معطاة لنا، وجب أولًا وصف المجموعة اللانهائية بعبارة لا تتوقف على ذكر الأعداد الطبيعية نفسها. ولهذا عرض هيلبرت في محاضرة سنة 1924 تصويرًا حسنًا، فدعانا إلى تخيل».

# بطاقات شروط القطع — القرارات ٣٧٩–٣٨٥

[الرجوع إلى مقدمة الدفعة](README.md)

## عدم الخلو والجزئية الحقيقية

الأصل الإنجليزي: `non-empty, proper`. معرّف القرار: `retro-0005-0050:emphasis:0adb1c1144d899b7`.

**المعنى المقصود:** شرطا قطع ديديكند الأوليان: ألا يخلو من النسبية وألا يساوي مجموعة النسبية كلها.

**سبب الاختيار:** الأصل يكتب ∅≠α⊊Q تحت non-empty, proper. جعلت التراثية الاسمين «عدم الخلو والجزئية الحقيقية» ليكونا عنوانًا موحدًا لبند الشرط، والصيغة الرياضية تمنع حمل proper على معنى أخلاقي أو إتقان. لكن المعجم يطبع proper subset «مجموعة جزئية فعلية»؛ الفرق اللفظي يستحق مراجعة.

**سؤال مفتوح:** هل «الجزئية الحقيقية» مفهومة في شرط α⊊Q أم تفضل «الجزئية الفعلية» المعجمية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L31) — الرمزان يضبطان معنى عدم الخلو والجزئية غير المساوية.

**وجه جمع المواضع:** الرمزان يضبطان معنى عدم الخلو والجزئية غير المساوية.

**مواضع المعجم المعاينة:** [ص ٥٧١ من PDF (المطبوعة ٥٥٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=571)

**حدود الشاهد المعجمي:** PDF ص ٥٧١، المطبوعة ٥٥٩، يطبع proper subset = «مجموعة جزئية فعلية» ويشرح أنها ليست المجموعة الأم كلها؛ «حقيقية» مرادف طبعة غير مطبوع في هذا المدخل.

**بديل جدير بالمقارنة:** عدم الخلو والجزئية الفعلية؛ يوافق رأس المعجم للجزئية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الشرط الرمزي، متوسطة في تفضيل «حقيقية» على «فعلية».

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L31). الشاهد المسجل: «\item \emph{non-empty, proper}: $\emptyset \neq \alpha \subsetneq \Rat$».
  - **العربية المعيارية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L28)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item \emph{غير خالٍ وحقيقي}: $\emptyset \neq \alpha \subsetneq \Rat$».
  - **العربية التراثية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L19)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item \emph{عدم الخلو والجزئية الحقيقية}: $\emptyset \neq \alpha \subsetneq \Rat$».

## انتفاء العنصر الأعظم

الأصل الإنجليزي: `no maximum`. معرّف القرار: `retro-0005-0050:emphasis:176f1c83fed78096`.

**المعنى المقصود:** لا يوجد في القطع عنصر أعظم؛ لكل عدد نسبي داخله عدد أكبر منه لا يزال داخله.

**سبب الاختيار:** يوضح الأصل no maximum فورًا بكمّية لكل ف∈α يوجد ق∈α أكبر منه. جعلت التراثية عنوان البند «انتفاء العنصر الأعظم»، فسمّت غياب العنصر لا غياب حد علوي خارجي؛ وهذا فرق لازم في تعريف القطع. لم يظهر في البحث المعجمي المحدود مدخل maximum element مطابق، فتسند الصيغة الرياضية المعنى لا شاهدًا اصطلاحيًا مدعى.

**سؤال مفتوح:** هل يقي «انتفاء العنصر الأعظم» من الخلط بين عدم وجود أكبر عضو وعدم وجود حد علوي للمجموعة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L33) — الكمية التابعة للعنوان تفصل الأكبر عضوًا عن الحد العلوي الخارجي.

**وجه جمع المواضع:** الكمية التابعة للعنوان تفصل الأكبر عضوًا عن الحد العلوي الخارجي.

**نتيجة البحث المعجمي المحدود:** لم يظهر رأس maximum element أو greatest element في البحث المحدود للمعجم المصور؛ هذا لا ينفي وجوده في أدبيات أخرى، وصيغة الأصل الكمية هي شاهد المعنى هنا.

**بديل جدير بالمقارنة:** لا قيمة عظمى له؛ صيغة المعيارية وقد تلتبس بحد أعلى غير محقق

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت وقوع الأصل والترجمة، لكن أفضلية السبك تحتاج نظر قارئ خبير.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L33). الشاهد المسجل: «\item \emph{no maximum}: for all $p \in \alpha$ there is a $q \in \alpha$ such that $p < q$».
  - **العربية المعيارية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L30)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠)، [ص ٩٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=92) (ترقيم المتن: ٩١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠)، [ص ٩٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=92) (ترقيم المتن: ٩١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item \emph{لا قيمة عظمى له}: لكل $p \in \alpha$ يوجد $q \in \alpha$ بحيث $p < q$».
  - **العربية التراثية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L21)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦)، [ص ٨٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=88) (ترقيم المتن: ٨٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item \emph{انتفاء العنصر الأعظم}: لكل $p \in \alpha$ يوجد $q \in \alpha$ يحقق $p < q$».

## القطع

الأصل الإنجليزي: `cut`. معرّف القرار: `retro-0005-0050:emphasis:7927db879ef8c967`.

**المعنى المقصود:** قطع ديديكند ممثلًا بنصف سفلي غير خال وحقيقي وابتدائي وبلا عنصر أعظم.

**سبب الاختيار:** يسمي الأصل cut مجموعة جزئية من النسبية وفق الشروط الأربعة اللاحقة. عرّفته التراثية «القطع» باسم عام سابق ثم بسطت الشروط؛ المعجم يطبع «مقطع ديديكند» ويعرضه بزوج نصفي الفصل، لا بهذه الصورة السفلى المنفردة. تتكافأ الصورتان في السياق المناسب لكن لا ندعي حرفية المدخل للصياغة المختارة.

**سؤال مفتوح:** هل الاسم المختصر «القطع» كاف بعد نسبة البناء إلى ديديكند، أم ينبغي «مقطع ديديكند» المعجمي عند التعريف؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L27) — تعريف الأصل نفسه يجعل القطع نصفًا سفليًا بالشروط المدرجة.

**وجه جمع المواضع:** تعريف الأصل نفسه يجعل القطع نصفًا سفليًا بالشروط المدرجة.

**مواضع المعجم المعاينة:** [ص ١٧٥ من PDF (المطبوعة ١٦٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=175)

**حدود الشاهد المعجمي:** PDF ص ١٧٥، المطبوعة ١٦٣، يطبع Dedekind cut = «مقطع ديديكند» ويصف فصل المجال إلى نصفيه؛ ليس فيه رأس cut المختصر بالمعنى نفسه.

**بديل جدير بالمقارنة:** مقطع ديديكند؛ الاسم المباشر في المعجم؛ قطعة؛ قد تلتبس بالقطعة الابتدائية وحدها

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في شروط التعريف، متوسطة في الاسم المختصر.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L27). الشاهد المسجل: «A \emph{cut} $\alpha$ is any non-empty proper».
  - **العربية المعيارية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L25)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الـ\emph{قطع} $\alpha$ هو كل مقطع ابتدائي حقيقي غير خالٍ من الأعداد».
  - **العربية التراثية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L17)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{القطع} $\alpha$ مقطع ابتدائي من الأعداد النسبية، غير خال، وليس هو النسبية كلها، ولا عنصر أعظم فيه. أي إن $\alpha$ قطع إذا وفقط إذا استوفى الشروط:».

## كونه ابتدائيًّا

الأصل الإنجليزي: `initial`. معرّف القرار: `retro-0005-0050:emphasis:a45a9371b1a38d81`.

**المعنى المقصود:** القطع ابتدائي في ترتيب النسبية: إذا كان ق داخله وكل ف<ق، فف داخله أيضًا.

**سبب الاختيار:** وضع الأصل initial على شرط الإغلاق إلى الأسفل. حوّلت التراثية الصفة إلى مصدر مؤول «كونه ابتدائيًّا» ليطابق عناوين الشروط الأخرى، وأبقت الصيغة الكمية التي تعين اتجاه الترتيب. المعجم يطبع «قطعة ابتدائية» ويذكر في الترتيب جميع العناصر الأصغر من حد معين؛ شاهد للمفهوم لا للعبارة النحوية كلها.

**سؤال مفتوح:** هل «كونه ابتدائيًّا» مع الصيغة كافٍ لتمييز الإغلاق نحو الأصغر من مفهوم البداية الزمني؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L32) — سطر الأصل يقرن initial بشرط دخول كل عنصر أصغر.

**وجه جمع المواضع:** سطر الأصل يقرن initial بشرط دخول كل عنصر أصغر.

**مواضع المعجم المعاينة:** [ص ٣٦١ من PDF (المطبوعة ٣٤٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=361)

**حدود الشاهد المعجمي:** PDF ص ٣٦١، المطبوعة ٣٤٩، يطبع initial segment = «قطعة ابتدائية» وفي أحد معانيه عناصر الترتيب الأصغر من حد؛ اسم الصفة في الطبعة مشتق من هذا المفهوم.

**بديل جدير بالمقارنة:** الابتدائية؛ أقصر لكنه لا يطابق نسق عناوين الشروط

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت وقوع الأصل والترجمة، لكن أفضلية السبك تحتاج نظر قارئ خبير.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L32). الشاهد المسجل: «\item \emph{initial}: for all $p,q \in \Rat$: if $p < q \in \alpha$ then $p \in \alpha$».
  - **العربية المعيارية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L29)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item \emph{ابتدائي}: لكل $p,q \in \Rat$: إذا كان $p < q \in \alpha$ فإن $p \in \alpha$».
  - **العربية التراثية:** [السطر ٢٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L20)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦)، [ص ٨٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=88) (ترقيم المتن: ٨٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item \emph{كونه ابتدائيًّا}: لكل $p,q \in \Rat$، من $p < q \in \alpha$ يلزم $p \in \alpha$».

## قطوعًا

الأصل الإنجليزي: `cuts`. معرّف القرار: `retro-0005-0050:emphasis:a8f5c793153aff6b`.

**المعنى المقصود:** القطوع التي تمثل الأعداد الحقيقية في بناء ديديكند، بصيغة الجمع المنصوب.

**سبب الاختيار:** يجعل الأصل reals as the cuts التي تفصل النسبية. سبكت التراثية الجملة «نجعل الأعداد الحقيقية قطوعًا» فجاء الجمع نكرةً منصوبًا بعد فعل الجعل؛ لا يغير التنكير تعريف القطع الآتي. المعجم يورد الاسم المركب «مقطع ديديكند»، فلا نحتج به لإثبات جمع «قطوع» حرفيًا.

**سؤال مفتوح:** هل جمع «قطوعًا» طبيعي بعد فعل «نجعل»، أم أن «مقاطع ديديكند» أظهر قبل التعريف الرسمي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L17) — الموضع يقترح جعل الحقيقية هي فواصل النسبية في البناء.

**وجه جمع المواضع:** الموضع يقترح جعل الحقيقية هي فواصل النسبية في البناء.

**مواضع المعجم المعاينة:** [ص ١٧٥ من PDF (المطبوعة ١٦٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=175)

**حدود الشاهد المعجمي:** PDF ص ١٧٥ يسمي الأصل النظري «مقطع ديديكند» مفردًا؛ صيغة الجمع «قطوع» اختيار تحرير الطبعة وليست مدخلًا مصورًا.

**بديل جدير بالمقارنة:** مقاطع ديديكند؛ موافقة للاسم المعجمي لكنها أطول في صدر الشرح

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت وقوع الأصل والترجمة، لكن أفضلية السبك تحتاج نظر قارئ خبير.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ١٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L17). الشاهد المسجل: «reals as the \emph{cuts} that partition the rationals. That is, we».
  - **العربية المعيارية:** [السطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L16)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الأعداد الحقيقية ببساطة على أنها \emph{القطوع} التي تقسم الأعداد».
  - **العربية التراثية:** [السطر ١٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L12)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «تدل خاصية الاكتمال، في جوهرها، على أن كل نقطة $\alpha$ من المستقيم الحقيقي تفصل ما على جانبيها فصلًا تامًّا: فهي $\alpha$ أصغر حد علوي للجانب الأدنى، وهي $\alpha$ أكبر حد سفلي للجانب الأعلى. ومن هنا اقترح ديديكند، في \emph{بناء} الأعداد الحقيقية من النسبية،…».

## الأدنى

الأصل الإنجليزي: `bottom`. معرّف القرار: `retro-0005-0050:emphasis:e987ccf680685811`.

**المعنى المقصود:** النصف الأدنى من النسبية الناتج من القطع، الذي يكفي لتعيين التقسيم كله.

**سبب الاختيار:** يشرح الأصل أن تعيين bottom half يكفي لتعيين الآخر. اختارت التراثية «الأدنى» لتربط النصف باتجاه ترتيب النسبية، لا بمكان هندسي سفلي في الصفحة؛ المعنى الرياضي يثبته شرح الفصل اللاحق لا مدخل «نصف» في المعجم.

**سؤال مفتوح:** هل «الأدنى» يبين اتجاه ترتيب الأعداد أو قد يوهم أنه نصف أصغر مقدارًا لا النصف الأسفل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L23) — النصف المذكور هو المجموعة الابتدائية التي تحدد القطع.

**وجه جمع المواضع:** النصف المذكور هو المجموعة الابتدائية التي تحدد القطع.

**انطباق المعجم الرياضي:** هذا الاختيار في تركيب العبارة أو توكيدها، لا في تسمية كائن رياضي مستقلة؛ فلا نستعمل المعجم الرياضي شاهدًا لحرفية هذا الأسلوب.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت وقوع الأصل والترجمة، لكن أفضلية السبك تحتاج نظر قارئ خبير.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ٢٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L23). الشاهد المسجل: «\emph{bottom} half. So, getting precise, we offer the following».
  - **العربية المعيارية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L21)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «التقسيم الذي أحدثناه تعيينًا وحيدًا بمجرد النظر إلى نصفه \emph{السفلي}.».
  - **العربية التراثية:** [السطر ١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L14)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ولنحقق هذا التصور. إذا فصلنا الأعداد النسبية نصفين، كفى تعيين النصف \emph{الأدنى} لتعيين التقسيم كله تعيينًا وحيدًا. فنضبطه بالتعريف الآتي.».

## القطع

الأصل الإنجليزي: `Cut`. معرّف القرار: `retro-0005-0050:named-defn:7b83ecc9edaa46dd`.

**المعنى المقصود:** اسم التعريف الرسمي لمقطع ديديكند في صورة المجموعة الجزئية الدنيا من النسبية.

**سبب الاختيار:** عنوان التعريف Cut يتلوه تعداد عدم الخلو والجزئية الحقيقية والابتدائية وانتفاء الأكبر. أبقت التراثية «القطع» معرّفًا بأل لأنه الاسم الذي قدمته قبل سطر التعريف؛ المعيارية تضع «قطع» نكرة. معجم دمشق يفضل «مقطع ديديكند» للاسم الكامل، وهو فرق نضعه أمام المراجع.

**سؤال مفتوح:** هل عنوان «القطع» مناسب في رأس التعريف، أم ينبغي توضيح النسبة إلى ديديكند منعًا لالتباس القطع الهندسي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L26) — العنوان يتبع شرح البناء مباشرة ويسبق الشروط الرسمية.

**وجه جمع المواضع:** العنوان يتبع شرح البناء مباشرة ويسبق الشروط الرسمية.

**مواضع المعجم المعاينة:** [ص ١٧٥ من PDF (المطبوعة ١٦٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=175)

**حدود الشاهد المعجمي:** PDF ص ١٧٥ يطبع Dedekind cut = «مقطع ديديكند»؛ عنوان الطبعة المختصر لا يطابق الاسم المعجمي كاملًا.

**بديل جدير بالمقارنة:** مقطع ديديكند؛ الاسم المعجمي الكامل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في ارتباط العنوان بالشروط، متوسطة في اختيار الاسم المختصر.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0045 — قطوع ديديكند، وقوع ١:**
  - **الأصل:** [السطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/cuts.tex#L26). الشاهد المسجل: «\begin{defn}[Cut]».
  - **العربية المعيارية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/cuts.tex#L24)؛ الطبعة الدولية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[قطع]».
  - **العربية التراثية:** [السطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/cuts.tex#L16)؛ الطبعة التراثية: [ص ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=87) (ترقيم المتن: ٨٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[القطع]».

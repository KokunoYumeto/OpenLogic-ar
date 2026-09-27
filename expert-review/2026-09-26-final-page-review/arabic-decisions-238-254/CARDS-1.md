# بطاقات اتجاه الاختزال والمجال المقابل — القرارات ٢٣٨–٢٤٢

[الرجوع إلى مقدمة الدفعة](README.md)

## لو كانت ℘(PosInt) قابلة للتعداد لكانت 2^ω قابلة للتعداد أيضًا

الأصل الإنجليزي: `if $\Pow{\PosInt}$ is enumerable then $\Bin^\omega$ is also enumerable`. معرّف القرار: `retro-0005-0050:emphasis:31aedb1bb056bdb4`.

**المعنى المقصود:** إذا أمكن تعداد مجموعة أجزاء الموجبات أمكن تعداد جميع المتتاليات الثنائية اللانهائية؛ هذه هي القضية الشرطية التي يقع نقض مقدمها لاحقًا.

**سبب الاختيار:** الأصل يبرز شرطًا ذا جهة واحدة، من تعداد مجموعة الأجزاء إلى تعداد المتتاليات، لا دعوى تكافؤ ولا تبديلًا للمقدم والتالي. نقلت التراثية ذلك بقرينة «لو ... لكانت»، وأبقت الرمزين كما هما. لا يقرر مدخل reduction المعجمي هذه الجهة، إذ يشرح اختزال الكسور، فتستند الجهة إلى بناء الأصل وبرهانه.

**سؤال مفتوح:** هل تظهر جهة الشرط بوضوح في الصياغة التراثية، أم توحي «لو» بدعوى امتناع قبل اكتمال البرهان؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٤-٢٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L24-L25) — هذه الجملة هي الدعوى المبرزة التي سيبرهنها النص لتؤدي إلى التناقض.

**مواضع المعجم المعاينة:** [ص ٦٠١ من PDF (المطبوعة ٥٨٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=601)

**حدود الشاهد المعجمي:** PDF ص ٦٠١، المطبوعة ٥٨٩، يذكر reduction «اختزال/اختصار» في الكسور؛ شاهد لفظي محدود، لا سند مباشر لاتجاه اختزال مسائل التعداد.

**بديل جدير بالمقارنة:** إذا وفقط إذا؛ مرفوضة لأنها تزيد اتجاهًا غير مبرهن في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الجهة المنطقية؛ متوسطة في المفاضلة الأسلوبية بين لو وإذا.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0034 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L24). الشاهد المسجل: «Show that \emph{if $\Pow{\PosInt}$ is !!{enumerable} then $\Bin^\omega$ is also !!{enumerable}}. Since we know $\Bin^\omega$ is not».
  - **العربية المعيارية:** [السطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/reduction.tex#L23)؛ الطبعة الدولية: [ص ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=73) (ترقيم المتن: ٧٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=73) (ترقيم المتن: ٧٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لإثبات أن $\Pow{\PosInt}$ !!{nonenumerable}: أثبت أنه \emph{إذا كانت $\Pow{\PosInt}$ !!{enumerable}، فإن $\Bin^\omega$ تكون أيضًا !!{enumerable}}. وبما أننا نعلم أن $\Bin^\omega$ ليست».
  - **العربية التراثية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction.tex#L17)؛ الطبعة التراثية: [ص ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=69) (ترقيم المتن: ٦٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «قد ثبت بالحجة القطرية أن $\Pow{\PosInt}$ !!{nonenumerable}، وكان قد سبق ثبوت ذلك لـ$\Bin^\omega$، أي مجموعة المتتاليات اللانهائية من~$0$ و~$1$، فهي !!{nonenumerable}. ويمكن أن نجعل النتيجة الثانية سبيلًا آخر إلى إثبات أن $\Pow{\PosInt}$ !!{nonenumerable}: ف…».

## مع أن المجال المقابل

الأصل الإنجليزي: `codomain of the corrected example`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0034-CODOMAIN-CLASSICAL-20260907`.

**المعنى المقصود:** المجال المقابل للدالة المصححة h هو مجموعة جميع المتتاليات الثنائية اللانهائية، لكن مداها الفعلي لا يملأ هذه المجموعة.

**سبب الاختيار:** كتب الأصل h من الموجبات إلى المتتاليات اللانهائية ثم أعطى قيمًا منتهية غير داخلة في مجالها المقابل. أصلحت الطبعة التراثية القيم إلى n أصفار يتلوها ذيل لا نهائي من الآحاد؛ وبعد التصحيح بقي المثال غير شامل لأن متتالية الآحاد وحدها، مثلًا، ليست صورة لأي n موجب. يسمي المعجم codomain «مجالًا مقابلًا لدالة» ويفرقه عن range، فاختير لفظ المجال المقابل في التنبيه بدل المدى.

**سؤال مفتوح:** هل يميز التنبيه التراثي بين صلاحية القيم للمجال المقابل وبين عدم شمول المدى، أم يلزمه مثال صريح لقيمة غير مصابة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩٩-١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L99-L100) — نوع الدالة المكتوب في الأصل يحدد المجموعة الهدف التي لا تنتمي إليها قيمه المنتهية.

**مواضع المعجم المعاينة:** [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)، [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ١١٢، المطبوعة ١٠٠: codomain «مجال مقابل لدالة»؛ وص ٥٩١، المطبوعة ٥٧٩: range «مدى». الفرق هنا بين الهدف وصور الدالة الفعلية.

**بديل جدير بالمقارنة:** المدى؛ مرفوض هنا لأنه مجموعة القيم المصابة لا المجموعة الهدف المكتوبة بعد السهم

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الفرق بين المجال المقابل والمدى وفي التصويب الرياضي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0034 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ٩٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L99). الشاهد المسجل: «defines a function $h\colon \PosInt \to \Bin^\omega$, but $\PosInt$ is !!{enumerable}.».
  - **العربية التراثية:** [السطر ٦٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction.tex#L66)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «جعل الأصل قيمة $h(n)$ سلسلة منتهية من الأصفار مع أن المجال المقابل».

## مع أن المجال المقابل

الأصل الإنجليزي: `codomain of the corrected example`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0034-CODOMAIN-MSA-20260907`.

**المعنى المقصود:** يذكر تنبيه الطبعة المعاصرة أن المتتاليات المنتهية لا تصلح قيمًا لدالة مجالها المقابل مجموعة المتتاليات اللانهائية.

**سبب الاختيار:** نوع h في الأصل هو PosInt→Bin^ω، فكل قيمة يجب أن تكون متتالية لا نهائية، ولو لم تكن الدالة شاملة. إصلاح المثال بإلحاق آحاد لا نهائية يزيل مخالفة النوع وحدها؛ ولا يثبت الشمول. اختارت الطبعة المعاصرة «المجال المقابل» المطابق لمدخل codomain المعجمي، لا «المدى» الذي يعني الصور الواقعة فعلًا.

**سؤال مفتوح:** هل يوضح النص المعاصر أن تصحيح قيم h لا يحول المثال إلى دالة شاملة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩٩-١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L99-L100) — عبارة الدالة في الأصل والمثال المنتهي موضع التنبيه المصحح في الطبعة المعاصرة.

**مواضع المعجم المعاينة:** [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)، [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ١١٢ يطبع codomain «مجال مقابل لدالة»، وص ٥٩١ يطبع range «مدى»؛ لا يجوز التبادل بينهما في حجة الشمول.

**بديل جدير بالمقارنة:** المدى؛ قد يتغير بتغير h ولا يعبر عن المجموعة الهدف المكتوبة في النوع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التمييز الاصطلاحي والرياضي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0034 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ٩٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L99). الشاهد المسجل: «defines a function $h\colon \PosInt \to \Bin^\omega$, but $\PosInt$ is !!{enumerable}.».
  - **العربية المعيارية:** [السطر ١٠٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/reduction.tex#L107)؛ الطبعة الدولية: [ص ٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=74) (ترقيم المتن: ٧٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=74) (ترقيم المتن: ٧٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «جعل النص الإنجليزي قيمة $h(n)$ سلسلة منتهية من الأصفار مع أن المجال المقابل».

## وحاصل ذلك أنه لو كانت ℘(ℤ⁺) قابلة للتعداد لكانت 𝔹^ω قابلة للتعداد.

الأصل الإنجليزي: `if the powerset were enumerable, binary sequences would be enumerable`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0034-DIRECT-CONDITIONAL-20260907`.

**المعنى المقصود:** يفيد ختام البرهان: لو كانت مجموعة أجزاء الموجبات قابلة للتعداد لكانت مجموعة المتتاليات الثنائية كذلك، وهذا يناقض عدم تعداد الثانية.

**سبب الاختيار:** يصرح الأصل بالشرط بعد إثبات شمول الدالة من مجموعة الأجزاء إلى المتتاليات؛ ثم يستعمل نفي التالي لنفي المقدم. أبقت التراثية «وحاصل ذلك أنه لو ... لكانت» في هذا الموضع لتعيد الجهة نفسها بعبارة عربية متصلة بالاستنتاج، لا بقفزة من عدم تعداد الثانية إلى الأولى بلا واسطة. المعجم يعرض لفظ الاختزال في مجال آخر، فلا ينوب عن قراءة سلسلة البرهان.

**سؤال مفتوح:** هل تصل العبارة الشرطية المباشرة بين الشمول والتناقض من غير التباس في جهة الرد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧٩-٨٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L79-L80) — هذا هو الاستنتاج الصريح بعد بناء الدالة الشاملة وقبل استعمال عدم التعداد المعروف.

**مواضع المعجم المعاينة:** [ص ٦٠١ من PDF (المطبوعة ٥٨٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=601)

**حدود الشاهد المعجمي:** PDF ص ٦٠١ شاهد لفظي للاختزال الحسابي، ولا يقدم برهان شرط التعداد؛ أخذ الاستدلال من الأصل.

**بديل جدير بالمقارنة:** وحاصل ذلك تكافؤ التعدادين؛ يزيد دعوى لم يستعملها الاستدلال هنا

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في حفظ جهة الشرط والتناقض.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0034 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ٧٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L79). الشاهد المسجل: «So if $\Pow{\PosInt}$ were !!{enumerable}, $\Bin^\omega$ would be !!{enumerable}. But $\Bin^\omega$ is !!{nonenumerable}».
  - **العربية التراثية:** [السطر ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction.tex#L44)؛ الطبعة التراثية: [ص ٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=70) (ترقيم المتن: ٦٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وحاصل ذلك أنه لو كانت $\Pow{\PosInt}$ !!{enumerable} لكانت $\Bin^\omega$ !!{enumerable}. وقد ثبت أن $\Bin^\omega$ !!{nonenumerable} (\olref[nen]{thm:nonenum-bin-omega})، فلزم أن $\Pow{\PosInt}$ !!{nonenumerable}.».

## لظفرنا بذلك بحل الأولى

الأصل الإنجليزي: `a solution of the latter yields a solution of the former`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0034-INSTRUMENTAL-ANTECEDENT-20260907`.

**المعنى المقصود:** حل المسألة الثانية، أي تعداد مجموعة أجزاء الموجبات، يولد بذلك حل الأولى، أي تعداد المتتاليات الثنائية.

**سبب الاختيار:** سمي الأصل تعداد مجموعة الأجزاء «الأخيرة» وتعداد المتتاليات «الأولى»، فلا يكفي ضمير مبهم يعود إلى «حل» و«تعداد» معًا. ربطت التراثية الجملة بـ«بذلك» عائدة إلى الظفر بتعداد الثانية، ثم ذكرت الأولى بالاسم، محافظة على جهة الرد. شاهد المعجم لكلمة reduction يخص تبسيط الكسور، ولذلك بقي استعمال «اختزال مسألة» قرارًا سياقيًا قابلًا للمراجعة.

**سؤال مفتوح:** هل «لظفرنا بذلك بحل الأولى» بينة المرجع، أم «لأفضى ذلك إلى حل الأولى» أفصح؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٩-٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L29-L31) — الجملة الأصلية تسمي الطرفين صراحة وتحدد أي حل ينتج الآخر.

**مواضع المعجم المعاينة:** [ص ٦٠١ من PDF (المطبوعة ٥٨٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=601)

**حدود الشاهد المعجمي:** PDF ص ٦٠١ يورد اختزال/اختصار في سياق الكسور فقط؛ لا يلزم منه اصطلاح رد المسائل، فتجري المفاضلة من نص المسألة نفسه.

**بديل جدير بالمقارنة:** لظفرنا به بحل الأولى؛ مرجع الهاء ملتبس بين التعداد والحل؛ لأفضى ذلك إلى حل الأولى؛ بديل أسلوبي صالح للمراجعة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في اتجاه الاستدلال، متوسطة في صياغة الرابط.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0034 — الاختزال، وقوع ١:**
  - **الأصل:** [السطر ٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/reduction.tex#L29). الشاهد المسجل: «$\Pow{\PosInt}$. A solution to the latter---an enumeration of $\Pow{\PosInt}$---would yield a solution to the former---an enumeration of $\Bin^\omega$.».
  - **العربية التراثية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/reduction.tex#L17)؛ الطبعة التراثية: [ص ٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=69) (ترقيم المتن: ٦٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «قد ثبت بالحجة القطرية أن $\Pow{\PosInt}$ !!{nonenumerable}، وكان قد سبق ثبوت ذلك لـ$\Bin^\omega$، أي مجموعة المتتاليات اللانهائية من~$0$ و~$1$، فهي !!{nonenumerable}. ويمكن أن نجعل النتيجة الثانية سبيلًا آخر إلى إثبات أن $\Pow{\PosInt}$ !!{nonenumerable}: ف…».

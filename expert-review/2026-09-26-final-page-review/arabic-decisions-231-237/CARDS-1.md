# بطاقات شرط عدم الخلو وعدم التعداد — القرارات ٢٣١–٢٣٣

[الرجوع إلى مقدمة الدفعة](README.md)

## فلكل مجموعة غير خالية

الأصل الإنجليزي: `enumerable`. معرّف القرار: `semantic-propagation-20260906:0033-P1`.

**المعنى المقصود:** كل مجموعة غير خالية قابلة للتعداد تقبل دالة شاملة من الموجبات إليها؛ لا تصح الدعوى نفسها للخالية وإن عدت قابلة للتعداد بالقائمة الخالية.

**سبب الاختيار:** تستعمل جملة الأصل For any enumerable set A من غير تقييد الخلو بعد أن أدخلت الخالية في حد قابلية التعداد، مع أن دالة من PosInt غير الخالية إلى الخالية ممتنعة. أضافت التراثية «غير خالية» وحاشية توضح سبب القيد، محافظة على الحد العام السابق لا ناقضة له. يعرف المعجم المجموعة العدودة بتقابل مع جزء من الموجبات، لكنه لا يحسم هذا الخطأ في صيغة الدالة الشاملة المحددة هنا؛ الدليل من نوع الدالة نفسه.

**سؤال مفتوح:** هل يظهر في الموضع المنشور أن الخالية تبقى قابلة للتعداد بالقائمة الخالية مع امتناع دالة كلية من الموجبات إليها؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٥-٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L25-L31) — جملة الأصل المطلقة على A هي موضع القيد الرياضي الذي أضيف في الطبعتين.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦، المطبوعة ١٤٤، يعرف countable set بتقابل مع جزء من الموجبات؛ لا يسند وجود دالة شاملة من جميع الموجبات إلى الخالية.

**بديل جدير بالمقارنة:** الإبقاء على «لكل مجموعة قابلة للتعداد» من غير قيد؛ مرفوض لأن الخالية مثال مضاد

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في ضرورة القيد وفي بقاء الخالية داخل الفئة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L26). الشاهد المسجل: «!!{nonenumerable} sets. For any !!{enumerable} set~$A$ there is».
  - **العربية المعيارية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L25)؛ الطبعة الدولية: [ص ٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=70) (ترقيم المتن: ٦٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=70) (ترقيم المتن: ٦٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ولعل وجود مجموعات !!{nonenumerable} مدعاة للدهشة أصلًا. فلكل مجموعة غير خالية».
  - **العربية التراثية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L19)؛ الطبعة التراثية: [ص ٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=67) (ترقيم المتن: ٦٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وقد يستغرب المرء أول الأمر وجود مجموعات !!{nonenumerable}. ووجه ذلك أن المجموعة غير الخالية !!{enumerable}~$A$ تقبل دالة~!!a{surjective} $f \colon \PosInt \to A$، وأما المجموعة !!{nonenumerable} فلا تقبلها. فمهما أرسلنا !!{element}s~$\PosInt$، على ما فيها م…».

## فالمجموعة التي تنتفي عنها هذه الخاصية هي غير قابلة للتعداد

الأصل الإنجليزي: `Such sets are called nonenumerable`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0033-REPAIR-G03-20260907`.

**المعنى المقصود:** ليس كل ما لا نهاية له قابلًا للتعداد؛ وتسمى المجموعات التي تخلو من خاصية التعداد غير قابلة للتعداد.

**سبب الاختيار:** يرجع Such sets في الأصل إلى المجموعات اللانهائية التي لا تملك خاصية التعداد، لا إلى كل مجموعة لا نهائية. جعلت التراثية المرجع ظاهرًا بقول «فالمجموعة التي تنتفي عنها هذه الخاصية» وبمطابقة الضمير والصفة المؤنثة، فلم تغير المقابلة المنطقية. يبين المعجم countable set بلفظ «مجموعة عدودة»، ولا يورد في الصفحة نفسها اسمًا حرفيًا للنفي المنشور.

**سؤال مفتوح:** هل يؤمن التصريح بـ«هذه الخاصية» من قراءة خاطئة تقول إن كل مجموعة لا نهائية غير قابلة للتعداد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٠-٢٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L20-L23) — السياق السابق مباشرة يقيد اسم الإشارة بالمجموعات اللانهائية التي لا تقبل التعداد.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يعرف المجموعة العدودة ويذكر عدودة غير منتهية؛ فلا يجعل اللانهاية وحدها نفيًا للمعدودية.

**بديل جدير بالمقارنة:** فكل مجموعة لا نهائية غير قابلة للتعداد؛ مرفوضة لمخالفة الأمثلة السابقة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في نطاق اسم الإشارة والمقابلة الرياضية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٢٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L20). الشاهد المسجل: «Some sets, such as the set $\PosInt$ of positive integers, are infinite. So far we've seen examples of infinite sets which were all !!{enumerable}. However, there are also infinite sets which do not have this property. Such sets are called \emph{!!{nonenume…».
  - **العربية التراثية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L17)؛ الطبعة التراثية: [ص ٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=67) (ترقيم المتن: ٦٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «من المجموعات ما لا نهاية له، كمجموعة الأعداد الصحيحة الموجبة~$\PosInt$. وقد كانت المجموعات اللانهائية التي تقدمت أمثلتها كلها !!{enumerable}؛ وليس ذلك شأن كل مجموعة لا نهائية. فالمجموعة التي تنتفي عنها هذه الخاصية هي \emph{!!{nonenumerable}}.».

## وطريق إثبات أن المجموعة غير الخالية غير قابلة للتعداد

الأصل الإنجليزي: `Rule out a surjection from positive integers to a nonempty set`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0033-REPAIR-G06-20260907`.

**المعنى المقصود:** إثبات عدم قابلية مجموعة غير خالية للتعداد يقتضي نفي كل دالة شاملة من الموجبات إليها، لا مجرد عدم تعيين قائمة بعينها.

**سبب الاختيار:** يصف الأصل معيار نفي التعداد بالدالة الشاملة، لكنه يحتاج شرط غير الخلو الذي ظهر في تصويب الجملة السابقة؛ فالخالية قابلة للتعداد ولا تقبل أي دالة كلية من الموجبات. أعادت التراثية «المجموعة غير الخالية» في افتتاح المعيار حتى لا يفقد القارئ القيد عند الانتقال إلى البرهان القطري. مدخل المعجم للعدودة يفسر الفئة، لكن صحة الاستثناء تتبع حد الأصل ونوع الدالة.

**سؤال مفتوح:** هل تكرار شرط عدم الخلو في بداية معيار النفي كاف لئلا يعمم القارئ البرهان على المجموعة الخالية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٣-٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L33-L38) — المقطع الأصلي يحول عدم التعداد إلى نفي دالة شاملة لكل قائمة مفترضة.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يبين معنى المجموعة العدودة، ولا يقرر تقييد معيار الدالة الشاملة هنا؛ القيد الرياضي مستنتج من تعريف الأصل.

**بديل جدير بالمقارنة:** نفي الدالة الشاملة لكل مجموعة بلا استثناء؛ مرفوض بالمجموعة الخالية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في ضرورة القيد وبنية البرهان.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0033 — المجموعات غير القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L33). الشاهد المسجل: «How would one prove that a set is !!{nonenumerable}? You have to show that no such surjective function can exist. Equivalently, you have to show that the elements of~$A$ cannot be enumerated in a one way infinite list. The best way to do this is to show tha…».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/non-enumerability.tex#L25)؛ الطبعة التراثية: [ص ٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=67) (ترقيم المتن: ٦٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وطريق إثبات أن المجموعة غير الخالية !!{nonenumerable} أن ننفي إمكان تلك الدالة الشاملة؛ ومعناه أن عناصر~$A$ لا تستوعبها قائمة لا نهائية تمتد في جهة واحدة. ويكفينا لذلك أن نبين أن كل قائمة من !!{element}s~$A$ يفوتها عنصر على الأقل، أي إن الدالة $f\colon \Pos…».

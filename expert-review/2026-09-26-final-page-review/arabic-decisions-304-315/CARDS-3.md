# بطاقات الاتحاد والفرق والفرض في البرهان — القرارات ٣١٢–٣١٥

[الرجوع إلى مقدمة الدفعة](README.md)

## واتحاد المجموعة بإحدى مجموعاتها الجزئية هو المجموعة الأصلية نفسها:

الأصل الإنجليزي: `The union of a set and one of its subsets is just the bigger set:`. معرّف القرار: `semantic-propagation-20260906:AR-OLP-0008-CLASSICAL-C005`.

**المعنى المقصود:** اتحاد مجموعة مع مجموعة جزئية منها يعيد المجموعة الأصلية نفسها، بما في ذلك حالة مساواة الجزئية لها.

**سبب الاختيار:** قال الأصل bigger set على سبيل البيان، لا إن عدد العناصر أكبر بالضرورة. اختارت التراثية «المجموعة الأصلية نفسها» وجعلت الجزئية منسوبة إليها صراحة؛ فيصدق الحكم حتى عند A⊆A، ولا يعتمد على مقارنة الحجم. يشهد المعجم لـ«اتحاد» و«مجموعة جزئية»، أما التعبير الكامل فينتج من المثال وقانون الاتحاد.

**سؤال مفتوح:** هل «المجموعة الأصلية نفسها» تحدد مرجع الاتحاد من غير إيحاء بأن الجزئية أصغر عددًا على الدوام؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٧-٤٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L47-L48) — مثال الامتصاص بالاتحاد مع الجزئية يحدد النتيجة دون شرط صرامة الاحتواء.

**مواضع المعجم المعاينة:** [ص ٦٩٦ من PDF (المطبوعة ٦٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=696)، [ص ٧٥٤ من PDF (المطبوعة ٧٤٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=754)

**حدود الشاهد المعجمي:** PDF ص ٦٩٦ للمجموعة الجزئية، وص ٧٥٤ للاتحاد؛ لا يقرر أي مدخل وحده لفظ «المجموعة الأصلية» أو معنى bigger البلاغي.

**بديل جدير بالمقارنة:** المجموعة الأكبر؛ مرفوضة إذا فهمت مقارنة عددية صارمة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الهوية A∪B=A عند B⊆A، متوسطة في قوة الإيضاح الأسلوبي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ١:**
  - **الأصل:** [السطر ٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L47). الشاهد المسجل: «The union of a set and one of its subsets is just the bigger set: $\{a,».
  - **العربية التراثية:** [السطر ٤٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L43)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «واتحاد المجموعة بإحدى مجموعاتها الجزئية هو المجموعة الأصلية نفسها: $\{a,».

## ومتى وجدت عناصر مشتركة بين مجموعتين، كان تقاطعهما المجموعة التي تضمها جميعًا ولا تضم غيرها، نحو: وتقاطع المجموعة بإحدى مجموعاتها الجزئية هو تلك المجموعة الجزئية:

الأصل الإنجليزي: `If two sets do have !!{element}s in common, their intersection is the set of all those: / The intersection of a set with one of its subsets is just the smaller set:`. معرّف القرار: `semantic-propagation-20260906:AR-OLP-0008-CLASSICAL-C009`.

**المعنى المقصود:** تقاطع مجموعتين يجمع جميع عناصرهما المشتركة وحدها، وإذا تقاطعت مجموعة مع جزئية منها كانت النتيجة تلك الجزئية.

**سبب الاختيار:** جاءت التراثية بوصف تقاطع المجموعة بأنه المجموعة التي «تضمها جميعًا ولا تضم غيرها» بعد ذكر العناصر المشتركة، فتحفظ الشمول والحصر. وفي المثال التالي سمت «تلك المجموعة الجزئية» بدل «المجموعة الأصغر»، لأن A∩B=B متى B⊆A حتى إذا B=A؛ فلا يثبت من الاحتواء فرق صارم في العدد.

**سؤال مفتوح:** هل مرجع الضمير في «تضمها جميعًا» واضح أنه العناصر المشتركة فقط، وهل تسمية الجزئية تمنع فهم «الأصغر» بمعنى عددي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٥-٨٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L85-L86) — تعريف التقاطع بتمام العناصر المشتركة دون سواها؛ [الأسطر ٨٨-٨٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L88-L89) — نتيجة التقاطع مع مجموعة جزئية تشمل حالة المساواة.

**وجه جمع المواضع:** ربط موضعي الأصل المتجاورين يبين وظيفة الحصر في التعريف ووظيفة الاحتواء في المثال.

**مواضع المعجم المعاينة:** [ص ٣٧٠ من PDF (المطبوعة ٣٥٨)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=370)، [ص ٦٩٦ من PDF (المطبوعة ٦٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=696)

**حدود الشاهد المعجمي:** PDF ص ٣٧٠ يشرح التقاطع بجميع العناصر المشتركة، وص ٦٩٦ يشرح احتواء المجموعة الجزئية؛ لا يفرض أيهما صوغ الضمير في العبارة التراثية.

**بديل جدير بالمقارنة:** العناصر المشتركة وحدها؛ أوضح مرجعًا وأطول داخل الجملة الحالية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في قانون التقاطع، متوسطة في مدى وضوح الضمير.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ١:**
  - **الأصل:** [السطر ٨٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L88). الشاهد المسجل: «The intersection of a set with one of its subsets is just the smaller set: $\{a, b, c\} \cap \{a, b\} = \{a, b\}$.».
  - **العربية التراثية:** [السطر ٨٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L83)؛ الطبعة التراثية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وتقاطع المجموعة بإحدى مجموعاتها الجزئية هو تلك المجموعة الجزئية:».
- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ٢:**
  - **الأصل:** [السطر ٨٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L85). الشاهد المسجل: «If two sets do have !!{element}s in common, their intersection is the set of all those: $\{a, b, c \} \cap \{a, b, d \} = \{a, b\}$.».
  - **العربية التراثية:** [السطر ٧٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L79)؛ الطبعة التراثية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ومتى وجدت !!{element}s مشتركة بين مجموعتين، كان تقاطعهما المجموعة التي تضمها جميعًا ولا تضم غيرها، نحو:».

## أثبت أنه إذا كانت A مجموعة وكان A ∈ B، فإن A ⊆ ⋃ B.

الأصل الإنجليزي: `Show that if $A$ is a set and $A \in B$, then $A \subseteq \bigcup B$.`. معرّف القرار: `semantic-propagation-20260906:AR-OLP-0008-CLASSICAL-C014`.

**المعنى المقصود:** التمرين يطلب إثبات أنه من كون A مجموعة وA∈B ينتج A⊆⋃B، لا إثباتًا لمجموعة مجهولة المخاطب.

**سبب الاختيار:** حفظت التراثية الشرطين صريحين: نوع A مجموعة، وانتماؤها إلى B؛ ولكل x∈A تكون A نفسها عنصرًا في B، ومن ثم x∈⋃B. جاء «أثبت أنه إذا...» طلبًا لبرهان الشرط لا تصريفًا غامضًا لعبارة إنجليزية مختزلة.

**سؤال مفتوح:** هل الأمر البرهاني والشرطان مفهومان من أول قراءة، وهل تظهر ضرورة فرض A∈B في خطوة الانتماء إلى الاتحاد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L135) — هذه مسألة قصيرة تحفظ الفرضين والاستنتاج واتجاه برهانه.

**مواضع المعجم المعاينة:** [ص ٢١٤ من PDF (المطبوعة ٢٠٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=214)، [ص ٦٩٦ من PDF (المطبوعة ٦٨٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=696)

**حدود الشاهد المعجمي:** PDF ص ٢١٤ يشرح العضوية وص ٦٩٦ الاحتواء؛ خطوة الاستنتاج من تعريف الاتحاد في الأصل لا من مقابلة لفظية منفردة في المعجم.

**بديل جدير بالمقارنة:** برهن على أن...؛ مرادف أسلوبي لا يغيّر الفرضين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لأن الفرض والنتيجة وخطوة البرهان محددة رمزيًا.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ١:**
  - **الأصل:** [السطر ١٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L135). الشاهد المسجل: «Show that if $A$ is a set and $A \in B$, then $A \subseteq \bigcup B$.».
  - **العربية التراثية:** [السطر ١٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L131)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «أثبت أنه إذا كانت $A$ مجموعة وكان $A \in B$، فإن $A \subseteq \bigcup B$.».

## فرق المجموعتين A ∖ B هو مجموعة جميع عناصر A التي ليست من عناصر B، أي

الأصل الإنجليزي: `The \emph{set difference}~$A \setminus B$ is the set of all !!{element}s of $A$ which are not also !!{element}s of~$B$, i.e.,`. معرّف القرار: `semantic-propagation-20260906:AR-OLP-0008-CLASSICAL-C016`.

**المعنى المقصود:** فرق A وB هو جميع x التي تنتمي إلى A ولا تنتمي إلى B، أي A∖B، لا عملية حسابية على عدد عناصرهما.

**سبب الاختيار:** جعلت التراثية التعريف امتداديًا بقول «مجموعة جميع عناصر A التي ليست من عناصر B»، فتحفظ شرطَي x∈A وx∉B معًا. المعجم يطبع set difference = «فرق مجموعتين» ويشرح الشرط نفسه بالرسم، فيسند الاسم والمعنى. اللفظ لا يعني حذف جميع B من A إذا كانت B لا تشترك معها أصلًا، فالفارق المعين هو العناصر المشتركة بالمجال A.

**سؤال مفتوح:** هل «فرق المجموعتين» كافٍ مع الصيغة A∖B لإظهار الاتجاه، أم ينبغي التنبيه أن تبديل A وB يغيّر النتيجة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٦٢-١٦٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L162-L166) — التعريف الأصلي يجمع انتماء x إلى A ونفي انتمائه إلى B.

**مواضع المعجم المعاينة:** [ص ٦٤٤ من PDF (المطبوعة ٦٣٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=644)

**حدود الشاهد المعجمي:** PDF ص ٦٤٤ (المطبوعة ٦٣٢) يطبع «فرق مجموعتين» ويرسم A∖B مع شرط الانتماء إلى A وعدم الانتماء إلى B؛ شاهد مباشر.

**بديل جدير بالمقارنة:** طرح المجموعتين؛ قد يوهم عملية حسابية على العدد، فلا يُفضل هنا

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لاتفاق التعريف الرمزي والمدخل المعجمي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0008 — الاتحاد والتقاطع والفرق، وقوع ١:**
  - **الأصل:** [السطر ١٦٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L163). الشاهد المسجل: «The \emph{set difference}~$A \setminus B$ is the set of all !!{element}s of $A$ which are not also !!{element}s of~$B$, i.e.,».
  - **العربية التراثية:** [السطر ١٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L159)؛ الطبعة التراثية: [ص ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=35) (ترقيم المتن: ٣٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{فرق المجموعتين}~$A \setminus B$ هو مجموعة جميع !!{element}s $A$ التي ليست من !!{element}s~$B$، أي».

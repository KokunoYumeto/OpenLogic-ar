# بطاقات الصياغة والفهرسة — القرارات ٢٢٥–٢٢٨

[الرجوع إلى مقدمة الدفعة](README.md)

## وعينت العبارة المكافئة في النص الإنجليزي هذا المعنى.

الأصل الإنجليزي: `equivalent formulation, not reward`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0031-CLASSICAL-COFINITE-SOURCE-NOTE-20260907`.

**المعنى المقصود:** متممة A منتهية تعني وجود مجموعة منتهية F داخل الطبيعيّات تحقق A=Nat∖F؛ والجملة المعادلة في الأصل تزيل اللبس النحوي في التعريف الأول.

**سبب الاختيار:** عبارة الأصل complement of a finite set Nat مضطربة نحويًا، لكن ما بعدها يصرح بأن Nat∖A منتهية. تصوغ التراثية وجود F منتهية داخل Nat وتصف الجملة الثانية بأنها «العبارة المكافئة» لا «المكافأة» بمعنى الجزاء؛ وتحيل إلى النص الإنجليزي الذي يحمل الشاهد. لم يظهر cofinite مدخلًا مطابقًا في بحث المعجم المحدود، ولا يصح حمل مدخل المجموعة العدودة على هذا المصطلح.

**سؤال مفتوح:** هل «متممتها منتهية» مع الصيغة Nat∖A يوضح أن المتممة نسبية إلى Nat لا إلى مجموعة شاملة مجهولة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩١-٩٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L91-L97) — التعريف الأصلي وجملته المكافئة يحددان أن المتممة تؤخذ داخل الطبيعيّات وأنها منتهية.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يتناول المجموعة العدودة، وليس المتممة المنتهية؛ لم يظهر cofinite مدخلًا مطابقًا في بحث OCR المحدود، فالحد هنا من صيغة الأصل نفسها.

**بديل جدير بالمقارنة:** جزئية ذات متممة منتهية؛ وصف أصرح وأطول من عبارة الطبعة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الصيغة الرياضية والتصويب الدلالي، ومتوسطة في الاسم الاصطلاحي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0031 — دوال المزاوجة والرموز، وقوع ١:**
  - **الأصل:** [السطر ٩٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L92). الشاهد المسجل: «A subset of $\Nat$ is said to be \emph{cofinite} iff it is the complement of a finite set $\Nat$; that is, $A \subseteq \Nat$ is cofinite iff $\Nat\setminus A$ is finite. Let $I$ be the set whose».
  - **العربية التراثية:** [السطر ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/pairing.tex#L94)؛ الطبعة التراثية: [ص ٦٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=65) (ترقيم المتن: ٦٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وعينت العبارة المكافئة في النص الإنجليزي هذا المعنى.».

## هو مجموعة قابلة للتعداد. هو مجموعة قابلة للتعداد أيضًا.

الأصل الإنجليزي: `enumerable union of an enumerable family of enumerable sets`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0031-CLASSICAL-UNION-PREDICATE-20260907`.

**المعنى المقصود:** المقصود اتحاد مجموعات قابلة للتعداد مفهرسة فهرسة قابلة للتعداد؛ ويسند وصف القابلية إلى مجموعة الاتحاد نفسها.

**سبب الاختيار:** في نص المسألة الإنجليزي يجتمع وصف العائلة والمجموعات والاتحاد. أضافت التراثية الخبر «هو مجموعة قابلة للتعداد» كي تتعلق الصفة المؤنثة بالمجموعة لا بـ«اتحاد» المذكر، وأبقت الصيغة التي تجمع A_i. لا يثبت مدخل المجموعة العدودة في المعجم برهان اتحاد عائلة كاملة؛ بل يشرح وصف كل مجموعة. وقد يتطلب البرهان العام اختيار تعدادات للمجموعات، فينبغي عدم نسبة إسقاط هذا الافتراض إلى المعجم أو إلى التصحيح النحوي.

**سؤال مفتوح:** هل يحتاج تمرين اتحاد عائلة من مجموعات عدودة إلى تصريح بافتراض اختيار معدود أو بناء تعدادات معطاة، أم يكفي السياق التأسيسي للكتاب؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩٩-١٠٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L99-L104) — المسألة الأصلية تتطلب اتحاد عائلة مفهرسة وتصف كل عضو والاتحاد بقابلية التعداد.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يعرف المجموعة العدودة منفردة؛ لا يقرر في هذه الصفحة نظرية الاتحاد المعدود أو شروط اختيار تعدادات العائلة.

**بديل جدير بالمقارنة:** اتحادها قابل للتعداد؛ صحيح التركيب لكنه يحتاج تحويل الرمز المشترك للصفة؛ هو عدود؛ لفظ أقرب للمعجم وقد يخالف نظام الطبعة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في مرجع الصفة والنحو، ومتوسطة في الاكتفاء بالافتراضات التأسيسية المضمرة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0031 — دوال المزاوجة والرموز، وقوع ١:**
  - **الأصل:** [السطر ١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L100). الشاهد المسجل: «Show that the !!{enumerable} union of !!{enumerable} sets is !!{enumerable}. That is, whenever $A_1$, $A_2$, \dots{} are sets, and each $A_i$ is !!{enumerable}, then the union $\bigcup_{i=1}^\infty A_i$ of all of them is also !!{enumerable}. [NB: this is ha…».
  - **العربية التراثية:** [السطر ١٠١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/pairing.tex#L101)؛ الطبعة التراثية: [ص ٦٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=64) (ترقيم المتن: ٦٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «A_i$ هو مجموعة !!{enumerable} أيضًا. [تنبيه: المسألة صعبة!]».
- **OLP-0031 — دوال المزاوجة والرموز، وقوع ٢:**
  - **الأصل:** [السطر ١٠٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L100). الشاهد المسجل: «Show that the !!{enumerable} union of !!{enumerable} sets is !!{enumerable}. That is, whenever $A_1$, $A_2$, \dots{} are sets, and each $A_i$ is !!{enumerable}, then the union $\bigcup_{i=1}^\infty A_i$ of all of them is also !!{enumerable}. [NB: this is ha…».
  - **العربية التراثية:** [السطر ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/pairing.tex#L99)؛ الطبعة التراثية: [ص ٦٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=64) (ترقيم المتن: ٦٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «هو مجموعة !!{enumerable}. أي إذا أعطيت $A_1$، $A_2$، \dots{}، وكانت كل».

## (n+m)

الأصل الإنجليزي: `ordinal rank of the triangular number`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0031-MSA-ARABIC-ORDINAL-20260907`.

**المعنى المقصود:** الإشارة إلى العدد المثلثي ذي الرتبة n+m هي فهرسة حد من متتالية، لا رفع n+m إلى قوة تسمى th.

**سبب الاختيار:** المصدر يكتب لاحقة ترتيب إنجليزية فوق الفهرس، لا أسًا ذا أثر حسابي. أبقت المعيارية المقدار n+m بتمامه وحذفت الغلاف اللغوي لللاحقة لأن «ذي الرتبة» يؤديه عربيًا، مع بقاء الصيغة الجبرية التالية. المدخل المعجمي للأعداد المثلثية يثبت الاسم والمتتالية، أما النقل الصحيح لللاحقة فمقيد ببنية جملة الأصل.

**سؤال مفتوح:** هل يبدو الفرق بين الفهرس n+m والأس في الفقرة المعيارية واضحًا عند الانتقال من الجملة إلى صيغة g؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤١-٤٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L41-L43) — العبارة الأصلية تسمي الحد الترتيبي قبل إضافة n إليه في تعريف دالة المزاوجة.

**مواضع المعجم المعاينة:** [ص ٧٣٧ من PDF (المطبوعة ٧٢٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=737)

**حدود الشاهد المعجمي:** PDF ص ٧٣٧ يسمي triangular number «عددًا مثلثيًا» ويبين تتابع حدوده؛ لا يذكر اللاحقة الإنجليزية th.

**بديل جدير بالمقارنة:** العدد المثلثي رقم n+m؛ أوضح من جهة الفهرس وأقل انسجامًا مع سياق التعريف

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الفصل بين الفهرسة والأس وبقاء المقدار.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0031 — دوال المزاوجة والرموز، وقوع ١:**
  - **الأصل:** [السطر ٤١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L41). الشاهد المسجل: «is easier on the eyes. This tells you first to determine the $(n+m)^\text{th}$ triangle number, and then add $n$ to it. And it populates the array in exactly the way we would like. So in».
  - **العربية المعيارية:** [السطر ٤١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/pairing.tex#L41)؛ الطبعة الدولية: [ص ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=68) (ترقيم المتن: ٦٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=68) (ترقيم المتن: ٦٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$(n+m)$، ثم إضافة $n$ إليه. وهو يملأ المصفوفة بالطريقة».

## الصيغة المكافئة في النص الإنجليزي.

الأصل الإنجليزي: `equivalent English formulation in the cofinite correction note`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0031-MSA-COFINITE-SOURCE-NOTE-20260907`.

**المعنى المقصود:** تصويب تعريف ذوات المتممات المنتهية يستند إلى صيغة التكافؤ المكتوبة في الأصل الإنجليزي، لا إلى صيغة لاحقة في الطبعة العربية.

**سبب الاختيار:** ترد بعد التمرين حاشية تصويب عربية على العبارة الإنجليزية المضطربة. لو قيل «الصيغة التالية» لتوهم القارئ أن الشاهد آت بعد الحاشية، مع أن معادلة Nat∖A المنتهية سابقة في الأصل. «الصيغة المكافئة في النص الإنجليزي» تحدد جهة الإحالة وتحفظ أن المتممة داخل Nat. لا يوثق المعجم لفظ cofinite في الصفحات المعاينة؛ والبرهان الدلالي من الحد الأصلي.

**سؤال مفتوح:** هل تعين الحاشية في المعيارية عبارة الأصل الدالة على التكافؤ بوضوح يكفي القارئ الذي يقرأ النسخة العربية وحدها؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩١-٩٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L91-L97) — الصيغة المكافئة في نهاية تعريف الأصل ترفع اضطراب جملة المتممة الأولى.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ لا يعرف cofinite؛ استعملت صفحته هنا فقط لمقارنة باب المعدودية المحيط، وليس لإثبات لفظ المتممة المنتهية.

**بديل جدير بالمقارنة:** الصيغة التالية؛ توحي بإحالة إلى موضع عربي متأخر غير موجود

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في جهة الإحالة وصحة التكافؤ.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0031 — دوال المزاوجة والرموز، وقوع ١:**
  - **الأصل:** [السطر ٩٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/pairing.tex#L92). الشاهد المسجل: «A subset of $\Nat$ is said to be \emph{cofinite} iff it is the complement of a finite set $\Nat$; that is, $A \subseteq \Nat$ is cofinite iff $\Nat\setminus A$ is finite. Let $I$ be the set whose».
  - **العربية المعيارية:** [السطر ١٠٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/pairing.tex#L100)؛ الطبعة الدولية: [ص ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=68) (ترقيم المتن: ٦٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=68) (ترقيم المتن: ٦٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «في $\Nat$ لمجموعة جزئية منتهية منها، على ما تثبته الصيغة المكافئة في النص الإنجليزي.».

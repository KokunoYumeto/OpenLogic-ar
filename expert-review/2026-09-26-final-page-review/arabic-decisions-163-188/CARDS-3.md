# بطاقات أنواع الدوال — القرارات ١٨١–١٨٨

[الرجوع إلى مقدمة الدفعة](README.md)

## وتسمى هذه الدوال شاملة، وصورتها

الأصل الإنجليزي: `surjective functions`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0022-CLASSICAL-SURJECTIVE-OPENING-20260907`.

**المعنى المقصود:** الدالة الشاملة تصيب قيمها كل عنصر في المجال المقابل؛ أي يتحد المجال المقابل ومداها.

**سبب الاختيار:** يقدم الأصل الخاصية قبل اسم surjective، وتبقي التراثية هذا الترتيب بعبارة «تبلغ قيمه كل عنصر». يستعمل سجل الطبعات «شاملة»، بينما يطبع المعجم surjection «تطبيقًا غامرًا» ويسمي surjective mapping «تطبيقًا غامرًا». المعنى مضبوط في الأصل، لكن اختلاف الاصطلاح بين الشمول والغمر يستحق مراجعة لا استبدالًا آليًا.

**سؤال مفتوح:** هل ينبغي اعتماد «غامرة» وفق المعجم للدالة الشاملة في هذا العمل، أم إبقاء «شاملة» لشيوعها ووضوحها مع تسجيل المرادف؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٦-١٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L16-L19) — مقدمة الأصل تعطي الخاصية الدلالية لكل قيمة قبل صياغة التعريف الكمي.

**مواضع المعجم المعاينة:** [ص ٧٠٣ من PDF (المطبوعة ٦٩١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=703)، [ص ٧٠٤ من PDF (المطبوعة ٦٩٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=704)

**حدود الشاهد المعجمي:** PDF ص ٧٠٣، المطبوعة ٦٩١، يطبع surjection «تطبيقًا غامرًا»؛ وص ٧٠٤، المطبوعة ٦٩٢، يطبع surjective mapping «تطبيقًا غامرًا». لا يطبع هذان المدخلان «شاملة» مقابله.

**بديل جدير بالمقارنة:** غامرة؛ عنوان المعجم للتطبيق الشامل

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في شرط إصابة المجال المقابل، ومتوسطة في اختيار الاسم العربي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ١٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L17). الشاهد المسجل: «that every member of the codomain is a value of the function. Such functions are called !!{surjective}, and can be pictured as in».
  - **العربية التراثية:** [السطر ١٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L15)؛ الطبعة التراثية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فلنبدأ بما تبلغ قيمه كل عنصر من المجال المقابل. وتسمى هذه الدوال !!{surjective}، وصورتها في \olref{fig:surjective}.».

## تستحث

الأصل الإنجليزي: `every function induces a surjection onto its range`. معرّف القرار: `locale-ar-chosen-25f47f96cf8c27d5`.

**المعنى المقصود:** كل دالة f من A إلى B تستحث دالة f' من A إلى مداها تحفظ القيم نفسها، وتكون f' شاملة على هذا المدى.

**سبب الاختيار:** التحويل في الأصل لا يغير قاعدة f(x)، بل يضيق المجال المقابل إلى مجموعة القيم المتحققة؛ عندئذ كل عنصر فيه صورة مدخل. اختارت الطبعات «تستحث» لـinduces لتشير إلى دالة ناشئة من المعطاة لا إلى مساواة الدالتين بوصف المجال المقابل جزءًا من هوية الدالة. يميز المعجم المدى من المجال المقابل، لكنه لا يثبت فعل «تستحث» الاصطلاحي.

**سؤال مفتوح:** هل «تستحث» مفهوم في النثر العربي الرياضي هنا، أم الأوضح «تنشئ دالة شاملة» مع بيان أن f' غير f عند اختلاف المجال المقابل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٤-٤٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L44-L48) — الإنشاء الأصلي يسمي f' ويغير مجالها المقابل إلى مدى f مع إبقاء جميع القيم.

**مواضع المعجم المعاينة:** [ص ١١٢ من PDF (المطبوعة ١٠٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=112)، [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ١١٢ يفرق المجال المقابل من القيم، وص ٥٩١ يحدد المدى؛ لا يشهد أيهما لفعل «تستحث» نفسه.

**بديل جدير بالمقارنة:** تنشئ؛ فعل تفسيري أوضح لكنه أقل اصطلاحية في هذا السياق

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في صحة الإنشاء، ومتوسطة في فعل «تستحث».

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ٤٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L44). الشاهد المسجل: «Note that any function \emph{induces} !!a{surjection}. After all, given a function $f \colon A \to B$, let $f' \colon A \to \ran{f}$ be defined by $f'(x) = f(x)$. Since $\ran{f}$ is \emph{defined} as $\Setabs{f(x) \in B}{x \in A}$, this function $f'$ is gua…».
  - **العربية المعيارية:** [السطر ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-kinds.tex#L44)؛ الطبعة الدولية: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لاحظ أن كل دالة \emph{تستحث} !!a{surjection}. فبالنظر إلى دالة $f \colon A \to B$، لتكن $f' \colon A \to \ran{f}$ معرفة بـ$f'(x) = f(x)$. وبما أن $\ran{f}$ \emph{معرّف} بأنه $\Setabs{f(x) \in B}{x \in A}$، فلا بد أن تكون الدالة $f'$ !!a{surjection}».

## بتعريفه

الأصل الإنجليزي: `defined`. معرّف القرار: `retro-0005-0050:emphasis:a82fd8754715e4c2`.

**المعنى المقصود:** قول «بتعريفه» يعلل أن مدى f هو مجموعة قيم f(x) حيث x من A، فيثبت شمول f' على هذا المدى.

**سبب الاختيار:** يضع الأصل defined بين علامتي إبراز قبل صيغة المدى، لأن نتيجة الشمول هنا مباشرة من تعريف المدى لا من فرض جديد على f. حفظت التراثية هذه العلاقة بلفظ «بتعريفه»؛ وتؤكد صفحة المعجم الخاصة بالمدى أنه مجموعة القيم التي تصيبها الدالة. ينبغي فحص صيغة بناء المجموعة المطبوعة في الأصل على حدة؛ لا يسوغ أن يطمس اختيار اللفظ حد المدى.

**سؤال مفتوح:** هل تربط «بتعريفه» نتيجة الشمول بالتعريف السابق ربطًا كافيًا، وهل يلزم تصحيح صيغة بناء المدى في متن الأصل والطبعات إذا ثبت اضطرابها؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٤-٤٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L44-L48) — العبارة الأصلية تحتج بتعريف المدى لتبرير كون f' دالة شاملة.

**مواضع المعجم المعاينة:** [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ٥٩١، المطبوعة ٥٧٩، يحدد range بمجموعة القيم المصابة؛ لا يشهد المدخل لاختيار «بتعريفه» أسلوبيًا.

**بديل جدير بالمقارنة:** بحسب تعريف المدى؛ صيغة أطول تبين مرجع الضمير

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في حجة الشمول، ومتوسطة في مرجع الضمير وصيغة البناء المطبوعة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ٤٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L46). الشاهد المسجل: «defined by $f'(x) = f(x)$. Since $\ran{f}$ is \emph{defined} as».
  - **العربية المعيارية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-kinds.tex#L46)؛ الطبعة الدولية: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «معرفة بـ$f'(x) = f(x)$. وبما أن $\ran{f}$ \emph{معرّف} بأنه».
  - **العربية التراثية:** [السطر ٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L40)؛ الطبعة التراثية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=52) (ترقيم المتن: ٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فـ$\ran{f}$ \emph{بتعريفه} $\Setabs{f(x) \in B}{x \in A}$،».

## فهي متباينة وشاملة معًا.

الأصل الإنجليزي: `both injective and surjective (identity)`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0022-CLASSICAL-IDENTITY-PREDICATE-20260907`.

**المعنى المقصود:** دالة الهوية على الطبيعيّات تحقق التباين والشمول معًا لأنها تعيد كل عنصر إلى نفسه.

**سبب الاختيار:** يختبر الأصل الهوية f(x)=x بوصفها مثالًا يجمع injective وsurjective، وقد حفظت التراثية الخاصيتين معًا. يطبع المعجم identity function «دالة مطابقة»، والتطبيق المطابق مرادفًا، بينما تقول الطبعات «الهوية»؛ وهذه مفاضلة لفظية لا تغير البرهان المباشر، إذ لا يختلط مدخلان ولا يغيب عنصر من المجال المقابل.

**سؤال مفتوح:** هل الأفضل في الطبعات تسمية المثال «دالة مطابقة» وفق المعجم، أم إبقاء «دالة الهوية» مع ذكر المقابل المعجمي في سجل المصطلحات؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧٦-٨٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L76-L84) — المثال الأصلي يحدد f(x)=x ويقارن حاله بالدالة الثابتة ودالة اللاحق.

**مواضع المعجم المعاينة:** [ص ٣٤٦ من PDF (المطبوعة ٣٣٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=346)، [ص ٣٦١ من PDF (المطبوعة ٣٤٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=361)، [ص ٧٠٣ من PDF (المطبوعة ٦٩١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=703)

**حدود الشاهد المعجمي:** PDF ص ٣٤٦، المطبوعة ٣٣٤، يطبع identity function «دالة مطابقة»؛ وص ٣٦١ و٧٠٣ يثبتان اسمي التباين والغمر. صحة الخاصيتين من المعادلة في الأصل.

**بديل جدير بالمقارنة:** دالة مطابقة؛ اسم المعجم لهذا المثال

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في خاصيتي الدالة، ومتوسطة في اسم الهوية مقابل المطابقة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ٨٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L80). الشاهد المسجل: «The identity function $f\colon \Nat \to \Nat$ given by $f(x) = x$ is both !!{injective} and !!{surjective}.».
  - **العربية التراثية:** [السطر ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L71)؛ الطبعة التراثية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فهي !!{injective} و!!{surjective} معًا.».

## فهي شاملة غير متباينة.

الأصل الإنجليزي: `surjective, but not injective (piecewise function)`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0022-CLASSICAL-PIECEWISE-PREDICATE-20260907`.

**المعنى المقصود:** الدالة المحددة بحالتي الزوجي والفردي على الطبيعيّات شاملة، لكنها ليست متباينة لأن مدخلين مختلفين قد يعطيان القيمة نفسها.

**سبب الاختيار:** في مثال الأصل تعطي الدالة صفرًا عند الصفر، وتبلغ كل طبيعي آخر بقيمة مدخل ملائم؛ كما يشترك واحد واثنان في القيمة واحد. حفظت التراثية «شاملة غير متباينة» من غير أن تقلب النفي إلى نفي الخاصيتين. يطبع المعجم التباين «تطبيقًا متباينًا» والشمول «تطبيقًا غامرًا»، فاختيار شاملة هنا يحتاج مراجعة لفظية لا تغيير الحكم الرياضي.

**سؤال مفتوح:** هل المثال واللفظ «شاملة غير متباينة» واضحان مع شمول الصفر، أم يلزم إضافة شاهد قصير مثل f(1)=f(2)=1 إلى الشرح؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٦-٩٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L86-L95) — الصيغة بالحالتين وحكم الأصل اللاحق يحددان الشمول ونفي التباين معًا.

**مواضع المعجم المعاينة:** [ص ٣٦١ من PDF (المطبوعة ٣٤٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=361)، [ص ٧٠٣ من PDF (المطبوعة ٦٩١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=703)، [ص ٧٠٤ من PDF (المطبوعة ٦٩٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=704)

**حدود الشاهد المعجمي:** PDF ص ٣٦١ يطبع injection «تطبيقًا متباينًا»، وص ٧٠٣–٧٠٤ يطبعان surjection وsurjective mapping «تطبيقًا غامرًا»؛ المثال العددي من الأصل.

**بديل جدير بالمقارنة:** غامرة غير متباينة؛ تستبدل الشمول بالمدخل المعجمي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الحكم الرياضي، ومتوسطة في لفظ الشمول.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ٩٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L94). الشاهد المسجل: «is !!{surjective}, but not !!{injective}. \end{ex} \begin{explain}».
  - **العربية التراثية:** [السطر ٨٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L84)؛ الطبعة التراثية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فهي !!{surjective} غير !!{injective}.».
- **OLP-0022 — أنواع الدوال، وقوع ٢:**
  - **الأصل:** [السطر ٩٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L94). الشاهد المسجل: «is !!{surjective}, but not !!{injective}. \end{ex} \begin{explain}».
  - **العربية التراثية:** [السطر ٧٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L76)؛ الطبعة التراثية: [ص ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=52) (ترقيم المتن: ٥١)، [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وأما الدالة $f \colon \Nat \to \Nat$ ذات التعريف:».

## الدوال التي تكون متباينة وشاملة معًا

الأصل الإنجليزي: `functions which are both injective and surjective`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0022-CLASSICAL-BIJECTIVE-RELATIVE-20260907`.

**المعنى المقصود:** المقصود الدوال التي تجمع التباين والشمول في الوقت نفسه، فيسمى الواحد منها تقابليًا.

**سبب الاختيار:** يبني الأصل صلة الوصفين قبل تسمية bijective؛ وأبقت التراثية صلتهما بعبارة «التي تكون متباينة وشاملة معًا»، فلا تختزل الشرط إلى واحد منهما. يعرف المعجم bijection تطبيقًا «متباينًا وغامرًا» ويسمي bijective mapping «تطبيقًا تقابليًا». اختلاف «شاملة» عن «غامرة» مسجل، لا مسوغ لطمس أحد الشرطين.

**سؤال مفتوح:** هل يفضل ربط «تقابلية» في هذا الموضع بلفظ «غامرة» المعجمي بدل «شاملة» مع إبقاء التباين مصرحًا به؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩٧-١٠٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L97-L103) — مقدمة الأصل تسرد الخاصيتين مجتمعَتين قبل عرض اسم التقابل والمراسلة.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ٣٦١ من PDF (المطبوعة ٣٤٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=361)، [ص ٧٠٣ من PDF (المطبوعة ٦٩١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=703)

**حدود الشاهد المعجمي:** PDF ص ٦٩، المطبوعة ٥٧، يعرّف bijection بالتباين والغمر، وص ٣٦١ و٧٠٣ يثبتان اسمي الخاصيتين؛ لا يطبع «شاملة» بدل غامرة.

**بديل جدير بالمقارنة:** الدوال المتباينة الغامرة؛ تتبع عبارتي المعجم لكنها تغير لفظ الشمول المنشور

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في اجتماع الشرطين، ومتوسطة في توحيد لفظ الشمول.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ٩٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L98). الشاهد المسجل: «Often enough, we want to consider functions which are both !!{injective} and !!{surjective}. We call such functions !!{bijective}. They look like the function pictured in \olref{fig:bijective}. !!^{bijection}s are also sometimes called».
  - **العربية التراثية:** [السطر ٨٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L88)؛ الطبعة التراثية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ويكثر احتياجنا إلى الدوال التي تكون !!{injective} و!!{surjective} معًا؛».

## تقابلية؛ دالة تقابلية؛ مراسلات واحد إلى واحد

الأصل الإنجليزي: `bijective function; bijection; one-to-one correspondence`. معرّف القرار: `locale-ar-chosen-522efe1b7efc3f19`.

**المعنى المقصود:** الدالة التقابلية تجمع التباين والشمول، فيقابل كل عنصر من المجال المقابل عنصر وحيد من المجال، وتسمى تقابلًا.

**سبب الاختيار:** يفسر الأصل bijection بأنه one-to-one correspondence بعد اجتماعهما، وليس مجرد injection؛ وحفظت الطبعات «تقابلية» ثم «مراسلات واحد إلى واحد» شرحًا. يطبع المعجم bijection «تقابل» وbijective mapping «تطبيق تقابلي»، ويطبع one-to-one correspondence «تقابلًا واحدًا لواحد». لكن مدخل one-to-one function فيه يعني الدالة المتباينة وحدها، لذا يلزم حفظ سياق المراسلة التقابلية وعدم تسوية العبارتين.

**سؤال مفتوح:** هل «مراسلات واحد إلى واحد» واضحة بصفتها تقابلًا بين المجموعتين، أم الأفضل «تقابلات واحد لواحد» وفق المعجم لتجنب الخلط بالدالة المتباينة فقط؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٩٧-١١٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L97-L115) — المقطع الأصلي يذكر اجتماع الخاصيتين ويشرح لماذا يصح اسم المراسلة واحدًا لواحد.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ٥٠٢ من PDF (المطبوعة ٤٩٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=502)

**حدود الشاهد المعجمي:** PDF ص ٦٩ يطبع اسم التقابل «تقابلًا» واسم التطبيق التقابلي «تطبيقًا تقابليًا»؛ وص ٥٠٢، المطبوعة ٤٩٠، يميز المراسلة الواحدة لواحد من الدالة المتباينة وحدها.

**بديل جدير بالمقارنة:** تقابل واحد لواحد؛ الصيغة المطبوعة في مدخل المراسلة؛ تطبيق تقابلي؛ اسم المعجم للنوع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الفرق الرياضي بين التقابل والتباين وحده، ومتوسطة في صياغة المراسلة العربية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ٩٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L97). الشاهد المسجل: «\begin{explain} Often enough, we want to consider functions which are both !!{injective} and !!{surjective}. We call such functions !!{bijective}. They look like the function pictured in \olref{fig:bijective}. !!^{bijection}s are also sometimes called \emph…».
  - **العربية المعيارية:** [السطر ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/function-kinds.tex#L97)؛ الطبعة الدولية: [ص ٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=55) (ترقيم المتن: ٥٤)، [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=55) (ترقيم المتن: ٥٤)، [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{explain} كثيرًا ما نريد النظر في الدوال التي تكون !!{injective} و!!{surjective} معًا. ونسمي هذه الدوال !!{bijective}. وهي تشبه الدالة الممثلة في \olref{fig:bijective}. وتسمى !!^{bijection}s أحيانًا أيضًا \emph{مراسلات واحد إلى واحد}، لأنها تقرن كل عن…».
  - **العربية التراثية:** [السطر ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L87)؛ الطبعة التراثية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{explain} ويكثر احتياجنا إلى الدوال التي تكون !!{injective} و!!{surjective} معًا؛ واسمها !!{bijective}، وصورتها في \olref{fig:bijective}. وتسمى !!^{bijection}s أيضًا \emph{مراسلات واحد إلى واحد}، إذ يقابل كل عنصر من المجال المقابل فيها عنصر واحد من ال…».

## إذا وفقط إذا كانت شاملة ومتباينة معًا

الأصل الإنجليزي: `bijective iff surjective and injective`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0022-CLASSICAL-BIJECTION-IFF-20260907`.

**المعنى المقصود:** الدالة f تقابلية إذا وفقط إذا كانت شاملة ومتباينة معًا؛ فلا يكفي أحد الشرطين وحده.

**سبب الاختيار:** يضع الأصل iff في حد bijection بعد تعريف الشمول والتباين، وأبقت التراثية «إذا وفقط إذا» والشرطين كليهما. يقرر مدخل bijection المعجمي أنه تطبيق متباين وغامر، وهو شاهد على اجتماع الخاصيتين لا على لفظ «شاملة» بعينه؛ فيبقى اختلاف الاصطلاح سؤالًا للخبراء لا خللًا في الحد المنطقي.

**سؤال مفتوح:** هل يعتمد في هذا الحد «غامرة ومتباينة» لمطابقة المدخل المعجمي، أم تبقى «شاملة ومتباينة» مع إحالة واضحة إلى مرادف الغمر؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١١٢-١١٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L112-L115) — حد الأصل يثبت التكافؤ المنطقي بين اسم الدالة التقابلية واجتماع الشرطين.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ٣٦١ من PDF (المطبوعة ٣٤٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=361)، [ص ٧٠٤ من PDF (المطبوعة ٦٩٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=704)

**حدود الشاهد المعجمي:** PDF ص ٦٩ يطبع bijection «تقابلًا» مشروطًا بالتباين والغمر، وص ٣٦١ و٧٠٤ يثبتان اسمي الخاصيتين؛ لفظ الشمول من الطبعات.

**بديل جدير بالمقارنة:** غامرة ومتباينة؛ أقرب إلى عبارة المعجم من غير تغيير البنية المنطقية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التكافؤ الرياضي، ومتوسطة في تسمية الشمول.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0022 — أنواع الدوال، وقوع ١:**
  - **الأصل:** [السطر ١١٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/function-kinds.tex#L112). الشاهد المسجل: «\begin{defn}[!!^{bijection}] A function $f \colon A \to B$ is \emph{!!{bijective}} iff it is both !!{surjective} and !!{injective}. We call such a function !!a{bijection} from $A$ to~$B$ (or between $A$ and~$B$). \end{defn} \end{document}».
  - **العربية التراثية:** [السطر ١٠٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/function-kinds.tex#L100)؛ الطبعة التراثية: [ص ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=53) (ترقيم المتن: ٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الدالة $f \colon A \to B$ \emph{!!{bijective}} إذا وفقط إذا كانت !!{surjective} و!!{injective} معًا. وحينئذ تسمى !!a{bijection}».

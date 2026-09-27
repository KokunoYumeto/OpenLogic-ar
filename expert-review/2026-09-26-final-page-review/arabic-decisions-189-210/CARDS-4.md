# بطاقات الدوال الجزئية — القرارات ٢٠٦–٢١٠

[الرجوع إلى مقدمة الدفعة](README.md)

## الدوال الجزئية

الأصل الإنجليزي: `Partial Functions`. معرّف القرار: `retro-0005-0050:section:96674126bfbf9016`.

**المعنى المقصود:** الدوال الجزئية تسمح بمدخلات من A لا قيمة معينة لها في B، مع بقاء تفرد القيمة متى عرفت.

**سبب الاختيار:** يمهد الأصل للقسم بإسقاط شرط وجود مخرج لكل مدخل من تعريف الدالة التامة مع عدم إسقاط شرط التفرد. عنوان «الدوال الجزئية» يحفظ نطاق القسم. لم تعثر القراءة المعجمية المحدودة على مدخل عام مطابق لعبارة partial function؛ ومدخل «دالة تكرارية جزئية» أخص من المقصود هنا، فلا يجوز الاستناد إليه بوصفه تعريفًا عامًا.

**سؤال مفتوح:** هل «الدوال الجزئية» هو اللفظ القياسي الأنسب للدالة غير المعرفة على جميع A، أم تفضل المراجع العربية التخصصية «الدوال غير الكلية» في هذا الباب؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٢-١٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L12-L17) — عنوان القسم ومقدمته يعينان بالضبط الشرط المخفف من تعريف الدالة.

**مواضع المعجم المعاينة:** [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)، [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٥٢٣، المطبوعة ٥١١، يطبع partial recursive function «دالة تكرارية جزئية»، وهو صنف متخصص لا مدخل عام للدالة الجزئية؛ وص ٢٧٦ يشرح شرط الدالة التامة.

**بديل جدير بالمقارنة:** دوال غير كلية؛ وصف شارح لا شاهد معجمي مباشر لهذا العنوان

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الشرط الرياضي، ومتوسطة في ثبوت الاصطلاح العام من المعجم المعاين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ١٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L12). الشاهد المسجل: «\olsection{Partial Functions}».
  - **العربية المعيارية:** [السطر ١٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L12)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الدوال الجزئية}».
  - **العربية التراثية:** [السطر ١٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/partial-functions.tex#L12)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الدوال الجزئية}».

## دوالًا جزئية

الأصل الإنجليزي: `partial functions`. معرّف القرار: `retro-0005-0050:emphasis:f2abe603fe0e095c`.

**المعنى المقصود:** التعيينات التي قد تترك بعض عناصر A بلا مخرج تسمى دوالًا جزئية، لا علاقات متعددة القيم.

**سبب الاختيار:** جملة الأصل تقرر اسم الفئة بعد تخفيف شرط الوجود وحده؛ لذلك أبقت التراثية الجمع المنصوب «دوالًا جزئية» في موضع التسمية، وحفظت شرط عدم تجاوز قيمة واحدة لكل مدخل في التعريف التالي. مدخل المعجم المتاح يثبت استعمال «جزئية» في اسم نوع متخصص، ولا يثبت وحده الحد العام؛ فيبقى التعليل مرتبطًا بالأصل.

**سؤال مفتوح:** هل يستدعي هذا التمهيد تقديم قيد التفرد في الجملة نفسها، أم يكفي وروده في التعريف اللاحق مباشرة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٤-١٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L14-L18) — العبارة الأصلية المسماة تأتي عقب بيان حذف شرط وجود القيمة لكل مدخل.

**مواضع المعجم المعاينة:** [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)

**حدود الشاهد المعجمي:** PDF ص ٥٢٣ يورد «جزئية» في «دالة تكرارية جزئية» فقط ضمن الصفحات المعاينة؛ هذا استعمال للصفة لا توثيق للحد العام.

**بديل جدير بالمقارنة:** تعيينات غير كلية؛ شرح الحالة بدل اسم الفئة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في سبب التسمية والشرط الرياضي، ومتوسطة في الشاهد الاصطلاحي العام.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ١٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L17). الشاهد المسجل: «possible inputs. Such mappings are called \emph{partial functions}.».
  - **العربية المعيارية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L17)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{دوالًا جزئية}.».
  - **العربية التراثية:** [السطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/partial-functions.tex#L16)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ممكن. والتعيينات التي تجوز عند هذا التخفيف تسمى \emph{دوالًا جزئية}.».

## الدالة الجزئية

الأصل الإنجليزي: `partial function`. معرّف القرار: `retro-0005-0050:emphasis:3b8bacfc19dff697`.

**المعنى المقصود:** الدالة الجزئية f من A إلى B تعين لكل x من A صفر قيمة أو قيمة واحدة في B، ويكون مجال تعريفها جزءًا من A.

**سبب الاختيار:** حد الأصل يستعمل at most one ليجيز غياب القيمة ويمنع تعددها، ثم يضبط المجال بمجموعة المدخلات التي تكون f(x) عندها معرفة. تنقل التراثية ذلك بعبارة «ما لا يزيد على عنصر واحد» ولا تخلط مجال التعريف A المقترح بمجال الدالة الجزئية الفعلي. استعمال المعجم «جزئية» في الدالة التكرارية شاهد لغوي محدود لا يسند هذا الحد العام.

**سؤال مفتوح:** هل تعبير «مجال الجزئية» في متن الطبعة يوضح أن المقصود مجموعة المدخلات المعرفة، لا مجموعة A الأكبر المكتوبة في سهم الدالة الجزئية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٠-٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L20-L27) — التعريف الأصلي يثبت حد القيمة الواحدة أو غيابها ويعرّف المجال الفعلي بالضبط.

**مواضع المعجم المعاينة:** [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)، [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٥٢٣ يورد دالة تكرارية جزئية وهي أخص؛ وص ٢٧٦ يصف الدالة التامة بقيمة لكل عنصر. تعريف الصنف الجزئي العام من الأصل هنا.

**بديل جدير بالمقارنة:** دالة غير كلية؛ قد يوهم أنها يجب أن تفشل في موضع ما، مع أن كل دالة تامة جزئية أيضًا

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الحد الرياضي، ومتوسطة في التعبير الاصطلاحي المفضل.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ٢١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L21). الشاهد المسجل: «A \emph{partial function} $f \colon A \pto B$ is a mapping which».
  - **العربية المعيارية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L21)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن \emph{الدالة الجزئية} $f \colon A \pto B$ تعيينٌ يرسل كل».
  - **العربية التراثية:** [السطر ٢٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/partial-functions.tex#L20)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{الدالة الجزئية} $f \colon A \pto B$ تعيين يجعل لكل».

## غير معرّفة

الأصل الإنجليزي: `undefined`. معرّف القرار: `retro-0005-0050:emphasis:18613202aa5a7c86`.

**المعنى المقصود:** قيمة f(x) غير معرّفة عند مدخل لم تعين له الدالة الجزئية عنصرًا في B؛ وهذا يختلف عن قيمة موجودة لكنها مجهولة.

**سبب الاختيار:** يقابل الأصل بين defined وundefined بوصفهما حالتي وجود قيمة للدالة الجزئية عند x، لا بوصف الثانية جهلًا بالقيمة. استعملت التراثية «غير معرّفة» وربطتها برمز عدم التعريف وبمجال التعريف. لم يظهر في الصفحات المعجمية المحدودة مدخل مطابق لهذه العبارة في هذا السياق، فلا تنسب صياغة اللفظ إلى المدخل المتخصص للدالة التكرارية.

**سؤال مفتوح:** هل ينبغي التفريق في الشرح بين «غير معرّفة» و«غير محددة» لكيلا يحمل القارئ اللفظ على جهلنا بقيمة موجودة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٠-٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L20-L27) — حد الأصل يبين متى توجد قيمة f(x) ومتى لا توجد، ويقرن الحالتين برمزين مختلفين.

**مواضع المعجم المعاينة:** [ص ٥٢٣ من PDF (المطبوعة ٥١١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=523)

**حدود الشاهد المعجمي:** PDF ص ٥٢٣ لا يعطي في المدخل المعاين تعريف undefined العام، بل اسم نوع دالة تكرارية جزئية؛ اعتماد معنى غياب القيمة هنا على حد الأصل.

**بديل جدير بالمقارنة:** غير محددة؛ قد تلتبس بقيمة موجودة لم تعين في المسألة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في فرق الوجود والجهل، ومتوسطة في اللفظ القياسي عند متخصصي المنطق.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L24). الشاهد المسجل: «\emph{defined}, and otherwise \emph{undefined}. If $f(x)$ is defined,».
  - **العربية المعيارية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L24)؛ الطبعة الدولية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{معرّفة}، وإلا فهي \emph{غير معرّفة}. وإذا كانت قيمة $f(x)$ معرّفة،».
  - **العربية التراثية:** [السطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/partial-functions.tex#L23)؛ الطبعة التراثية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{معرّفة}، وإلا كانت \emph{غير معرّفة}. ونكتب في الحال الأولى،».

## تسلسلية؛ كلية

الأصل الإنجليزي: `serial relation inducing a total partial function`. معرّف القرار: `locale-ar-chosen-21e90fab9c46cec8`.

**المعنى المقصود:** العلاقة ذات قيمة واحدة لكل مدخل تستحث دالة جزئية؛ وتكون الدالة كلية إذا كانت العلاقة تسلسلية بمعنى وجود مخرج لكل مدخل.

**سبب الاختيار:** تجمع قضية الأصل شرط uniqueness لعدم تعدد المخرج وشرط serial لوجود مخرج لكل x من A، فتتحول الجزئية إلى كلية عند اجتماع الشرطين. أبقت التراثية «تسلسلية» مع تفسيره صراحة بالكم الوجودي، فلا تخلطه بترتيب خطي. يرد في المعجم serial order بمعنى ترتيب تام/خطي، وهذا مدخل مختلف لا شاهد مطابق لاسم العلاقة في هذه القضية؛ والغمر كذلك شرط على إصابة كل عنصر في B، لا شرط وجود مخرج لكل x.

**سؤال مفتوح:** هل تبقى «علاقة تسلسلية» مفهومة مع شرح ∀x∈A∃y∈B، أم يكون «علاقة كلية المجال» أوضح لتجنب التباسها بالترتيب التسلسلي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٥٨-٧٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L58-L72) — القضية وبرهانها يثبتان تفرد المخرج أولًا، ثم يستعملان التسلسل لإثبات كلية الدالة المستحثة.

**مواضع المعجم المعاينة:** [ص ٤٢٥ من PDF (المطبوعة ٤١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=425)، [ص ٧٠٣ من PDF (المطبوعة ٦٩١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=703)، [ص ٧٠٤ من PDF (المطبوعة ٦٩٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=704)

**حدود الشاهد المعجمي:** PDF ص ٤٢٥، المطبوعة ٤١٣، يورد serial order في معنى الترتيب الخطي لا serial relation؛ وص ٧٠٣–٧٠٤ يشرح الغمر في اتجاه المجال المقابل. معنى تسلسلية العلاقة هنا من حد الأصل الكمي، ويبقى اللفظ للمراجعة.

**بديل جدير بالمقارنة:** علاقة كلية المجال؛ يشرح المعنى لكن قد يلتبس بكون العلاقة نفسها دالة كلية؛ علاقة ذات مخرج لكل مدخل؛ شرح غير اصطلاحي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الكم والنتيجة الرياضية، ومنخفضة نسبيًا في توثيق اللفظ الاصطلاحي من المعجم المتاح.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ٥٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L58). الشاهد المسجل: «\begin{prop} Suppose $R \subseteq A \times B$ has the property that whenever $Rxy$ and $Rxy'$ then $y = y'$. Then $R$ is the graph of the partial function $f\colon A \pto B$ defined by: if there is a $y$ such that $Rxy$, then $f(x) = y$, otherwise $f(x) \fu…».
  - **العربية المعيارية:** [السطر ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L57)؛ الطبعة الدولية: [ص ٦١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=61) (ترقيم المتن: ٦٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=61) (ترقيم المتن: ٦٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{prop} افترض أن $R \subseteq A \times B$ تتصف بالخاصية الآتية: متى صدق $Rxy$ و$Rxy'$ كان $y = y'$. عندئذ تكون $R$ الرسم البياني للدالة الجزئية $f\colon A \pto B$ المعرّفة كما يأتي: إذا وُجد $y$ بحيث $Rxy$، كان $f(x) = y$؛ وإلا فـ$f(x) \fundefined$. وإ…».

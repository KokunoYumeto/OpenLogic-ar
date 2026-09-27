# بطاقات الدالة والحساب — القرارات ٨٠٦–٨٠٧

[الرجوع إلى مقدمة الدفعة](README.md)

## U دالة وT علاقة عوديتان بدائيتان؛ ومن ثم ينتهي حساب الأولى والبت في الثانية لكل مدخل.

الأصل الإنجليزي: `U and T are primitive recursive and therefore total`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0321-FUNCTION-RELATION-20260907`.

**المعنى المقصود:** U دالة عودية بدائية وT علاقة عودية بدائية، ومن كليتهما القابلة للحساب ينتهي حساب الأولى والبت في الثانية.

**سبب الاختيار:** تمييز نوع U الدالي من نوع T العلائقي لازم: الدالة ترد قيمة والعلاقة يُبت في صدقها. قول «عوديتان بدائيتان» لا يمحو الفرق.

**سؤال مفتوح:** هل توضح العربية أن T قابلة للقرار لا أنها ترد قيمة من جنس U؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٥٧-٥٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/incompleteness/incompleteness-provability/tarski-thm.tex#L57-L58) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0321 — عدم قابلية الصدق للتعريف، وقوع ١:**
  - **الأصل:** [السطر ٥٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/incompleteness/incompleteness-provability/tarski-thm.tex#L57). الشاهد المسجل: «U(\umin{s}{T(e,x,s)})$ for all $x \in \Nat$, where $U$ and $T$ are primitive recursive and therefore total. Thus, $f(x)$ is defined».
  - **العربية المعيارية:** [السطر ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/incompleteness/incompleteness-provability/tarski-thm.tex#L54)؛ الطبعة الدولية: [ص ٥٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=596) (ترقيم المتن: ٥٩٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=597) (ترقيم المتن: ٥٩٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$U$ دالة و$T$ علاقة عوديتان بدائيتان؛ ومن ثم ينتهي حساب الأولى والبت في الثانية لكل مدخل. ولذلك تكون~$f(x)$ معرفة».
  - **العربية التراثية:** [السطر ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/incompleteness-provability/tarski-thm.tex#L53)؛ الطبعة التراثية: [ص ٥٨٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=582) (ترقيم المتن: ٥٨١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لكل $x \in \Nat$. وهنا $U$ دالة و$T$ علاقة عوديتان بدائيتان، فالحساب الخاص بكل منهما كلي. وعليه يكون $f(x)$ معرفًا،».

## البحث غير المحدود / الدالة المنتظمة / الدالة المميزة / الإسقاطات / قابلية التمثيل

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `unbounded search / regular function / characteristic function / projection / representability`. معرّف القرار: `compact:T-COMPUTABILITY-OPERATIONS`.

**المعنى المقصود:** عمليات في قابلية الحساب تشمل البحث غير المحدود والدوال المنتظمة والمميزة والإسقاطات والتمثيل.

**سبب الاختيار:** لا تساوي الدالة المميزة دالة الإسقاط؛ الأولى ترمز خاصية بقيمتين، والثانية تختار حجة. البحث غير المحدود قد يورث الجزئية، والتمثيل يتطلب صيغة مناسبة.

**سؤال مفتوح:** هل يوضح النص نوع كل عملية وشروط كليتها وجزئيتها؟

**شواهد عربية دقيقة مستعادة استدراكًا:** الطبعة التراثية: [الأسطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c.tex#L24) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.؛ الطبعة التراثية: [الأسطر ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c-representable.tex#L51) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/incompleteness/representability-in-q/c.tex#L24) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.؛ [الأسطر ٥٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/incompleteness/representability-in-q/c-representable.tex#L53) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**حدود استدراك الشاهد:** المؤشر المجمّد لا يسجّل وقوعًا إنجليزيًا دقيقًا لهذا القرار؛ استعيد سياق وحدته من أصل مثبت لا على أنه موضع معجمي حرفي لكل أجزاء الرأس المركب.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0648 — طائفة الدوال C، وقوع ١:**
  - **العربية التراثية:** [السطر ١٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c.tex#L18)؛ الطبعة التراثية: [ص ١٠١٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1013) (ترقيم المتن: ١٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item والإسقاطات،».
  - **العربية التراثية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c.tex#L19)؛ الطبعة التراثية: [ص ١٠١٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1013) (ترقيم المتن: ١٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item والدالة المميزة للمساواة،~$\Char{=}$؛».
  - **العربية التراثية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c.tex#L24)؛ الطبعة التراثية: [ص ١٠١٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1013) (ترقيم المتن: ١٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item والبحث غير المحدود المطبق على الدوال المنتظمة.».
- **OLP-0647 — تمثيل دوال C في ThQ، وقوع ٢:**
  - **العربية التراثية:** [السطر ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c-representable.tex#L51)؛ الطبعة التراثية: [ص ١٠١٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1010) (ترقيم المتن: ٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وسنمثل الصفر والخلف والجمع والضرب والدالة المميزة للمساواة والإسقاطات.».
  - **العربية التراثية:** [السطر ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/incompleteness/representability-in-q/c-representable.tex#L91)؛ الطبعة التراثية: [ص ١٠١١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1011) (ترقيم المتن: ١٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ويبقى البحث غير المحدود. لتكن~$g(x,\vec z)$ منتظمة قابلة للتمثيل».

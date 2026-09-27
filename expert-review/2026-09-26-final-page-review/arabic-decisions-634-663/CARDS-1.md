# بطاقات الاختيارات 634–636 — القرارات ٦٣٤–٦٣٦

[الرجوع إلى مقدمة الدفعة](README.md)

## مركّب النقطة الثابتة

الأصل الإنجليزي: `fixed-point combinator`. معرّف القرار: `TERM-FIXPOINT-COMBINATOR`.

**صفة الرأس المختصر:** جزء عربي من رأس السجل الموروث، لا اقتباس حرفي من السطر الجاري.

**المعنى المقصود:** حد في حساب لامبدا يعيد عند تطبيقه على دالة ما حدًا يحقق معادلة النقطة الثابتة لتلك الدالة.

**سبب الاختيار:** «مركّب النقطة الثابتة» يصف دوره التركيبي لا نقطة ثابتة بعينها. يظهر في متن الطبعة أيضًا «مؤلف النقطة الثابتة»؛ لا أُسوّي اللفظين صامتًا، وأبقي توحيدهما موضع مراجعة.

**سؤال مفتوح:** أيهما أنسب لحساب لامبدا: «مركّب» أم «مؤلف»، وهل يميز القارئ بين المؤثر والنقطة الناتجة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/lambda-definability/fixpoints.tex#L67) — يبني الأصل حدًا من حدود لامبدا يؤدي وظيفة إيجاد النقطة الثابتة، لا الدالة الثابتة.؛ [الأسطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/introduction/fixed-point-combinator.tex#L33) — يبني الأصل حدًا من حدود لامبدا يؤدي وظيفة إيجاد النقطة الثابتة، لا الدالة الثابتة.

**وجه جمع المواضع:** يبني الأصل حدًا من حدود لامبدا يؤدي وظيفة إيجاد النقطة الثابتة، لا الدالة الثابتة.

**تنقية رأس البطاقة الموروث:** فُصل الرأس الاصطلاحي من التعليق الإنجليزي الموروث؛ يظل «مؤلف النقطة الثابتة» في النص ويعرض السؤال للمراجع.

**مواضع المعجم المعاينة:** [ص ٢٦٤ من PDF (المطبوعة ٢٥٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=264)

**حدود الشاهد المعجمي:** PDF ص ٢٦٤، المطبوعة ٢٥٢، يثبت «نقطة ثابتة» ومعادلة f(x)=x، ولا يثبت اسم المركب اللامبدي.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0379 — النقاط الثابتة، وقوع ١:**
  - **الأصل:** [السطر ٦٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/lambda-definability/fixpoints.tex#L67). الشاهد المسجل: «The \emph{Y-combinator} is the term:».
  - **العربية المعيارية:** [السطر ٦٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/lambda-definability/fixpoints.tex#L65)؛ الطبعة الدولية: [ص ٦٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=668) (ترقيم المتن: ٦٦٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٦٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=669) (ترقيم المتن: ٦٦٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مركّب~Y} هو الحد:».
  - **العربية التراثية:** [السطر ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/lambda-definability/fixpoints.tex#L63)؛ الطبعة التراثية: [ص ٦٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=652) (ترقيم المتن: ٦٥١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مركّب~Y} هو الحد:».
- **OLP-0354 — مؤلفات النقطة الثابتة، وقوع ٢:**
  - **الأصل:** [السطر ٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/introduction/fixed-point-combinator.tex#L33). الشاهد المسجل: «g(Yg)$. This is known as ``Curry's combinator.'' If instead one takes».
  - **العربية المعيارية:** [السطر ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/introduction/fixed-point-combinator.tex#L33)؛ الطبعة الدولية: [ص ٦٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=632) (ترقيم المتن: ٦٣١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=633) (ترقيم المتن: ٦٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$Yg \equiv_\beta g(Yg)$. وهذا ما يعرف باسم «مؤلف كاري». أما إذا أخذنا».
  - **العربية التراثية:** [السطر ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/introduction/fixed-point-combinator.tex#L33)؛ الطبعة التراثية: [ص ٦١٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=616) (ترقيم المتن: ٦١٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$Yg \equiv_\beta g(Yg)$. وهذا هو «مؤلف كاري». وأما إذا وضعنا».
- **OLP-0379 — النقاط الثابتة، وقوع ٣:**
  - **الأصل:** [السطر ١٥٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/lambda-definability/fixpoints.tex#L157). الشاهد المسجل: «The $Y$ combinator of \olref{defn:Turing-Y} is due to Alan».
  - **العربية المعيارية:** [السطر ١٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/lambda-definability/fixpoints.tex#L154)؛ الطبعة الدولية: [ص ٦٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=670) (ترقيم المتن: ٦٦٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=671) (ترقيم المتن: ٦٧٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «يرجع مركّب~$Y$ في \olref{defn:Turing-Y} إلى آلان تورنغ. وقد اقترح».
  - **العربية التراثية:** [السطر ١٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/lambda-definability/fixpoints.tex#L152)؛ الطبعة التراثية: [ص ٦٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=654) (ترقيم المتن: ٦٥٣)، [ص ٦٥٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=655) (ترقيم المتن: ٦٥٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ومركّب~$Y$ في \olref{defn:Turing-Y} من وضع آلان تورنغ. ولألونزو تشيرش صيغة أخرى نرمز إليها بـ~$Y_C$: \[ Y_C \ident \lambd[g][(\lambd[x][g(xx)])(\lambd[x][g(xx)])]. \] ومركّب تشيرش أضعف قليلًا من مركّب تورنغ: فهو يحقق».

## علاقة الإلزام

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `forcing relation`. معرّف القرار: `compact:T-FORCING`.

**المعنى المقصود:** علاقة بين حالة أو عالم وصيغة تقرر متى تلزم الصيغة في تلك الحالة بحسب تعريف دلالي استقرائي.

**سبب الاختيار:** «علاقة الإلزام» تحفظ كونها علاقة دلالية لا إكراهًا سببيًا؛ يجب عدم استيراد دلالة forcing في نظرية المجموعات إلى هذه الوحدة الحدسية بغير تحقق.

**سؤال مفتوح:** هل «الإلزام» واضح في دلالة كريبكه الحدسية، أم الأفضل «علاقة الفرض» أو إبقاء الاسم الأجنبي عند أول ورود؟

**شواهد عربية دقيقة مستعادة استدراكًا:** الطبعة التراثية: [الأسطر ١٧٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/first-order-logic/beyond/intuitionistic-logic.tex#L174) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ٢٠٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/beyond/intuitionistic-logic.tex#L207) — يعرّف الأصل forcing relation مع حالة وصيغة وشروط صدقها.

**وجه جمع المواضع:** يعرّف الأصل forcing relation مع حالة وصيغة وشروط صدقها.

**حدود استدراك الشاهد:** المؤشر المجمّد لا يسجّل وقوعًا إنجليزيًا دقيقًا لهذا القرار؛ استعيد سياق وحدته من أصل مثبت لا على أنه موضع معجمي حرفي لكل أجزاء الرأس المركب.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0179 — المنطق الحدسي، وقوع ١:**

## متتالية تكوين؛ بناء من الأسفل إلى الأعلى؛ استقراء قوي؛ متتالية جزئية ابتدائية حقيقية

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `formation sequence; bottom-up construction; strong induction; proper initial subsequence`. معرّف القرار: `locale-ar-chosen-c48bedf13e287c34`.

**المعنى المقصود:** متتالية تُظهر مراحل تكوين الصيغة، ويجري عليها الاستقراء القوي لأن الصيغ الجزئية تقع في مقاطع أولية حقيقية.

**سبب الاختيار:** «متتالية تكوين» تُبقي ترتيب البناء؛ و«مقطع ابتدائي حقيقي» يضبط أن طول الجزء أقصر من المتتالية الأصلية. عبارة البناء من الأسفل إلى الأعلى وصف لاتجاه البرهان لا رتبة لغوية إنجليزية منقولة بلا معنى.

**سؤال مفتوح:** هل يفضّل «مقطع أولي حقيقي» على «متتالية جزئية ابتدائية حقيقية»، وهل توضّح الصياغة سبب جواز فرض الاستقراء القوي؟

**شواهد عربية دقيقة مستعادة استدراكًا:** الطبعة التراثية: [الأسطر ١٥١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/propositional-logic/syntax-and-semantics/formation-sequences.tex#L151) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ١٤٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/propositional-logic/syntax-and-semantics/formation-sequences.tex#L145) — يعطي الأصل متتالية تكوين لصيغة ويقارن مواضع صيغها الجزئية برقمها الأخير.

**وجه جمع المواضع:** يعطي الأصل متتالية تكوين لصيغة ويقارن مواضع صيغها الجزئية برقمها الأخير.

**حدود استدراك الشاهد:** المؤشر المجمّد لا يسجّل وقوعًا إنجليزيًا دقيقًا لهذا القرار؛ استعيد سياق وحدته من أصل مثبت لا على أنه موضع معجمي حرفي لكل أجزاء الرأس المركب.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0060 — متتاليات التكوين، وقوع ١:**

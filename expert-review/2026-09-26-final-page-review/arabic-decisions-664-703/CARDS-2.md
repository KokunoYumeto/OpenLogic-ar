# بطاقات القابلية للعكس والتشاكل — القرارات ٦٦٦–٦٦٧

[الرجوع إلى مقدمة الدفعة](README.md)

## قاعدة قابلة للعكس

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `invertible rule`. معرّف القرار: `TERM-INVERTIBLE`.

**المعنى المقصود:** قاعدة برهانية يتيح تطبيقها في جهة معينة استرجاع حالة تعادل الحكم الأصلي في شروط النسق.

**سبب الاختيار:** «قابلة للعكس» في حساب التتابعيات ليست بالضرورة وجود معكوس جبري لعنصر أو مصفوفة؛ مدخل المعجم لذلك السياق الجبري مجاور فقط.

**سؤال مفتوح:** هل يحدد النص جهة العكس ومجال صلاحية القاعدة، أم يتركها كخاصية غير مشروطة؟

**شواهد عربية دقيقة مستعادة استدراكًا:** الطبعة التراثية: [الأسطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/sequent-calculus/invertibility.tex#L23) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ٢٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/invertibility.tex#L23) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**حدود استدراك الشاهد:** المؤشر المجمّد لا يسجّل وقوعًا إنجليزيًا دقيقًا لهذا القرار؛ استعيد سياق وحدته من أصل مثبت لا على أنه موضع معجمي حرفي لكل أجزاء الرأس المركب.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0701 — في قابلية القواعد للعكس، وقوع ١:**
  - **العربية التراثية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/sequent-calculus/invertibility.tex)؛ الطبعة التراثية: [ص ١١١٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1115) (ترقيم المتن: ١١٤) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «\olsection{في قابلية القواعد للعكس} \begin{defn} نقول إن القاعدة~$R$، \[ \AxiomC{$S_1$} \AxiomC{$\dots$} \AxiomC{$S_n$} \RightLabel{$R$} \TrinaryInfC{$S$} \DisplayProof \] \emph{قابلة للعكس} في نظام ما متى كان ثبوت~$\Proves S$ يستلزم $\Proves S_i$ لكل~$i=1$…».

## التشاكل

الأصل الإنجليزي: `isomorphism`. معرّف القرار: `ar-classical-0701-0722-isomorphism`.

**المعنى المقصود:** تطابق بنيوي بواسطة تقابل يحفظ العلاقات والعمليات المعنية في الجهتين.

**سبب الاختيار:** اختارت الطبعة «التشاكل»؛ المعجم المصور يطبع isomorphism «تماكل»، وربما يعكس تخصصًا جبريًا. لم أبدل لفظ الطبعة آليًا لأن صون البنية وشروط الحفظ أهم من التشابه الصوتي.

**سؤال مفتوح:** هل «تشاكل» هو الاصطلاح الأنسب للنماذج والبنى المنطقية، أم «تماكل» المعجمي، وهل يوضح النص تقابل الحفظ العكسي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/isomorphic-functions.tex#L38) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**مواضع المعجم المعاينة:** [ص ٣٧٩ من PDF (المطبوعة ٣٦٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=379)

**حدود الشاهد المعجمي:** PDF ص ٣٧٩، المطبوعة ٣٦٧، يطبع isomorphism «تماكل» ويصف دالة تقابلية تحفظ العمليات بين بنيتين جبريتين.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0717 — في التشاكل، وقوع ١:**
  - **الأصل:** [السطر ٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/isomorphic-functions.tex#L38). الشاهد المسجل: «Y$ where $f(x) = 7-x$ is an isomorphism between $\tuple{X,<}$ and».
  - **العربية المعيارية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L11)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{التشاكل}».
  - **العربية المعيارية:** [السطر ١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L14)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{التشاكل} هو تقابل يحفظ بنية المجموعتين اللتين يربط بينهما، حيث تتمثل».
  - **العربية المعيارية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L17)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «التالي، وأصغر من، وأكبر من. ويكون التشاكل بينهما !!a{bijection} يحفظ».
  - **العربية المعيارية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L19)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فإنها تكون تشاكلًا متى تحقق، لكل $i,j\in X$، أن $i<j$ إذا وفقط إذا».
  - **العربية المعيارية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L24)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[التشاكل]».
  - **العربية المعيارية:** [السطر ٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L28)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$Y$. يكون $f$ \emph{تشاكلًا} من $U$ إلى $V$ إذا وفقط إذا كان يحفظ».
  - **العربية المعيارية:** [السطر ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/isomorphic-functions.tex#L36)؛ الطبعة الدولية: [ص ١١٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=1157) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ١١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=1158) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$f(x) = 7-x$ تشاكل بين $\tuple{X,<}$ و$\tuple{Y,>}$.».
  - **العربية التراثية:** [السطر ١١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L11)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{في التشاكل}».
  - **العربية التراثية:** [السطر ١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L14)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{التشاكل} تقابل بين مجموعتين يصون بنيتهما، والمراد بالبنية هنا».
  - **العربية التراثية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L17)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «من، وأكبر من. والتشاكل بينهما !!a{bijection} يحفظ هذه العلاقات. فإذا».
  - **العربية التراثية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L19)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «كانت $f \colon X \to Y$~!!a{bijective}، كانت تشاكلًا متى تحقق،».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L25)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[التشاكل]».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L29)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$f$ \emph{تشاكل} من $U$ إلى $V$ إذا وفقط إذا حفظ البنية العلائقية؛».
  - **العربية التراثية:** [السطر ٣٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/isomorphic-functions.tex#L37)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$f(x) = 7-x$ تشاكلًا بين $\tuple{X,<}$ و$\tuple{Y,>}$.».

# بطاقات الحلقة والحقل — القرارات ٣٩٦–٤٠٥

[الرجوع إلى مقدمة الدفعة](README.md)

## حلقة تبديلية؛ حلقة مرتبة؛ حقل مرتب

الأصل الإنجليزي: `commutative ring; ordered ring; ordered field`. معرّف القرار: `locale-ar-chosen-58fe03b0a1ac0858`.

**المعنى المقصود:** الحلقة التبديلية ذات جمع وضرب تبديليين؛ والحلقة أو الحقل المرتب بنية توافق فيها العلاقة المرتبة العمليات؛ والحقل يضيف معكوس الضرب لغير الصفر.

**سبب الاختيار:** يفرق أصل فصل الفحص بين حلقة تبديليّة للصحيحة، وبنية مرتبة، وحقل مرتب للنسبية والحقيقية. أبقت الطبعة «حلقة» و«حقل» رأسين مختلفين، ووصفي «تبديلية» و«مرتبة» حيث تقرر المعادلات الملائمة. المعجم يطبع commutative ring «حلقة تبديلية»، ordered field «حقل مرتب»، وordered rings بصيغة الجمع «حلقات مرتبة»؛ يشهد للأسماء لا لكل بديهية في الأصل.

**سؤال مفتوح:** هل تظهر فروق الحلقة والحقل والترتيب والتبديل في النصوص الثلاثة دون نقل خاصية الحقل إلى الصحيحة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٨-٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L18-L24) — تعدد المواضع يشهد لاختلاف البنى التي يثبتها الفصل تباعًا.

**وجه جمع المواضع:** تعدد المواضع يشهد لاختلاف البنى التي يثبتها الفصل تباعًا.

**مواضع المعجم المعاينة:** [ص ١١٧ من PDF (المطبوعة ١٠٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=117)، [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)

**حدود الشاهد المعجمي:** PDF ص ١١٧ يطبع commutative ring = «حلقة تبديلية»؛ وص ٥٠٦ يطبع ordered field = «حقل مرتب» وordered rings = «حلقات مرتبة». هذا يؤيد أسماء البنى، أما اختلاف بديهياتها فيحكمه الأصل.

**بديل جدير بالمقارنة:** جبر تبديلي؛ أعم من المقصود بالحلقات هنا

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في فصل البنى وفي شاهدي الاسمين، متوسطة في انتظام الصيغ عبر الطبعات.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ١٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L18). الشاهد المسجل: «In \olref[int]{sec}, we defined addition and multiplication on $\Int$. We want to show that, as defined, they endow $\Int$ with the structure we ``would want'' it to have. In particular, the structure in question is that of a commutative ring. \begin{defn}…».
  - **الأصل:** [السطر ١١١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L111). الشاهد المسجل: «\begin{defn} An \emph{ordered ring} is a commutative ring which is also equipped with a total order relation, $\leq$, such that: \begin{align*} a \leq b &\lif a + c \leq b + c\\ (a \leq b \land 0 \leq c) &\lif a \times c \leq b \times c \end{align*} \end{defn}».
  - **الأصل:** [السطر ١٢٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L127). الشاهد المسجل: «This takes care of the integers. But now we need to show very similar things of the rationals. In particular, we now need to show that the rationals form an ordered \emph{field}, under our given definitions of $+$, $\times$, and $\leq$: \begin{defn}\ollabel…».
  - **العربية المعيارية:** [السطر ١٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L17)؛ الطبعة الدولية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=94) (ترقيم المتن: ٩٣)، [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=94) (ترقيم المتن: ٩٣)، [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «عرّفنا في \olref[int]{sec} الجمع والضرب على $\Int$. ونريد أن نبين أن هاتين العمليتين، كما عُرّفتا، تمنحان $\Int$ البنية التي «نريد» لها أن تتمتع بها. والبنية المقصودة على وجه الخصوص هي بنية حلقة تبديلية. \begin{defn} \emph{الحلقة التبديلية} هي مجموعة $S$ مز…».
  - **العربية المعيارية:** [السطر ١١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L110)؛ الطبعة الدولية: [ص ٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=96) (ترقيم المتن: ٩٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=96) (ترقيم المتن: ٩٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn} \emph{الحلقة المرتبة} هي حلقة تبديلية مزودة أيضًا بعلاقة ترتيب كلي، $\leq$، بحيث: \begin{align*} a \leq b &\lif a + c \leq b + c\\ (a \leq b \land 0 \leq c) &\lif a \times c \leq b \times c \end{align*} \end{defn}».
  - **العربية المعيارية:** [السطر ١٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L126)؛ الطبعة الدولية: [ص ٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=96) (ترقيم المتن: ٩٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=96) (ترقيم المتن: ٩٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وهذا يفرغ من الأعداد الصحيحة. لكن يلزمنا الآن أن نبين أمورًا شديدة الشبه بشأن الأعداد النسبية. وعلى وجه الخصوص، يلزمنا أن نبين أن الأعداد النسبية تكوّن \emph{حقلًا} مرتبًا، وفق تعريفاتنا المعطاة لـ$+$ و$\times$ و$\leq$: \begin{defn}\ollabel{orderedfield} %…».
  - **العربية التراثية:** [السطر ١٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L14)؛ الطبعة التراثية: [ص ٩٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=90) (ترقيم المتن: ٨٩)، [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «قد عرفنا الجمع والضرب على $\Int$ في \olref[int]{sec}. ومطلبنا أن تمنح هاتان العمليتان $\Int$ البنية التي قصدناها لها، وهي على التعيين بنية الحلقة التبديلية. \begin{defn} \emph{الحلقة التبديلية} مجموعة $S$ عين فيها عنصران $0$ و$1$ وعمليتان $+$ و$\times$، واس…».
  - **العربية التراثية:** [السطر ٨٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L85)؛ الطبعة التراثية: [ص ٩٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=92) (ترقيم المتن: ٩١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn} \emph{الحلقة المرتبة} حلقة تبديلية عين فيها ترتيب كلي $\leq$ يحقق: \begin{align*} a \leq b &\lif a + c \leq b + c\\ (a \leq b \land 0 \leq c) &\lif a \times c \leq b \times c \end{align*} \end{defn}».
  - **العربية التراثية:** [السطر ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L99)؛ الطبعة التراثية: [ص ٩٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=92) (ترقيم المتن: ٩١)، [ص ٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=93) (ترقيم المتن: ٩٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وبهذا يفرغ النظر في الصحيحة، ونطلب للنسبية أحكامًا قريبة منها. والمقصود خاصة أنها \emph{حقل} مرتب، وفق ما عرفناه من $+$ و$\times$ و$\leq$: \begin{defn}\ollabel{orderedfield} % تصحيح تعريفي (0047-I1): استُبعدت الحلقة الصفرية بإضافة الشرط القياسي 0 != 1. \emp…».

## التبديلية

الأصل الإنجليزي: `Commutativity`. معرّف القرار: `retro-0005-0050:emphasis:021e057d3e2a7d19`.

**المعنى المقصود:** تبديل طرفي الجمع والضرب من غير تغيير النتيجة في بديهيات الحلقة.

**سبب الاختيار:** يقابل عنوان Commutativity المعادلتين أ+ب=ب+أ وأب=بأ. «التبديلية» اسم الخاصية المتكرر مع الحلقة؛ ويطبع المعجم «قانون تبديلي» و«حلقة تبديلية»، فيسند الاشتقاق وإن لم يطبع المصدر المجرد نفسه في هذين المدخلين.

**سؤال مفتوح:** هل «التبديلية» عنوان مختصر مناسب للمعادلتين معًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L28) — المعادلتان تحت العنوان هما دليل المقصود بالتبديل.

**وجه جمع المواضع:** المعادلتان تحت العنوان هما دليل المقصود بالتبديل.

**مواضع المعجم المعاينة:** [ص ١١٧ من PDF (المطبوعة ١٠٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=117)

**حدود الشاهد المعجمي:** PDF ص ١١٧ يطبع commutative law = «قانون تبديلي» وcommutative ring = «حلقة تبديلية»؛ عنوان «التبديلية» اشتقاق اسم خاصية منهما.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية لأن المعادلات والمدخل متوافقان.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ٢٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L28). الشاهد المسجل: «\emph{Commutativity}&&a + b &= b+ a \\».
  - **العربية المعيارية:** [السطر ٢٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L27)؛ الطبعة الدولية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{التبديلية}&&a + b &= b+ a \\».
  - **العربية التراثية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L21)؛ الطبعة التراثية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{التبديلية}&&a + b &= b+ a \\».

## العنصران المحايدان

الأصل الإنجليزي: `Identities`. معرّف القرار: `retro-0005-0050:emphasis:28d75bf7884cf22f`.

**المعنى المقصود:** العنصران المحايدان: صفر للجمع وواحد للضرب في البديهيات المعروضة.

**سبب الاختيار:** رأس Identities في الأصل يغطي سطرَي أ+٠=أ وأ×١=أ، لا عنصرًا واحدًا ولا متطابقة حسابية عامة. صيغة التثنية «العنصران المحايدان» تجعل عدد الشاهدين وموضع كل منهما ظاهرين. يشرح المعجم العنصر المحايد جمعيًا في مدخله، أما تثنية الرأس فمستفادة من الجدول.

**سؤال مفتوح:** هل تمنع التثنية الخلط بين العنصر المحايد والمتطابقة بوصفها مساواة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L30) — سطرَا الصفر والواحد يتبعان رأس Identities نفسه.

**وجه جمع المواضع:** سطرَا الصفر والواحد يتبعان رأس Identities نفسه.

**مواضع المعجم المعاينة:** [ص ١٩ من PDF (المطبوعة ٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=19)

**حدود الشاهد المعجمي:** PDF ص ١٩ يطبع additive identity = «عنصر محايد جمعي»؛ لا يطبع رأس «العنصران المحايدان» المركب، الذي يستفاد من معادلتَي الأصل.

**بديل جدير بالمقارنة:** المحايدان؛ أقصر لكنه لا يصرح بأنهما عنصران

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في عدد العنصرين والوظيفة الجبرية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ٣٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L30). الشاهد المسجل: «\emph{Identities}&&a + 0 &= a \\».
  - **العربية المعيارية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L29)؛ الطبعة الدولية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{العنصران المحايدان}&&a + 0 &= a \\».
  - **العربية التراثية:** [السطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L23)؛ الطبعة التراثية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{العنصران المحايدان}&&a + 0 &= a \\».

## التجميعية

الأصل الإنجليزي: `Associativity`. معرّف القرار: `retro-0005-0050:emphasis:521887fad68ed704`.

**المعنى المقصود:** ثبات حاصل الجمع أو الضرب عند تغيير موضع الأقواس بين ثلاثة عناصر.

**سبب الاختيار:** تضع لائحة الحلقة Associativity قبل معادلتَي أ+(ب+ج)=(أ+ب)+ج ومثيلتهما للضرب. أخذت الطبعة «التجميعية» اسمًا للخاصية، ويطبع المعجم «قانون تجميعي» بالمعادلة نفسها؛ لا نخلطها بالتبديلية التي تبدل ترتيب العناصر.

**سؤال مفتوح:** هل «التجميعية» عنوان واضح لتغيير الأقواس دون تبديل ترتيب العناصر؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L26) — معادلات الأصل تعين خاصية الأقواس لا تبديل الطرفين.

**وجه جمع المواضع:** معادلات الأصل تعين خاصية الأقواس لا تبديل الطرفين.

**مواضع المعجم المعاينة:** [ص ٥٢ من PDF (المطبوعة ٤٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=52)

**حدود الشاهد المعجمي:** PDF ص ٥٢، المطبوعة ٤٠، يطبع associative law = «قانون تجميعي» مع أ⋅(ب⋅ج)=(أ⋅ب)⋅ج؛ «التجميعية» اسم خاصية مشتق لا اقتباس حرفي للرأس.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التمييز الرياضي والشاهد المعجمي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L26). الشاهد المسجل: «\emph{Associativity}&&a + (b+ c) & = (a + b) + c \\».
  - **العربية المعيارية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L25)؛ الطبعة الدولية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{التجميعية}&&a + (b+ c) & = (a + b) + c \\».
  - **العربية التراثية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L19)؛ الطبعة التراثية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{التجميعية}&&a + (b+ c) & = (a + b) + c \\».
- **OLP-0047 — الحلقات والحقول، وقوع ٢:**
  - **الأصل:** [السطر ٤١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L41). الشاهد المسجل: «here is how to prove \emph{Associativity}, in the case of addition:».
  - **العربية المعيارية:** [السطر ٤٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L42)؛ الطبعة الدولية: [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{التجميعية} في حالة الجمع:».
  - **العربية التراثية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L31)؛ الطبعة التراثية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فإثبات أن الأعداد الصحيحة حلقة تبديلية يرجع إلى تحقيق هذه الشروط الثمانية. وليس واحد منها {صعبًا}، وإن كان في استيفائها شيء من المشقة. ونمثل لذلك ببرهان \emph{التجميعية} للجمع.».

## وجود المعكوس الجمعي

الأصل الإنجليزي: `Additive Inverse`. معرّف القرار: `retro-0005-0050:emphasis:5c0e63242ecf9e05`.

**المعنى المقصود:** إثبات وجود معكوس جمعي لكل عنصر في الحلقة، لا مجرد تسمية عنصر معلوم.

**سبب الاختيار:** بعد عرض البديهيات يقول الأصل here is how to prove Additive Inverse. أضافت الطبعة «وجود» لأن الفقرة تبرهن كمية الوجود ∀أ∃ب(أ+ب=٠)، لا لأنها غيرت اسم المعكوس نفسه. يطبع المعجم «نظير جمعي (مقلوب جمعي)» لا «معكوس جمعي»، فنصرح بالخلاف.

**سؤال مفتوح:** هل «وجود المعكوس الجمعي» أوضح من رأس الخاصية المقتضب، وهل يُراجع لفظ «معكوس» قياسًا إلى «نظير» المعجمي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L62) — السياق يفتتح برهان شرط الوجود العام لكل عنصر.

**وجه جمع المواضع:** السياق يفتتح برهان شرط الوجود العام لكل عنصر.

**مواضع المعجم المعاينة:** [ص ١٩ من PDF (المطبوعة ٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=19)

**حدود الشاهد المعجمي:** PDF ص ١٩ يطبع additive inverse = «نظير جمعي (مقلوب جمعي)»؛ لا يطبع «معكوس جمعي» ولا لفظ «وجود» في رأس المدخل، مع بقاء الصيغة الجبرية في الأصل حاكمة للمعنى.

**بديل جدير بالمقارنة:** وجود النظير الجمعي؛ يقرب من رأس المعجم

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في وظيفة فقرة البرهان، متوسطة في اسم العنصر.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ٦٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L62). الشاهد المسجل: «Equally, here is how to prove \emph{Additive Inverse}:».
  - **العربية المعيارية:** [السطر ٦٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L62)؛ الطبعة الدولية: [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=95) (ترقيم المتن: ٩٤) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وبالمثل، إليك كيفية برهنة \emph{وجود المعكوس الجمعي}:».
  - **العربية التراثية:** [السطر ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L49)؛ الطبعة التراثية: [ص ٩٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=92) (ترقيم المتن: ٩١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ونبين على النهج نفسه \emph{وجود المعكوس الجمعي}.».

## حقل

الأصل الإنجليزي: `field`. معرّف القرار: `retro-0005-0050:emphasis:8dcf0a8f9e05ce62`.

**المعنى المقصود:** الحقل بنية فيها المعكوس الضربي لكل عنصر غير صفر، وتناقش هنا مرتبةً للنسبية.

**سبب الاختيار:** في عبارة ordered field يقع التوكيد على field وحده، ولكن وصف المرتب بعده جزء من البنية المرادة. أبقت التراثية «حقل» من غير علامة نصب ظاهرة في اللفظ الموكَّد، مع إلحاق «مرتب»؛ المدخل المعجمي يطبع «حقل مرتب» مركبًا.

**سؤال مفتوح:** هل يظهر في «إنها حقل مرتب» أن الترتيب جزء من الدعوى لا صفة عرضية تضاف بعد تقرير الحقل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L129) — الجملة الأصلية تعرض الهدف المخصوص لبناء النسبية بوصفها حقلًا مرتبًا.

**وجه جمع المواضع:** الجملة الأصلية تعرض الهدف المخصوص لبناء النسبية بوصفها حقلًا مرتبًا.

**مواضع المعجم المعاينة:** [ص ٥٠٦ من PDF (المطبوعة ٤٩٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=506)

**حدود الشاهد المعجمي:** PDF ص ٥٠٦ يطبع ordered field = «حقل مرتب»؛ شاهد للاسم المركب، لا للمعادلات التي تثبت تحقق النسبية له.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في اسم البنية، متوسطة في سبك الجملة التراثية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ١٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L129). الشاهد المسجل: «rationals form an ordered \emph{field}, under our given definitions of».
  - **العربية المعيارية:** [السطر ١٢٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L128)؛ الطبعة الدولية: [ص ٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=96) (ترقيم المتن: ٩٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=96) (ترقيم المتن: ٩٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «النسبية تكوّن \emph{حقلًا} مرتبًا، وفق تعريفاتنا المعطاة لـ$+$».
  - **العربية التراثية:** [السطر ٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L99)؛ الطبعة التراثية: [ص ٩٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=92) (ترقيم المتن: ٩١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وبهذا يفرغ النظر في الصحيحة، ونطلب للنسبية أحكامًا قريبة منها. والمقصود خاصة أنها \emph{حقل} مرتب، وفق ما عرفناه من $+$ و$\times$ و$\leq$:».

## المعكوس الجمعي

الأصل الإنجليزي: `Additive Inverse`. معرّف القرار: `retro-0005-0050:emphasis:9985b6886e382b19`.

**المعنى المقصود:** بديهية لكل أ يوجد ب يحقق أ+ب=٠، أي المعكوس الجمعي.

**سبب الاختيار:** عنوان لائحة البديهيات مختصر Additive Inverse وبجانبه كمية الوجود، فحافظت الطبعة على «المعكوس الجمعي» عنوانًا قصيرًا بخلاف فقرة البرهان التي قالت «وجود المعكوس». يطبع المعجم «نظير جمعي (مقلوب جمعي)»؛ فاختلاف الاسم مؤقت للمراجعة.

**سؤال مفتوح:** هل «المعكوس الجمعي» مألوف وواضح مع الصيغة، أم يُستبدل بـ«النظير الجمعي» المعجمي اتساقًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L32) — كمية الوجود والصفر إلى يمين العنوان تعين المقصود.

**وجه جمع المواضع:** كمية الوجود والصفر إلى يمين العنوان تعين المقصود.

**مواضع المعجم المعاينة:** [ص ١٩ من PDF (المطبوعة ٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=19)

**حدود الشاهد المعجمي:** PDF ص ١٩ يطبع additive inverse = «نظير جمعي (مقلوب جمعي)»؛ رأس الطبعة «المعكوس الجمعي» مختلف لفظًا مع اتحاد الوظيفة الجبرية.

**بديل جدير بالمقارنة:** النظير الجمعي؛ رأس المعجم المصور

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الصيغة والوظيفة، متوسطة في تفضيل الاسم.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L32). الشاهد المسجل: «\emph{Additive Inverse}&&(\exists b\in S)0&=a + b\\».
  - **العربية المعيارية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L31)؛ الطبعة الدولية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{المعكوس الجمعي}&&(\exists b\in S)0&=a + b\\».
  - **العربية التراثية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L25)؛ الطبعة التراثية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{المعكوس الجمعي}&&(\exists b\in S)0&=a + b\\».

## كامل

الأصل الإنجليزي: `complete`. معرّف القرار: `retro-0005-0050:emphasis:9c33589d88c53a80`.

**المعنى المقصود:** حقل مرتب كامل: يملك خاصية أن لكل مجموعة غير خالية محدودة من أعلى أصغر حد علوي.

**سبب الاختيار:** يطلب الأصل أن تكون الحقيقية complete ordered field، ثم يحيل إلى برهان اكتمال القطوع. جاء «كامل» نعتًا للحقل بعد «مرتب» في سبك التراثية، لا وصفًا لعدد عناصره. يطبع المعجم رأس «حقل مرتب تام»؛ لفظ «كامل» هنا مرادف طبعة يحتاج نظرًا في الملاءمة الاصطلاحية.

**سؤال مفتوح:** هل «حقل مرتب كامل» أو «حقل مرتب تام» المعجمي أجلى في هذا الباب، مع إرجاع معنى الكمال إلى أصغر حد علوي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L147) — تحدد الإحالة إلى برهان الاكتمال نوع الكمال المطلوب.

**وجه جمع المواضع:** تحدد الإحالة إلى برهان الاكتمال نوع الكمال المطلوب.

**مواضع المعجم المعاينة:** [ص ١٢١ من PDF (المطبوعة ١٠٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=121)

**حدود الشاهد المعجمي:** PDF ص ١٢١، المطبوعة ١٠٩، يطبع complete ordered field = «حقل مرتب تام» ويصف بديهية أصغر حد أعلى؛ «كامل» ليس لفظ الرأس المطبوع.

**بديل جدير بالمقارنة:** تام؛ يطابق المعجم مباشرة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى الاكتمال، متوسطة في اختيار «كامل» أمام «تام».

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ١٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L147). الشاهد المسجل: «constitutes a \emph{complete} ordered field, i.e., an ordered field».
  - **العربية المعيارية:** [السطر ١٥١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L151)؛ الطبعة الدولية: [ص ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=97) (ترقيم المتن: ٩٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=97) (ترقيم المتن: ٩٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{كاملًا}، أي حقلًا مرتبًا يتمتع بخاصية الاكتمال. وقد أثبتت».
  - **العربية التراثية:** [السطر ١١٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L118)؛ الطبعة التراثية: [ص ٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=93) (ترقيم المتن: ٩٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فإذا فرغنا من الصحيحة والنسبية بقيت الحقيقية. ومطلبنا أن $\Real$ حقل مرتب \emph{كامل}؛ أي حقل مرتب ذو خاصية الاكتمال. وقد ثبت في \olref[cuts]{realcompleteness} أن $\Real$ كاملة، وبقي استيفاء الحساب الذي يثبت أن $\Real$ حقل مرتب، وفيه طول.».

## المعكوس الضربي

الأصل الإنجليزي: `Multiplicative Inverse`. معرّف القرار: `retro-0005-0050:emphasis:9fc2b87b3802a051`.

**المعنى المقصود:** لكل عنصر غير صفر في الحقل عنصر يضرب فيه فيعطي واحدًا.

**سبب الاختيار:** يورد الأصل Multiplicative Inverse مع الصيغة ∀أ≠٠∃ب(أ×ب=١)؛ «المعكوس الضربي» يحدد جهة العملية وشرط غير الصفر. يطبع المعجم الاسم نفسه لفظًا، فتسند الصفحة الرأس دون أن تبيح إسقاط شرط أ≠٠.

**سؤال مفتوح:** هل تظل لا صفرية العنصر ظاهرة عند قراءة رأس «المعكوس الضربي» مع الصيغة المجاورة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L134) — الصيغة تمنع شمول الصفر بوجود معكوس ضربي.

**وجه جمع المواضع:** الصيغة تمنع شمول الصفر بوجود معكوس ضربي.

**مواضع المعجم المعاينة:** [ص ٤٧٢ من PDF (المطبوعة ٤٦٠)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=472)

**حدود الشاهد المعجمي:** PDF ص ٤٧٢، المطبوعة ٤٦٠، يطبع multiplicative inverse = «معكوس ضربي»؛ شاهد مباشر للاسم، مع بقاء شرط غير الصفر مستندًا إلى صيغة الأصل.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المصطلح والمعنى والشرط.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ١٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L134). الشاهد المسجل: «\emph{Multiplicative Inverse}& & (\forall a \in S \setminus \{0\})(\exists b \in S) a\times b& = 1».
  - **العربية المعيارية:** [السطر ١٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L134)؛ الطبعة الدولية: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=94) (ترقيم المتن: ٩٣) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{المعكوس الضربي}& & (\forall a \in S \setminus \{0\})(\exists b \in S) a\times b& = 1».
  - **العربية التراثية:** [السطر ١٠٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L104)؛ الطبعة التراثية: [ص ٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=91) (ترقيم المتن: ٩٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{المعكوس الضربي}& & (\forall a \in S \setminus \{0\})(\exists b \in S) a\times b& = 1».

## قطع

الأصل الإنجليزي: `cut`. معرّف القرار: `retro-0005-0050:emphasis:dd196344e6fa924c`.

**المعنى المقصود:** مجموع قطعين α وβ، بحسب التعريف، يفي من جديد بشروط قطع ديديكند.

**سبب الاختيار:** يحيل الأصل إلى إثبات أن α+β cut بعد تعريف جمع القطوع؛ التراثية تستعمل «قطع» نكرة خبرًا للنتيجة، لا عملية قطع هندسية. معجم دمشق يطبع «مقطع ديديكند» للاسم الكامل، فيبقى المختصر في الطبعة موضع مراجعة مع سياقه الصريح α وβ.

**سؤال مفتوح:** هل «قطع» واضح في إثبات انغلاق الجمع على القطوع، أم ينبغي الاسم الكامل دفعًا لاحتمال المعنى الهندسي؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٥٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L155) — الجملة تختبر بقاء شروط القطع بعد عملية الجمع.

**وجه جمع المواضع:** الجملة تختبر بقاء شروط القطع بعد عملية الجمع.

**مواضع المعجم المعاينة:** [ص ١٧٥ من PDF (المطبوعة ١٦٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=175)

**حدود الشاهد المعجمي:** PDF ص ١٧٥ يطبع Dedekind cut = «مقطع ديديكند»؛ «قطع» اختصار الطبعة في سياق سبق فيه التعريف الرسمي.

**بديل جدير بالمقارنة:** مقطع ديديكند؛ أوضح خارج السياق لكنه أطول في برهان مكرر

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في وظيفة الإغلاق، متوسطة في الاختصار الاصطلاحي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0047 — الحلقات والحقول، وقوع ١:**
  - **الأصل:** [السطر ١٥٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L155). الشاهد المسجل: «that $\alpha + \beta$, as defined, is indeed a \emph{cut}, for any».
  - **العربية المعيارية:** [السطر ١٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L158)؛ الطبعة الدولية: [ص ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=97) (ترقيم المتن: ٩٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=97) (ترقيم المتن: ٩٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «كما عُرّفت، \emph{قطع} بالفعل لأي قطعين $\alpha$ و$\beta$. وإليك برهان».
  - **العربية التراثية:** [السطر ١٢٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L120)؛ الطبعة التراثية: [ص ٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=93) (ترقيم المتن: ٩٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وقبل الشروع في \emph{ذلك} التمرين، نحقق أمورًا أقرب مأخذًا. فمنها أن $\alpha + \beta$ كما عرفناه \emph{قطع} حقًّا، متى كان $\alpha$ و$\beta$ قطعين. وبيانه الآتي.».
- **OLP-0047 — الحلقات والحقول، وقوع ٢:**
  - **الأصل:** [السطر ١٨٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/arithmetization/checking-details.tex#L182). الشاهد المسجل: «that this set is a \emph{cut}. Here is a proof of that fact:».
  - **العربية المعيارية:** [السطر ١٨٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/arithmetization/checking-details.tex#L189)؛ الطبعة الدولية: [ص ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=97) (ترقيم المتن: ٩٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=97) (ترقيم المتن: ٩٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نبين أن هذه المجموعة \emph{قطع}. وإليك برهان ذلك:».
  - **العربية التراثية:** [السطر ١٤٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/arithmetization/checking-details.tex#L142)؛ الطبعة التراثية: [ص ٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=93) (ترقيم المتن: ٩٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\Setabs{p \in \Rat}{p < 0 \text{ أو }p^2 < 2}$، ولا بد من إثبات أن هذه المجموعة \emph{قطع}.».

# بطاقات الدوال والعلاقات — القرارات ١٨٩–١٩٣

[الرجوع إلى مقدمة الدفعة](README.md)

## تطبيق

الأصل الإنجليزي: `application`. معرّف القرار: `retro-0005-0050:emphasis:99034ec1a13b1c71`.

**المعنى المقصود:** تطبيق العلاقة أو الدالة على مجموعة مدخلات هو مجموعة عناصر المخرج التي يصل إليها بعض تلك المدخلات.

**سبب الاختيار:** يعرّف الأصل تطبيق العلاقة R على A بمجموعة y التي تتصل بعنصر x من A، ثم تطبيق الدالة f على C بمجموعة f(x) حيث x من C؛ فاختيار «تطبيق» يجمع عمليتي أخذ الصورة من غير أن يجعل الدالة نفسها مساوية لعملية التطبيق. يطبع المعجم map وmapping «تطبيقًا» ولكنه لا يقدم في الصفحة المعاينة هذا الاستعمال العملياتي على مجموعة جزئية حرفيًا.

**سؤال مفتوح:** هل «تطبيق الدالة على C» يميز العملية من الدالة نفسها، أم ينبغي تسمية المجموعة «صورة C» مباشرة في الموضعين؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٨-٣٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L28-L33) — يعطي تطبيق العلاقة على المجموعة بصيغة وجود عنصر مدخل.؛ [الأسطر ٧٨-٩٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L78-L90) — يسمي مجموعة قيم الدالة على جزء من مجالها تطبيقًا وصورة.

**وجه جمع المواضع:** موضعا الأصل يحددان تطبيق العلاقة وتطبيق الدالة بصيغتي مجموعة نواتج مختلفتين متكافئتين في الحالة الدالية.

**مواضع المعجم المعاينة:** [ص ٤٤٤ من PDF (المطبوعة ٤٣٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=444)، [ص ٣٤٧ من PDF (المطبوعة ٣٣٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=347)

**حدود الشاهد المعجمي:** PDF ص ٤٤٤، المطبوعة ٤٣٢، يطبع map وmapping «تطبيقًا»؛ وص ٣٤٧، المطبوعة ٣٣٥، يطبع image «صورة». لا يطبع المدخلان عبارة تطبيق دالة على مجموعة جزئية.

**بديل جدير بالمقارنة:** صورة المجموعة؛ اسم النتيجة لا فعل التطبيق نفسه

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في صيغة الناتج، ومتوسطة في استعمال «تطبيق» اسمًا لهذه العملية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0019 — عمليات العلاقات، وقوع ١:**
  - **الأصل:** [السطر ٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L31). الشاهد المسجل: «The \emph{application} of $R$ to $A$ is $\funimage{R}{A} = \{y :».
  - **العربية المعيارية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/operations.tex#L31)؛ الطبعة الدولية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تطبيق} $R$ على $A$ هو $\funimage{R}{A} = \{y :».
  - **العربية التراثية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/operations.tex#L30)؛ الطبعة التراثية: [ص ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=49) (ترقيم المتن: ٤٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «و\emph{تطبيق} $R$ على $A$ معرّف بـ$\funimage{R}{A} = \{y :».
- **OLP-0023 — الدوال بوصفها علاقات، وقوع ٢:**
  - **الأصل:** [السطر ٨٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L87). الشاهد المسجل: «The \emph{application} of~$f$ to~$C$ is $\funimage{f}{C} =».
  - **العربية المعيارية:** [السطر ٨٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/functions-relations.tex#L86)؛ الطبعة الدولية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن \emph{تطبيق}~$f$ على~$C$ هو $\funimage{f}{C} =».
  - **العربية التراثية:** [السطر ٧٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/functions-relations.tex#L77)؛ الطبعة التراثية: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «و\emph{تطبيق}~$f$ على~$C$ تعريفه $\funimage{f}{C} =».

## رسم بياني

الأصل الإنجليزي: `graph`. معرّف القرار: `retro-0005-0050:emphasis:2c690313f4397617`.

**المعنى المقصود:** رسم الدالة التامة أو الجزئية هو علاقتها المكونة من الأزواج المرتبة للمدخلات المعرفة وقيمها، لا شبكة رؤوس وحواف.

**سبب الاختيار:** يستعمل الأصل graph في حد الدالة التامة وفي حد الجزئية، وكلتاهما علاقة جزئية من A×B تعطي الأزواج التي تحقق f(x)=y. أبقت العربيتان «رسم بياني» في الموضعين، لكن المعجم يطبع graph «بيانًا» ويعرض في المدخل نفسه معنى رسم الدالة بوصفه مجموعة أزواج؛ فينبغي تمييز هذا المعنى من بيان الرؤوس والحواف ولا ننسب اللفظ المنشور إلى رأس المدخل حرفيًا.

**سؤال مفتوح:** هل يكفي سياق الدالة للتمييز بين رسمها كمجموعة أزواج والبيان الشبكي، أم يفضل «منحنى الدالة» في بعض المواضع مع أنه قد يوهم تمثيلًا هندسيًا فقط؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٤-٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L24-L29) — يعرف رسم الدالة التامة مجموعة الأزواج المطابقة لقيمها.؛ [الأسطر ٥٠-٥٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L50-L55) — يعرف رسم الجزئية بالأزواج حيث تكون القيمة معرفة.

**وجه جمع المواضع:** حدا الأصل يربطان رسم الدالة بالعلاقة الثنائية في حالتي الدالة التامة والجزئية.

**مواضع المعجم المعاينة:** [ص ٢٩٩ من PDF (المطبوعة ٢٨٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=299)

**حدود الشاهد المعجمي:** PDF ص ٢٩٩، المطبوعة ٢٨٧، يسمي graph «بيانًا» ويعطي له أيضًا معنى مجموعة الأزواج المرتبة لدالة؛ واللفظ «رسم بياني» ليس رأس هذا المدخل.

**بديل جدير بالمقارنة:** بيان الدالة؛ أقرب إلى رأس المعجم لكنه قد يلتبس بالبيان الشبكي؛ منحنى الدالة؛ أضيق من علاقة الأزواج العامة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في معنى مجموعة الأزواج، ومتوسطة في اختيار اللفظ العربي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0026 — الدوال الجزئية، وقوع ١:**
  - **الأصل:** [السطر ٥١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/partial-functions.tex#L51). الشاهد المسجل: «Let $f\colon A \pto B$ be a partial function. The \emph{graph} of~$f$».
  - **العربية المعيارية:** [السطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/partial-functions.tex#L50)؛ الطبعة الدولية: [ص ٦١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=61) (ترقيم المتن: ٦٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=61) (ترقيم المتن: ٦٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لتكن $f\colon A \pto B$ دالة جزئية. إن \emph{الرسم البياني} لـ~$f$».
  - **العربية التراثية:** [السطر ٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/partial-functions.tex#L48)؛ الطبعة التراثية: [ص ٥٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=58) (ترقيم المتن: ٥٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «للدالة الجزئية $f\colon A \pto B$ \emph{رسم بياني} للدالة~$f$، وهو العلاقة».
- **OLP-0023 — الدوال بوصفها علاقات، وقوع ٢:**
  - **الأصل:** [السطر ٢٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L25). الشاهد المسجل: «The \emph{graph} of~$f$ is the relation $R_f \subseteq A \times B$».
  - **العربية المعيارية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/functions-relations.tex#L25)؛ الطبعة الدولية: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن \emph{الرسم البياني} للدالة~$f$ هو العلاقة $R_f \subseteq A \times B$».
  - **العربية التراثية:** [السطر ٢٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/functions-relations.tex#L23)؛ الطبعة التراثية: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «للدالة $f\colon A \to B$ \emph{رسم بياني} للدالة~$f$، وهو العلاقة».

## الرسم البياني لدالة؛ علاقة دالية

الأصل الإنجليزي: `graph of a function; functional relation`. معرّف القرار: `locale-ar-chosen-3ca23dad963d5841`.

**المعنى المقصود:** رسم الدالة هو علاقتها الثنائية بين المدخلات والقيم، والعلاقة الدالية هي التي تعطي لكل مدخل قيمة وحيدة مع شرط الوجود عند كل عنصر من المجال.

**سبب الاختيار:** يسمي الأصل رسم الدالة ثم يثبت في القضية أن العلاقة إذا كانت وحيدة المخرج لكل x وشاملة لكل x في A فهي رسم دالة تامة. حفظت الطبعات الفرق بين الرسم والعلاقة الدالية؛ لكن وصف «functional» وحده في كلام الأصل يحتاج قراءة القضية كاملة، لأنه قد يدل في سياقات أخرى على التفرد بلا كلية. مدخل graph المعجمي يصف الأزواج ولا يقرر شرط الكلية في هذه القضية.

**سؤال مفتوح:** هل عبارة «علاقة دالية» في الشرح توحي بالوجود لكل عنصر من A، أم يلزم ذكر شرطي التفرد والوجود صراحة كلما استعملت؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٤-٥٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L24-L50) — التعريف والقضية في الأصل يفرقان بين رسم الدالة وعلاقة لا تصير دالة تامة إلا بشرطي الوجود والتفرد.

**مواضع المعجم المعاينة:** [ص ٢٩٩ من PDF (المطبوعة ٢٨٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=299)، [ص ٢٧٦ من PDF (المطبوعة ٢٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=276)

**حدود الشاهد المعجمي:** PDF ص ٢٩٩ يذكر رسم الدالة مجموعة أزواج، وص ٢٧٦ يثبت للدالة تعيين قيمة واحدة لكل عنصر من مجالها؛ شرطا القضية التفصيليان من الأصل.

**بديل جدير بالمقارنة:** علاقة تعين قيمة وحيدة لكل مدخل؛ شرح أدق لكنه أطول من الاسم الاصطلاحي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في شرطي القضية، ومتوسطة في دلالة «دالية» منفردة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0023 — الدوال بوصفها علاقات، وقوع ١:**
  - **الأصل:** [السطر ٢٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L24). الشاهد المسجل: «\begin{defn}[Graph of a function] Let $f\colon A \to B$ be a function. The \emph{graph} of~$f$ is the relation $R_f \subseteq A \times B$ defined by \[ R_f = \Setabs{\tuple{x,y}}{f(x) = y}. \] \end{defn}».
  - **الأصل:** [السطر ٣٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L39). الشاهد المسجل: «Similarly, if a relation is ``functional'', then it is the graph of a function. \end{explain} \begin{prop}\ollabel{prop:graph-function} Let $R \subseteq A \times B$ be such that: \begin{enumerate} \item If $Rxy$ and $Rxz$ then $y = z$; and \item for every $…».
  - **العربية المعيارية:** [السطر ٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/functions-relations.tex#L24)؛ الطبعة الدولية: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}[الرسم البياني لدالة] لتكن $f\colon A \to B$ دالة. إن \emph{الرسم البياني} للدالة~$f$ هو العلاقة $R_f \subseteq A \times B$ المعرّفة بـ \[ R_f = \Setabs{\tuple{x,y}}{f(x) = y}. \] \end{defn}».
  - **العربية المعيارية:** [السطر ٣٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/functions-relations.tex#L39)؛ الطبعة الدولية: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=56) (ترقيم المتن: ٥٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وبالمثل، إذا كانت العلاقة «دالية»، فهي الرسم البياني لدالة. \end{explain} \begin{prop}\ollabel{prop:graph-function} لتكن $R \subseteq A \times B$ بحيث: \begin{enumerate} \item إذا كان $Rxy$ و$Rxz$ فإن $y = z$؛ و \item لكل $x \in A$ يوجد $y \in B$ بحيث $\tup…».

## معاملتها

الأصل الإنجليزي: `treat`. معرّف القرار: `retro-0005-0050:emphasis:5548578af0c7d7e8`.

**المعنى المقصود:** معاملة الدوال مجموعات أزواج اصطلاح تمثيلي نافع للحساب عليها، لا دعوى ميتافيزيقية عن حقيقة الدوال.

**سبب الاختيار:** ينفي الأصل صراحة أن تعريف الدوال بمجموعات الأزواج حكم في الماهية، ويطلب فقط أن نعاملها هكذا لسهولة إجراء عمليات العلاقات. اختارت التراثية «معاملتها» لفعل treat، محافظة على هذا التحفظ. مدخل graph المعجمي يسوغ التمثيل بالأزواج لكنه لا يثبت الدعوى الفلسفية أو ينفيها؛ فالعمدة هنا قيد الأصل.

**سؤال مفتوح:** هل تحفظ «معاملتها مجموعات معينة» الفرق بين الاصطلاح التمثيلي والدعوى الوجودية، أم تحتاج جملة التراثية إلى ضمير أو بيان أوضح؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٠-٧٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L60-L75) — الفقرة الأصلية تضع القيد الصريح على معنى المطابقة بين الدالة ومجموعة الأزواج.

**مواضع المعجم المعاينة:** [ص ٢٩٩ من PDF (المطبوعة ٢٨٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=299)

**حدود الشاهد المعجمي:** PDF ص ٢٩٩ يصف رسم الدالة مجموعة أزواج؛ لا يتناول هذا المدخل حد الادعاء الفلسفي، فيرجع فيه إلى عبارة الأصل.

**بديل جدير بالمقارنة:** نعدها مجموعات أزواج لأغراض العمل؛ أوضح من جهة القصد وقد يفقد الإيجاز التراثي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التحفظ الفكري، ومتوسطة في سلاسة العبارة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0023 — الدوال بوصفها علاقات، وقوع ١:**
  - **الأصل:** [السطر ٧١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L71). الشاهد المسجل: «functions, but an observation that it is convenient to \emph{treat}».
  - **العربية المعيارية:** [السطر ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/functions-relations.tex#L71)؛ الطبعة الدولية: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=56) (ترقيم المتن: ٥٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=56) (ترقيم المتن: ٥٥) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «ملاحظة مفادها أنه من الملائم \emph{معاملة} الدوال بوصفها مجموعات».
  - **العربية التراثية:** [السطر ٦٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/functions-relations.tex#L64)؛ الطبعة التراثية: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «بل إجازة نافعة لـ\emph{معاملتها} مجموعات معينة. ومن نفع ذلك أن }{}».

## صورة

الأصل الإنجليزي: `image`. معرّف القرار: `retro-0005-0050:emphasis:a06ee3b55f8ac6ac`.

**المعنى المقصود:** صورة المجموعة C تحت الدالة f هي مجموعة القيم f(x) لكل x في C، وتساوي مدى f إذا كانت C مجالها كله.

**سبب الاختيار:** يعرف الأصل تطبيق f على C ثم يسمي الناتج image of C، ويستنتج أن صورة المجال هي المدى. اختارت الطبعات «صورة» واحتفظت بعلاقة الجزئية C⊆A بدل جعل الصورة قيمة عنصر مفرد. يطبع المعجم image «صورة» ويفرق في الشرح صورة نقطة من صورة مجموعة، وهو شاهد مطابق لهذا الانتقال.

**سؤال مفتوح:** هل يحتاج تعريف صورة C إلى تمييز مرئي عن صورة عنصر مفرد في الفهرس الاصطلاحي، أم تكفي الصيغة المجموعة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧٨-٩٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L78-L94) — التعريف والنتيجة اللاحقة في الأصل يصلان صورة الجزء C بمدى الدالة عند اختيار المجال كله.

**مواضع المعجم المعاينة:** [ص ٣٤٧ من PDF (المطبوعة ٣٣٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=347)، [ص ٥٩١ من PDF (المطبوعة ٥٧٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=591)

**حدود الشاهد المعجمي:** PDF ص ٣٤٧، المطبوعة ٣٣٥، يطبع image «صورة» للعنصر وللمجموعة؛ وص ٥٩١، المطبوعة ٥٧٩، يطبع range «مدى» لمجموعة القيم.

**بديل جدير بالمقارنة:** مجموعة القيم على C؛ شرح صحيح لا اسم اصطلاحي موجز

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في المصطلح والصيغة والعلاقة بالمدى.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0023 — الدوال بوصفها علاقات، وقوع ١:**
  - **الأصل:** [السطر ٨٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/functions/functions-relations.tex#L88). الشاهد المسجل: «\Setabs{f(x)}{x \in C}$. We also call this the \emph{image} of~$C$».
  - **العربية المعيارية:** [السطر ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/functions/functions-relations.tex#L87)؛ الطبعة الدولية: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=57) (ترقيم المتن: ٥٦) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\Setabs{f(x)}{x \in C}$. ونسميه أيضًا \emph{صورة}~$C$».
  - **العربية التراثية:** [السطر ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/functions/functions-relations.tex#L78)؛ الطبعة التراثية: [ص ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=54) (ترقيم المتن: ٥٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\Setabs{f(x)}{x \in C}$؛ ويسمى أيضًا \emph{صورة}~$C$ تحت~$f$.».

# بطاقات الأشجار وعمليات العلاقات — القرارات ٣٥٨–٣٦٠

[الرجوع إلى مقدمة الدفعة](README.md)

## شجرة منتهية / الأشجار المنتهية

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `finite tree`. معرّف القرار: `REPAIR-0001-0100-finite-tree`.

**المعنى المقصود:** الشجرة المنتهية هي التي مجموعة عقدها منتهية، لا مجرد شجرة لكل عقدة فيها عدد منته من الأبناء.

**سبب الاختيار:** تعريف الأصل يميز finite tree من finitely branching، ويجعل الانتهاء صفة لمجموعة العقد كلها. تستعمل التراثية في موضع المثال «شجرة منتهية»، فيتعلق الوصف بالشجرة لا بنهايات الفروع؛ و«منتهيات الأشجار» كان سيحيل إلى الأجزاء الطرفية. المؤشر المجمد لم يربط موضعًا إنجليزيًا منفردًا لهذه البطاقة، لذا أضفنا رابط التعريف المثبت وموضعًا عربيًا محددًا من غير تغيير دعوى المؤشر.

**سؤال مفتوح:** هل «شجرة منتهية» و«منتهية التفرع» يميزان عدد العقد الكلي من عدد الخلف المباشر لكل عقدة؟

**الموضع الدقيق في النص العربي:** [الأسطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/trees.tex#L21) — هذا الشاهد المفرد الدقيق يرفع غموض وقوعَي الاسم في الملف دون محو تعذر المؤشر المجمد.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ٨٣-٨٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/trees.tex#L83-L88) — يعرف الأصل انتهاء الشجرة والتفرع المنتهي في موضعين متجاورين.

**وجه جمع المواضع:** استُخدم تعريف الأصل المثبت في سجل المراجعة المستقل، لا وقوعًا إنجليزيًا سجله المؤشر المجمد.

**حدود استدراك الشاهد:** لا يسجل المؤشر لهذا القرار وقوعًا إنجليزيًا دقيقًا، وسجل الشاهد المستقل هو الذي عين تعريف الأصل الأسطر ٨٣–٨٨؛ الرابط الإضافي قابل للتحقق ولا يحول الغياب إلى وقوع مسجل.

**نتيجة البحث المعجمي المحدود:** لم يظهر مدخل مطابق للتركيب finite tree في البحث المحدود للمعجم، مع وجود مداخل لأنواع أخرى من الأشجار؛ لذلك يسند تعريف الأصل التمييز ولا ندعي اعتمادًا اصطلاحيًا رسميًا للاسم.

**بديل جدير بالمقارنة:** منتهيات الأشجار؛ يوهم أجزاءها الطرفية؛ الأشجار المحدودة؛ لا يحدد نوع الحد

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الفرق الرياضي بين الانتهاء والتفرع المنتهي، ومتوسطة في تفضيل الصيغة العربية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0018 — الأشجار، وقوع ١:**
  - **العربية التراثية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/trees.tex)؛ الطبعة التراثية: [ص ٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=47) (ترقيم المتن: ٤٦) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».

## تقييد العلاقة على A؛ تطبيق العلاقة على A

الأصل الإنجليزي: `restriction of a relation to A; application of a relation to A`. معرّف القرار: `locale-ar-chosen-c909e0ca3b848fac`.

**المعنى المقصود:** تقييد العلاقة ر على أ هو ر∩أ²، أما تطبيقها على أ فهو مجموعة كل ص يرتبط به س من أ وفق ر.

**سبب الاختيار:** يضع الأصل عمليتين متتاليتين مختلفتين: تقاطع العلاقة مع مربع أ يقيد طرفي الزوج، وصورة أ تحت العلاقة تجمع الأطراف الثانية التي شاهدها عنصر من أ. أبقت الطبعة «تقييد» للأولى و«تطبيق» للثانية بدل دمجهما في عملية واحدة، مع المحافظة على الصيغتين الرسميتين. يشرح المعجم العلاقة الثنائية عمومًا لكنه لا يثبت بهذا المدخل اسم العمليتين المركبين.

**سؤال مفتوح:** هل «تطبيق العلاقة على أ» يميز صورة أ تحت ر من تقييد ر إلى أ²، أم أن «صورة أ بالعلاقة» أدق في الاستعمال؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٩-٣٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L19-L34) — التعريفان والصيغتان ر∩أ² و ر[أ] متجاوران في الأصل.

**مواضع المعجم المعاينة:** [ص ٧١ من PDF (المطبوعة ٥٩)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=71)

**حدود الشاهد المعجمي:** PDF ص ٧١ يعرّف العلاقة الثنائية جزئية من الجداء الديكارتي فقط؛ لا يشهد حرفيًا لاسم تقييد علاقة أو تطبيقها على مجموعة.

**بديل جدير بالمقارنة:** صورة أ تحت ر؛ أوضح للنتيجة لكنه يبتعد عن رأس application الذي اختاره سجل الطبعة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تمييز الصيغتين، ومتوسطة في اسم العملية الثانية.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0019 — عمليات العلاقات، وقوع ١:**
  - **الأصل:** [السطر ١٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L19). الشاهد المسجل: «\begin{defn}\ollabel{relationoperations} Let $R$, $S$ be relations, and $A$ be any set. The \emph{inverse} of $R$ is $R^{-1} = \Setabs{\tuple{y, x}}{\tuple{x, y} \in R}$. The \emph{relative product} of $R$ and $S$ is $(R \mid S) = \{\tuple{x, z} : \exists y…».
  - **العربية المعيارية:** [السطر ١٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/operations.tex#L19)؛ الطبعة الدولية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\begin{defn}\ollabel{relationoperations} لتكن $R$ و$S$ علاقتين، ولتكن $A$ أي مجموعة. \emph{معكوس العلاقة} $R$ هو $R^{-1} = \Setabs{\tuple{y, x}}{\tuple{x, y} \in R}$. \emph{الضرب النسبي} للعلاقتين $R$ و$S$ هو $(R \mid S) = \{\tuple{x, z} : \exists y(Rxy \la…».

## اتحاد

الأصل الإنجليزي: `union`. معرّف القرار: `retro-0005-0050:emphasis:66c41165fc503adf`.

**المعنى المقصود:** اتحاد مجموعتين أ وب هو مجموعة العناصر التي تنتمي إلى إحداهما؛ وينطبق على العلاقات لأنها مجموعات أزواج مرتبة.

**سبب الاختيار:** يرد لفظ union في الأصل مرة لاتحاد علاقتين ومرة لتعريف اتحاد المجموعتين أ وب بالرمز أ∪ب. أبقت التراثية «اتحاد» في السياقين لأن العلاقة نفسها مجموعة أزواج، فلا تتغير العملية. المعجم يطبع «اتحاد (اجتماع)» اسمًا أول ويعرّف جمع عناصر مجموعتين؛ فالاختيار يأخذ الرأس الأول من شاهد مباشر.

**سؤال مفتوح:** هل اتساق «اتحاد» بين المجموعات والعلاقات أنسب من «اجتماع» المعجمي البديل في هذين الموضعين؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٠-١٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L10-L15) — الاستعمال الأول لعلاقتين تعاملان كمجموعتين من الأزواج.؛ [الأسطر ٣٣-٣٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L33-L37) — الاستعمال الثاني تعريف مباشر لاتحاد مجموعتين.

**وجه جمع المواضع:** تطابق العملية عبر سياقي العلاقة والمجموعة هو سبب توحيد المصطلح.

**مواضع المعجم المعاينة:** [ص ٧٥٤ من PDF (المطبوعة ٧٤٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=754)

**حدود الشاهد المعجمي:** PDF ص ٧٥٤، المطبوعة ٧٤٢، يطبع union = «اتحاد (اجتماع)» ويشرح اتحاد مجموعتين وطرق تعميمه؛ شاهد مباشر للرأسين.

**بديل جدير بالمقارنة:** اجتماع؛ مرادف مذكور في المدخل نفسه ولم يختر هنا اتساقًا مع المصدر العربي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في هوية العملية والمصطلح المعجمي، ومتوسطة في تفضيل أحد المترادفين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0019 — عمليات العلاقات، وقوع ١:**
  - **الأصل:** [السطر ١٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/relations/operations.tex#L13). الشاهد المسجل: «\olref[sfr][rel][ord]{prop:stricttopartial}, we considered the \emph{union}».
  - **العربية المعيارية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/relations/operations.tex#L13)؛ الطبعة الدولية: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=50) (ترقيم المتن: ٤٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olref[sfr][rel][ord]{prop:stricttopartial}، نظرنا في \emph{اتحاد}».
  - **العربية التراثية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/relations/operations.tex#L13)؛ الطبعة التراثية: [ص ٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=48) (ترقيم المتن: ٤٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olref[sfr][rel][ord]{prop:stricttopartial} أخذنا \emph{اتحاد} علاقتين،».
- **OLP-0008 — الاتحادات والتقاطعات، وقوع ٢:**
  - **الأصل:** [السطر ٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/unions-and-intersections.tex#L35). الشاهد المسجل: «The \emph{union} of two sets $A$ and $B$, written $A \cup B$, is the».
  - **العربية المعيارية:** [السطر ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/unions-and-intersections.tex#L34)؛ الطبعة الدولية: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=34) (ترقيم المتن: ٣٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{اتحاد} مجموعتين $A$ و$B$، ويكتب $A \cup B$، هو مجموعة».
  - **العربية التراثية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/unions-and-intersections.tex#L31)؛ الطبعة التراثية: [ص ٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=33) (ترقيم المتن: ٣٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{اتحاد} $A$ و$B$، ورمزه $A \cup B$، مجموعة الأشياء التي هي من !!{element}s $A$ أو $B$».

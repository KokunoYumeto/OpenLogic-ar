# بطاقات المواضع والدوال — القرارات ٦٩٢–٦٩٣

[الرجوع إلى مقدمة الدفعة](README.md)

## عملية n-موضعية

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `n-ary operation`. معرّف القرار: `TERM-N-ARY`.

**المعنى المقصود:** عملية أو رمز يقبل n مواضع إدخال مرتبة، حيث n عدد محدد أو متغير من الأعداد الطبيعية.

**سبب الاختيار:** «n-موضعية» تحافظ على عدد الحجج ولا تخلطه بدرجة الدالة أو عدد نتائجها. مهم: الأصل المسمّر يعرّف الإغلاق تحت دالة أحادية f(x)، بينما عممت الطبعة العربية التعريف إلى n مدخلات؛ هذا توسيع تحريري صحيح شكليًا إن تحققت شروط التعريف، وليس ترجمة حرفية، ويحتاج قرار تحرير موثقًا.

**سؤال مفتوح:** هل يوافق الفريق على تعميم تعريف الإغلاق من الدالة الأحادية في الأصل إلى الدالة n-موضعية في الطبعات العربية، وهل «نونية» أوجز اصطلاحًا؟

**شواهد عربية دقيقة مستعادة استدراكًا:** الطبعة التراثية: [الأسطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L26) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ٢٧-٢٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L27-L29) — شاهد سياق فقط: الأصل يعرّف حالة الدالة الأحادية، والطبعة توسعها إلى n مدخلات.

**وجه جمع المواضع:** الأصل عند هذا الموضع يعرّف الإغلاق للدالة الأحادية فقط؛ تُعرض الأسطر لإظهار حد الشاهد لا لإثبات ورود n-ary فيه.

**حدود استدراك الشاهد:** المؤشر المجمّد لا يسجّل وقوعًا إنجليزيًا دقيقًا لهذا القرار؛ استعيد سياق وحدته من أصل مثبت لا على أنه موضع معجمي حرفي لكل أجزاء الرأس المركب.

**مواضع المعجم المعاينة:** [ص ٤٧٦ من PDF (المطبوعة ٤٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=476)

**حدود الشاهد المعجمي:** PDF ص ٤٧٦، المطبوعة ٤٦٤، يطبع n-ary composition «تركيب نوني» ويعطي n عنصرًا مدخلًا؛ ليس رأسًا لكل عملية n-موضعية.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0718 — في الاستقراء، وقوع ١:**
  - **العربية التراثية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L26)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لتكن $f$ دالة $n$-موضعية. ونقول إن المجموعة $S$ \emph{مغلقة} تحت $f$ إذا وفقط إذا كان $f(x_1,\dots,x_n) \in S$ كلما كانت $x_1,\dots,x_n \in S$ وكانت $f$ معرفة عند هذه المدخلات.».
- **OLP-0718 — في الاستقراء، وقوع ٢:**
  - **العربية التراثية:** [السطر ٣٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L39)؛ الطبعة التراثية: [ص ١١٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1138) (ترقيم المتن: ١٣٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «نقول إن الخاصية $P$ \emph{محفوظة تحت} الدالة $n$-موضعية $f$ إذا كان، لكل مدخلات $a_1,\dots,a_n$ من مجال $f$، صدق $P(a_1),\dots,P(a_n)$ مستلزمًا لصدق $P(f(a_1,\dots,a_n))$.».

## دالة ذات n مواضع؛ محمول ذو n مواضع

الأصل الإنجليزي: `n-place function; n-place predicate`. معرّف القرار: `owner-followup-OWNER_FOLLOWUP_REPAIRS_20260905:C185-01`.

**المعنى المقصود:** تمييز دالة n-موضعية من محمول n-موضعي في لغة منطقية.

**سبب الاختيار:** كلاهما يأخذ n مدخلات، لكن الدالة تعطي عنصرًا من المجال والمحمول يقرر علاقة صدق؛ لا يجوز تغيير نوع الرمز عند توحيد الصياغة.

**سؤال مفتوح:** هل يظهر الفرق في التعريف وفي جميع الأمثلة عند نقل n-ary function وn-ary predicate؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/model-theory/basics/substructures.tex#L32) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**مواضع المعجم المعاينة:** [ص ٤٧٦ من PDF (المطبوعة ٤٦٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=476)

**حدود الشاهد المعجمي:** PDF ص ٤٧٦ يوضح n مدخلات لتركيب عام ولا يحدد فرق الدالة والمحمول المنطقي.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0185 — الstructures الجزئية، وقوع ١:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/model-theory/basics/substructures.tex#L32). الشاهد المسجل: «\item For each $n$-place !!{predicate} $R \in \Lang L$, $\langle».
  - **العربية المعيارية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/model-theory/basics/substructures.tex#L29)؛ الطبعة الدولية: [ص ٣٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=396) (ترقيم المتن: ٣٩٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=396) (ترقيم المتن: ٣٩٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item لكل !!{function}~$f \in \Lang L$ ذات $n$ مواضع،».
  - **العربية المعيارية:** [السطر ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/model-theory/basics/substructures.tex#L32)؛ الطبعة الدولية: [ص ٣٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=396) (ترقيم المتن: ٣٩٥) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=396) (ترقيم المتن: ٣٩٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item لكل !!{predicate}~$R \in \Lang L$ ذي $n$ مواضع، تكون $\langle».
  - **العربية التراثية:** [السطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/model-theory/basics/substructures.tex#L29)؛ الطبعة التراثية: [ص ٣٨٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=386) (ترقيم المتن: ٣٨٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item لكل !!{function}~$f \in \Lang L$ ذات $n$ مواضع،».
  - **العربية التراثية:** [السطر ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/model-theory/basics/substructures.tex#L32)؛ الطبعة التراثية: [ص ٣٨٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=386) (ترقيم المتن: ٣٨٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item لكل !!{predicate}~$R \in \Lang L$ ذي $n$ مواضع، تكون $\langle».

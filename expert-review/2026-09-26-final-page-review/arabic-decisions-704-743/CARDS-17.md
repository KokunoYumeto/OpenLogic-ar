# بطاقات الاختيارات 736–737 — القرارات ٧٣٦–٧٣٧

[الرجوع إلى مقدمة الدفعة](README.md)

## موضع الاختزال؛ ناتج التقلّص؛ تقلّص؛ اختزال

الأصل الإنجليزي: `redex / contractum / contraction / reduction`. معرّف القرار: `TERM-BETA-REDUCTION-FAMILY`.

**المعنى المقصود:** موضع β قابل للاختزال، ونتيجة خطوة تقلصه، والخطوة نفسها في حساب لامبدا.

**سبب الاختيار:** «اختزال» اسم العلاقة أو العملية، و«تقلص» الخطوة، و«الناتج» الحد بعد الاستبدال؛ لا يمكن مبادلتها دون تغيير اتجاه السهم أو عدد الخطوات.

**سؤال مفتوح:** هل استقرت أسماء redex وreduct وcontraction في الرسوم والنص، وهل تنفذ إحلالًا متجنبًا لأسر المتغيرات؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/syntax/beta.tex#L17) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.؛ [الأسطر ٢٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/introduction/reduction.tex#L28) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0365 — اختزال β، وقوع ١:**
  - **الأصل:** [الملف](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/syntax/beta.tex)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [الملف](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/syntax/beta.tex)؛ الطبعة الدولية: [ص ٦٤٧](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=647) (ترقيم المتن: ٦٤٦) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٦٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=648) (ترقيم المتن: ٦٤٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية التراثية:** [السطر ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/syntax/beta.tex#L87)؛ الطبعة التراثية: [ص ٦٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=632) (ترقيم المتن: ٦٣١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وهي تقلّص دائمًا موضع الاختزال \emph{الأبعد إلى اليسار}،».
- **OLP-0345 — اختزال حدود لامبدا، وقوع ٢:**
  - **الأصل:** [السطر ٢٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/introduction/reduction.tex#L28). الشاهد المسجل: «\emph{$\beta$-contraction}. $(\lambd[x][M])N$ is called a \emph{redex} and $\Subst{M}{N}{x}$ its \emph{contractum}. Generally, if it is».
  - **العربية المعيارية:** [السطر ٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/introduction/reduction.tex#L26)؛ الطبعة الدولية: [ص ٦٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=625) (ترقيم المتن: ٦٢٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=626) (ترقيم المتن: ٦٢٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وتسمى عملية استبدال الحد الأول بالثاني \emph{تقلّص~$\beta$}.».
  - **العربية التراثية:** [السطر ٢٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/introduction/reduction.tex#L27)؛ الطبعة التراثية: [ص ٦٠٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=609) (ترقيم المتن: ٦٠٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «الفهم الحدسي؛ وإحلال الثاني محل الأول يسمى \emph{تقلّص~$\beta$}. الأول~$(\lambd[x][M])N$ هو \emph{موضع الاختزال}، والثاني~$\Subst{M}{N}{x}$ هو \emph{ناتج التقلّص}. وبوجه عام، إذا تحول الحد~$P$ إلى~$P'$ بتقلّص~$\beta$ في أحد حدوده الجزئية، قلنا إن~$P$ \emph{…».

## ردكس / مختزَل / التلاقي / خاصية تشيرش--روسر

مصطلح الأصل بشاهد إضافي مستعاد (لا يسجّل المؤشر وقوعه الإنجليزي): `redex / reduct(um) / confluence / Church-Rosser`. معرّف القرار: `compact:T-REDEX-REDUCT-CONFLUENCE`.

**المعنى المقصود:** حد قابل للاختزال ونتيجته، مع خاصية التلاقي لمساري اختزال من حد واحد في حساب لامبدا.

**سبب الاختيار:** «ردكس» نقل اسم موضع الاختزال، و«مختزل» قد يعني الفاعل أو الناتج؛ خاصية تشيرش–روسر تقول بإمكان الوصول إلى حد مشترك، لا مساواة الخطوتين فورًا.

**سؤال مفتوح:** هل اسم الناتج العربي غير ملتبس، وهل تُرسم جهة السهمين والحد المشترك بوضوح؟

**شواهد عربية دقيقة مستعادة استدراكًا:** الطبعة التراثية: [الأسطر ١٧٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L170) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.؛ الطبعة التراثية: [الأسطر ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/reduction.tex#L54) — شاهد من الوحدة العربية يحدّد سياق القرار؛ المطابقة اللفظية لكل أجزاء الرأس غير مفترضة.

**شاهد الأصل الإنجليزي المستعاد استدراكًا:** [الأسطر ١٨٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/propositions-as-types/normalization.tex#L185) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.؛ [الأسطر ٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/propositions-as-types/reduction.tex#L3) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**حدود استدراك الشاهد:** المؤشر المجمّد لا يسجّل وقوعًا إنجليزيًا دقيقًا لهذا القرار؛ استعيد سياق وحدته من أصل مثبت لا على أنه موضع معجمي حرفي لكل أجزاء الرأس المركب.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0687 — في التطبيع، وقوع ١:**
  - **العربية التراثية:** [السطر ٢٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L27)؛ الطبعة التراثية: [ص ١٠٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1091) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ويقاس تعقيد الردكس~$M$ بـ\emph{رتبة القطع}~$\cutrank{M}$:».
  - **العربية التراثية:** [السطر ٣٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L38)؛ الطبعة التراثية: [ص ١٠٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1091) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ويقاس تعقيد حد البرهان بأعلى رتبة لردكس فيه، وبالصفر إذا كان عاديًا:».
  - **العربية التراثية:** [السطر ٤١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L41)؛ الطبعة التراثية: [ص ١٠٩١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1091) (ترقيم المتن: ٩٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\text{ وهو ردكس}\}\cup\{0\}\bigr).».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
  - **العربية التراثية:** [السطر ١٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/normalization.tex#L193)؛ الطبعة التراثية: [ص ١٠٩٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1094) (ترقيم المتن: ٩٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وجود مختزَل مشترك.».
- **OLP-0691 — في الاختزال، وقوع ٢:**
  - **العربية التراثية:** [السطر ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/reduction.tex#L53)؛ الطبعة التراثية: [ص ١٠٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1099) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «يسمى الحد الواقع على يسار~$\redone$ \emph{ردكسًا}، والحد الواقع على يمينه».
  - **العربية التراثية:** [السطر ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/reduction.tex#L54)؛ الطبعة التراثية: [ص ١٠٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1099) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{مختزَلًا}. وعلى خلاف حساب لامبدا غير المنمّط، حيث لا يعد ردكسًا إلا».
  - **العربية التراثية:** [السطر ٥٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/proof-theory/propositions-as-types/reduction.tex#L57)؛ الطبعة التراثية: [ص ١٠٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=1099) (ترقيم المتن: ٩٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$\dcase{N}{x_1}{M_1}{x_2}{M_2}$ و$\abort{!A}{N}$، مع الردكسات المقابلة.».

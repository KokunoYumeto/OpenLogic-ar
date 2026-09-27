# بطاقات المصفوفة والقيم — القرارات ٦٧٤–٦٧٥

[الرجوع إلى مقدمة الدفعة](README.md)

## مصفوفة؛ قيم الصدق المميزة

الأصل الإنجليزي: `logical matrix; designated truth values`. معرّف القرار: `ar-classical-0351-0400-logical-matrix-designated`.

**المعنى المقصود:** مصفوفة منطقية تحدد العمليات على القيم وأي القيم معدودة مميزة لحفظ اللزوم.

**سبب الاختيار:** فصلت اسم البنية عن وصف قيم الصدق؛ «مميزة» لا تعني قيمة وحيدة، وقد تكون مجموعة منها، فيؤثر ذلك في تعريف الاستنتاج.

**سؤال مفتوح:** هل صيغة الجمع للقيم المميزة ظاهرة، وهل تميّز الطبعة المعنى المنطقي للمصفوفة من الجبري؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/syntax-and-semantics/matrices.tex#L14) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0388 — المصفوفات، وقوع ١:**
  - **الأصل:** [الملف](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/syntax-and-semantics/matrices.tex)؛ ⚠ لم يثبت السطر الحالي لهذا الاختيار؛ لا تُعامل أرقام المرشحات القديمة إحالة دقيقة. الشاهد المسجل: «».
  - **العربية المعيارية:** [السطر ١٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/many-valued-logic/syntax-and-semantics/matrices.tex#L15)؛ الطبعة الدولية: [ص ٦٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=678) (ترقيم المتن: ٦٧٧) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٦٧٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=679) (ترقيم المتن: ٦٧٨) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emph{مصفوفة}.».
  - **العربية التراثية:** [السطر ١٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/many-valued-logic/syntax-and-semantics/matrices.tex#L15)؛ الطبعة التراثية: [ص ٦٦٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=662) (ترقيم المتن: ٦٦١) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «هذه الأمور يسمى \emph{مصفوفة}.».

## تحتوي A وحدها في كل موضع يقابل قيمة صدق مميّزة في 𝐋، وتخلو سائر المواضع. ونكتب

الأصل الإنجليزي: `Make the empty undesignated positions explicit in the theorem sequent.`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0404-THEOREM-EMPTY-SLOTS-20260907`.

**المعنى المقصود:** مواضع معينة في متتالية أو مصفوفة تحمل A إذا قابلت قيمة مميزة، وتبقى المواضع الأخرى خالية.

**سبب الاختيار:** إضافة «وحدها» و«تخلو» تصون القيدين المتقابلين وتمنع قراءة توحي بأن بقية المواضع تحمل حكمًا آخر. هذه مراجعة صياغة حكم رياضي لا اصطلاح منفرد.

**سؤال مفتوح:** هل تقابل المواضع غير المميزة الخانات الفارغة حرفيًا، أم ينبغي تسمية قيمة أخرى وفق الأصل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٧-٤٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex#L47-L48) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0404 — القواعد والDerivations، وقوع ١:**
  - **الأصل:** [السطر ٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex#L47). الشاهد المسجل: «of the $n$-sequent containing $!A$ in each position corresponding to a designated truth value of~$\Log{L}$. We write $\Proves[\Log{L}]».
  - **العربية التراثية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex#L46)؛ الطبعة التراثية: [ص ٦٨٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=683) (ترقيم المتن: ٦٨٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «تحتوي~$!A$ وحدها في كل موضع يقابل قيمة صدق مميّزة في~$\Log{L}$، وتخلو سائر المواضع. ونكتب».
- **OLP-0404 — القواعد والDerivations، وقوع ٢:**
  - **الأصل:** [السطر ٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex#L47). الشاهد المسجل: «of the $n$-sequent containing $!A$ in each position corresponding to a designated truth value of~$\Log{L}$. We write $\Proves[\Log{L}]».
  - **العربية المعيارية:** [السطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/many-valued-logic/sequent-calculus/rules-and-proofs.tex#L46)؛ الطبعة الدولية: [ص ٦٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=699) (ترقيم المتن: ٦٩٨) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٧٠٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=700) (ترقيم المتن: ٦٩٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «تحتوي~$!A$ وحدها في كل موضع يقابل قيمة صدق مميّزة في~$\Log{L}$، وتخلو سائر المواضع. ونكتب».

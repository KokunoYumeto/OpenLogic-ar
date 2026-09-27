# بطاقات الاختيارات 718–719 — القرارات ٧١٨–٧١٩

[الرجوع إلى مقدمة الدفعة](README.md)

## مجموعة أولية من الصيغ

الأصل الإنجليزي: `prime set of formulas`. معرّف القرار: `TERM-PRIME-SET-INTUITIONISTIC`.

**المعنى المقصود:** مجموعة صيغ مغلقة استنتاجيًا تحقق شرط الأولية للفصل في بناء نموذج حدسي.

**سبب الاختيار:** «أولية» هنا ليست كون عدد أوليًا؛ إذا كان A∨B في المجموعة لزم وقوع أحد الطرفين فيها بحسب التعريف، وهو ما يحتاجه شاهد الصدق في النموذج.

**سؤال مفتوح:** هل يرد شرط الفصل صريحًا، وهل يفرق النص المجموعة الأولية من المجموعة المتسقة القصوى؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/intuitionistic-logic/soundness-completeness/lindenbaum.tex#L32) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0506 — لمّة ليندنباوم، وقوع ١:**
  - **الأصل:** [السطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/intuitionistic-logic/soundness-completeness/lindenbaum.tex#L32). الشاهد المسجل: «a prime set of formulas:».
  - **العربية المعيارية:** [السطر ٣٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/intuitionistic-logic/soundness-completeness/lindenbaum.tex#L34)؛ الطبعة الدولية: [ص ٨٤٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=840) (ترقيم المتن: ٨٣٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٨٤١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=841) (ترقيم المتن: ٨٤٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «تكون مجموعة ال!!{formula}s~$\Gamma$ \emph{أولية} إذا وفقط إذا:».
  - **العربية التراثية:** [السطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/intuitionistic-logic/soundness-completeness/lindenbaum.tex#L30)؛ الطبعة التراثية: [ص ٨٢٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=826) (ترقيم المتن: ٨٢٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «ونأخذ عوضًا عن المجموعة الكاملة~$\Gamma^*$ مجموعةً أولية من الصيغ، بالمعنى الذي نحدّه الآن. \begin{defn}\ollabel{defn:prime} مجموعة ال!!{formula}s~$\Gamma$ \emph{أولية} إذا وفقط إذا اجتمعت لها الشروط الآتية:».

## دالة عودية بدائية

الأصل الإنجليزي: `primitive recursive function`. معرّف القرار: `ar-classical-0351-0400-primitive-recursive`.

**المعنى المقصود:** دالة تبنى من دوال الأساس بالتركيب والعودية البدائية المحددة، دون التصغير غير المحدود.

**سبب الاختيار:** «بدائية» اسم لصنف مضبوط من الدوال ولا يعني الدالة البسيطة في الاستعمال العام؛ الفصل من الجزئية مهم لأن الدوال العودية البدائية كلية.

**سؤال مفتوح:** هل يشرح النص مولدات الصنف وشموله الكلي وفرقَه من العودية الجزئية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٤٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/lambda-definability/primitive-recursive-functions.tex#L142) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0378 — الدوال العودية البدائية lambd-Definable، وقوع ١:**
  - **الأصل:** [السطر ١٤٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/lambda-definability/primitive-recursive-functions.tex#L142). الشاهد المسجل: «Every primitive recursive function is !!{lambda definable}.».
  - **العربية المعيارية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/lambda-definability/primitive-recursive-functions.tex#L10)؛ الطبعة الدولية: [ص ٦٦٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=665) (ترقيم المتن: ٦٦٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٦٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=666) (ترقيم المتن: ٦٦٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الدوال العودية البدائية \usetoken{S}{lambda definable}}».
  - **العربية التراثية:** [السطر ١٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/lambda-definability/primitive-recursive-functions.tex#L10)؛ الطبعة التراثية: [ص ٦٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=649) (ترقيم المتن: ٦٤٨) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\olsection{الدوال العودية البدائية \usetoken{S}{lambda definable}}».

# بطاقات التكرار ونطاق الامتدادية — القرارات ٣٠٢–٣٠٣

[الرجوع إلى مقدمة الدفعة](README.md)

## المرات

الأصل الإنجليزي: `many times`. معرّف القرار: `retro-0005-0050:emphasis:cf27957d400376cd`.

**المعنى المقصود:** تكرار ذكر العنصر الواحد في كتابة المجموعة لا يزيد عدد عناصرها المختلفة.

**سبب الاختيار:** حوّلت التراثية many times إلى «عدد المرات التي نعد فيها عناصرها» في توازٍ مع التعيين والترتيب. المثال {a,a,b}={a,b} يبيّن أن المقصود تكرار السرد لا جمع نسخ جديدة من العنصر؛ فجاء جمع «المرات» طبيعيًا بعد «عدد».

**سؤال مفتوح:** هل «نعد فيها عناصرها» قد توهم حساب عناصر متعددة بدل تكرار ذكر العنصر، أم المثال اللاحق كاف؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢١-٢٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L21-L22) — الوجه الثالث الذي لا يغيّر المجموعة، ويفسره المثال الرمزي التالي.

**انطباق المعجم الرياضي:** اختيار لفظ «المرات» لتكرار السرد مسألة بيان جملة لا اسم مصطلح؛ المساواة الرمزية في الأصل هي الدليل.

**بديل جدير بالمقارنة:** عدد مرات ذكر العنصر؛ يرفع اللبس لكنه يقطع التوازي النحوي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الدلالة، متوسطة في وضوح العبارة لمن يقرأها قبل المثال.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0005 — الامتدادية وعناصر المجموعات، وقوع ١:**
  - **الأصل:** [السطر ٢١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L21). الشاهد المسجل: «\emph{order} its !!{element}s, or indeed how \emph{many times} we».
  - **العربية المعيارية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/basics.tex#L21)؛ الطبعة الدولية: [ص ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=30) (ترقيم المتن: ٢٩) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=30) (ترقيم المتن: ٢٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{نرتب} !!{element}sها، ولا حتى كم \emph{مرة} نعدّ».
  - **العربية التراثية:** [السطر ٢١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/basics.tex#L21)؛ الطبعة التراثية: [ص ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=30) (ترقيم المتن: ٢٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{المرات} التي نعد فيها !!{element}sها. ويضبط هذا المعنى المبدأ الآتي.».

## إذا وُجدت مجموعة

الأصل الإنجليزي: `extensionality`. معرّف القرار: `semantic-propagation-20260906:0005-P1`.

**المعنى المقصود:** مبدأ الامتدادية يثبت أن مجموعتين لهما العناصر نفسها متساويتان، ومنه وحدانية المجموعة المعينة بخاصية إن وُجدت؛ ولا يثبت وجودها لكل خاصية.

**سبب الاختيار:** يقول الأصل الإنجليزي في نهاية المثال إن الامتدادية تضمن دائمًا وجود مجموعة واحدة لكل خاصية، وفيه خلط بين الوجود والوحدة. النصان العربيان الحاضران يصححان النطاق: المعاصرة تشترط صراحة «إذا وُجدت مجموعة» وتختم بأن المبدأ لا يثبت الوجود وحده؛ والتراثية تقول «إذا عُيّنت مجموعة» قبل حكم الوحدة. تحفظ البطاقة هذا التصحيح الرياضي للطبعتين ولا تنسب إلى المعجم إثبات مسلمة وجود مفقودة.

**سؤال مفتوح:** هل يبرز شرط الوجود بما يكفي في النصين، ولا سيما التراثي، بحيث لا يفهم القارئ أن كل خاصية تنشئ مجموعة بمجرد الامتدادية؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٧-٨٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L87-L88) — الموضع الذي يوهم ثبوت الوجود لكل خاصية من الامتدادية وحدها.؛ [الأسطر ٨٩-٩٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L89-L90) — الموضع اللاحق الذي يقصر التصحيح العربي على الوحدة في التسمية.

**وجه جمع المواضع:** قرئت الجملتان المتتاليتان مع تعريف الامتدادية السابق ومع الشرط الصريح في الطبعتين العربيتين.

**مواضع المعجم المعاينة:** [ص ٢١٤ من PDF (المطبوعة ٢٠٢)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=214)

**حدود الشاهد المعجمي:** PDF ص ٢١٤ يشرح علاقة انتماء العنصر إلى المجموعة؛ لا يثبت وجود مجموعة لكل محمول. الفصل المنطقي بين مسلمة وجود ومبدأ مساواة المجموعات مأخوذ من تعريف الامتدادية نفسه وسياق الأصل.

**بديل جدير بالمقارنة:** توجد دائمًا مجموعة واحدة؛ مرفوضة لأن الامتدادية لا تعطي الوجود؛ على الأكثر مجموعة واحدة؛ أدق منطقيًا لكنه يحتاج بيان شرط الوجود عند تقديم رمز التعيين

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التصحيح الرياضي، متوسطة في مقدار التصريح المطلوب في الأسلوب التراثي.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0005 — الامتدادية وعناصر المجموعات، وقوع ١:**
  - **الأصل:** [السطر ٨٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L87). الشاهد المسجل: «And, more generally, extensionality guarantees that there is always».
  - **الأصل:** [السطر ٨٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/basics.tex#L89). الشاهد المسجل: «So, extensionality justifies calling».
  - **العربية المعيارية:** [السطر ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/sets/basics.tex#L87)؛ الطبعة الدولية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «وعلى نحو أعم، إذا وُجدت مجموعة تضم جميع قيم $x$ التي تحقق $\phi(x)$».
  - **العربية التراثية:** [السطر ٧٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/sets/basics.tex#L78)؛ الطبعة التراثية: [ص ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=31) (ترقيم المتن: ٣٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$x$ بالخاصية $\phi(x)$، قضت الامتدادية بوحدتها. ولهذا يصح أن نسمي».

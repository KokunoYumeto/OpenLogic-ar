# بطاقات حد التعداد واستعماله — القرارات ٢١٥–٢١٩

[الرجوع إلى مقدمة الدفعة](README.md)

## القائمة الخالية تعدّد المجموعة الخالية؛ والتعداد الرسمي لغير الخالية دالة شاملة مجالها PosInt

الأصل الإنجليزي: `enumeration of the empty set versus surjection from PosInt`. معرّف القرار: `locale-ar-chosen-1ad51ac8d8532bf2`.

**المعنى المقصود:** القائمة الخالية تعدد المجموعة الخالية في المعنى غير الرسمي؛ أما التعداد الرسمي بدالة شاملة من الموجبات فيخص المجموعة غير الخالية.

**سبب الاختيار:** يسجل الأصل القائمة الخالية صراحة مثالًا لتعداد الخالية، ثم يقيد تعريف الدالة الشاملة بشرط A غير خالية، ويعرف قابلية التعداد بأنها الخلو أو وجود تعداد. من مجموعة موجبات غير خالية لا توجد دالة إلى الخالية، فلا يجوز حذف الاستثناء عند صوغ الحد. يذكر المعجم في مدخل المجموعة العدودة المجموعات المنتهية ضمن الفئة، لكنه لا يقرر في الصفحة المعاينة اصطلاح القائمة الخالية؛ فالعمدة هنا تمييز الأصل نفسه.

**سؤال مفتوح:** هل يفهم القارئ من متن التعريفين الفرق بين القائمة الخالية وبين الدالة الشاملة ذات المجال غير الخالي، أم يحتاج الإحالة إلى الاستثناء عند تكرار لفظ التعداد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٦٤-١١٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L64-L116) — يجمع المدى المختار مثال القائمة الخالية والتعريف الرسمي المقيد بغير الخالية وحد قابلية التعداد الذي يستثني الخالية.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يدخل المجموعات المنتهية في معنى countable set، لكنه لا يشرح القائمة الخالية أو دالة من الموجبات إلى الخالية في المدخل المعاين.

**بديل جدير بالمقارنة:** جعل الخالية دالة شاملة من الموجبات؛ مرفوض رياضيًا لعدم وجود أي دالة من مجال غير خال إليها

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في استثناء الخالية واتساق الحدين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0029 — التعداد والمجموعات القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٦٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L64). الشاهد المسجل: «\item The empty set is enumerable: it is enumerated by the empty list!{}».
  - **الأصل:** [السطر ٢٦٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L268). الشاهد المسجل: «\begin{prob} According to \olref[sfr][siz][enm]{defn:enumerable}, a set $A$ is enumerable iff $A = \emptyset$ or there is !!a{surjective} $f\colon \PosInt \to A$. It is also possible to define ``!!{enumerable} set'' precisely by: a set is enumerable iff the…».
  - **العربية المعيارية:** [السطر ٦٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/enumerability.tex#L62)؛ الطبعة الدولية: [ص ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=63) (ترقيم المتن: ٦٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=63) (ترقيم المتن: ٦٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item المجموعة الخالية قابلة للتعداد: إذ تعدّدها القائمة الخالية!{}».
  - **العربية المعيارية:** [السطر ٢٧٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/enumerability.tex#L272)؛ الطبعة الدولية: [ص ٦٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=62) (ترقيم المتن: ٦١) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة)؛ طبعة المشرق: [ص ٦٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=62) (ترقيم المتن: ٦١) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\begin{prob} بحسب \olref[sfr][siz][enm]{defn:enumerable}، تكون المجموعة $A$ قابلة للتعداد إذا وفقط إذا كان $A = \emptyset$ أو وجدت دالة !!a{surjective} $f\colon \PosInt \to A$. ومن الممكن أيضًا أن نعرّف «مجموعة !!{enumerable}» تعريفًا دقيقًا كما يأتي: تكون…».

## معتبران

الأصل الإنجليزي: `do`. معرّف القرار: `retro-0005-0050:emphasis:666633a1c0498a8e`.

**المعنى المقصود:** ترتيب العناصر وتكرارها لا يغيران المجموعة المعدودة لكنهما معتبران عند تعيين تعداد بعينه.

**سبب الاختيار:** تؤكد do المبرزة في الأصل مقابلة الجملة السابقة التي تجيز التعدادات المكررة؛ فالمراد أن ترتيب القائمة والتكرار يهمان في هوية القائمة المحددة، لا في مجرد المجموعة التي تشملها. اختارت التراثية «معتبران» لتؤدي هذا القيد بإيجاز، مع مراعاة المثنى في ترتيب وتكرار. مدخل المجموعة العدودة في المعجم يعنى بوجود التقابل لا بهوية قائمة معينة؛ لذلك لا يسند هذه الدقة الأسلوبية مباشرة.

**سؤال مفتوح:** هل «معتبران» تحمل قوة التأكيد المقصودة في do من غير أن توهم أن التكرار شرط لصحة التعداد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٨-٥٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L48-L54) — تعاقب المثال الخاص بالقوائم المكررة مع الجملة المؤكدة يحدد نطاق معنى do.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يعرف المعدودية من جهة وجود تقابل ولا يناقش ترتيب قائمة بعينها أو تأكيد do؛ الدليل على هذا التفريق هو سياق الأصل.

**بديل جدير بالمقارنة:** مهمان؛ أضعف في تقييد هوية التعداد؛ لا بد من مراعاتهما؛ قد يوهم اشتراط ترتيب خاص

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الفرق المنطقي، ومتوسطة في قوة لفظ التأكيد.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0029 — التعداد والمجموعات القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٥١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L51). الشاهد المسجل: «\item Order and redundancy \emph{do} matter when we specify an».
  - **العربية المعيارية:** [السطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/enumerability.tex#L50)؛ الطبعة الدولية: [ص ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=63) (ترقيم المتن: ٦٢) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=63) (ترقيم المتن: ٦٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item إن الترتيب والتكرار \emph{مهمان بالفعل} حين نحدد تعدادًا: فيمكننا».
  - **العربية التراثية:** [السطر ٤٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/enumerability.tex#L44)؛ الطبعة التراثية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\item غير أن الترتيب والتكرار \emph{معتبران} في تعيين التعداد نفسه.».

## تعدادًا

الأصل الإنجليزي: `enumeration`. معرّف القرار: `retro-0005-0050:emphasis:8d5d6f30552c5539`.

**المعنى المقصود:** تعداد مجموعة غير خالية في الحد الرسمي هو دالة شاملة من الأعداد الموجبة إلى تلك المجموعة.

**سبب الاختيار:** يبـرز الأصل enumeration في التعريف الرسمي بعد تعريف القائمة غير الرسمي، ويقيد A بعدم الخلو لأن مجال الدالة موجب وغير خال. أبقت التراثية «تعدادًا» مع الفعل الرابط والإعراب، وحفظت شرط الشمول؛ فلا تسوي هذا الحد بالقائمة الخالية السابقة. مدخل countable set في المعجم يصوغ مكافئًا آخر بتقابل مع جزء من الأعداد الموجبة، لا يستعمل اسم enumeration في الصفحة المعاينة.

**سؤال مفتوح:** هل يفهم من «تعدادًا» في هذا التعريف أنه دالة شاملة ولو كررت القيم، أم ينبغي تنبيه موجز يفرقها من التقابل مع جزء من الموجبات؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٧-٩٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L87-L90) — التعريف الأصلي يعطي الحد الرسمي، وشرطي عدم الخلو والشمول ظاهرين في الجملة نفسها.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يعرف countable set بتقابل مع جزء من الموجبات؛ هو معيار مكافئ للمعدودية العامة، لا تعريف حرفي للتعداد بدالة شاملة.

**بديل جدير بالمقارنة:** سرد؛ يشرح القائمة ولا يسمي الدالة المعرفة في الحد الرسمي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الحد الرياضي، ومتوسطة في أقرب لفظ موحد بين التعريفين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0029 — التعداد والمجموعات القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ٨٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L88). الشاهد المسجل: «An \emph{enumeration} of a set $A \neq \emptyset$ is any».
  - **العربية المعيارية:** [السطر ٨٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/sets-functions-relations/size-of-sets/enumerability.tex#L84)؛ الطبعة الدولية: [ص ٦٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=64) (ترقيم المتن: ٦٣) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٤](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=64) (ترقيم المتن: ٦٣) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{تعداد} مجموعة $A \neq \emptyset$ هو أي دالة».
  - **العربية التراثية:** [السطر ٧٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/enumerability.tex#L73)؛ الطبعة التراثية: [ص ٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=60) (ترقيم المتن: ٥٩) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «لكل مجموعة $A \neq \emptyset$ يسمى \emph{تعدادًا} لها كل دالة».

## فافرض دالتين، كل منهما شاملة، هما

الأصل الإنجليزي: `surjective functions f and g`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0029-CLASSICAL-DUAL-SURJECTIVE-20260907`.

**المعنى المقصود:** في برهان اتحاد مجموعتين قابليتين للتعداد تفترض دالتان f وg، كل واحدة منهما شاملة لمجموعتها المقابلة.

**سبب الاختيار:** ينص الأصل على دالتين شاملتين مستقلتين f من الموجبات إلى A وg إلى B. العبارة التراثية «دالتين، كل منهما شاملة» تزيل خلل مطابقة الصفة المفردة للمثنى وتحفظ توزيـع الخاصية على كل دالة، فلا توهم شمول اتحادهما وحده. مدخل المجموعة العدودة يبين إمكان عد عناصر كل مجموعة، لكن تفصيل الدالتين واتجاه الشمول من مسألة الأصل.

**سؤال مفتوح:** هل «كل منهما شاملة» مع ذكر مجالي f وg يحدد مجموعتي الوصول مستقلتين بما يكفي قبل بناء دالة الاتحاد؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٦٤-١٧٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L164-L170) — المسألة الأصلية تذكر f وg والشمول لكل منهما ثم تطلب إنشاء تعداد الاتحاد والحالات الخالية.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يربط المعدودية بتقابل مع جزء من الموجبات؛ لا يسند صياغة المثنى هنا، وهي مستفادة من ترتيب الفرض في الأصل.

**بديل جدير بالمقارنة:** دالتين شاملتين؛ صحيح نحويًا وأوجز لكنه يبتعد عن إبقاء الرمز المشترك المفرد في المصدر العربي

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في توزع الشرط على الدالتين، ومتوسطة في أفضل ترتيب للجملة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0029 — التعداد والمجموعات القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ١٦٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L166). الشاهد المسجل: «this, suppose there are !!{surjective} functions $f\colon \PosInt \to A$ and $g\colon \PosInt \to B$, and define !!a{surjective}».
  - **العربية التراثية:** [السطر ١٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/enumerability.tex#L150)؛ الطبعة التراثية: [ص ٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=59) (ترقيم المتن: ٥٨) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «فافرض دالتين، كل منهما !!{surjective}، هما $f\colon \PosInt \to A$ و$g\colon \PosInt \to B$،».

## فيتحدثون عن عناصر القائمة ذات الرتب

الأصل الإنجليزي: `zeroth, first, second elements of a list`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0029-CLASSICAL-ZERO-INDEXED-ELEMENTS-20260907`.

**المعنى المقصود:** ترقيم عناصر القائمة بالطبيعيّات يبدأ بالرتبة صفر، ثم الأولى والثانية؛ وهو إزاحة للفهرسة لا حذف للعنصر الأول.

**سبب الاختيار:** يقول الأصل إن الرياضيين يتحدثون عن العنصر الصفري ثم الأول ثم الثاني بدل الفهرسة التي تبدأ بواحد. كانت صيغة سابقة تلحق مفردًا مذكرًا بجمع غير عاقل وتوهم فعل التسمية؛ فجاءت التراثية «فيتحدثون عن عناصر القائمة ذات الرتب» محافظة على مرجع الحديث والمطابقة، وتأتي الأرقام التالية صفر وواحد واثنان. مدخل المجموعة العدودة المعجمي يستعمل الموجبات، ولا يملي صيغة فهرسة هذه القائمة.

**سؤال مفتوح:** هل عبارة «ذات الرتب» ثم الأعداد المشرقية في الطبعة التراثية تبين للقارئ أن الصفري أول القائمة في هذا الاصطلاح؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٨٦-١٩٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L186-L192) — موضع الأصل يبين التحول من الفهرسة بالموجبات إلى الفهرسة بالطبيعيّات بدءًا بالصفر.

**مواضع المعجم المعاينة:** [ص ١٥٦ من PDF (المطبوعة ١٤٤)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=156)

**حدود الشاهد المعجمي:** PDF ص ١٥٦ يذكر الأعداد الصحيحة الموجبة عند تعريف المجموعة العدودة، ولا يتناول الرتبة الصفرية في القائمة؛ الحكم هنا من سياق الأصل والعدد المعروض.

**بديل جدير بالمقارنة:** العناصر الصفرية والأولى؛ قد توهم تعدد العناصر الصفرية بدل تحديد رتبة عنصر واحد

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في ترتيب الفهرسة ومرجع العبارة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0029 — التعداد والمجموعات القابلة للتعداد، وقوع ١:**
  - **الأصل:** [السطر ١٨٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/enumerability.tex#L189). الشاهد المسجل: «talk about the $0$th, $1$st, $2$nd, and so on, !!{element}s of a list.».
  - **العربية التراثية:** [السطر ١٧١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/enumerability.tex#L171)؛ الطبعة التراثية: [ص ٦١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=61) (ترقيم المتن: ٦٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «فيتحدثون عن !!{element}s القائمة ذات الرتب $0$ ثم $1$ ثم $2$، وهكذا.».

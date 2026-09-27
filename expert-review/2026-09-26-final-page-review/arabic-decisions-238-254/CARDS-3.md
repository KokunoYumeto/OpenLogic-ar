# بطاقات العكس والتركيب وفرعا الخلو — القرارات ٢٥٠–٢٥٤

[الرجوع إلى مقدمة الدفعة](README.md)

## توجد دالتها العكسية … وهي تقابلية أيضًا

الأصل الإنجليزي: `inverse exists and is also bijective`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0035-ar-classical-G09`.

**المعنى المقصود:** إذا كانت f تقابلًا، وجدت دالتها العكسية f^{-1} وكانت تقابلًا أيضًا، فتنتقل المساواة العددية في الاتجاه المقابل.

**سبب الاختيار:** رتبت التراثية الجملة «توجد دالتها العكسية ... وهي تقابلية أيضًا» حتى تقدم الفعل والفاعل بسياق عربي جارٍ، مع الإبقاء على وجود المعكوس وصفته وهدفه B→A. شاهد المعجم على «دالة عكسية» و«تقابل» يسند الأسماء، ولا يملي ترتيب الجملة أو برهان التناظر.

**سؤال مفتوح:** هل الجملة التراثية واضحة المرجع وسلسة دون أن توحي بأن كل دالة تملك معكوسًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٤٧-٤٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L47-L49) — شرط تقابل f في الأصل هو علة وجود المعكوس التقابلي في البرهان.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ٣٧٣ من PDF (المطبوعة ٣٦١)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=373)

**حدود الشاهد المعجمي:** PDF ص ٣٧٣ يورد inverse function «دالة عكسية» وص ٦٩ bijection «تقابلًا»؛ تقييد الوجود بالتقابل من برهان الأصل.

**بديل جدير بالمقارنة:** ولها عكس تقابلي؛ موجزة لكنها أقل بيانًا لوجود الدالة ونوعها

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في الشرط الرياضي والرمز، متوسطة في جرس العبارة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0035 — التساوي العددي، وقوع ١:**
  - **الأصل:** [السطر ٤٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L47). الشاهد المسجل: «!!a{bijection} $f\colon A \to B$. Since $f$ is !!{bijective}, its inverse $f^{-1}$ exists and is also !!{bijective}. Hence, $f^{-1}\colon B \to A$ is !!a{bijection}, so $\cardeq{B}{A}$.».
  - **العربية التراثية:** [السطر ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L32)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «\emph{التناظر.} من $\cardeq{A}{B}$ نحصل على !!a{bijection} $f\colon A \to B$. ولكون $f$ !!{bijective} توجد دالتها العكسية $f^{-1}$، وهي !!{bijective} أيضًا. فالدالة $f^{-1}\colon B \to A$ !!a{bijection} تشهد بأن $\cardeq{B}{A}$.».

## والدالة المركبة منهما … تقابلية، فيثبت بها …

الأصل الإنجليزي: `composition is bijective, so A and C are equinumerous`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0035-ar-classical-G10`.

**المعنى المقصود:** تركيب التقابلين f:A→B وg:B→C يعطي تقابلًا A→C، فيثبت التعدي.

**سبب الاختيار:** يحفظ الأصل ترتيب الأسهم حتى يكون مجال المركب A ومجاله المقابل C؛ وتقول التراثية «الدالة المركبة منهما ... تقابلية، فيثبت بها» لتبقي الشاهد دالة بعينها لا مجرد دعوى وجود. يسمي المعجم تركيب الدوال، لكنه لا يحسم ترتيب الرمز الخاص بالمشروع؛ حسمه نوع السهمين وتعريف comp في المصدر.

**سؤال مفتوح:** هل «منهما» و«بها» واضحتا العود على f وg والدالة المركبة، وهل يظهر ترتيب التركيب صحيحًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٥١-٥٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L51-L54) — مقطع التعدي في الأصل يسمي سهمي f وg ثم يكتب المركب A→C ونتيجته.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ١٢٥ من PDF (المطبوعة ١١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=125)

**حدود الشاهد المعجمي:** PDF ص ١٢٥ composition of functions «تركيب دوال»، وص ٦٩ bijection «تقابل»؛ صحة ترتيب التركيب تستند إلى الأسهم الأصلية لا إلى مدخل المعجم.

**بديل جدير بالمقارنة:** تركيب g وf؛ قد يكون اصطلاحًا صحيحًا عند تعريف آخر، لكن تبديل الأسماء دون فحص رمز comp هنا يوقع لبسًا

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في النتيجة والنوع، متوسطة في وضوح الضميرين.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0035 — التساوي العددي، وقوع ١:**
  - **الأصل:** [السطر ٥١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L51). الشاهد المسجل: «\emph{Transitivity.} Suppose that $\cardeq{A}{B}$ and $\cardeq{B}{C}$, i.e., there are !!{bijection}s $f\colon A \to B$ and $g\colon B \to C$. Then the composition $\comp{f}{g}\colon A \to C$ is !!{bijective}, so that $\cardeq{A}{C}$.».
  - **العربية التراثية:** [السطر ٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L35)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «C$. والدالة المركبة منهما $\comp{f}{g}\colon A \to C$ !!{bijective}، فيثبت بها $\cardeq{A}{C}$.».

## إذ لو لم تكن الثانية خالية، لوجد …؛ فالدالة المركبة … شاملة

الأصل الإنجليزي: `if A is empty then B is empty (otherwise ...); composition is surjective`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0035-ar-classical-G14`.

**المعنى المقصود:** في الفرع الأول: إذا خلت A ووجد تقابل f:A→B، لزم خلو B؛ وإلا كان y في B بلا سابق x في A. وفي الفرع غير الخالي، تركيب تعداد A مع f شامل إلى B.

**سبب الاختيار:** فصلت التراثية الفرض المخالف «لو لم تكن الثانية خالية» عن حالة وجود تعداد g، حتى لا يقرأ القارئ g كأنها معرفة في الفرع الخالي. الأصل كتب g(x)=y في حجة الخلو قبل تعريف g؛ صححته الطبعتان إلى f(x)=y لأن f هو التقابل المفترض منذ مطلع البرهان. أبقت التراثية بعد ذلك شمول المركب g ثم f، وهو ما يلزم لنقل التعداد.

**سؤال مفتوح:** هل يعود وصف «الثانية» بوضوح إلى B، وهل يستبين أن تصحيح f(x) في فرع الخلو مستقل عن شمول المركب في الفرع الآخر؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٧٢-٧٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L72-L77) — المقطع الأصلي يعرض فرعي الخلو والشمول وفيه اسم g(x) غير المعرف في الأول.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ١٢٥ من PDF (المطبوعة ١١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=125)

**حدود الشاهد المعجمي:** PDF ص ٦٩ يعرّف التقابل، وص ١٢٥ تركيب الدوال؛ تصحيح f بدل g يستند إلى ربط الرموز في البرهان لا إلى مدخل معجمي.

**بديل جدير بالمقارنة:** إبقاء g(x)=y كما في الأصل؛ مرفوض لأن g غير موجودة في فرع A الخالية

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في تصحيح الرمز وانفصال الفرعين، متوسطة في وضوح «الثانية».

**كل وقوع مسجل لهذا القرار:**

- **OLP-0035 — التساوي العددي، وقوع ١:**
  - **الأصل:** [السطر ٧٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L72). الشاهد المسجل: «Then either $A = \emptyset$ or there is !!a{surjective} function $g\colon \PosInt \to A$. If $A = \emptyset$, then $B = \emptyset$ also (otherwise there would be !!a{element}~$y \in B$ but no $x \in A$ with $g(x) = y$). If, on the other hand, $g\colon \PosI…».
  - **العربية التراثية:** [السطر ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L51)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «A$ يحقق $f(x) = y$. وأما إذا وجدت $g\colon \PosInt \to A$ !!{surjective}، فالدالة المركبة $\comp{g}{f} \colon \PosInt \to B$ !!{surjective}. وبيانه أن نأخذ $y \in B$؛ فالدالة $f$ !!{surjective}، ولذلك يوجد $x \in A$ يحقق $f(x) = y$. ثم إن $g$ !!{surjective}…».
- **OLP-0035 — التساوي العددي، وقوع ٢:**
  - **الأصل:** [السطر ٧٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L72). الشاهد المسجل: «Then either $A = \emptyset$ or there is !!a{surjective} function $g\colon \PosInt \to A$. If $A = \emptyset$, then $B = \emptyset$ also (otherwise there would be !!a{element}~$y \in B$ but no $x \in A$ with $g(x) = y$). If, on the other hand, $g\colon \PosI…».
  - **العربية التراثية:** [السطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L50)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «فإما $A = \emptyset$، وإما أن توجد دالة~!!a{surjective} $g\colon \PosInt \to A$. فإن كان $A = \emptyset$ لزم $B = \emptyset$؛ إذ لو لم تكن الثانية خالية، لوجد !!a{element}~$y \in B$ ولم يوجد $x \in».

## إذ لو لم تكن الثانية خالية، لوجد …

الأصل الإنجليزي: `if A is empty then B is empty (otherwise ...), in the alternative enumeration branch`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0035-ar-classical-G15`.

**المعنى المقصود:** في فرع تعريف التعداد البديل بالتقابل، يقتضي خلو A خلو B؛ ثم عند عدم الخلو يركب تقابل التعداد g مع f لينقل التعداد.

**سبب الاختيار:** يكرر الأصل حجة الخلو في الفرع المشروط بتعريف آخر للقابلة للتعداد، ويكرر الخطأ g(x)=y قبل وجود g في تلك الحالة. صححته التراثية إلى f(x)=y، وأبقت «الثانية» عائدة إلى B، ثم انتقلت إلى حالة وجود تقابل g مستقل. لا يزيل التصويب أحد التعريفين البديلين ولا يدمج فرعي البرهان.

**سؤال مفتوح:** هل مرجع «الثانية» صريح بما يكفي عند قراءة الفرع البديل وحده، وهل فصلت النسخة المعروضة الفرعين من غير تكرار مضلل؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٨٧-٩٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L87-L94) — هذا المقطع هو فرع تعريف التعداد بالتقابل، وفيه الموضع الثاني لخطأ g(x) الأصلي.

**مواضع المعجم المعاينة:** [ص ٦٩ من PDF (المطبوعة ٥٧)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=69)، [ص ١٢٥ من PDF (المطبوعة ١١٣)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=125)

**حدود الشاهد المعجمي:** PDF ص ٦٩ للتقابل وص ١٢٥ للتركيب شاهدان على الاسمين فقط؛ تصحيح الرمز وحفظ الفرع من الأصل الرياضي.

**بديل جدير بالمقارنة:** نقل g(x)=y إلى العربية كما هو؛ يبقي دالة غير معرفة في هذه الحالة

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في التصويب الرياضي، متوسطة في عبارة الإحالة «الثانية».

**كل وقوع مسجل لهذا القرار:**

- **OLP-0035 — التساوي العددي، وقوع ١:**
  - **الأصل:** [السطر ٨٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L87). الشاهد المسجل: «Then either $A = \emptyset$ or there is !!a{bijection}~$g$ whose range is $A$ and whose domain is either $\Nat$ or an initial sequence of natural numbers. If $A = \emptyset$, then $B = \emptyset$ also (otherwise there would be some~$y \in B$ with no $x \in…».
  - **العربية التراثية:** [السطر ٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L59)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (صفحة بدء الوحدة فحسب، لا صفحة اللفظ المثبتة بالدقة). الشاهد المسجل: «\emptyset$؛ إذ لو لم تكن الثانية خالية، لوجد~$y \in B$ ولم يوجد $x».

## أيًّا

الأصل الإنجليزي: `any (size)`. معرّف القرار: `semantic-propagation-20260907:AR-OLP0035-ar-classical-NFC01`.

**المعنى المقصود:** صيغة «أيًّا» المضبوطة تعرض العموم نفسه في مقارنة حجم مجموعتين من كل نوع.

**سبب الاختيار:** يخص السجل هنا ترتيب الشدة والتنوين وتوحيد الترميز لا اختيار كلمة جديدة؛ تظل any الأصلية دالة على عموم الحجم. قورنت الجملة العربية والأصلية لئلا يوهم التغيير الكتابي بتخصيص المجموعات اللانهائية وحدها. مدخل المجموعات المتساوية في المعجم سياق اصطلاحي، وليس شاهدًا على ترتيب العلامات في Unicode.

**سؤال مفتوح:** هل تظهر «أيًّا» بالضبط المقصود في الملفات والهواتف، مع بقاء العموم واضحًا؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ١٣-١٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L13-L16) — الأصل يستعمل any المبرزة لإطلاق الحجم قبل تعريف التساوي العددي.

**مواضع المعجم المعاينة:** [ص ٢٢٧ من PDF (المطبوعة ٢١٥)](https://archive.org/download/DAM2018ENAR/%D9%85%D8%B9%D8%AC%D9%85%20%D9%85%D8%B5%D8%B7%D9%84%D8%AD%D8%A7%D8%AA%20%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA.pdf#page=227)

**حدود الشاهد المعجمي:** PDF ص ٢٢٧ يقدم سياق أسماء المجموعات المتساوية العدد؛ لا يقرر شكل الضبط أو معيار NFC.

**بديل جدير بالمقارنة:** ترك ترتيب العلامات غير الموحد؛ لا يغير المعنى لكنه يضعف ثبات العرض والبحث

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** عالية في عدم تغير المعنى، ومتوسطة في مطابقة العرض على جميع الأجهزة.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0035 — التساوي العددي، وقوع ١:**
  - **الأصل:** [السطر ١٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L13). الشاهد المسجل: «We have an intuitive notion of ``size'' of sets, which works fine for finite sets. But what about infinite sets? If we want to come up with a formal way of comparing the sizes of two sets of \emph{any} size, it is a good idea to start by defining when sets…».
  - **العربية التراثية:** [السطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/sets-functions-relations/size-of-sets/equinumerous-sets.tex#L13)؛ الطبعة التراثية: [ص ٧١](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=71) (ترقيم المتن: ٧٠) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إن تصورنا المعتاد لحجم المجموعة يكفينا ما دامت منتهية؛ فإذا صرنا إلى المجموعات اللانهائية احتجنا إلى تحقيقه. ولإقامة مقارنة صورية بين مجموعتين، \emph{أيًّا} كان حجمهما، نبدأ بضبط معنى تساويهما في الحجم. وفي هذا يقول فريغه:».

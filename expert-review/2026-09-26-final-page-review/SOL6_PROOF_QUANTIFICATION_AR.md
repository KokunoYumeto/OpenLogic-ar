# المتغير المميّز والروابط والمكمّمات — مواضع الاختيار وتصحيحاته

[مدخل المراجعة](INDEX_AR.md) · [القائمة الكاملة](DIRECTORY_READABLE_AR.md)

ثلاثة قرارات في تسع مجموعات وقوع مسجلة، وتسعة وستون موضعًا للأصل والترجمتين. تشمل المقابلة جميع المواضع المسجلة لهذه القرارات، لا كل وقوعات هذه الألفاظ في الكتاب. صُحح قصور شرح المتغير المميّز عن احتواء الاستنتاج الطبيعي، ونُقل تصحيحان رياضيان موجودان في التراثية إلى المصدر المعياري المشترك. لم تصدر بعد قارئات جديدة عن هذين التعديلين المحليين.

OpenAI Codex — GPT-6.1 Sol، جهد Ultra: المقابلة والتعليل الجديدان. التعليلات السابقة لـOpenAI Codex — GPT-6 Sol، جهد Ultra، محفوظة في [الدفعة السابقة](START_HERE_AR.md). لا تنسب المقابلة إلى مراجع بشري أو إلى دوافع تاريخية مجهولة.

حُفظت الوقوعات الأصلية وصفحات القارئات السابقة بلا تبديل. خمس إحالات إنجليزية لم يكن لها سطر محلول: أضيف لها سياق مقروء محدد، مع التصريح إن كان اللفظ الإنجليزي موجودًا أم كانت العربية شرحًا أو استدراكًا. لا يجعل ذلك موضع اللفظ الغائب وقوعًا حرفيًا. صفحات المعيارية في OLP-0087 تدل على النسخة السابقة؛ ليس فيها بعد النص المصحح المعروض هنا، وقد تتغير بعد البناء. رابط المصدر المصحح نسبي إلى ملفات هذه البطاقة؛ لا يزعم أن الالتزام المثبت السابق يحتوي التصحيح. تجزئات النسخ المحلية ونهايات الأسطر موثقة؛ التنزيل المثبت للملف المتغير يثبت السابق فقط، ويُستعاد السابق بعكس التعديلين كاملًا.

## التصحيحات في المتن

الحالة الآتية محفوظة من وقت المقابلة الأولى قبل إعادة بناء القارئين؛ راجع [مدخل القراءة](INDEX_AR.md) لحالة PDF وEPUB الحالية.

في OLP-0087، سطر٥٧–٥٩: صُرح بأن الافتراضات المؤقتة A(a) التي تسقطها قاعدة حذف المكمّم الوجودي مستثناة من المنع. الأصل المفصل، سطر٥٢–٥٦، والتراثية، سطر٥٠–٦٣، ينصان على الاستثناء؛ ملخص الأصل سطر٥٨–٦١ ناقص فلا يحكم التعريف. وفي سطر٨٤–٨٥: انتفاء شرط المتغير المميّز لا يبيح حدًا غير مغلق؛ لذلك قُيد اختيار t بكونه مغلقًا، وفق الأصل سطر٢٧ و٥٢ و١٠٥–١٠٧ والتراثية سطر٨٨. يصحح ذلك المصدر المشترك للدولية والمشرق، لا الصيغ أو أشجار البرهان. لم يُبن أو يُنشر بعد PDF/EPUB جديد يتضمن هذين التعديلين.

- [المصدر المصحح الموافق لهذه البطاقة](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L57-L59)؛ السابق SHA-256 `4a35f7a7a408828a889a9df3233addcc625b4ff2551af04ad4d8f0b248983b23`؛ المصحح `703474b299636221bb5da83487d565cc39619c79e9156274fe91ea60e45b666f`.

## المتغير المميَّز

معرّف القرار: `RETRO0051-0100-eigenvariable`.

**أين وما الذي يراجع؟** التراثية PDFص٢٦١–٢٦٢ و٢٨٦–٢٨٧؛ المعيارية السابقة ص٢٦٧–٢٦٨ و٢٩٣–٢٩٤. راجعوا اسم المتغير المميّز مع حاشية أن a ثابت، وفرق شروط النسقين؛ لا تحذفوا استثناء الفروض المؤقتة في حذف الوجودي، ولا تجعلوا t غير مغلق. المعجم المفتوح للمراجعة هنا لا يوثق eigenvariable توثيقًا مستقلًا؛ كل اختيار مفتوح للتصحيح.

**المعنى:** المعلَمة a، وهي ثابت هنا وإن بقي الاسم التاريخي متغيرًا: في حساب التتابعيات، يشترط عدم ورودها في التتابعية السفلى لقاعدتي إدخال الكلي يمينًا والوجودي يسارًا. وفي الاستنتاج الطبيعي، يشترط في إدخال الكلي ألا ترد في النتيجة ولا الفروض الباقية، وفي حذف الوجودي ألا ترد في المقدمة الوجودية ولا النتيجة ولا الفروض الباقية، مع استثناء فروض A(a) التي تسقطها تلك القاعدة. ليس مجرد متغير حر أو مجرد قيمة ذاتية.

**لماذا أُبقي؟** أُبقي الاسم مع حاشية الثابت وشرط عدم الوقوع في جميع المواضع المسجلة، بعد قراءة قسمي القواعد الثلاثية اللغة كاملين. التعليل السابق وصف قاعدتي التتابعيات فقط، مع أن السجل يشمل OLP-0087 للاستنتاج الطبيعي أيضًا؛ أُصلح هذا القصور هنا. في شروط الاستنتاج الطبيعي تفصيل مختلف، فلا تنقل عبارة التتابعية السفلى إلى كل نسق. صُرح في المصدر المعياري باستثناء الفروض التي تسقطها قاعدة حذف الوجودي، وقُيد اختيار t بكونه مغلقًا، لأن التراثية والتعريفات الأصلية المفصلة يثبتان هذين القيدين. الاسم الحالي اختيار مؤقت واضح عند إلحاق شروطه، لا اصطلاح موثق في شاهد عربي مستقل قرأناه؛ مدخل متغير العام لا يكفي لتوثيق المميّز.

**البدائل:** الثابت الجديد يبين نوع a هنا، لكنه يترك الاسم التاريخي وقد يوهم أن أي ثابت جديد يفي بكل شرط دون بيان مواضع المنع؛ المعلَمة المميّزة صياغة شارحة محتملة، ولم يثبت في الشاهد المقروء أنها الاسم الاصطلاحي المستقر؛ المتغير الحر أو القيمة الذاتية لا يؤديان هذا الدور البرهاني، فلا يستبدلان به

**الثقة وحدود الشاهد:** عالية في المقابلة الرياضية وفي تحديد القيدين المصححين؛ مؤقتة في الاسم العربي المستقر لعدم شاهد مباشر. تقدير تحريري غير معاير، وليس احتمالًا إحصائيًا. فجوة توثيق اصطلاحي عربي مباشر صريحة. صفحة متغير شاهد للنوع العام فقط، وليست إثباتًا لاسم المتغير المميّز أو شرطه. صحة الشروط مأخوذة من القواعد والتعريفات الأصلية المقروءة، لا من تشابه لفظي.

- [معجم مصطلحات الرياضيات](https://archive.org/details/DAM2018ENAR)، PDF ص ٧٦٠؛ المطبوع ٧٤٨؛ variable: «متغير». المدخل العام قُرئ مع تعريفه؛ لا يوثق eigenvariable، لذلك لا ينسب إليه الاسم الخاص

**جميع مواضع الأصل والترجمتين:**

### OLP-0072

- [الأصل الإنجليزي، سطر ٣٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L30-L30)

```tex
call $a$ the \emph{eigenvariable} of the \RightR{\forall}
```

- [الأصل الإنجليزي، سطر ٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L31-L31)

```tex
inference.\footnote{We use the term ``eigenvariable'' even though $a$
```

- [الأصل الإنجليزي، سطر ٥٠](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L50-L50)

```tex
the \emph{eigenvariable} of the \LeftR{\lexists} inference.
```

- [الأصل الإنجليزي، سطر ٥٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L52-L52)

```tex
The condition that an eigenvariable not occur in the lower sequent of
```

- [الأصل الإنجليزي، سطر ٥٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L54-L54)

```tex
\emph{eigenvariable condition}.
```

- [الأصل الإنجليزي، سطر ٧٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L72-L72)

```tex
!!{variable}~$x$. However, the eigenvariable conditions in
```

- [الأصل الإنجليزي، سطر ٨٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L82-L82)

```tex
\RightR{\lforall} rules, the eigenvariable condition requires that the
```

- [المعيارية — الدولية والمشرق، سطر ٣٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L30-L30)؛ الطبعة الدولية — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث

```tex
\emph{المتغير المميَّز} لاستدلال~\RightR{\forall}.\footnote{نستعمل
```

- [المعيارية — الدولية والمشرق، سطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L31-L31)؛ الطبعة الدولية — المتن: PDF ص ٢٦٧ — بدء القسم فقط، ليس وقوع اللفظ · طبعة المشرق — المتن: PDF ص ٢٦٧ — بدء القسم فقط، ليس وقوع اللفظ

```tex
مصطلح «المتغير المميَّز» مع أن~$a$ في القاعدة أعلاه !!a{constant}؛
```

- [المعيارية — الدولية والمشرق، سطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L50-L50)؛ الطبعة الدولية — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث

```tex
\emph{المتغير المميَّز} لاستدلال~\LeftR{\lexists}.
```

- [المعيارية — الدولية والمشرق، سطر ٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L52-L52)؛ الطبعة الدولية — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث

```tex
يسمى الشرط القاضي بألا يرد المتغير المميَّز في التتابعية السفلى
```

- [المعيارية — الدولية والمشرق، سطر ٥٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L54-L54)؛ الطبعة الدولية — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٦٧ — وقوع دقيق بحسب الربط الموروث

```tex
\emph{شرط المتغير المميَّز}.
```

- [المعيارية — الدولية والمشرق، سطر ٧٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L72-L72)؛ الطبعة الدولية — المتن: PDF ص ٢٦٨ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٦٨ — وقوع دقيق بحسب الربط الموروث

```tex
كلها. غير أن شرطي المتغير المميَّز في~\RightR{\lforall}
```

- [المعيارية — الدولية والمشرق، سطر ٨٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L83-L83)؛ الطبعة الدولية — المتن: PDF ص ٢٦٨ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٦٨ — وقوع دقيق بحسب الربط الموروث

```tex
و~\RightR{\lforall}، فيقتضي شرط المتغير المميَّز ألا يرد
```

- [التراثية، سطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L29-L29)؛ الطبعة التراثية — المتن: PDF ص ٢٦١ — وقوع دقيق بحسب الربط الموروث

```tex
ويسمى~$a$ \emph{المتغير المميَّز} لاستدلال~\RightR{\forall}.\footnote{إنما بقيت تسمية «المتغير المميَّز» لأسباب تاريخية، وإن كان~$a$ هنا !!a{constant}.}
```

- [التراثية، سطر ٢٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L29-L29)؛ الطبعة التراثية — المتن: PDF ص ٢٦١ — وقوع دقيق بحسب الربط الموروث

```tex
ويسمى~$a$ \emph{المتغير المميَّز} لاستدلال~\RightR{\forall}.\footnote{إنما بقيت تسمية «المتغير المميَّز» لأسباب تاريخية، وإن كان~$a$ هنا !!a{constant}.}
```

- [التراثية، سطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L46-L46)؛ الطبعة التراثية — المتن: PDF ص ٢٦١ — وقوع دقيق بحسب الربط الموروث

```tex
وهو، أعني~$a$، \emph{المتغير المميَّز} لاستدلال~\LeftR{\lexists}.
```

- [التراثية، سطر ٤٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L48-L48)؛ الطبعة التراثية — المتن: PDF ص ٢٦١ — وقوع دقيق بحسب الربط الموروث

```tex
يسمى الشرط القاضي بألا يرد المتغير المميَّز في التتابعية السفلى
```

- [التراثية، سطر ٥٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L50-L50)؛ الطبعة التراثية — المتن: PDF ص ٢٦١ — وقوع دقيق بحسب الربط الموروث

```tex
\emph{شرط المتغير المميَّز}.
```

- [التراثية، سطر ٦٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L67-L67)؛ الطبعة التراثية — المتن: PDF ص ٢٦٢ — وقوع دقيق بحسب الربط الموروث

```tex
كلها. غير أن شرطي المتغير المميَّز في~\RightR{\lforall}
```

- [التراثية، سطر ٧٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L77-L77)؛ الطبعة التراثية — المتن: PDF ص ٢٦٢ — وقوع دقيق بحسب الربط الموروث

```tex
و~\LeftR{\lforall} من جهة المتغير المميَّز. وأما~\LeftR{\lexists}
```

### OLP-0087

- [الأصل الإنجليزي، سطر ٣١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L31-L31)

```tex
premise~$!A(a)$. We call $a$ the \emph{eigenvariable} of the
```

- [الأصل الإنجليزي، سطر ٣٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L32-L32)

```tex
\Intro{\lforall} inference.\footnote{We use the term ``eigenvariable''
```

- [الأصل الإنجليزي، سطر ٥٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L56-L56)

```tex
$a$ the \emph{eigenvariable} of the \Elim{\lexists} inference.
```

- [الأصل الإنجليزي، سطر ٥٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L58-L58)

```tex
The condition that an eigenvariable neither occur in the premises nor
```

- [الأصل الإنجليزي، سطر ٦١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L61-L61)

```tex
inference is called the \emph{eigenvariable condition}.
```

- [الأصل الإنجليزي، سطر ٧٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L78-L78)

```tex
!!{variable}~$x$. However, the eigenvariable conditions in
```

- [الأصل الإنجليزي، سطر ٨٩](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L89-L89)

```tex
\Intro{\lforall} rules, the eigenvariable condition requires that the
```

- [المعيارية — الدولية والمشرق، سطر ٣١](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L31-L31)؛ الطبعة الدولية — المتن: PDF ص ٢٩٣ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٣ — وقوع دقيق بحسب الربط الموروث

```tex
\emph{المتغير المميَّز} لاستدلال~\Intro{\lforall}.
```

- [المعيارية — الدولية والمشرق، سطر ٣٢](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L32-L32)؛ الطبعة الدولية — المتن: PDF ص ٢٩٣ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٣ — وقوع دقيق بحسب الربط الموروث

```tex
\footnote{نستعمل مصطلح ``المتغير المميَّز'' حتى وإن كان~$a$ في القاعدة
```

- [المعيارية — الدولية والمشرق، سطر ٥٤](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L54-L54)؛ الطبعة الدولية — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث

```tex
الافتراضات~$!A(a)$). ونسمي~$a$ \emph{المتغير المميَّز} لاستدلال
```

- [المعيارية — الدولية والمشرق، سطر ٥٧](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L57-L57)؛ الطبعة الدولية — المتن: PDF ص ٢٩٣,٢٩٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٣,٢٩٤ — وقوع دقيق بحسب الربط الموروث

```tex
يسمى الشرط القاضي بألا يرد المتغير المميَّز في النتائج ولا في أي
```

- [المعيارية — الدولية والمشرق، سطر ٥٩](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L59-L59)؛ الطبعة الدولية — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث

هذا السطر صُحح محليًا ليظهر استثناء الفروض المؤقتة. السطر القديم والصفحة القديمة محفوظان في الوقوع الأصلي؛ النص هنا للمصدر المصحح لا للقارئ السابق.

```tex
أو~\Elim{\lexists}، مع استثناء الافتراضات~$!A(a)$ التي تسقطها القاعدة الأخيرة، \emph{شرط المتغير المميَّز}.\footnote{تنبيه تصحيحي على الأصل: أُظهر استثناء الافتراضات المؤقتة التي تسقطها قاعدة حذف المكمّم الوجودي؛ فقد نصت عليه القاعدة المفصلة قبل هذا الملخص، وإغفاله يوسّع المنع خطأً.}
```

- [المعيارية — الدولية والمشرق، سطر ٧٦](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L76-L76)؛ الطبعة الدولية — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث

```tex
المقيد~$x$. غير أن شرطي المتغير المميَّز في~$\Intro\lforall$
```

- [المعيارية — الدولية والمشرق، سطر ٨٦](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L86-L86)؛ الطبعة الدولية — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — المتن: PDF ص ٢٩٤ — وقوع دقيق بحسب الربط الموروث

```tex
\Elim{\lexists} و\Intro{\lforall}، فيقتضي شرط المتغير المميَّز ألا
```

- [التراثية، سطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L31-L31)؛ الطبعة التراثية — المتن: PDF ص ٢٨٦ — وقوع دقيق بحسب الربط الموروث

```tex
ويسمى~$a$ \emph{المتغير المميَّز} لاستدلال~\Intro{\lforall}.
```

- [التراثية، سطر ٣٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L32-L32)؛ الطبعة التراثية — المتن: PDF ص ٢٨٦ — وقوع دقيق بحسب الربط الموروث

```tex
\footnote{بقيت تسمية «المتغير المميَّز» لأسباب تاريخية، وإن كان~$a$ في هذه القاعدة رمزًا ثابتًا.}
```

- [التراثية، سطر ٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L53-L53)؛ الطبعة التراثية — المتن: PDF ص ٢٨٧ — وقوع دقيق بحسب الربط الموروث

```tex
ويسمى~$a$ \emph{المتغير المميَّز} لاستدلال
```

- [التراثية، سطر ٥٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L56-L56)؛ الطبعة التراثية — المتن: PDF ص ٢٨٧ — وقوع دقيق بحسب الربط الموروث

```tex
هذا المنع لورود المتغير المميَّز في النتائج، أو في فرض
```

- [التراثية، سطر ٥٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L59-L59)؛ الطبعة التراثية — المتن: PDF ص ٢٨٧ — وقوع دقيق بحسب الربط الموروث

```tex
حذف المكمّم الوجودي، يسمى \emph{شرط المتغير المميَّز}.
```

- [التراثية، سطر ٦٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L63-L63)؛ الطبعة التراثية — المتن: PDF ص ٢٨٧ — وقوع دقيق بحسب الربط الموروث

```tex
قبله، وإسقاطه من الملخص يوسّع شرط المتغير المميز خطأً.
```

- [التراثية، سطر ٨٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L80-L80)؛ الطبعة التراثية — المتن: PDF ص ٢٨٧ — وقوع دقيق بحسب الربط الموروث

```tex
المقيد~$x$. غير أن شرطي المتغير المميَّز في~$\Intro\lforall$
```

- [التراثية، سطر ٨٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L88-L88)؛ الطبعة التراثية — المتن: PDF ص ٢٨٧ — وقوع دقيق بحسب الربط الموروث

```tex
أما~\Intro{\lexists} و\Elim{\lforall} فلا يلزمهما شرط المتغير المميَّز؛ ويجوز اختيار الحد المغلق~$t$ كيف اتفق.
```

**السياقات المقروءة:**

- [الأصل، quantifier-rules.tex، الأسطر ١١–١٠٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L11-L104)؛ SHA-256 للنسخة المقروءة محليًا: `254abc98503c7370e046c43f8fec7cf7b5e9909be2959b0f1c513bb278d85b78`.
- [الأصل، quantifier-rules.tex، الأسطر ١١–١١١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/first-order-logic/natural-deduction/quantifier-rules.tex#L11-L111)؛ SHA-256 للنسخة المقروءة محليًا: `5d9c3a507fe1b79e4d376963b5e3efca4a3352cc7cef7d18255c61e60592f71b`.
- [المعيارية، quantifier-rules.tex، الأسطر ١١–١٠٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L11-L105)؛ SHA-256 للنسخة المقروءة محليًا: `acbfdf7dfcf111cde788957becd9fdd0a03f9d736baa907b59bac3e8b2aee657`.
- [التراثية، quantifier-rules.tex، الأسطر ١١–٩٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/sequent-calculus/quantifier-rules.tex#L11-L98)؛ SHA-256 للنسخة المقروءة محليًا: `f00e5ad1a829a1717b132b40f6f1f38e732c724d0961c7d1ea96704d1ded230e`.
- [المعيارية، quantifier-rules.tex، الأسطر ١١–١٠٧](../../source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex#L11-L107)؛ SHA-256 للنسخة المقروءة محليًا: `703474b299636221bb5da83487d565cc39619c79e9156274fe91ea60e45b666f`.
- [التراثية، quantifier-rules.tex، الأسطر ١١–١٠٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/first-order-logic/natural-deduction/quantifier-rules.tex#L11-L109)؛ SHA-256 للنسخة المقروءة محليًا: `594bad6dd0327dcbe88ad702bc95adbbdb6fb56c4aa56e9d7ed3213362546fbe`.

## الرابط المنطقي؛ الروابط

معرّف القرار: `ar-classical-0701-0722-logical-connective`.

**أين وما الذي يراجع؟** التراثية PDFص١١٣٧ و١١٣٩ و١١٤٣–١١٤٤؛ المعيارية الدولية ص١١٥٦ و١١٥٨ و١١٦٢–١١٦٣، والمشرق يزيد صفحة في هذه المواضع. هل يفضل رابط أم رابطة في هذه الأسرة؟ لا تخلطوا رابطة الحمل بجميع الروابط، وانتبهوا أن النفي أحادي وأن عبارتي الحذف تفسران الرمزين. الاختيار مفتوح للتصحيح.

**المعنى:** رمز/عامل منطقي يبني صيغة من مدخلاتها، كالنفي والاقتران والفصل؛ ليس كل رابط ثنائيًا ولا هو مجرد رابطة بين موضوع ومحمول. في OLP-0716 من رموز اللغة؛ وفي OLP-0718 دالة بناء للصيغ؛ وفي OLP-0721 تشير عبارة حذف الرابط إلى قاعدتي حذف الاقتران والفصل في البرهان.

**لماذا أُبقي؟** أُبقيت الروابط والرابط بعد مقابلة السياقات الثلاثة بالمعجم: صفحة٤٣٤ تعرض روابط منطقية وتشرح الرموز ومثال النفي، فتثبت الجمع والفئة، لا المفاضلة النهائية بين رابط ورابطة بالمفرد. ربط الأصل في لغة الرتبة الثانية صريح، أما فقرة الاستقراء فتسميها operators وتبين دوال بناء الصيغ، وأما برهان المجموعات فيسمي قواعد الحذف برموزها؛ العربية تشرح هناك معنى الرمز ولا تقابل لفظ connective حرفيًا. بحث ابن سينا يناقش الرابطة الحملية، فلا يكفي عنوانه لتغيير أسماء كل الروابط. تصون الصياغة دالة النفي الأحادية والمثال الثنائي ولا تختزل الجميع إلى وصل قضيتين.

**البدائل:** الرابطة المنطقية مستعملة في البحث المقروء لسياق الرابطة الحملية، فلا يجعل ذلك كل استعمالها مطابقًا لconnective؛ العامل المنطقي شرح ممكن، وفي موضع الاستقراء operators لفظ الأصل؛ لا يستلزم ذلك تغيير اسم الأسرة في الكتاب؛ أداة الربط شرح لغوي محتمل لا يدعى توثيقه هنا اسمًا رياضيًا معجميًا

**الثقة وحدود الشاهد:** عالية في المفهوم والسياقات ومطابقة الجمع للشاهد؛ جيدة لا قطعية في تفضيل المفرد. تقدير تحريري غير معاير. الشاهد المباشر للجمع روابط منطقية ومفهوم الرمز؛ المفرد الحالي تكييف نحوي لا رأس معجمي مقروء في هذه الصفحة. البحث شاهد مقارنة متميزة للرابطة الحملية، لا دليل توحيد مصطلحات أو موافقة على كل الكتاب.

- [معجم مصطلحات الرياضيات](https://archive.org/details/DAM2018ENAR)، PDF ص ٤٣٤؛ المطبوع ٤٢٢؛ logical connectives: «روابط منطقية». رأس معجمي مباشر للجمع، مع شرح الرموز وأمثلتها بما فيها النفي
- [مشكلة الرابطة المنطقية عند ابن سينا وتجلياتها في المنطق المعاصر](https://asjp.cerist.dz/en/downArticle/60/14/1/222989)، PDF ص ١٢؛ المطبوع ٤٤٤؛ الرابطة والقضية: «الرابطة والقضية». قرئت الفقرة التي تميز القضية الحملية من دالة القضية؛ شاهد لحدود الرابطة الحملية لا بديل لتعريف connectives كله

**جميع مواضع الأصل والترجمتين:**

### OLP-0716

- [الأصل الإنجليزي، سطر ١٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L16-L18)

الأصل يذكر logical connectives في سطر١٦. الربط القديم بلا سطر باقٍ كما كان؛ هذه إضافة تحديد مباشر للفقرة المقروءة.

```tex
\emph{!!{function}s}.  From them, together with logical connectives,
quantifiers, and punctuation symbols such as parentheses and commas,
\emph{terms} and \emph{!!{formula}s} are formed.  The difference is
```

- [المعيارية — الدولية والمشرق، سطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L16-L16)؛ الطبعة الدولية — الملحق: PDF ص ١١٥٦ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٥٧ — وقوع دقيق بحسب الربط الموروث

```tex
مع الروابط المنطقية والمكمّمات وعلامات الترقيم كالأقواس والفواصل،
```

- [التراثية، سطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L16-L16)؛ الطبعة التراثية — الملحق: PDF ص ١١٣٧ — وقوع دقيق بحسب الربط الموروث

```tex
الروابط المنطقية والمكمّمات وعلامات الفصل، من أقواس وفواصل، أنشأنا
```

### OLP-0718

- [الأصل الإنجليزي، سطر ٨٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L88-L98)

الأصل يسميها operators ويشرح دوال بناء الصيغ، لا يسميها logical connective هنا. هذه مقابلة المعنى والسياق، لا وقوع حرفي مختلق.

```tex
For !!{formula}s, the basic elements are the atomic !!{formula}s. More
complex !!{formula}s are obtained by joining together less-complicated
!!{formula}s using operators. Each operator can be seen as
corresponding to a function of !!{formula}s that returns a new
!!{formula} joining these two together with the operator in
question. For example, the function that joins two !!{formula}s $!!^a$
and $!B$ into a conjunction can be written as $\mathcal E _\land (!!^a,
!B) = !!^a \land !B$. We can call these \emph{formula-building
  functions}. The set of !!{formula}s is closed these functions:
whenever $!!^a$ and $!B$ are !!{formula}s, so are $\lnot !!^a$, $!!^a \land
!B$, etc.
```

- [المعيارية — الدولية والمشرق، سطر ٨٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L86-L86)؛ الطبعة الدولية — الملحق: PDF ص ١١٥٨ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٥٩ — وقوع دقيق بحسب الربط الموروث

```tex
بعض باستعمال الروابط. ويمكن النظر إلى كل رابط على أنه يقابل دالة على
```

- [المعيارية — الدولية والمشرق، سطر ٨٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L87-L87)؛ الطبعة الدولية — الملحق: PDF ص ١١٥٨ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٥٩ — وقوع دقيق بحسب الربط الموروث

```tex
!!{formula}s تُرجع !!{formula} جديدة بتطبيق الرابط على مدخلاتها. فمثلًا،
```

- [التراثية، سطر ٨٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L84-L84)؛ الطبعة التراثية — الملحق: PDF ص ١١٣٩ — وقوع دقيق بحسب الربط الموروث

```tex
بضم !!{formula}s أقل تعقيدًا بواسطة الروابط. فلكل رابط دالة على
```

- [التراثية، سطر ٨٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L85-L85)؛ الطبعة التراثية — الملحق: PDF ص ١١٣٩ — وقوع دقيق بحسب الربط الموروث

```tex
!!{formula}s، ترد !!{formula} جديدة عند تطبيق الرابط على مدخلاته. ومن
```

### OLP-0721

- [الأصل الإنجليزي، سطر ٥٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/proofs-about-sets.tex#L52-L56)

الأصل يسمي conjunction elimination ويرمز لها، لا يذكر connective في هذه العبارة. العربية تشرح حذف الرابط. وقُرئ كذلك تلميح حذف الفصل في سطر٩٦–١٠٠، وهو ضمن السياق الكامل الموثق.

```tex
This completes the first half of the proof. Note that in the last
step we used the fact that if a conjunction ($z \in X$ and $z \in X
\cup Y$) follows from an assumption, each conjunct follows from that
same assumption. You may know this rule as ``conjunction
elimination,'' or $\land$Elim. Now let's prove (b):
```

- [المعيارية — الدولية والمشرق، سطر ٥١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/sets-functions-relations/sets/proofs-about-sets.tex#L51-L51)؛ الطبعة الدولية — الملحق: PDF ص ١١٦٢ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٦٣ — وقوع دقيق بحسب الربط الموروث

```tex
«حذف الاقتران»، أي قاعدة حذف الرابط~$\land$. والآن لنبرهن (ب):
```

- [المعيارية — الدولية والمشرق، سطر ٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/sets-functions-relations/sets/proofs-about-sets.tex#L93-L93)؛ الطبعة الدولية — الملحق: PDF ص ١١٦٣ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٦٤ — وقوع دقيق بحسب الربط الموروث

```tex
إلى البرهان بالحالات، أي قاعدة حذف الرابط~$\lor$.)
```

- [التراثية، سطر ٤٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/sets-functions-relations/sets/proofs-about-sets.tex#L49-L49)؛ الطبعة التراثية — الملحق: PDF ص ١١٤٣ — وقوع دقيق بحسب الربط الموروث

```tex
ذلك الفرض. وهذه هي قاعدة «حذف الاقتران»، أي حذف الرابط~$\land$. وننتقل
```

- [التراثية، سطر ٩٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/sets-functions-relations/sets/proofs-about-sets.tex#L90-L90)؛ الطبعة التراثية — الملحق: PDF ص ١١٤٤ — وقوع دقيق بحسب الربط الموروث

```tex
إلى تقسيم البرهان إلى حالات، أي إلى قاعدة حذف الرابط~$\lor$.)
```

**السياقات المقروءة:**

- [الأصل، language-of-sol.tex، الأسطر ٩–٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L9-L35)؛ SHA-256 للنسخة المقروءة محليًا: `b334d1a0decdc9ded917dc1b9b5e49dfafc14c67949233c912f7b19b432121d8`.
- [الأصل، introduction.tex، الأسطر ٧٦–١٠٤](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L76-L104)؛ SHA-256 للنسخة المقروءة محليًا: `0a3327920db03385bcae0062435654fd82227d5e622e87f4194628de4fdbddda`.
- [الأصل، proofs-about-sets.tex، الأسطر ٣٧–١٠١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/sets-functions-relations/sets/proofs-about-sets.tex#L37-L101)؛ SHA-256 للنسخة المقروءة محليًا: `394714c03cea3d400ca79ed47f0c4b47c496cb714a3fd8e5c03debec1ab55161`.
- [المعيارية، language-of-sol.tex، الأسطر ٩–٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L9-L35)؛ SHA-256 للنسخة المقروءة محليًا: `0fdf2ae513bd8fdfb721d0198a2c2356e9214649858d3da1d872181c47929235`.
- [التراثية، language-of-sol.tex، الأسطر ٩–٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L9-L35)؛ SHA-256 للنسخة المقروءة محليًا: `67f741f81409d9b080b20d2f07095d5ceb00c2c0e9d5f7d39c59031119bd5f76`.
- [المعيارية، introduction.tex، الأسطر ٧٩–٩٩](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L79-L99)؛ SHA-256 للنسخة المقروءة محليًا: `7fe61358500b6f1f30e6656fb1ed55f5131d0283e511fcb37606703debf00871`.
- [التراثية، introduction.tex، الأسطر ٧٨–٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/sets-functions-relations/inductive-defs-proofs/introduction.tex#L78-L97)؛ SHA-256 للنسخة المقروءة محليًا: `4f214c68a56b9037ef45c3000c5a624754596c77de92f97eea7cee2d6a5427c6`.
- [المعيارية، proofs-about-sets.tex، الأسطر ٣٦–٩٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/sets-functions-relations/sets/proofs-about-sets.tex#L36-L96)؛ SHA-256 للنسخة المقروءة محليًا: `6ae09e651ccf3a960a3ac7deac385e5471a3c2e27e4df4a172ad101a859af831`.
- [التراثية، proofs-about-sets.tex، الأسطر ٣٥–٩٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/sets-functions-relations/sets/proofs-about-sets.tex#L35-L93)؛ SHA-256 للنسخة المقروءة محليًا: `b18798c07d8d9d7948a341c08189a1ca60e8aa8762e6320e5d5d73cbd8f10b72`.

## المكمِّم؛ الكمية

معرّف القرار: `ar-classical-0701-0722-quantifier`.

**أين وما الذي يراجع؟** التراثية PDFص١١٢٥–١١٢٦ و١١٢٩ و١١٣٥ و١١٣٧؛ الدولية ص١١٤٤ و١١٤٨ و١١٥٤ و١١٥٦، والمشرق يزيد صفحة في هذه المواضع. هل توحد الأسرة على السور أم تبقى المكمّم مع وصف القواعد كميًا؟ راجعوا علاقات/دوال الرتبة الثانية، ولا تعدوا استدراك OLP-0713 ترجمة حرفية لفقرة إنجليزية. الاختيار مفتوح للتصحيح.

**المعنى:** عامل يربط متغيرًا تكميمًا كليًا أو وجوديًا، وقواعد الاستدلال الخاصة به. في لغة الرتبة الثانية قد يكون المتغير لعلاقة أو دالة، لا لفرد فقط. المكمّم اسم العامل؛ كمي/كمية وصف للاستدلال أو القاعدة، وليس اسمًا ثانيًا للرمز أو كمية عددية.

**لماذا أُبقي؟** أُبقيت أسرة المكمّم/الكمي في المواضع المسجلة بعد قراءة لغة الرتبة الثانية وصيغ قواعد البرهان؛ التعليل السابق اقتصر على حساب التتابعيات ولم يوضح متغيرات الرتبة الثانية. يثبت البحث العربي المقروء في صفحة١٧ السور الكلي والسور الوجودي مع الصيغ الرمزية، ولذلك يسجل السور بديلًا موثقًا لا مجرد تخمين. لا يثبت البحث لفظ المكمّم المختار ولا شروط المتغير المميّز. في OLP-0713 القاعدتان الكميتان شجرتا استدراك عربيتان لتفصيل تحويل G3c إلى G1c، وليس في النص الإنجليزي المقابل لفظ quantifier أو تلك الشجرتان؛ يُصرح بذلك بدل إيجاد موضع لفظ غائب. التناوب بين الاسم والصفة لا يبيح حذف نوع الكمية أو تبديل نطاقها.

**البدائل:** السور: بديل له شاهد عربي معاصر مقروء للسور الكلي والوجودي، ويحتاج توحيدًا مدروسًا للأسرة إن اختير؛ العامل الكلي/الوجودي: شرح المعنى، لا يزعم أنه رأس معجمي للفظ العام؛ الكمية بوصفها مقدارًا عدديًا لا تؤدي معنى quantifier؛ استعمال كمي للقواعد وصف سياقي وليس هذا الخلط

**الثقة وحدود الشاهد:** عالية في هوية العامل ونطاق المتغيرات وفي فصل الاسم عن الصفة؛ مؤقتة في أولوية المكمّم على السور. تقدير تحريري غير معاير. السور موثق في البحث؛ المكمّم غير موثق مباشرة في الصفحات المعجمية المقروءة هنا، وفجوة الاختيار محفوظة. البحث يتكلم على المنطق المعاصر ولا يثبت اسمًا أصيلًا لابن سينا لكل استعمال حديث. المقابلة لا تصدق جميع وقوعات الأسرة أو كل براهين الملحق.

- [مشكلة الرابطة المنطقية عند ابن سينا وتجلياتها في المنطق المعاصر](https://asjp.cerist.dz/en/downArticle/60/14/1/222989)، PDF ص ١٧؛ المطبوع ٤٤٩؛ النفي القضوي: «السور الكلي؛ السور الوجودي». قرئت الصفحة كاملة وصيغ النفي فيها؛ تثبت البديل الاسمي، ولا تحدد قواعد الكتاب أو شاهدًا لاسم المكمّم

**جميع مواضع الأصل والترجمتين:**

### OLP-0716

- [الأصل الإنجليزي، سطر ١٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L16-L21)

الأصل يذكر quantifiers في سطر١٧، ثم يصرح بتكميم متغيرات العلاقات والدوال في الرتبة الثانية. هذا تحديد جديد لسياق مقروء لا تغيير للوقوع الموروث.

```tex
\emph{!!{function}s}.  From them, together with logical connectives,
quantifiers, and punctuation symbols such as parentheses and commas,
\emph{terms} and \emph{!!{formula}s} are formed.  The difference is
that in addition to variables for objects, second-order logic also
contains variables for relations and functions, and allows
quantification over them. So the logical symbols of second-order logic
```

- [المعيارية — الدولية والمشرق، سطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L16-L16)؛ الطبعة الدولية — الملحق: PDF ص ١١٥٦ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٥٧ — وقوع دقيق بحسب الربط الموروث

```tex
مع الروابط المنطقية والمكمّمات وعلامات الترقيم كالأقواس والفواصل،
```

- [التراثية، سطر ١٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L16-L16)؛ الطبعة التراثية — الملحق: PDF ص ١١٣٧ — وقوع دقيق بحسب الربط الموروث

```tex
الروابط المنطقية والمكمّمات وعلامات الفصل، من أقواس وفواصل، أنشأنا
```

### OLP-0703

- [الأصل الإنجليزي، سطر ٤٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/quantifiers.tex#L48-L48)

```tex
  exercises. We consider the cases where $\pi$ ends in a quantifier
```

- [المعيارية — الدولية والمشرق، سطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/proof-theory/sequent-calculus/quantifiers.tex#L13-L13)؛ الطبعة الدولية — الملحق: PDF ص ١١٤٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٤٥ — وقوع دقيق بحسب الربط الموروث

```tex
تُدخل قواعد الكميات بعض التعقيدات بسبب «شروط المتغير المميَّز» التي تنطبق
```

- [التراثية، سطر ١٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/quantifiers.tex#L13-L13)؛ الطبعة التراثية — الملحق: PDF ص ١١٢٥ — وقوع دقيق بحسب الربط الموروث

```tex
تنشأ في قواعد الكميات دقة زائدة من «شروط المتغير المميَّز» الملازمة
```

- [التراثية، سطر ٤٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/quantifiers.tex#L46-L46)؛ الطبعة التراثية — الملحق: PDF ص ١١٢٦ — وقوع دقيق بحسب الربط الموروث

```tex
  فظاهرة، ونكلها إلى القارئ تمرينًا. ويبقى أن ننظر في الاستدلال الكمي
```

### OLP-0713

- [الأصل الإنجليزي، سطر ٧٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/translations.tex#L75-L99)

ليس هنا لفظ quantifier ولا الاشتقاقان الكميان؛ النص العربي يستدرك حالتي الكلي يسارًا والوجودي يمينًا. السياق الإنجليزي يبين التحويل لكنه ناقص في حصر القواعد المختلفة؛ الربط سياقي غير حرفي، لا شهادة وقوع لفظ غائب.

```tex
  If $\pi$ ends in a rule~$R$, the inductive hypothesis yields
  !!{proof}s in \Log{G1c} of the premises, and we can apply the same
  rule~$R$ to those !!{proof}s. The exceptions are the rules
  \LeftR{\land} and \RightR{\lor}, which differ between \Log{G1c}
  and~\Log{G3c}. The \Log{G3c} versions are derivable in \Log{G1c} as follows:
  \[
  \Axiom$!A, !B, \Gamma \fCenter \Delta$
  \RightLabel{\LeftR{\land}}
  \UnaryInf$!A \land !B, !B, \Gamma \fCenter \Delta$
  \RightLabel{\LeftR{\land}}
  \UnaryInf$!A \land !B, !A \land !B, \Gamma \fCenter \Delta$
  \RightLabel{\LeftR{\Contraction}}
  \UnaryInf$!A \land !B, \Gamma \fCenter \Delta$
    \DisplayProof
\qquad
  \Axiom$\Gamma \fCenter \Delta, !A, !B$
  \RightLabel{\RightR{\lor}}
  \UnaryInf$\Gamma \fCenter \Delta, !A \lor !B, !B$
  \RightLabel{\RightR{\lor}}
  \UnaryInf$\Gamma \fCenter \Delta, , !A \lor !B, !A \lor !B$
  \RightLabel{\RightR{\Contraction}}
  \UnaryInf$\Gamma \fCenter \Delta, !A \lor !B$
    \DisplayProof
  \]
\end{proof}
```

- [المعيارية — الدولية والمشرق، سطر ١٠٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/proof-theory/sequent-calculus/translations.tex#L100-L100)؛ الطبعة الدولية — الملحق: PDF ص ١١٥٤ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٥٥ — وقوع دقيق بحسب الربط الموروث

```tex
  وتُشتق نسختا القاعدتين الكميتين على النحو الآتي:
```

- [التراثية، سطر ٩٧](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/translations.tex#L97-L97)؛ الطبعة التراثية — الملحق: PDF ص ١١٣٥ — وقوع دقيق بحسب الربط الموروث

```tex
  وأما صورتا القاعدتين الكميتين فتشتقان على الوجه الآتي:
```

### OLP-0711

- [الأصل الإنجليزي، سطر ٣٨](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/rules-proofs.tex#L38-L38)

```tex
The quantifier rules are slightly more complicated. E.g., the rules in
```

- [المعيارية — الدولية والمشرق، سطر ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/proof-theory/sequent-calculus/rules-proofs.tex#L36-L36)؛ الطبعة الدولية — الملحق: PDF ص ١١٤٨ — وقوع دقيق بحسب الربط الموروث · طبعة المشرق — الملحق: PDF ص ١١٤٩ — وقوع دقيق بحسب الربط الموروث

```tex
قواعد الكميات أعقد قليلًا. فقواعد~$\lforall$ في~\Log{G1c} مثلًا هي:
```

- [التراثية، سطر ٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/rules-proofs.tex#L36-L36)؛ الطبعة التراثية — الملحق: PDF ص ١١٢٩ — وقوع دقيق بحسب الربط الموروث

```tex
وأما قواعد الكميات ففيها مزيد دقة. فقواعد~$\lforall$ في~\Log{G1c} مثلًا:
```

**السياقات المقروءة:**

- [الأصل، language-of-sol.tex، الأسطر ٩–٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L9-L35)؛ SHA-256 للنسخة المقروءة محليًا: `b334d1a0decdc9ded917dc1b9b5e49dfafc14c67949233c912f7b19b432121d8`.
- [الأصل، quantifiers.tex، الأسطر ١١–٦٣](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/quantifiers.tex#L11-L63)؛ SHA-256 للنسخة المقروءة محليًا: `15c8fe5ebaeac187948c9c217934511e70735afdb4de68191355fb590b25287c`.
- [الأصل، translations.tex، الأسطر ١١–١٠١](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/translations.tex#L11-L101)؛ SHA-256 للنسخة المقروءة محليًا: `fe035ce79aae2c23f8756a69fc344736ff35e02f1ce9a40fe957ea55fab5b7d0`.
- [الأصل، rules-proofs.tex، الأسطر ٣٥–٦٢](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/proof-theory/sequent-calculus/rules-proofs.tex#L35-L62)؛ SHA-256 للنسخة المقروءة محليًا: `8eed76ae91f4518e1cdc5f7cdd36890e1c8004a7f2f94b263e7caa8f405e5c8a`.
- [المعيارية، language-of-sol.tex، الأسطر ٩–٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L9-L35)؛ SHA-256 للنسخة المقروءة محليًا: `0fdf2ae513bd8fdfb721d0198a2c2356e9214649858d3da1d872181c47929235`.
- [التراثية، language-of-sol.tex، الأسطر ٩–٣٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/second-order-logic/syntax-and-semantics/language-of-sol.tex#L9-L35)؛ SHA-256 للنسخة المقروءة محليًا: `67f741f81409d9b080b20d2f07095d5ceb00c2c0e9d5f7d39c59031119bd5f76`.
- [المعيارية، quantifiers.tex، الأسطر ١١–٦٢](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/proof-theory/sequent-calculus/quantifiers.tex#L11-L62)؛ SHA-256 للنسخة المقروءة محليًا: `fcb3dc31a0eed525c92ceefc6a223ac072a8ec4238f646f23853d63c3e78a0a8`.
- [التراثية، quantifiers.tex، الأسطر ١١–٦٠](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/quantifiers.tex#L11-L60)؛ SHA-256 للنسخة المقروءة محليًا: `79d0924201d56d2fe8e9aada39348997ace6da4b28560c3b1578eb5acf52f7e7`.
- [المعيارية، translations.tex، الأسطر ١١–١١٨](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/proof-theory/sequent-calculus/translations.tex#L11-L118)؛ SHA-256 للنسخة المقروءة محليًا: `6e3e1ef93e734b4cec71ddecc722ddbfd482aa030bd3188a9cae599f4a551870`.
- [التراثية، translations.tex، الأسطر ١١–١١٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/translations.tex#L11-L115)؛ SHA-256 للنسخة المقروءة محليًا: `817dbd6e9ef4e6331d5043c6396aa48e83e4bc8b968da0f6907b722729620f57`.
- [المعيارية، rules-proofs.tex، الأسطر ٣٤–٦١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar/content/proof-theory/sequent-calculus/rules-proofs.tex#L34-L61)؛ SHA-256 للنسخة المقروءة محليًا: `acbc35b432142705dc63e74af0ceea3f71c4d39ed78b2e7947175564c5bdbddb`.
- [التراثية، rules-proofs.tex، الأسطر ٣٤–٦١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/a0f19b713fcc9a199e8bc71e16d171e1a858ba2f/source/locale/ar-classical/content/proof-theory/sequent-calculus/rules-proofs.tex#L34-L61)؛ SHA-256 للنسخة المقروءة محليًا: `5e1ba8c3dec20ee4d0ddad2efc94726e7868b0a3fc4d8953b8147a4ebaadf148`.

## حدود القراءة

قورنت صياغة التعليل والشرح بفقرة المعجم التعريفية وبعرض البحث العربي للسور والنفي، مع تمييز اللغة التاريخية المروية عن لغة كاتب البحث المعاصر. وضوح التعريف وشروطه مقدم على محاكاة جملة بعينها. لا ادعاء بأن هذه المصطلحات الحديثة هي أسماء علماء العصور الوسطى، أو بأننا قرأنا كل المصادر التي يستشهد بها البحث. شواهد نصوص Rasaif المقروءة سابقًا تظل مقارنات أسلوبية محدودة وليست توثيقًا جديدًا للمصطلحات الثلاثة. لا فجوة اصطلاحية توقف الإنتاج في انتظار شخص.

[الموسوعة: هوية المقارنة السابقة](SOL6_FUNCTION_DEFINITIONS_AR.md). لا تنشر هذه البطاقة صفحات المعجم أو الموسوعة أو أزواج النصوص التراثية الكاملة، ولا تتخذ نتائج البحث غير المقروءة شاهدًا. سجل JSON يحفظ النصوص المصدرية المحددة والتجزئات والوقوعات الأصلية والتعليل السابق. كل اختيار مفتوح للتصحيح؛ لا تنتظر عملية الإنتاج استجابة المراجع.

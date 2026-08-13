# نص المنطق المفتوح — الإصدار العربي التراكمي

[افتح القارئ العربي الحالي (OLP-0010، عشرة من 722 وحدة)](reader/00_OPENLOGIC_ar_CUMULATIVE_LINKED_READER_OLP-0010.pdf)

- DOI المفهومي العربي الثابت: [10.5281/zenodo.21921850](https://doi.org/10.5281/zenodo.21921850)
- DOI إصدار OLP-0010: [10.5281/zenodo.21921851](https://doi.org/10.5281/zenodo.21921851)
- الكائن المعلن: إصدار عربي تراكمي متطور لمشروع المنطق المفتوح
- التغطية الحالية: الوحدات OLP-0001–OLP-0010، أي 10/722 من وحدات المحتوى المجمدة
- اللغة: العربية الفصحى الحديثة الرسمية (`ar`؛ رمز Zenodo `ara`)
- سلطة المصدر المجمدة: تعهد مشروع المنطق المفتوح
  `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`، وشجرة Git
  `f67757bb9305b173634082ab4cefd5601a707a34`

هذا المستودع هو سطح النشر المستقل للإصدار العربي. يضم القارئ التراكمي
المقدمة والبنية الافتتاحية والفصل الكامل «المجموعات» بأقسامه الستة، ولا
يستورد الوحدات الإنجليزية غير المترجمة. لا يدّعي أن الوحدات الـ712 الباقية
قد تُرجمت.

## محتويات النشر

- `reader/00_OPENLOGIC_ar_CUMULATIVE_LINKED_READER_OLP-0010.pdf`: قارئ مرتبط من 13 صفحة.
- `source/locale/ar/`: مصادر LaTeX العربية القابلة للتحرير، وضبط اللغة، وبرنامج التشغيل التراكمي.
- `build/BUILD.ps1`: بناء LuaLaTeX حتمي بتاريخ مصدر مثبت.
- `evidence/COMPONENT_COVERAGE.tsv`: ربط كل وحدة بالمصدر والترجمة والهاش.
- `evidence/QA_STATE.json`: حالة فحوص المصدر والبناء والعرض والاستخراج والمراجعة.
- `evidence/UNRESOLVED_ITEMS.tsv`: النطاق المتبقي وقيود النفاذية المعلنة.
- `evidence/DATACITE_RELATIONS.json`: نية علاقات DataCite، ومنها `IsTranslationOf`.

أُعيد بناء القارئ العام من هذا المستودع نفسه في بيئة UTC. هاش PDF العام هو
`AFFF3F21E71060462FD842C18E48B15F7C8284175FB2D39C23920B870DA57ABD`؛
وتطابق الصفحات المصورة الثلاث عشرة ونص Poppler بنيويًا وبالبايت شهود البناء
الداخلي المجمد، مع اختلاف بايتات PDF الناتج عن تمثيل المنطقة الزمنية في
بيانات LuaTeX الوصفية.

سيعرض سجل Zenodo عند نشر هذا الإصدار أربعة ملفات فقط: القارئ، وحزمة المصادر القابلة للتحرير،
وحزمة الأدلة والمنشأ والقرارات، وبيان SHA-256. تحفظ حزمة الأدلة سجلات
المصطلحات والقرارات والإخفاقات والتصحيحات وسلطة المصدر والبناء والعرض
والمراجعة وحدودها.

لا يوجد حتى تاريخ هذا الإصدار DOI حقيقي لمجموعة عالمية متعددة اللغات خاصة
بمشروع المنطق المفتوح؛ لذلك لا نخترع علاقة `IsPartOf`. يمكن إضافتها بتحديث
وصفي حين يوجد المحور الفعلي.

المصدر الأصلي مرخص بموجب CC BY 4.0. هذه ترجمة معدلة مستقلة، ولا تعني اعتماد
مشروع المنطق المفتوح لها. أُغلق نطاق هذا الإصدار بفحص مباشر للمصدر، ومراجعة
آلية مستقلة، وبناء حتمي، وفحص مرئي لكل صفحة، وهاشات دقيقة. لا توجد مراجعة
بشرية/أهلية أصلية حتى الآن، ولا يُدّعى اعتماد مجتمعي أو شهادة نفاذية.

## English identification

This is the independently maintained Arabic evolving edition of *The Open
Logic Text*, produced from the Open Logic Project source. This immutable
checkpoint contains OLP-0001 through OLP-0010 (10/722 source-ordered units),
not the complete corpus. It provides a linked 13-page reader, editable source,
the exact CC BY 4.0 source license, deterministic build inputs, and complete
translation/typesetting/provenance evidence for the declared checkpoint.
There is no human/native review or PDF accessibility certification. The Git
release tag and commit are recorded only after the standalone publication
repository is initialized and committed; no placeholder commit is asserted.

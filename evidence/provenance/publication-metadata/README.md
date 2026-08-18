# نص المنطق المفتوح — النسخة العربية الكاملة للمصدر المثبّت

هذه هي النسخة العربية المستقلة الكاملة من متن مشروع المنطق المفتوح عند
الإصدار `OLP-0722-20260818`. يغطي إغلاق الترجمة جميع وحدات المحتوى
المثبّتة البالغ عددها 722 وحدة.

## هوية الإصدار

- DOI المفهومي العربي الثابت: [10.5281/zenodo.21921850](https://doi.org/10.5281/zenodo.21921850)
- DOI الدقيق لهذه النسخة: [10.5281/zenodo.21987686](https://doi.org/10.5281/zenodo.21987686)
- إصدار GitHub: [ar-olp-0722-20260818](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-20260818)
- النسخة: `OLP-0722-20260818`
- اللغة: العربية الفصحى المعاصرة العالمية (`ar`؛ رمز Zenodo `ara`)
- المؤلف والمنشئ الوحيد في بيانات الاستشهاد: `Open Logic Project`
- المساهم الوحيد: `AI typesetting & translation`، بدور Zenodo «Other»، بلا معرّف أو انتساب مؤسسي
- سلطة المصدر: التعهد `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`
- شجرة المصدر: `f67757bb9305b173634082ab4cefd5601a707a34`
- الترخيص: CC BY 4.0، ما لم يذكر مكوّن بعينه خلاف ذلك

## نطاق الإغلاق

- القارئ المترابط الأساسي: 642 وحدة يصل إليها مسار الكتاب، في 819 صفحة.
- ملحق الإغلاق التقني المستقل: 80 وحدة محتفظًا بها خارج مسار القارئ، في 123 صفحة.
- الحساب الكامل: 642 + 80 = 722 وحدة.

الملحق منشور بوصفه شاهدًا تقنيًا على إغلاق الترجمة والبناء، لكنه ليس جزءًا
من ترتيب القراءة الأساسي للكتاب ولا يغيّر بنية القارئ.

## أصول الإصدار

| الرقم | الأصل | الوظيفة |
|---:|---|---|
| 00 | `00_OPENLOGIC_ar_COMPLETE_LINKED_READER_OLP-0722.pdf` | القارئ العربي المترابط الكامل |
| 01 | `01_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_OLP-0722.pdf` | الملحق التقني للوحدات الثمانين |
| 02 | `02_OPENLOGIC_ar_EDITABLE_SOURCES_OLP-0722.zip` | مصادر TeX القابلة للتحرير ومدخلات البناء الدقيقة |
| 03 | `03_OPENLOGIC_ar_EVIDENCE_AND_PROVENANCE_OLP-0722.zip` | أدلة المصدر والبناء والعرض والاستخراج والمنشأ |
| 04 | `04_OPENLOGIC_ar_SHA256_MANIFEST_OLP-0722.txt` | هاشات SHA-256 للأصول 00–03 |

لا تُعد أي نسخة في مجلد بناء عامل أصلًا منشورًا. تُثبت البايتات النهائية
وهاشاتها فقط في بيان SHA-256 بعد نجاح البناء النهائي وإعادة بنائه بصورة
مستقلة.

## البناء القابل لإعادة التشغيل

يشغّل `build/BUILD.ps1` القارئ الكامل أولًا باستخدام LuaLaTeX وBibTeX،
ثم يبني الملحق مرتين مع حل المراجع من ملف AUX للقارئ. يثبت البرنامج
`SOURCE_DATE_EPOCH` والمنطقة الزمنية، ويتحقق من عدد الصفحات، ويمكنه التحقق
من هاشات متوقعة وتمهيد أصلي PDF النهائيين صراحةً فقط عند تمرير المفتاح
`-StageReleaseAssets`.

متطلبات البيئة وخطوات البناء التفصيلية في `build/BUILD_REQUIREMENTS.md`.

## حدود معلنة

- ملفا PDF غير موسومين بعناصر بنيوية ولا يحملان شهادة PDF/UA أو اعتماد نفاذية.
- استخراج Unicode للرياضيات وترتيب بعض النصوص ثنائية الاتجاه غير كاملين؛ مصادر TeX القابلة للتحرير هي المرجع النصي.
- لم تُجرَ مراجعة بشرية عربية أو أهلية، ولا يُدّعى اعتماد المجتمع اللغوي.
- هذا الإصدار المستقل لا يعني تأييد مشروع المنطق المفتوح.
- العلاقة المقصودة بالمصدر هي اشتقاق/ترجمة من التعهد المثبّت؛ لا تُخترع علاقة `IsPartOf` لمجموعة عالمية غير موجودة.

## English descriptor

This is the independently maintained complete Arabic edition of *The Open
Logic Text* for the frozen Open Logic source release. Version
`OLP-0722-20260818` closes all 722 translation units as a 642-unit, 819-page
canonical linked reader plus a separate 80-unit, 123-page technical closure
supplement. The PDFs are untagged; mathematical and RTL extraction is not
fully authoritative; editable TeX is authoritative. No Arabic-speaking
human/native review, community approval, accessibility certification, or
Open Logic Project endorsement is claimed.

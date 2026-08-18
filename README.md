# نص المنطق المفتوح — النسخة العربية الكاملة مع إعادة تنضيد إضافية للشاشة

يضم هذا المستودع النسخة العربية المستقلة الكاملة من متن مشروع المنطق المفتوح
للمصدر المثبّت. يضيف الإصدار `OLP-0722-SCREEN-20260818` ملفّي PDF للقراءة
على الشاشة، ويحفظ جميع أصول الطباعة في الإصدار `OLP-0722-20260818` من دون
أي تغيير في بايتاتها.

## هوية الإصدار

- DOI المفهومي العربي الثابت: [10.5281/zenodo.21921850](https://doi.org/10.5281/zenodo.21921850)
- آخر DOI دقيق منشور في Zenodo قبل إصدار الشاشة هذا: [10.5281/zenodo.21987686](https://doi.org/10.5281/zenodo.21987686)، وهو خاص بإصدار الطباعة `OLP-0722-20260818`
- إصدار GitHub الإضافي: [ar-olp-0722-screen-20260818](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-screen-20260818)
- النسخة: `OLP-0722-SCREEN-20260818`
- اللغة: العربية الفصحى المعاصرة العالمية (`ar`؛ رمز Zenodo: `ara`)
- المؤلف والمنشئ الوحيد في بيانات الاستشهاد: `Open Logic Project`
- سلطة المصدر: التعهد `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`
- شجرة المصدر: `f67757bb9305b173634082ab4cefd5601a707a34`
- الترخيص: CC BY 4.0، ما لم يذكر مكوّن بعينه خلاف ذلك

لا يُدّعى بعدُ DOI دقيق مستقل لإصدار الشاشة. يقدّم ملف `.zenodo.json` بيانات
وصفية عربية أولًا لنسخة Zenodo جديدة مستقبلًا؛ ولم تُعدَّل سجلات Zenodo
المنشورة سابقًا.

## النطاق والتنسيقان

المحتوى واحد في تنسيق الطباعة وتنسيق الشاشة:

- القارئ المترابط الأساسي: 642 وحدة.
- ملحق الإغلاق التقني المستقل: 80 وحدة خارج مسار القارئ.
- الحساب الكامل: 642 + 80 = 722 وحدة.

يبقى تنسيق الطباعة في 819 و123 صفحة. وتعرض إعادة تنضيد الشاشة المحتوى نفسه
بخط 14 نقطة، وكتلة نص أوسع، وهوامش متناظرة، وعرض افتتاحي ملائم لعرض الشاشة،
في 946 و136 صفحة. هذا تنسيق ثابت، وليس مستندًا متجاوبًا أو قابلًا لإعادة
التدفق الحقيقي.

## أصول الإصدار

| الرقم | الأصل | الوظيفة |
|---:|---|---|
| 00 | `00_OPENLOGIC_ar_COMPLETE_LINKED_READER_OLP-0722.pdf` | القارئ العربي المترابط في تنسيق الطباعة، بلا تغيير في البايتات |
| 01 | `01_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_OLP-0722.pdf` | الملحق التقني في تنسيق الطباعة، بلا تغيير في البايتات |
| 02 | `02_OPENLOGIC_ar_EDITABLE_SOURCES_OLP-0722.zip` | المصادر الكاملة القابلة للتحرير للإصدار الأساس |
| 03 | `03_OPENLOGIC_ar_EVIDENCE_AND_PROVENANCE_OLP-0722.zip` | الأدلة والمنشأ للإصدار الأساس |
| 04 | `04_OPENLOGIC_ar_SHA256_MANIFEST_OLP-0722.txt` | هاشات الأصول 00 إلى 03 |
| 05 | `05_OPENLOGIC_ar_COMPLETE_LINKED_READER_SCREEN_OLP-0722.pdf` | القارئ المُعاد تنضيده للشاشة، 946 صفحة |
| 06 | `06_OPENLOGIC_ar_CLOSURE_SUPPLEMENT_80_UNITS_SCREEN_OLP-0722.pdf` | الملحق المُعاد تنضيده للشاشة، 136 صفحة |
| 07 | `07_OPENLOGIC_ar_SCREEN_LAYOUT_SOURCES_AND_EVIDENCE_OLP-0722.zip` | مشغّلات التنضيد الإضافية، وتعليمات البناء، وأدلة البناء وQA المنقّحة |
| 08 | `08_OPENLOGIC_ar_SHA256_MANIFEST_SCREEN_UPDATE_OLP-0722.txt` | هاشات SHA-256 لجميع الأصول 00 إلى 07 |

لا يضع البيان 08 هاشًا لنفسه. يتألف كل سطر من 64 رقمًا سداسيًا عشريًا كبيرًا،
ثم مسافتين، ثم اسم الأصل الأساس.

## البناء القابل لإعادة التشغيل

يُبنى تنسيق الطباعة بواسطة `build/BUILD.ps1`، وتُبنى إعادة تنضيد الشاشة بواسطة
`build/BUILD_SCREEN.ps1`. يبني برنامج الشاشة القارئ أولًا باستخدام LuaLaTeX
وBibTeX، ثم يبني الملحق مع إحالات AUX إلى قارئ الشاشة. يتحقق البرنامج من
عدد الصفحات، ووجود DOI المفهومي، وغياب DOI الدقيق للنسخة من المشغّلات،
والهاشات الاختيارية، ويرفض الكتابة فوق أي أصل إصدار موجود.

ترد التفاصيل في `build/BUILD_REQUIREMENTS.md` و
`build/BUILD_SCREEN_REQUIREMENTS.md`.

## حدود معلنة

- ملفات PDF غير موسومة بعناصر بنيوية ولا تحمل شهادة PDF/UA أو اعتماد نفاذية.
- استخراج Unicode للرياضيات وترتيب بعض النصوص ثنائية الاتجاه غير كاملين؛ مصادر TeX القابلة للتحرير هي المرجع النصي.
- لم تُجرَ مراجعة بشرية عربية أو أهلية، ولا يُدّعى اعتماد المجتمع اللغوي.
- هذا الإصدار المستقل لا يعني تأييد مشروع المنطق المفتوح.
- العلاقة المقصودة بالمصدر هي اشتقاق/ترجمة من التعهد المثبّت؛ لا تُخترع علاقة `IsPartOf` لمجموعة عالمية غير موجودة.

## English descriptor

This repository contains the independently maintained complete Arabic edition
of *The Open Logic Text*. The additive `OLP-0722-SCREEN-20260818` release
preserves the existing print assets byte-for-byte and adds a 642-unit,
946-page linked reader plus an 80-unit, 136-page closure supplement retypeset
for on-screen reading. These PDFs use a fixed Letter page with 14-point type,
a wider text block, symmetric margins, and FitH opening behavior; they are not
genuinely responsive or reflowable. They remain untagged and are not PDF/UA
certified. No separate Zenodo version DOI is claimed until a new Zenodo version
is actually published.

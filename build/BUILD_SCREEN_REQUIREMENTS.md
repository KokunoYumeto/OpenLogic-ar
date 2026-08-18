# متطلبات بناء إعادة تنضيد الشاشة العربية OLP-0722

يصف هذا المستند بناء ملفّي PDF إضافيين وثابتين للقراءة على الشاشة. يبقى بناء
الطباعة وجميع الأصول 00 إلى 04 بلا تغيير.

## الهوية والمخرجات المثبّتة

- النسخة: `OLP-0722-SCREEN-20260818`
- DOI المفهومي الثابت: `10.5281/zenodo.21921850`
- لا يُدرج DOI دقيق للنسخة في المشغّلات، لأن نسخة Zenodo الجديدة لم تُنشر بعد.
- تعهد المصدر: `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`
- قارئ الشاشة: 946 صفحة، 8,562,041 بايتًا، SHA-256 `BD8380128CCE7E4450758DCD31CFD3E067C822883EC0495A3107397F54EC323A`
- ملحق الشاشة: 136 صفحة، 1,310,705 بايتات، SHA-256 `29102C967BCE24F8F1D8CB1005C4A60728F45C2AAF6ED9253B62DED70FBAEB7F`

## المدخلات

- `source/locale/ar/open-logic-complete-ar-screen.tex`
- `source/locale/ar/open-logic-closure-supplement-ar-screen.tex`
- مشغّلا الأساس المناظران وجميع ملفات الهدف الـ722 في حزمة مصدر OLP-0722
- قائمة المراجع ونمط BibTeX تحت `source/bib/`
- خطوط Scheherazade المثبّتة تحت `00_control/fonts/scheherazade-2.100/`

لا يغيّر مشغّلا الشاشة أي ملف هدف ترجمة أو بيان إغلاق أو ربط وحدات. وهما
يضيفان فقط هندسة الشاشة، وحجم الخط، والعنوان الفرعي، وسلوك افتتاح PDF،
وتصغيرًا موضعيًا محدودًا لصيغتين عريضتين، ثم يُدخلان مشغّلَي الأساس المثبّتين.

## الأدوات والتسلسل

- PowerShell 7 أو Windows PowerShell 5.1
- LuaLaTeX وBibTeX وPoppler `pdfinfo`
- بيئة MiKTeX والخطوط المثبّتة نفسها المسجلة في أدلة OLP-0722

يضبط `BUILD_SCREEN.ps1` القيم `SOURCE_DATE_EPOCH=1783874174` و
`FORCE_SOURCE_DATE=1` و`TZ=UTC` في عملية البناء فقط، ثم يعيد القيم السابقة.
يُبنى القارئ ثلاث مرات مع تمرير BibTeX بين التمريرين الأول والثاني، ثم يُبنى
الملحق مرتين مع AUX قارئ الشاشة.

تنفيذ بناء نظيف والتحقق من الهاشات النهائية:

```powershell
pwsh -NoProfile -File .\build\BUILD_SCREEN.ps1 `
  -OutputDirectory <مجلد-نظيف-صريح> `
  -ExpectedCompleteSha256 BD8380128CCE7E4450758DCD31CFD3E067C822883EC0495A3107397F54EC323A `
  -ExpectedSupplementSha256 29102C967BCE24F8F1D8CB1005C4A60728F45C2AAF6ED9253B62DED70FBAEB7F
```

لا ينزّل البرنامج ملفات، ولا يشغّل Git، ولا يمسح نظام الملفات. لا يُستخدم
`-StageReleaseAssets` إلا للمرحلة الأولى من نسخ 05 و06، ويرفض البرنامج
الكتابة فوق أي وجهة موجودة.

## بوابات القبول

- 946 و136 صفحة، بلا تشفير، في حجم Letter.
- العرض الافتتاحي `/FitH`، والتخطيط `/OneColumn`، ولوحة العلامات `/UseOutlines`.
- وجود DOI المفهومي وغياب DOI الدقيق السابق أو الحالي من كلا المشغّلين.
- تقارب LuaLaTeX وBibTeX وغياب أخطاء التوقف في التقارير.
- تطابق بايتات بناءين نظيفين مستقلين.
- تطابق هاشات المشغّلات وملفات PDF مع قائمة الإصدار.
- حفظ بايتات أصول الطباعة 00 إلى 04.

لا تنشئ هذه البوابات ادعاء مستند متجاوب أو قابل لإعادة التدفق أو PDF/UA أو
نفاذية أو مراجعة بشرية عربية.

## English descriptor

Build the additive fixed-layout Arabic screen reader and closure supplement
from the frozen OLP-0722 source without changing any translation target,
closure manifest, binding, or print asset. Require 946 and 136 pages, the
recorded SHA-256 values, FitH opening behavior, and byte-identical independent
rebuilds. The screen PDFs are untagged and are not genuinely responsive or
reflowable.

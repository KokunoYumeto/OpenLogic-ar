# متطلبات بناء النسخة العربية الكاملة OLP-0722

يصف هذا الملف البناء النهائي للقارئ العربي القانوني وملحق الإغلاق التقني.
لا يُعد أي PDF ناتجًا منشورًا حتى ينجح البناء النظيف مرتين، وتتطابق البايتات
والهاشات، وتُسجّل في بيان SHA-256 النهائي.

## الهوية المثبّتة

- النسخة: `OLP-0722-20260818`
- DOI المفهومي: `10.5281/zenodo.21921850`
- DOI الدقيق المحجوز: `10.5281/zenodo.21987686`
- تعهد المصدر: `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`
- شجرة المصدر: `f67757bb9305b173634082ab4cefd5601a707a34`
- هاش بيان إغلاق الوحدات: `0CCA3735E506581BE93C87542FA1F8236281834B71831C9D767C4B43E5361952`
- ربط الهدفين الكامل: `C7ADBCC67F6D7C6ED79FF81EE2F12E8597A994EB4894BA1AAA2F6B1610B78BB4`

## شجرة الإدخال المطلوبة

يُشغّل البرنامج من مستودع النشر، ويتوقع:

- `source/locale/ar/open-logic-complete-ar.tex`
- `source/locale/ar/open-logic-closure-supplement-ar.tex`
- جميع ملفات الهدف العربية الـ722 المسماة في `CLOSURE_MANIFEST.csv`
- اتحاد مدخلات `INPUT` في ملفي FLS النهائيين، بعد استبعاد نواتج البناء
- `source/bib/open-logic.bib` و`source/bib/natbib-oup.bst`
- ملفات Scheherazade المثبّتة تحت `00_control/fonts/scheherazade-2.100/`

يجب أن يثبت FLS أن القارئ يصل إلى 642 ملف هدف، وأن الملحق يصل إلى 80 ملفًا
آخر، وأن اتحادهما يساوي 722 بلا فقد أو تداخل غير معلن.

## الأدوات

- PowerShell 7 أو Windows PowerShell 5.1
- LuaLaTeX من توزيعة MiKTeX المثبّتة والمُسجّلة في إيصال البناء
- BibTeX
- Poppler `pdfinfo`

لا ينزّل برنامج البناء حزمًا، ولا يشغّل Git، ولا يبحث في نظام الملفات. يجب
أن تكون كل الحزم المطلوبة موجودة قبل التشغيل، وأن تُحفظ نسخة MiKTeX ونسخ
الحزم والخطوط في أدلة الإصدار.

## الخطوط المثبّتة

| الملف | SHA-256 |
|---|---|
| `Scheherazade-Regular.ttf` | `034C3ED203CCF91E20A75181350759CC5878E0E369BB0E2E83ACEE15A829184F` |
| `Scheherazade-Bold.ttf` | `62DDE529B296DF074EFBF75B40A986E8FF82E997B98CEC9AD7AB6795BB17A622` |
| `OFL.txt` | `458314C1EBC013A6ED6055EC23ACB93C4EF54BC41D8BA35C0BBC232849D0D804` |
| `FONT_RECEIPT.md` | `8CFE02B657E0120BC98884F75CDFFBF3C0BFD6E572FDE5E67969EF795A51A879` |

## تسلسل البناء

يضبط `BUILD.ps1` القيم الآتية في عملية البناء ثم يعيد قيم البيئة السابقة:

- `SOURCE_DATE_EPOCH=1783874174`
- `FORCE_SOURCE_DATE=1`
- `TZ=UTC`
- `TEXINPUTS` بحيث يسبق مجلد الناتج المسار الافتراضي

ثم ينفذ:

1. LuaLaTeX على القارئ الكامل.
2. BibTeX على مهمة القارئ في مجلد الناتج.
3. تمريرين إضافيين من LuaLaTeX على القارئ.
4. تمريرين من LuaLaTeX على الملحق، مع حل المراجع من AUX القارئ.
5. فحص وجود PDFين، وعدد الصفحات، وSHA-256.

الاستخدام العادي:

```powershell
pwsh -NoProfile -File .\build\BUILD.ps1 -OutputDirectory <مجلد-نظيف-صريح>
```

للتحقق من هاشات معروفة:

```powershell
pwsh -NoProfile -File .\build\BUILD.ps1 `
  -OutputDirectory <مجلد-نظيف-صريح> `
  -ExpectedCompleteSha256 <SHA256> `
  -ExpectedSupplementSha256 <SHA256>
```

لا يُستخدم `-StageReleaseAssets` إلا بعد اكتمال الفحص النهائي؛ ويرفض البرنامج
الكتابة فوق أي أصل إصدار موجود.

## بوابات القبول

- القارئ الكامل: 819 صفحة.
- ملحق الوحدات الثمانين: 123 صفحة.
- غياب DOI إصدار OLP-0010 القديم من كلا المشغّلين.
- وجود DOI المحجوز `10.5281/zenodo.21987686` في كلا المشغّلين.
- تقارب المراجع والاستشهادات وعدم وجود خطأ LuaLaTeX/BibTeX.
- تطابق هاش PDF لكل مهمة بين بناءين نظيفين مستقلين.
- نجاح فحص الروابط والخطوط والاستخراج والعرض لكل الصفحات.

ملفا PDF غير موسومين بنيويًا، واستخراج الرياضيات والنص ثنائي الاتجاه غير
كامل؛ لذلك لا ينشئ نجاح البناء ادعاء PDF/UA أو نفاذية أو مراجعة بشرية عربية.

## English descriptor

Build the 642-unit, 819-page canonical Arabic reader first, including BibTeX,
then build the separate 80-unit, 123-page closure supplement against the
reader AUX. Run twice in distinct clean output directories and require
byte-identical PDFs before release staging. The script performs no Git or
network operation and refuses to overwrite existing release assets.

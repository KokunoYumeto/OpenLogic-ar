# تنقيح المسارات العامة لأدلة الشاشة 16:9

استُبدلت كل صورة لـ`C:\Users\Floris` و`C:/Users/Floris` في تقارير LOG وFLS
وBLG المنشورة بالعلامة `<USER_HOME>`. وحُوّلت حقول مسار الإدخال والإخراج في
إيصالَي إصلاح الروابط إلى أسماء عامة داخل `private-build/` و`release/`.
بلغ عدد الاستبدالات النصية 2927، وأعاد الفحص صفراً لاسم المستخدم أو لجذر
`C:\Users` و`C:/Users` داخل ملفات الحزمة العامة.

لا يغيّر التنقيح ملفات PDF أو المشغّلات أو ملفات الهدف أو قياسات الإصلاح.
تسجل قائمة `RAW_SCREEN_BUILD_EVIDENCE_SHA256.tsv` هاشات السجلات الخام،
وتسجل قائمة الحزمة هاشات النسخ العامة.

## English descriptor

All private user-home spellings in the published LOG/FLS/BLG records were
replaced with `<USER_HOME>`, and repair-receipt paths were made portable.
No PDF, TeX wrapper, translation target, link mapping, or semantic invariant
was changed.

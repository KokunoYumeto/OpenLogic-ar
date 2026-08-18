# تنقيح المسارات العامة

تبقى تقارير LOG وBLG الخام في مخرجات البناء الخاصة ولا تُنشر. استُبدلت جميع
صور اسم المستخدم وجذر ملف المستخدم في النسخ العامة بعلامات `<USER>` أو
`<USER_HOME>` أو `<USERS>`. بعد الاستبدال، أعاد البحث البايتي صفر نتيجة لاسم
المستخدم أو لصيغ جذور المستخدم في Windows.

يغيّر التنقيح الإيصالات النصية فقط. لم تتغير ملفات PDF 05 و06، ولا المشغّلات،
ولا ملفات هدف الترجمة. تسجل `inventories/RAW_BUILD_EVIDENCE_SHA256.tsv`
هاشات الإيصالات الخام، وتسجل `inventories/SCREEN_BUNDLE_SHA256.tsv` هاشات
النسخ العامة.

## English descriptor

Private user paths in the published LOG and BLG receipts were replaced with
public placeholders. Raw receipt hashes are retained separately. No PDF,
translation source, wrapper, manifest, or binding byte was changed.

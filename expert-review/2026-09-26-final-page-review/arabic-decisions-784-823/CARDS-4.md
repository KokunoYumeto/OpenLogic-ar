# بطاقات القيمة والنتيجة — القرارات ٧٩٠–٧٩١

[الرجوع إلى مقدمة الدفعة](README.md)

## 𝔳̅(¬ ◇(p ∧ ¬ p)) = 𝔽

الأصل الإنجليزي: `The final modal example evaluates to False, not Undef.`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0394-MODAL-FINAL-VALUE-20260907`.

**المعنى المقصود:** في امتداد لوكاشيفيتش الثلاثي بجداول □ و◇ المحددة هنا، إذا كانت v(p) مجهولة كانت قيمة ¬◇(p∧¬p) كاذبة.

**سبب الاختيار:** قد يبدو ذلك مخالفًا للحدس الكلاسيكي، لكنه مثال قصور جداول الإمكان الثلاثية المقترحة: p∧¬p غير محدد ثم ◇ له صادق فنفيه كاذب. لا أعممه على دلالة كريبكه العادية.

**سؤال مفتوح:** هل تعرض الخطوات الوسيطة للقيم الثلاث للقارئ، وهل يبقى المثال مقيدًا بجداول لوكاشيفيتش المعينة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٣٥-٢٣٧](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/three-valued-logics/lukasiewicz.tex#L235-L237) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0394 — منطق Łukasiewicz، وقوع ١:**
  - **الأصل:** [السطر ٢٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/three-valued-logics/lukasiewicz.tex#L235). الشاهد المسجل: «\land \lnot p)$ should be a tautology. However, if $\pAssign v(p) = \Undef$, then $\pValue v(\lnot \Diamond(p \land \lnot p)) = \Undef$. Although \L ukasiewicz was correct that two truth».
  - **العربية التراثية:** [السطر ٢٢٤](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/many-valued-logic/three-valued-logics/lukasiewicz.tex#L224)؛ الطبعة التراثية: [ص ٦٦٨](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=668) (ترقيم المتن: ٦٦٧) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$\pValue v(\lnot \Diamond(p \land \lnot p)) = \False$.».
- **OLP-0394 — منطق Łukasiewicz، وقوع ٢:**
  - **الأصل:** [السطر ٢٣٥](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/many-valued-logic/three-valued-logics/lukasiewicz.tex#L235). الشاهد المسجل: «\land \lnot p)$ should be a tautology. However, if $\pAssign v(p) = \Undef$, then $\pValue v(\lnot \Diamond(p \land \lnot p)) = \Undef$. Although \L ukasiewicz was correct that two truth».
  - **العربية المعيارية:** [السطر ٢٣٣](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/many-valued-logic/three-valued-logics/lukasiewicz.tex#L233)؛ الطبعة الدولية: [ص ٦٨٥](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=685) (ترقيم المتن: ٦٨٤) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٨٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=686) (ترقيم المتن: ٦٨٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «$\pValue v(\lnot \Diamond(p \land \lnot p)) = \False$. ومع أن».

## فلا تكون له نتيجتان نهائيتان مختلفتان؛ ولا تضمن هذه الخاصية وحدها وجود نتيجة نهائية.

الأصل الإنجليزي: `there is still only a single value of the expression`. معرّف القرار: `semantic-propagation-20260907:AR-OLP-0368-CONDITIONAL-NORMAL-FORM-UNIQUENESS-20260907`.

**المعنى المقصود:** خاصية تقول إن النتيجة النهائية فريدة إن وجدت، ولا تثبت بمفردها وجود نتيجة نهائية لكل حد.

**سبب الاختيار:** فصلت uniqueness المشروطة من normalizing existence؛ التلاقي قد يمنع نتيجتين مختلفتين ومع ذلك تبقى سلسلة اختزال لا تنتهي.

**سؤال مفتوح:** هل تبين العربية بوضوح الفرق بين الوحدانية والوجود في الخلاصة؟

**موضع الأصل الإنجليزي الذي استُعمل في هذه المراجعة:** [الأسطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/church-rosser/definitions-and-properties.tex#L26) — تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**وجه جمع المواضع:** تُقارن العبارة الأصلية بسياقها الرياضي المحدد قبل تقرير دلالة اللفظ في الطبعة العربية.

**نتيجة البحث المعجمي المحدود:** في الفحص المعجمي المحدود لهذه الدفعة لم يثبت شاهد مصور مطابق لهذا الدور؛ لذلك لا تُنسب الصياغة المختارة إلى المعجم دون بينة.

**بديل جدير بالمقارنة:** لا بديل محدد تقتضيه الشواهد في هذا الموضع

**تقدير الثقة التحريرية (ليس احتمالًا إحصائيًا):** متوسطة: ثبت المقصود من سياق المصدر، وتظل المفاضلة بين الألفاظ قابلة لتصحيح المختص.

**كل وقوع مسجل لهذا القرار:**

- **OLP-0368 — التعريف والخصائص، وقوع ١:**
  - **الأصل:** [السطر ٢٦](https://github.com/OpenLogicProject/OpenLogic/blob/9620cc73f9c8e0ad003c514a5d3748f29611c4c0/content/lambda-calculus/church-rosser/definitions-and-properties.tex#L26). الشاهد المسجل: «there is still only a single value of the expression.».
  - **العربية المعيارية:** [السطر ٢٥](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar/content/lambda-calculus/church-rosser/definitions-and-properties.tex#L25)؛ الطبعة الدولية: [ص ٦٥٢](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf#page=652) (ترقيم المتن: ٦٥١) (موضع السطر مطابق لصفحة القارئ)؛ طبعة المشرق: [ص ٦٥٣](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-current-msa-pdf-sync-20260924/03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf#page=653) (ترقيم المتن: ٦٥٢) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «سبيل لمتابعة حساب ما، فلا تكون له نتيجتان نهائيتان مختلفتان؛ ولا تضمن هذه الخاصية وحدها وجود نتيجة نهائية.».
  - **العربية التراثية:** [السطر ٣١](https://github.com/KokunoYumeto/OpenLogic-ar/blob/86a4a7c11c0a0289ade28cb8f96acbacf9c01844/source/locale/ar-classical/content/lambda-calculus/church-rosser/definitions-and-properties.tex#L31)؛ الطبعة التراثية: [ص ٦٣٦](https://github.com/KokunoYumeto/OpenLogic-ar/releases/download/ar-olp-0722-classical-eastern-rtl-complete-20260926/00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf#page=636) (ترقيم المتن: ٦٣٥) (موضع السطر مطابق لصفحة القارئ). الشاهد المسجل: «إذا جعلنا~$\xredone$ اختزال~$\beta$، لزم من خاصية تشيرش--روسر أن الصورة السوية، متى وجدت، لا تتعدد. فلنفرض أن~$M$ يختزل إلى~$P$ وإلى~$Q$،».

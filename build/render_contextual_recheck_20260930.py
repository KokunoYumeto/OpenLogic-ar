"""Personally assessed finite choices, with exact contexts and source transitions."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from stream_expert_review_decisions import iter_decisions
from render_function_definition_recheck_20260930 import ENGLISH, INDEX, ROOT, BASE, EAST

LEDGER = ROOT / 'evidence/classical/terminology/SOL6_CONTEXTUAL_RECHECK_20260930.json'
CARD = 'SOL6_CONTEXTUAL_CHOICES_AR.md'
OLD = ROOT / 'evidence/classical/terminology/ARABIC_REVIEW_BATCH_31_38_20260927.json'
EXPECTED_INDEX = 'FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12'
SFR = 'content/sets-functions-relations/'

# Ranges selected after actually reading the passages, not by keyword ranking.
# Each tuple is (English, MSA, Classical); support ranges are not new occurrences.
RANGES = {
    SFR+'arithmetization/cauchy.tex': ((109,125),(102,117),(50,57)),
    SFR+'relations/equivalence-relations.tex': ((17,21),(16,20),(16,20)),
    SFR+'size-of-sets/non-enumerability.tex': ((11,27),(11,27),(11,23)),
    SFR+'size-of-sets/non-enumerability-alt.tex': ((11,27),(11,27),(11,23)),
    SFR+'size-of-sets/enumerability.tex': ((252,266),(254,270),(228,241)),
    SFR+'size-of-sets/comparing-size.tex': ((70,88),(67,85),(47,58)),
    'content/open-logic-about.tex': ((11,19),(10,16),(9,15)),
}

CHOICES = {
 'retro-0005-0050:emphasis:e8e86fa8b14fc932': {
  'sense_ar': 'لكل دالة h من الطبيعي إلى النسبي: لكل ε نسبي موجب يوجد ℓ طبيعي بحيث يكون |h(n)| أصغر من ε لكل n أكبر من ℓ. لا يفترض هذا الحد وجود الأعداد الحقيقية التي يبنيها الفصل، ولا يقصر التعريف على متتاليات كوشي وحدها.',
  'rationale_ar': 'أُبقيت إن داخل مقول قلنا في التراثية، بعد مقابلة التعريف المكمم في النصوص الثلاثة. تعرض صفحة المعجم ١٤٧ التقارب بقول يتلوه حكم على المتتالية، وتوضح صفحة ٤٩٤ معنى المتتالية الصفرية. وتقدم فقرة ابن سينا canon-ibn-sina_00437 مثالًا مقروءًا لبناء فنقول ثم إنّا في بيان المقصود. هذه شواهد لبناء القول ومعنى التقارب، لا نقل حرفي لعبارة h تؤول إلى صفر. إن هنا أداة جملة، وليست جزءًا من اسم اصطلاح رياضي جديد. في المعيارية تقع إن قبل العبارة المؤكدة، وفي التراثية داخلها؛ لا يتغير الشرط أو نطاق الكميات بذلك.',
  'alternatives_ar': ['حذف إن من مقول قلنا ممكن في بناء آخر، لكنه ليس إصلاحًا رياضيًا ولا يثبت رجحانه هنا', 'h تتقارب من الصفر أقرب إلى صياغة المعجم؛ لم يثبت أن تبديل أسرة تؤول يحسن هذا الموضع أو الكتاب كله'],
  'expert_question_ar': 'التراثية PDF ص ٩٥: هل يجري قلنا إن h تؤول إلى صفر بسلاسة، وهل يكفي بيان أن ε نسبي موجب؟ لا تجعلوا هذا حدًا يفترض الأعداد الحقيقية قبل بنائها. الاختيار مفتوح للتصحيح.',
  'canon_limit_ar': 'يثبت الشاهد الرياضي مفهوم التقارب إلى الصفر، والشاهد الأسلوبي تركيب القول؛ لا يثبت أي منهما العبارة الحالية حرفيًا أو هوية طبعة النص التراثي. لا ننقل تكميمًا على الأعداد الحقيقية من تعريف المعجم إلى هذا البناء النسبي.',
  'confidence_ar': 'عالية في المعنى والكمّيات لمطابقة النصوص؛ جيدة في بناء مقول القول؛ مؤقتة في تفضيل تؤول على تتقارب. تقدير تحريري غير معاير.',
  'canon_evidence': [
   {'source_id':'DAM2018ENAR','physical_pdf_page':147,'printed_page':135,'entry':'convergent sequence','short_quote_ar':'متتالية متقاربة','relation_ar':'قرأنا الفقرة المكممة كاملة وبناء القول فيها؛ شاهد معنى وتركيب، لا نقل حروف التعريف النسبي'},
   {'source_id':'DAM2018ENAR','physical_pdf_page':494,'printed_page':482,'entry':'null sequence','short_quote_ar':'متتالية صفرية','relation_ar':'يشرح التقارب من الصفر؛ لا يقترح هنا استبدال عبارة الترجمة باسم المتتالية'},
  ],
 },
 'retro-0005-0050:emphasis:3f36b6b993e1028e': {
  'sense_ar':'إذا كانت R علاقة تكافؤ على A، كان العنصران x وy متكافئين وفق R متى تحقق Rxy؛ ليس المراد أنهما متساويان أو أن العلاقة عامة بلا تعيين.',
  'rationale_ar':'أُبقي متكافئان وفق R في النصين العربيين: التثنية تطابق العنصرين، والقيد يسند التكافؤ إلى العلاقة المعينة، ويعقبه الشرط Rxy نفسه. قُرئت صفحة المعجم ٢٢٨: علاقة التكافؤ تجمع الانعكاسية والتناظر والتعدية، أما مدخل عنصرين متكافئين فتعريفه خاص بعناصر حلقة وعامل قابل للعكس. لذلك يؤخذ منه الشاهد اللغوي للتثنية فقط، ولا ينقل شرط الحلقة إلى التعريف العام. وفق R اختيار ربط واضح لكنه ليس العبارة المعجمية الحرفية.',
  'alternatives_ar':['متكافئان بالنسبة إلى R يؤدي القيد نفسه؛ لا شاهد مقروء يرجحه هنا','متساويان يفسد المعنى العام: الهوية مثال للتكافؤ وليست كل علاقة تكافؤ'],
  'expert_question_ar':'التراثية PDF ص ٤٣، المعيارية ص ٤٥: راجعوا وضوح وفق R في هذا التعريف؛ هل تفضلون بالنسبة إلى R؟ أبقوا Rxy ولا تستبدلوا التكافؤ بالمساواة. الاختيار مفتوح للتصحيح.',
  'canon_limit_ar':'المعجم يثبت الفئة ووصف العناصر في سياق آخر، لا التركيب المقيد كله. لا دعوى أصالة تراثية لهذا الاصطلاح الحديث.',
  'confidence_ar':'عالية في حفظ المفهوم والتثنية، جيدة لا قطعية في اختيار حرف الربط. تقدير تحريري غير معاير.',
  'canon_evidence':[{'source_id':'DAM2018ENAR','physical_pdf_page':228,'printed_page':216,'entry':'equivalence relation; equivalent elements','short_quote_ar':'علاقة تكافؤ؛ عنصران متكافئان','relation_ar':'قرئ المدخلان؛ الأول للفئة العامة، والثاني شاهد لغوي بتعريف حلقي لا يعمم'}],
 },
 'retro-0005-0050:section:7a619a6b3e5be629': {
  'sense_ar':'مجموعات غير معدودة بالمعنى المجموعاتي: لا يوجد تقابل بينها وبين جزء من الصحيحات الموجبة. قابلية التعداد في هذا الفصل تشمل المجموعات المنتهية والخالية، ولا تطلب برنامجًا أو خوارزمية للتعداد.',
  'rationale_ar':'أُبقي العنوان في موضعي OLP-0033 وOLP-0039 بعد قراءة مدخليهما والتعريفين اللذين يحيلان إليهما. التعريف الأول يستعمل دالة شاملة من الصحيحات الموجبة للمجموعة غير الخالية، ويضم الخالية صراحة إلى القابلة للتعداد؛ والبديل يستعمل تقابلًا مع الطبيعي أو مقطع ابتدائي مع معالجة الخالية. لذلك ينفي غير قابلة للتعداد وجود التعداد المجموعاتي، لا إمكان حسابه آليًا. في صفحتي المعجم ٤٨٦ و٧٥٠ الرسم غير عدودة بلا ميم؛ له شاهد تعريفي مباشر، لكنه ليس لفظ العنوان الحالي. يحتفظ السجل بتصحيح النقل السابق ولا يعيد تقديمه كاكتشاف جديد. تغيير الاسم ينبغي أن يراعي الأسرة في الكتاب، لا هذين العنوانين وحدهما.',
  'alternatives_ar':['مجموعة غير عدودة: الرسم المطبوع في المدخلين اللذين قرأناهما؛ بديل اصطلاحي جدي','غير قابلة للعد: شرح ممكن، لا يدعى أنه رأس معجمي في الشاهدين','غير قابلة للتعداد الحسابي: مرفوض هنا لأنه يضيف شرطًا خوارزميًا لا يوجد في التعريف'],
  'expert_question_ar':'العنوانان: التراثية PDF ص ٦٦ و٧٦، المعيارية ص ٧٠ و٨٠. هل يبقى غير قابلة للتعداد أم توحد الأسرة على غير عدودة؟ انتبهوا أن المقصود countable، لا computably enumerable، وأن الخالية داخلة في القابل للتعداد. الاختيار مفتوح للتصحيح.',
  'canon_limit_ar':'تثبت الصفحتان غير عدودة وتعريف الكثرة المجموعاتية؛ لا تثبتان لفظ غير قابلة للتعداد حرفيًا. الموضعان فقط مفحوصان هنا، لا كل أسرة المصطلح.',
  'confidence_ar':'عالية في المعنى وفي نقل الرسم المعجمي بعد قراءة الأصل؛ مؤقتة في تفضيل اللفظ الجاري على البديل. تقدير تحريري غير معاير.',
  'canon_evidence':[
   {'source_id':'DAM2018ENAR','physical_pdf_page':486,'printed_page':474,'entry':'nondenumerable set','short_quote_ar':'مجموعة غير عدودة','relation_ar':'قرأنا الرأس والتعريف: انتفاء تقابل مع الصحيحات الموجبة أو جزء منها'},
   {'source_id':'DAM2018ENAR','physical_pdf_page':750,'printed_page':738,'entry':'uncountable set','short_quote_ar':'مجموعة غير عدودة','relation_ar':'الرسم نفسه؛ تعريف الكثرة لا يضيف قيد الحوسبة'},
  ],
 },
 'retro-0005-0050:shared-token:895d9bd2ecaafef3': {
  'sense_ar':'صفة لدالة تحقق التباين والشمول معًا. في OLP-0029 تثبت داخل برهان تحويل التعداد، وفي OLP-0036 ينفى وجودها من باب أولى بعد نفي الدالة الشاملة.',
  'rationale_ar':'أُبقيت تقابلية بعد فحص الموضعين الحقيقيين، لا عنوان التعريف وحده. في برهان OLP-0029 يصرح النص العربي باسم دالة ثم الصفة؛ وفي OLP-0036 تشير الصفة إلى الدالة التي يمتنع وجودها لأن الشمول ممتنع. يحفظ من باب أولى اتجاه الحجة: التقابل يستلزم الشمول، لا العكس. شاهد المعجم صفحة ٦٩ تطبيق تقابلي ومقالة التطبيق فقرة تطبيق التقابل يدلان على اجتماع التباين والغمر. التأنيث يتبع اسم دالة الذي يستعمله الكتاب؛ هذا تكييف نحوي معلل لا دعوى رأس معجمي حرفي. إحالة صفحة OLP-0036 الموروثة هي بدء القسم، ولم تتحول في هذه الدفعة إلى صفحة وقوع دقيقة.',
  'alternatives_ar':['تطبيق تقابلي شاهد معجمي، لكنه يغير اسم الكائن في الموضعين؛ لا يبدل منفردًا بلا مراعاة السياق','شاملة وحدها لا تعادل تقابلية؛ حذف شرط التباين يغير دلالة الصفة وإن استعمل البرهان الشمول لنفي وجود التقابل'],
  'expert_question_ar':'OLP-0029: التراثية PDF ص ٦٢، المعيارية ص ٦٦. OLP-0036: بدء القسم التراثي ص ٧٢ والمعياري ص ٧٦ فقط؛ استخدموا رابط السطر للفظ نفسه. هل يلائم تأنيث تقابلية اسم دالة؟ راجعوا أيضًا وضوح من باب أولى. الاختيار مفتوح للتصحيح.',
  'canon_limit_ar':'يعاد استعمال الشاهدين اللذين قرئا فعلًا في دفعة تعريفات الدوال؛ ليس ذلك ادعاء قراءة جديدة لكل مصادرهما. يثبتان الجذر والمفهوم لا العبارة المؤنثة حرفيًا. لا تصديق لسائر وقوعات التقابل في الكتاب.',
  'confidence_ar':'عالية في المعنى واتجاه الحجة والموافقة النحوية؛ الإحالة إلى OLP-0036 ليست دقيقة على مستوى الصفحة، وهذا قيد العثور لا شك رياضي. تقدير تحريري غير معاير.',
  'canon_evidence':[
   {'source_id':'DAM2018ENAR','physical_pdf_page':69,'printed_page':57,'entry':'bijective mapping','short_quote_ar':'تطبيق تقابلي','relation_ar':'شاهد سابق مقروء للجذر والصفة وشرطي التقابل'},
   {'source_id':'ARAB_ENC_APPLICATION_2747','section_ar':'أنواع التطبيقات / تطبيق التقابل','short_quote_ar':'تطبيق التقابل','full_consulted_passage_sha256':'18b66fdf796171f3ee15939838004884725e042f15cfb7a4acb8f41fe0a8e906','relation_ar':'فقرة سابقة مقروءة تجمع التباين والغمر، لا شاهد للتركيب المؤنث الكامل'},
  ],
 },
 'retro-0001-0150:glossary': {
  'sense_ar':'مرجع لألفاظ الكتاب وبيان معانيها، يذكره الأصل ضمن إضافات يخطط لها مستقبلًا؛ لا يقول إنه ملحق موجود الآن.',
  'rationale_ar':'أُبقي مسرد للمصطلحات بعد قراءة فقرة التعريف بالمشروع كاملة في الأصل والنسختين العربيتين. تصون نخطط لإضافة وأن يلحق به جهة الوعد المستقبلي. لا يلزم من لفظ معجم أنه مرجع رسمي محكم، وليس قائمة مصطلحات أطول بحسب عدد الكلمات؛ لذا حذفت هذين الترجيحين غير المثبتين من التعليل الجديد. تختار العبارة القائمة مرجعًا للمصطلحات في هذا السياق، لكن لم يتحقق هنا شاهد خارجي مقروء يرجحها على معجم مصطلحات. نتائج البحث عن صفحات رسمية لم تصبح شواهد بعد أن منع403 قراءة تلك الصفحات.',
  'alternatives_ar':['معجم مصطلحات بديل ممكن؛ لا يرفض بادعاء أنه مؤسسي أو محكم بالضرورة','قائمة مصطلحات بديل ممكن؛ قد تحتاج إلى توضيح اشتمالها على المعاني، ولا يرفض بادعاء طولها'],
  'expert_question_ar':'التراثية والمعيارية PDF ص ٢: هل مسرد للمصطلحات أوضح للقارئ من معجم مصطلحات؟ المقصود إضافة يعتزمها المشروع، لا ملحق حاضر. هذه المفاضلة مفتوحة للتصحيح ولا تستند بعد إلى شاهد عربي خارجي محقق.',
  'canon_limit_ar':'فحص سياقي وتحريري مع فجوة شاهد اصطلاحي خارجي صريحة. لا تقدم نتائج بحث ولا صفحة403 بوصفها مقروءة، ولا تدعي أن المعجم الرياضي يثبت glossary.',
  'confidence_ar':'عالية في الزمن والمعنى الأساسي لمطابقة الفقرة؛ مؤقتة في المفاضلة المعجمية لغياب شاهد خارجي مقروء في هذه الدفعة. تقدير تحريري غير معاير.',
  'canon_evidence':[],
 },
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def frozen_records(ids=None) -> list[dict]:
    digest=hashlib.sha256()
    with INDEX.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
    if digest.hexdigest().upper() != EXPECTED_INDEX:
        raise ValueError('Frozen index identity changed')
    return [r for r in iter_decisions(INDEX) if r['decision_id'] in (set(ids) if ids is not None else CHOICES)]


def witness(path: str, lo: int, hi: int, english: bool) -> dict:
    raw = ((ENGLISH if english else ROOT) / path).read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    passage = '\n'.join(lines[lo-1:hi])
    if not 1 <= lo <= hi <= len(lines):
        raise ValueError('Invalid personally selected range')
    return {'logical_path':path,'bytes':len(raw),'sha256':sha(raw),
        'line_start':lo,'line_end':hi,'exact_passage':passage,
        'passage_sha256':sha(passage.encode()),
        **({'public_lf_sha256':sha(raw.replace(b'\r\n',b'\n'))} if english else {})}


def prepare(data: dict) -> dict:
    """Bind manually authored ranges to bytes; this does not choose or read them."""
    out=copy.deepcopy(data)
    originals={r['decision_id']:r for r in frozen_records(out['finite_scope']['decision_ids'])}
    prior_path=ROOT/out['previous_ledger']
    prior_raw=prior_path.read_bytes()
    if sha(prior_raw)!=out['previous_ledger_sha256']:
        raise ValueError('Previous authored explanations changed')
    previous={r['decision_id']:r for r in json.loads(prior_raw)[out.get('previous_records_field','records')]}
    for row in out['records']:
        original=originals[row['decision_id']]
        row['original_occurrences']=copy.deepcopy(original['index_metadata']['occurrences'])
        row['previous_record']=copy.deepcopy(previous[row['decision_id']])
        row['open_to_correction']=True
        row['source_bindings']=[];row['target_bindings']=[]
        visited=set()
        for group in row['original_occurrences']:
            for loc in group['locations']:
                kind=loc['source_kind'];path=loc['logical_path']
                if (kind,path) in visited:continue
                visited.add((kind,path))
                relative=path if kind=='english' else path.split('/content/',1)[-1]
                if kind!='english':relative='content/'+relative
                lo,hi=out['personally_read_ranges'][relative][['english','msa','classical'].index(kind)]
                row['source_bindings' if kind=='english' else 'target_bindings'].append(witness(path,lo,hi,kind=='english'))
        row['fresh_location_bindings']={}
        if 'context_read_ranges' in row:
            row['context_bindings']=[]
            for spec in row['context_read_ranges']:
                w=witness(spec['logical_path'],spec['line_start'],spec['line_end'],spec['source_kind']=='english')
                w['source_kind']=spec['source_kind'];row['context_bindings'].append(w)
        for loc in (l for g in row['original_occurrences'] for l in g['locations']):
            spec=row.get('fresh_location_specs',{}).get(loc['location_id'])
            if not spec:continue
            w=witness(loc['logical_path'],spec['line_start'],spec['line_end'],loc['source_kind']=='english')
            row['fresh_location_bindings'][loc['location_id']]={
                k:w[k] for k in ['line_start','line_end','exact_passage','passage_sha256']}
            row['fresh_location_bindings'][loc['location_id']].update({k:v for k,v in spec.items() if k not in ['line_start','line_end']})
    return out


def transition_predecessor(t: dict, root: Path=ROOT) -> bytes:
    """An allowlisted prose change must invert to the frozen whole-file hash."""
    raw=(root/t['logical_path']).read_bytes()
    if sha(raw)!=t['after_sha256'] or len(raw)!=t['after_bytes']:
        raise ValueError('Source transition current identity changed')
    text=raw.decode('utf-8');inverse=text
    if not t['edits']:raise ValueError('Empty source transition')
    for edit in t['edits']:
        before,after=edit['before_text'],edit['after_text']
        if not before or not after or before==after or inverse.count(after)!=1:
            raise ValueError('Source transition is not uniquely invertible')
        inverse=inverse.replace(after,before,1)
    predecessor=inverse.encode('utf-8')
    if sha(predecessor)!=t['before_sha256'] or len(predecessor)!=t['before_bytes']:
        raise ValueError('Source transition inverse differs from frozen predecessor')
    if len(inverse.splitlines())!=len(text.splitlines()):
        raise ValueError('Source transition silently relocates lines')
    # Rule trees must stay byte-identical; the changes are prose, not schemata.
    import re
    pattern=r'\\begin\{(defish|prooftree)\}.*?\\end\{\1\}'
    old_blocks=re.findall(pattern,inverse,flags=re.S)
    new_blocks=re.findall(pattern,text,flags=re.S)
    old_full=[m.group() for m in re.finditer(pattern,inverse,flags=re.S)]
    new_full=[m.group() for m in re.finditer(pattern,text,flags=re.S)]
    if len(old_blocks)!=4 or old_blocks!=new_blocks or old_full!=new_full:
        raise ValueError('Source transition altered rule/derivation blocks')
    return predecessor


def inspected_bytes(data: dict, kind: str, path: str, root: Path, english: Path) -> bytes:
    full=(english if kind=='english' else root)/path
    if not full.is_file():
        full=root/BASE.relative_to(ROOT)/data.get('snapshot_subdir','reexamination-source')/('english' if kind=='english' else 'repo')/path
    return full.read_bytes()


def assess() -> dict:
    prior = json.loads((ROOT/'evidence/classical/terminology/SOL6_FUNCTION_DEFINITIONS_RECHECK_20260930.json').read_bytes())
    old = {r['decision_id']:r for r in json.loads(OLD.read_bytes())['records']}
    sources = copy.deepcopy(prior['canon_sources'])
    sources['DAM2018ENAR']['read_method_ar'] = 'قُرئت في هذه الدفعة الصور الكاملة لصفحات147/228/486/494/750؛ ويعاد استعمال شاهد69 المقروء في الدفعة السابقة. النقل من الصور الأصلية لا OCR وحده.'
    register = copy.deepcopy(prior['register_comparison'])
    register['personally_read_ids'] = ['canon-ibn-sina_00437','canon-ibn-sina_01161','optics-ibn-al-haytham_03352','muqaddima-ibn-khaldun_07592']
    register['consulted_arabic_passage_sha256'] = {
        'canon-ibn-sina_00437':'18167bb6fa6fd42519fda909e6a5e4ed9e46b1c85c579b87a5d77158b5819ffc',
        'canon-ibn-sina_01161':'36c82507d1b90da710f5fddbb5be0186e7430e3a5e91f35df8c30ce2695db48b',
        'optics-ibn-al-haytham_03352':'28f6e027795392712c2fb8d43f54940a2954a829864b5b2412eda32aee653018',
        'muqaddima-ibn-khaldun_07592':'4903e2e3c382ff3a5cb7bf431c4ea55e13e5f0168d35524638d2e30362e4383c'}
    register['relevance_ar'] = 'قرأنا الأزواج المحددة، ومنها فنقول ثم إنّا في canon-ibn-sina_00437، والتمييز بين حدود المعاني والاشتراط في الصفوف الأخرى. الأول فقط شاهد مباشر للبناء في قرار الآيل إلى صفر؛ ليس الباقي حجة معجمية لكل قرار.'
    rows=[]
    for frozen in frozen_records():
        identifier=frozen['decision_id']; row=copy.deepcopy(CHOICES[identifier])
        row.update({'decision_id':identifier,'surface_ar':old[identifier]['surface_ar'],
            'source_bindings':[],'target_bindings':[],
            'original_occurrences':copy.deepcopy(frozen['index_metadata']['occurrences']),
            'open_to_correction':True,'status_ar':'إبقاء معلل لاحق مفتوح للتصحيح؛ فجوات الشاهد ظاهرة',
            'previous_rationale_ar':old[identifier]['rationale_ar'],
            'previous_alternatives_ar':old[identifier]['alternatives_ar']})
        for group in row['original_occurrences']:
            for loc in group['locations']:
                kind=loc['source_kind']; path=loc['logical_path']
                logical=path.split('/content/',1)[-1] if kind!='english' else path.removeprefix('content/')
                ranges=RANGES['content/'+logical][['english','msa','classical'].index(kind)]
                field='source_bindings' if kind=='english' else 'target_bindings'
                row[field].append(witness(path,*ranges,kind=='english'))
        if identifier.endswith('7a619a6b3e5be629'):
            row['context_bindings']=[]
            for name,ranges in [('enumerability.tex',[(87,90),(113,116),(83,86),(108,112),(72,75),(94,97)]),('enumerability-alt.tex',[(39,43),(57,62),(37,41),(53,59),(25,27),(33,36)])]:
                for i,extent in enumerate(ranges):
                    kind=i//2; rel=SFR+'size-of-sets/'+name
                    path=rel if kind==0 else 'source/locale/'+('ar' if kind==1 else 'ar-classical')+'/'+rel
                    row['context_bindings'].append({'source_kind':['english','msa','classical'][kind],**witness(path,*extent,kind==0)})
        rows.append(row)
    return {'schema':'openlogic-arabic-contextual-recheck-v1','model':'GPT-6.1 Sol','effort':'Ultra',
        'assessed_on':'2026-09-30','source_index_sha256':EXPECTED_INDEX,
        'english_source_commit':prior['english_source_commit'],
        'arabic_source_commit':'a0f19b713fcc9a199e8bc71e16d171e1a858ba2f',
        'recording_mode':'fresh-retrospective-source-and-canon-assessment',
        'historical_intent_claimed':False,'source_edit_applied':False,'review_card':CARD,
        'scope_ar':'خمسة قرارات، سبعة مواضع مسجلة وواحد وعشرون موضعًا للأصل والترجمتين. صُحح تعليل المسرد غير المثبت، وفُصل التعداد المجموعاتي عن الحسابي، وأُبقي المتن الرياضي دون تغيير. ليس هذا تصديقًا لسائر القرارات أو لكل استعمالات هذه الألفاظ.',
        'source_identity_note_ar':'الوقوعات الموروثة محفوظة بلا زيادة أو حذف. التجزئات المعروضة تخص النسخ المقروءة محليًا؛ قد تكون نسخة الأصل المثبتة على الإنترنت مطابقة بايتًا أو تختلف بنهاياتCRLF/LF فقط، وتفصل إيصالات التنزيل ذلك. الصفحات موروثة من الربط المفحوص سابقًا؛ لم تجر هنا مقابلة مصورة جديدة لكل قارئ. موضع التقابل في OLP-0036 ذو صفحة بدء فقط، لا صفحة وقوع دقيقة.',
        'canon_sources':sources,'register_comparison':register,'records':rows}


def bind(data: dict, frozen: list[dict], root: Path=ROOT, english: Path=ENGLISH) -> dict:
    out=copy.deepcopy(data); originals={r['decision_id']:r for r in frozen}
    scope=out.get('finite_scope',{'decision_ids':list(CHOICES),'occurrence_groups':7,'source_locations':21})
    expected_ids=set(scope['decision_ids'])
    if set(originals)!=expected_ids or {r['decision_id'] for r in out['records']}!=expected_ids or len(out['records'])!=len(expected_ids):
        raise ValueError('Finite decision scope changed')
    transitions={t['logical_path']:t for t in out.get('source_transitions',[])}
    if len(transitions)!=len(out.get('source_transitions',[])):
        raise ValueError('Repeated source transition')
    for path,t in transitions.items():
        pins={l['current_sha256'].lower() for r in originals.values() for g in r['index_metadata']['occurrences'] for l in g['locations'] if l['logical_path']==path}
        if pins!={t['before_sha256']}:
            raise ValueError('Source transition not bound to frozen predecessor')
        transition_predecessor(t,root)
    groups=locations=0
    for row in out['records']:
        original=originals[row['decision_id']]
        if row['original_occurrences']!=original['index_metadata']['occurrences']:
            raise ValueError('Frozen occurrence identities changed')
        original_surface=original.get('review_display',{}).get('chosen_arabic') or original['chosen_arabic']
        old={r['decision_id']:r for r in json.loads(OLD.read_bytes())['records']}.get(row['decision_id'])
        if row['surface_ar']!=(old['surface_ar'] if old else original_surface):
            raise ValueError('Retention cannot substitute wording')
        witnesses=[]
        for field in ['source_bindings','target_bindings','context_bindings']:
            for w in row.get(field,[]):
                kind=('english' if field=='source_bindings' else w.get('source_kind') or ('classical' if '/ar-classical/' in w['logical_path'] else 'msa'))
                raw=inspected_bytes(out,kind,w['logical_path'],root,english)
                passage='\n'.join(raw.decode('utf-8-sig').splitlines()[w['line_start']-1:w['line_end']])
                if len(raw)!=w['bytes'] or sha(raw)!=w['sha256'] or passage!=w['exact_passage'] or sha(passage.encode())!=w['passage_sha256']:
                    raise ValueError('Changed inspected source passage')
                if field!='context_bindings':witnesses.append((kind,w))
        checked=[]
        actual_ids={l['location_id'] for g in row['original_occurrences'] for l in g['locations']}
        if set(row.get('fresh_location_bindings',{}))-actual_ids:
            raise ValueError('Invented fresh occurrence identity')
        for occurrence in row['original_occurrences']:
            groups+=1
            if set(l['source_kind'] for l in occurrence['locations'])!={'classical','english','msa'}:
                raise ValueError('Uninspected additional or missing location')
            for loc in occurrence['locations']:
                c=loc['line_reconciliation'];fresh=row.get('fresh_location_bindings',{}).get(loc['location_id'])
                a=fresh['line_start'] if fresh else c['current_line_start'];b=fresh['line_end'] if fresh else c['current_line_end']
                if a is None or b is None:raise ValueError('Missing explicit new context for unresolved locator')
                matches=[w for k,w in witnesses if k==loc['source_kind'] and w['logical_path']==loc['logical_path'] and w['line_start']<=a<=b<=w['line_end']]
                if (not c['resolved'] and not fresh) or len(matches)!=1:raise ValueError('Occurrence not contained in read context')
                w=matches[0];raw=inspected_bytes(out,loc['source_kind'],loc['logical_path'],root,english)
                excerpt='\n'.join(raw.decode('utf-8-sig').splitlines()[a-1:b])
                # The frozen token may be a substring of its full source line.
                # Require BOTH the exact recorded full line and contained token.
                token=loc['excerpt'].replace('\r\n','\n').strip()
                transition=transitions.get(loc['logical_path'])
                expected_file=transition['after_sha256'] if transition else loc['current_sha256'].lower()
                if sha(raw)!=expected_file:raise ValueError('Frozen source drift without explicit transition')
                if fresh:
                    if excerpt!=fresh['exact_passage'] or sha(excerpt.encode())!=fresh['passage_sha256'] or not fresh.get('reason_ar'):raise ValueError('Explicit context binding changed')
                elif excerpt!=loc['current_excerpt'] or token not in excerpt:raise ValueError('Frozen locator mismatch')
                checked.append({'location_id':loc['location_id'],'source_kind':loc['source_kind'],'logical_path':loc['logical_path'],'line_start':a,'line_end':b,'exact_passage':excerpt,'file_sha256':w['sha256'],'page_evidence':copy.deepcopy(loc['page_evidence']),**({'binding_reason_ar':fresh['reason_ar'],'literal_term_in_english':fresh.get('literal_term_in_english')} if fresh else {})})
                locations+=1
        row['checked_occurrences']=checked
    if (groups,locations)!=(scope['occurrence_groups'],scope['source_locations']):raise ValueError('Finite context coverage changed')
    return out


def source_url(data: dict, kind: str, path: str, lo: int, hi: int) -> str:
    if any(t['logical_path']==path for t in data.get('source_transitions',[])):
        # Link to this assessment's corresponding editable successor, never
        # mislabel the pinned PREDECESSOR as containing corrected prose.
        return f'../../{path}#L{lo}-L{hi}'
    commit=data['english_source_commit'] if kind=='english' else data['arabic_source_commit']
    repo='OpenLogicProject/OpenLogic' if kind=='english' else 'KokunoYumeto/OpenLogic-ar'
    return f'https://github.com/{repo}/blob/{commit}/{path}#L{lo}-L{hi}'


def render(data: dict) -> str:
    lines=[data.get('heading_ar','# مقابلة خمسة اختيارات في سياقاتها — ٣٠ سبتمبر ٢٠٢٦'),'','[مدخل المراجعة](INDEX_AR.md) · [القائمة الكاملة](DIRECTORY_READABLE_AR.md)','',data['scope_ar'],'',
        'OpenAI Codex — GPT-6.1 Sol، جهد Ultra: المقابلة والتعليل الجديدان. التعليلات السابقة لـOpenAI Codex — GPT-6 Sol، جهد Ultra، محفوظة في [الدفعة السابقة]('+data.get('previous_review_card','BATCH_31_38_AR.md')+'). لا تنسب المقابلة إلى مراجع بشري أو إلى دوافع تاريخية مجهولة.','',data['source_identity_note_ar'],'']
    if data.get('source_transitions'):
        lines+=['## التصحيحات في المتن','',
                'الحالة الآتية محفوظة من وقت المقابلة الأولى قبل إعادة بناء القارئين؛ '
                'راجع [مدخل القراءة](INDEX_AR.md) لحالة PDF وEPUB الحالية.','',
                data['body_corrections_ar'],'']
        for t in data['source_transitions']:
            lines+=['- [المصدر المصحح الموافق لهذه البطاقة]('+source_url(data,'msa',t['logical_path'],57,59)+')؛ السابق SHA-256 `'+t['before_sha256']+'`؛ المصحح `'+t['after_sha256']+'`.','']
    for row in data['records']:
        lines+=['## '+row.get('review_heading_ar',row['surface_ar']),'','معرّف القرار: `'+row['decision_id']+'`.','','**أين وما الذي يراجع؟** '+row['expert_question_ar'],'','**المعنى:** '+row['sense_ar'],'','**لماذا أُبقي؟** '+row['rationale_ar'],'','**البدائل:** '+'؛ '.join(row['alternatives_ar']),'','**الثقة وحدود الشاهد:** '+row['confidence_ar']+' '+row['canon_limit_ar'],'']
        for e in row['canon_evidence']:
            s=data['canon_sources'][e['source_id']];place=e.get('section_ar') or 'PDF ص '+str(e['physical_pdf_page']).translate(EAST)+'؛ المطبوع '+str(e['printed_page']).translate(EAST)+'؛ '+e['entry']
            lines+=['- ['+s['title_ar']+']('+s['url']+')، '+place+': «'+e['short_quote_ar']+'». '+e['relation_ar']]
        lines+=['','**جميع مواضع الأصل والترجمتين:**','']
        for group in row['original_occurrences']:
            lines+=['### '+group['unit']['unit_id'],'']
            for loc in group['locations']:
                checked=next(c for c in row['checked_occurrences'] if c['location_id']==loc['location_id'])
                kind=loc['source_kind'];a=checked['line_start'];b=checked['line_end']
                label={'english':'الأصل الإنجليزي','msa':'المعيارية — الدولية والمشرق','classical':'التراثية'}[kind]
                url=source_url(data,kind,loc['logical_path'],a,b)
                pages=[]
                for p in loc['page_evidence']:
                    pages.append(p['reader']+': PDF ص '+','.join(str(n).translate(EAST) for n in p['pdf_pages'])+(' — بدء القسم فقط، ليس وقوع اللفظ' if not p['exact_occurrence_page'] else ' — وقوع دقيق بحسب الربط الموروث'))
                lines+=['- ['+label+'، سطر '+str(a).translate(EAST)+']('+url+')'+('؛ '+' · '.join(pages) if pages else ''),'',*([checked['binding_reason_ar'],''] if 'binding_reason_ar' in checked else []),'```tex',checked['exact_passage'],'```','']
        lines+=['**السياقات المقروءة:**','']
        for field in ['source_bindings','target_bindings','context_bindings']:
            for w in row.get(field,[]):
                is_en=field=='source_bindings' or w.get('source_kind')=='english'
                url=source_url(data,'english' if is_en else 'msa',w['logical_path'],w['line_start'],w['line_end'])
                lines+=['- ['+('الأصل' if is_en else 'التراثية' if '/ar-classical/' in w['logical_path'] else 'المعيارية')+'، '+Path(w['logical_path']).name+'، الأسطر '+str(w['line_start']).translate(EAST)+'–'+str(w['line_end']).translate(EAST)+']('+url+')؛ SHA-256 للنسخة المقروءة محليًا: `'+w['sha256']+'`.']
        lines+=['']
    lines+=['## حدود القراءة','',data['register_comparison']['relevance_ar']+' '+data['register_comparison']['limits_ar'],'',
        '[الموسوعة: هوية المقارنة السابقة](SOL6_FUNCTION_DEFINITIONS_AR.md). لا تنشر هذه البطاقة صفحات المعجم أو الموسوعة أو أزواج النصوص التراثية الكاملة، ولا تتخذ نتائج البحث غير المقروءة شاهدًا. سجل JSON يحفظ النصوص المصدرية المحددة والتجزئات والوقوعات الأصلية والتعليل السابق. كل اختيار مفتوح للتصحيح؛ لا تنتظر عملية الإنتاج استجابة المراجع.','']
    return '\n'.join(lines)


def capture_public_sources(data: dict) -> None:
    """Bounded pinned downloads, including the referenced enumeration definitions."""
    witnesses={}
    for row in data['records']:
        for field in ['source_bindings','target_bindings','context_bindings']:
            for w in row.get(field,[]):
                is_en=field=='source_bindings' or w.get('source_kind')=='english'
                witnesses[(is_en,w['logical_path'])]=w
    files=[]
    transitions={t['logical_path']:t for t in data.get('source_transitions',[])}
    for (is_en,relative),w in sorted(witnesses.items()):
        repo='OpenLogicProject/OpenLogic' if is_en else 'KokunoYumeto/OpenLogic-ar'
        commit=data['english_source_commit'] if is_en else data['arabic_source_commit']
        url=f'https://raw.githubusercontent.com/{repo}/{commit}/{relative}'
        with urlopen(Request(url,headers={'User-Agent':'OpenLogic-Ar source verification'}),timeout=30) as response:
            raw=response.read(65537)
        local=((ENGLISH if is_en else ROOT)/relative).read_bytes()
        transition=transitions.get(relative)
        public_expected=transition_predecessor(transition) if transition else local
        allowed={transition['before_sha256']} if transition else {w['sha256'],w.get('public_lf_sha256',w['sha256'])}
        equal=(public_expected.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')) if is_en else public_expected==raw
        if len(raw)>65536 or sha(raw) not in allowed or not equal:
            raise ValueError('Pinned public source mismatch: '+relative)
        snapshot=BASE/data.get('snapshot_subdir','reexamination-source')/('english' if is_en else 'repo')/relative
        if snapshot.exists() and snapshot.read_bytes()!=local:raise ValueError('Different immutable witness exists')
        snapshot.parent.mkdir(parents=True,exist_ok=True);snapshot.write_bytes(local)
        files.append({'url':url,'public_bytes':len(raw),'public_sha256':sha(raw),
            'snapshot_path':snapshot.relative_to(ROOT).as_posix(),'snapshot_bytes':len(local),
            'snapshot_sha256':sha(local),'only_crlf_lf_difference':is_en and local!=raw,
            **({'public_represents':'frozen-predecessor-not-current-correction','inverse_predecessor_sha256':sha(public_expected)} if transition else {})})
    expected_files=data.get('finite_scope',{}).get('public_source_files',24)
    payload=(json.dumps({'status':f'PASS_{expected_files}_ANONYMOUS_PINNED_CONTEXT_SOURCE_FILES','files':files,
        'ledger_sha256':sha(LEDGER.read_bytes())},ensure_ascii=False,indent=2)+'\n').encode()
    if len(files)!=expected_files:raise ValueError('Context source-file scope changed')
    receipt=BASE/data.get('source_readback_receipt','CONTEXTUAL_SOURCE_READBACK_20260930.json')
    if receipt.exists() and receipt.read_bytes()!=payload:raise ValueError('Different historical receipt exists')
    receipt.write_bytes(payload)


def main() -> None:
    global LEDGER
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--initialize',action='store_true');p.add_argument('--prepare',action='store_true');p.add_argument('--capture-public-sources',action='store_true');p.add_argument('--ledger',type=Path);args=p.parse_args()
    if args.ledger is not None:LEDGER=args.ledger.resolve();LEDGER.relative_to(ROOT)
    if args.initialize and LEDGER.exists():raise ValueError('Existing assessment must not be silently replaced')
    data=assess() if args.initialize else json.loads(LEDGER.read_bytes())
    if args.prepare:data=prepare(data)
    ids=data.get('finite_scope',{}).get('decision_ids')
    bound=bind(data,frozen_records(ids));machine=(json.dumps(bound,ensure_ascii=False,indent=2)+'\n').encode();card=render(bound).encode()
    card_path=BASE/bound['review_card']
    if args.check:
        if LEDGER.read_bytes()!=machine or card_path.read_bytes()!=card:raise ValueError('Assessment not reproducible')
    else:LEDGER.write_bytes(machine);card_path.write_bytes(card)
    if args.capture_public_sources:capture_public_sources(bound)
    print(json.dumps({'status':'PASS_CONTEXTUAL_CHOICES','decisions':len(bound['records']),'occurrence_groups':sum(len(r['original_occurrences']) for r in bound['records']),'source_locations':sum(len(r['checked_occurrences']) for r in bound['records']),'body_changes':len(bound.get('source_transitions',[])),'ledger_sha256':sha(machine),'card_sha256':sha(card)}))


if __name__=='__main__':main()

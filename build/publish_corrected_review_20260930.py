"""Publish one checked correction batch, not a claim of full Sol6 re-review."""
import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys

import requests
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE))
import publish_classical_reader_20260926 as zenodo
import publish_arabic_review_359_github_20260927 as git_publication
from review_sol6_epub_20260930 import identity,require

ROOT=HERE.parent
BASE=ROOT/'expert-review/2026-09-26-final-page-review'
STATE=ROOT/'evidence/publication/review-corrections-20260930'
STAGE=ROOT/'output/release/review-corrections-20260930'
TAG='ar-openlogic-translation-review-corrections-20260930'
REMOTE='KokunoYumeto/OpenLogic-ar'
GITHUB=f'https://github.com/{REMOTE}/releases/tag/{TAG}'
ENTRY=f'https://github.com/{REMOTE}/blob/{TAG}/expert-review/2026-09-26-final-page-review/INDEX_AR.md'
FULL=ENTRY.replace('INDEX_AR.md','DIRECTORY_AR.md')
NAMES=('INDEX_AR.md','DIRECTORY_AR.md','DECISION_RECORD_AR.jsonl.gz',
       'SOL6_CORRECTIONS_AR.md','SOL6_SOURCE_REFERENCES_AR.md',
       '90-ARABIC-REVIEW-COMPLETE-SOURCE.zip','90-ARABIC-REVIEW-SHA256SUMS.txt')
REPLACED=('INDEX_AR.md','DIRECTORY_AR.md','DECISION_RECORD_AR.jsonl.gz',
          '90-ARABIC-REVIEW-COMPLETE-SOURCE.zip','90-ARABIC-REVIEW-SHA256SUMS.txt')
TITLE='المنطق المفتوح بالعربية: تصحيح خمسة شروح وإحالات ٣٢ قرارًا في دليل المراجعة'
COLD_RECEIPT='CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930.json'
READABLE=False
FUNCTION_RECHECK=False
CONTEXT_RECHECK=False
CURRENT_MSA=False
ASSET_INPUTS={}
ORIGINAL_NAMES=NAMES
CURRENT_MSA_SOURCE_ROOT=None
CURRENT_PDF_ROOT=ROOT/'output/pdf/msa-quantifier-reference-items-20260930'
STRUCTURAL_RECEIPT='COMPLETE_INDEPENDENT_READBACK_20260930_R3.json'
NOTES=(f'## دليل المراجعة العربية المصحح\n\n[ابدأ من هنا]({ENTRY}) · [القائمة الكاملة]({FULL})\n\n'
       'يضم الدليل ١٠٩٥ اختيارًا مسجلًا مع ألفاظها ومواضعها وتعليلاتها وأسئلة للمختصين. '
       'صُحِّح قيد قابلية الحساب في شرح قابلية المحورة، ومعنى التجاوز في هذه الوحدة، '
       'والمختزلات والتوسيعات في نظرية النماذج التي خلطها الشرح بحساب لامبدا. '
       'واستُبدلت ٥٩ إحالة إلى تعليقات أسماء الأقسام، في ٣٢ قرارًا، بمقاطع مقروءة من الأصل. '
       'متن الكتب لا يتغير بهذه الدفعة؛ كانت التعريفات المعنية صحيحة فيه بالفعل.\n\n'
       'حُفظت جميع الوقوعات والبطاقات القديمة وتاريخ التصحيح. تضم حزمة المصادر ملفات الدليل '
       'وبطاقاته وبياناته وبرامج بنائه، والملفات الأصلية المحددة اللازمة لإعادة بناء هذه التصحيحات. '
       'طابقت المقابلة ملفات الأصل والترجمة الـ٤٤ بتنزيلاتها المثبتة، '
       'وأعاد اختبار بارد من الحزمة الفعلية إنتاج البطاقات المصححة والدليل والسجل حرفيًا.\n\n'
       'الترجمة والتعليلات الموروثة: OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra. '
       'التعليلات العربية اللاحقة والفهرسة: OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. '
       'المقابلة والتصحيحات المحددة وهذه الدفعة: OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. '
       'لم تقع مراجعة بشرية شاملة. إعادة فحص فترة GPT-6 Sol كلها ما زالت جارية؛ '
       'هذه الدفعة لا تدعي تصديق كل تعليل أو شاهد معجمي، ولا تستعيد دوافع المترجم الأول.\n\n'
       '[القارئ التراثي PDF ومصدر لاتخ المباشر وحزمة المصدر الكامل](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-classical-eastern-rtl-fn-unicode-20260928) · '
       '[الكتب الإلكترونية الثلاثة ومصادرها](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-epub-provenance-correction-20260930).\n')


def stage():
    if CURRENT_MSA:
        check_current_msa()
    fresh=json.loads((BASE/STRUCTURAL_RECEIPT).read_bytes())
    cold=json.loads((BASE/COLD_RECEIPT).read_bytes())
    require(fresh['all_frozen_occurrences_preserved'] and fresh['verified_machine_records']==1095,'Fresh structural checks differ')
    archive=identity(BASE/NAMES[-2])
    require(cold['status']=='PASS_COLD_REPLAY_FROM_EXACT_CORRECTED_REVIEW_ZIP' and cold['source_zip_sha256']==archive['sha256'],'Cold source replay differs')
    for name,sha in cold['byte_identical_outputs'].items():
        require(identity(BASE/name)['sha256']==sha,'Cold-replayed output changed')
    require(identity(BASE/'DIRECTORY_AR.md')['sha256'].upper()==fresh['directory_sha256'] and
            identity(BASE/'DECISION_RECORD_AR.jsonl.gz')['sha256'].upper()==fresh['machine_record_sha256'],
            'Fresh directory/ledger identities differ')
    require(not STAGE.exists() and not STATE.exists(),'Existing publication state must be inspected')
    hashes=[{**identity(ASSET_INPUTS.get(name,BASE/name)),'file':name} for name in NAMES[:-1]]
    (BASE/NAMES[-1]).write_text(''.join(r['sha256']+'  '+r['file']+'\n' for r in hashes),encoding='utf-8',newline='\n')
    STAGE.mkdir(parents=True); STATE.mkdir(parents=True)
    rows=[]
    for name in NAMES:
        source=ASSET_INPUTS.get(name,BASE/name)
        row=identity(source); rows.append({'name':name,'bytes':row['bytes'],'sha256':row['sha256']})
        shutil.copy2(source,STAGE/name)
    zenodo.save(STATE/'STAGE.json',{'status':'PASS_CURRENT_CORRECTED_REVIEW_STAGE','files':rows})
    (STATE/'RELEASE_NOTES_AR.md').write_text(NOTES,encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PASS_CURRENT_CORRECTED_REVIEW_STAGE','files':len(rows)}))


def assets():
    rows=json.loads((STATE/'STAGE.json').read_bytes())['files']
    for r in rows:
        require(identity(STAGE/r['name'])=={'file':r['name'],'bytes':r['bytes'],'sha256':r['sha256']},'Accepted stage changed')
    return rows


def selected_files():
    base=BASE.relative_to(ROOT)
    paths=[(base/name).as_posix() for name in NAMES if name not in ASSET_INPUTS]
    paths.extend((base/name).as_posix() for name in (
        'README_BUILD_AR.md','COMPLETE_DIRECTORY_RECEIPT.json','COMPLETE_SOURCE_PACKAGE_RECEIPT.json',
        'COMPLETE_DIRECTORY_RECEIPT_20260927_HISTORICAL.json','COMPLETE_INDEPENDENT_READBACK_20260930_R3.json',
        'SOURCE_WITNESS_PUBLIC_READBACK_20260930.json','CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930.json'))
    paths.extend(p.relative_to(ROOT).as_posix() for p in (BASE/'reexamination-source').rglob('*') if p.is_file())
    paths.extend('evidence/classical/terminology/'+name for name in (
        'SOL6_REEXAMINATION_CORRECTIONS_20260930.json','SOL6_SOURCE_WITNESS_CORRECTIONS_20260930.json',
        'SOL6_COMMENT_ONLY_WITNESS_CENSUS_20260930.json'))
    paths.extend('build/'+name for name in (
        'assemble_complete_arabic_review.py','verify_complete_arabic_review.py','package_complete_arabic_review.py',
        'render_sol6_review_corrections_20260930.py','correct_added_source_witnesses_20260930.py',
        'replay_corrected_review_20260930.py','publish_corrected_review_20260930.py',
        'publish_arabic_review_359_github_20260927.py','publish_classical_reader_20260926.py',
        'review_sol6_epub_20260930.py','package_reviewed_epubs_20260930.py','publish_reviewed_epubs_20260930.py',
        'tests/test_source_witness_corrections_20260930.py','tests/test_publish_reviewed_epubs_20260930.py',
        'tests/test_review_sol6_epub_20260930.py','tests/test_recovered_review_witnesses_20260930.py'))
    if READABLE:
        paths.extend((base/name).as_posix() for name in (
            'DIRECTORY_READABLE_AR.md','READABLE_REVIEW_RECEIPT_20260930.json',
            'READABLE_REVIEW_VERIFICATION_20260930.json',COLD_RECEIPT))
        paths.extend(p.relative_to(ROOT).as_posix() for p in (BASE/'readable-review').glob('*.md'))
        paths.extend('build/'+name for name in (
            'render_readable_review_20260930.py','verify_readable_review_20260930.py',
            'tests/test_readable_review_20260930.py','tests/test_publish_corrected_review_20260930.py'))
    if FUNCTION_RECHECK:
        paths.extend((base/name).as_posix() for name in (
            STRUCTURAL_RECEIPT,'SOL6_FUNCTION_DEFINITIONS_AR.md',
            'FUNCTION_DEFINITION_SOURCE_READBACK_20260930.json'))
        paths.append('evidence/classical/terminology/SOL6_FUNCTION_DEFINITIONS_RECHECK_20260930.json')
        paths.extend('build/'+name for name in (
            'render_function_definition_recheck_20260930.py','tests/test_function_definition_recheck_20260930.py',
            'verify_readable_review_public_20260930.py'))
    if CONTEXT_RECHECK:
        paths.extend((base/name).as_posix() for name in (
            'SOL6_CONTEXTUAL_CHOICES_AR.md','SOL6_PROOF_QUANTIFICATION_AR.md',
            'CONTEXTUAL_SOURCE_READBACK_20260930.json','PROOF_QUANTIFICATION_SOURCE_READBACK_20260930.json',
            'COMPLETE_INDEPENDENT_READBACK_20260930_R5.json'))
        paths.extend(p.relative_to(ROOT).as_posix() for p in (BASE/'reexamination-source-proof-quantification').rglob('*') if p.is_file())
        paths.extend('evidence/classical/terminology/'+name for name in (
            'SOL6_CONTEXTUAL_RECHECK_20260930.json','SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json'))
        paths.extend('build/'+name for name in (
            'render_contextual_recheck_20260930.py','tests/test_contextual_recheck_20260930.py'))
        paths.append('source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex')
    if CURRENT_MSA:
        paths.extend((base/name).as_posix() for name in (
            'SOL6_FREE_BOUND_VARIABLE_AR.md','FREE_BOUND_VARIABLE_SOURCE_READBACK_20260930.json',
            STRUCTURAL_RECEIPT,COLD_RECEIPT))
        paths.extend(p.relative_to(ROOT).as_posix() for p in (BASE/'reexamination-source-free-bound-variable').rglob('*') if p.is_file())
        paths.extend('evidence/classical/terminology/'+name for name in (
            'SOL6_FREE_BOUND_VARIABLE_RECHECK_20260930.json','SOL6_ARABIC_REFERENCE_LOCALIZATION_20260930.json'))
        paths.extend(['README.md','source/locale/ar/open-logic-locale.sty',
            'source/locale/ar/open-logic-complete-ar.tex','source/locale/ar/open-logic-closure-supplement-ar.tex',
            'evidence/provenance/openlogic-control/CLOSURE_MANIFEST.csv',
            'evidence/provenance/openlogic-control/MSA_CLOSURE_MANIFEST_REBIND_20260930_FORMULA_ANNOTATED.json',
            'evidence/msa-source-successor-20260930/EFFECTIVE_BUILD_MANIFEST.json'])
        import prepare_editable_source_deliverables as source_export
        paths.extend(p.relative_to(ROOT).as_posix() for p in (ROOT/source_export.CURRENT_MSA_GRAPH_ROOT).glob('*.json'))
        paths.extend('build/'+name for name in (
            'BUILD_DUAL_NOTATION.ps1','BUILD_DUAL_NOTATION_INNER.ps1','profile_checkpoint.py',
            'repair_rtl_link_rects_letter_ar.py','qa_dual_notation_pdfs.py','rebind_msa_closure_manifest.py',
            'prepare_editable_source_deliverables.py','assemble_complete_722_tex.py',
            'tests/test_letter_rtl_link_repair.py','tests/test_msa_build_route.py',
            'tests/test_rebind_msa_closure_manifest.py','tests/test_prepare_editable_source_deliverables.py'))
        # Rendered books and their complete ZIPs are release assets, not large
        # Git blobs. All changed modular sources and reconstruction code are
        # committed here; the exact full editable bundles remain direct assets.
        paths=list(dict.fromkeys(paths))
    require(len(paths)==len(set(paths)) and all((ROOT/p).is_file() for p in paths),'Selected source inventory differs')
    return paths


def github_release():
    state=json.loads((STATE/'GITHUB_TRANSACTION.json').read_bytes())
    require(state['status']=='PASS_ANONYMOUS_GITHUB_READBACK','Git source commit is not publicly verified')
    probe=requests.get(f'https://api.github.com/repos/{REMOTE}/releases/tags/{TAG}',timeout=(20,60))
    require(probe.status_code==404,'Release exists or absence is unproved')
    result=subprocess.run(['gh','release','create',TAG,'--repo',REMOTE,'--target',state['commit'],
                           '--title',TITLE,'--notes-file',str(STATE/'RELEASE_NOTES_AR.md')]+[str(STAGE/r['name']) for r in assets()],capture_output=True,text=True)
    require(result.returncode==0,'Release creation failed; inspect before bounded retry')
    print(GITHUB)


def github_verify():
    result=requests.get(f'https://api.github.com/repos/{REMOTE}/releases/tags/{TAG}',timeout=(20,60)); result.raise_for_status()
    public=result.json(); require(not public['draft'],'Release is not public')
    entries={r['name']:r for r in public['assets']}; rows=assets(); checked=[]
    require(set(entries)=={r['name'] for r in rows},'Public asset inventory differs')
    with requests.Session() as anonymous:
        anonymous.trust_env=False
        for row in rows:
            h=hashlib.sha256(); count=0
            with anonymous.get(entries[row['name']]['browser_download_url'],stream=True,timeout=(20,90)) as response:
                require(response.status_code==200,'Anonymous release download failed')
                for block in response.iter_content(1048576):
                    count+=len(block); require(count<=row['bytes'],'Oversized public asset'); h.update(block)
            require((count,h.hexdigest())==(row['bytes'],row['sha256']),'Anonymous asset identity differs')
            checked.append({**row,'anonymous':True,'url':entries[row['name']]['browser_download_url']})
    zenodo.save(STATE/'GITHUB_READBACK.json',{'status':'PASS_ANONYMOUS_GITHUB_READBACK','release':GITHUB,'files':checked})
    print(json.dumps({'status':'PASS_ANONYMOUS_GITHUB_READBACK','files':len(checked)}))


def configure(readable=False,function_recheck=False,context_recheck=False):
    global READABLE,FUNCTION_RECHECK,CONTEXT_RECHECK,TAG,GITHUB,ENTRY,FULL,STAGE,STATE,TITLE,NOTES,COLD_RECEIPT,REPLACED,STRUCTURAL_RECEIPT
    READABLE=readable
    FUNCTION_RECHECK=function_recheck
    CONTEXT_RECHECK=context_recheck
    if readable:
        TAG='ar-openlogic-translation-review-readable-20260930'
        GITHUB=f'https://github.com/{REMOTE}/releases/tag/{TAG}'
        ENTRY=f'https://github.com/{REMOTE}/blob/{TAG}/expert-review/2026-09-26-final-page-review/INDEX_AR.md'
        FULL=ENTRY.replace('INDEX_AR.md','DIRECTORY_READABLE_AR.md')
        STAGE=ROOT/'output/release/review-readable-20260930'
        STATE=ROOT/'evidence/publication/review-readable-20260930'
        TITLE='المنطق المفتوح بالعربية: دليل المراجعة الكامل في صفحات قابلة للقراءة'
        NOTES=(f'## مراجعة اختيارات الترجمة العربية\n\n[ابدأ من هنا]({ENTRY}) · [القائمة الكاملة]({FULL})\n\n'
               'حُفظت جميع القرارات الـ١٠٩٥ ووقوعاتها وتعليلاتها. قُسِّم جدول البحث والبطاقات الكبيرة '
               'إلى صفحات قصيرة متصلة، مع حفظ الجدول والبطاقات الكاملة للتنزيل. لا يغيّر التقسيم '
               'النصوص أو أسباب الاختيار؛ يتيح قراءتها على الإنترنت من غير الاعتماد على عرض الملفات الكبيرة.\n\n'
               'تشمل هذه النسخة التصحيحات الخمسة للشروح الرياضية وإصلاح ٥٩ إحالة في ٣٢ قرارًا. '
               'متن الكتب لم يتغير بهذه الدفعة. تضم حزمة المصدر جميع الصفحات والبيانات والشيفرة '
               'والشواهد المحددة، وأعيد منها إنتاج الدليل والبطاقات وصفحات القراءة حرفيًا.\n\n'
               'الترجمة والتعليلات الموروثة: OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra. '
               'التعليلات اللاحقة والفهرسة: OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. '
               'المقابلة والتصحيحات المحددة وإصلاح الوصول: OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. '
               'لم تقع مراجعة بشرية شاملة؛ إعادة فحص الفترة كلها ما زالت جارية، '
               'ولا يثبت هذا الإصدار صحة كل تعليل أو شاهد معجمي. كل اختيار قابل للتصحيح.\n\n'
               '[PDF التراثي ومصدر لاتخ المباشر وحزمة المصدر](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-classical-eastern-rtl-fn-unicode-20260928) · '
               '[EPUB للطبعات الثلاث ومصادره](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-epub-provenance-correction-20260930).\n')
        COLD_RECEIPT='CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930_R2.json'
    if function_recheck:
        require(readable,'Function assessments retain the complete readable presentation')
        TAG='ar-openlogic-function-definitions-review-20260930'
        GITHUB=f'https://github.com/{REMOTE}/releases/tag/{TAG}'
        ENTRY=f'https://github.com/{REMOTE}/blob/{TAG}/expert-review/2026-09-26-final-page-review/INDEX_AR.md'
        FULL=ENTRY.replace('INDEX_AR.md','DIRECTORY_READABLE_AR.md')
        STAGE=ROOT/'output/release/review-function-definitions-20260930'
        STATE=ROOT/'evidence/publication/review-function-definitions-20260930'
        STRUCTURAL_RECEIPT='COMPLETE_INDEPENDENT_READBACK_20260930_R4.json'
        COLD_RECEIPT='CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930_R3.json'
        REPLACED=NAMES
        TITLE='المنطق المفتوح بالعربية: شواهد جديدة لثلاثة تعريفات للدوال في سجل المراجعة'
        card=ENTRY.replace('INDEX_AR.md','SOL6_FUNCTION_DEFINITIONS_AR.md')
        NOTES=(f'## اختيارات الترجمة العربية: مقابلة ثلاثة تعريفات للدوال\n\n[ابدأ من هنا]({ENTRY}) · [القائمة الكاملة]({FULL}) · [النتائج الجديدة ومواضعها]({card})\n\n'
               'يضم الدليل جميع القرارات الـ١٠٩٥ ووقوعاتها. قُرئت تعريفات الدوال المتباينة والشاملة والتقابلية '
               'في الأصل والترجمتين، وصفحات المعجم الأصلية ومقالة رياضية للموسوعة العربية. '
               'أضيف شاهد مستقل للتباين، وبقي الخلاف بين شاملة واللفظ المثبت غامر صريحًا. '
               'المقارنة التراثية أسلوبية محدودة ولا تثبت هذه المصطلحات الحديثة. '
               'هذه ثلاثة قرارات وتسعة مواضع محددة، لا شهادة على سائر استعمالات الأسرة أو الكتاب كله. '
               'أُبقي متن الطبعات الثلاث؛ لم تضف هذه الدفعة تغييرًا إلى PDF أو EPUB.\n\n'
               'بقيت التصحيحات الخمسة السابقة وإصلاح ٥٩ إحالة في ٣٢ قرارًا، والصفحات القصيرة '
               'والملفات الكاملة والتاريخ المنشور. تضم حزمة المصدر البطاقة الجديدة وشواهد التعريفات '
               'وبياناتها وشيفرة بنائها، وقد أعادت الحزمة الفعلية إنتاج العرض والبيانات حرفيًا. '
               'لا تشمل الحزمة المقالة المحمية أو الأزواج التراثية الكاملة.\n\n'
               'الترجمة والتعليلات الموروثة: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. '
               'التعليلات اللاحقة والفهرسة: OpenAI Codex — GPT-6 Sol، جهد Ultra. '
               'المقابلة الجديدة والتعليل اللاحق وإصلاح العرض: OpenAI Codex — GPT-6.1 Sol، جهد Ultra. '
               'لم تقع مراجعة بشرية شاملة؛ إعادة فحص الفترة كلها ما زالت جارية. '
               'كل اختيار قابل للتصحيح، ولا يدعي التعليل اللاحق استعادة دافع المترجم الأول.\n\n'
               '[PDF التراثي ولاتخ المباشر وحزمة المصدر](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-classical-eastern-rtl-fn-unicode-20260928) · '
               '[EPUB للطبعات الثلاث ومصادره](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-epub-provenance-correction-20260930).\n')
    if context_recheck:
        require(readable and function_recheck,'Context assessment preserves the previous checked layers')
        TAG='ar-openlogic-context-and-proof-review-20260930'
        GITHUB=f'https://github.com/{REMOTE}/releases/tag/{TAG}'
        ENTRY=f'https://github.com/{REMOTE}/blob/{TAG}/expert-review/2026-09-26-final-page-review/INDEX_AR.md'
        FULL=ENTRY.replace('INDEX_AR.md','DIRECTORY_READABLE_AR.md')
        STAGE=ROOT/'output/release/review-context-and-proof-20260930'
        STATE=ROOT/'evidence/publication/review-context-and-proof-20260930'
        STRUCTURAL_RECEIPT='COMPLETE_INDEPENDENT_READBACK_20260930_R6.json'
        COLD_RECEIPT='CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930_R4.json'
        REPLACED=NAMES
        TITLE='المنطق المفتوح بالعربية: ثمانية اختيارات في سياقاتها وتصحيح مصدر قواعد المكمّمات'
        contextual=ENTRY.replace('INDEX_AR.md','SOL6_CONTEXTUAL_CHOICES_AR.md')
        proof=ENTRY.replace('INDEX_AR.md','SOL6_PROOF_QUANTIFICATION_AR.md')
        NOTES=(f'## اختيارات الترجمة العربية في سياقاتها\n\n[ابدأ من هنا]({ENTRY}) · [القائمة الكاملة]({FULL})\n\n'
            f'[خمسة اختيارات في سياقاتها]({contextual}) · [المتغير المميّز والروابط والمكمّمات]({proof}). '
            'يحفظ الدليل جميع القرارات الـ١٠٩٥ ووقوعاتها. تضيف المقابلة ثمانية قرارات وتسعين '
            'موضعًا مسجلًا، مع أسباب الإبقاء والتصحيح والشواهد المقروءة والبدائل وفجواتها. '
            'صُحح تعليل المسرد غير المثبت ونطاق شرح المتغير المميّز، وفُصل التعداد المجموعاتي '
            'عن الحسابي والرابط المنطقي عن رابطة الحمل. شاهد السور بديل موثق، لا إثبات '
            'للفظ المكمّم. خمس إحالات إنجليزية بلا سطر قوبلت بسياقات محددة، مع بيان الشرح '
            'غير الحرفي والاستدراكات بدل اختلاق لفظ غائب.\n\n'
            '**المصدر المصحح ليس قارئًا جديدًا بعد:** نُقل إلى المصدر المعياري المشترك '
            'استثناء فروض حذف الوجودي المؤقتة، وقيد إغلاق حد الاستبدال؛ الصيغ وأشجار البرهان '
            'الأربعة لم تتغير. المصدر الموافق متاح في الالتزام وحزمة المراجعة، لكن PDFs '
            'وEPUBs المنشورة ما زالت النسخ السابقة ولا تشمل هذين التعديلين. '
            'تظل مصادرها الكاملة ولاتخ المباشر والملفات السابقة متاحة.\n\n'
            'تضم حزمة المصدر البيانات والبطاقات والبرامج والشواهد المحددة، وأعادت الحزمة '
            'الفعلية بناء سبعة ملفات كاملة وجميع صفحات العرض القصير حرفيًا. '
            'لا تضم المعجم أو البحث المحمي أو النصوص التراثية الكاملة. '
            'هذه دفعة مجمعة، لا إعادة بناء أو نشر للكتاب بعد كل تغيير منفرد.\n\n'
            'المقابلة والتعليل اللاحق والتصحيح المحدد: OpenAI Codex — GPT-6.1 Sol، جهد Ultra. '
            'التعليلات اللاحقة والفهرسة الموروثة: OpenAI Codex — GPT-6 Sol، جهد Ultra. '
            'الترجمة الأقدم: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. '
            'إعادة فحص فترة GPT-6 Sol كلها ما زالت جارية؛ لا دعوى بتصديق كل اختيار، '
            'أو استعادة دوافع المترجم الأول، أو مراجعة بشرية. كل اختيار مفتوح للتصحيح.\n')
    git_publication.ROOT=ROOT; git_publication.STATE=STATE/'GITHUB_TRANSACTION.json'
    git_publication.READBACK=STATE/'GITHUB_COMMIT_READBACK.json'
    git_publication.PACKAGE=BASE/'COMPLETE_SOURCE_PACKAGE_RECEIPT.json'
    git_publication.EXPECTED_PARENT=('a0f19b713fcc9a199e8bc71e16d171e1a858ba2f' if context_recheck else
        '9badef2df05c3e3c4a33708536f7f93566df3731' if function_recheck else
        '603ce2e93af4a7a31a54447689c8b79785677ceb' if readable else
        'c480a848dc403f05f6a810bea8542c6873779877')
    git_publication.COMMIT_MESSAGE='تصحيح شروح وإحالات محددة في فهرس مراجعة الترجمة العربية'
    git_publication.ALLOW_CHANGED=set(selected_files()); git_publication.selected_files=selected_files
    git_publication.READBACK_STATUS='PASS_ANONYMOUS_GITHUB_CORRECTED_REVIEW_EXACT_FILES'
    zenodo.STATE_DIR=STATE; zenodo.PREVIOUS=23051728 if context_recheck else 23050440 if function_recheck else 23050173; zenodo.SUCCESSOR=True
    zenodo.EXPECTED_PREDECESSOR_FILES=100 if function_recheck else 98
    zenodo.REPLACEMENT_NAMES=REPLACED; zenodo.assets=assets
    zenodo.VERSION=('OLP-0722-AR-CONTEXT-PROOF-REVIEW-20260930' if context_recheck else
                   'OLP-0722-AR-FUNCTION-DEFINITIONS-REVIEW-20260930' if function_recheck else
                   'OLP-0722-AR-REVIEW-READABLE-20260930' if readable
                   else 'OLP-0722-AR-REVIEW-CORRECTIONS-20260930')
    zenodo.release.STAGE=STAGE; zenodo.release.GITHUB=GITHUB
    zenodo.ORDER_PREFIX=('00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf','00-CLASSICAL-02_OPENLOGIC_ar_R3_CUMULATIVE.tex','00-CLASSICAL-03_OPENLOGIC_ar_R3_SOURCES.zip')
    def metadata(draft):
        value=dict(draft['metadata']); value.pop('doi',None); value.pop('prereserve_doi',None)
        value.update(version=zenodo.VERSION,publication_date='2026-09-30',language='ara',access_right='open')
        if context_recheck:
            contextual=ENTRY.replace('INDEX_AR.md','SOL6_CONTEXTUAL_CHOICES_AR.md')
            proof=ENTRY.replace('INDEX_AR.md','SOL6_PROOF_QUANTIFICATION_AR.md')
            value['title']='المنطق المفتوح بالعربية: الطبعات الثلاث وسجل اختيارات الترجمة المصحح'
            value['description']=(f'<div lang="ar" dir="rtl"><h2>{TITLE}</h2>'
                f'<p><a href="{ENTRY}">ابدأ من هنا</a> · <a href="{FULL}">القائمة الكاملة للمراجعة</a> · '
                f'<a href="{contextual}">خمسة اختيارات في سياقاتها</a> · <a href="{proof}">المتغير المميّز والروابط والمكمّمات</a>.</p>'
                '<p>يحفظ الدليل جميع القرارات الـ١٠٩٥ ووقوعاتها؛ أضيفت مقابلة ثمانية قرارات '
                'وتسعين موضعًا مسجلًا مع أسباب الاختيار والشواهد المقروءة والبدائل والثقة وحدودها. '
                'صُحح تعليل غير مثبت للمسرد ونطاق شرح المتغير المميّز، ووثقت فجوات الاسم '
                'بدل إخفائها. خمس إحالات إنجليزية كانت بلا سطر ربطت بسياقات محددة، '
                'مع تمييز اللفظ الموجود من الشرح أو الاستدراك غير الحرفي. '
                'أعادت حزمة المصدر الفعلية إنتاج سبعة ملفات كاملة وصفحات القراءة القصيرة حرفيًا.</p>'
                '<p><strong>فرق المصدر المصحح من القارئ المنشور:</strong> نُقل تصحيحان من التراثية '
                'إلى المصدر المعياري للدولية والمشرق: استثناء الفروض المؤقتة في حذف الوجودي '
                'وإغلاق حد الاستبدال. أشجار البرهان والصيغ لم تتغير. المصدر المصحح متاح '
                'مع البطاقة وحزمة المراجعة، لكن ملفاتPDF وEPUB هنا ما زالت النسخ السابقة '
                'ولا تشمل هذين التعديلين الجديدين. مصادرها الكاملة ولاتخ المباشر وكل التاريخ '
                'المنشور باقية، ومعاينة القراءة هيPDF التراثي الجاري.</p>'
                '<p>المقابلة والتعليل الجديد والتصحيح المحدد: OpenAI Codex — GPT-6.1 Sol، جهد Ultra. '
                'التعليلات اللاحقة والفهرسة الموروثة: OpenAI Codex — GPT-6 Sol، جهد Ultra. '
                'الترجمة الأقدم: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. '
                'إعادة فحص الفترة كلها ما زالت جارية؛ ليست هذه شهادة على كل الاختيارات '
                'ولا استعادة لدوافع تاريخية ولا مراجعة بشرية. كل اختيار مفتوح للتصحيح.</p>'
                f'<p><a href="{GITHUB}">الملفات ومصادر المراجعة علىGitHub</a>.</p></div>'+value.get('description',''))
        elif function_recheck:
            card=ENTRY.replace('INDEX_AR.md','SOL6_FUNCTION_DEFINITIONS_AR.md')
            value['description']=(f'<div lang="ar" dir="rtl"><h2>{TITLE}</h2>'
                f'<p><a href="{ENTRY}">ابدأ من هنا</a> · <a href="{FULL}">القائمة الكاملة للمراجعة</a> · '
                f'<a href="{card}">ثلاثة تعريفات للدوال: الكلمات والمواضع والأسباب</a>.</p>'
                '<p>يحفظ الدليل القرارات الـ١٠٩٥ ووقوعاتها كاملة. تضيف هذه النسخة شواهد مقروءة '
                'لثلاثة عناوين في OLP-0022 وتسعة مواضع في الأصل والترجمتين، مع البدائل وحدود '
                'الثقة والسؤال الموجه للمختص. أُبقي المتن الصحيح رياضيًا؛ وأضيف شاهد مستقل للتباين '
                'وبقي الخلاف بين شاملة وغامرة معلنًا. لا تعمم النتيجة على بقية الأسرة أو كل التعليلات. '
                'المصادر الكاملة للدليل والشيفرة والشواهد المحددة في حزمة المصدر؛ '
                'لا تعاد نشر المقالة المحمية أو الأزواج التراثية الكاملة. '
                'أُعيد من الحزمة الفعلية بناء العرض والبيانات حرفيًا.</p>'
                '<p>المقابلة والتعليل الجديد: OpenAI Codex — GPT-6.1 Sol، جهد Ultra. '
                'التعليلات العربية اللاحقة والفهرسة الموروثة: OpenAI Codex — GPT-6 Sol، جهد Ultra. '
                'الترجمة والتعليلات الأقدم: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. '
                'لم تقع مراجعة بشرية شاملة، وإعادة فحص الفترة كلها ما زالت جارية. '
                'كل اختيار قابل للتصحيح، ولا يستعاد بهذا التسويغ اللاحق دافع المترجم الأول.</p>'
                '<p>كل القراء ومصادر لاتخ المباشرة وحزمها وكتب EPUB والتاريخ الموروث باقية. '
                'لم يضف هذا الإصدار تعديلًا لمتن PDF أو EPUB؛ معاينة القراءة هي PDF التراثي الجاري.</p>'
                f'<p><a href="{GITHUB}">الدليل وملفات مصادره على GitHub</a>.</p></div>'+value.get('description',''))
        else:
            value['description']=(f'<div lang="ar" dir="rtl"><h2>{TITLE}</h2>'
            f'<p><a href="{ENTRY}">ابدأ من هنا</a> · <a href="{FULL}">القائمة الكاملة للمراجعة</a>.</p>'
            '<p>حُفظت جميع القرارات الـ١٠٩٥ ووقوعاتها. صُحِّحت خمسة شروح رياضية، واستُبدلت '
            '٥٩ إحالة إلى تعليقات أسماء الأقسام في ٣٢ قرارًا بمقاطع مقروءة من الأصل. '
            'متن الكتب لم يتغير بهذه الدفعة؛ كانت التعريفات المعنية صحيحة فيه بالفعل. '
            'أضيف عرض كامل في صفحات قصيرة متصلة لقراءة الجدول والبطاقات الكبيرة؛ '
            'حُفظ كل صف وكل نص، وبقيت الملفات الكاملة قابلة للتنزيل. '
            'تشمل الملفات البطاقتين المصححتين والدليل والبيانات وحزمة المصدر القابلة لإعادة البناء حرفيًا. '
            'تحتفظ هذه النسخة بكل القراء ومصادر لاتخ المباشرة وحزمها وكتب EPUB والملفات الموروثة؛ '
            'معاينة القراءة هي PDF القارئ التراثي الأحدث.</p>'
            '<p>الترجمة والتعليلات الموروثة: OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra. '
            'التعليلات اللاحقة والفهرسة: OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. '
            'المقابلة والتصحيحات المحددة وهذه الدفعة: OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. '
            'لم تقع مراجعة بشرية شاملة؛ إعادة فحص الفترة كلها ما زالت جارية، '
            'ولا يدعي هذا الإصدار تصديق كل تعليل أو شاهد معجمي. تبقى الاختيارات مفتوحة للتصحيح.</p>'
                f'<p><a href="{GITHUB}">ملفات التصحيح ومصادرها على GitHub</a>.</p></div>'+value.get('description',''))
        related=list(value.get('related_identifiers',[]))
        for url in (ENTRY,FULL,GITHUB):
            if not any(r.get('identifier')==url for r in related):
                related.append({'identifier':url,'relation':'isSupplementTo','scheme':'url'})
        value['related_identifiers']=related
        return value
    zenodo.metadata_for=metadata


def check_current_msa():
    require(CURRENT_MSA_SOURCE_ROOT is not None,'Explicit current source stage is required')
    cold=json.loads((CURRENT_MSA_SOURCE_ROOT/'COLD_REPLAY_COMPARISON.json').read_bytes())
    require(cold['status']=='PASS_BYTE_IDENTICAL_COLD_REPLAY' and cold['files_compared']==4,
            'Current editable source cold replay differs')
    for row in cold['files']:
        require(identity(CURRENT_MSA_SOURCE_ROOT/'primary/files'/row['file'])==
                {'file':row['file'],'bytes':row['bytes'],'sha256':row['sha256']},
                'Current editable source stage changed')
    qa=json.loads((CURRENT_PDF_ROOT/'OPENLOGIC_ar_DUAL_NOTATION_PDF_QA.json').read_bytes())
    require(qa.get('status')=='PASS','Current component PDF checks are incomplete')
    from profile_checkpoint import source_identity
    digest,_=source_identity(ROOT)
    for profile,pdf_name in (
        ('international','00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf'),
        ('machrek','01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf')):
        checkpoint=json.loads((CURRENT_PDF_ROOT/f'PROFILE_CHECKPOINT_{profile}.json').read_bytes())
        require(checkpoint['status']=='PASS' and checkpoint['source_tree_sha256']==digest,
                'Current compiled source identity differs')
        assembly=json.loads((CURRENT_PDF_ROOT/pdf_name.replace('.pdf','.assembly.json')).read_bytes())
        pdf=identity(CURRENT_PDF_ROOT/pdf_name)
        require(assembly['status']=='PASS' and assembly['output']['sha256'].lower()==pdf['sha256']
                and assembly['output']['bytes']==pdf['bytes'],'Current complete PDF assembly differs')


def configure_current_msa(source_root):
    """One finite, paired current-reader/review release in the existing lineage."""
    global CURRENT_MSA,CURRENT_MSA_SOURCE_ROOT,ASSET_INPUTS,NAMES,REPLACED
    global TAG,GITHUB,ENTRY,FULL,STATE,STAGE,TITLE,NOTES,STRUCTURAL_RECEIPT,COLD_RECEIPT
    CURRENT_MSA=True;CURRENT_MSA_SOURCE_ROOT=source_root.resolve()
    CURRENT_MSA_SOURCE_ROOT.relative_to((ROOT/'tmp').resolve())
    TAG='ar-openlogic-current-msa-and-review-20260930'
    GITHUB=f'https://github.com/{REMOTE}/releases/tag/{TAG}'
    ENTRY=f'https://github.com/{REMOTE}/blob/{TAG}/expert-review/2026-09-26-final-page-review/INDEX_AR.md'
    FULL=ENTRY.replace('INDEX_AR.md','DIRECTORY_READABLE_AR.md')
    STATE=ROOT/'evidence/publication/current-msa-and-review-20260930'
    STAGE=ROOT/'output/release/current-msa-and-review-20260930'
    STRUCTURAL_RECEIPT='COMPLETE_INDEPENDENT_READBACK_20260930_R8.json'
    COLD_RECEIPT='CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930_R8.json'
    stems=('MSA_INTERNATIONAL','MSA_MACHREK')
    books=[];ASSET_INPUTS={}
    for i,stem in enumerate(stems):
        published=(f'{i*3:02d}_OPENLOGIC_ar_R3_{stem}.pdf',
                   f'{i*3+1:02d}_OPENLOGIC_ar_R3_{stem}.tex',
                   f'{i*3+2:02d}_OPENLOGIC_ar_R3_{stem}_SOURCES.zip')
        component=('00_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_INTERNATIONAL_NOTATION_OLP-0722.pdf'
                   if i==0 else '01_OPENLOGIC_ar_COMPLETE_722_UNIT_READER_MACHREK_NOTATION_OLP-0722.pdf')
        ASSET_INPUTS.update(zip(published,(CURRENT_PDF_ROOT/component,
            CURRENT_MSA_SOURCE_ROOT/f'primary/files/OPENLOGIC_ar_R3_{stem}.tex',
            CURRENT_MSA_SOURCE_ROOT/f'primary/files/OPENLOGIC_ar_R3_{stem}_SOURCES.zip')))
        books.extend(published)
    NAMES=tuple(books)+ORIGINAL_NAMES;REPLACED=NAMES
    TITLE='المنطق المفتوح بالعربية: القارئان المعياريان المصححان وسجل المراجعة الكامل'
    NOTES=(f'## القارئان المعياريان المصححان وسجل الاختيارات\n\n[ابدأ من هنا]({ENTRY}) · [القائمة الكاملة]({FULL})\n\n'
        'تتضمن ملفات PDF الحالية تصحيحي قواعد المكممات: استثناء الفرض المؤقت الذي يسقطه حذف '
        'الوجودي، وإغلاق حد الاستبدال. عُرّبت أدوات وصل الإحالات ولفظ بنودها. لم تُغير قواعد '
        'البرهان أو المعاني الرياضية. يعرض ترميز المشرق أرقام الصيغ بالأشكال العربية الهندية؛ '
        'أرقام الصفحات والفصول باقية بالأشكال الدولية في هذا المسار الموروث. '
        'لكل قارئ ملف لاتخ تراكمي مباشر وحزمة المصدر الكاملة '
        'المقابلة، بما فيها الخطوط والصور والمراجع وبرامج البناء.\n\n'
        'يحفظ دليل المراجعة جميع القرارات الـ١٠٩٥ ووقوعاتها وتعليلاتها. أضيف تصحيح وصف شاهد '
        'المتغير الحر والمقيد: المواضع الثلاثة المسجلة تثبت الحرية فقط، والتعريف المساند '
        'يستعمل مقيد لا مربوط. بقيت فجوة الشاهد المستقل ظاهرة، ولم يتغير متن هذه الفقرة. '
        'أعادت حزمة المراجعة الفعلية بناء العرض والبيانات وصفحات القراءة حرفيًا.\n\n'
        'الترجمة الموروثة: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. التعليلات والفهرسة اللاحقة '
        'وإكمال EPUB السابق: OpenAI Codex — GPT-6 Sol، جهد Ultra. التصحيح المحدد والمقابلة '
        'الجديدة وإعادة بناء هذين القارئين: OpenAI Codex — GPT-6.1 Sol، جهد Ultra. '
        'لم تقع مراجعة بشرية شاملة، وإعادة فحص فترة GPT-6 Sol كلها ما زالت جارية. '
        'كل اختيار مفتوح للتصحيح.\n\n'
        '**EPUB ليس هذا PDF:** الكتب الإلكترونية المحفوظة لا تتضمن تصحيحي المتن الجديدين. '
        'القارئ التراثي وملف لاتخ المباشر ومصدره الكامل وجميع الإصدارات السابقة باقية؛ '
        'لم يعاد بناء التراثية في هذه الدفعة.\n\n')
    labels=('القارئ الدولي PDF','لاتخ الدولي الكامل','حزمة مصادر الدولي',
            'قارئ المشرق PDF','لاتخ المشرق الكامل','حزمة مصادر المشرق')
    for label,name in zip(labels,books):
        NOTES+=f'- [{label}](https://github.com/{REMOTE}/releases/download/{TAG}/{name})\n'
    git_publication.STATE=STATE/'GITHUB_TRANSACTION.json'
    git_publication.READBACK=STATE/'GITHUB_COMMIT_READBACK.json'
    git_publication.EXPECTED_PARENT='3902c93a8fb8448b299044564a4c875080c7e042'
    git_publication.COMMIT_MESSAGE='تحديث القارئين المعياريين ومصادرهما وسجل مراجعة الاختيارات'
    git_publication.ALLOW_CHANGED=set(selected_files());git_publication.selected_files=selected_files
    zenodo.STATE_DIR=STATE;zenodo.PREVIOUS=23055816;zenodo.SUCCESSOR=True
    zenodo.EXPECTED_PREDECESSOR_FILES=100;zenodo.REPLACEMENT_NAMES=REPLACED
    zenodo.PREVIEW=books[0];zenodo.ORDER_PREFIX=tuple(books)
    zenodo.VERSION='OLP-0722-AR-CURRENT-MSA-REVIEW-20260930'
    zenodo.release.STAGE=STAGE;zenodo.release.GITHUB=GITHUB
    def metadata(draft):
        value=dict(draft['metadata']);value.pop('doi',None);value.pop('prereserve_doi',None)
        value.update(title=TITLE,version=zenodo.VERSION,publication_date='2026-09-30',language='ara',access_right='open')
        # Do not append superseded current-status claims from the predecessor.
        value['description']=(f'<div lang="ar" dir="rtl"><h2>{TITLE}</h2>'
            f'<p><a href="{ENTRY}">ابدأ من هنا</a> · <a href="{FULL}">القائمة الكاملة للمراجعة</a>.</p>'
            '<p>تتضمن الطبعتان المعياريتان الكاملتان تصحيحي قواعد المكمّمات والإحالات العربية. '
            'كل ملف PDF يضم الوحدات الـ٧٢٢، ويرافقه ملف لاتخ كامل مباشر وحزمة المصدر الدقيق '
            'مع الخطوط والصور والمراجع وبرامج البناء. المعاينة للقارئ الدولي المصحح. '
            'ترميز المشرق يحول أرقام الصيغ فقط؛ أرقام الصفحات والفصول باقية بالأشكال الدولية. '
            'يحفظ الدليل جميع القرارات الـ١٠٩٥ ووقوعاتها وأسبابها وأسئلة المراجع، مع تصحيح '
            'نطاق شاهد المتغير الحر والمقيد وإظهار فجوات التوثيق.</p>'
            '<p>الترجمة الموروثة: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. التعليلات والفهرسة '
            'اللاحقة وإكمال EPUB السابق: OpenAI Codex — GPT-6 Sol، جهد Ultra. '
            'التصحيح المحدد والمقابلة الجديدة وإعادة بناء القارئين المعياريين: '
            'OpenAI Codex — GPT-6.1 Sol، جهد Ultra. إعادة فحص الفترة كلها ما زالت جارية؛ '
            'لا دعوى بمراجعة بشرية شاملة أو تصديق جميع الاختيارات. كل اختيار مفتوح للتصحيح.</p>'
            '<p>التراثية ومصدرها والإصدارات السابقة محفوظة. EPUB يظل بالمتن المجمد السابق '
            'ولا يتضمن تصحيحي المعيارية الجديدين؛ ليس نسخة مطابقة للقارئين الجديدين.</p>'
            f'<p><a href="{GITHUB}">تنزيل القارئين ولاتخ المباشر وحزم المصادر ودليل المراجعة</a>.</p></div>')
        related=list(value.get('related_identifiers',[]))
        for url in (ENTRY,FULL,GITHUB):
            if not any(r.get('identifier')==url for r in related):
                related.append({'identifier':url,'relation':'isSupplementTo','scheme':'url'})
        value['related_identifiers']=related
        return value
    zenodo.metadata_for=metadata


def revise_existing_draft():
    require(READABLE,'This repair must use the explicitly selected readable edition')
    rows=assets(); zenodo.checked_github_receipt(rows)
    old_dir=ROOT/'evidence/publication/review-corrections-20260930'
    old_path=old_dir/'ZENODO_TRANSACTION.json'
    old=json.loads(old_path.read_bytes())
    require(old['status']=='READY_TO_PUBLISH' and old['draft_id']==23050440,
            'Existing draft state must be inspected; no duplicate version')
    old_stage=ROOT/'output/release/review-corrections-20260930'
    def md5(path):
        with path.open('rb') as stream:
            return 'md5:'+hashlib.file_digest(stream,'md5').hexdigest()
    before=dict(old['inherited'])
    for item in old['assets']:
        path=old_stage/item['name']
        require(identity(path)=={'file':item['name'],'bytes':item['bytes'],'sha256':item['sha256']},
                'Historical accepted stage differs')
        before[item['name']]={'bytes':item['bytes'],'checksum':md5(path)}
    transaction=STATE/'ZENODO_TRANSACTION.json'
    require(not transaction.exists(),'Inspect the saved same-draft revision instead of restarting it')
    updated=dict(old); updated.update(status='REVISING_EXISTING_DRAFT',assets=rows,
                                     predecessor_correction_state=str(old_path.relative_to(ROOT)))
    with zenodo.authenticated() as session:
        legacy=zenodo.call(session,'GET',f'{zenodo.API}/deposit/depositions/{old["draft_id"]}').json()
        require(not legacy['submitted'] and int(legacy['conceptrecid'])==zenodo.CONCEPT,
                'Existing record is no longer this unpublished draft')
        modern=zenodo.draft_record(session,old['draft_id'])
        observed={n:{'bytes':v['size'],'checksum':v['checksum']} for n,v in modern['files']['entries'].items()}
        require(observed==before,'Existing draft inventory changed')
        require(zenodo.public_record(zenodo.PREVIOUS)['versions']['is_latest'],'Predecessor changed')
        zenodo.save(transaction,updated)
        old['status']='SUPERSEDED_BY_READABILITY_REVISION_SAME_DRAFT'
        old['successor_transaction']=str(transaction.relative_to(ROOT)); zenodo.save(old_path,old)
        old_rows={r['name']:r for r in old['assets']}
        files={r['filename']:r for r in legacy['files']}
        replaced=[]
        for row in rows:
            if row==old_rows[row['name']]:
                continue
            zenodo.call(session,'DELETE',f'{zenodo.API}/deposit/depositions/{old["draft_id"]}/files/{files[row["name"]]["id"]}')
            with (STAGE/row['name']).open('rb') as stream:
                zenodo.call(session,'PUT',legacy['links']['bucket']+'/'+row['name'],data=stream,
                            headers={'Content-Type':'application/octet-stream'})
            replaced.append(row['name'])
        zenodo.call(session,'PUT',f'{zenodo.API}/deposit/depositions/{old["draft_id"]}',
                    json={'metadata':zenodo.metadata_for(legacy)})
        modern=zenodo.draft_record(session,old['draft_id'])
        expected=dict(updated['inherited'])
        expected.update({r['name']:{'bytes':r['bytes'],'checksum':md5(STAGE/r['name'])} for r in rows})
        observed={n:{'bytes':v['size'],'checksum':v['checksum']} for n,v in modern['files']['entries'].items()}
        require(observed==expected and len(observed)==100,'Revised draft identities differ')
        payload={k:modern[k] for k in ('metadata','access','custom_fields') if k in modern}
        payload['files']={'enabled':True,'default_preview':zenodo.PREVIEW,
                         'order':list(zenodo.ORDER_PREFIX)+sorted(set(expected)-set(zenodo.ORDER_PREFIX))}
        zenodo.call(session,'PUT',f'{zenodo.API}/records/{old["draft_id"]}/draft',headers={'Accept':zenodo.RDM},json=payload)
        final=zenodo.draft_record(session,old['draft_id'])
        require(final['files']['default_preview']==zenodo.PREVIEW and final['metadata']['version']==zenodo.VERSION,
                'Revised preview/version differs')
        require(final['access']['record']==final['access']['files']=='public','Draft access differs')
        updated.update(status='READY_TO_PUBLISH',revised_private_draft_files=replaced,
                       draft_files=100,default_preview=zenodo.PREVIEW)
        zenodo.save(transaction,updated)
    print(json.dumps({'status':updated['status'],'same_draft_id':updated['draft_id'],
                      'replaced_private_files':len(replaced),'public_access_removed':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    actions={'stage':stage,'git-prepare':git_publication.prepare,'git-push':git_publication.push,
             'git-verify':git_publication.verify,'github':github_release,'github-verify':github_verify,
             'prepare':zenodo.prepare,'publish':zenodo.publish,'verify':zenodo.verify,
             'revise-draft':revise_existing_draft}
    parser.add_argument('action',choices=actions)
    parser.add_argument('--readable',action='store_true')
    parser.add_argument('--function-recheck',action='store_true')
    parser.add_argument('--context-recheck',action='store_true')
    parser.add_argument('--current-msa-source',type=Path,
                        help='Checked four-file current-MSA source export under repo/tmp; selects the paired current-reader release.')
    args=parser.parse_args(); configure(args.readable or args.function_recheck or args.context_recheck or bool(args.current_msa_source),args.function_recheck or args.context_recheck or bool(args.current_msa_source),args.context_recheck or bool(args.current_msa_source))
    if args.current_msa_source:configure_current_msa(args.current_msa_source)
    require(not(args.readable and not args.function_recheck and args.action=='prepare'),'Readable repair reuses the existing draft; use revise-draft')
    try: actions[args.action]()
    except requests.RequestException as error:
        raise SystemExit('Publication transport failed ('+type(error).__name__+'); inspect saved state before one bounded retry') from None

"""Publish one checked correction batch, not a claim of full Sol6 re-review."""
import argparse
import hashlib
import json
import os
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
    fresh=json.loads((BASE/'COMPLETE_INDEPENDENT_READBACK_20260930_R3.json').read_bytes())
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
    hashes=[identity(BASE/name) for name in NAMES[:-1]]
    (BASE/NAMES[-1]).write_text(''.join(r['sha256']+'  '+r['file']+'\n' for r in hashes),encoding='utf-8',newline='\n')
    STAGE.mkdir(parents=True); STATE.mkdir(parents=True)
    rows=[]
    for name in NAMES:
        row=identity(BASE/name); rows.append({'name':name,'bytes':row['bytes'],'sha256':row['sha256']})
        os.link(BASE/name,STAGE/name)
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
    paths=[(base/name).as_posix() for name in NAMES]
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


def configure(readable=False):
    global READABLE,TAG,GITHUB,ENTRY,FULL,STAGE,STATE,TITLE,NOTES,COLD_RECEIPT
    READABLE=readable
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
    git_publication.ROOT=ROOT; git_publication.STATE=STATE/'GITHUB_TRANSACTION.json'
    git_publication.READBACK=STATE/'GITHUB_COMMIT_READBACK.json'
    git_publication.PACKAGE=BASE/'COMPLETE_SOURCE_PACKAGE_RECEIPT.json'
    git_publication.EXPECTED_PARENT=('603ce2e93af4a7a31a54447689c8b79785677ceb' if readable
                                     else 'c480a848dc403f05f6a810bea8542c6873779877')
    git_publication.COMMIT_MESSAGE='تصحيح شروح وإحالات محددة في فهرس مراجعة الترجمة العربية'
    git_publication.ALLOW_CHANGED=set(selected_files()); git_publication.selected_files=selected_files
    git_publication.READBACK_STATUS='PASS_ANONYMOUS_GITHUB_CORRECTED_REVIEW_EXACT_FILES'
    zenodo.STATE_DIR=STATE; zenodo.PREVIOUS=23050173; zenodo.SUCCESSOR=True
    zenodo.REPLACEMENT_NAMES=REPLACED; zenodo.assets=assets
    zenodo.VERSION=('OLP-0722-AR-REVIEW-READABLE-20260930' if readable
                   else 'OLP-0722-AR-REVIEW-CORRECTIONS-20260930')
    zenodo.release.STAGE=STAGE; zenodo.release.GITHUB=GITHUB
    zenodo.ORDER_PREFIX=('00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf','00-CLASSICAL-02_OPENLOGIC_ar_R3_CUMULATIVE.tex','00-CLASSICAL-03_OPENLOGIC_ar_R3_SOURCES.zip')
    def metadata(draft):
        value=dict(draft['metadata']); value.pop('doi',None); value.pop('prereserve_doi',None)
        value.update(version=zenodo.VERSION,publication_date='2026-09-30',language='ara',access_right='open')
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
    parser.add_argument('--readable',action='store_true'); args=parser.parse_args(); configure(args.readable)
    require(not(args.readable and args.action=='prepare'),'Readable repair reuses the existing draft; use revise-draft')
    try: actions[args.action]()
    except requests.RequestException as error:
        raise SystemExit('Publication transport failed ('+type(error).__name__+'); inspect saved state before one bounded retry') from None

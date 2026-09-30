"""One finite successor release of the three disclosure-corrected EPUBs.

The wider Sol6 semantic review is unfinished and is not represented as passed.
Only four changed existing Zenodo files are replaced in a new version; every
public predecessor and inherited reader/source/review asset remains public.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import requests

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE))
import publish_complete_epubs_20260925 as baseline
import publish_classical_reader_20260926 as transaction
from review_sol6_epub_20260930 import identity, require

ROOT=HERE.parent
SOURCE=ROOT/'tmp/epub/sol6-independent-review-20260930-r1'
STAGE=ROOT/'output/release/epub-provenance-correction-20260930'
STATE=ROOT/'evidence/publication/epub-provenance-correction-20260930'
TAG='ar-olp-0722-epub-provenance-correction-20260930'
REMOTE='KokunoYumeto/OpenLogic-ar'
GITHUB=f'https://github.com/{REMOTE}/releases/tag/{TAG}'
CHANGED=('22_OpenLogic-Arabic-Complete-722-international.epub',
         '25_OpenLogic-Arabic-Complete-722-machrek.epub',
         '28_OpenLogic-Arabic-Complete-722-classical.epub',
         '29_OPENLOGIC_ar_R3_COMPLETE_EPUB_SOURCE_AND_QA.zip')
TITLE='نص المنطق المفتوح بالعربية: تصحيح بيان إنتاج الكتب الإلكترونية الثلاثة'
NOTES=(
    '## الكتب الإلكترونية العربية الثلاثة ومصادرها القابلة للتحرير\n\n'
    'تضم هذه النسخة الكتب الكاملة ذات الوحدات الـ٧٢٢، بالترميز الدولي، والترقيم المشرقي، '
    'والصياغة التراثية ذات الرموز العربية والصيغ من اليمين إلى اليسار. '
    'صُحِّح بيان النماذج التي أنتجت تحويل EPUB وحزمته؛ لم يتغير متن الترجمة أو MathML. '
    'لكل كتاب ملف LaTeX تراكمي مباشر وحزمة مصدر كاملة بجواره. '
    'تحوي الحزمة المشتركة ملفات EPUB الداخلية القابلة للتحرير وبرنامج إعادة بنائها حرفيًا.\n\n'
    'الترجمة والتصحيحات الموروثة منسوبة في المصدر إلى OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra. '
    'استكمال تحويل EPUB وتجميعه والتحقق الآلي منه وحزم مصادره: OpenAI Codex — GPT-6 Sol، بمستوى جهد Ultra. '
    'إعادة فحص البناء وتصحيح البيان والتحقق من هذه النسخة: OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. '
    'لم تقع مراجعة بشرية شاملة.\n\n'
    'أعيدت النسخ القديمة من مصادرها وطابقت بايتاتها المنشورة، ثم اجتازت النسخ المصححة EPUBCheck 5.3.0 '
    'دون خطأ أو إنذار وAce 1.4.6 دون إخفاق، وأعادت حزمة المصدر إنتاجها بايتًا ببايت. '
    'بقيت ٨١٧ من ٨١٩ ملفًا داخليًا في كل كتاب بلا تغيير؛ تغير ملف الحزمة وصفحة بيان الإنتاج فقط. '
    'هذه فحوص محددة، وليست شهادة على صحة كل اختيار ترجمي أو على جميع تفاصيل العرض.\n\n'
    'متن EPUB هو النسخة المثبتة في ٢٥ سبتمبر؛ لا يضم تلقائيًا تصحيحات تنضيد PDF اللاحقة. '
    '[القارئ التراثي PDF الأحدث ومصدره المباشر وحزمته](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-olp-0722-classical-eastern-rtl-fn-unicode-20260928) '
    'باقية متاحة. إعادة فحص تعليلات المراجعة في فترة GPT-6 Sol ما زالت جارية، ولم تُقدَّم هنا بوصفها مكتملة.\n'
)
for profile, label, stem, number in (
    ('international','الفصحى المعاصرة بالترميز الدولي','MSA_INTERNATIONAL',20),
    ('machrek','الفصحى المعاصرة بترميز المشرق','MSA_MACHREK',23),
    ('classical','العربية التراثية ذات الصيغ من اليمين إلى اليسار','CLASSICAL_EASTERN_RTL',26),
):
    base=f'https://github.com/{REMOTE}/releases/download/{TAG}/'
    NOTES += (f'\n{label}: '
              f'[ملف لاتخ الكامل المباشر]({base}{number}_OPENLOGIC_ar_R3_{stem}.tex) · '
              f'[حزمة مصدر لاتخ الكاملة]({base}{number+1}_OPENLOGIC_ar_R3_{stem}_SOURCES.zip) · '
              f'[الكتاب الإلكتروني]({base}{number+2}_OpenLogic-Arabic-Complete-722-{profile}.epub).\n')


def description_html():
    """Render this fixed, reader-facing Markdown without raw markup in Zenodo."""
    blocks=[]
    for paragraph in NOTES.strip().split('\n\n'):
        heading=paragraph.startswith('## ')
        value=paragraph[3:] if heading else paragraph
        value=html.escape(value.strip())
        value=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',
                     r'<a href="\2">\1</a>',value)
        tag='h2' if heading else 'p'
        blocks.append(f'<{tag}>{value}</{tag}>')
    return '<div lang="ar" dir="rtl">'+''.join(blocks)+'</div>'


def all_assets():
    manifest=json.loads((STATE/'STAGE.json').read_bytes())
    require(manifest['status']=='PASS_EXACT_LOCAL_STAGE','Stage is not accepted')
    for row in manifest['files']:
        require(identity(STAGE/row['name'])=={'file':row['name'],'bytes':row['bytes'],'sha256':row['sha256']},'Stage bytes changed')
    return manifest['files']


def changed_assets():
    return [r for r in all_assets() if r['name'] in CHANGED]


def stage():
    package=json.loads((SOURCE/'SOURCE_PACKAGE_RECEIPT.json').read_bytes())
    replay=json.loads((SOURCE/'EXTRACTED_SOURCE_COLD_REPLAY.json').read_bytes())
    require(package['status']=='PASS_FRESH_CHECKERS_COLD_REPLAY_AND_EXACT_SOURCE' and
            replay['status']=='PASS_REBUILD_FROM_ACTUAL_CORRECTED_SOURCE_ZIP' and
            package['archive']['sha256']==replay['source_zip_sha256'],'Fresh source/checker gates differ')
    require(not STAGE.exists() and not STATE.exists(),'Existing stage must be inspected, not replaced')
    STAGE.mkdir(parents=True); STATE.mkdir(parents=True)
    names={r['profile']:r['epub'] for r in package['profiles']}
    files=[]
    for name,original,size,sha in baseline.FILES:
        if name in CHANGED:
            original=SOURCE/original.name
            record=identity(original); size,sha=record['bytes'],record['sha256']
            if name.endswith('.epub'):
                require(any(r['sha256']==sha for r in names.values()),'EPUB is not checker-bound')
            else:
                require(record==package['archive'],'Source archive is not accepted')
        else:
            require(identity(original)=={'file':original.name,'bytes':size,'sha256':sha},'Original direct source differs')
        os.link(original,STAGE/name)
        files.append({'name':name,'bytes':size,'sha256':sha})
    (STATE/'STAGE.json').write_text(json.dumps({'status':'PASS_EXACT_LOCAL_STAGE','files':files},indent=2)+'\n',encoding='utf-8')
    (STATE/'RELEASE_NOTES_AR.md').write_text(NOTES,encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PASS_EXACT_LOCAL_STAGE','files':len(files)}))


def github():
    files=all_assets()
    probe=requests.get(f'https://api.github.com/repos/{REMOTE}/releases/tags/{TAG}',timeout=(20,60))
    require(probe.status_code==404,'Release exists or its absence could not be proved; inspect without duplicate creation')
    result=subprocess.run(['gh','release','create',TAG,'--repo',REMOTE,'--target','0723c24608828898bfc72b3b131915efbb1f2658',
                           '--title',TITLE,'--notes-file',str(STATE/'RELEASE_NOTES_AR.md')]+[str(STAGE/r['name']) for r in files],capture_output=True,text=True)
    require(result.returncode==0,'GitHub release creation failed; inspect release state before retry')
    print(GITHUB)


def github_verify():
    files=all_assets(); checked=[]
    response=requests.get(f'https://api.github.com/repos/{REMOTE}/releases/tags/{TAG}',timeout=(20,60)); response.raise_for_status()
    release=response.json(); require(not release['draft'] and not release['prerelease'],'Wrong release state')
    entries={r['name']:r for r in release['assets']}; require(set(entries)=={r['name'] for r in files},'GitHub inventory differs')
    with requests.Session() as anonymous:
        anonymous.trust_env=False
        for row in files:
            require(entries[row['name']]['size']==row['bytes'],'GitHub inventory size differs')
            h=hashlib.sha256(); count=0
            with anonymous.get(entries[row['name']]['browser_download_url'],stream=True,timeout=(20,90)) as r:
                require(r.status_code==200,'Anonymous GitHub download failed')
                for block in r.iter_content(1048576):
                    count+=len(block); require(count<=row['bytes'],'Public bytes exceed expected size'); h.update(block)
            require((count,h.hexdigest())==(row['bytes'],row['sha256']),'GitHub public bytes differ')
            checked.append({**row,'url':entries[row['name']]['browser_download_url'],'anonymous':True})
    whole={'status':'PASS_ANONYMOUS_GITHUB_READBACK','release':GITHUB,'files':checked}
    transaction.save(STATE/'GITHUB_ALL_ASSETS_READBACK.json',whole)
    transaction.save(STATE/'GITHUB_READBACK.json',{**whole,'files':[r for r in checked if r['name'] in CHANGED]})
    print(json.dumps({'status':whole['status'],'files':len(checked)}))


def configure():
    transaction.STATE_DIR=STATE; transaction.PREVIOUS=23004225; transaction.VERSION='OLP-0722-AR-EPUB-DISCLOSURE-20260930'
    transaction.SUCCESSOR=True; transaction.assets=changed_assets
    transaction.release.STAGE=STAGE; transaction.release.GITHUB=GITHUB
    transaction.ORDER_PREFIX=('00-CLASSICAL-01_OPENLOGIC_ar_R3_READER.pdf','00-CLASSICAL-02_OPENLOGIC_ar_R3_CUMULATIVE.tex','00-CLASSICAL-03_OPENLOGIC_ar_R3_SOURCES.zip')
    transaction.PREVIEW=transaction.ORDER_PREFIX[0]
    def metadata(draft):
        value=dict(draft['metadata']); value.pop('doi',None); value.pop('prereserve_doi',None)
        value.update(version=transaction.VERSION,publication_date='2026-09-30',language='ara',access_right='open',
                     description=description_html()+value.get('description',''))
        related=list(value.get('related_identifiers',[]))
        if not any(r.get('identifier')==GITHUB for r in related): related.append({'identifier':GITHUB,'relation':'isIdenticalTo','scheme':'url'})
        value['related_identifiers']=related
        return value
    transaction.metadata_for=metadata


def zenodo_verify():
    transaction.verify()
    state=json.loads((STATE/'ZENODO_TRANSACTION.json').read_bytes())
    public=transaction.public_record(int(state['draft_id']))
    entries=public['files']['entries']
    checked=[]
    # The six inherited direct-source files are prerequisites for these EPUBs,
    # not merely filenames whose presence is sufficient proof of source access.
    with requests.Session() as anonymous:
        anonymous.trust_env=False
        for row in all_assets():
            if row['name'] in CHANGED:
                continue
            h=hashlib.sha256(); count=0
            with anonymous.get(entries[row['name']]['links']['content'],stream=True,timeout=(20,90)) as result:
                require(result.status_code==200,'Anonymous editable-source download failed')
                for block in result.iter_content(1048576):
                    count+=len(block); require(count<=row['bytes'],'Editable source exceeds expected size'); h.update(block)
            require((count,h.hexdigest())==(row['bytes'],row['sha256']),'Public editable source differs')
            checked.append({**row,'anonymous':True,'url':entries[row['name']]['links']['content']})
    transaction.save(STATE/'ZENODO_EDITABLE_SOURCE_READBACK.json',{
        'status':'PASS_ANONYMOUS_EXACT_SIX_EDITABLE_SOURCE_FILES',
        'record_id':state['draft_id'],'files':checked,
        'default_preview':public['files']['default_preview'],
        'reported_order':public['files'].get('order',[]),
        'requested_order_prefix':list(transaction.ORDER_PREFIX)})
    print(json.dumps({'status':'PASS_ANONYMOUS_EXACT_SIX_EDITABLE_SOURCE_FILES','files':len(checked)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    actions={'stage':stage,'github':github,'github-verify':github_verify,'prepare':transaction.prepare,'publish':transaction.publish,'verify':zenodo_verify}
    parser.add_argument('action',choices=actions); action=parser.parse_args().action
    configure()
    try: actions[action]()
    except requests.RequestException as error:
        raise SystemExit('Publication transport failed ('+type(error).__name__+'); preserve and inspect the recorded transaction') from None

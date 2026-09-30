"""One coherent EPUB correction release in the existing GitHub/Zenodo lineage.

Replace seven existing Zenodo assets only: two EPUBs, their four exact current
LaTeX/source files, and the shared exact-source archive. Preserve Classical,
the current PDF preview and the other 93 public files. No historical default
or public predecessor is edited, and no duplicate transaction is created.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import publish_reviewed_epubs_20260930 as prior
import publish_classical_reader_20260926 as zenodo
import publish_arabic_review_359_github_20260927 as git
from package_msa_epub_successor_20260930 import SOURCE_IDS, CURRENT, CLASSICAL, OLD
from review_sol6_epub_20260930 import identity, require

ROOT = HERE.parent
SOURCE = ROOT / 'tmp/epub/msa-quantifier-successor-20260930-r1'
STAGE = ROOT / 'output/release/epub-quantifier-corrections-20260930'
STATE = ROOT / 'evidence/publication/epub-quantifier-corrections-20260930'
TAG = 'ar-olp-0722-epub-quantifier-corrections-20260930'
REMOTE = 'KokunoYumeto/OpenLogic-ar'
GITHUB = f'https://github.com/{REMOTE}/releases/tag/{TAG}'
PARENT = '764222630c19886f6963f682e8f41cc5671b9eaa'
CHANGED = (
    '20_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.tex',
    '21_OPENLOGIC_ar_R3_MSA_INTERNATIONAL_SOURCES.zip',
    '22_OpenLogic-Arabic-Complete-722-international.epub',
    '23_OPENLOGIC_ar_R3_MSA_MACHREK.tex',
    '24_OPENLOGIC_ar_R3_MSA_MACHREK_SOURCES.zip',
    '25_OpenLogic-Arabic-Complete-722-machrek.epub',
    '29_OPENLOGIC_ar_R3_COMPLETE_EPUB_SOURCE_AND_QA.zip',
)
TITLE = 'المنطق المفتوح بالعربية: تصحيح قواعد المكممات في الكتابين الإلكترونيين المعياريين'
NOTES = (
    '## الكتب الإلكترونية ومصادرها الدقيقة\n\n'
    'تضم الطبعتان المعياريتان الآن تصحيحي OLP-0087 المنشورين في PDF: استثناء الفرض '
    'المؤقت الذي يسقطه حذف الوجودي، وإغلاق حد الاستبدال، مع هامش التصحيح. بقيت '
    '٨١٦ من ٨١٩ ملفًا داخليًا في كل كتاب بلا تغيير، وحُفظت الصيغ السابقة وأشجار '
    'البرهان الأربعة ومعرّفات الروابط. بقي EPUB التراثي ومصدراه بلا تغيير.\n\n'
    'لكل كتاب ملف لاتخ تراكمي مباشر وحزمة مصادره الكاملة. مصادر المعياريتين '
    'هي النسخة الحالية المقابلة لتصحيحي المتن؛ أما مصادر التراثية فتطابق متن '
    'EPUB المحفوظ، وليست مصادر PDF التراثي المصحح في ٢٨ سبتمبر. تضم الحزمة '
    'المشتركة XHTML وMathML والخطوط والأنماط والبرنامج الذي أعاد الكتب الثلاثة '
    'بايتًا ببايت من الحزمة الفعلية.\n\n'
    'اجتاز الكتابان الجديدان EPUBCheck 5.3.0 بلا خطأ أو إنذار، وAce 1.4.6 '
    'بـ٨١٥ نتيجة ناجحة لكل منهما. فُحص القسم المصحح بصريًا في الطبعتين والانتقال '
    'إلى الهامش؛ ليس ذلك اختبارًا لكل جهاز قراءة أو مراجعة دلالية للكتاب كله.\n\n'
    'الترجمة الموروثة: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. تحويل EPUB '
    'الموروث وتجميعه: OpenAI Codex — GPT-6 Sol، جهد Ultra. المقابلة وتصحيح '
    'العبارتين ونقلهما والتحقق من هذه النسخة: OpenAI Codex — GPT-6.1 Sol، '
    'جهد Ultra. لم تقع مراجعة بشرية شاملة؛ إعادة فحص فترة GPT-6 Sol كلها '
    'ما زالت جارية، وكل اختيار مفتوح للتصحيح.\n\n'
    '[القارئان PDF الحاليان ومصدراهما وسجل المراجعة](https://github.com/KokunoYumeto/OpenLogic-ar/releases/tag/ar-openlogic-current-msa-and-review-20260930) '
    'باقية متاحة. [ابدأ مراجعة الاختيارات](https://github.com/KokunoYumeto/OpenLogic-ar/blob/ar-openlogic-current-msa-and-review-20260930/expert-review/2026-09-26-final-page-review/INDEX_AR.md) '
    '· [القائمة الكاملة](https://github.com/KokunoYumeto/OpenLogic-ar/blob/ar-openlogic-current-msa-and-review-20260930/expert-review/2026-09-26-final-page-review/DIRECTORY_READABLE_AR.md). '
    'روابط EPUB داخل ذلك الفهرس هي لقطة الإصدار السابق؛ الكتب المصححة هنا. '
    'تبقى كل الإصدارات السابقة ومصادرها وروابطها العامة محفوظة.\n'
)
for profile, label, stem, number in (
    ('international', 'المعيارية بالترميز الدولي', 'MSA_INTERNATIONAL', 20),
    ('machrek', 'المعيارية بترميز المشرق', 'MSA_MACHREK', 23),
    ('classical', 'التراثية المحفوظة ذات الصيغ من اليمين إلى اليسار', 'CLASSICAL_EASTERN_RTL', 26),
):
    base = f'https://github.com/{REMOTE}/releases/download/{TAG}/'
    NOTES += (f'\n{label}: [لاتخ الكامل المباشر]({base}{number}_OPENLOGIC_ar_R3_{stem}.tex) · '
              f'[حزمة المصدر الكامل]({base}{number+1}_OPENLOGIC_ar_R3_{stem}_SOURCES.zip) · '
              f'[EPUB]({base}{number+2}_OpenLogic-Arabic-Complete-722-{profile}.epub).\n')
NOTES += f'\n[مصادر EPUB الثلاثة الدقيقة وبرنامج إعادة البناء والفحوص](https://github.com/{REMOTE}/releases/download/{TAG}/29_OPENLOGIC_ar_R3_COMPLETE_EPUB_SOURCE_AND_QA.zip).\n'


def stage():
    package = json.loads((SOURCE / 'SOURCE_PACKAGE_RECEIPT.json').read_bytes())
    replay = json.loads((SOURCE / 'EXTRACTED_SOURCE_COLD_REPLAY.json').read_bytes())
    require(package['status'] == 'PASS_FRESH_CHECKERS_COLD_REPLAY_AND_EXACT_SOURCE' and
            replay['status'] == 'PASS_REBUILD_FROM_ACTUAL_CORRECTED_SOURCE_ZIP' and
            replay['source_zip_sha256'] == package['archive']['sha256'], 'Exact source gate failed')
    require(not STAGE.exists() and not STATE.exists(), 'Inspect existing stage, do not recreate')
    STAGE.mkdir(parents=True); STATE.mkdir(parents=True)
    accepted = {r['epub']['file']: r['epub'] for r in package['profiles']}
    files = []
    for name, original, size, sha in prior.baseline.FILES:
        if name.startswith(('20_', '21_', '23_', '24_')):
            original = CURRENT / original.name
            size, sha = SOURCE_IDS[original.name]
        elif name.startswith(('22_', '25_')):
            original = SOURCE / original.name
            size, sha = accepted[original.name]['bytes'], accepted[original.name]['sha256']
        elif name.startswith('28_'):
            original = OLD / CLASSICAL[0]; size, sha = CLASSICAL[1:]
        elif name.startswith('29_'):
            original = SOURCE / original.name
            size, sha = package['archive']['bytes'], package['archive']['sha256']
        require(identity(original) == {'file': original.name, 'bytes': size, 'sha256': sha}, 'Asset source drift')
        shutil.copyfile(original, STAGE / name)  # independent bytes, never hard-linked
        require(identity(STAGE / name) == {'file': name, 'bytes': size, 'sha256': sha}, 'Copied stage differs')
        files.append({'name': name, 'bytes': size, 'sha256': sha})
    zenodo.save(STATE / 'STAGE.json', {'status': 'PASS_EXACT_LOCAL_STAGE', 'files': files})
    (STATE / 'RELEASE_NOTES_AR.md').write_text(NOTES, encoding='utf-8', newline='\n')
    print(json.dumps({'status': 'PASS_EXACT_LOCAL_STAGE', 'files': len(files)}))


def git_paths():
    return ['README.md', 'build/refresh_msa_epub_quantifiers_20260930.py',
            'build/tests/test_refresh_msa_epub_quantifiers_20260930.py',
            'build/tests/test_publish_msa_epub_successor_20260930.py',
            'build/package_msa_epub_successor_20260930.py',
            'build/check_msa_epub_section_20260930.cjs',
            'build/publish_msa_epub_successor_20260930.py']


def github():
    probe = requests.get(f'https://api.github.com/repos/{REMOTE}/releases/tags/{TAG}', timeout=(20,60))
    require(probe.status_code == 404, 'Release absent state unproved; inspect without duplication')
    state = json.loads((STATE / 'GITHUB_TRANSACTION.json').read_bytes())
    require(state['status'] == 'PASS_ANONYMOUS_GITHUB_READBACK', 'Source commit must be publicly verified')
    result = subprocess.run(['gh','release','create',TAG,'--repo',REMOTE,'--target',state['commit'],
        '--title',TITLE,'--notes-file',str(STATE / 'RELEASE_NOTES_AR.md')]+
        [str(STAGE / r['name']) for r in prior.all_assets()], capture_output=True, text=True)
    require(result.returncode == 0, 'Creation attempt failed; inspect actual release before any retry')
    print(GITHUB)


def configure():
    prior.SOURCE = SOURCE; prior.STAGE = STAGE; prior.STATE = STATE
    prior.TAG = TAG; prior.GITHUB = GITHUB; prior.CHANGED = CHANGED
    prior.NOTES = NOTES; prior.TITLE = TITLE
    git.ROOT = ROOT; git.STATE = STATE / 'GITHUB_TRANSACTION.json'
    git.READBACK = STATE / 'GITHUB_COMMIT_READBACK.json'
    git.PACKAGE = SOURCE / 'SOURCE_PACKAGE_RECEIPT.json'
    git.EXPECTED_PARENT = PARENT; git.ALLOW_CHANGED = set(git_paths())
    git.selected_files = git_paths
    git.COMMIT_MESSAGE = 'تصحيح متني EPUB المعياريين ومزامنة مصادرهما الدقيقة'
    git.READBACK_STATUS = 'PASS_ANONYMOUS_GITHUB_EPUB_SUCCESSOR_EXACT_FILES'
    zenodo.STATE_DIR = STATE; zenodo.PREVIOUS = 23060802; zenodo.SUCCESSOR = True
    zenodo.EXPECTED_PREDECESSOR_FILES = 100; zenodo.REPLACEMENT_NAMES = CHANGED
    zenodo.assets = prior.changed_assets
    zenodo.VERSION = 'OLP-0722-AR-EPUB-QUANTIFIER-CORRECTIONS-20260930'
    zenodo.release.STAGE = STAGE; zenodo.release.GITHUB = GITHUB
    zenodo.PREVIEW = '00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf'
    zenodo.ORDER_PREFIX = ('00_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.pdf',
        '01_OPENLOGIC_ar_R3_MSA_INTERNATIONAL.tex','02_OPENLOGIC_ar_R3_MSA_INTERNATIONAL_SOURCES.zip',
        '03_OPENLOGIC_ar_R3_MSA_MACHREK.pdf','04_OPENLOGIC_ar_R3_MSA_MACHREK.tex',
        '05_OPENLOGIC_ar_R3_MSA_MACHREK_SOURCES.zip')
    def metadata(draft):
        value = dict(draft['metadata']); value.pop('doi',None); value.pop('prereserve_doi',None)
        value.update(title='المنطق المفتوح بالعربية: الطبعات الثلاث وسجل الاختيارات والكتب الإلكترونية المصححة',
            version=zenodo.VERSION,publication_date='2026-09-30',language='ara',access_right='open')
        # Do not append superseded current-status claims from the predecessor.
        value['description'] = prior.description_html() + '<div lang="ar" dir="rtl"><p>' + (
            'ملفات PDF الحالية محفوظة من الإصدار السابق، ومعاينة القراءة للقارئ الدولي. '
            'سجل المراجعة الكامل ذو القرارات الـ١٠٩٥ ومصادره باقٍ؛ روابط EPUB داخل '
            'الفهرس القديم لقطة سابقة، وروابط الكتابين المصححين هنا هي الحالية.') + '</p></div>'
        related = list(value.get('related_identifiers', []))
        if not any(r.get('identifier') == GITHUB for r in related):
            related.append({'identifier': GITHUB, 'relation':'isIdenticalTo', 'scheme':'url'})
        value['related_identifiers'] = related
        return value
    zenodo.metadata_for = metadata


def verify():
    zenodo.verify()
    state = json.loads((STATE / 'ZENODO_TRANSACTION.json').read_bytes())
    public = zenodo.public_record(int(state['draft_id']))
    entries = public['files']['entries']; checked = []
    # Also download the unchanged Classical book and its exact two source files.
    with requests.Session() as anonymous:
        anonymous.trust_env = False
        for row in prior.all_assets():
            if row['name'] in CHANGED:
                continue
            digest = hashlib.sha256(); count = 0
            with anonymous.get(entries[row['name']]['links']['content'], stream=True, timeout=(20,90)) as response:
                require(response.status_code == 200, 'Inherited Classical download failed')
                for block in response.iter_content(1048576):
                    count += len(block); require(count <= row['bytes'], 'Unexpected larger inherited asset')
                    digest.update(block)
            require((count, digest.hexdigest()) == (row['bytes'], row['sha256']), 'Inherited Classical bytes differ')
            checked.append({**row, 'anonymous': True})
    zenodo.save(STATE / 'ZENODO_CLASSICAL_UNCHANGED_READBACK.json', {
        'status': 'PASS_ANONYMOUS_EXACT_UNCHANGED_CLASSICAL_BOOK_AND_SOURCE_PAIR',
        'record_id': state['draft_id'], 'files': checked,
        'default_preview': public['files']['default_preview'],
        'reported_order': public['files'].get('order', [])})
    print(json.dumps({'status': 'PASS_ANONYMOUS_EXACT_UNCHANGED_CLASSICAL_BOOK_AND_SOURCE_PAIR', 'files': len(checked)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    actions = {'stage': stage, 'git-prepare': git.prepare, 'git-push': git.push,
        'git-verify': git.verify, 'github': github, 'github-verify': prior.github_verify,
        'prepare': zenodo.prepare, 'publish': zenodo.publish, 'verify': verify}
    parser.add_argument('action', choices=actions); action = parser.parse_args().action
    configure()
    try:
        actions[action]()
    except requests.RequestException as error:
        raise SystemExit('Transport failed ('+type(error).__name__+'); inspect and resume the same transaction') from None

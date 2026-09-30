"""Package the two exact source-grounded EPUB successors; retain Classical bytes.

Read one bounded predecessor archive, replace only verified members and the
four current MSA editable-source files, retain historical receipts explicitly,
then cold-rebuild all three books from the actual newly written source ZIP.
No TeX engine or full-workspace scan is used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from review_sol6_epub_20260930 import identity, require
from package_reviewed_epubs_20260930 import outcomes
from refresh_msa_epub_quantifiers_20260930 import DISCLOSURE

ROOT = HERE.parent
OLD = ROOT / 'tmp/epub/sol6-independent-review-20260930-r1'
CURRENT = ROOT / 'tmp/editable-current-msa-20260930-v13/primary/files'
OLD_ARCHIVE = (34565044, '317e3912a4a1aaf3e9754010cb0d78560a26a7422cbb40e0ee2edd9df45ec5df')
SOURCE_IDS = {
    'OPENLOGIC_ar_R3_MSA_INTERNATIONAL.tex': (4026031, 'cd57a37eab6d89308b1ba844f6c3a6ba630f46cec04cd4e61f25cc4fd17ae3c7'),
    'OPENLOGIC_ar_R3_MSA_INTERNATIONAL_SOURCES.zip': (15617812, '858ec8a4b65204a3aa0d54b392ef91633640f5a2725197ffdb4f8c536a76f7e3'),
    'OPENLOGIC_ar_R3_MSA_MACHREK.tex': (4025896, '63f755fa29eff4a5e7de057412b3553615d0610ec011e7a446ffff7385254469'),
    'OPENLOGIC_ar_R3_MSA_MACHREK_SOURCES.zip': (15608523, '300ccca3bd808f8a98fc41bb9116b29a3428fdc37c96dff589eb24306e5989c0'),
}
CLASSICAL = ('OpenLogic-Arabic-Complete-722-classical.epub',
             5084887, '3b1c3696d0597e16a6a372dedefa17083f274a1719072515c21b646556a1842b')


def checked_reports(directory, row):
    profile = row['profile']
    check_path = directory / ('epubcheck-' + profile + '.json')
    check = json.loads(check_path.read_bytes())
    counts = check['checker']
    require(counts['checkerVersion'] == '5.3.0' and
            counts['filename'] == row['successor']['file'] and
            all(counts[k] == 0 for k in ('nFatal', 'nError', 'nWarning')) and
            not check['messages'], 'Fresh EPUBCheck did not pass')
    ace_path = directory / ('ace-' + profile) / 'report.json'
    ace = json.loads(ace_path.read_bytes())
    results = list(outcomes(ace))
    require(ace['earl:assertedBy']['doap:release']['doap:revision'] == '1.4.6' and
            len(results) == 815 and set(results) == {'pass'}, 'Fresh Ace did not pass')
    return {'profile': profile, 'epub': row['successor'],
            'epubcheck': identity(check_path), 'ace': identity(ace_path),
            'ace_outcomes': len(results), 'freshly_checked': True}, {
        'qa/current-quantifier/epubcheck-' + profile + '.json': check_path.read_bytes(),
        'qa/current-quantifier/ace-' + profile + '.json': ace_path.read_bytes(),
    }


def package(directory):
    target = directory / 'OPENLOGIC_ar_R3_COMPLETE_EPUB_SOURCE_AND_QA.zip'
    require(not target.exists(), 'Inspect an existing archive instead of overwriting it')
    old_path = OLD / target.name
    old_id = identity(old_path)
    require((old_id['bytes'], old_id['sha256']) == OLD_ARCHIVE, 'Pinned predecessor archive changed')
    receipt_path = directory / 'BODY_SUCCESSOR_RECEIPT.json'
    body = json.loads(receipt_path.read_bytes())
    require(body['status'] == 'BODY_SUCCESSORS_PENDING_FRESH_CHECKERS_AND_EXACT_CURRENT_SOURCE_PACKAGE' and
            {r['profile'] for r in body['profiles']} == {'international', 'machrek'} and
            body['classical_epub_unchanged'], 'Wrong finite body successor')
    extra = {'qa/current-quantifier/BODY_SUCCESSOR_RECEIPT.json': receipt_path.read_bytes()}
    books = {}; checked = []
    for row in body['profiles']:
        path = directory / row['successor']['file']
        require(identity(path) == row['successor'], 'Checked EPUB drift')
        checked_row, reports = checked_reports(directory, row)
        checked.append(checked_row); extra.update(reports)
        with zipfile.ZipFile(path) as source:
            books[row['profile']] = {n: source.read(n) for n in source.namelist()}
    classical = OLD / CLASSICAL[0]
    require(identity(classical) == {'file': CLASSICAL[0], 'bytes': CLASSICAL[1], 'sha256': CLASSICAL[2]},
            'Unchanged Classical EPUB differs')
    checked.append({'profile': 'classical', 'epub': identity(classical), 'freshly_checked': False,
                    'reason_ar': 'بايتات النسخة التراثية لم تتغير؛ شهادات فحصها محفوظة بتاريخها، لا بوصفها فحوصًا جديدة.'})
    for name, expected in SOURCE_IDS.items():
        path = CURRENT / name; record = identity(path)
        require((record['bytes'], record['sha256']) == expected, 'Current MSA editable source differs')
        extra['latex/' + name] = path.read_bytes()
    ledger = ROOT / 'evidence/classical/terminology/SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json'
    require(identity(ledger) == body['choice_ledger'], 'Correction ledger differs')
    extra['qa/current-quantifier/CHOICE_LEDGER.json'] = ledger.read_bytes()
    extra['qa/current-quantifier/SOURCE_QUANTIFIER_RULES.tex'] = (
        ROOT / 'source/locale/ar/content/first-order-logic/natural-deduction/quantifier-rules.tex').read_bytes()
    visual_path = directory / 'VISUAL_SECTION_CHECK.json'
    visual = json.loads(visual_path.read_bytes())
    require(visual['status'] == 'PASS_TARGETED_TWO_PROFILE_RENDER_AND_FOOTNOTE' and
            {r['profile'] for r in visual['profiles']} == {'international', 'machrek'},
            'Targeted rendered check is absent')
    for row in visual['profiles']:
        require(row['epub'] == next(r['successor'] for r in body['profiles'] if r['profile'] == row['profile']),
                'Visual report is not bound to current bytes')
    extra['qa/current-quantifier/VISUAL_SECTION_CHECK.json'] = visual_path.read_bytes()
    extra['README_AR.md'] = (
        '# مصادر الكتب الإلكترونية العربية الكاملة\n\n'
        'تضم الحزمة الوحدات الـ٧٢٢ في ثلاث طبعات، مع ملفات XHTML وMathML والخطوط والأنماط '
        'القابلة للتحرير وملفات لاتخ الكاملة وحزم مصادرها. لإعادة إنتاج الكتب المنشورة '
        'بايتًا ببايت، فك الحزمة وشغّل `python REBUILD_EPUBS.py`؛ يلزم Python 3 وzlib، '
        'ولا يلزم محرّك لاتخ. يحفظ `SOURCE_MANIFEST.json` تجزئة كل ملف.\n\n'
        'تضم الطبعتان المعياريتان تصحيحي OLP-0087 المنشورين في PDF: استثناء الفرض الذي '
        'يسقطه حذف الوجودي، وإغلاق حد الاستبدال، مع هامش التصحيح. مصادر لاتخ لهما هي '
        'المصادر الحالية المنشورة مع PDF، لا مصادر سبتمبر القديمة. لا تعني هذه المطابقة '
        'مطابقة تنضيد EPUB وPDF. بقيت النسخة التراثية ومصادرها المقابلة لمتن EPUB بلا تغيير؛ '
        'لا يُقدم مصدر PDF التراثي المصحح في ٢٨ سبتمبر بوصفه مصدر EPUB الأقدم.\n\n'
        'الفحوص الجديدة للمعياريتين في `qa/current-quantifier/`. شهادات الحزمة السابقة '
        'في `qa/predecessor-provenance/` وما سبقها في المسارات التاريخية الأصلية؛ لا يُدَّعى '
        'أنها فحوص جديدة لبايتات تغيرت. صفحات البيان تبين منشأ كل طبعة.\n\n'
        + DISCLOSURE + '\n'
    ).encode('utf-8')
    extra['QA_SUMMARY_AR.md'] = (
        '# فحوص تصحيح متني EPUB المعياريين\n\n'
        'تغيرت عبارتان وهامش واحد فقط في وحدة OLP-0087، مع تحديث بيان الإنتاج. بقيت '
        '٨١٦ من ٨١٩ ملفًا داخليًا في كل طبعة معيارية بلا تغيير، وحُفظت أشجار البرهان '
        'الأربعة والصيغ السابقة ومعرّفات الروابط. اجتازت بايتات الكتابين الجديدين '
        'EPUBCheck 5.3.0 بلا خطأ أو إنذار، وAce 1.4.6: ٨١٥ نتيجة ناجحة لكل منهما. '
        'فُحص عرض القسم المصحح في الطبعتين والخطوط والانتقال إلى الهامش؛ لا يُدَّعى '
        'اختبار كل جهاز قراءة أو مراجعة دلالية شاملة. النسخة التراثية لم تتغير. '
        'أعيد بناء الكتب الثلاثة من محتويات هذه الحزمة الفعلية وطابقت تجزئاتها.\n\n'
        + DISCLOSURE + '\n'
    ).encode('utf-8')
    with zipfile.ZipFile(old_path) as old:
        old_manifest = json.loads(old.read('SOURCE_MANIFEST.json'))['members']
        expected_old = {r['path']: r for r in old_manifest}
        require(set(old.namelist()) == set(expected_old) | {'SOURCE_MANIFEST.json'}, 'Predecessor inventory differs')
        script = old.read('REBUILD_EPUBS.py').decode('utf-8')
        for row in body['profiles']:
            require(script.count(row['preimage']['sha256']) == 1, 'Rebuilder old pin not unique')
            script = script.replace(row['preimage']['sha256'], row['successor']['sha256'])
        extra['REBUILD_EPUBS.py'] = script.encode('utf-8')
        manifest = []
        with zipfile.ZipFile(target, 'w', allowZip64=True) as output:
            def write(name, raw):
                require(not name.startswith('/') and '..' not in Path(name).parts and
                        b'C:/Users/' not in raw and b'C:\\Users\\' not in raw, 'Unsafe public source member')
                item = zipfile.ZipInfo(name, (2026, 9, 30, 0, 0, 0))
                item.create_system = 3; item.external_attr = 0o100644 << 16
                item.compress_type = zipfile.ZIP_DEFLATED
                output.writestr(item, raw, compresslevel=9)
                manifest.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
            for name in old.namelist():
                if name == 'SOURCE_MANIFEST.json':
                    continue
                raw = old.read(name); pin = expected_old[name]
                require((len(raw), hashlib.sha256(raw).hexdigest()) == (pin['bytes'], pin['sha256']),
                        'Predecessor source member differs')
                if name in extra:
                    raw = extra.pop(name)
                elif name.startswith('epub-source/'):
                    _, profile, member = name.split('/', 2)
                    if profile in books:
                        raw = books[profile][member]
                elif name.startswith('qa/current/'):
                    name = 'qa/predecessor-provenance/' + name[len('qa/current/'):]
                write(name, raw)
            for name, raw in sorted(extra.items()):
                write(name, raw)
            write('SOURCE_MANIFEST.json', (json.dumps({'schema': 'exact-epub-quantifier-source-v1',
                'members': sorted(manifest, key=lambda r: r['path'])}, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
    with zipfile.ZipFile(target) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) == len(manifest), 'Duplicate/missing new source member')
        for row in manifest:
            raw = archive.read(row['path'])
            require((len(raw), hashlib.sha256(raw).hexdigest()) == (row['bytes'], row['sha256']),
                    'New packaged source differs')
        cold = directory / 'cold-source-replay'
        require(not cold.exists(), 'Existing replay must be inspected, not overwritten')
        cold.mkdir()
        archive.extractall(cold)
    process = subprocess.run([sys.executable, '-X', 'utf8', str(cold / 'REBUILD_EPUBS.py')],
                             capture_output=True, text=True, encoding='utf-8', timeout=90)
    require(process.returncode == 0, 'Actual extracted-source cold rebuild failed: '+process.stderr[:800])
    replayed = []
    for row in checked:
        record = identity(cold / 'rebuilt' / row['epub']['file'])
        require(record == row['epub'], 'Extracted source did not reproduce exact EPUB')
        replayed.append(record)
    receipt = {'schema': 'msa-epub-successor-exact-source-v1',
        'status': 'PASS_FRESH_CHECKERS_COLD_REPLAY_AND_EXACT_SOURCE',
        'model': 'GPT-6.1 Sol', 'effort': 'Ultra', 'archive': identity(target),
        'members': len(manifest), 'profiles': checked, 'source_files': SOURCE_IDS,
        'all_three_extracted_source_replays_byte_identical': replayed,
        'classical_unchanged': True, 'human_review_claimed': False}
    (directory / 'SOURCE_PACKAGE_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (directory / 'EXTRACTED_SOURCE_COLD_REPLAY.json').write_text(json.dumps({
        'status': 'PASS_REBUILD_FROM_ACTUAL_CORRECTED_SOURCE_ZIP',
        'source_zip_sha256': receipt['archive']['sha256'], 'files': replayed}, indent=2)+'\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    result = package(parser.parse_args().directory)
    print(json.dumps({'status': result['status'], 'archive': result['archive'], 'members': result['members']}))

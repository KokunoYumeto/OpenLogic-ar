"""Package the exact disclosure-corrected EPUBs with fresh checker evidence.

Historical checker receipts stay labelled as historical; no old PASS is
represented as a test of new bytes. The archive contains editable internals,
the directly published cumulative LaTeX/source pairs, and an exact rebuilder.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from review_sol6_epub_20260930 import BASELINE, BASELINE_ID, EXPECTED, DISCLOSURE_AR, identity, pack, require


def outcomes(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'earl:outcome':
                yield child
            else:
                yield from outcomes(child)
    elif isinstance(value, list):
        for child in value:
            yield from outcomes(child)


def package(directory: Path) -> dict:
    target = directory / 'OPENLOGIC_ar_R3_COMPLETE_EPUB_SOURCE_AND_QA.zip'
    require(not target.exists(), 'Refusing to overwrite source archive')
    old_id = identity(BASELINE)
    require((old_id['bytes'], old_id['sha256']) == BASELINE_ID, 'Baseline source changed')
    review_path = directory / 'REVIEW_RECEIPT.json'
    review = json.loads(review_path.read_bytes())
    require(review['status'] == 'CORRECTED_EPUBS_PENDING_FRESH_CHECKERS_AND_SOURCE_PACKAGING', 'Wrong review state')
    rows = {r['profile']: r for r in review['profiles']}
    extra = {'qa/current/REVIEW_RECEIPT.json': review_path.read_bytes()}
    checked = []
    current_epubs = {}
    for profile, (name, old_sha) in EXPECTED.items():
        epub = directory / name
        require(identity(epub) == rows[profile]['successor'], 'Revised EPUB changed')
        check_path = directory / ('epubcheck-' + profile + '.json')
        check = json.loads(check_path.read_bytes())
        counts = check['checker']
        require(counts['checkerVersion'] == '5.3.0' and counts['filename'] == name and
                all(counts[k] == 0 for k in ['nFatal', 'nError', 'nWarning']) and not check['messages'], 'Fresh EPUBCheck failed')
        ace_path = directory / ('ace-' + profile) / 'report.json'
        ace = json.loads(ace_path.read_bytes())
        require(ace['earl:assertedBy']['doap:release']['doap:revision'] == '1.4.6', 'Ace version differs')
        result_outcomes = list(outcomes(ace))
        require(len(result_outcomes) == 815 and set(result_outcomes) == {'pass'}, 'Fresh Ace outcome failed')
        for kind, path in [('epubcheck', check_path), ('ace', ace_path)]:
            extra['qa/current/' + kind + '-' + profile + '.json'] = path.read_bytes()
        with zipfile.ZipFile(epub) as source:
            current_epubs[profile] = {n: source.read(n) for n in source.namelist()}
        replay = directory / ('SOURCE-REPLAY-' + name)
        pack(current_epubs[profile], replay)
        require(identity(replay)['sha256'] == rows[profile]['successor']['sha256'], 'Revised cold replay differs')
        checked.append({'profile': profile, 'epub': identity(epub), 'epubcheck': identity(check_path),
                        'ace': identity(ace_path), 'ace_outcomes': len(result_outcomes), 'cold_replay_byte_identical': True})
    with zipfile.ZipFile(BASELINE) as old:
        script = old.read('REBUILD_EPUBS.py').decode('utf-8')
        for profile, (_, old_sha) in EXPECTED.items():
            require(script.count(old_sha) == 1, 'Rebuilder pin is ambiguous')
            script = script.replace(old_sha, rows[profile]['successor']['sha256'])
        extra['REBUILD_EPUBS.py'] = script.encode('utf-8')
        original_readme = old.read('README_AR.md').decode('utf-8')
        old_disclosure = 'أُنجزت الترجمة والتصحيح الآلي بواسطة OpenAI Codex — GPT-5.6 Sol، بمستوى جهد Ultra؛ ولا يُفهم من ذلك أنها خضعت لمراجعة بشرية.'
        require(original_readme.count(old_disclosure) == 1, 'Old README disclosure differs')
        extra['README_AR.md'] = (original_readme.replace(old_disclosure, DISCLOSURE_AR) +
            '\nفحوص ٣٠ سبتمبر محفوظة في `qa/current/`، وإيصالات ٢٥ سبتمبر محفوظة في '
            '`qa/historical-20260925/` بوصفها شهادات على النسخة السابقة، لا فحوصًا للملفات الجديدة. '
            'مصادر LaTeX المقابلة لمتن EPUB هي النسخة المثبتة في ٢٥ سبتمبر؛ '
            'تصحيح البيان لا يغيّر متنها أو رموزها.\n').encode('utf-8')
        extra['QA_SUMMARY_AR.md'] = (
            '# فحص النسخة المصححة من الكتب الإلكترونية\n\n'
            'أعيد بناء الكتب الثلاثة القديمة من أرشيف مصادرها، وطابقت تجزئاتها المنشورة. '
            'صُحِّح بيان الإنتاج فقط في ملف الحزمة وصفحة البيان بكل طبعة؛ بقيت الملفات '
            'الأخرى وعددها ٨١٧ بايتًا ببايت. اجتازت النسخ المصححة EPUBCheck 5.3.0 '
            'من غير خطأ أو إنذار، وAce 1.4.6 من غير إخفاق، وأعيد بناؤها بايتًا ببايت. '
            'يحفظ الفحص المستقل أيضًا ٨١٢ مستندًا في كل طبعة وتطابق الروابط المحلية '
            'والصيغ الرياضية؛ لا يساوي ذلك مراجعة دلالية شاملة أو قبولًا بصريًا لجميع الصفحات.\n\n'
            + DISCLOSURE_AR + '\n').encode('utf-8')
        names = {}
        for name in old.namelist():
            if name in extra:
                names[name] = extra.pop(name)
            elif name.startswith('epub-source/'):
                _, profile, member = name.split('/', 2)
                names[name] = current_epubs[profile][member]
            elif name.startswith('qa/'):
                names['qa/historical-20260925/' + name[3:]] = old.read(name)
            else:
                names[name] = old.read(name)
        names.update(extra)
    # Keep memory bounded: the source archive is under 300 MB; no workspace scan.
    manifest = [{'path': n, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} for n, raw in sorted(names.items())]
    names['SOURCE_MANIFEST.json'] = (json.dumps({'schema':'exact-reviewed-epub-source-v1','members':manifest},ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with zipfile.ZipFile(target, 'w', allowZip64=True) as output:
        for name, raw in sorted(names.items()):
            require(b'C:/Users/' not in raw and b'C:\\Users\\' not in raw, 'Personal path in public archive: ' + name)
            info = zipfile.ZipInfo(name, (2026,9,30,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, raw, compresslevel=9)
    with zipfile.ZipFile(target) as output:
        require(len(output.namelist()) == len(set(output.namelist())) == len(names), 'Packaged inventory differs')
        for row in manifest:
            raw = output.read(row['path'])
            require((len(raw),hashlib.sha256(raw).hexdigest()) == (row['bytes'],row['sha256']), 'Packaged member bytes differ')
    receipt = {'schema':'reviewed-epub-exact-source-package-v1','status':'PASS_FRESH_CHECKERS_COLD_REPLAY_AND_EXACT_SOURCE',
               'model':'GPT-6.1 Sol','effort':'Ultra','archive':identity(target),'members':len(names),'profiles':checked,
               'historical_receipts_relabelled':True,'direct_cumulative_tex_and_source_zip_pairs_present':6}
    with (directory/'SOURCE_PACKAGE_RECEIPT.json').open('x',encoding='utf-8',newline='\n') as output:
        output.write(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    return receipt


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,required=True)
    print(json.dumps(package(parser.parse_args().directory),ensure_ascii=True))

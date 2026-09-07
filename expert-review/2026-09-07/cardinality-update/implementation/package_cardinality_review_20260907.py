"""One bounded, additive public snapshot of the applied five-unit source batch."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from build import package_expert_review_publication_20260907 as projection

REPO = Path(__file__).resolve().parents[1]
STAGE = REPO.parent.parent / 'openlogic-arabic-review-publication-20260907'
PUBLIC = STAGE / 'expert-review/2026-09-07'
UPDATE = PUBLIC / 'cardinality-update'
OLD_COMMIT = '2fab516ea997f315483e768fe9c846d252589b7b'
LEDGERS = [
    'OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907',
    'OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907',
    'OLP0034_REDUCTION_CONSTRUCTIONS_20260907',
    'OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907',
]
TESTS = [
    'test_pairing_constructions_0031_0032_20260907',
    'test_nonenumerability_constructions_0033_20260907',
    'test_reduction_constructions_0034_20260907',
    'test_equinumerosity_constructions_0035_20260907',
]
BASE = 'https://github.com/KokunoYumeto/OpenLogic-ar/blob/main/expert-review/2026-09-07/'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def put(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(raw, str):
        raw = raw.encode('utf-8')
    path.write_bytes(raw)


def save(path, value):
    put(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def identity(path, root):
    return {'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size,
            'sha256': projection.hash_file(path)}


def display(raw):
    """Finite semantic projection of the exact 25 patches, never a TeX parser."""
    value = raw
    for token, arabic in {'enumerable': 'قابلة للتعداد', 'nonenumerable': 'غير قابلة للتعداد',
                          'bijective': 'تقابلية', 'surjective': 'شاملة', 'element': 'عنصر'}.items():
        value = value.replace('!!{' + token + '}', arabic).replace('!!a{' + token + '}', arabic)
    value = value.replace(r'^\text{th}', 'ᵗʰ').replace(r'f^{-1}', 'f⁻¹')
    value = re.sub(r'\\comp\{([^{}]+)\}\{([^{}]+)\}', r'\2∘\1', value)
    value = re.sub(r'\\tuple\{([^{}]+)\}', r'⟨\1⟩', value)
    value = value.replace(r'\Pow{\PosInt}', '℘(ℤ⁺)').replace(r'\Bin^\omega', '𝔹^ω')
    value = re.sub(r'\\emph\{([^{}]+)\}', r'\1', value)
    for command, symbol in {r'\emptyset': '∅', r'\PosInt': 'ℤ⁺', r'\colon': ':', r'\to': '→', r'\in': '∈'}.items():
        value = value.replace(command, symbol)
    value = ' '.join(value.replace('$', '').replace('~', ' ').split())
    assert not re.search(r'\\|!!|[{}]', value), 'Unsupported display input: ' + value
    return value


def decision_patches(ledger, decision):
    matches = []
    for transaction in ledger['transactions']:
        for patch in transaction['patches']:
            owned = decision['decision_id'] in patch.get('decision_ids', [])
            if 'occurrences' in decision and not patch.get('decision_ids'):
                owned = (transaction['path'] == decision['occurrences'][0]['target_path']
                         and patch['before'] == decision['before_arabic'])
            if owned:
                matches.append((transaction, patch))
    assert matches, decision['decision_id']
    return matches


def prepare():
    assert not UPDATE.exists(), 'Existing update must be inspected; no automatic overwrite'
    old_manifest_path = PUBLIC / 'PUBLICATION_MANIFEST.json'
    old_raw = old_manifest_path.read_bytes()
    assert sha(old_raw) == '489e8d6e352e8ea75d9551fb8d77b859d9f507ca14f2d055168931d15ebabee4'
    old = json.loads(old_raw)
    for row in old['files']:
        assert identity(PUBLIC / row['path'], PUBLIC) == row
    # Check source definitions for every finite rendering operation.
    config = (REPO / 'source/open-logic-config.sty').read_text(encoding='utf-8')
    ar_config = (REPO / 'source/locale/ar/open-logic-config.sty').read_text(encoding='utf-8')
    assert r'\DeclareDocumentCommand \comp { m m }{#2 \circ #1}' in config
    assert r'\DeclareDocumentMacro \Bin {\mathbb{B}}' in config
    assert r'\DeclareDocumentCommand \Pow { m }{\wp(#1)}' in config
    for token, term in {'enumerable': 'قابلة للتعداد', 'nonenumerable': 'غير قابلة للتعداد',
                        'bijective': 'تقابلية', 'surjective': 'شاملة', 'element': 'عنصر'}.items():
        assert '\\settexttoken{' + token + '}{' + term + '}' in ar_config
    tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', *['build.tests.' + t for t in TESTS]],
                           cwd=REPO, capture_output=True, timeout=60)
    assert tests.returncode == 0, tests.stderr.decode('utf-8', errors='replace')
    assert b'Ran 42 tests' in tests.stderr
    UPDATE.mkdir()
    put(UPDATE / 'history/PREVIOUS_PUBLICATION_MANIFEST.json', old_raw)
    for name in ('EXPERT_REVIEW_START_HERE.md', 'ALL_RECORDED_CHOICES.md'):
        put(UPDATE / 'history' / name, (PUBLIC / name).read_bytes())
    source_rows, raw_rows, cards, decisions = [], [], [], []
    for stem in LEDGERS:
        original = REPO / 'evidence/classical/repairs' / (stem + '.json')
        ledger = json.loads(original.read_bytes())
        raw_rows.append({'name': stem + '.json', 'original_sha256': sha(original.read_bytes())})
        put(UPDATE / 'ledgers' / original.name, projection.private_projection(original.read_text(encoding='utf-8')))
        for t in ledger['transactions']:
            raw = (REPO / t['path']).read_bytes()
            assert (len(raw), sha(raw)) == (t['after_bytes'], t['after_sha256'])
            previous = raw.decode('utf-8')
            for p in reversed(t['patches']):
                assert previous.count(p['after']) == 1
                previous = previous.replace(p['after'], p['before'], 1)
            before = previous.encode('utf-8')
            assert (len(before), sha(before)) == (t['before_bytes'], t['before_sha256'])
            forward = previous
            for p in t['patches']:
                assert forward.count(p['before']) == 1
                forward = forward.replace(p['before'], p['after'], 1)
            assert forward.encode('utf-8') == raw
            for phase, data in (('current', raw), ('before', before)):
                destination = UPDATE / 'sources' / phase / t['path']
                put(destination, data)
                source_rows.append(identity(destination, UPDATE))
        for d in ledger['decisions']:
            matches = decision_patches(ledger, d)
            reason = d.get('rationale_arabic') or d.get('rationale_ar') or d['rationale']
            question = d.get('expert_question_ar') or d.get('expert_question')
            if not question and 'NFC' in d['decision_id']:
                question = 'هل ظهر اختلاف في عرض الحركات بعد ترتيبها القانوني؟ لم يتغير اللفظ أو المعنى.'
            assert reason and question and d['open_to_correction']
            card = [f'## {d["decision_id"]}', '',
                    f'{d["unit_id"]} — ' + ('العربية المعاصرة المشتركة بين نسختي الترميز' if d['edition'] == 'msa' else 'العربية ذات الأسلوب التراثي'), '']
            for t, p in matches:
                location = p['after_location']
                raw = (REPO / t['path']).read_bytes()
                start = location['byte_start']
                assert raw[start:location['byte_end']].decode('utf-8') == p['after']
                assert raw[:start].count(b'\n') + 1 == location['line_start']
                url = 'sources/current/' + t['path'] + '#L' + str(location['line_start'])
                card.extend([f'[الموضع: السطر {location["line_start"]}]({url})', '',
                             'السابق: ' + display(p['before']), '', 'الآن: ' + display(p['after']), ''])
            card.extend(['سبب الاختيار: ' + reason, '', 'سؤال للمراجعة: ' + question, '',
                         f'[السجل الدقيق والشواهد والبدائل](ledgers/{stem}.json)', ''])
            cards.append('\n'.join(card))
            decisions.append({'id': d['decision_id'], 'unit': d['unit_id'], 'edition': d['edition'],
                              'status': 'applied-open-to-correction', 'locations': len(matches)})
    assert len(decisions) == 23 and sum(d['locations'] for d in decisions) == 25
    assert len(source_rows) == 20
    assert len({d['id'] for d in decisions}) == 23
    # Frozen English witnesses are copied from the previously checked public snapshot.
    for filename in ('pairing.tex', 'pairing-alt.tex', 'non-enumerability.tex', 'reduction.tex', 'equinumerous-sets.tex'):
        relative = 'content/sets-functions-relations/size-of-sets/' + filename
        original = projection.ENGLISH / relative
        destination = UPDATE / 'sources/english' / relative
        put(destination, original.read_bytes())
        source_rows.append(identity(destination, UPDATE))
    for name in ('source/open-logic-config.sty', 'source/locale/ar/open-logic-config.sty'):
        put(UPDATE / 'sources/current' / name, (REPO / name).read_bytes())
    for test in TESTS:
        origin = REPO / 'build/tests' / (test + '.py')
        put(UPDATE / 'implementation' / origin.name, projection.private_projection(origin.read_text(encoding='utf-8')))
    put(UPDATE / 'implementation' / Path(__file__).name, projection.private_projection(Path(__file__).read_text(encoding='utf-8')))
    put(UPDATE / 'FOCUSED_TEST_RESULTS.txt', projection.private_projection(tests.stderr.decode('utf-8', errors='replace')))
    put(UPDATE / 'ALL_23_DECISIONS.md', '# مواضع المراجعة: ٢٣ قرارًا مطبقًا\n\n'
        'لكل قرار موضع وصياغة سابقة وجديدة وسبب وسؤال مفتوح للتصحيح. أرقام المواضع هي أسطر المصدر، لا صفحات PDF. '
        'هذه القراءة تستعمل رموزًا دولية واضحة لعرض المقارنة؛ لا تمثل إخراج الصيغ النهائي من اليمين إلى اليسار.\n\n'
        'التعليلات تخص التصحيحات المسجلة الآن؛ ولا تزعم معرفة نيات المترجم الأول أو ورود الجمل كاملة في المعاجم. '
        'تبين السجلات الدقيقة ما فُحص مباشرة وما نُقل من مراجعات موثقة سابقة.\n\n' + '\n'.join(cards))
    put(UPDATE / 'README.md', '# Arabic Open Logic: applied review update\n\n'
        '[Read all 23 decisions, with wording, location and reasons](ALL_23_DECISIONS.md).\n\n'
        'This update covers pairing, alternative pairing, non-enumerability, reduction and equinumerosity. '
        'Twenty-five exact replacements in ten Arabic source files are applied and checked by 42 focused tests. '
        'Seven entries supersede the seven pairing proposals in the earlier 1,073-entry snapshot; the other sixteen are additional correction records. '
        'Counts refer to records, not unique words. Four records concern Unicode mark ordering.\n\n'
        'Useful starting points: the nonempty-set qualification (OLP-0033), the distinction between range and codomain '
        '(OLP-0034), the referent of the empty-set counter-assumption (OLP-0035), and the disclosure of two source '
        'corrections in pairing (OLP-0032). The remaining entries cover agreement and idiomatic phrasing.\n\n'
        'The modern-Arabic changes apply to the shared source for the two existing notation readers. '
        'Current and exact prior Arabic sources, frozen English witnesses, ledgers and focused test results accompany this update. '
        'The earlier snapshot remains unchanged and should be read as historical wherever these entries supersede it.\n\n'
        'This is shareable work in progress, not a complete audit or final Classical edition. Existing PDFs have not been '
        'rebuilt with these corrections; final book page references and RTL typography remain unfinished. '
        'Specialist feedback is welcome for later revisions.\n\n'
        '[Full register and earlier records](../ALL_RECORDED_CHOICES.md).\n')
    save(UPDATE / 'BATCH_MANIFEST.json', {'status': 'PASS_42_FOCUSED_TESTS_EXACT_SOURCE_AND_LOCATION_READBACK',
         'decisions': decisions, 'sources': source_rows, 'original_ledger_identities': raw_rows,
         'projection': 'Metadata paths are privacy-projected; literal source bytes and SHA identities are exact.',
         'reader_pdfs_rebuilt': False, 'full_audit_complete': False})
    put(PUBLIC / 'EXPERT_REVIEW_START_HERE.md', '# Arabic translation review — start here\n\n'
        '[Start with the latest corrected choices](cardinality-update/README.md). '
        '[Full recorded list](ALL_RECORDED_CHOICES.md).\n\n'
        'The latest update gives 23 applied decisions: wording, exact source location, reason and an open question. '
        'Seven replace proposals previously marked unapplied.\n\n'
        '[Earlier priority choices](integrated-review/EXPERT_REVIEW_START_HERE.md) remain available. '
        'This is an unfinished working register: suitable to share for feedback, not a completed audit or rebuilt Classical book.\n')
    put(PUBLIC / 'ALL_RECORDED_CHOICES.md', '# Arabic translation review — full recorded list\n\n'
        'Read the latest corrections first, then the earlier complete recorded snapshot. '
        'Every listed choice remains open to correction.\n\n'
        '- [Latest: all 23 applied decisions, locations and reasons](cardinality-update/ALL_23_DECISIONS.md).\n'
        '- [Earlier 1,073-entry recorded snapshot, organized by section](integrated-review/reviewer-index/README.md).\n'
        '- [Earlier sortable occurrence table](integrated-review/EXPERT_REVIEW_OCCURRENCES.csv).\n'
        '- [Earlier machine-readable register](integrated-review/EXPERT_REVIEW_INDEX.json.gz).\n\n'
        'Seven of the latest decisions supersede the seven pairing proposals in the earlier snapshot; sixteen are additional '
        'correction records. Do not count superseded records twice or read their old proposal status as current. '
        'The update includes four Unicode mark-ordering records. These are counts of records, not unique terms.\n\n'
        'The earlier snapshot reports 902 flagged choices, 534 unresolved lexical locations and 110 flags without explicit '
        'questions. Those are historical snapshot counts, not a new full-corpus audit. The 23 latest decisions all supply '
        'exact source locations, reasons and questions. Final PDF page mapping, exhaustive audit and the Classical reader '
        'are unfinished; existing reader PDFs have not been rebuilt with these changes.\n\n'
        '[Start here](EXPERT_REVIEW_START_HERE.md).\n')
    # Check every new local link. Historical entry copies deliberately retain old relative paths.
    links = 0
    for origin in [UPDATE / 'README.md', UPDATE / 'ALL_23_DECISIONS.md', PUBLIC / 'EXPERT_REVIEW_START_HERE.md', PUBLIC / 'ALL_RECORDED_CHOICES.md']:
        body = origin.read_text(encoding='utf-8')
        assert projection.private_projection(body) == body
        for url in projection.all_links(body):
            path, _, fragment = url.partition('#')
            target = (origin.parent / path).resolve()
            assert target.is_relative_to(PUBLIC) and target.is_file(), url
            if fragment:
                assert re.fullmatch(r'L\d+', fragment)
                assert int(fragment[1:]) <= len(target.read_bytes().splitlines())
            links += 1
    # All original files remain byte-identical except the two explicitly updated entry pages.
    for row in old['files']:
        if row['path'] not in ('EXPERT_REVIEW_START_HERE.md', 'ALL_RECORDED_CHOICES.md'):
            assert identity(PUBLIC / row['path'], PUBLIC) == row
    all_files = [p for p in sorted(PUBLIC.rglob('*')) if p.is_file() and p != old_manifest_path]
    save(old_manifest_path, {'schema': 'arabic-expert-review-cardinality-update-v1',
         'status': 'CHECKED_WORKING_REGISTER_WITH_APPLIED_UPDATE', 'predecessor_commit': OLD_COMMIT,
         'latest_applied_decisions': 23, 'superseded_proposals': 7, 'latest_patch_locations': 25,
         'new_local_links_checked': links, 'reader_pdfs_rebuilt': False,
         'files': [identity(p, PUBLIC) for p in all_files]})
    archive = STAGE / 'OPENLOGIC_ARABIC_EXPERT_REVIEW_CARDINALITY_20260907.zip'
    assert not archive.exists()
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for origin in sorted(PUBLIC.rglob('*')):
            if origin.is_file():
                item = zipfile.ZipInfo(origin.relative_to(PUBLIC).as_posix(), date_time=(2026, 9, 7, 0, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(item, origin.read_bytes())
    expected = {p.relative_to(PUBLIC).as_posix(): identity(p, PUBLIC) for p in PUBLIC.rglob('*') if p.is_file()}
    with zipfile.ZipFile(archive) as bundle:
        assert len(bundle.namelist()) == len(set(bundle.namelist()))
        assert set(bundle.namelist()) == set(expected)
        for name, row in expected.items():
            raw = bundle.read(name)
            assert (len(raw), sha(raw)) == (row['bytes'], row['sha256'])
    guide = STAGE / 'START_HERE_AND_FULL_CARDINALITY_LIST_20260907.md'
    put(guide, '# Arabic translation review\n\n'
        f'[Start here]({BASE}EXPERT_REVIEW_START_HERE.md).\n\n'
        f'[Full recorded list]({BASE}ALL_RECORDED_CHOICES.md).\n\n'
        'Includes the latest 23 applied decisions and the preserved earlier register. '
        'Open to correction; exact source lines are given, not unverified PDF pages. '
        'The full audit and final Classical reader remain unfinished. Existing PDFs are unchanged.\n')
    sums = STAGE / 'EXPERT_REVIEW_CARDINALITY_SHA256_20260907.txt'
    put(sums, ''.join(projection.hash_file(p) + '  ' + p.name + '\n' for p in (archive, guide)))
    receipt = {'status': 'PASS_LOCAL_EXACT_PACKAGE', 'files': [identity(p, STAGE) for p in (archive, guide, sums)],
               'public_package_files': len(expected), 'source_files_in_update': 25,
               'latest_decisions': 23, 'latest_literal_replacements': 25, 'focused_tests': 42,
               'new_local_links_checked': links, 'manifest_sha256': projection.hash_file(old_manifest_path),
               'predecessor_commit': OLD_COMMIT, 'reader_pdfs_rebuilt': False}
    save(STAGE / 'CARDINALITY_PACKAGE_RECEIPT.json', receipt)
    print(json.dumps(receipt))


if __name__ == '__main__':
    prepare()

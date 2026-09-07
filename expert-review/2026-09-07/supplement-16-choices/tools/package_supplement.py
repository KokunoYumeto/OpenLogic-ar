"""Build this finite source-review supplement from explicit input roots.

Only writes below this script's supplement directory. No network/build/Git.
The public ledgers are privacy-normalized projections; original bytes stay in
the source evidence tree and their hashes are recorded in PROJECTION_RECEIPT.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907",
    "OLP0022_0028_0029_ADJECTIVE_CONSTRUCTIONS_20260907",
    "OLP0394_0399_0400_0404_0409_MODAL_SCOPE_20260907",
)
TESTS = (
    "test_classical_function_constructions_0021_0022_0024.py",
    "test_classical_adjective_constructions_0022_0028_0029.py",
    "test_modal_scope_0394_0399_0400_0404_0409.py",
)
LINK = re.compile(r'\]\(([^)]+)\)')
TITLES = (
    "ترتيب اللاحق والسابق / Successor order",
    "دالة الهوية / Identity predicate",
    "التعريف بحسب الزوجية / Piecewise predicate",
    "الدوال التقابلية / Bijective relative clause",
    "شرط التقابل / Bijection biconditional",
    "تعريف المعكوس / Inverse predicate",
    "الدوال الشاملة / Surjective opening",
    "المجموعات القابلة للتعداد / Enumerable sets",
    "كل من الدالتين شاملة / Dual surjective maps",
    "عناصر القائمة ورتبها / Zero-indexed elements",
    "قيمة المثال: كاذب / Final value: False",
    "شرط الشبكة m≥2 / Grid domain",
    "تناهي المقدمات / Finite-premise converse",
    "خلو المواضع الأخرى / Empty sequent positions",
    "ترتيب الضرورة والإمكان / Modal order",
    "صدق عبارة الضرورة / Necessity truth",
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": digest(raw)}


def write(value, raw):
    target = (ROOT / value).resolve()
    if not target.is_relative_to(ROOT) or target == ROOT:
        raise ValueError("out-of-supplement write")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)


def dump(value, data):
    write(value, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())


def slug(heading):
    text = heading.strip().lower()
    text = ''.join(c for c in text if not unicodedata.category(c).startswith(('P', 'S')) or c in '_-')
    return text.replace(' ', '-')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--english', type=Path, required=True)
    args = parser.parse_args()
    repo, english = args.repo.resolve(), args.english.resolve()
    if (ROOT / 'MANIFEST.json').exists():
        raise ValueError('Completed supplement exists; do not overwrite')
    raw_receipt = (repo / 'evidence/classical/repairs/CONSOLIDATED_SOURCE_CHECKS_20260907.json').read_bytes()
    receipt = json.loads(raw_receipt)
    if (receipt['status'], receipt['tests_run'], receipt['exit_code'], receipt['decision_count'],
            receipt['literal_patch_count'], receipt['distinct_changed_source_files']) != (
                'PASS_34_SOURCE_ONLY_TESTS', 34, 0, 16, 26, 15):
        raise ValueError('Not the verified finite source batch')
    original_ids = {x['path']: x for x in receipt['artifacts'] + receipt['current_changed_sources']}
    projections = []

    def read_checked(value):
        raw = (repo / value).read_bytes()
        if identity(value, raw) != original_ids[value]:
            raise ValueError('Verified input drift: ' + value)
        return raw

    def project(text):
        # These are provenance labels, not fabricated public download URLs.
        for source, replacement in ((english, 'english'), (repo, '.'),
                                    (repo.parent.parent.parent / 'interlanguage-task-state', 'private-evidence')):
            for variant in (str(source), source.as_posix(), str(source).replace('\\', '\\\\')):
                text = text.replace(variant, replacement)
        # Task-state trees are not distributed: keep their suffixes as labelled
        # private provenance, with no local drive or personal directory name.
        text = re.sub(r'[A-Za-z]:(?:/|\\\\|\\)interlanguage-task-state', 'private-evidence', text)
        text = re.sub(r'[A-Za-z]:(?:/|\\\\|\\)Users(?:/|\\\\|\\)[^/\\\s"<>]+', '[private-user]', text, flags=re.I)
        user = os.environ.get('USERNAME', '')
        if len(user) >= 3:
            text = re.sub(re.escape(user), '[user]', text, flags=re.I)
        # Remaining private production roots are provenance only. Do not copy
        # third-party canon material just to make a local authority path resolve.
        text = re.sub(r'[A-Za-z]:(?:/|\\\\|\\)', 'private-path/', text)
        return text

    def publish(value, raw, *, projection=False):
        output = project(raw.decode()).encode() if projection else raw
        write(value, output)
        projections.append({"path": value, "original_bytes": len(raw), "original_sha256": digest(raw),
                            "published_bytes": len(output), "published_sha256": digest(output),
                            "mode": 'privacy-projection' if output != raw else 'exact-original'})

    ledgers, guides = [], []
    for name in NAMES:
        value = 'evidence/classical/repairs/' + name
        raw = read_checked(value + '.json')
        ledgers.append(json.loads(raw))
        publish(value + '.json', raw, projection=True)
        raw_guide = read_checked(value + '.md')
        # Mirrored repo structure preserves all original guide links and bytes.
        publish(value + '.md', raw_guide)
        guides.append(raw_guide.decode())
    for row in receipt['current_changed_sources']:
        publish(row['path'], read_checked(row['path']))
    for name in TESTS:
        value = 'build/tests/' + name
        publish(value, read_checked(value), projection=True)
    publish('evidence/classical/repairs/CONSOLIDATED_SOURCE_CHECKS_20260907.json', raw_receipt)

    baseline = json.loads((repo / 'evidence/classical/BASELINE.json').read_bytes())
    units = {u['id']: u for u in baseline['units']}
    changed_units = sorted({t['unit_id'] for d in ledgers for t in d['transactions']})
    english_rows = []
    for uid in changed_units:
        unit = units[uid]
        raw = (english / unit['source_path']).read_bytes()
        if digest(raw) != unit['english_sha256']:
            raise ValueError('Frozen English changed')
        value = 'english/' + unit['source_path']
        publish(value, raw)
        english_rows.append((uid, value))
    proof_links = []
    for row in ledgers[-1]['proof_support']:
        path = Path(row['path']).resolve()
        if not path.is_relative_to(english):
            raise ValueError('Unexpected proof witness root')
        raw = path.read_bytes()
        if (len(raw), digest(raw)) != (row['bytes'], row['sha256']):
            raise ValueError('Semantic definition witness drift')
        value = 'english/' + path.relative_to(english).as_posix()
        publish(value, raw)
        proof_links.append(f'[{path.stem}]({value})')

    rows, decisions, line_count = [], [], 0
    for ledger, guide, name in zip(ledgers, guides, NAMES):
        for decision in ledger['decisions']:
            did = decision['decision_id']
            start = guide.index('`' + did + '`')
            heading = re.findall(r'^## (.+)$', guide[:start], re.M)[-1]
            guide_value = 'evidence/classical/repairs/' + name + '.md'
            locations = []
            for tx in ledger['transactions']:
                for patch in tx['patches']:
                    if did not in patch['decision_ids']:
                        continue
                    raw = (ROOT / tx['path']).read_bytes()
                    needle = patch['after'].encode()
                    if raw.count(needle) != 1:
                        raise ValueError('Current location not unique: ' + did)
                    position = raw.index(needle)
                    if needle.startswith(b'%'):
                        position += needle.index(b'\n') + 1
                    line = raw[:position].count(b'\n') + 1
                    label = ('كلاسيكي' if tx['edition'] == 'classical' else 'MSA') + ' ' + tx['unit_id'] + ':' + str(line)
                    locations.append(f'[{label}]({tx["path"]}#L{line})')
                    line_count += 1
            title = TITLES[len(decisions)]
            rows.append(f'| {len(decisions)+1} | [{title}]({guide_value}#{slug(heading)}) | ' + '; '.join(locations) + ' |')
            decisions.append(did)
    if len(decisions) != 16 or len(set(decisions)) != 16 or line_count != 26:
        raise ValueError('Review directory not 16 decisions / 26 places exact')
    body = '''# Translation-choice supplement / ملحق اختيارات الترجمة

Sixteen documented decisions, with **26 exact source locations** in 15 corrected
Arabic files. These include revisions to earlier choices and new clarifications;
they are **not 16 additional unique terms** to add to the main register's count.
The 34 focused source tests passed. **No book was rebuilt for this supplement.**
It is a checked source-review update, not completion of the whole Classical
edition, the full audit, or final PDF/RTL/layout validation.

ستة عشر قرارًا موثقًا في الصياغة والمعنى، في ستة وعشرين موضعًا من خمسة عشر
ملفًا عربيًا. منها مراجعات لاختيارات سابقة، فلا نعدها ستة عشر مصطلحًا جديدًا.
اجتازت الدفعة أربعة وثلاثين اختبارًا للمصدر. لم يُعَد بناء الكتاب لهذه الدفعة،
ولا تعني اكتمال الطبعة الكلاسيكية أو مراجعة صفحاتها. جميع الاختيارات مفتوحة
للتصحيح، ولا يتوقف العمل على ورود جواب خبير.

## Review these places / مواضع المراجعة

Select a topic for the old wording, chosen wording, reason, and optional expert
question. Source links give exact current lines, **not final PDF page numbers**.
MSA denotes the shared text used by the international and Machrek editions.

اختر الموضوع لقراءة العبارة السابقة والمختارة وسبب الاختيار وسؤال المراجعة.
روابط المصدر تحيل إلى الأسطر الحالية، لا إلى صفحات PDF نهائي.

| # | Choice and reason / الاختيار وتعليله | Exact places / المواضع |
| --- | --- | --- |
''' + '\n'.join(rows) + '''

## Evidence and reading notes / الأدلة وحدودها

The three linked guides retain their exact verified bytes. Their JSON ledgers
are explicitly labelled privacy-normalized projections: local machine roots
are replaced by public-relative paths or `private-evidence` / `private-path`
provenance labels; personal directory names are removed. Original ledger hashes
and published hashes are distinguished in [PROJECTION_RECEIPT](PROJECTION_RECEIPT.json).
No translation, motive, question, quotation, source hash, or historical phase is
reassigned. Original private ledger bytes remain preserved in the evidence tree.
Private provenance labels are not public links and their external canon files
are not included. An old source hash refers to its recorded phase, not necessarily
the latest file: OLP0022 has two successive exact repairs.

النصوص التفسيرية الثلاثة محفوظة كما فُحصت. نسخ السجلات المنشورة تنقح مسارات
الجهاز والبيانات الشخصية فقط؛ وتفصل قائمة البصمات الأصل من النسخة المنشورة.
البصمة القديمة تخص مرحلتها ولا تُنسب إلى النص الحالي. بيانات الشواهد الخاصة
ليست روابط تنزيل عامة، ولا تُعد الشواهد المعجمية غير المفحوصة شهادات جديدة.

The [34-test source receipt](evidence/classical/repairs/CONSOLIDATED_SOURCE_CHECKS_20260907.json)
records the original verified inputs. Included test modules are audit evidence
for that complete source-tree context, **not a standalone runnable distribution**:
this supplement intentionally omits unrelated corpus files and private packets.
The main review index, source closure, generated readers, and final page bindings
still need their consolidated integration. Experts can review these exact passages
now without waiting for that work or for any other person.

### Frozen English witnesses / الشواهد الإنجليزية المجمدة

''' + '\n'.join(f'- [{uid}]({value})' for uid, value in english_rows) + '\n\n' + \
        'Semantic definitions for the finite-premise question / تعريفات المسألة: ' + ', '.join(proof_links) + '''.

### Package verification / فحص الحزمة

[Byte manifest](MANIFEST.json) · [Local link and line checks](LINK_CHECK_RECEIPT.json)
· [Projection identities](PROJECTION_RECEIPT.json).

This is a Markdown/source edition with direct online reading through this README
and the linked guides. No pertinent new PDF exists; no PDF is created merely to
fill a preview slot. A ZIP, if provided by the parent release, is an offline copy.
'''
    write('README.md', body.encode())
    dump('PROJECTION_RECEIPT.json', {"schema": 'arabic-sixteen-choice-public-projection-v1',
         "status": 'PASS', "decision_ids": decisions, "exact_current_source_places": line_count,
         "source_decisions": 16, "changed_arabic_sources": 15, "frozen_english_witnesses": len(english_rows) + len(proof_links),
         "note": 'Original source receipt hashes refer to original ledgers; publication projections have separately recorded hashes.',
         "artifacts": projections})
    checked = []
    for page in sorted(ROOT.rglob('*.md')):
        text = page.read_text(encoding='utf-8')
        for link in LINK.findall(text):
            value, _, fragment = unquote(link.strip('<>')).partition('#')
            if re.match(r'^(https?:|mailto:)', value):
                continue
            target = (page.parent / value).resolve() if value else page
            if target in {ROOT / 'MANIFEST.json', ROOT / 'LINK_CHECK_RECEIPT.json'} and not fragment:
                checked.append({"from": page.relative_to(ROOT).as_posix(), "target": target.name,
                                "fragment": '', "identity_binding": 'manifest-or-self; existence checked after finalization'})
                continue
            if not target.is_relative_to(ROOT) or not target.is_file():
                raise ValueError('Broken local link: ' + link)
            raw = target.read_bytes()
            if re.fullmatch(r'L\d+', fragment):
                line = int(fragment[1:])
                lines = raw.decode().splitlines()
                if not 1 <= line <= len(lines) or not lines[line-1].strip():
                    raise ValueError('Broken source-line link')
            elif fragment:
                headings = re.findall(r'^#{1,6} (.+)$', raw.decode(), re.M)
                if fragment not in {slug(x) for x in headings}:
                    raise ValueError('Broken heading link: ' + fragment)
            checked.append({"from": page.relative_to(ROOT).as_posix(), "target": target.relative_to(ROOT).as_posix(),
                            "fragment": fragment, "target_sha256": digest(raw)})
    # All text artifacts must pass the public-path/credential shape check.
    username = os.environ.get('USERNAME', '')
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix in {'.md', '.json', '.py', '.tex'}:
            text = path.read_text(encoding='utf-8')
            if re.search(r'(?i)\b[a-z]:[/\\]|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}', text):
                raise ValueError('Private path or credential shape in ' + path.name)
            if len(username) >= 3 and re.search(re.escape(username), text, re.I):
                raise ValueError('Personal name in ' + path.name)
    dump('LINK_CHECK_RECEIPT.json', {"schema": 'arabic-supplement-local-links-v1', "status": 'PASS',
         "markdown_files": 4, "local_links_checked": len(checked), "decision_places_checked": line_count,
         "privacy_check": 'PASS_NO_LOCAL_DRIVE_PATHS_PERSONAL_NAME_OR_CREDENTIAL_SHAPES', "links": checked})
    files = [identity(p.relative_to(ROOT).as_posix(), p.read_bytes()) for p in sorted(ROOT.rglob('*'))
             if p.is_file() and p.name != 'MANIFEST.json']
    dump('MANIFEST.json', {"schema": 'arabic-supplement-byte-manifest-v1', "status": 'PASS',
         "scope": 'Every supplement file except this self-referential manifest; no PDF or full-edition claim.',
         "files": files})
    for link in checked:
        if not (ROOT / link['target']).is_file():
            raise ValueError('Final local target absent')
    print(json.dumps({"status": 'PASS', "files": len(files)+1, "local_links": len(checked),
                      "manifest": identity('MANIFEST.json', (ROOT/'MANIFEST.json').read_bytes())}))


if __name__ == '__main__':
    main()

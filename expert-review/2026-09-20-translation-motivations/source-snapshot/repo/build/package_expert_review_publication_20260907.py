"""Package the checked reviewer snapshot without regenerating sources or books.

The public projection changes transport paths/privacy strings only. Exact cited
Arabic/English source bytes are preserved in a separate immutable snapshot.
No network, Git mutation, TeX, or original-artifact write occurs here.
"""
from pathlib import Path
import gzip
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[1]
ENGLISH = REPO.parent.parent / 'openlogic-interfarsi/repo/source/upstream'
EXPORT = REPO / 'tmp/expert-index-consolidated-20260907-reviewer-resume1'
STAGE = REPO.parent.parent / 'openlogic-arabic-review-publication-20260907'
PUBLIC = STAGE / 'expert-review/2026-09-07'
EXPECTED_INDEX = '98cc5e1870daa23b5889b98721d668f0b80a903e738f47b2d8df13f8409a93d4'
EXPECTED_CLOSURE = '76a3d9cf4635aa39cc18d6cdc722e8490062cf53fc985f062cdbc0cfda6c2978'
REPAIR = REPO / 'evidence/classical/repairs/OLP0021_0022_0024_CLASSICAL_CONSTRUCTIONS_20260907.json'
LINK = re.compile(r'\]\((<?[^)\n]+>?)\)')
REFERENCE = re.compile(r'^(\[[^\]\n]+\]:\s*)(\S+)', re.M)

def all_links(body):
    return [m.group(1).strip('<>') for m in LINK.finditer(body)] + [m.group(2).strip('<>') for m in REFERENCE.finditer(body)]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def hash_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

def private_projection(text):
    # Preserve private original files; publish only a clearly identified projection.
    for root, replacement in ((str(EXPORT), 'review-snapshot'), (str(ENGLISH), 'source-snapshot/english'),
                              (str(REPO), 'source-snapshot/repo')):
        for variant in (root, root.replace('\\','/'), root.replace('\\','\\\\')):
            text = text.replace(variant, replacement)
    text = re.sub(r'C:(?:/|\\\\|\\)Users(?:/|\\\\|\\)[^/\\\s"<>]+', '[local-user]', text, flags=re.I)
    username = os.environ.get('USERNAME', '')
    if len(username) >= 3:
        text = re.sub(re.escape(username), '[user]', text, flags=re.I)
    return text

def public_target(original):
    original = original.resolve()
    if original.is_relative_to(EXPORT):
        result = PUBLIC / original.relative_to(EXPORT)
        if result.name == 'EXPERT_REVIEW_INDEX.json':
            return result.with_suffix('.json.gz')
        return result
    if original.is_relative_to(REPO):
        return PUBLIC / 'source-snapshot/repo' / original.relative_to(REPO)
    if original.is_relative_to(ENGLISH):
        return PUBLIC / 'source-snapshot/english' / original.relative_to(ENGLISH)
    raise ValueError('Unadmitted local link root')

def rewrite_markdown(text, source, target):
    def rewritten_url(url):
        url = url.strip('<>')
        if re.match(r'^(https?:|mailto:|#)', url, re.I):
            return url
        pathname, separator, fragment = url.partition('#')
        origin = (source.parent / unquote(pathname)).resolve()
        destination = public_target(origin)
        relative = Path(os.path.relpath(destination, target.parent)).as_posix()
        return relative + (separator+fragment if separator else '')
    text = LINK.sub(lambda m: ']('+rewritten_url(m.group(1))+')', text)
    text = REFERENCE.sub(lambda m: m.group(1)+rewritten_url(m.group(2)), text)
    return private_projection(text)

def finalize_link_projection():
    """Finish the missed reference-style links; preserve generated/source bytes."""
    manifest_path = PUBLIC/'PUBLICATION_MANIFEST.json'
    assert hash_file(manifest_path) == '8b00405c46e485c99e7c3ca200e8364749720f1259cdfb0d1b05720dacf95f1c'
    old_manifest=json.loads(manifest_path.read_bytes())
    for row in old_manifest['files']:
        path=PUBLIC/row['path']
        assert hash_file(path)==row['sha256'] and path.stat().st_size==row['bytes']
    md_sources=list(EXPORT.glob('*.md'))+list((EXPORT/'reviewer-index').glob('*.md'))
    for source in md_sources:
        body=source.read_text(encoding='utf-8')
        target=public_target(source)
        for link in all_links(body):
            if re.match(r'^(https?:|mailto:|#)',link,re.I):continue
            origin=(source.parent/unquote(link.partition('#')[0])).resolve()
            destination=public_target(origin)
            if origin.is_relative_to(EXPORT) or destination.exists():continue
            assert origin.suffix.lower() in ('.json','.md','.tex','.txt','.sty') and origin.stat().st_size<4*1024*1024
            destination.parent.mkdir(parents=True,exist_ok=True)
            raw=origin.read_bytes()
            if origin.suffix.lower() not in ('.tex','.sty'):raw=private_projection(raw.decode('utf-8')).encode('utf-8')
            destination.write_bytes(raw)
        projected=rewrite_markdown(body,source,target)
        if source.name=='EXPERT_REVIEW_START_HERE.md':
            projected='Working snapshot — 7 September 2026. [All recorded choices](ALL_RECORDED_CHOICES.md).\n\n'+projected
        target.write_text(projected,encoding='utf-8',newline='\n')
    count=0
    for source in [*PUBLIC.glob('*.md'),*(PUBLIC/'reviewer-index').glob('*.md')]:
        body=source.read_text(encoding='utf-8')
        refs=dict(REFERENCE.findall(body))
        declared=set(re.findall(r'^\[([^\]]+)\]:',body,re.M))
        assert set(re.findall(r'\[[^\]\n]*\]\[([^\]]+)\]',body)) <= declared
        for link in all_links(body):
            if re.match(r'^(https?:|mailto:|#)',link,re.I):continue
            pathpart,_,frag=link.partition('#')
            destination=(source.parent/unquote(pathpart)).resolve()
            assert destination.is_relative_to(PUBLIC) and destination.is_file(), str(destination)
            if frag and destination.suffix=='.tex':
                assert re.fullmatch(r'L\d+(?:-L?\d+)?',frag), frag
                assert max(map(int,re.findall(r'\d+',frag)))<=len(destination.read_bytes().splitlines())
            if frag and destination.suffix=='.md' and frag.startswith(('priority-','decision-','complete-')):
                assert ('id="'+frag+'"') in destination.read_text(encoding='utf-8'),frag
            count+=1
    with gzip.open(PUBLIC/'EXPERT_REVIEW_INDEX.json.gz','rt',encoding='utf-8') as f:
        for line in f:
            assert os.environ.get('USERNAME','!absent!').lower() not in line.lower()
    old_receipt=json.loads((STAGE/'PACKAGE_RECEIPT.json').read_bytes())
    dump(STAGE/'PACKAGE_INLINE_LINKS_CHECKPOINT.json',old_receipt)
    old_manifest['local_links_verified']=count
    old_manifest['link_validation']='Inline and reference-style local links; reference uses declared; explicit decision anchors and source line ranges checked.'
    old_manifest['files']=[{'path':p.relative_to(PUBLIC).as_posix(),'bytes':p.stat().st_size,'sha256':hash_file(p)} for p in sorted(PUBLIC.rglob('*')) if p.is_file() and p!=manifest_path]
    dump(manifest_path,old_manifest)
    archive=STAGE/'OPENLOGIC_ARABIC_EXPERT_REVIEW_20260907.zip'
    assert hash_file(archive)==old_receipt['archive_sha256']
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for source in sorted(PUBLIC.rglob('*')):
            if source.is_file():
                info=zipfile.ZipInfo(source.relative_to(PUBLIC).as_posix(),date_time=(2026,9,7,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,source.read_bytes())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    receipt={**old_receipt,'file_count':len(old_manifest['files'])+1,'local_links_verified':count,'archive_bytes':archive.stat().st_size,'archive_sha256':hash_file(archive),'manifest_sha256':hash_file(manifest_path),'status':'PASS_ALL_LOCAL_LINKS_AND_PACKAGE'}
    dump(STAGE/'PACKAGE_RECEIPT.json',receipt)
    print(json.dumps(receipt))

def main():
    if PUBLIC.exists() and sys.argv[1:] != ['--resume-checked-sources']:
        raise RuntimeError('Publication directory already exists; inspect and resume, never overwrite')
    assert hash_file(EXPORT/'EXPERT_REVIEW_INDEX.json') == EXPECTED_INDEX
    closure_path = REPO/'evidence/classical/SOURCE_RECONCILIATION_CLOSURE_MANIFEST_20260905.json'
    assert hash_file(closure_path) == EXPECTED_CLOSURE
    closure = json.loads(closure_path.read_bytes())
    validation = json.loads((EXPORT/'READBACK_VALIDATION.json').read_bytes())
    assert validation['status'] == 'PASS' and not validation['errors']
    assert validation['snapshot_json_sha256'] == EXPECTED_INDEX
    repairs = json.loads(REPAIR.read_bytes())
    tx = {row['path']: row for row in repairs['transactions']}
    PUBLIC.mkdir(parents=True, exist_ok=True)
    inventory, recovered = [], []
    for unit in closure['units']:
        sources = [('english', ENGLISH/unit['source_path'], unit['english_sha256'], None)]
        sources += [(kind, REPO/unit[kind]['path'], unit[kind]['sha256'], unit[kind]['bytes']) for kind in ('msa','classical')]
        for kind, source, expected, expected_size in sources:
            raw = source.read_bytes()
            if sha(raw) != expected.lower():
                rel = source.relative_to(REPO).as_posix()
                repair = tx[rel]
                assert sha(raw) == repair['after_sha256']
                original = raw.decode('utf-8')
                for patch in reversed(repair['patches']):
                    assert original.count(patch['after']) == 1
                    original = original.replace(patch['after'], patch['before'], 1)
                raw = original.encode('utf-8')
                assert sha(raw) == repair['before_sha256'] == expected.lower()
                recovered.append(rel)
            assert sha(raw) == expected.lower()
            if expected_size is not None:
                assert len(raw) == expected_size
            destination = public_target(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                assert destination.read_bytes() == raw, 'Existing source snapshot differs'
            else:
                destination.write_bytes(raw)
            inventory.append({'unit':unit['id'], 'edition':kind, 'path':destination.relative_to(PUBLIC).as_posix(), 'bytes':len(raw), 'sha256':sha(raw)})
    assert len(inventory) == 2166 and len(recovered) == 3
    md_sources = list(EXPORT.glob('*.md')) + list((EXPORT/'reviewer-index').glob('*.md'))
    for source in md_sources:
        target = public_target(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        body = source.read_text(encoding='utf-8')
        for match in LINK.finditer(body):
            link = match.group(1).strip('<>')
            if re.match(r'^(https?:|mailto:|#)', link, re.I):
                continue
            pathpart = link.partition('#')[0]
            origin = (source.parent/unquote(pathpart)).resolve()
            destination = public_target(origin)
            if origin.is_relative_to(EXPORT) or destination.exists():
                continue
            assert origin.suffix.lower() in ('.json','.md','.tex','.txt','.sty')
            assert origin.stat().st_size < 2*1024*1024
            destination.parent.mkdir(parents=True, exist_ok=True)
            if origin.suffix.lower() in ('.tex','.sty'):
                destination.write_bytes(origin.read_bytes())
            else:
                destination.write_text(private_projection(origin.read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
        target.write_text(rewrite_markdown(body,source,target), encoding='utf-8', newline='\n')
    # Stream the 100 MB index; no full in-memory JSON parse or regenerated decisions.
    with (EXPORT/'EXPERT_REVIEW_INDEX.json').open(encoding='utf-8') as src:
        with (PUBLIC/'EXPERT_REVIEW_INDEX.json.gz').open('wb') as dst:
            with gzip.GzipFile(filename='',fileobj=dst,mode='wb',mtime=0) as compressed:
                for line in src:
                    compressed.write(private_projection(line).encode('utf-8'))
    csv = EXPORT/'EXPERT_REVIEW_OCCURRENCES.csv'
    with csv.open(encoding='utf-8-sig', newline='') as src, (PUBLIC/csv.name).open('w',encoding='utf-8-sig',newline='') as dst:
        for line in src:
            dst.write(private_projection(line))
    dump(PUBLIC/'SOURCE_SNAPSHOT.json', {'source_closure_sha256':EXPECTED_CLOSURE,'sources':inventory,'historical_bytes_recovered_by_exact_inverse':recovered,'live_sources_modified':False})
    dump(PUBLIC/'READBACK_VALIDATION.json',json.loads(private_projection(json.dumps(validation,ensure_ascii=False))))
    # Preserve newer work separately, never silently substitute it into the checked index.
    work = PUBLIC/'additional-work'
    work.mkdir()
    for source in [REPAIR, REPO/'tmp/redo-20260906-propagation/units-0391-0410-continuation.json', REPO/'tmp/redo-20260906-propagation/units-0391-0410-continuation.md']:
        (work/source.name).write_text(private_projection(source.read_text(encoding='utf-8')),encoding='utf-8',newline='\n')
    for rel, row in tx.items():
        source=REPO/rel
        assert hash_file(source)==row['after_sha256']
        destination=work/'function-constructions'/Path(rel).name
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(source.read_bytes())
    (work/'README.md').write_text('''# Additional current work — not merged into the checked index

The functions ledger preserves six new Classical construction decisions and
seven reversible replacements across three files. These newer files are kept
here separately from the exact source snapshot used by the review index.
Focused verification and central integration are unfinished.

The 0391–0410 intake adds 49 terminology records and six correction proposals.
Its recorded checks are attributed to its author; independent readback was
interrupted before a final receipt. Proposals are not silently treated as fixes.
These files preserve current work but do not certify full-book completion.
Operational machine paths in public evidence are privacy-normalized projections.
''',encoding='utf-8',newline='\n')
    (PUBLIC/'ALL_RECORDED_CHOICES.md').write_text('''# All recorded Arabic translation choices / جميع اختيارات الترجمة المسجلة

Working snapshot, 7 September 2026 — **1,050 human-readable entries**, not a claim
that every translation decision in the 722-unit work has been fully reviewed.

- [Start with 30 priority choices](EXPERT_REVIEW_START_HERE.md).
- [Browse every recorded entry, in readable parts](reviewer-index/README.md#complete-shards--الأجزاء-الكاملة).
- [Browse all priority and complete parts](reviewer-index/README.md).
- [Download the sortable occurrence table](EXPERT_REVIEW_OCCURRENCES.csv).
- [Download the machine-readable register (gzip)](EXPERT_REVIEW_INDEX.json.gz).
- [Newer source work and audit intake, kept separately](additional-work/README.md).

Entries show the English term, Arabic wording, reasons, alternatives, and exact
source locations when proved. Unresolved locations remain visibly unresolved.
There are 879 flagged choices, 495 unresolved lexical locations, 110 flags still
needing explicit questions, and no certified final PDF page numbers. Earlier
reasons reconstructed retrospectively are labelled as such. Expert corrections
are welcome; no expert response is required before work continues.

The accompanying source snapshot preserves the exact bytes reviewed, including
three predecessor files reconstructed by verified inverse patches. It does not
overwrite the actively improving translation. This is a review publication,
not a newly built or certified Classical book.
''',encoding='utf-8',newline='\n')
    start=PUBLIC/'EXPERT_REVIEW_START_HERE.md'
    start.write_text('Working snapshot — 7 September 2026. [All recorded choices](ALL_RECORDED_CHOICES.md).\n\n'+start.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    # Do not rely on a guessed heading fragment: use the real complete-shard heading.
    all_page=PUBLIC/'ALL_RECORDED_CHOICES.md'
    all_page.write_text(all_page.read_text(encoding='utf-8').replace('reviewer-index/README.md#complete-shards--الأجزاء-الكاملة','reviewer-index/README.md'),encoding='utf-8',newline='\n')
    checked_links=0
    for source in [*PUBLIC.glob('*.md'),*(PUBLIC/'reviewer-index').glob('*.md')]:
        for match in LINK.finditer(source.read_text(encoding='utf-8')):
            link=match.group(1).strip('<>')
            if re.match(r'^(https?:|mailto:|#)',link,re.I):continue
            pathpart,_,frag=link.partition('#')
            destination=(source.parent/unquote(pathpart)).resolve()
            assert destination.is_relative_to(PUBLIC) and destination.is_file(), str(destination)
            if destination.suffix=='.tex' and frag:
                assert re.fullmatch(r'L\d+(?:-L?\d+)?',frag),frag
                assert max(map(int,re.findall(r'\d+',frag))) <= len(destination.read_bytes().splitlines())
            checked_links+=1
    # Check sources stay byte-exact and every published text excludes the local user's name.
    username=os.environ.get('USERNAME','').lower()
    for source in PUBLIC.rglob('*'):
        if source.is_file() and source.suffix in ('.md','.json','.tex','.csv','.txt'):
            assert not username or username not in source.read_text(encoding='utf-8-sig').lower(), 'Privacy scan failed'
    manifest=[]
    for source in sorted(PUBLIC.rglob('*')):
        if source.is_file():manifest.append({'path':source.relative_to(PUBLIC).as_posix(),'bytes':source.stat().st_size,'sha256':hash_file(source)})
    dump(PUBLIC/'PUBLICATION_MANIFEST.json',{'schema':'arabic-expert-review-public-projection-v1','status':'PASS_WORKING_SNAPSHOT','review_index_original_sha256':EXPECTED_INDEX,'counts':validation['counts'],'local_links_verified':checked_links,'privacy_normalization':'Public review metadata only; cited source bytes unchanged. Original private artifacts preserved.','files':manifest})
    archive=STAGE/'OPENLOGIC_ARABIC_EXPERT_REVIEW_20260907.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for source in sorted(PUBLIC.rglob('*')):
            if source.is_file():
                info=zipfile.ZipInfo(source.relative_to(PUBLIC).as_posix(),date_time=(2026,9,7,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,source.read_bytes())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    receipt={'status':'PASS_PACKAGED','file_count':len(manifest)+1,'local_links_verified':checked_links,'source_files':len(inventory),'recovered_predecessors':len(recovered),'archive':archive.name,'archive_bytes':archive.stat().st_size,'archive_sha256':hash_file(archive),'manifest_sha256':hash_file(PUBLIC/'PUBLICATION_MANIFEST.json')}
    dump(STAGE/'PACKAGE_RECEIPT.json',receipt)
    print(json.dumps(receipt))

if __name__=='__main__':
    if sys.argv[1:]==['--finalize-link-projection']:
        finalize_link_projection()
    else:
        main()

"""Resume a completed data export in two bounded, independently receipted stages.

This does not regenerate or reassess decisions. The predecessor's FAIL remains
intact. Only the two reviewed renderer/readback code successors are admitted;
all amendment and other frozen-input bytes must still match. No network or TeX.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os

try:
    from build import generate_expert_review_index as producer
    from build import validate_expert_review_snapshot as validator
    from build import reviewer_input_inventory_20260909 as inventory
    from build.run_expert_review_readback_20260906 import Job, CAP
except ModuleNotFoundError:
    import generate_expert_review_index as producer
    import validate_expert_review_snapshot as validator
    import reviewer_input_inventory_20260909 as inventory
    from run_expert_review_readback_20260906 import Job, CAP

REPO = Path(__file__).resolve().parents[1]
ENGLISH = REPO.parents[1] / 'openlogic-interfarsi/repo/source/upstream'
PREDECESSOR = REPO / 'tmp/expert-index-relation-motivations-20260919-v2'
PREVIOUS_ACCEPTED = REPO / 'tmp/expert-index-integrated-20260913-corrected'
OUTPUT = REPO / 'tmp/expert-index-relation-motivations-20260920-rendered'
INDEX_SHA = '27a4ac1386ab31a3dfaf9f4b43c750d3dda221a8957fcc57b905357b23a1326b'
OLD_ERROR = 'retro-0005-0050:named-defn:f7c277e69d8cf7d5: missing/truncated full CSV expert question'
CODE_SUCCESSORS = {'build/generate_expert_review_index.py', 'build/validate_expert_review_snapshot.py'}


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    temporary.replace(path)


def admit_inventory(old, new):
    require(old['schema'] == new['schema'], 'Inventory schema changed')
    require(old['semantic_amendments'] == new['semantic_amendments'], 'Semantic amendments changed')
    before = {r['path']: r for r in old['supporting_inputs']}
    after = {r['path']: r for r in new['supporting_inputs']}
    require(len(before) == len(old['supporting_inputs']) and len(after) == len(new['supporting_inputs']),
            'Duplicate supporting identity')
    require(before.keys() == after.keys(), 'Supporting input inventory changed')
    changed = {p for p in before if before[p] != after[p]}
    require(changed == CODE_SUCCESSORS, 'Unadmitted supporting-code change')
    return [{'path': p, 'before': before[p], 'after': after[p]} for p in sorted(changed)]


def record_digest(rows):
    result = hashlib.sha256()
    encoder = json.JSONEncoder(ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    for row in rows:
        for chunk in encoder.iterencode(row):
            result.update(chunk.encode('utf-8'))
        result.update(b'\n')
    return result.hexdigest()


def verify_source_locations(payload):
    """Recheck every displayed exact location against its original full-file hash."""
    cache = {}
    checked = 0
    for row in payload['decisions']:
        if not row['index_metadata']['human_index_included']:
            continue
        groups = [producer.human_location_rows(o) for o in producer.human_occurrence_rows(row)]
        groups.append(producer.human_global_source_rows(row))
        for group in groups:
            for loc in group:
                rec = loc['line_reconciliation']
                if not rec['resolved']:
                    continue
                root = ENGLISH if loc['source_kind'] == 'english' else REPO
                path = (root / loc['logical_path']).resolve()
                allowed = ENGLISH if root == ENGLISH else REPO / 'source'
                require(path.is_relative_to(allowed.resolve()) and path.is_file(), 'Location escapes its source root')
                if path not in cache:
                    raw = path.read_bytes()
                    cache[path] = (hashlib.sha256(raw).hexdigest(), raw.decode('utf-8-sig').splitlines())
                current_hash, lines = cache[path]
                require(current_hash == str(loc.get('current_sha256', '')).lower(),
                        'Exact-location source changed: ' + loc['logical_path'])
                start, end = rec['current_line_start'], rec['current_line_end']
                require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                        'Invalid exact source range')
                require(producer.strip_tex_comments('\n'.join(lines[start-1:end])).strip(),
                        'Exact location contains only comments or whitespace')
                checked += 1
    return checked, [{'path': str(p), 'sha256': h} for p, (h, _) in sorted(cache.items())]


def render(receipt):
    require(not OUTPUT.exists(), 'Render checkpoint exists; inspect or use the check stage')
    old_validation = json.loads((PREDECESSOR / 'READBACK_VALIDATION.json').read_bytes())
    require(old_validation['status'] == 'FAIL' and old_validation['errors'] == [OLD_ERROR],
            'Predecessor failure is not the specifically corrected human-display failure')
    index = PREDECESSOR / 'EXPERT_REVIEW_INDEX.json'
    require(index.stat().st_size <= 128 * 1024 * 1024 and digest(index) == INDEX_SHA,
            'Completed predecessor data identity changed')
    frozen = inventory.capture(REPO)
    with index.open(encoding='utf-8') as stream:
        payload = json.load(stream)
    successors = admit_inventory(payload['frozen_amendment_inventory'], frozen)
    before = record_digest(payload['decisions'])
    checked, sources = verify_source_locations(payload)
    payload['frozen_amendment_inventory'] = frozen
    payload['reviewer_sharding']['directory'] = (OUTPUT / 'reviewer-index').relative_to(REPO).as_posix()
    groups = producer.reviewer_shard_groups(payload)
    for kind in ('priority', 'complete'):
        payload['reviewer_sharding'][kind + '_file_count'] = len(groups[kind])
        payload['summary'][kind + '_reviewer_shards'] = len(groups[kind])
    payload['render_recovery'] = {'predecessor_index_sha256': INDEX_SHA,
        'predecessor_readback_sha256': digest(PREDECESSOR / 'READBACK_VALIDATION.json'),
        'preserved_decision_records_sha256': before, 'code_successors': successors,
        'scope': 'Human presentation repair only; every predecessor decision record retained unchanged.'}
    prefix = producer.markdown_relative_prefix(OUTPUT, REPO)
    md = producer.render_markdown(payload, arabic_prefix=prefix, reviewer_index_href='reviewer-index')
    start = producer.render_start_here_markdown(payload, 30, arabic_prefix=prefix,
        reviewer_index_href='reviewer-index', priority_href_by_id=producer.priority_shard_href_map(
            payload, reviewer_index_href='reviewer-index', groups=groups['priority']))
    priority = producer.render_priority_markdown(payload, arabic_prefix=prefix, reviewer_index_href='reviewer-index')
    csv_text = producer.render_occurrence_csv(payload)
    shards = producer.render_review_shards(payload,
        arabic_prefix=producer.markdown_relative_prefix(OUTPUT / 'reviewer-index', REPO),
        start_here_href='../EXPERT_REVIEW_START_HERE.md', groups=groups)
    surfaces = {OUTPUT / 'EXPERT_REVIEW_INDEX.md': md,
        OUTPUT / 'EXPERT_REVIEW_START_HERE.md': start,
        OUTPUT / 'EXPERT_REVIEW_PRIORITY_ONLY.md': priority,
        **{OUTPUT / 'reviewer-index' / name: text for name, text in shards.items()}}
    producer.verify_human_surfaces({**{str(p): s for p, s in surfaces.items()}, 'CSV': csv_text})
    producer.verify_generated_markdown_links(surfaces)
    require(producer.verify_occurrence_csv(payload, csv_text) == payload['summary']['human_csv_rows'], 'CSV count differs')
    producer.verify_reviewer_shards(payload, shards, groups)
    require(record_digest(payload['decisions']) == before, 'A decision record changed during rendering')
    inventory.verify(REPO, frozen)
    for source in sources:
        require(digest(Path(source['path'])) == source['sha256'], 'Source changed during rendering')
    producer.write_outputs(payload, md, start, priority, csv_text,
        OUTPUT / 'EXPERT_REVIEW_INDEX.json', OUTPUT / 'EXPERT_REVIEW_INDEX.md',
        OUTPUT / 'EXPERT_REVIEW_START_HERE.md', OUTPUT / 'EXPERT_REVIEW_PRIORITY_ONLY.md',
        OUTPUT / 'EXPERT_REVIEW_OCCURRENCES.csv', shards, OUTPUT / 'reviewer-index')
    save(OUTPUT / 'AMENDMENT_INPUT_INVENTORY.json', frozen)
    receipt.update(status='PASS_RENDERED_PENDING_INDEPENDENT_READBACK',
        snapshot_json_sha256=digest(OUTPUT / 'EXPERT_REVIEW_INDEX.json'),
        unchanged_decision_records=len(payload['decisions']), decision_records_sha256=before,
        exact_locations_rechecked=checked, source_files=sources, code_successors=successors)


def check(receipt):
    rendered = json.loads((OUTPUT / 'RENDER_RECEIPT.json').read_bytes())
    require(rendered['status'] == 'PASS_RENDERED_PENDING_INDEPENDENT_READBACK', 'Rendering did not pass')
    require(digest(OUTPUT / 'EXPERT_REVIEW_INDEX.json') == rendered['snapshot_json_sha256'], 'Rendered data changed')
    require(rendered['runner_sha256'] == digest(Path(__file__)), 'Recovery runner changed')
    frozen = json.loads((OUTPUT / 'AMENDMENT_INPUT_INVENTORY.json').read_bytes())
    inventory.verify(REPO, frozen)
    for source in rendered['source_files']:
        require(digest(Path(source['path'])) == source['sha256'], 'A rendered exact-location source changed')
    validation = validator.check(REPO, OUTPUT, PREVIOUS_ACCEPTED, ENGLISH, frozen_inventory=frozen)
    inventory.verify(REPO, frozen)
    save(OUTPUT / 'READBACK_VALIDATION.json', validation)
    receipt.update(status=validation['status'], readback_counts=validation['counts'],
        errors=validation['errors'], snapshot_json_sha256=validation['snapshot_json_sha256'],
        render_receipt_sha256=digest(OUTPUT / 'RENDER_RECEIPT.json'))
    require(validation['status'] == 'PASS', 'Independent readback failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=('render', 'check'))
    args = parser.parse_args()
    guard = Job()
    guard.assign()
    receipt = {'scope': 'Retained-data human-surface recovery: ' + args.stage,
        'status': 'STARTED', 'pid': os.getpid(), 'memory_cap_bytes': CAP, 'public_release': False,
        'runner_sha256': digest(Path(__file__)), 'predecessor_index_sha256': INDEX_SHA}
    try:
        (render if args.stage == 'render' else check)(receipt)
    except Exception as error:
        receipt.update(status='FAIL', failure=str(error))
        raise
    finally:
        receipt['peak_committed_bytes'] = guard.peak()
        if OUTPUT.exists():
            save(OUTPUT / ('RENDER_RECEIPT.json' if args.stage == 'render' else 'RUN_RECEIPT.json'), receipt)
        print(json.dumps({k: v for k, v in receipt.items() if k not in {'source_files', 'code_successors'}}, ensure_ascii=False))
        guard.close()


if __name__ == '__main__':
    main()

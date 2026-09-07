"""Exact cardinality source-reference integration; read-only except patch emission.

Only two registry witnesses are stale; no amendment JSON is changed. Every
source predecessor is recovered by a pinned inverse and forward replay.
"""
from __future__ import annotations
import argparse
import copy
import difflib
import json
from collections import Counter
from pathlib import Path
from build import audit_expert_source_binding_next_source_batch_20260907 as prior

ROOT, ENGLISH, PROV = prior.ROOT, prior.ENGLISH, prior.PROV
BINDINGS = prior.BINDINGS
HISTORY_DIR = PROV + 'expert-review-binding-history/cardinality-source-batch-20260907/'
PREVIOUS = HISTORY_DIR + 'pre-refresh/EXPERT_REVIEW_SOURCE_BINDINGS.json'
RECEIPT = HISTORY_DIR + 'REFRESH_RECEIPT.json'
AUTHORITY_KEY = 'cardinality_source_batch_refresh_20260907'
PRIOR_IDENTITY = ('9afd2636aaec780a26613ad1262b6410ac01ec1d72f6bad5519ee6748573bd34', 160635)
EXPECTED = {'/bindings/20/occurrences/1/locations/1', '/bindings/22/occurrences/0/locations/1'}
LEDGERS = {
    'evidence/classical/repairs/OLP0031_0032_PAIRING_CONSTRUCTIONS_20260907.json':
        ('86da173ac4083f2effe84cf60efe0e726e6caf79023aa8fa3ae6d852d73c8bc9', 'openlogic-pairing-construction-repairs-v1', 4, 8, 7),
    'evidence/classical/repairs/OLP0033_NONENUMERABILITY_CONSTRUCTIONS_20260907.json':
        ('13aa46d70ae164ca7b2be107503238027c2fadc3d0204a3bc0c68d9feb26aecc', 'arabic-bounded-source-repairs.v1', 2, 6, 6),
    'evidence/classical/repairs/OLP0034_REDUCTION_CONSTRUCTIONS_20260907.json':
        ('8addb4be1b7b8cc92f7044ab4ef357de6ea8105e134ac4ad921d9e5348580631', 'openlogic-reduction-construction-repairs-v1', 2, 4, 4),
    'evidence/classical/repairs/OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.json':
        ('4615dbc5636212dc0c9ca3c2244afef44f13a49d8a330ffd5dd6ce51415f68ed', 'openlogic-equinumerosity-construction-repairs-v1', 2, 7, 6),
}
PRIOR_RECEIPTS = {**prior.PRIOR_RECEIPTS,
    prior.RECEIPT: '66ed75128bd0a7017c8b942dd0a9135e24f4bc68fd988f41375b8e15e6ddb09f'}
require, sha, read, dump, identity = prior.require, prior.sha, prior.read, prior.dump, prior.identity
declarations, excerpt, ranges_of = prior.declarations, prior.excerpt, prior.ranges_of


def source_chains():
    chains, inputs = {}, []
    ids = set()
    for logical, contract in LEDGERS.items():
        raw = read(logical)
        require(sha(raw) == contract[0], 'Pinned repair ledger mismatch: ' + logical)
        data = json.loads(raw)
        require((data['schema'], len(data['transactions']), sum(len(t['patches']) for t in data['transactions']),
                 len(data['decisions'])) == contract[1:], 'Pinned repair inventory mismatch')
        inputs.append(identity(logical, raw))
        for d in data['decisions']:
            require(d['decision_id'] not in ids and d['open_to_correction'], 'Duplicate or closed decision')
            ids.add(d['decision_id'])
        for original in data['transactions']:
            t = copy.deepcopy(original)
            require(t['path'] not in chains, 'Unplanned multi-stage source chain')
            for p in t['patches']:
                # The reduction ledger has no occurrences/decision_ids fields;
                # derive exactly one owner by its explicit path/literal record.
                owners = p.get('decision_ids')
                if owners is None:
                    owners = [d['decision_id'] for d in data['decisions']
                              if d['occurrences'][0]['target_path'] == t['path'] and d['before_arabic'] == p['before']]
                    require(len(owners) == 1, 'No exact literal decision owner')
                require(set(owners) <= ids and owners, 'Unknown patch owner')
                p['decision_ids'] = owners
                require(p.get('occurrences', 1) == 1, 'Patch is not a single occurrence')
                p['occurrences'] = 1
            after = read(t['path'])
            before = prior.inverse(after, t)
            chains[t['path']] = [{'ledger': logical, 'transaction': t, 'before': before, 'after': after}]
    require((len(chains), len(ids), sum(len(c[0]['transaction']['patches']) for c in chains.values())) == (10, 23, 25),
            'Cardinality source inventory differs')
    return chains, inputs


def source_snapshot(t):
    return HISTORY_DIR + 'sources/' + t['unit_id'] + '-' + t['edition'] + '.tex'


def expected_documents():
    chains, inputs = source_chains()
    raw = read(PREVIOUS) if (ROOT / PREVIOUS).exists() else read(BINDINGS)
    require((sha(raw), len(raw)) == PRIOR_IDENTITY, 'Pinned predecessor registry differs')
    old = json.loads(raw)
    require(dump(old) == raw, 'Predecessor is not canonical LF JSON')
    new = copy.deepcopy(old)
    artifacts, changes = {PREVIOUS: raw}, []
    for chain in chains.values():
        step = chain[0]
        artifacts[source_snapshot(step['transaction'])] = step['before']
    for pointer, decision, unit, w in declarations(new, True):
        root = ENGLISH if w['source_kind'] == 'english' else ROOT
        path = (root / w['path']).resolve()
        require(path.is_relative_to(root.resolve()), 'Witness path escapes root')
        live = path.read_bytes()
        if sha(live) == w['file_sha256'].lower():
            continue
        require(pointer in EXPECTED and w['source_kind'] == 'msa', 'Unexpected stale witness: ' + pointer)
        chain = chains[w['path']]
        before = chain[0]['before']
        require(sha(before) == w['file_sha256'].lower(), 'Witness is not exact predecessor')
        quote = excerpt(before, w['line_ranges'])
        require(sha(quote.encode()) == w['cited_text_sha256'].lower(), 'Historical quotation differs')
        current, ranges, affected = prior.mapped_passage(before, chain, w['line_ranges'])
        require(current == live and not affected and excerpt(live, ranges) == quote,
                'Expected unchanged quotation needs explicit new review')
        old_witness = copy.deepcopy(w)
        w['file_sha256'] = sha(live)
        w['line_ranges'] = ranges
        changes.append({'pointer': pointer, 'decision_id': decision, 'unit_id': unit,
            'before': old_witness, 'after': copy.deepcopy(w), 'quoted_text': quote,
            'quotation_unchanged': True, 'canonical_wording_decisions': [],
            'changed_fields': [key for key in w if w[key] != old_witness[key]],
            'new_assessment': "New current-source binding assessment, not the original translator's motive: the selected quotation and its semantic_basis are unchanged. Only the exact file identity and any proven line relocation are refreshed.",
            'source_repair_ledger': chain[0]['ledger'],
            'historical_source': identity(source_snapshot(chain[0]['transaction']), before)})
    require({c['pointer'] for c in changes} == EXPECTED, 'Exact stale-pointer inventory differs')
    require(AUTHORITY_KEY not in new['authority'], 'Refresh already present in predecessor')
    new['authority'][AUTHORITY_KEY] = {
        'assessed_on': '2026-09-07', 'recording_mode': 'new-independent-current-source-witness-refresh',
        'previous_file': identity(PREVIOUS, raw), 'receipt': RECEIPT,
        'scope': 'Two MSA file identities and one exact line relocation; quotations, semantic bases, original reasons and authority remain unchanged. No amendment JSON changes.',
        'changed_pointers': sorted(EXPECTED), 'human_response_is_gate': False}
    artifacts[BINDINGS] = dump(new)
    return artifacts, new, changes, chains, inputs


def verify_current():
    from build import generate_expert_review_index as index
    artifacts, registry, changes, chains, inputs = expected_documents()
    for path, expected in artifacts.items():
        require(read(path) == expected, 'Current or preserved artifact differs: ' + path)
    baseline_raw = read('evidence/classical/BASELINE.json')
    require(sha(baseline_raw) == prior.BASELINE_SHA, 'Frozen baseline differs')
    baseline = {x['id']: x for x in json.loads(baseline_raw)['units']}
    inventory, totals, rows = {}, Counter(), []
    for pointer, decision, unit, w in declarations(registry, True):
        kind = w['source_kind']
        expected_path = None if unit is None else baseline[unit][{'english': 'source_path', 'msa': 'arabic_path', 'classical': 'target_path'}[kind]]
        index._validated_expert_source_group(w, ROOT, ENGLISH, expected_path, sha(artifacts[BINDINGS]).upper())
        path = (ENGLISH if kind == 'english' else ROOT) / w['path']
        raw = path.read_bytes()
        require(sha(raw) == w['file_sha256'].lower() and sha(excerpt(raw, w['line_ranges']).encode()) == w['cited_text_sha256'].lower(),
                'Current registry witness differs')
        inventory[str(path)] = sha(raw)
        totals[kind] += 1
        totals['unit' if unit else 'global'] += 1
        rows.append({'file': BINDINGS, 'pointer': pointer, 'decision_id': decision, 'witness': w, 'status': 'PASS'})
    require(len(registry['bindings']) == 70 and len(rows) == 190 and dict(totals) ==
            {'english': 71, 'unit': 179, 'msa': 82, 'classical': 37, 'global': 11}, 'Registry inventory changed')
    amendment_ids, amendments = set(), []
    for path in sorted((ROOT / (PROV + 'expert-review-amendments')).glob('*.json')):
        raw = read(path.relative_to(ROOT).as_posix())
        amendments.append(identity(path.relative_to(ROOT).as_posix(), raw))
        payload = json.loads(raw)
        for row in payload['amendments']:
            require(row['decision_id'] not in amendment_ids, 'Duplicate amendment decision')
            amendment_ids.add(row['decision_id'])
        for pointer, decision, _, w in declarations(payload, False):
            root = ENGLISH if w['source_kind'] == 'english' else ROOT
            target = (root / w['path']).resolve()
            require(target.is_relative_to(root.resolve()), 'Amendment path escapes root')
            data = target.read_bytes()
            quoted = excerpt(data, ranges_of(w))
            require(sha(data) == w['file_sha256'].lower() and sha(quoted.encode()) == w['excerpt_sha256'].lower(),
                    'Current amendment witness differs')
            require('excerpt' not in w or w['excerpt'] == quoted, 'Current amendment literal differs')
            inventory[str(target)] = sha(data)
            rows.append({'file': path.relative_to(ROOT).as_posix(), 'pointer': pointer, 'decision_id': decision, 'witness': w, 'status': 'PASS'})
    require((len(amendment_ids), len(rows) - 190) == (68, 257), 'Amendment inventory changed')
    for path, digest in inventory.items():
        require(sha(Path(path).read_bytes()) == digest, 'Source changed during audit')
    previous_receipts = []
    for path, digest in PRIOR_RECEIPTS.items():
        raw = read(path)
        require(sha(raw) == digest, 'Historical receipt differs')
        previous_receipts.append(identity(path, raw))
    return {'schema': 'openlogic-review-bindings-cardinality-source-batch-v1', 'assessed_on': '2026-09-07', 'status': 'PASS',
        'scope': 'all-190-live-registry-and-257-live-amendment-witnesses-no-historical-source-substitution',
        'counts': {'bindings': 70, 'registry_declarations': 190, 'amendments': 68, 'amendment_witnesses': 257,
            'changed_registry_declarations': 2, 'changed_amendment_witnesses': 0, 'unchanged_quotations': 2,
            'wording_reassessments': 0, 'source_files': 10, 'source_patches': 25, 'source_decisions': 23, **dict(totals)},
        'previous_file': identity(PREVIOUS, artifacts[PREVIOUS]), 'current_file': identity(BINDINGS, artifacts[BINDINGS]),
        'repair_ledgers': inputs, 'pointer_changes': changes,
        'source_inverse_proofs': [{'path': p, 'ledger': c[0]['ledger'], 'before': identity(source_snapshot(c[0]['transaction']), c[0]['before']),
             'after': identity(p, c[0]['after']), 'patches': c[0]['transaction']['patches']} for p, c in chains.items()],
        'complete_live_locator_audit': rows, 'unchanged_amendment_files': amendments, 'preserved_prior_receipts': previous_receipts,
        'limits': ['No full reviewer export, translation edit, reader build, final page mapping or publication.',
                   'Unchanged selected quotations need no new terminology rationale; original raw decisions remain authoritative.']}


def emit(path):
    expected = dump(verify_current()) if path == RECEIPT else expected_documents()[0].get(path)
    require(expected is not None, 'Unapproved output')
    target = ROOT / path
    if target.exists():
        current = target.read_bytes()
        if current == expected:
            print('*** Begin Patch\n*** End Patch')
            return
        require(path == BINDINGS and (sha(current), len(current)) == PRIOR_IDENTITY, 'Unexpected edit or immutable history')
        diff = list(difflib.unified_diff(current.decode().splitlines(), expected.decode().splitlines(), n=3))
        print('*** Begin Patch\n*** Update File: ' + target.as_posix())
        for line in diff[2:]:
            print('@@' if line.startswith('@@') else line)
    else:
        print('*** Begin Patch\n*** Add File: ' + target.as_posix())
        for line in expected.decode().splitlines():
            print('+' + line)
    print('*** End Patch')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-patch')
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    if args.emit_patch:
        emit(args.emit_patch)
    elif args.plan:
        artifacts, _, changes, _, _ = expected_documents()
        print(json.dumps({'artifacts': [identity(p, raw) for p, raw in artifacts.items()], 'changes': changes}, ensure_ascii=False, indent=2))
    else:
        report = verify_current()
        print(json.dumps({k: report[k] for k in ('status', 'counts', 'current_file')}, indent=2))

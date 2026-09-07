"""Read-only exact verification of the six applied OLP0035 decisions.

No TeX, production writes, global registry updates, or corpus-wide scans.
Canonical mark order is separate from semantic judgment. Formula checks do
not certify the remainder of the Classical reader.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
import unittest

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / 'evidence/classical/repairs/OLP0035_EQUINUMEROSITY_CONSTRUCTIONS_20260907.json'
SPEC = importlib.util.spec_from_file_location('equ0035_static', REPO / 'build/validate_classical_overlay.py')
STATIC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = STATIC
SPEC.loader.exec_module(STATIC)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def replace_once(raw, old, new):
    old, new = old.encode('utf-8'), new.encode('utf-8')
    if raw.count(old) != 1:
        raise ValueError('Expected one exact literal')
    return raw.replace(old, new, 1)


def math_bodies(text):
    parsed = STATIC.analyze(text)
    if parsed.errors:
        raise ValueError(parsed.errors)
    return [(kind, STATIC.raw_body(parsed, tokens)) for kind, tokens in parsed.formulas]


def remove_olsiz_note(text):
    pattern = r'\\begin\{editorial\}\s*\\textbf\{[^\n]*OLSIZ-006[^\n]*\n.*?\\end\{editorial\}'
    matches = list(re.finditer(pattern, text, re.S))
    if len(matches) != 1:
        raise ValueError('Expected one named OLSIZ-006 note')
    m = matches[0]
    return text[:m.start()] + text[m.end():], m.group()


def language_contract(text, edition):
    if edition == 'msa':
        required = [r'دالتها العكسية $f^{-1}$ موجودة وهي أيضًا !!{bijective}']
    else:
        required = [
            r'توجد دالتها العكسية $f^{-1}$، وهي !!{bijective}',
            r'والدالة المركبة منهما $\comp{f}{g}\colon A \to C$ !!{bijective}، فيثبت بها',
            r'فالدالة المركبة $\comp{g}{f} \colon \PosInt \to B$ !!{surjective}',
            r'\emph{أيًّا}',
        ]
        if text.count('إذ لو لم تكن الثانية خالية، لوجد') != 2:
            raise ValueError('Missing explicit B-nonempty counter-assumption')
        if text.count('؛ وإلا وجد'):
            raise ValueError('Ambiguous otherwise survived')
        if r'وأما إذا وجدت $g\colon \PosInt \to A$ !!{surjective}' not in text:
            raise ValueError('First nonempty branch changed')
        if r'وأما مع وجود !!{bijection}~$g$' not in text:
            raise ValueError('Alternative nonempty branch changed')
    for literal in required:
        if text.count(literal) != 1:
            raise ValueError('Missing or duplicated repaired construction: ' + literal)


class EquinumerosityConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_bytes())
        cls.txs = {x['path']: x for x in cls.data['transactions']}
        cls.before, cls.after = {}, {}
        for row in cls.data['primary_source_inventory']:
            raw = (REPO / row['path']).read_bytes()
            if (len(raw), sha(raw)) != (row['after_bytes'], row['after_sha256']):
                raise AssertionError('Unrecognized live source transition: ' + row['path'])
            cls.after[row['path']] = raw
            for patch in reversed(cls.txs.get(row['path'], {}).get('patches', [])):
                raw = replace_once(raw, patch['after'], patch['before'])
            cls.before[row['path']] = raw
        cls.english_path = next(r['path'] for r in cls.data['primary_source_inventory'] if r['edition'] == 'english')

    def check_location(self, raw, location):
        start, end = location['byte_start'], location['byte_end']
        self.assertGreaterEqual(start, 0)
        self.assertGreater(end, start)
        self.assertLessEqual(end, len(raw))
        self.assertEqual(raw[start:end], location['text'].encode('utf-8'))
        self.assertEqual(raw[:start].count(b'\n') + 1, location['line_start'])
        self.assertEqual(raw[:end - 1].count(b'\n') + 1, location['line_end'])
        self.assertEqual('\n'.join(raw.decode().splitlines()[location['line_start'] - 1:location['line_end']]), location['excerpt'])

    def test_scope_six_decisions_seven_patches_only_two_targets(self):
        self.assertEqual(len(self.data['decisions']), 6)
        self.assertEqual(len(self.txs), 2)
        self.assertEqual(sum(len(t['patches']) for t in self.txs.values()), 7)
        self.assertEqual({t['edition'] for t in self.txs.values()}, {'msa', 'classical'})
        self.assertEqual({d['decision_id'] for d in self.data['decisions']}, {
            'AR-OLP0035-ar-G09', 'AR-OLP0035-ar-classical-G09',
            'AR-OLP0035-ar-classical-G10', 'AR-OLP0035-ar-classical-G14',
            'AR-OLP0035-ar-classical-G15', 'AR-OLP0035-ar-classical-NFC01'})

    def test_complete_before_after_hashes_and_reversible_replay(self):
        for row in self.data['primary_source_inventory']:
            with self.subTest(path=row['path']):
                for phase, values in [('before', self.before), ('after', self.after)]:
                    self.assertEqual((len(values[row['path']]), sha(values[row['path']])),
                                     (row[phase + '_bytes'], row[phase + '_sha256']))
                replay = self.before[row['path']]
                for patch in self.txs.get(row['path'], {}).get('patches', []):
                    replay = replace_once(replay, patch['before'], patch['after'])
                self.assertEqual(replay, self.after[row['path']])
                self.assertEqual(replay.count(b'\n'), self.before[row['path']].count(b'\n'))
        self.assertEqual(self.before[self.english_path], self.after[self.english_path])

    def test_exact_patch_locations_and_complete_decision_ownership(self):
        owned = set()
        for tx in self.txs.values():
            for patch in tx['patches']:
                self.assertEqual(patch['occurrences'], 1)
                owned.update(patch['decision_ids'])
                for phase, values in [('before', self.before), ('after', self.after)]:
                    self.assertEqual(patch[phase], patch[phase + '_location']['text'])
                    self.check_location(values[tx['path']], patch[phase + '_location'])
        self.assertEqual(owned, {d['decision_id'] for d in self.data['decisions']})

    def test_each_raw_formula_macro_reference_and_comment_unchanged(self):
        for path in self.txs:
            before, after = self.before[path].decode(), self.after[path].decode()
            result = STATIC.compare(before, after)
            self.assertEqual(result['failures'], [])
            self.assertTrue(all(result['checks'].values()))
            self.assertEqual(result['declared_exceptions'], [])
            self.assertEqual(math_bodies(before), math_bodies(after))
            self.assertEqual(len(math_bodies(after)), 78)
            a, b = STATIC.analyze(before), STATIC.analyze(after)
            for field in ('keys', 'terminology', 'environments', 'formal_commands', 'imports', 'protected'):
                self.assertEqual(getattr(a, field), getattr(b, field), field)
            self.assertEqual(re.findall(r'\\(?:[A-Za-z@]+|[^\r\n])', before), re.findall(r'\\(?:[A-Za-z@]+|[^\r\n])', after))
            self.assertEqual([s for s in before.splitlines() if s.startswith('%')], [s for s in after.splitlines() if s.startswith('%')])

    def test_original_two_formula_repairs_and_note_retained_in_both_registers(self):
        english = math_bodies(self.after[self.english_path].decode())
        self.assertEqual(len(english), 74)
        for path in self.txs:
            body, note = remove_olsiz_note(self.after[path].decode())
            before_body, before_note = remove_olsiz_note(self.before[path].decode())
            self.assertEqual(note, before_note)
            self.assertEqual(len(math_bodies(note)), 4)
            target = math_bodies(body)
            self.assertEqual(len(target), 74)
            compact = lambda item: (item[0], re.sub(r'\s+', '', item[1]))
            differences = [(i, compact(a), compact(b)) for i, (a, b) in enumerate(zip(english, target)) if compact(a) != compact(b)]
            self.assertEqual(len(differences), 2)
            for i, original, repaired in differences:
                self.assertEqual(original[1], '$g(x)=y$')
                self.assertEqual(repaired[1], '$f(x)=y$')
                self.assertEqual(original[0], repaired[0])
            self.assertNotIn('$g(x) = y$', body)

    def test_language_contract_and_unchanged_outer_assumptions(self):
        for path, tx in self.txs.items():
            language_contract(self.after[path].decode(), tx['edition'])
            if tx['edition'] == 'classical':
                text = self.after[path].decode()
                self.assertEqual(text.count(r'فإن كان $A = \emptyset$ لزم $B ='), 2)

    def test_one_canonical_mark_reordering_not_semantic_substitution(self):
        path = next(p for p, tx in self.txs.items() if tx['edition'] == 'classical')
        before, after = self.before[path].decode(), self.after[path].decode()
        self.assertNotEqual(unicodedata.normalize('NFC', before), before)
        self.assertEqual(unicodedata.normalize('NFC', after), after)
        old, new = 'أيًّا', 'أيًّا'
        self.assertEqual(unicodedata.normalize('NFC', old), new)
        self.assertEqual(sorted(map(ord, old)), sorted(map(ord, new)))
        self.assertEqual(unicodedata.normalize('NFC', before), before.replace(old, new))
        self.assertEqual(before.count(old), 1)
        self.assertEqual(after.count(new), 1)

    def test_witnesses_current_and_historical_both_byte_bound(self):
        for decision in self.data['decisions']:
            for w in decision['source_witnesses']:
                raw = (self.before if w['phase'] == 'before' else self.after)[w['path']]
                self.assertEqual((len(raw), sha(raw)), (w['bytes'], w['sha256']))
                self.check_location(raw, w)
            for w in decision['literal_review_occurrences']:
                self.assertEqual(sha(self.after[w['path']]), w['sha256'])
                self.check_location(self.after[w['path']], w)
                self.assertIsNone(w['component_printed_page'])
                self.assertIsNone(w['assembled_pdf_page'])

    def test_authority_bytes_and_actual_macro_realizations(self):
        authority = self.data['authority']
        for item in authority['manager_evidence'] + [authority['independently_inspected'], authority['independently_inspected']['visual_evidence'], authority['macro_config']]:
            raw = (REPO / item['path']).read_bytes()
            self.assertEqual((len(raw), sha(raw)), (item['bytes'], item['sha256']))
        macro = authority['macro_config']
        text = (REPO / macro['path']).read_text(encoding='utf-8')
        for line in macro['selected_exact_definitions']:
            self.assertIn(line, text.splitlines())
        self.assertIn('does not directly attest', authority['independently_inspected']['limits'])

    def test_explanations_honest_timing_and_optional_review(self):
        for d in self.data['decisions']:
            self.assertEqual(d['recording_mode'], 'contemporaneous')
            self.assertEqual(d['inherited_choice_explanation_mode'], 'retrospective-reconstruction')
            self.assertTrue(d['rationale'])
            self.assertTrue(d['open_to_correction'])
            if d['expert_review_useful']:
                self.assertTrue(d['expert_question_ar'])
            self.assertTrue(d['alternatives'])
            self.assertTrue(d['authority_checks'])
        self.assertFalse(self.data['authority']['human_response_is_gate'])

    def test_adversarial_formula_regression_is_detected(self):
        path = next(iter(self.txs))
        good = self.after[path].decode()
        damaged = good.replace('$f(x) = y$', '$g(x) = y$', 1)
        self.assertNotEqual(math_bodies(good), math_bodies(damaged))
        self.assertTrue(STATIC.compare(good, damaged)['failures'])

    def test_adversarial_scope_and_agreement_regressions_are_detected(self):
        path = next(p for p, tx in self.txs.items() if tx['edition'] == 'classical')
        good = self.after[path].decode()
        for old, new in [('إذ لو لم تكن الثانية خالية، لوجد', 'وإلا وجد'),
                         ('لم تكن الثانية خالية', 'تكن الثانية خالية'),
                         ('وهي !!{bijective}', 'وهو !!{bijective}'),
                         ('فيثبت بها', 'فيثبت به')]:
            with self.assertRaises(ValueError):
                language_contract(good.replace(old, new, 1), 'classical')

    def test_exact_replay_rejects_ambiguous_or_missing_literal(self):
        with self.assertRaises(ValueError):
            replace_once(b'aa', 'a', 'b')
        with self.assertRaises(ValueError):
            replace_once(b'a', 'b', 'c')


if __name__ == '__main__':
    unittest.main()

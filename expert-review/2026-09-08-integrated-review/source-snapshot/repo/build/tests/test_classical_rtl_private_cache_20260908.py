"""Private-cache recorder readback tests; no TeX or cache code is executed."""
from pathlib import Path
import tempfile
import unittest

from build.tests.test_classical_rtl_closure_receipt import ROOT, ReceiptFixture, validator


class PrivateCacheTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.fixture = ReceiptFixture(self.temporary.name)
        self.contract = validator.load_readback_contract(ROOT)
        self.directory = self.fixture.manifests['primary'].parent
        self.other = self.fixture.manifests['replay'].parent
        self.manifest = validator.read_json(self.fixture.manifests['primary'])

    def tearDown(self):
        self.temporary.cleanup()

    def readback(self):
        return self.contract.validate_fls(self.directory, ROOT, self.manifest, 'control', self.other)

    def test_every_input_has_individual_identity_and_exact_aggregate(self):
        facts = self.readback()
        self.assertEqual(len(facts['inputs']), facts['input_count'])
        self.assertEqual(self.contract.inventory_digest(facts['inputs']), facts['input_inventory_sha256'])
        cached = [row for row in facts['inputs'] if 'luatex-cache' in row['path']]
        self.assertEqual(len(cached), 1)
        self.assertTrue(cached[0]['path'].startswith('@OUTPUT@/texmf-cache/'))
        self.assertEqual(facts, self.fixture.payload['recorder']['primary']['control'])

    def test_absent_private_cache_is_not_accepted(self):
        fls = self.directory / 'control.fls'
        fls.write_text('\n'.join(line for line in fls.read_text().splitlines()
                                 if 'luatex-cache' not in line) + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'missing private'):
            self.readback()

    def test_shared_cache_input_is_not_accepted_even_alongside_private_cache(self):
        foreign = self.fixture.root / 'foreign/luatex-cache/generic/fonts/otl/foreign.luc'
        foreign.parent.mkdir(parents=True)
        foreign.write_bytes(b'foreign cache bytes; never executed')
        fls = self.directory / 'control.fls'
        fls.write_text(fls.read_text() + f'INPUT {foreign}\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'unexpected shared font-cache'):
            self.readback()

    def test_local_cache_byte_mutation_changes_recorded_input_identity(self):
        cache = self.directory / 'texmf-cache/luatex-cache/generic/fonts/otl/fixture.luc'
        before = self.readback()
        cache.write_bytes(cache.read_bytes() + b'mutation')
        after = self.readback()
        self.assertNotEqual(before['input_inventory_sha256'], after['input_inventory_sha256'])
        with self.assertRaisesRegex(validator.ValidationError, 'recorder differs'):
            validator.exact_fact(before, after, 'recorder')

    def test_equal_primary_replay_private_inputs_have_equal_normalized_identities(self):
        primary = self.readback()
        replay = self.contract.validate_fls(self.other, ROOT,
            validator.read_json(self.fixture.manifests['replay']), 'control', self.directory)
        self.assertEqual(primary['inputs'], replay['inputs'])
        self.assertEqual(primary['input_inventory_sha256'], replay['input_inventory_sha256'])

    def test_private_scratch_must_be_recorded_but_already_removed(self):
        scratch = self.directory / 'texmf-cache/m_t_x_t_e_s_t.tmp'
        scratch.write_bytes(b'not removed')
        with self.assertRaisesRegex(ValueError, 'persistent private recorder scratch'):
            self.readback()

    def test_no_external_output_is_admitted(self):
        fls = self.directory / 'control.fls'
        fls.write_text(fls.read_text() + f'OUTPUT {self.fixture.root / "outside.tmp"}\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'output outside build directory'):
            self.readback()


if __name__ == '__main__':
    unittest.main()

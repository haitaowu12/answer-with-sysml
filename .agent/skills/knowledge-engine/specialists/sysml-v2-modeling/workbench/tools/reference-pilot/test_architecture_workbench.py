"""Exercise the public candidate command and its source/evidence boundaries."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_architecture import recipe


CLI = Path(__file__).resolve().parents[3] / 'scripts/sysml.py'


class ArchitectureCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.input = self.root / 'reviewed.json'
        self.output = self.root / 'candidate'

    def execute(self, value):
        self.input.write_text(json.dumps(value))
        self.input_bytes = self.input.read_bytes()
        return subprocess.run([sys.executable, '-B', str(CLI), 'architecture',
            '--architecture', str(self.input), '--output', str(self.output), '--no-reader'],
            capture_output=True, text=True, cwd=self.root)

    def test_unqualified_candidate_never_claims_native_or_executed_evidence(self):
        run = self.execute(recipe())
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        result = json.loads((self.output / 'build-result.json').read_text())
        self.assertEqual(result['stages']['nativeLanguage'], 'not-run')
        self.assertEqual(result['stages']['nativeReconciliation'], 'not-run')
        self.assertEqual(result['verificationExecution'], 'not-run')
        self.assertEqual(result['engineeringAcceptance'], 'not-assessed')
        self.assertEqual(self.input.read_bytes(), self.input_bytes)
        model = (self.output / 'model.sysml').read_bytes()
        bindings = json.loads((self.output / 'bindings.json').read_text())
        self.assertEqual(bindings['modelSha256'], hashlib.sha256(model).hexdigest())

    def test_unresolved_allocation_endpoint_blocks_generation_and_retains_findings(self):
        value = recipe(); value['allocations'][0]['component'] = 'missing-responsibility'
        run = self.execute(value)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertFalse((self.output / 'model.sysml').exists())
        findings = json.loads((self.output / 'architecture-checks.json').read_text())
        self.assertFalse(findings['structuralConsistencyPassed'])
        self.assertTrue(findings['issues'])
        self.assertEqual(self.input.read_bytes(), self.input_bytes)

    def test_existing_candidate_is_preserved_on_second_build(self):
        self.assertEqual(self.execute(recipe()).returncode, 0)
        before = {p.name:p.read_bytes() for p in self.output.iterdir() if p.is_file()}
        second = self.execute(recipe())
        self.assertEqual(second.returncode, 2)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.output.iterdir() if p.is_file()})


if __name__ == '__main__':
    unittest.main()

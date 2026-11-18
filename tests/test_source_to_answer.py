"""Public worked-example traceability; not automatic prose-entailment validation."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/source-to-answer'
FIXTURE = ROOT / '.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/fixtures/architecture/tool-library'

class SourceToAnswerTests(unittest.TestCase):
    def test_source_and_model_revisions_match_claim_provenance(self):
        p = json.loads((EXAMPLE/'provenance.json').read_text())
        for name, path in [('source', FIXTURE/'source.md'), ('model', EXAMPLE/'model.sysml')]:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), p[name+'Sha256'])
        self.assertEqual(hashlib.sha256((EXAMPLE/p['authoredRecipe']).read_bytes()).hexdigest(), p['recipeSha256'])
        self.assertEqual(hashlib.sha256((EXAMPLE/p['renderedRecipe']).read_bytes()).hexdigest(), p['renderedRecipeSha256'])
        canonical = json.dumps(json.loads((EXAMPLE/p['authoredRecipe']).read_text()), sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), p['canonicalRecipeSha256'])
        self.assertEqual(len(p['claims']), 4)
        source = (FIXTURE/'source.md').read_text()
        model = (EXAMPLE/'model.sysml').read_text()
        for claim in p['claims']:
            self.assertTrue(claim['sourceRefs'])
            self.assertTrue(claim['modelElements'])
            for ref in claim['sourceRefs']: self.assertIn('## '+ref, source)
            for element in claim['modelElements']:
                self.assertTrue(element['qualifiedName'].startswith('ToolLibraryArchitecture::'))
                self.assertIn(element['qualifiedName'].split('::')[-1], model)

    def test_html_preserves_source_clauses_and_declared_unknowns(self):
        html = (EXAMPLE/'answer.html').read_text()
        for clause in range(1,9): self.assertIn('TL-%02d' % clause, html)
        self.assertIn('F_CONFIRM', html)
        self.assertIn('F_REASSESS', html)
        import re
        for path in set(re.findall(r'diagrams/[A-Za-z0-9_\-]+\.svg', html)):
            self.assertTrue((EXAMPLE/path).is_file(), path)
        for private_path in ['/Users/', '/workspace/', 'file://']: self.assertNotIn(private_path, html)

if __name__ == '__main__': unittest.main()

import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/tools/reference-pilot'))
from architecture_review import Graph
from architecture_palette import stylesheet
class PaletteTests(unittest.TestCase):
 def test_themes_change_paint_not_model_labels_or_identities(self):
  records={'F':{'id':'F','label':'Preserve literal #eff7f4','collection':'functions'},'G':{'id':'G','label':'Finish','collection':'functions'}}
  g=Graph(records,'s','m','F','Flow','What happens?');g.node('F');g.node('G');g.edge('X','F','G','Valid',kind='transition')
  views=[g.render(t) for t in ['paper','blueprint','ink']]
  def facts(view):
   root=ET.fromstring(view['svg'])
   return ([x.text for x in root.iter() if x.tag.endswith('text')],[(x.get('data-record-id'),x.get('data-mark-kind')) for x in root.iter() if x.get('data-record-id')])
  self.assertEqual(facts(views[0]),facts(views[1]));self.assertEqual(facts(views[0]),facts(views[2]))
  self.assertIn('Preserve literal #eff7f4',facts(views[0])[0])
  self.assertNotEqual(views[0]['svg'],views[1]['svg'])
  self.assertNotIn('fill="#eff7f4"',views[0]['svg'])
 def test_reader_css_uses_selected_palette(self):
  self.assertIn('#285dc5',stylesheet(':root{color:#1c655e}','blueprint'))
if __name__=='__main__':unittest.main()

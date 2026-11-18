"""Behavioral contracts for question-led, no-script-capable delivery."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from render_explanation import validate, canonical, sha, CSS
class ExplanationTests(unittest.TestCase):
 def setUp(self):
  self.model=b'package Example;'
  self.recipe={'functions':[{'id':'F','label':'Read','sourceRefs':['S1']}]}
  self.bindings={'modelSha256':sha(self.model),'recipeSha256':sha(canonical(self.recipe)),'elements':{'F':{'qualifiedName':'Example::F'}}}
  self.plan={'theme':'paper','modelSha256':sha(self.model),'sections':[{'id':'read','question':'How?','answer':'Read the source.','layout':'composition','modelIds':['F']}]}
 def check(self):return validate(self.plan,self.recipe,self.bindings,self.model)
 def test_current_bound_plan_passes(self):self.assertIn('F',self.check())
 def test_model_change_invalidates_plan(self):
  self.model+=b' ';self.assertRaises(ValueError,self.check)
 def test_recipe_change_invalidates_bindings(self):
  self.recipe['functions'][0]['label']='Write';self.assertRaises(ValueError,self.check)
 def test_stale_plan_fails(self):
  self.plan['modelSha256']='bad';self.assertRaises(ValueError,self.check)
 def test_unknown_identity_rejected(self):
  self.plan['sections'][0]['modelIds']=['GUESS'];self.assertRaises(ValueError,self.check)
 def test_duplicate_identity_rejected(self):
  self.plan['sections'][0]['modelIds']=['F','F'];self.assertRaises(ValueError,self.check)
 def test_explicit_theme_required(self):
  del self.plan['theme'];self.assertRaises(ValueError,self.check)
 def test_duplicate_anchor_rejected(self):
  self.plan['sections']*=2;self.assertRaises(ValueError,self.check)
 def test_source_grounding_required(self):
  self.recipe['functions'][0]['sourceRefs']=[];self.bindings['recipeSha256']=sha(canonical(self.recipe));self.assertRaises(ValueError,self.check)
 def test_process_cannot_invent_order(self):
  self.plan['sections'][0]['layout']='process';self.assertRaises(ValueError,self.check)
 def test_unknown_visual_form_rejected(self):
  self.plan['sections'][0]['layout']='magic';self.assertRaises(ValueError,self.check)
 def test_safe_section_id(self):
  self.plan['sections'][0]['id']='x\" onclick=\"bad';self.assertRaises(ValueError,self.check)
if __name__=='__main__':unittest.main()

class StaticDeliveryTests(unittest.TestCase):
 def sample(self):
  return b'<nav><a href="#a">A</a></nav><section id="a">Answer</section><a download="model.sysml" href="data:text/plain;base64,eA==">Model</a>'
 def test_real_links_and_visible_answers_pass(self):
  from check_explanation import check
  self.assertTrue(check(self.sample())['passed'])
 def test_hidden_answer_is_rejected(self):
  from check_explanation import check
  self.assertFalse(check(self.sample().replace(b'<section',b'<section hidden'))['passed'])
 def test_missing_link_target_rejected(self):
  from check_explanation import check
  self.assertFalse(check(self.sample().replace(b'href="#a"',b'href="#bad"'))['passed'])
 def test_inline_switch_button_rejected(self):
  from check_explanation import check
  self.assertFalse(check(self.sample()+b'<button onclick="show(1)">Switch</button>')['passed'])

"""A selected path must not discard the native transition predicates."""
import json
from pathlib import Path
from html.parser import HTMLParser
import unittest
EXAMPLE=Path(__file__).resolve().parents[1]/'examples/agent-skills'
class Guards(HTMLParser):
 def __init__(self,text):super().__init__();self.inside=False;self.in_label=False;self.current='';self.values=[];self.full_flows=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='p' and a.get('class')=='condition':self.inside=True;self.current=''
  if self.inside and tag=='span':self.in_label=True
  if tag=='details' and a.get('class')=='full-flow':self.full_flows+=1
 def handle_data(self,data):
  if self.inside and not self.in_label:self.current+=data
 def handle_endtag(self,tag):
  if tag=='span':self.in_label=False
  if tag=='p' and self.inside:self.values.append(self.current);self.inside=False
class GuardFidelityTests(unittest.TestCase):
 def test_each_displayed_transition_retains_exact_native_condition(self):
  plan=json.loads((EXAMPLE/'plan.json').read_text());recipe=json.loads((EXAMPLE/'architecture.json').read_text());scenarios={s['id']:s for s in recipe['scenarios']};expected=[];paths=0
  for section in plan['sections']:
   if section['layout']!='process':continue
   paths+=1;s=scenarios[section['scenarioId']];steps={x['id']:x['function'] for x in s['steps']}
   for a,b in zip(section['modelIds'],section['modelIds'][1:]):
    edges=[x for x in s['transitions'] if (steps[x['from']],steps[x['to']])==(a,b)]
    self.assertEqual(len(edges),1)
    expected.append(edges[0].get('condition') or 'Unconditional transition')
  actual=Guards((EXAMPLE/'answer.html').read_text())
  self.assertEqual(actual.values,expected)
  self.assertEqual(actual.full_flows,paths)
if __name__=='__main__':unittest.main()

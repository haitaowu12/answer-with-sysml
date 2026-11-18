#!/usr/bin/env python3
"""Check static delivery contracts, not browser interaction or visual quality."""
from html.parser import HTMLParser
import argparse
import hashlib
import json
from pathlib import Path
class Inspect(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.sections=[];self.errors=[];self.in_nav=False;self.downloads=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='nav':self.in_nav=True
  if tag=='a' and self.in_nav:self.links.append(a.get('href',''))
  if tag=='section':
   self.sections.append(a.get('id'))
   if 'hidden' in a or 'display:none' in a.get('style','').replace(' ',''):self.errors.append('answer hidden before script initialization')
  if any(k.startswith('on') for k in a):self.errors.append('inline-script-dependent control')
  if tag=='button':self.errors.append('button needs explicit browser-tested behavior; use a link for navigation')
  if tag=='a' and 'download' in a:self.downloads.append(a)
 def handle_endtag(self,tag):
  if tag=='nav':self.in_nav=False

def check(raw):
 p=Inspect();p.feed(raw.decode());errors=p.errors
 if len(p.ids)!=len(set(p.ids)):errors.append('duplicate document identity')
 if not p.links:errors.append('missing question navigation')
 for link in p.links:
  if not link.startswith('#') or link[1:] not in p.sections:errors.append('navigation target missing: '+link)
 if set(x[1:] for x in p.links)!=set(p.sections):errors.append('inaccessible question section')
 if not any(x.get('download','').endswith('.sysml') and x.get('href','').startswith('data:text/plain;base64,') for x in p.downloads):errors.append('native model download missing')
 return {'passed':not errors,'errors':errors,'sha256':hashlib.sha256(raw).hexdigest(),'sections':len(p.sections),'browserInteraction':'not-assessed','visualQuality':'not-assessed'}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('html',type=Path);a=parser.parse_args();r=check(a.html.read_bytes());print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 2)

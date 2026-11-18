"""Presentation-only palettes for native architecture projections."""
import re
PALETTES={
 'paper':dict(ink='#242333',text='#3f3b4e',muted='#696277',line='#ddd8e2',paper='#faf8f4',accent='#6554a4',light='#eeeaf7',edge='#786b99'),
 'blueprint':dict(ink='#152544',text='#344766',muted='#596d89',line='#cfdaeb',paper='#f1f5fc',accent='#285dc5',light='#e4ecfa',edge='#5775ad'),
 'ink':dict(ink='#292233',text='#4a3c54',muted='#72667c',line='#e0d7e4',paper='#f8f5fa',accent='#763e92',light='#f1e6f6',edge='#946b9f'),
}
def colours(theme):
 p=PALETTES[theme]
 groups={'ink':['#173c3c','#153c3a','#335e59','#144c47'], 'text':['#304849','#355f5a','#596660'], 'muted':['#637575','#718078','#5f745b','#637a5b'], 'line':['#dce5df','#a8afa9','#a0aaa4','#d8e1d7'], 'paper':['#f5f6f1','#f6f6f3'], 'accent':['#1c655e','#527975','#4c8a73'], 'light':['#e6f1eb','#eff7f4','#e7f5ef','#eef4ef','#ecf0e9'], 'edge':['#588b86']}
 return {old:p[key] for key,values in groups.items() for old in values}
def paint(value,theme):return colours(theme).get(value,value)
def stylesheet(css,theme):return re.sub(r'#[0-9a-fA-F]{6}',lambda m:paint(m[0].lower(),theme),css)

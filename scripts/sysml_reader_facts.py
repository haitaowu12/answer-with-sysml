"""Reusable, read-only queries over qualified SysML v2 engine facts.

No SysML text parser. Expressions outside the declared scalar/quantity profile
stay unknown; this module is not a language interpreter or simulation engine.
"""
from dataclasses import dataclass
import math
import re


def refs(value):
    if isinstance(value, dict) and isinstance(value.get('id'), str): return [value]
    return [r for r in value if isinstance(r, dict) and isinstance(r.get('id'), str)] if isinstance(value, list) else []


def human(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])',' ',name or '').replace('_',' ').strip()


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str = ''

    def text(self):
        return f'{self.value:g}' + (' '+self.unit if self.unit else '')


class Facts:
    def __init__(self, report, labels=None):
        if report.get('staticChecksPassed') is not True:
            raise ValueError('A statically valid SysML model is required')
        if report.get('semanticFieldsVersion', 0) < 2:
            raise ValueError('Requalify with the extended SysML semantic exporter')
        self.report = report
        self.labels = {} if labels is None else labels
        if not isinstance(self.labels, dict) or any(not isinstance(k, str) or not k.strip() or
                not isinstance(v, str) or not v.strip() for k, v in self.labels.items()):
            raise ValueError('Reader labels must map qualified names to nonempty text')
        self.ix = {e['sessionElementId']:e for e in report['elements']}
        if len(self.ix) != len(report['elements']):raise ValueError('Duplicate semantic identities')
        self.children = {}
        for e in self.ix.values():
            for owner in refs(self.sem(e,'owner')):self.children.setdefault(owner['id'],[]).append(e)
        for children in self.children.values():children.sort(key=lambda e:(e.get('line') or 0,e['sessionElementId']))

    def sem(self,e,field,default=None):
        return e.get('semantics',{}).get(field,default)

    def resolve(self,target):
        matches=[e for e in self.ix.values() if e.get('qualifiedName')==target]
        if len(matches)!=1:raise ValueError('Select one unambiguous model element: '+target)
        return matches[0]

    def eid(self,e):return e['sessionElementId']

    def named(self,e):
        if e.get('qualifiedName') in self.labels:return self.labels[e['qualifiedName']]
        if self.sem(e,'owningMembership',{}).get('metaclass')=='ObjectiveMembership':return 'Objective'
        name=human(e.get('name'))
        return name[:1].upper()+name[1:] if name else 'Unnamed '+human(e['metaclass'])

    def local(self,value):return [self.ix[r['id']] for r in refs(value) if r['id'] in self.ix]

    def members(self,e):
        # ownedMember is the engine's namespace membership, distinct from a
        # part's inherited/instantiated feature tree.
        return self.local(self.sem(e,'ownedMember',[]))

    def descendants(self,e):
        result=[];seen=set();pending=[e]
        while pending:
            item=pending.pop()
            if self.eid(item) in seen:raise ValueError('Cyclic model ownership')
            seen.add(self.eid(item));result.append(item)
            pending.extend(reversed(self.children.get(self.eid(item),[])))
            if len(seen)>3000:raise ValueError('Choose a smaller source scope')
        return result

    def direct(self,e,kinds=None):
        result=self.children.get(self.eid(e),[])
        return [x for x in result if not kinds or x['metaclass'] in kinds]

    def types(self,e):return refs(self.sem(e,'type',[]))

    def type_text(self,e):return ', '.join(human(t.get('name') or t.get('qualifiedName','').split('::')[-1]) for t in self.types(e))

    def documentation(self,e):
        return '\n'.join(self.sem(d,'body','') for d in self.local(self.sem(e,'documentation')) if self.sem(d,'body'))

    def one(self,value,what):
        rr=refs(value)
        if len(rr)!=1 or rr[0]['id'] not in self.ix:raise ValueError(what+' has an unresolved local identity')
        return self.ix[rr[0]['id']]

    def endpoint(self,ref):
        e=self.one(ref,'Endpoint')
        chain=refs(self.sem(e,'chainingFeature'))
        if chain:
            for c in chain:
                if c['id'] not in self.ix:raise ValueError('Endpoint chain leaves source evidence')
            return chain[-1]['id'], [c['id'] for c in chain]
        return self.eid(e),[self.eid(e)]

    def referenced_feature(self,expr,trail=()):
        eid=self.eid(expr)
        if eid in trail or len(trail)>20:raise ValueError('Cyclic feature reference')
        trail=trail+(eid,)
        if expr['metaclass']=='FeatureReferenceExpression':
            feature=self.one(self.sem(expr,'referent'),'Feature reference')
        elif expr['metaclass'] in ('FeatureChainExpression','FeatureChainingExpression'):
            base=self.one(self.sem(expr,'targetFeature'),'Feature chain target')
            operands=self.local(self.sem(expr,'operand'))
            if len(operands)!=1:raise ValueError('Feature chain requires one context')
            context=self.referenced_feature(operands[0],trail)
            _, chain=self.endpoint({'id':self.eid(base)})
            feature=context
            for member_id in chain:
                feature=self.feature(feature,member_id)
                alias=self.default_expression(feature)
                if alias and alias['metaclass'] in ('FeatureReferenceExpression','FeatureChainExpression','FeatureChainingExpression'):
                    feature=self.referenced_feature(alias,trail)
        else:raise ValueError('Unsupported feature-reference expression')
        chain=refs(self.sem(feature,'chainingFeature'))
        if chain:
            feature=self.one(chain[0],'Contextual feature')
            for member in chain[1:]:
                feature=self.feature(feature,member['id'])
                alias=self.default_expression(feature)
                if alias and alias['metaclass'] in ('FeatureReferenceExpression','FeatureChainExpression','FeatureChainingExpression'):
                    feature=self.referenced_feature(alias,trail)
        value=self.default_expression(feature)
        if value and value['metaclass'] in ('FeatureReferenceExpression','FeatureChainExpression','FeatureChainingExpression'):
            return self.referenced_feature(value,trail)
        return feature

    def default_expression(self,e):
        values=[x for x in self.local(self.sem(e,'ownedMembership')) if x['metaclass']=='FeatureValue']
        values+= [x for x in self.direct(e) if x['metaclass']=='FeatureValue' and x not in values]
        if len(values)>1:raise ValueError('Multiple values need an explicit evaluation context')
        return self.one(self.sem(values[0],'value'),'Declared value') if values else None

    def redefinitions(self,e):
        result=refs(self.sem(e,'redefinedFeature'))
        for relation in self.local(self.sem(e,'ownedRedefinition')):
            result.extend(refs(self.sem(relation,'general')))
        return result

    def redefining(self,e,base):
        seen=set();pending=self.redefinitions(e)
        while pending:
            r=pending.pop()
            if r['id']==base:return True
            if r['id'] in seen:continue
            seen.add(r['id'])
            if r['id'] in self.ix:pending.extend(self.redefinitions(self.ix[r['id']]))
        return False

    def feature(self,owner,base):
        candidates=[e for e in self.local(self.sem(owner,'feature',[])) if self.eid(e)==base or self.redefining(e,base)]
        # An explicit redefinition is more specific than its inherited feature.
        specific=[e for e in candidates if self.eid(e)!=base]
        candidates=specific or candidates
        if len(candidates)!=1:raise ValueError('A required feature is missing or ambiguous')
        return candidates[0]

    def expression_elements(self,e):
        result=[];pending=[e];seen=set()
        while pending:
            node=pending.pop()
            if self.eid(node) in seen:continue
            seen.add(self.eid(node));result.append(node)
            pending.extend(self.local(self.sem(node,'operand'))+self.local(self.sem(node,'argument')))
            if len(seen)>100:raise ValueError('Select a smaller expression')
        return result

    def expression_text(self,e,depth=0):
        if depth>18:raise ValueError('Expression nesting exceeds the reading profile')
        kind=e['metaclass'];v=self.sem(e,'value')
        if kind.startswith('Literal'):return str(v).lower() if isinstance(v,bool) else str(v)
        if kind=='FeatureReferenceExpression':
            r=refs(self.sem(e,'referent'))
            if r and r[0]['id'] in self.ix:
                target=self.ix[r[0]['id']];chain=refs(self.sem(target,'chainingFeature'))
                if chain:return human(chain[-1].get('name')) or '?'
                return self.named(target)
            return human(r[0].get('name')) if r else '?'
        if kind in ('FeatureChainExpression','FeatureChainingExpression'):
            try:return self.named(self.referenced_feature(e))
            except ValueError:return ' '.join(e.get('source','').split())[:180] or 'Unresolved reference'
        operands=self.local(self.sem(e,'operand',[]))
        if kind=='OperatorExpression' and operands:
            args=[self.expression_text(x,depth+1) for x in operands];op=self.sem(e,'operator','?')
            return (' '+op+' ').join(args) if op!='[' else args[0]+' ['+args[-1]+']'
        # Exact source is a quotation only; never used to infer evaluation or topology.
        return ' '.join(e.get('source','').split())[:180] or 'Expression not supplied'

    def evaluate(self,e,bindings=None,trail=()):
        bindings=bindings or {};eid=self.eid(e)
        if eid in trail or len(trail)>30:raise ValueError('Cyclic or deep declared expression')
        if eid in bindings:return bindings[eid]
        trail=trail+(eid,);kind=e['metaclass'];value=self.sem(e,'value')
        if kind in ('LiteralInteger','LiteralRational') and isinstance(value,(int,float)) and not isinstance(value,bool):
            if not math.isfinite(value):raise ValueError('Non-finite quantity')
            return Quantity(value)
        if kind=='FeatureReferenceExpression':
            target=self.referenced_feature(e);return self.evaluate(target,bindings,trail)
        if kind in ('FeatureChainExpression','FeatureChainingExpression'):
            return self.evaluate(self.referenced_feature(e),bindings,trail)
        if kind=='OperatorExpression':
            operands=self.local(self.sem(e,'operand',[]));op=self.sem(e,'operator')
            if op=='[' and len(operands)==2:
                num=self.evaluate(operands[0],bindings,trail)
                unit_refs=refs(self.sem(operands[1],'referent'))
                # Units are recognized through their engine-resolved SI identities.
                units={'SI::metre':('m',1),'SI::meter':('m',1),'SI::second':('s',1),'SI::millimetre':('m',.001),'SI::millimeter':('m',.001),'SI::kilogram':('kg',1)}
                qname=unit_refs[0].get('qualifiedName') if len(unit_refs)==1 else None
                if qname not in units:raise ValueError('Unsupported quantity unit: '+str(qname))
                unit,scale=units[qname]
                if num.unit:raise ValueError('Nested unit construction is outside the profile')
                return Quantity(num.value*scale,unit)
            values=[self.evaluate(x,bindings,trail) for x in operands]
            if op in ('+','-') and len(values)==2 and values[0].unit==values[1].unit:
                return Quantity(values[0].value+(1 if op=='+' else -1)*values[1].value,values[0].unit)
            if op=='*' and len(values)==2 and not (values[0].unit and values[1].unit):
                return Quantity(values[0].value*values[1].value,values[0].unit or values[1].unit)
            raise ValueError('Expression is outside the declared arithmetic profile: '+str(op))
        expr=self.default_expression(e)
        if expr:return self.evaluate(expr,bindings,trail)
        # A contextual feature can inherit a value from a local source definition.
        base=self.local(self.redefinitions(e))
        if len(base)==1:return self.evaluate(base[0],bindings,trail)
        raise ValueError('No declared numeric value for '+self.named(e))

    def value_text(self,e):
        try:return self.evaluate(e).text()
        except ValueError:
            expr=self.default_expression(e)
            return self.expression_text(expr) if expr else 'Not supplied'

"""Concern-specific SysML v2 projections from managed, typed engine facts."""
from sysml_reader_facts import Facts, refs, human

STANDARD = {'viewpoints':'GeneralView','use-cases':'GeneralView','membership':'BrowserView',
    'definition-usage':'GeneralView','scenarios':'SequenceView','action-flow':'ActionFlowView',
    'state-regions':'StateTransitionView','allocation':'GridView','verification-coverage':'GridView',
    'parameters':'InterconnectionView','analysis':'GeneralView','configuration':'GeneralView',
    'geometry':'GeometryView','time':'GridView','requirements':'GeneralView'}
QUESTIONS = {
    'viewpoints':'Whose concerns do these views address?', 'use-cases':'What useful outcomes does the system provide?',
    'membership':'How is the model organized?', 'definition-usage':'Which definitions are used in this context?',
    'scenarios':'Who exchanges what, in which declared order?', 'action-flow':'How are these actions coordinated?',
    'state-regions':'Which state regions coexist?', 'allocation':'Which component is responsible for each function?',
    'verification-coverage':'Which requirements have planned verification?', 'parameters':'Which values are bound, calculated or constrained?',
    'analysis':'What does the declared analysis conclude?', 'configuration':'Which variants and selections are declared?',
    'geometry':'Which shapes and dimensions are declared?', 'time':'How is the declared timing budget distributed?',
    'requirements':'What is required, assumed and satisfied?'}


class Projection:
    def __init__(self,f,root,profile,request):
        self.f=f;self.root=root;self.profile=profile;self.request=request
        self.nodes={};self.edges=[];self.rows=[];self.warnings=[];self.detail={}
        self.mode='graph'

    def node(self,e,*,id=None,label=None,role=None,parent=None,**extra):
        eid=self.f.eid(e);key=id or eid
        if key not in self.nodes:
            node={'id':key,'elementId':eid,'label':label or self.f.named(e),'role':role or e['metaclass'],
                  'metaclass':e['metaclass'],'sublabel':self.f.type_text(e),'parent':parent,**extra}
            if '/' in key:node['selectionKey']='occurrence:'+key
            self.nodes[key]=node
        return key

    def edge(self,e,a,b,label,kind='trace',**extra):
        if a not in self.nodes or b not in self.nodes:raise ValueError('A relationship leaves the visible semantic scope')
        edge={'id':'p'+str(len(self.edges)+1),'elementId':self.f.eid(e),'source':a,'target':b,
              'label':label,'kind':kind,**extra};self.edges.append(edge);return edge

    def row(self,e,title,body):
        self.rows.append({'title':title,'body':body,'elementIds':[self.f.eid(e)]})

    def result(self):
        if not self.nodes:raise ValueError('No semantic facts in the selected view')
        return {'viewKind':self.profile,'title':self.request.get('label',self.f.named(self.root)),
            'question':self.request.get('question',QUESTIONS[self.profile]),'scopeElementId':self.f.eid(self.root),
            'scopeLabel':self.f.named(self.root),'scope':self.root.get('qualifiedName'),
            'sourceSha256':self.f.report['sourceSha256'],'nodes':list(self.nodes.values()),'edges':self.edges,
            'rows':self.rows,'components':[],'legendItems':[], 'statement':self.f.documentation(self.root),
            'warnings':self.warnings,'omissions':[],'presentation':self.mode,'details':self.detail}


def viewpoints(p):
    f=p.f
    elements=f.descendants(p.root)
    allowed={'ConcernUsage','ViewpointUsage','ViewUsage','PartUsage'}
    for e in elements:
        if e['metaclass'] in allowed and e.get('name'):p.node(e)
    for e in elements:
        if f.eid(e) not in p.nodes:continue
        for field,label in [('framedConcern','Frames'),('satisfiedViewpoint','Satisfies'),('stakeholderParameter','Stakeholder')]:
            for target in f.local(f.sem(e,field)):
                p.node(target);p.edge(e,f.eid(e),f.eid(target),label)
        if e['metaclass']=='ViewUsage':
            for assertion in f.direct(e,{'SatisfyRequirementUsage'}):
                target=f.one(f.sem(assertion,'satisfiedRequirement'),'Satisfied viewpoint')
                p.node(target);p.edge(assertion,f.eid(e),f.eid(target),'Satisfies')
            # Exposed content is scope evidence; avoid flooding the concern map.
            p.row(e,f.named(e),str(len(refs(f.sem(e,'exposedElement'))))+' exposed model elements')


def use_cases(p):
    f=p.f;cases=[e for e in f.descendants(p.root) if e['metaclass'] in ('UseCaseUsage','UseCaseDefinition')]
    for e in cases:p.node(e)
    for e in cases:
        for field,label in [('subjectParameter','Subject'),('actorParameter','Actor')]:
            for role in f.local(f.sem(e,field)):
                p.node(role,role=label)
                p.edge(role,f.eid(e),f.eid(role),label)
        for included in f.direct(e,{'IncludeUseCaseUsage'}):
            target=f.one(f.sem(included,'useCaseIncluded') or f.sem(included,'performedAction'),'Included use case')
            p.node(target);p.edge(included,f.eid(e),f.eid(target),'Includes')
        for objective in f.local(f.sem(e,'objectiveRequirement')):
            text=f.documentation(objective)
            if text:p.row(objective,f.named(e)+' · Objective',text)


def membership(p):
    f=p.f;p.mode='browser'
    kinds={'Package','PartDefinition','PartUsage','ItemDefinition','ItemUsage','PortDefinition','PortUsage',
           'ActionDefinition','ActionUsage','PerformActionUsage','StateDefinition','StateUsage','ExhibitStateUsage',
           'RequirementUsage','RequirementDefinition','VerificationCaseDefinition','VerificationCaseUsage',
           'AnalysisCaseDefinition','AnalysisCaseUsage','CalculationDefinition','CalculationUsage','ConstraintUsage','AttributeUsage',
           'UseCaseUsage','ViewUsage','ViewpointUsage','ConcernUsage','AllocationUsage','FlowUsage'}
    def visit(e,parent=None,depth=0):
        if depth>10:raise ValueError('Membership view exceeds its depth profile')
        key=p.node(e,parent=parent)
        for member in f.members(e):
            if member.get('name') and member['metaclass'] in kinds:
                child=visit(member,key,depth+1);p.edge(member,key,child,'Owns','containment')
        return key
    visit(p.root)
    p.detail['libraryMemberships']='Imported library content is outside this source browser.'


def definitions(p):
    f=p.f
    root=p.root
    selected=f.direct(root,{'PartUsage','PortUsage','ItemUsage','AttributeUsage','ActionUsage','PerformActionUsage'})
    if root['metaclass']=='Package':selected=f.direct(root,{'PartUsage'})
    for e in selected:
        p.node(e)
        for target in f.local(f.sem(e,'type')):
            if not target['metaclass'].endswith('Definition'):continue
            p.node(target);p.edge(e,f.eid(e),f.eid(target),'Defined by','typing')
    for e in list(p.nodes.values()):
        source=f.ix[e['elementId']]
        for target in f.local(f.sem(source,'general')):
            if target['metaclass'].endswith('Definition'):
                p.node(target);p.edge(source,f.eid(source),f.eid(target),'Specializes','specialization')
    p.detail['scopeNote']='Direct source usages and their declared source definitions.'


ACTION_NODES={'ActionUsage','PerformActionUsage','ForkNode','JoinNode','DecisionNode','MergeNode',
              'SendActionUsage','AcceptActionUsage'}
CONTROL={'ForkNode','JoinNode','DecisionNode','MergeNode'}
RELATIONS={'SuccessionAsUsage','SuccessionFlowUsage','FlowUsage','BindingConnectorAsUsage','TransitionUsage'}


def action_flow(p):
    f=p.f;root=p.root;rootid=f.eid(root);p.mode='actions'
    owners=[root];pending=[root]
    while pending:
        owner=pending.pop()
        for e in f.direct(owner):
            if e['metaclass'] in ACTION_NODES:
                p.node(e,parent=None if owner==root else f.eid(owner))
                nested=f.direct(e,ACTION_NODES)
                if nested:owners.append(e);pending.append(e)
                for param in f.local(f.sem(e,'feature',[])):
                    if f.sem(param,'direction') in ('in','out','inout') and param['metaclass'] in ('ReferenceUsage','AttributeUsage','ItemUsage'):
                        p.node(param,id=f.eid(e)+'/'+f.eid(param),role='parameter',parent=f.eid(e),
                               direction=f.sem(param,'direction'),sublabel=f.type_text(param))
            elif e['metaclass'].endswith('ActionUsage') and e['metaclass'] not in {'TransitionUsage','CalculationUsage'}:
                raise ValueError('Action subtype needs its own semantic profile: '+e['metaclass'])
    def endpoint(ref,relation):
        rr=refs(ref)
        if len(rr)!=1:raise ValueError('Action relation requires one source and one target')
        if rr[0]['id'] not in f.ix:
            q=rr[0].get('qualifiedName')
            if q not in ('Actions::Action::start','Actions::Action::done'):
                raise ValueError('Unresolved action endpoint')
            key=rr[0]['id']
            p.node(relation,id=key,label='Entry' if q.endswith('::start') else 'Done',role='boundary',boundary=q.split('::')[-1])
            return key
        eid,chain=f.endpoint(rr)
        key='/'.join(chain)
        if key in p.nodes:return key
        if eid in p.nodes:return eid
        raise ValueError('An action relationship leaves the selected control/parameter scope')
    for owner in owners:
        for e in f.direct(owner,RELATIONS):
            a=endpoint(f.sem(e,'source' if e['metaclass']=='TransitionUsage' else 'sourceFeature'),e)
            b=endpoint(f.sem(e,'target' if e['metaclass']=='TransitionUsage' else 'targetFeature'),e)
            kind='binding' if e['metaclass']=='BindingConnectorAsUsage' else 'item-flow' if e['metaclass']=='FlowUsage' else 'control'
            if kind=='item-flow':
                def flow_parameter(action_key,field):
                    end=f.one(f.sem(e,field),'Flow parameter')
                    candidates=[action_key+'/'+r['id'] for r in f.redefinitions(end) if action_key+'/'+r['id'] in p.nodes]
                    if len(candidates)!=1:raise ValueError('Item transfer requires one exact contextual parameter endpoint')
                    return candidates[0]
                a=flow_parameter(a,'sourceOutputFeature');b=flow_parameter(b,'targetInputFeature')
            label='Same value' if kind=='binding' else 'Item flow' if kind=='item-flow' else ''
            guards=f.local(f.sem(e,'guardExpression'))
            if guards:label='['+'; '.join(f.expression_text(g) for g in guards)+']'
            p.edge(e,a,b,label,kind)
    p.detail['legend']=['Dashed arrows: control succession','Solid arrows: item transfer','Bars: fork / join; diamonds: decision / merge']
    p.detail['scopeNote']='Declared coordination and parameters; not an execution trace.'


def state_regions(p):
    f=p.f;p.mode='regions';owners=[]
    def visit(e,parent=None):
        if f.sem(e,'isParallel') not in (True,False):raise ValueError('State concurrency is unknown; requalify first')
        p.node(e,parent=parent,parallel=f.sem(e,'isParallel'),sublabel='')
        owners.append(e)
        for field,label in [('entryAction','Entry'),('doAction','During'),('exitAction','Exit')]:
            for action in f.local(f.sem(e,field)):
                if action.get('name') not in (None,'entryAction','doAction','exitAction') or action.get('source','').strip() not in ('entry;','exit;'):
                    p.row(action,f.named(e)+' · '+label, f.named(action) if action.get('name') not in ('entryAction','doAction','exitAction') else label+' action')
        for child in f.direct(e,{'StateUsage','ExhibitStateUsage'}):visit(child,f.eid(e))
    visit(p.root)
    for owner in owners:
        for e in f.direct(owner,{'TransitionUsage'}):
            a=f.one(f.sem(e,'source'),'Transition source');b=f.one(f.sem(e,'target'),'Transition target')
            if f.eid(a) not in p.nodes or f.eid(b) not in p.nodes:raise ValueError('Transition exits the selected state scope')
            for field in ('triggerAction','guardExpression','effectAction'):
                if not isinstance(e.get('semantics',{}).get(field),list):raise ValueError('Transition condition is unknown; requalify first')
            triggers=[]
            for trigger in f.local(f.sem(e,'triggerAction')):
                payload=f.local(f.sem(trigger,'payloadParameter'))
                triggers.append(', '.join(f.type_text(x) for x in payload) or f.named(trigger))
            guards=[f.expression_text(g) for g in f.local(f.sem(e,'guardExpression'))]
            effects=[f.named(a) for a in f.local(f.sem(e,'effectAction'))]
            label=' · '.join(triggers)+(' ['+'; '.join(guards)+']' if guards else '')+(' / '+', '.join(effects) if effects else '')
            p.edge(e,f.eid(a),f.eid(b),label,'transition')
            p.row(e,f.named(a)+' → '+f.named(b),label or 'Unconditional transition')
        # Initial entry uses the exact exported action or membership witness.
        entries=f.local(f.sem(owner,'entryAction'))
        declarations=f.local(f.sem(owner,'entryDeclaration'))
        entryids={f.eid(x) for x in entries+declarations}
        for e in f.direct(owner,{'SuccessionAsUsage'}):
            ar=refs(f.sem(e,'source'));br=refs(f.sem(e,'target'))
            if len(ar)==1 and len(br)==1 and ar[0]['id'] in entryids and br[0]['id'] in p.nodes:
                action=f.ix[ar[0]['id']];key=p.node(action,label='Entry',role='entry',parent=f.eid(owner))
                p.edge(e,key,br[0]['id'],'','transition')
    p.detail['legend']=['Side-by-side regions marked concurrent coexist.','Arrows: trigger [guard] / effect; entry markers require a source declaration.']


def allocation(p):
    f=p.f;p.mode='matrix';rows=[];cols=[]
    for e in f.descendants(p.root):
        if e['metaclass']!='AllocationUsage':continue
        endpoints=refs(f.sem(e,'relatedFeature'))
        if len(endpoints)!=2:raise ValueError('Allocation needs exactly two resolved endpoints')
        keys=[]
        for ref in endpoints:
            eid,chain=f.endpoint(ref);target=f.ix[eid]
            key=p.node(target,id='/'.join(chain),role='function' if not keys else 'component')
            keys.append(key)
        if keys[0] not in rows:rows.append(keys[0])
        if keys[1] not in cols:cols.append(keys[1])
        p.edge(e,*keys,'Allocated','allocation')
    p.detail.update(rowIds=rows,columnIds=cols,matrixCaption='Rows: source intent · columns: responsible target · blank cells mean no represented allocation')


def verification(p):
    f=p.f;p.mode='matrix'
    requirements=[e for e in f.descendants(p.root) if e['metaclass']=='RequirementUsage' and
                  (not f.sem(e,'owner') or f.one(f.sem(e,'owner'),'Requirement owner')['metaclass'] not in ('VerificationCaseDefinition','VerificationCaseUsage'))
                  and e.get('name')]
    checks=[e for e in f.descendants(p.root) if e['metaclass'] in ('VerificationCaseDefinition','VerificationCaseUsage') and e.get('name')]
    # Only actual source requirements outside case-objective scaffolding form rows.
    requirements=[e for e in requirements if not any(a['metaclass'] in ('VerificationCaseDefinition','VerificationCaseUsage','UseCaseDefinition','UseCaseUsage','AnalysisCaseDefinition','AnalysisCaseUsage','ObjectiveMembership') for a in ancestors(f,e))]
    for e in requirements:p.node(e,role='requirement')
    for e in checks:
        result=f.local(f.sem(e,'result'))
        if any(f.default_expression(r) for r in result):
            raise ValueError('A bound verification result needs a separate executed-evidence profile')
        p.node(e,role='verification',sublabel='Planned · no executed verdict')
    for check in checks:
        objective=refs(f.sem(check,'objectiveRequirement'))
        witnesses=[e for e in f.ix.values() if e['metaclass']=='RequirementVerificationMembership' and
                   any(r['id'] in {o['id'] for o in objective} for r in refs(f.sem(e,'source')))]
        for e in witnesses:
            for target in f.local(f.sem(e,'verifiedRequirement')):
                if f.eid(target) not in p.nodes:
                    subset=f.local(f.sem(target,'subsettedFeature'));target=next((x for x in subset if f.eid(x) in p.nodes),target)
                if f.eid(target) not in p.nodes:raise ValueError('Verification target is outside the obligation inventory')
                p.edge(e,f.eid(target),f.eid(check),'Planned verification','verify')
        for e in f.direct(check,{'ActionUsage','PerformActionUsage'}):p.row(e,f.named(check)+' · Procedure',f.named(e))
    p.detail.update(rowIds=[f.eid(e) for e in requirements],columnIds=[f.eid(e) for e in checks],matrixCaption='Rows: requirements · columns: planned verification cases · no executed verdict is asserted')


def ancestors(f,e):
    result=[];seen=set()
    while refs(f.sem(e,'owner')):
        e=f.one(f.sem(e,'owner'),'Owner')
        if f.eid(e) in seen:raise ValueError('Cyclic ownership')
        seen.add(f.eid(e));result.append(e)
    return result


def requirements(p):
    f=p.f
    for req in f.descendants(p.root):
        if req['metaclass']!='RequirementUsage' or not req.get('name'):continue
        if any(a['metaclass'] in ('UseCaseUsage','VerificationCaseDefinition','VerificationCaseUsage','AnalysisCaseUsage') for a in ancestors(f,req)):continue
        p.node(req,role='requirement',sublabel='Requirement')
        statement=f.documentation(req)
        if statement:p.row(req,f.named(req),statement)
        for subject in f.local(f.sem(req,'subjectParameter')):
            p.node(subject,role='subject',sublabel='Subject · '+f.type_text(subject));p.edge(subject,f.eid(req),f.eid(subject),'Subject')
        for field,label in [('assumedConstraint','Assumes'),('requiredConstraint','Requires')]:
            for constraint in f.local(f.sem(req,field)):
                expressions=[x for x in f.direct(constraint) if x['metaclass'].endswith('Expression')]
                formula=f.expression_text(expressions[0]) if len(expressions)==1 else 'Inspect constraint source'
                p.node(constraint,label=formula,role='constraint',sublabel=label+' constraint')
                p.edge(constraint,f.eid(req),f.eid(constraint),label,'constraint')
    for assertion in f.descendants(p.root):
        if assertion['metaclass']!='SatisfyRequirementUsage':continue
        target=f.local(f.sem(assertion,'satisfiedRequirement'))
        if len(target)!=1 or f.eid(target[0]) not in p.nodes:continue
        values=f.local(f.sem(assertion,'satisfyingFeature'))
        if len(values)!=1:raise ValueError('Satisfaction has an unresolved satisfying feature')
        actual=values[0]
        if actual['metaclass'].endswith('Expression'):actual=f.referenced_feature(actual)
        p.node(actual,role='component');polarity=f.sem(assertion,'isNegated')
        if type(polarity) is not bool:raise ValueError('Satisfaction polarity is unknown')
        p.edge(assertion,f.eid(actual),f.eid(target[0]),'Does not satisfy' if polarity else 'Satisfies (asserted)','satisfaction')
    p.detail['scopeNote']='Requirements and design assertions; verification coverage and executed evidence remain separate.'


def configuration(p):
    f=p.f
    for e in f.descendants(p.root):
        if f.sem(e,'isVariation') is not True:continue
        p.node(e,role='variation',sublabel='Variation point')
        for v in f.local(f.sem(e,'variant')):
            p.node(v,role='variant',sublabel='Variant')
            p.edge(v,f.eid(e),f.eid(v),'Variant','containment')
            for value in f.direct(v,{'AttributeUsage'}):p.row(value,f.named(v)+' · '+f.named(value),f.value_text(value))
    for e in f.descendants(p.root):
        if e['metaclass']!='PartUsage' or f.sem(e,'isVariation'):continue
        expr=f.default_expression(e)
        if not expr:continue
        rr=refs(f.sem(expr,'referent'))
        if len(rr)==1 and rr[0]['id'] in p.nodes:
            p.node(e,role='configuration',sublabel='Declared selection')
            p.edge(e,f.eid(e),rr[0]['id'],'Selects','selection')


def parameters(p):
    f=p.f;root=p.root;p.node(root,role='calculation')
    types=f.local(f.sem(root,'type'));definition=next((e for e in types if e['metaclass']=='CalculationDefinition'),None)
    if not definition:raise ValueError('Select a calculation usage with a local definition')
    p.node(definition,role='calculation-definition');p.edge(root,f.eid(root),f.eid(definition),'Defined by','typing')
    for param in f.local(f.sem(root,'feature')):
        if f.sem(param,'direction') not in ('in','out'):continue
        p.node(param,role='parameter',direction=f.sem(param,'direction'),sublabel=f.value_text(param))
        p.edge(param,f.eid(param) if f.sem(param,'direction')=='in' else f.eid(root),f.eid(root) if f.sem(param,'direction')=='in' else f.eid(param),f.sem(param,'direction'),'parameter')
        expr=f.default_expression(param)
        if expr:
            p.row(param,f.named(param),f.expression_text(expr))
            if f.sem(param,'direction')=='in' and expr['metaclass'] in ('FeatureReferenceExpression','FeatureChainExpression'):
                source=f.referenced_feature(expr);p.node(source,role='value',sublabel=f.value_text(source))
                p.edge(expr,f.eid(source),f.eid(param),'Bound value','binding')
    for target in p.request.get('constraints',[]):
        constraint=f.resolve(target)
        if constraint['metaclass'] not in ('ConstraintUsage','AssertConstraintUsage'):raise ValueError('Select a typed constraint')
        expressions=[x for x in f.direct(constraint) if x['metaclass'].endswith('Expression')]
        if len(expressions)!=1:raise ValueError('Constraint needs one declared predicate in this profile')
        p.node(constraint,role='constraint',sublabel=f.expression_text(expressions[0]))
        p.row(constraint,f.named(constraint),f.expression_text(expressions[0]))
        # Exact expression referents supply the constraint's inputs.
        for expression in f.expression_elements(expressions[0]):
            if expression['metaclass']!='FeatureChainExpression':continue
            feature=f.referenced_feature(expression);p.node(feature,role='parameter',sublabel=f.value_text(feature))
            p.edge(expression,f.eid(constraint),f.eid(feature),'References','reference')
    p.detail['scopeNote']='Declared parameter values and equations; arbitrary solver execution is outside this view.'


def analysis(p):
    f=p.f;cases=[p.root] if p.root['metaclass'] in ('AnalysisCaseUsage','AnalysisCaseDefinition') else f.direct(p.root,{'AnalysisCaseUsage','AnalysisCaseDefinition'})
    if not cases:raise ValueError('Select an analysis case or a package of analysis cases')
    results=[]
    for case in cases:
        p.node(case,role='analysis')
        for subject in f.local(f.sem(case,'subjectParameter')):
            p.node(subject,role='subject');p.edge(subject,f.eid(case),f.eid(subject),'Subject')
        for objective in f.local(f.sem(case,'objectiveRequirement')):
            p.node(objective,label='Objective',role='objective',sublabel='Analysis objective')
            p.edge(objective,f.eid(case),f.eid(objective),'Objective')
            if f.documentation(objective):p.row(objective,f.named(case)+' · Objective',f.documentation(objective))
        for calc in f.direct(case,{'CalculationUsage'}):
            result=calculation_result(f,calc)
            p.node(calc,role='calculation',sublabel='Declared result: '+result.text());p.edge(calc,f.eid(case),f.eid(calc),'Calculation')
            for param in f.direct(calc,{'ReferenceUsage','AttributeUsage'}):
                if f.sem(param,'direction')=='in':p.row(param,f.named(case)+' · '+f.named(param),f.value_text(param))
            p.row(calc,f.named(case)+' · '+f.named(calc),result.text())
            results.append({'label':f.named(case),'value':result.value,'unit':result.unit,'elementId':f.eid(calc)})
    if not results:raise ValueError('Analysis has no supported declared calculation')
    p.detail['results']=results
    if len(results)==1:p.detail['result']=results[0]
    p.detail['scopeNote']='Calculated from the declared inputs and equations; no physical test result is asserted.'


def calculation_result(f,calc):
    definition=next((e for e in f.local(f.sem(calc,'type')) if e['metaclass']=='CalculationDefinition'),None)
    if not definition:raise ValueError('Calculation definition is outside source evidence')
    bindings={}
    for base in f.direct(definition):
        if f.sem(base,'direction')=='in':
            actual=f.feature(calc,f.eid(base));bindings[f.eid(base)]=f.evaluate(actual)
    results=f.local(f.sem(definition,'result'))
    if len(results)!=1:raise ValueError('Calculation requires one explicit result')
    return f.evaluate(results[0],bindings)


def geometry(p):
    f=p.f;p.mode='geometry';shapes=[]
    for e in f.descendants(p.root):
        if not any(t.get('qualifiedName')=='ShapeItems::RectangularCuboid' for t in f.types(e)):continue
        dims={};witnesses={}
        for base in ('length','width','height'):
            attrs=[a for a in f.direct(e) if any(r.get('qualifiedName')=='ShapeItems::RectangularCuboid::'+base for r in f.redefinitions(a))]
            if len(attrs)!=1:raise ValueError('Box dimension is missing or ambiguous: '+base)
            q=f.evaluate(attrs[0])
            if q.unit!='m' or q.value<=0:raise ValueError('Box dimensions must be positive supported length quantities')
            dims[base]=q.value;witnesses[base]=f.eid(attrs[0])
            p.row(attrs[0],human(base).capitalize(),q.text())
        p.node(e,role='shape',sublabel=' × '.join(f'{dims[k]:g}' for k in ('length','width','height'))+' m')
        shapes.append({'elementId':f.eid(e),'nodeId':f.eid(e),'label':f.named(e),'dimensions':dims,'dimensionWitnesses':witnesses})
    if not shapes:raise ValueError('No supported declared box geometry in this scope')
    p.detail.update(shapes=shapes,scopeNote='Box dimensions in metres. Isometric views of local shapes; assembly positions and clearances are not declared.')


def timing(p):
    f=p.f;p.mode='timing';start=f.resolve(p.request['startFeature']);duration=f.resolve(p.request['durationFeature']);spans=[]
    for e in f.direct(p.root,{'ActionUsage','PerformActionUsage'}):
        a=f.feature(e,f.eid(start));b=f.feature(e,f.eid(duration));x=f.evaluate(a);d=f.evaluate(b)
        if x.unit!='s' or d.unit!='s' or d.value<0 or x.value<0:raise ValueError('Timing profile requires nonnegative second quantities')
        p.node(e,role='planned-action',sublabel=f'{x.value:g}–{x.value+d.value:g} s')
        spans.append({'nodeId':f.eid(e),'start':x.value,'duration':d.value,'witnesses':[f.eid(a),f.eid(b)]})
    p.detail.update(spans=spans,scopeNote='Declared planning budget in seconds from cycle start; overlap does not by itself assert control-flow concurrency. Not measured execution.')


def sequence(p):
    f=p.f;p.mode='sequence';parts=f.direct(p.root,{'PartUsage'});event_owner={};lifelines=[]
    for part in parts:
        p.node(part,role='lifeline');lifelines.append(f.eid(part))
        for event in f.direct(part,{'EventOccurrenceUsage'}):
            p.node(event,role='event',parent=f.eid(part));event_owner[f.eid(event)]=f.eid(part)
    order=[];messages=[]
    for e in f.descendants(p.root):
        if e['metaclass'] not in ('FlowUsage','SuccessionAsUsage'):continue
        if e['metaclass']=='FlowUsage':
            if not any(t.get('qualifiedName')=='Flows::Message' for t in f.types(e)):
                raise ValueError('Sequence requires a declared message, not an ordinary streaming flow')
            # sourceEvent/targetEvent are the standard Message role names. Their
            # EventOccurrenceUsage.eventOccurrence bindings supply the endpoints;
            # neither source order nor visible labels supplies topology.
            def role_event(role):
                roles=[x for x in f.direct(e,{'EventOccurrenceUsage'}) if x.get('name')==role]
                if len(roles)!=1:raise ValueError('Message event role is missing or ambiguous')
                return f.sem(roles[0],'eventOccurrence')
            a,ac=f.endpoint(role_event('sourceEvent'));b,bc=f.endpoint(role_event('targetEvent'))
        else:
            a,ac=f.endpoint(f.sem(e,'sourceFeature'));b,bc=f.endpoint(f.sem(e,'targetFeature'))
        if a not in event_owner or b not in event_owner:raise ValueError('Sequence endpoint is not an exposed local event occurrence')
        if e['metaclass']=='FlowUsage':
            edge=p.edge(e,a,b,f.named(e),'message');messages.append(edge['id'])
        else:p.edge(e,a,b,'Before','succession')
        order.append((a,b))
    ranks=topological_ranks(list(event_owner),order)
    p.detail.update(lifelines=lifelines,eventRanks=ranks,messages=messages,
                   scopeNote='Vertical placement follows declared event precedence. No duration or total ordering between independent lifelines is asserted.')


def topological_ranks(nodes,edges):
    remaining=set(nodes);ranks={}
    while remaining:
        ready=[n for n in nodes if n in remaining and all(a in ranks for a,b in edges if b==n)]
        if not ready:raise ValueError('Event precedence contains a cycle')
        for n in ready:
            ranks[n]=max((ranks[a]+1 for a,b in edges if b==n),default=0);remaining.remove(n)
    return ranks


PROJECTORS={'viewpoints':viewpoints,'use-cases':use_cases,'membership':membership,'definition-usage':definitions,
    'action-flow':action_flow,'state-regions':state_regions,'allocation':allocation,'verification-coverage':verification,
    'configuration':configuration,'requirements':requirements,'parameters':parameters,'analysis':analysis,'geometry':geometry,'time':timing,'scenarios':sequence}


def project(report,request):
    f=Facts(report, labels=request.get('labels'));profile=request['readerProfile'];targets=request.get('names',request.get('targets'))
    if profile not in PROJECTORS or not isinstance(targets,list) or len(targets)!=1:raise ValueError('Unsupported semantic reader profile')
    p=Projection(f,f.resolve(targets[0]),profile,request);PROJECTORS[profile](p);return p.result()

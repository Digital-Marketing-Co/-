#!/usr/bin/env python3
"""Canonicalize explicit skill nodes and topologically order dependency phases."""
import argparse,json
ALIASES={'pe':'prompt-engineer','promptengineer':'prompt-engineer','wca-ivy-biblio':'academy-ivy-biblio','ivy-biblio':'academy-ivy-biblio','6429':'4629'}
def canonical(name):
    name=name.strip().lstrip('/$').lower()
    return ALIASES.get(name,name)
def plan(requested,dependencies=None):
    graph={}
    for node,deps in (dependencies or {}).items():
        graph.setdefault(canonical(node),[]).extend(canonical(d) for d in deps)
    done=set();active=set();ordered=[]
    def visit(node):
        node=canonical(node)
        if node in active: raise ValueError('Dependency cycle at '+node+'; use a phase handoff')
        if node in done:return
        active.add(node)
        for dep in graph.get(node,[]):visit(dep)
        active.remove(node);done.add(node);ordered.append(node)
    for node in requested:visit(node)
    return ordered
def operation_key(run,document,revision,skill,phase,input_digest,options_digest,scope):
    return (run,document,revision,canonical(skill),phase,input_digest,options_digest,scope)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('skills',nargs='+');p.add_argument('--dependencies',default='{}');a=p.parse_args()
    try:print(json.dumps(plan(a.skills,json.loads(a.dependencies))))
    except (ValueError,TypeError) as e:p.exit(1,str(e)+'\n')

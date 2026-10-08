from __future__ import annotations
import json,re,datetime
from .prompts import PLANNER,BUILDER,REVIEWER
from ..workspace import read_context,safe_write
from ..skills import context

def j(text):
    text=text.strip(); text=re.sub(r'^```(?:json)?\s*|\s*```$','',text,flags=re.I|re.S); return json.loads(text)

class Engine:
    def __init__(self,provider,ui): self.p,self.ui=provider,ui
    def run(self,req):
        root=req.workspace; root.mkdir(parents=True,exist_ok=True)
        ctx=read_context(root); skills=context()
        self.ui.phase('inspect',f'{len(ctx)} chars of local context')
        self.ui.think('architecting')
        plan=j(self.p.ask(PLANNER,f'USER REQUEST:\n{req.prompt}\n\nWORKSPACE:\n{ctx}\n\nSKILLS:\n{skills}'))
        self.ui.phase('plan',plan.get('summary','architecture contract ready'))
        self.ui.think('building')
        build=j(self.p.ask(BUILDER,f'PLAN:\n{json.dumps(plan,indent=2)}\n\nWORKSPACE:\n{ctx}\n\nSKILLS:\n{skills}\n\nImplement complete files.'))
        changed=[]
        for f in build.get('files',[]): changed.append(str(safe_write(root,f['path'],f.get('content','')).relative_to(root)))
        self.ui.phase('review',f'{len(changed)} files generated')
        self.ui.think('reviewing')
        review=j(self.p.ask(REVIEWER,f'PLAN:\n{json.dumps(plan)}\nFILES:\n{json.dumps(changed)}'))
        audit={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request':req.prompt,'plan':plan,'files':changed,'review':review}
        (root/'.fade-generation.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
        self.ui.phase('verify',review.get('status','unknown'))
        return changed,review

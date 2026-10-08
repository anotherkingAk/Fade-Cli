from __future__ import annotations
import argparse,getpass,sys
from pathlib import Path
from .config import ensure,load,save,resolve
from .providers import create
from .skills import all_skills,install,remove
from .core.engine import Engine
from .models import Request
from .ui import UI,logo,title,ok,err,warn

def main():
    ap=argparse.ArgumentParser(prog='fade',description='Fade 1.1 — local-first autonomous coding agent')
    ap.add_argument('prompt',nargs='*'); ap.add_argument('--dir',default='.',help='workspace'); ap.add_argument('--allow-run',action='store_true')
    sub=ap.add_subparsers(dest='cmd')
    sub.add_parser('init'); sub.add_parser('doctor'); sub.add_parser('version')
    k=sub.add_parser('key'); ks=k.add_subparsers(dest='action'); ks.add_parser('set'); ks.add_parser('show')
    s=sub.add_parser('skill'); ss=s.add_subparsers(dest='action'); ss.add_parser('list'); i=ss.add_parser('install'); i.add_argument('source'); r=ss.add_parser('remove'); r.add_argument('name')
    args=ap.parse_args(); ui=UI()
    if args.cmd=='version': print('Fade CLI 1.1.0'); return
    if args.cmd=='init': ensure(); print(logo()); ok('Fade initialized'); return
    if args.cmd=='doctor':
        c=resolve(); print(title()); print('provider:',c.get('provider')); print('model:',c.get('model') or '(missing)'); print('api key:', 'configured' if c.get('api_key') else 'missing'); print('skills:',len(all_skills())); return
    if args.cmd=='key':
        c=load()
        if args.action=='show': print({k:('***' if k=='api_key' and v else v) for k,v in c.items()}); return
        if args.action=='set':
            c['provider']=input(f"provider [{c.get('provider','openai')}]: ").strip() or c.get('provider','openai')
            c['model']=input(f"model [{c.get('model','')}]: ").strip() or c.get('model','')
            c['api_key']=getpass.getpass('API key: '); save(c); ok('saved locally'); return
    if args.cmd=='skill':
        if args.action=='list':
            for x in all_skills(): print('•',x.name)
            return
        if args.action=='install': ok(f'installed {install(args.source).name}'); return
        if args.action=='remove': remove(args.name); ok('removed '+args.name); return
    if not args.prompt:
        print(title()); ap.print_help(); return
    prompt=' '.join(args.prompt); root=Path(args.dir).expanduser().resolve(); c=resolve()
    try:
        print(title()); print(f'{ui.__class__.__name__}: local workspace {root}')
        files,review=Engine(create(c),ui).run(Request(prompt,root,args.allow_run))
        print(); ok(f'generated {len(files)} files'); print('workspace:',root); print('review:',review.get('status','unknown'))
        for f in files[:24]: print('  +',f)
        if len(files)>24: print(f'  … {len(files)-24} more')
    except Exception as e: err(str(e)); sys.exit(1)

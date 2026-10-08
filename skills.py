from pathlib import Path
import re, shutil, subprocess, tempfile
from .config import SKILLS

def _name(s): return re.sub(r'[^a-zA-Z0-9._-]+','-',s).strip('-') or 'skill'
def all_skills(): SKILLS.mkdir(parents=True,exist_ok=True); return sorted(p for p in SKILLS.iterdir() if p.is_dir())
def context():
    out=[]
    for p in all_skills():
        f=p/'SKILL.md'
        if f.exists(): out.append(f"## {p.name}\n{f.read_text(errors='ignore')[:10000]}")
    return '\n\n'.join(out)
def install(source):
    SKILLS.mkdir(parents=True,exist_ok=True)
    if '/' in source and not source.startswith(('http://','https://')) and not Path(source).exists(): source='https://github.com/'+source+'.git'
    if source.startswith(('http://','https://')):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'repo'; subprocess.run(['git','clone','--depth','1',source,str(d)],check=True,capture_output=True)
            target=SKILLS/_name(d.name); shutil.rmtree(target,ignore_errors=True); shutil.copytree(d,target); return target
    src=Path(source).expanduser().resolve()
    if not (src/'SKILL.md').exists(): raise ValueError('skill must contain SKILL.md')
    target=SKILLS/_name(src.name); shutil.rmtree(target,ignore_errors=True); shutil.copytree(src,target); return target
def remove(name): shutil.rmtree(SKILLS/_name(name))

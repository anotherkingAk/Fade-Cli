from __future__ import annotations
from pathlib import Path
import hashlib

def inventory(root: Path, limit=160):
    out=[]
    ignored={".git","node_modules",".venv","venv","dist","build",".fade"}
    for p in root.rglob("*"):
        if len(out)>=limit: break
        if p.is_dir() or any(x in ignored for x in p.parts): continue
        try:
            size=p.stat().st_size
            if size>200_000: continue
            out.append({"path":str(p.relative_to(root)),"bytes":size})
        except OSError: pass
    return out

def read_context(root: Path, max_chars=50000):
    parts=[]; total=0
    for item in inventory(root):
        p=root/item["path"]
        try:
            s=p.read_text(errors="ignore")
        except Exception: continue
        if len(s)>12000: s=s[:12000]+"\n…truncated"
        if total+len(s)>max_chars: break
        parts.append(f"\n### {item['path']}\n{s}"); total+=len(s)
    return "".join(parts)

def safe_write(root: Path, rel: str, content: str):
    p=(root/rel).resolve(); rr=root.resolve()
    if rr not in p.parents and p!=rr: raise ValueError(f"unsafe generated path: {rel}")
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")
    return p

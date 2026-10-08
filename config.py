from __future__ import annotations
import json, os
from pathlib import Path

HOME = Path(os.getenv("FADE_HOME", Path.home() / ".fade"))
CONFIG = HOME / "config.json"
SKILLS = HOME / "skills"
LOGS = HOME / "logs"
WORKSPACES = HOME / "workspaces"

def ensure():
    for p in (HOME, SKILLS, LOGS, WORKSPACES): p.mkdir(parents=True, exist_ok=True)

def load():
    ensure()
    if not CONFIG.exists(): return {"provider":"openai","model":"","api_key":""}
    try: return json.loads(CONFIG.read_text())
    except Exception: return {"provider":"openai","model":"","api_key":""}

def resolve():
    c=load(); c["provider"]=os.getenv("FADE_PROVIDER",c.get("provider","openai")); c["model"]=os.getenv("FADE_MODEL",c.get("model","")); c["api_key"]=os.getenv("FADE_API_KEY",c.get("api_key","")); return c

def save(c):
    ensure(); CONFIG.write_text(json.dumps(c,indent=2));
    try: CONFIG.chmod(0o600)
    except OSError: pass

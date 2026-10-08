import json, urllib.request, urllib.error

def post(url, headers, payload, timeout=180):
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json",**headers},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"provider HTTP {e.code}: {e.read().decode(errors='replace')[:1200]}")
    except urllib.error.URLError as e: raise RuntimeError(f"provider connection failed: {e}")

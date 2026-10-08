from .base import Provider
from .http import post
class OpenAIProvider(Provider):
    def __init__(self,key,model,base="https://api.openai.com/v1"): self.key,self.model,self.base=key,model,base.rstrip('/')
    def ask(self,system,user):
        if not self.key or not self.model: raise RuntimeError("OpenAI provider requires FADE_API_KEY and FADE_MODEL")
        d=post(self.base+"/chat/completions",{"Authorization":f"Bearer {self.key}"},{"model":self.model,"messages":[{"role":"system","content":system},{"role":"user","content":user}],"temperature":0.12})
        return d["choices"][0]["message"]["content"]

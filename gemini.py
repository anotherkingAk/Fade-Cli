from .base import Provider
from .http import post
class GeminiProvider(Provider):
    def __init__(self,key,model): self.key,self.model=key,model
    def ask(self,system,user):
        if not self.key or not self.model: raise RuntimeError("Gemini provider requires FADE_API_KEY and FADE_MODEL")
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.key}"
        d=post(url,{}, {"systemInstruction":{"parts":[{"text":system}]},"contents":[{"role":"user","parts":[{"text":user}]}],"generationConfig":{"temperature":0.12}})
        return d["candidates"][0]["content"]["parts"][0]["text"]

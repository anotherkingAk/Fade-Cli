from .terminal import *
class UI:
    def __init__(self): pass
    def phase(self,name,detail=''): status(name,detail)
    def think(self,label='Thinking'): think(label)

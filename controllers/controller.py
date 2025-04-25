
'''
Base class for pawn controllers
'''
from entities.entity import Entity
class Controller(Entity):

    _pawn = None

    def __init__(self,pawn=None):
        super().__init__()
        self.pawn = pawn

    @property
    def pawn(self):
        return self._pawn
    @pawn.setter
    def pawn(self,value):
        self._pawn = value

    def update(self,dt,parent=None):
        super().update(dt)
        
    def draw(self,viewport,parent=None):
        pass

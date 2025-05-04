import entities.entity as ent
from entities.viewport import Viewport
import mathquest.matrix as mqm
import mathquest.quaternion as mqq
from graphics.render_engine import RenderEngine

class World(ent.Entity):

    def __init__(self):
        super().__init__()

    def update(self,dt):
        super().update(dt)

    def draw(self,viewport):
        super().draw(viewport)
        RenderEngine.draw_scene()

    def spawn_entity(self,entity):
        self.add_child(entity)
    
    def despawn_entity(self,entity):
        self.remove_child(entity)
    


    @property
    def ents(self):
        return self._child_entities
    @ents.setter
    def ents(self,value):
        self._child_entities = value
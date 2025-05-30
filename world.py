import entities.entity as ent
from graphics.render_engine import RenderEngine
from collision.collision import CollisionManager

class World(ent.Entity):

    def __init__(self):
        super().__init__()
        self.collision_manager = CollisionManager()

    def update(self,dt):
        super().update(dt)


    def draw(self,viewport):
        super().draw(viewport)

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
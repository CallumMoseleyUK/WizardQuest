from graphics.mesh import Mesh
import numpy as np
from collision.bounding_geometry import *
from mathquest.quaternion import Quat

class CollisionManager:
    def __init__(self):
        pass

    def apply_collisions(self,models):
        model_list = models.copy()
        for i,model in enumerate(model_list):
            if model is not None: model.calculate_collisions(model_list)
            #model_list[i] = None

class CollisionModel:
    ''' A collection of primitives and methods for checking collision with other models. '''
    def __init__(self):
        super().__init__(self)
        self.primitives = []
        self._bounding_geometry = None
        self.set_impulse_event(lambda : None)

    def set_impulse_event(self,hook):
        self._impulse_event = hook

    def add_primitive(self,primitive,bUpdate=False):
        self.primitives.append(primitive)
        if bUpdate:
            self.update_bounding_geometry()
    
    def remove_primitive(self,primitive,bUpdate=False):
        self.primitives.remove(primitive)
        if bUpdate:
            self.update_bounding_geometry()

    def update(self,world_position,world_quaternion):
        self.world_position, self.world_quaternion = world_position, world_quaternion


    def update_bounding_geometry(self):
        ''' Fit a bounding geometry around that of all collision primitives
        TODO: consider refitting this as the parent entity rotates. Only applicable for boxes, not spheres. '''
        self._bounding_geometry = self.collision_primitives[0]._bounding_geometry
        for primitive in self.collision_primitives[1:]:
            self._bounding_geometry = self._bounding_geometry.union(primitive._bounding_geometry)

    def bounding_collision(self,other):
        ''' Check if the bounding geometries of two collision models intersect. '''
        displacement = self.world_position - other.world_position
        return self._bounding_geometry.check_intersects(other._bounding_geometry,displacement=displacement)
    
    def cull_model_collisions(self,others):
        ''' Remove models from a list if their bounding geometry does not intersect with self. '''
        return [other for other in others if other and self.bounding_collision(other)]

    def calculate_collisions(self,others):
        ''' Cull other models by checking bounding geometries, then calculate the outcome of the collision. '''
        for other in self.cull_model_collisions(others):
            self.calculate_model_collision(other)

    def calculate_model_impulse(self,other):
        ''' Calculate the outcome of collision with each primitive in another collision model. '''
        impulse = np.zeros(3)
        displacement = self.world_position - other.world_position
        for a in self.primitives:
            for b in other.primitives:
                impulse,impulse_displacement = a.collision_impulse(b,displacement)
                self.impulse_event(impulse,impulse_displacement)


    
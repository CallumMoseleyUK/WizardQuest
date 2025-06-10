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
            model_list[i] = None

class CollisionModel:
    ''' A collection of primitives '''
    def __init__(self):
        super().__init__(self)
        self.primitives = []
        self._bounding_geometry = None

    def add_primitive(self,primitive,bUpdate=False):
        self.primitives.append(primitive)
        if bUpdate:
            self.update_bounding_geometry()
    
    def remove_primitive(self,primitive,bUpdate=False):
        self.primitives.remove(primitive)
        if bUpdate:
            self.update_bounding_geometry()

    def update(self,world_position,world_quaternion):
        pass


    def update_bounding_box(self):
        self._bounding_geometry = self.collision_primitives[0]._bounding_geometry
        for primitive in self.collision_primitives[1:]:
            self._bounding_geometry = self._bounding_geometry.union(primitive._bounding_geometry)

    def bounding_collision(self,other):
        return self._bounding_geometry.check_intersects(other._bounding_geometry)
    
    def cull_model_collisions(self,others):
        return [other for other in others if other and self.bounding_collision(other)]

    def calculate_model_collision(self,other):
        pass

    def calculate_collisions(self,others):
        for other in self.cull_model_collisions(others):
            self.calculate_model_collision(other)


    
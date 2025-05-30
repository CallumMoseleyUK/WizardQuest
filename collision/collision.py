from graphics.mesh import Mesh
import numpy as np
from collision.bounding_geometry import *

class CollisionManager:
    def __init__(self):
        pass

    def apply_collisions(self,models):
        model_list = models.copy()
        for i,a in enumerate(model_list):
            for b in model_list:
                if not a or not b or a==b or a.cull_collision(b):
                    continue
                a.calculate_collision(b)
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

    def update_bounding_box(self):
        self._bounding_geometry = self.collision_primitives[0]._bounding_geometry
        for primitive in self.collision_primitives[1:]:
            self._bounding_geometry = self._bounding_geometry.union(primitive._bounding_geometry)

    def cull_collision(self,other):
        return not self._bounding_geometry.check_intersects(other._bounding_geometry)
    
    def calculate_collision(self,other):
        for a in self.primitives:
            for b in other.primitives:
                a.calculate_collision(b)
        




    
from graphics.mesh import Mesh
import numpy as np
from collision.bounding_geometry import *

class CollisionManager:
    def __init__(self):
        pass

    def apply_collisions(self,dt,ent_list):
        for ent1 in ent_list:
            for ent2 in ent_list:
                if ent1==ent2 or not ent1.collision_model.check_collision(ent2.collision_model):
                    continue
                displacement = ent1.position - ent2.position
                distance_squared = np.dot(displacement, displacement)
                

                
            

class CollisionModel:
    ''' A collection of primitives '''
    def __init__(self):
        super().__init__(self)
        self.collision_primitives = []
        self._bounding_geometry = BoundingBox(np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]))

    def add_primitive(self,primitive,bUpdate=False):
        self.collision_primitives.append(primitive)
        if bUpdate:
            self.update_bounding_geometry()
    
    def remove_primitive(self,primitive,bUpdate=False):
        self.collision_primitives.remove(primitive)
        if bUpdate:
            self.update_bounding_geometry()

    def update_bounding_box(self):
        for primitive in self.collision_primitives:
            self._bounding_geometry = self._bounding_geometry.union(primitive._bounding_geometry)
        




    
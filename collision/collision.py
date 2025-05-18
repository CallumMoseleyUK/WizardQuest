from meshes.mesh import Mesh
import numpy as np
from collision.bounding_geometry import *

class CollisionManager:
    def __init__(self):
        pass

    def apply_collisions(self,dt,ent_list):
        for ent1 in ent_list:
            for ent2 in ent_list:
                if ent1==ent2 or not ent1.check_collision(ent2):
                    continue
                displacement = ent1.position - ent2.position
                distance_squared = np.dot(displacement, displacement)
                

                
            

class CollisionModel:
    ''' A collection of primitives, i.e. meshes, spheres etc.
    TODO: assumes mostly symmetric objects, as bounding box does not rotate with the object.'''

    def __init__(self):
        super().__init__(self)
        self.collision_primitives = []
        self._bounding_box = BoundingBox(np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]))

    def add_primitive(self,primitive):
        self.collision_primitives.append(primitive)
        self.update_bounding_box()
    
    def remove_primitive(self,primitive):
        self.collision_primitives.remove(primitive)
        self.update_bounding_box()

    def update_bounding_box(self):
        upper = np.array([0.0,0.0,0.0])
        lower = np.array([0.0,0.0,0.0])
        for primitive in self.collision_primitives:
            self._bounding_box = self._bounding_box.union(primitive._bounding_box)
        self._bounding_box = BoundingBox(lower,upper)

class CollisionPrimitive:
    def __init__(self):
        self._bounding_box = BoundingBox(np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]))

    def check_collision(self,primitive):
        return 

class CollisionPrimitiveSphere:
    '''
    In this primitive, if boundingsphere check is passed, move straight to collision response, skipping boundingbox checks.
    '''
    def __init__(self, radius=1.0):
        self.radius = radius





    
from models.mesh import Mesh
import numpy as np

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
    ''' A collection of primitives, i.e. meshes, spheres etc. '''
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
            
class BoundingBox:
    def __init__(self,lower,upper,offset=np.array([0.0,0.0,0.0])):
        self._lower = lower
        self._upper = upper
        self.offset = offset

    @property
    def lower(self):
        return self._lower + self.offset
    @property
    def upper(self):
        return self._upper + self.offset
    
    
    # def check_intersects(self,point):
    #     upper_diff = self.upper+self.offset - point
    #     lower_diff = self.lower+self.offset - point
    #     return np.all(upper_diff>=0.0) and np.all(lower_diff<=0.0)
    def check_encloses(self,box):
        upper_diff = self.upper - box.upper
        lower_diff = self.lower - box.lower
        return np.all(upper_diff>=0.0) and np.all(lower_diff<=0.0)
    
    def check_intersects(self,box):
        upper_diff = self.lower - box.upper
        lower_diff = self.upper - box.lower
        print('upper_diff: ', upper_diff)
        print('lower_diff: ', lower_diff)
        return not (np.any(upper_diff>=0.0) or np.any(lower_diff<=0.0))

    def union(self,box):
        upper1,lower1 = self.upper+self.offset, self.lower+self.offset
        upper2,lower2 = box.upper+box.offset, box.lower+self.offset
        
        upper1[0] = np.max([upper1[0],upper2[0]])
        upper1[1] = np.max([upper1[1],upper2[1]])
        upper1[2] = np.max([upper1[2],upper2[2]])
        lower1[0] = np.min([lower1[0],lower2[0]])
        lower1[1] = np.min([lower1[1],lower2[1]])
        lower1[2] = np.min([lower1[2],lower2[2]])

        offset = (upper1+lower1)/2
        upper1 = upper1 - offset
        upper2 = upper2 - offset
        return BoundingBox(lower1,upper1,offset=offset)


class CollisionPrimitive:
    def __init__(self):
        self._bounding_box = BoundingBox(np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]))

    def check_collision(self,primitive):
        return 

class CollisionPrimitiveSphere:
    def __init__(self, radius=1.0):
        self.radius = radius





    
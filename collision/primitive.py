import numpy as np
from bounding_geometry import BoundingSphere

class Primitive:
    def __init__(self):
        self._bounding_geometry = None
    def cull_collision(self,other):
        return self._bounding_geometry.check_intersects(other)
    def calculate_collision(self,other):
        return None

class PrimitiveSphere(Primitive):
    def __init__(self, radius=1.0,offset=np.zeros(3)):
        self.radius = radius
        self.offset = offset
        self._bounding_geometry = BoundingSphere(radius=radius,offset=offset)
    
    def calculate_collision(self,other):
        if self.cull_collision(other):
            return None
        distance_squared = np.dot(self.offset,other.offset)
        # how to get the actual spatial position?
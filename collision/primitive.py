import numpy as np
from bounding_geometry import BoundingSphere

class Primitive:
    def __init__(self):
        self._bounding_geometry = None
    def cull_collision(self,other):
        return self._bounding_geometry.check_intersects(other)
    def collision_impulse(self,other):
        return None

class PrimitiveSphere(Primitive):
    _impulse_constant = 1.0
    def __init__(self, radius=1.0,offset=np.zeros(3)):
        self.radius = radius
        self.offset = offset
        self._bounding_geometry = BoundingSphere(radius=radius,offset=offset)
    
    def collision_impulse(self,other,model_displacement):
        if self._bounding_geometry.check_intersects(other._bound, displacement=model_displacement):
            prim_displacement = self.offset - other.offset + model_displacement
            return prim_displacement * self._impulse_constant, prim_displacement



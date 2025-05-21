import numpy as np
from bounding_geometry import BoundingSphere

class Primitive:
    def __init__(self):
        pass
    def check_collision(self,other):
        pass

class PrimitiveSphere:
    '''
    In this primitive, if boundingsphere check is passed, move straight to collision response, skipping boundingbox checks.
    '''
    def __init__(self, radius=1.0):
        self.radius = radius


import numpy as np

class BoundingGeometry:
    def check_intersects(self,other):
        print('Override this in subclasses.')
        return False

class BoundingSphere(BoundingGeometry):
    def __init__(self, radius, offset = np.array([0.0,0.0,0.0])):
        self.radius = radius
        self.offset = offset

    def check_intersects(self,other):
        displacement = self.offset - other.offset
        distance_squared = np.dot(displacement,displacement)
        return distance_squared<=(self.radius+other.radius)**2
    
class BoundingBox(BoundingSphere):
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
    
    def check_encloses(self,other):
        upper_diff = self.upper - other.upper
        lower_diff = self.lower - other.lower
        return np.all(upper_diff>=0.0) and np.all(lower_diff<=0.0)
    
    def check_intersects(self,other):
        upper_diff = self.lower - other.upper
        lower_diff = self.upper - other.lower
        return not (np.any(upper_diff>=0.0) or np.any(lower_diff<=0.0))

    def union(self,other):
        upper1,lower1 = self.upper, self.lower
        upper2,lower2 = other.upper, other.lower
        
        upper1[0] = np.max([upper1[0],upper2[0]])
        upper1[1] = np.max([upper1[1],upper2[1]])
        upper1[2] = np.max([upper1[2],upper2[2]])
        lower1[0] = np.min([lower1[0],lower2[0]])
        lower1[1] = np.min([lower1[1],lower2[1]])
        lower1[2] = np.min([lower1[2],lower2[2]])

        offset = (upper1+lower1)/2
        upper1 = upper1 - offset
        lower1 = lower1 - offset
        return BoundingBox(lower1,upper1,offset=offset)

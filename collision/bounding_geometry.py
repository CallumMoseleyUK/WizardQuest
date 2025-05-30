import numpy as np

class BoundingGeometry:

    _SQRT2 = np.sqrt(2.0)
    _INV_SQRT2 = 1.0/_SQRT2
    _SQRT3 = np.sqrt(3.0)
    _INV_SQRT3 = 1.0/_SQRT3

    def __str__(self):
        out = ''
        for key,value in self.__dict__.items():
            out += '%s: %s\n' % (key,str(value))
        return out
    
    def __init__(self):
        self._upper = np.zeros(3)
        self._lower = np.zeros(3)
        self._offset = np.zeros(3)
    
    def check_encloses(self,other):
        upper_diff = self.upper - other.upper
        lower_diff = self.lower - other.lower
        return np.all(upper_diff>=0.0) and np.all(lower_diff<=0.0)
    
    def check_intersects(self,other):
        upper_diff = self.lower - other.upper
        lower_diff = self.upper - other.lower
        return not (np.any(upper_diff>=0.0) or np.any(lower_diff<=0.0))

    def union(self,other):
        upper_new = np.max([self.upper,other.upper],axis=0)
        lower_new = np.min([self.lower,other.lower],axis=0)
        offset_new = 0.5*(upper_new+lower_new)
        new_geometry = type(self)()
        new_geometry.offset = offset_new
        new_geometry.upper = upper_new
        new_geometry.lower = lower_new
        return new_geometry

    @property
    def offset(self):
        return self._offset
    @offset.setter
    def offset(self,value):
        self._offset = np.array(value)

    @property
    def lower(self):
        return self._lower + self._offset
    @property
    def upper(self):
        return self._upper + self._offset
    @lower.setter
    def lower(self,value):
        self._lower = value - self._offset
    @upper.setter
    def upper(self,value):
        self._upper = value - self._offset

class BoundingSphere(BoundingGeometry):
    def __init__(self, radius=0.0, offset = [0.0,0.0,0.0]):
        self.radius = radius
        self.offset = offset

    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self,value):
        self._radius = value
        self._upper = np.zeros(3) + self.radius
        self._lower = np.zeros(3) - self.radius

    def radius_contains_box(self,lower,upper):
        diff = upper-lower
        return np.linalg.norm(diff)*0.5
    
    def radius_inside_box(self,lower,upper):
        diff = upper-lower
        return min(diff)*0.5

    def check_intersects(self,other):
        if not isinstance(other, BoundingSphere):
            return super().check_intersects(other)
        displacement = self.offset - other.offset
        distance_squared = np.dot(displacement,displacement)
        return distance_squared<=(self.radius+other.radius)**2
    
    def union(self,other):
        if not isinstance(other,BoundingSphere):
            return super().union(other)
        offset_diff = other.offset - self.offset
        distance = np.linalg.norm(offset_diff)
        if distance>0:
            direction = offset_diff/distance
            other_lower = other.offset - direction*other.radius
            self_lower = self.offset - direction*self.radius
            other_upper = other.offset + direction*other.radius
            self_upper = self.offset + direction*self.radius
            new_upper = np.max([other_lower,self_lower,other_upper,self_upper],axis=0)
            new_lower = np.min([other_lower,self_lower,other_upper,self_upper],axis=0)
            new_offset = 0.5*(new_upper+new_lower)
            new_radius = 0.5*np.linalg.norm(new_upper-new_lower)
        else:
            new_offset = self.offset
            new_radius = max(self.radius,other.radius)
        return BoundingSphere(radius=new_radius,offset=new_offset)

class BoundingBox(BoundingGeometry):
    def __init__(self,lower=[0.0,0.0,0.0],upper=[0.0,0.0,0.0],offset=[0.0,0.0,0.0]):
        self._lower = lower
        self._upper = upper
        self.offset = offset
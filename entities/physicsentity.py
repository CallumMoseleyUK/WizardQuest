import entities.entity as ent
import numpy as np

class PhysicsEntity(ent.DynamicEntity):
    '''
    Dynamic entities with inertia.
    '''
    _mass_minmax = (1e-3, 1.0e10)
    _inertia_tensor_minmax = (1e-3, 1.0e10)
    
    def __init__(self):
        super().__init__()
        self.mass = 1.0
        self.inertia_tensor = np.array([1.0, 1.0, 1.0])

    def update(self, dt, parent=None):
        super().update(dt, parent=parent)

    def apply_impulse(self,impulse):
        self.velocity += impulse/self.mass
    def apply_angular_impulse(self,angular_impulse):
        self.angular_velocity += angular_impulse/self.inertia_tensor

    @property
    def mass(self):
        return self._mass
    @mass.setter
    def mass(self,value):
        self._mass = min(max(value,PhysicsEntity._mass_minmax[0]),PhysicsEntity._mass_minmax[1])

    @property
    def inertia_tensor(self):
        return self._inertia_tensor
    @mass.setter
    def inertia_tensor(self,value):
        self._inertia_tensor = np.array([min(max(value[0],PhysicsEntity._mass_minmax[0]),PhysicsEntity._mass_minmax[1]),
                                        min(max(value[1],PhysicsEntity._mass_minmax[0]),PhysicsEntity._mass_minmax[1]),
                                        min(max(value[2],PhysicsEntity._mass_minmax[0]),PhysicsEntity._mass_minmax[1])])

    
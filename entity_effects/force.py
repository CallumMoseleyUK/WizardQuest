import numpy as np
from entity_effects.entity_effect import EntEffect
from entities.entity import Entity,DynamicEntity
from entities.physicsentity import PhysicsEntity

class Acceleration(EntEffect):
    
    def __init__(self,acceleration=np.zeros(3),angular_acceleration=np.zeros(3),duration=-1.0):
        super().__init__(duration=duration)
        self.acceleration = acceleration
        self.angular_acceleration = angular_acceleration

    def update(self,dt,entity):
        super().update(dt, entity)
        entity.velocity += self.acceleration*dt
        entity.angular_velocity += self.angular_acceleration*dt

    def is_compatible(self, entity):
        back_compatible = super().is_compatible(entity)
        return back_compatible and isinstance(entity,DynamicEntity)
    
class Force(Acceleration):

    def __init__(self, force=np.zeros(3), torque=np.zeros(3), duration=-1.0):
        super().__init__(acceleration=np.zeros(3),
                         angular_acceleration=np.zeros(3),
                         duration=duration)
        self.force = force
        self.torque = torque

    def update(self,dt, entity):
        if self.is_compatible(entity):
            self.acceleration = self.force/entity.mass
            self.angular_acceleration = self.torque/entity.inertia_tensor
        super().update(dt,entity)

    def is_compatible(self, entity):
        back_compatible = super().is_compatible(entity)
        return back_compatible and isinstance(entity,PhysicsEntity)
    
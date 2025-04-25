import numpy as np
from entity_effects.entity_effect import EntEffect
from entities.entity import Entity,DynamicEntity
from entities.physicsentity import PhysicsEntity

class Acceleration(EntEffect):
    
    def __init__(self,acceleration=np.zeros(3),angular_acceleration=np.zeros(3)):
        super().__init__()
        self.acceleration = acceleration
        self.angular_acceleration = angular_acceleration

    def update(self, entity, dt):
        super().update(entity, dt)
        entity.velocity += self.acceleration*dt
        entity.angular_velocity += self.angular_acceleration*dt

    def is_compatible(self, entity):
        back_compatible = super().is_compatible(entity)
        return back_compatible and isinstance(entity,DynamicEntity)
    
class Force(Acceleration):

    def __init__(self, force=np.zeros(3)):
        super().__init__(acceleration=np.zeros(3),
                         angular_acceleration=np.zeros(3))
        self.force = force

    def update(self,entity, dt):
        if self.is_compatible(entity):
            self.acceleration = self.force/entity.mass
        super().update(entity,dt)

    def added(self,entity):
        super.added(entity)

    def is_compatible(self, entity):
        back_compatible = super().is_compatible(entity)
        return back_compatible and isinstance(entity,PhysicsEntity)
    
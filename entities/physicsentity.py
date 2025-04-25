import entities.entity as ent
import numpy as np

class PhysicsEntity(ent.DynamicEntity):
    '''
    Dynamic entities with physics.
    '''
    def __init__(self):
        super().__init__()
        self.mass = 1.0
        self.inertia_tensor = np.array([1.0,1.0,1.0])

    def update(self, dt, parent=None):
        super().update(dt, parent)

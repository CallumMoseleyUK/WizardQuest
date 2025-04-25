import numpy as np
from entities.entity import Entity
class EntEffect:
    def __init__(self):
        self.timer = 0.0
        self.duration = -1.0

    def update(self,entity,dt):
        if self.duration >= 0.0:
            self.timer += dt
            if self.timer > self.duration:
                entity.remove_effect(self)

    def added(self,entity):
        print('Effect ',type(self), ' added.')
        if not self.is_compatible(entity):
            entity.remove_effect(self)

    def removed(self,entity):
        print('Effect ',type(self), ' removed.')

    def is_compatible(self,entity):
        return isinstance(entity,Entity)
import entities.physicsentity as physEnt

class Pawn(physEnt.PhysicsEntity):
    '''
    Base class for entities with a controller
    '''
    base_speed = 15.0
    def __init__(self):
        super().__init__()

    def move(self,movement_direction):
        self.velocity = movement_direction*self.base_speed
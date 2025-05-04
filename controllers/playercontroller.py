from controllers.controller import Controller
from entities.viewport import Viewport
import numpy as np

class PlayerController(Controller):

    def __init__(self,pawn=None):
        super().__init__(pawn)
    
    def apply_input_direction(self,input_direction,viewport):
        if not self.pawn: return
        world_direction = np.dot(viewport.rotation_matrix(),input_direction)
        #print('world_direction: ', world_direction)
        self.pawn.move(world_direction)


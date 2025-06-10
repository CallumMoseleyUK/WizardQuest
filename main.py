import numpy as np
import entities.physicsentity as phys_ent
from entities.viewport import *
import entity_effects.force as force_effect
from collision.collision import CollisionModel
import os
from game import Game

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def exit_event():
    print('Exit event called')

if __name__ == '__main__':
    print('WizardQuest running')

    ## Settings
    screen_resolution = (800, 480)
    framerate = 60
    field_of_view = 60.0
    znear = 0.01
    zfar = 1000.0

    ## Initialize game
    game = Game(screen_resolution=screen_resolution,
                framerate=framerate,
                field_of_view=field_of_view,
                znear=znear,
                zfar=zfar)
    
    ## Spawn entities
    ent_list = []
    pos = np.array([[6.0,0.0,0.0],
                    [-6.0,0.0,0.0],
                    [0.0,6.0,0.0],
                    [0.0,-6.0,0.0]])

    render_model_name = 'suzanne'

    for i in range(len(pos)):
        e = phys_ent.PhysicsEntity()
        e.add_render_model(game.asset_manager.load_render_model_from_db(render_model_name))
        e.position = pos[i]
        e.angular_velocity[0] = 0.0
        ent_list.append(e)
        game.world.spawn_entity(e)
    first_entity = ent_list[0]
    first_entity.velocity = [
        0.0,
        0.0,
        0.0
        ]
    first_entity.angular_velocity = [
        0.0,
        0.2,
        0.2
        ]
    
    ## Add a force
    #force_duration = -3.0
    #force = force_effect.Force(duration=force_duration)
    #force.force[2] = 0.5
    #first_entity.add_effect(force)

    ## Game loop
    game.run()

    print('WizardQuest quit')
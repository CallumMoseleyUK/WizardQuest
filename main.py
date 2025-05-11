import pygame as pg
import numpy as np
from asset_manager import AssetManager
import entities.entity as ent
import entities.physicsentity as phys_ent
from entities.viewport import *
from entities.pawn import Pawn
from world import World
from display import Display
import math
from userinput import UserInput
from controllers.playercontroller import PlayerController
import entity_effects.force as force_effect

try:
    import OpenGL.GL as GL
    import OpenGL.GLU as GLU
except ImportError:
    print("pyopengl missing. Requires: pyopengl numpy")
    raise SystemExit
import os

from graphics.render_engine import RenderModel,RenderEngine
from models.mesh import Mesh
from graphics.shader import Shader

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def init_key_bindings():
    key_bindings = {}
    key_bindings['exit'] = pg.K_ESCAPE
    key_bindings['move_forward'] = pg.K_w
    key_bindings['move_backward'] = pg.K_s
    key_bindings['move_left'] = pg.K_a
    key_bindings['move_right'] = pg.K_d
    key_bindings['move_up'] = pg.K_SPACE
    key_bindings['move_down'] = pg.K_LCTRL
    key_bindings['rotate_up'] = pg.K_DOWN
    key_bindings['rotate_down'] = pg.K_UP
    key_bindings['rotate_left'] = pg.K_LEFT
    key_bindings['rotate_right'] = pg.K_RIGHT
    return key_bindings

def exit_event():
    print('Exit event called')

if __name__ == '__main__':
    print('BoredomQuest running')

    ## Settings
    screen_resolution = (800, 480)
    framerate = 60
    field_of_view = 60.0
    znear = 0.1
    zfar = 50.0

    ## Initialise input
    user_input = UserInput()
    user_input.set_exit_function(exit_event)

    ## Initialise display
    display = Display(screen_resolution=screen_resolution,
                      framerate=framerate,
                      field_of_view=field_of_view,
                      znear=znear,
                      zfar=zfar)
    display.init_render_engine()
    
    ## Initialise asset management
    asset_manager = AssetManager(display)

    ## Initialise world
    world = World()
    viewport = Viewport()

    ## Initialise player
    player_pawn = Pawn()
    player_pawn.add_child(viewport)
    player_controller = PlayerController(player_pawn)
    player_pawn.position[0] = 0.0
    world.spawn_entity(player_controller)
    world.spawn_entity(player_pawn)

    ## Spawn entities
    ent_list = []
    pos = np.array([[0.0,0.0,6.0],
                    [-6.0,0.0,0.0],
                    [0.0,6.0,0.0],
                    [0.0,-6.0,0.0]])
    #pos = np.array([[6.0,0.0,0.0]])

    #dummy_model = RenderModel(Mesh(),Shader())
    #dummy_model.update((5.0,0,0),viewport.rotation_matrix())
    #RenderEngine.add_model(dummy_model)

    for i in range(len(pos)):
        e = phys_ent.PhysicsEntity()
        e.add_render_model(asset_manager.load_render_model(None,None))
        e.position = pos[i]
        e.angular_velocity[0] = 0.0
        ent_list.append(e)
        world.spawn_entity(e)
    first_entity = ent_list[0]
    first_entity.velocity = [
        0.0,
        0.2,
        0.0
        ]
    first_entity.angular_velocity = [
        0.0,
        0.0,
        0.2
        ]
    
    ## Add a force
    force_duration = -3.0
    force = force_effect.Force(duration=force_duration)
    #force.force[2] = 0.5
    first_entity.add_effect(force)

    ## Game loop
    running = True
    dt = 0.0 #time per frame in seconds
    while running:
        running = user_input.update(dt)
        viewport.set_rotation(user_input.view_rotation[0],
                              user_input.view_rotation[1],
                              user_input.view_rotation[2], bDegrees=True)
        player_controller.apply_input_direction(user_input.input_direction,viewport)

        P,I,D = 5.0, 1.0, 1.0
        force.force = P*(viewport.x_axis()*8.0 +player_pawn.position - first_entity.position) + D*(-first_entity.velocity)

        world.update(dt)
        display.set_view(viewport.position, viewport.x_axis(), (0,0,1))
        world.draw(viewport)
        dt = display.update()
        
        print('ent p: ',first_entity.position)

    pg.quit()

    print('BoredomQuest quit')
import pygame as pg
import numpy as np
from asset_manager import AssetManager
import entities.entity as ent
from entities.viewport import *
from entities.pawn import Pawn
from models.model import RenderObject
from world import World
from display import Display
import math
from userinput import UserInput
from controllers.playercontroller import PlayerController
try:
    import OpenGL.GL as GL
    import OpenGL.GLU as GLU
except ImportError:
    print("pyopengl missing. Requires: pyopengl numpy")
    raise SystemExit

import os

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



# def handle_event_queue(viewport):
#     # poll for events
#     # pg.QUIT event means the user clicked X to close your window
#     bRunning = True
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             bRunning = False
#     # Input
#     keys = pg.key.get_pressed()
    
#     rspeed = 0.05
#     speed = 0.2
#     if keys[key_bindings['move_forward']]:
#         viewport.position += speed*viewport.x_axis()
#     if keys[key_bindings['move_backward']]:
#         viewport.position -= speed*viewport.x_axis()
#     if keys[key_bindings['move_left']]:
#         viewport.position += speed*viewport.y_axis()
#     if keys[key_bindings['move_right']]:
#         viewport.position -= speed*viewport.y_axis()
#     if keys[key_bindings['move_up']]:
#         viewport.position[2] += speed
#     if keys[key_bindings['move_down']]:
#         viewport.position[2] -= speed
#     if keys[key_bindings['rotate_up']]:
#         viewport.rotate([0.0,-rspeed,0.0])
#     if keys[key_bindings['rotate_down']]:
#         viewport.rotate([0.0,rspeed,0.0])
#     if keys[key_bindings['rotate_left']]:
#         viewport.rotate([0.0,0.0,rspeed])
#     if keys[key_bindings['rotate_right']]:
#         viewport.rotate([0.0,0.0,-rspeed])
#     if keys[key_bindings['exit']]:
#         bRunning = False

#     return bRunning

def exit_event():
    print('Exit event called')

if __name__ == '__main__':
    print('BoredomQuest running')

    ## Settings
    screen_resolution = (800, 600)
    framerate = 60
    field_of_view = 60.0

    ## Initialise input
    user_input = UserInput()
    user_input.set_exit_function(exit_event)

    ## Initialise display
    display = Display(screen_resolution=screen_resolution,
                      framerate=framerate,
                      field_of_view=field_of_view)
    
    ## Initialise asset management
    asset_manager = AssetManager(display)

    ## Initialise world
    world = World()
    viewport = Viewport()
    viewport.position[0] = -6.0

    ## Initialise player
    player_pawn = Pawn()
    player_pawn.add_child(viewport)
    player_controller = PlayerController(player_pawn)
    player_pawn.position[0] = -6.0
    world.spawn_entity(player_controller)
    world.spawn_entity(player_pawn)

    ## Add an entity
    first_entity = ent.DynamicEntity()
    first_entity.render_object = asset_manager.load_render_object(None,None)
    first_entity.velocity = [
        0.0,
        0.0,
        0.0
        ]
    first_entity.angular_velocity = [
        0.2,
        0.2,
        0.2
        ]
    first_entity.position = [
        0.0,
        0.0,
        0.0
        ]
    
    world.spawn_entity(first_entity)

    ## Game loop
    running = True
    dt = 0.0 #time per frame in seconds
    while running:
        running = user_input.update(dt)
        viewport.set_rotation(user_input.view_rotation[0],
                              user_input.view_rotation[1],
                              user_input.view_rotation[2], bDegrees=True)
        player_controller.apply_input_direction(user_input.input_direction,viewport)

        world.update(dt)
        dt = display.update()
        world.draw(viewport)
        #print('View [roll,pitch,yaw]: ', user_input.view_rotation)
        #print('Input direction: ',user_input.input_direction)
        #print('first_entity pos: ',first_entity.position)

    pg.quit()

    print('BoredomQuest quit')
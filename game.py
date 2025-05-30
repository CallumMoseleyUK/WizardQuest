import pygame as pg
import numpy as np
from asset_manager import AssetManager
from entities.viewport import *
from entities.pawn import Pawn
from world import World
from display import Display
from userinput import UserInput
from controllers.playercontroller import PlayerController
from graphics.render_engine import RenderEngine

class Game:
    def exit_event(self):
        pass
    def __init__(self,screen_resolution=(800,480),framerate=60,field_of_view=60.0,znear=0.1,zfar=50.0):
        ## Initialise input
        self.user_input = UserInput()
        self.user_input.set_exit_function(self.exit_event)

        ## Initialise display
        self.display = Display(screen_resolution=screen_resolution,
                        framerate=framerate,
                        field_of_view=field_of_view,
                        znear=znear,
                        zfar=zfar)
        self.display.init_render_engine()

        ## Initialise asset management
        self.asset_manager = AssetManager()

        ## Initialise world
        self.world = World()
        self.viewport = Viewport()

        ## Initialise player
        self.player_pawn = Pawn()
        self.player_pawn.add_child(self.viewport)
        self.player_controller = PlayerController(self.player_pawn)
        self.player_pawn.position[0] = 0.0
        self.world.spawn_entity(self.player_controller)
        self.world.spawn_entity(self.player_pawn)

    def run(self):
        running = True
        dt = 0.0 #time per frame in seconds
        while running:
            running = self.user_input.update(dt)
            self.viewport.set_rotation(self.user_input.view_rotation[0],
                                self.user_input.view_rotation[1],
                                self.user_input.view_rotation[2], bDegrees=True)
            self.player_controller.apply_input_direction(self.user_input.input_direction,self.viewport)

            #P,I,D = 3.0, 1.0, 1.0
            #force.force = P*(viewport.x_axis()*8.0 +player_pawn.position - first_entity.position) + D*(-first_entity.velocity)

            self.world.update(dt)
            self.display.set_view(self.viewport.position, self.viewport.x_axis(), (0,0,1))
            self.world.draw(self.viewport)
            RenderEngine.draw_scene()
            dt = self.display.update()

        pg.quit()

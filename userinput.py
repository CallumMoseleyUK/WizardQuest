import numpy as np
import pygame as pg

class UserInput:

    def __init__(self):
        self.view_minmax = (-80.0,80.0)
        self.view_sensitivity = np.array([60.0, 60.0, 60.0])
        self.view_rotation = np.array([0.0, 0.0, 0.0])
        self.input_direction = np.array([0.0, 0.0, 0.0])
        self._exit_function = lambda : print('User input exit function not set') 

        self.key_bindings = self.init_key_bindings()

    def set_exit_function(self,exit_function):
        self._exit_function = exit_function

    def init_key_bindings(self):
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
    
    def update(self,dt):
        bRunning = self.handle_event_queue(dt,self.key_bindings)
        if not bRunning:
            self._exit_function()
        return bRunning
    
    def handle_event_queue(self,dt,key_bindings):
        # poll for events
        # pg.QUIT event means the user clicked X to close your window
        bRunning = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                bRunning = False
        # Input
        keys = pg.key.get_pressed()

        if keys[key_bindings['rotate_up']]:
            self.view_rotation[1] -= self.view_sensitivity[1]*dt
        if keys[key_bindings['rotate_down']]:
            self.view_rotation[1] += self.view_sensitivity[1]*dt
        if keys[key_bindings['rotate_left']]:
            self.view_rotation[2] += self.view_sensitivity[2]*dt
        if keys[key_bindings['rotate_right']]:
            self.view_rotation[2] -= self.view_sensitivity[2]*dt
        self.view_rotation[0] = min(max(self.view_rotation[0],self.view_minmax[0]),self.view_minmax[1])
        self.view_rotation[1] = min(max(self.view_rotation[1],self.view_minmax[0]),self.view_minmax[1])
        self.view_rotation[2] = self.view_rotation[2]%360.0

        self.input_direction = np.array([0.0, 0.0, 0.0])
        if keys[key_bindings['move_forward']]:
            self.input_direction[0] += 1.0
        if keys[key_bindings['move_backward']]:
            self.input_direction[0] -= 1.0
        if keys[key_bindings['move_left']]:
            self.input_direction[1] += 1.0
        if keys[key_bindings['move_right']]:
            self.input_direction[1] -= 1.0
        if keys[key_bindings['move_up']]:
            self.input_direction[2] += 1.0
        if keys[key_bindings['move_down']]:
            self.input_direction[2] -= 1.0
        if np.vecdot(self.input_direction,self.input_direction) > 0:
            self.input_direction = self.input_direction/np.linalg.norm(self.input_direction)
        
        if keys[key_bindings['exit']]:
            bRunning = False

        return bRunning
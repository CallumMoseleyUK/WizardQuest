import numpy as np
import mathquest.matrix as mqm
import pygame as pg
try:
    import OpenGL.GL as GL
except ImportError:
    print("pyopengl missing. The GLCUBE example requires: pyopengl numpy")
    raise SystemExit

class Display:

    _screen = None
    _clock = None
    _bFullscreen = False

    def __init__(self,screen_resolution=(800,600),
                 framerate=60.0,
                 field_of_view=75.0,
                 znear=2.0,
                 zfar=100.0,
                 caption='BoredomQuest',
                 icon_path='data/window_icon.png'):
    
        self.screen_resolution = screen_resolution
        self.framerate = framerate
        self.field_of_view = field_of_view
        self.znear = znear
        self.zfar = zfar
        self.dt = round(1000.0/framerate)

        ## Initialise pg
        pg.init()
        pg.display.set_caption(caption)
        pg.display.set_icon(pg.image.load(icon_path))

        gl_version = (3, 1)  # GL Version number (Major, Minor)

        # By setting these attributes we can choose which Open GL Profile
        # to use, profiles greater than 3.2 use a different rendering path
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        #pg.mouse.set_visible(False)
        self._screen = pg.display.set_mode(self.screen_resolution, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self._clock = pg.time.Clock()

    def set_fullscreen(self,bFullscreen=True):
        if bFullscreen==self._bFullscreen: return
        if bFullscreen:
            pg.display.set_mode(self.screen_resolution, pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        else:
            pg.display.set_mode(self.screen_resolution, pg.OPENGL | pg.DOUBLEBUF)
        self._bFullscreen = bFullscreen

    def update(self):
        pg.display.flip()
        pg.time.wait(self.dt)
        return self.dt/1000.0

    @property
    def screen_resolution(self):
        return self._screen_resolution
    @screen_resolution.setter
    def screen_resolution(self,value):
        self._screen_resolution = value
    @property
    def framerate(self):
        return self._framerate
    @framerate.setter
    def framerate(self,value):
        self._framerate = value
    @property
    def field_of_view(self):
        return self._field_of_view
    @field_of_view.setter
    def field_of_view(self,value):
        self._field_of_view = value
    @property
    def znear(self):
        return self._znear
    @znear.setter
    def znear(self,value):
        self._znear = value
    @property
    def zfar(self):
        return self._zfar
    @zfar.setter
    def zfar(self,value):
        self._zfar = value
    


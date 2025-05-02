from models.mesh import Mesh
from graphics.shader import Shader
from OpenGL.GL import *
#import OpenGL.GLU as glu
import glm
class RenderEngine:

    def __init__(self):
        self.models = []

    def init_context(self):
        self.models = []

    def init_opengl(self):
        glClearColor(0.0,0,0.4,0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def add_model(self,model):
        self.models.append(model.make_context())
    
class RenderModel:

    def __init__(self,mesh,shader):
        self.mesh = mesh
        self.shader = shader

    def make_context(self):
        self.load_shader()
        self.load_object()
        self.load_texture()
        return self
        
    def load_shader(self):
        pass

    def load_object(self):
        pass

    def load_texture(self):
        pass

    def draw(self, MVP,View,Projection):
        pass#glPushMatrix()
        

from models.model import Mesh
from OpenGL.GL import *

class RenderEngine:

    def __init__(self):
        self.models = []

    def init_opengl(self):
		glClearColor(0.0,0,0.4,0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)

    def add_model(self,model)
        self.models.append(model)
    
class RenderModel:

    def __init__(self):
        self.mesh = Mesh()

    def make_context(self):
        self.load_shader()
        self.load_object()
        self.load_texture()
        return self
        
    def load_shader(self):
        self.shader = Shader()
        self.shader.initShaderFromGLSL(
            ["glsl/tu01/vertex.glsl"], ["glsl/tu01/fragment.glsl"])
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")

    def load_object(self):
        self.vertexbuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertex_data)*4, 
            (GLfloat * len(self.vertex_data))(*self.vertex_data), GL_STATIC_DRAW)

        self.vertexLen = len(self.vertex_data)

        self.colorbuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorbuffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.color_data)*4, (GLfloat *
                                                               len(self.color_data))(*self.color_data), GL_STATIC_DRAW)
    def load_texture(self):
        self.texture = None
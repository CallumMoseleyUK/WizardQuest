import numpy as np
import mathquest.matrix as mqm
from mathquest.quaternion import Quat
import glm
import pygame as pg
from graphics.render_engine import RenderEngine,RenderModel
from models.mesh import Mesh
from graphics.shader import Shader

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print("pyopengl missing. The GLCUBE example requires: pyopengl numpy")
    raise SystemExit

class SimpleRender:

    def __init__(self):
        self.mesh=Mesh()
        self.shader=Shader()
        self.load_shader()
        self.load_object()
        self.load_texture()

        self.position = np.array([0,0,0])

    def update(self):
        pass

    def load_shader(self):
        self.shader.initShaderFromGLSL(["data/example/cube/vertex.glsl"], ["data/example/cube/fragment.glsl"])
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")

    def load_object(self):
        self.vertexbuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.mesh.vertex_data)*4, 
            (GLfloat * len(self.mesh.vertex_data))(*self.mesh.vertex_data), GL_STATIC_DRAW)

        self.vertexLen = len(self.mesh.vertex_data)

        self.colorbuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorbuffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.mesh.color_data)*4, (GLfloat *
                                                               len(self.mesh.color_data))(*self.mesh.color_data), GL_STATIC_DRAW)
        
    def load_texture(self):
        self.texture = None

    def draw(self,MVP):
        self.shader.begin()
        glUniformMatrix4fv(self.MVP_ID, 1, GL_FALSE,  glm.value_ptr(MVP)  )

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.colorbuffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        
        glDrawArrays(GL_TRIANGLES, 0, self.vertexLen)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        self.shader.end()




if __name__ == '__main__':


    view_quat = Quat.euler_to_quat(0.0,0.0,0.0,bDegrees=True)
    view_position = np.array([0.0,0.0,0.0])
    object_position = np.array([0.0,0.0,-5.0])
    object_quat = Quat()

    width,height = screen_resolution = (800,480)
    znear = 0.1
    zfar = 50.0
    fov = 45.0


    ### Setup pygame
    pg.init()
    pg.display.set_caption('Simple renderer')

    gl_version = (3, 1)  # GL Version number (Major, Minor)

    # By setting these attributes we can choose which Open GL Profile
    # to use, profiles greater than 3.2 use a different rendering path
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    #pg.mouse.set_visible(False)
    _screen = pg.display.set_mode(screen_resolution, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
    _clock = pg.time.Clock()

    

    ### Init view

    #gluPerspective(fov, (screen_resolution[0]/screen_resolution[1]), znear, zfar)
    #glTranslatef(0.0,0.0, -5)

    glClearColor(0.0,0,0.4,0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Multiply quaternion with current modelview matrix    
    #glMultMatrixf(view_quat.perspective_matrix())

    # Some other transformations
    #glTranslatef(-0.5, -0.5, -0.5)

    # Draw something, i.e. cube

    cubes = [SimpleRender()]
    projection_matrix = glm.perspective(glm.radians(fov), float(width) / float(height), znear, zfar)

    #transformation order: scale, rotate, translate
    for t in range(1000):

        view_position = glm.vec3([0,0,5.0])
        look_position = view_position + glm.vec3(-view_quat.z_axis())
        up_axis = (0,1,0)
        view_matrix = glm.lookAt(view_position,look_position,up_axis)
        model_matrix = glm.translate(glm.vec3(cubes[0].position))
        MVP = projection_matrix * view_matrix * model_matrix
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #cubes[0].position = -5 + np.sin(float(t)/300)*2

        cubes[0].draw(MVP)
        #cubes[1].draw(np.array([0.0,0.0,-5.0]),view_quat,object_position,object_quat)
        pg.display.flip()
        pg.time.wait(10)
    pg.quit()
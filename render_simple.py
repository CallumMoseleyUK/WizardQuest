import numpy as np
import mathquest.matrix as mqm
from mathquest.quaternion import Quat
import glm
import pygame as pg
from graphics.render_engine import RenderEngine,RenderModel
from models.mesh import Mesh
from graphics.shader import Shader
from userinput import UserInput
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

        self.position = np.array([0.0,0.0,0.0])

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

    user_input = UserInput()

    ### Init view

    #gluPerspective(fov, (screen_resolution[0]/screen_resolution[1]), znear, zfar)
    #glTranslatef(0.0,0.0, -5)

    glClearColor(0.0,0,0.4,0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    projection_matrix = glm.perspective(glm.radians(fov), float(width) / float(height), znear, zfar)

    cubes = [SimpleRender(),SimpleRender()]

    #transformation order: scale, rotate, translate
    running = True
    dt = 10
    t = 0.0
    view_position = glm.vec3([-5.0, 0.0, 0.0])
    view_quat = Quat()
    while running:
        running = user_input.update(dt/1000)
        t+=dt/1000
        view_quat = Quat.euler_to_quat(user_input.view_rotation[0],
                                       user_input.view_rotation[1],
                                       user_input.view_rotation[2],
                                       bDegrees=True)
        view_position += glm.vec3(user_input.input_direction)*0.2
        look_position = view_position + glm.vec3(view_quat.x_axis())
        up_axis = (0,0,1)#glm.vec3(view_quat.z_axis())
        
        f = 0.8
        osc = np.sin(f*6.28*t)
        p = [[0.0, 0.0, osc],
             [0.0, 0.0, 0.0]]

        ### --- rendering stuff
        view_matrix = glm.lookAt(view_position,look_position,up_axis)

        i = 0
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for cube in cubes:
            cube.position = np.array(p[i])
            i=(i+1)%len(cubes)
            model_matrix = glm.translate(glm.vec3(cube.position))
            
            MVP = projection_matrix * view_matrix * model_matrix
            cube.draw(MVP)
        # ----- end of rendering stuff

        pg.display.flip()
        pg.time.wait(dt)
    pg.quit()
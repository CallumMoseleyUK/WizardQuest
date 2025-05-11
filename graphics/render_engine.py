from OpenGL.GL import *
import glm

class RenderEngine:

    bInitialized = False
    models = []

    @staticmethod
    def init(field_of_view,screen_resolution,znear,zfar):
        width,height = screen_resolution
        if height<=0:
            print('RenderEngine screen height must be greater than 0.')
            return
        RenderEngine.resize_screen(field_of_view,width,height,znear,zfar)
        RenderEngine.set_view((0,0,0),(1,0,0),up_axis=(0,0,1))
        RenderEngine.init_opengl()
        RenderEngine.models = []
        RenderEngine.bInitialized = True

    @staticmethod
    def resize_screen(field_of_view,width,height,znear,zfar):
        RenderEngine.projection_matrix = glm.perspective(glm.radians(field_of_view),
                                                float(width) / float(height),
                                                znear, zfar)
    @staticmethod
    def init_opengl():
        glClearColor(0.0,0,0.4,0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    @staticmethod
    def add_model(model):
        model.make_context()
        RenderEngine.models.append(model)
    
    @staticmethod
    def remove_model(self,model):
        model.removed()
        RenderEngine.models.remove(model)
    
    @staticmethod
    def set_view(view_position, view_direction, up_axis=(0,0,1)):
        view_position = glm.vec3(view_position)
        view_direction = glm.vec3(view_direction)
        look_position = view_position + view_direction
        RenderEngine.view_matrix = glm.lookAt(view_position,look_position,up_axis)

    @staticmethod
    def draw_scene():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for model in RenderEngine.models:
            model.draw(RenderEngine.view_matrix, RenderEngine.projection_matrix)
    
class RenderModel:

    def __init__(self,mesh,shader):
        self.model_matrix = glm.mat4(1)
        self.mesh = mesh
        self.shader = shader

    def make_context(self):
        self.load_shader()
        self.load_object()
        self.load_texture()
        return self
    
    def removed(self):
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

    def update(self, new_position, new_rotation_matrix, new_scale=(1,1,1)):
        # order should be scale, rotate, translate. So trans_mat*rot_mat*scale_mat.
        rotation_4d = glm.mat4(glm.mat3(new_rotation_matrix))
        translation_4d = glm.translate(glm.mat4(1),glm.vec3(new_position))
        self.model_matrix = translation_4d*rotation_4d

    def get_MVP_matrix(self, view_matrix, projection_matrix):
        return projection_matrix * view_matrix * self.model_matrix
        
    def draw(self, view_matrix, projection_matrix):
        model_view_projection = self.get_MVP_matrix(view_matrix,projection_matrix)
        
        self.shader.begin()
        glUniformMatrix4fv(self.MVP_ID, 1, GL_FALSE,  glm.value_ptr(model_view_projection)  )

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
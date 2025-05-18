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
    
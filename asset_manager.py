from models.mesh import Mesh
from graphics.shader import Shader
from graphics.render_engine import RenderModel

class AssetManager:
    '''
    Used for managing data assets such as models and shaders,
    constructing them according to display settings, etc.
    '''

    def __init__(self,display=None):
        self.display = display

    def load_mesh(self,mesh_path=None):
        if mesh_path==None:
            return Mesh()
        else: pass #load from file here

    def load_shader(self,shader_path=None):
        if shader_path==None:
            # return Shader(screen_resolution=self.display.screen_resolution,
            #                 field_of_view=self.display.field_of_view,
            #                 znear=self.display.znear,
            #                 zfar=self.display.zfar)
            return Shader()
        else: pass #load from file here

    def load_render_model(self,mesh_path=None,shader_path=None):
        mesh = self.load_mesh(mesh_path)
        shader = self.load_shader(shader_path)
        return RenderModel(mesh,shader)
            
    @property
    def display(self):
        return self._display
    @display.setter
    def display(self,value):
        self._display = value
from meshes.mesh import Mesh
from graphics.shader import Shader
from graphics.render_model import RenderModel

class AssetManager:
    '''
    Used for managing data assets.
    '''

    def __init__(self,display=None):
        self.display = display

    def load_mesh(self,mesh_path=None):
        if mesh_path==None:
            return Mesh()
        else:
            return Mesh() # load here

    def load_shader(self,shader_path=None):
        if shader_path==None:
            # return Shader(screen_resolution=self.display.screen_resolution,
            #                 field_of_view=self.display.field_of_view,
            #                 znear=self.display.znear,
            #                 zfar=self.display.zfar)
            return Shader()
        else: pass #load from file here

    def load_render_model(self,mesh_path=None,texture_path=None,shader_path=None):
        return RenderModel(mesh_path, texture_path=texture_path, shader_path=shader_path)
            
    @property
    def display(self):
        return self._display
    @display.setter
    def display(self,value):
        self._display = value
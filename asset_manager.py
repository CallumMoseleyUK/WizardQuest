from models.model import Model,RenderObject
from models.shaders import Shader

class AssetManager:
    '''
    Used for managing data assets such as models and shaders,
    constructing them according to display settings, etc.
    '''

    def __init__(self,display=None):
        self.display = display

    def load_model(self,model_path=None):
        if model_path==None:
            return Model()
        else: pass #load from file here

    def load_shader(self,shader_path=None):
        if shader_path==None:
            return Shader(screen_resolution=self.display.screen_resolution,
                          field_of_view=self.display.field_of_view,
                          znear=self.display.znear,
                          zfar=self.display.zfar)
        else: pass #load from file here

    def load_render_object(self,model_path=None,shader_path=None):
        model = self.load_model(model_path)
        shader = self.load_shader(shader_path)
        return RenderObject(model,shader)
            
    @property
    def display(self):
        return self._display
    @display.setter
    def display(self,value):
        self._display = value
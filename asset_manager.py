from meshes.mesh import Mesh
from graphics.shader import Shader
from graphics.render_model import RenderModel
from graphics.texture import Texture

class AssetManager:
    '''
    Used for managing data assets.
    '''
    def __init__(self,display=None):
        self.display = display
        self.manifest = {}

    def retrieve_from_manifest(self,key):
        key = str(key)
        if self.check_manifest(key): return self.manifest[key,'asset']
        else: return None

    def add_to_manifest(self,key,asset):
        key = str(key)
        if self.check_manifest(key): self.manifest[key,'count'] += 1
        else:
            self.manifest[key,'asset'] = asset
            self.manifest[key,'count'] = 1

    def check_manifest(self,key):
        return (key,'asset') in self.manifest

    def load_asset(self, asset_class:type, key):
        if key==None: return None
        asset = self.retrieve_from_manifest(key)
        if not asset:
            asset = asset_class(key)
            self.add_to_manifest(key,asset)
        return asset

    def load_render_model(self,mesh_path=None,texture_path=None,shader_paths=None):
        mesh = self.load_asset(Mesh,mesh_path)
        texture = self.load_asset(Texture,texture_path)
        shader = self.load_asset(Shader,shader_paths)
        return RenderModel(mesh, texture=texture, shader=shader)
            
    @property
    def display(self):
        return self._display
    @display.setter
    def display(self,value):
        self._display = value
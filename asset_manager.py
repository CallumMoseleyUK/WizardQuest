from graphics.mesh import Mesh
from graphics.shader import Shader
from graphics.render_model import RenderModel
from graphics.texture import Texture
from database import db_handler as db

class AssetManager:
    '''
    Used for managing data assets.
    '''
    def __init__(self):
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
        if key is None: return None
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
    
    def load_render_model_from_db(self,model_name):
        model_data = db.get_model_data(model_name)
        mesh_path = model_data['mesh']
        texture_path = model_data['texture']
        shader_paths = (model_data['vert_shader'], model_data['frag_shader'])
        return self.load_render_model(mesh_path=mesh_path,texture_path=texture_path,shader_paths=shader_paths)
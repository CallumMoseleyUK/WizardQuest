
''' Placerholder for database functions '''

_model_data = {}
_model_data['suzanne'] = {
    'mesh': 'data/meshes/suzanne/suzanne.obj',
    'texture': 'data/meshes/suzanne/suzanne.DDS',
    'vert_shader': 'data/shaders/suzanne_vert.glsl',
    'frag_shader': 'data/shaders/suzanne_frag.glsl',
    'collision_model': None
}
_model_data['terrain'] = {
    'mesh': 'data/meshes/terrain.obj',
    'texture': None,
    'vert_shader': 'data/shaders/terrain_vert.glsl',
    'frag_shader': 'data/shaders/terrain_frag.glsl',
    'collision_model': None
}
_model_data['unit_sphere'] = {
    'mesh': 'data/meshes/unit_sphere.obj',
    'texture': None,
    'vert_shader': 'data/shaders/sphere_vert.glsl',
    'frag_shader': 'data/shaders/sphere_frag.glsl',
    'collision_model': None
}
_model_data['unit_cube'] = {
    'mesh': 'data/meshes/unit_cube.obj',
    'texture': None,
    'vert_shader': 'data/shaders/sphere_vert.glsl',
    'frag_shader': 'data/shaders/sphere_frag.glsl',
    'collision_model': None
}

def get_model_data(model_name):
    return _model_data[model_name]
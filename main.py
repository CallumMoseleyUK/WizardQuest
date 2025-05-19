import numpy as np
import entities.physicsentity as phys_ent
from entities.viewport import *
import entity_effects.force as force_effect
import os
from game import Game

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def exit_event():
    print('Exit event called')

if __name__ == '__main__':
    print('WizardQuest running')

    ## Settings
    screen_resolution = (800, 480)
    framerate = 60
    field_of_view = 60.0
    znear = 0.1
    zfar = 50.0

    ## Initialize game
    game = Game(screen_resolution=screen_resolution,
                framerate=framerate,
                field_of_view=field_of_view,
                znear=znear,
                zfar=zfar)
    
    ## Spawn entities
    ent_list = []
    pos = np.array([[0.0,0.0,6.0],
                    [-6.0,0.0,0.0],
                    [0.0,6.0,0.0],
                    [0.0,-6.0,0.0]])
    #pos = np.array([[6.0,0.0,0.0]])

    #dummy_model = RenderModel(Mesh(),Shader())
    #dummy_model.update((5.0,0,0),viewport.rotation_matrix())
    #RenderEngine.add_model(dummy_model)

    mesh_path = r'data\models\suzanne\suzanne.obj'
    texture_path = r'data\models\suzanne\suzanne.DDS'
    #shader_paths = [ r'data\shaders\suzanne_vert.glsl', r'data\shaders\suzanne_frag.glsl' ]
    shader_paths = [ r'data\shaders\terrain_vert.glsl', r'data\shaders\terrain_frag.glsl' ]
    
    for i in range(len(pos)):
        e = phys_ent.PhysicsEntity()
        e.add_render_model(game.asset_manager.load_render_model(mesh_path,texture_path=texture_path,shader_paths=shader_paths))
        e.position = pos[i]
        e.angular_velocity[0] = 0.0
        ent_list.append(e)
        game.world.spawn_entity(e)
    first_entity = ent_list[0]
    first_entity.velocity = [
        0.0,
        0.0,
        0.0
        ]
    first_entity.angular_velocity = [
        0.0,
        0.2,
        0.2
        ]
    
    ## Add a force
    #force_duration = -3.0
    #force = force_effect.Force(duration=force_duration)
    #force.force[2] = 0.5
    #first_entity.add_effect(force)

    ## Game loop
    game.run()

    print('WizardQuest quit')
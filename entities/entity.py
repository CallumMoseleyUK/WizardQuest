import numpy as np
import mathquest.quaternion as mqq
from graphics.render_engine import RenderEngine
from collision.collision import CollisionModel

class Entity:
    '''
    Base class for entities with position, rotation and render/collision models
    '''

    def __init__(self):
        self._quaternion_correction_counter = 0
        self._quaternion_correction_frame_limit = 100 #number of orientation changes before quaternion normalization

        self._position = np.array([0.0,0.0,0.0])
        self._quaternion = mqq.Quat()

        self._effects = []

        self._child_entities = []
        self._render_model = None

        self._collision_model = None

    def update(self,dt,parent=None):
        for effect in self._effects:
            effect.update(dt,self)
        for child in self._child_entities:
            child.update(dt,parent=self)
        

    def draw(self,viewport,parent=None):
        draw_position = self.position
        draw_quat = self.quaternion
        if self._render_model is not None:
            self._render_model.update(draw_position,draw_quat.rotation_matrix())
        for child in self._child_entities:
            child.draw(viewport,parent=self)

    def add_render_model(self,render_model):
        self._render_model = render_model
        RenderEngine.add_model(render_model)
        
    def remove_render_model(self):
        RenderEngine.remove_model(self._render_model)
        self._render_model = None

    def check_collision(self,other):
        self._collision_model.offset = self.position
        other._collision_model.offset = other.position
        return self._collision_model.check_intersects(other._collision_model)
        

    def add_effect(self,effect):
        self._effects.append(effect)
        effect.added(self)
    def remove_effect(self,effect):
        self._effects.remove(effect)
        effect.removed(self)

    def add_collision_model(self,collision_model):
        self._collision_model = collision_model

    def remove_collision_model(self):
        self._collision_model = None
    
    
    def add_child(self,child):
        self._child_entities.append(child)
        child.parent_added(self)
    def remove_child(self,child):
        self._child_entities.remove(child)
        child.parent_removed(self)

    def parent_added(self,parent):
        pass
    def parent_removed(self,parent):
        pass
    
    def set_rotation(self,roll,pitch,yaw,bDegrees=False):
        self.quaternion = mqq.Quat.euler_to_quat(roll,pitch,yaw,bDegrees=bDegrees)

    def rotate(self,angle_axis):
        self.quaternion = self.quaternion.rotate(angle_axis)
        
    def x_axis(self):
        return self.quaternion.x_axis()
    def y_axis(self):
        return self.quaternion.y_axis()
    def z_axis(self):
        return self.quaternion.z_axis()

    ## Properties 
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self,value):
        value = np.array(value)
        self._position = np.array(value)

    @property
    def quaternion(self):
        return self._quaternion
    @quaternion.setter
    def quaternion(self,value):
        self._quaternion = mqq.Quat(value)
        if self._quaternion_correction_counter < self._quaternion_correction_frame_limit:
            self._quaternion_correction_counter += 1
        else:
            self._quaternion = self._quaternion.normalize()
            self._quaternion_correction_counter = 0
    @property
    def rotation(self):
        '''Format: (roll, pitch, yaw)'''
        return self._quaternion.to_euler()
    @rotation.setter
    def rotation(self,value):
        self._quaternion = mqq.Quat.euler_to_quat(roll=value[0],pitch=value[1],yaw=value[2])

    @property
    def render_model(self):
        return self._render_model
    @render_model.setter
    def render_model(self,value):
        self._render_model = value
    

class DynamicEntity(Entity):
    '''
    Base class for anything that exists and moves
    '''

    def __init__(self):
        super().__init__()
        self._velocity = np.zeros(3)
        self._angular_velocity = np.zeros(3)

    def update(self,dt,parent=None):
        super().update(dt,parent)
        self.position += self.velocity*dt
        self.quaternion = self.quaternion.rotate(self.angular_velocity*dt)

    ## Properties
    @property
    def velocity(self):
        return self._velocity
    @velocity.setter
    def velocity(self,value):
        self._velocity = np.array(value)
    @property
    def angular_velocity(self):
        return self._angular_velocity
    @angular_velocity.setter
    def angular_velocity(self,value):
        self._angular_velocity = np.array(value)
        

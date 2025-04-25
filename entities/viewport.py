import numpy as np
import ctypes
import mathquest.quaternion as mqq
import mathquest.matrix as mqm
from entities.entity import Entity
class Viewport(Entity):

    def __init__(self):
        super().__init__()
        self.view_position_offset = np.array([0.0,0.0,0.0])
        self.view_quat_offset = mqq.Quat()

    def parent_added(self,parent):
        super().parent_added(parent)
        self.view_offset = parent.position - self.position
        #self.view_quat_offset = parent.quaternion

    def update(self,dt,parent=None):
        super().update(dt,parent)
        self.position = parent.position + self.view_position_offset
        #self.quaternion = self.view_quat_offset.rotate_by_quat(parent.quaternion)

    def draw(self,viewport,parent=None):
        pass

    def rotation_matrix(self,bInverse=False):
        return self.quaternion.rotation_matrix(bInverse=bInverse)

    def translation_matrix(self):
        return mqm.translate(np.eye(3),self.position[0],self.position[1],self.position[2])
    
    def perspective_matrix(self):
        rot_matrix = np.eye(4,4)
        rot_matrix[:3,:3] = self.rotation_matrix()
        return mqm.translate(rot_matrix,self.position[0],self.position[1],self.position[2])

    # @property
    # def position(self):
    #     return self._position
    # @position.setter
    # def position(self,value):
    #     self._position = np.array(value)
    # @property
    # def quaternion(self):
    #     return self._quaternion
    # @quaternion.setter
    # def quaternion(self,value):
    #     self._quaternion = value
    # @property
    # def rotation(self):
    #     return self._quaternion.to_euler()
    # @rotation.setter
    # def rotation(self,value):
    #     self._quaternion = mqq.Quat.euler_to_quat(value)




        

import numpy as np
import math

class Quat(np.ndarray):
   
    def __new__(cls, input_array=[1.0,0.0,0.0,0.0]):
            return np.asarray(input_array).view(cls)
    
    def __mul__(self,other):
        [q0,q1,q2,q3] = [self[0],self[1],self[2],self[3]]
        [r0,r1,r2,r3] = [other[0],other[1],other[2],other[3]]
        t0 = r0*q0 - r1*q1 - r2*q2 - r3*q3
        t1 = r0*q1 + r1*q0 - r2*q3 + r3*q2
        t2 = r0*q2 + r1*q3 + r2*q0 - r3*q1
        t3 = r0*q3 - r1*q2 + r2*q1 + r3*q0
        return Quat([t0,t1,t2,t3])
    
    def norm(self):
        return np.linalg.norm(self)
    
    def rotate(self,angle_tensor):
        '''Rotates the quaternion about an axis by an angle equal to its norm'''
        return self.rotate_by_quat(Quat.angle_axis_to_quat(np.array(angle_tensor)))
    
    def rotate_by_quat(self,rotation_quaternion):
        return self*rotation_quaternion
    
    def normalize(self):
        mag = self.norm()
        if mag > 0:
            return self / mag
        else:
            return Quat(0.0, 0.0, 0.0, 0.0)
        
    def invert(self):
        q = Quat([self[0],-self[1],-self[2],-self[3]])
        return q/np.vecdot(q,q)
    
    def x_axis(self):
        ''' Returns the vector axis pointing in the local x direction'''
        q0,q1,q2,q3 = self
        return np.array([1-2*(q2**2+q3**2), 2*(q1*q2-q3*q0), 2*(q1*q3+q2*q0)])
    def y_axis(self):
        ''' Returns the vector axis pointing in the local y direction'''
        q0,q1,q2,q3 = self
        return np.array([2*(q1*q2+q3*q0), 1-2*(q1**2+q3**2), 2*(q2*q3-q1*q0)])
    def z_axis(self):
        ''' Returns the vector axis pointing in the local z direction'''
        q0,q1,q2,q3 = self
        return np.array([2*(q1*q3-q2*q0), 2*(q2*q3+q1*q0), 1-2*(q1**2+q2**2)])
    
    def rotation_matrix(self,bInverse=False):
        if bInverse: q = self.invert()
        else: q = self
        return np.array(
                        [q.x_axis(),
                        q.y_axis(),
                        q.z_axis()]
                        )

    def perspective_matrix(self):
        M = np.eye(4,4)
        M[:3,:3] = self.rotation_matrix()
        return M

    @staticmethod
    def angle_axis_to_quat(angle_tensor):
        '''Converts an angle and axis to a quaternion (vector length is the angle)'''
        angle = np.linalg.norm(angle_tensor)
        if angle<=0.0:
            return Quat([1,0,0,0])
        
        axis = angle_tensor/angle
        [mx,my,mz] = axis
        return Quat([math.cos(angle/2),
                  math.sin(angle/2)*mx,
                  math.sin(angle/2)*my,
                  math.sin(angle/2)*mz])

    def to_euler(quat,bDegrees=False):
        '''Converts a quaternion to Euler angles'''
        [qw,qx,qy,qz] = [quat[0],quat[1],quat[2],quat[3]]
        
        roll = math.atan2( 2*(qw*qx+qy*qz), 1-2*(qx**2 + qy**2) )
        pitch = -math.pi/2 + 2*math.atan2( math.sqrt(1+2*(qw*qy-qx*qz)), math.sqrt(1-2*(qw*qy-qx*qz)) )
        yaw = math.atan2( 2*(qw*qz+qx*qy), 1-2*(qy**2+qz**2))

        if bDegrees:
            roll = roll * 180.0/math.pi
            pitch = pitch * 180.0/math.pi
            yaw = yaw * 180.0/math.pi

        return np.array([roll,pitch,yaw])

    @staticmethod
    def euler_to_quat(roll,pitch,yaw,bDegrees=False):
        '''Converts Euler angles to a quaternion'''
        if bDegrees:
            roll = roll * math.pi/180.0
            pitch = pitch * math.pi/180.0
            yaw = yaw * math.pi/180.0
        
        cosr = math.cos(roll*0.5)
        sinr = math.sin(roll*0.5)
        cosp = math.cos(pitch*0.5)
        sinp = math.sin(pitch*0.5)
        cosy = math.cos(yaw*0.5)
        siny = math.sin(yaw*0.5)
        
        qw = cosr*cosp*cosy + sinr*sinp*siny
        qx = sinr*cosp*cosy - cosr*sinp*siny
        qy = cosr*sinp*cosy + sinr*cosp*siny
        qz = cosr*cosp*siny - sinr*sinp*cosy

        return Quat([qw,qx,qy,qz])
        


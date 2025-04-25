import math
import mathquest.matrix as mqm
import mathquest.quaternion as mqq
import numpy as np
from models.shaders import Shader
from entities.viewport import Viewport

try:
    import OpenGL.GL as GL
except ImportError:
    print("pyopengl missing. The GLCUBE example requires: pyopengl numpy")
    raise SystemExit

class Model:
    '''
    Container for model data
    '''
    # Some simple data for a colored cube here we have the 3D point position
    # and color for each corner. A list of indices describes each face, and a
    # list of indices describes each edge.
    _points = (
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, -0.5),
        (0.5, -0.5, 0.5),
        (0.5, 0.5, 0.5),
        (-0.5, -0.5, 0.5),
        (-0.5, 0.5, 0.5),
    )

    # colors are 0-1 floating values
    _colors = (
        (1, 0, 0),
        (1, 1, 0),
        (0, 1, 0),
        (0, 0, 0),
        (1, 0, 1),
        (1, 1, 1),
        (0, 0, 1),
        (0, 1, 1),
    )

    _quad_verts = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6),
    )

    _edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7),
    )

    def __init__(self):
        pass

    @property
    def points(self):
        return self._points
    @points.setter
    def points(self,value):
        self._points = value
    @property
    def colors(self):
        return self._colors
    @colors.setter
    def colors(self,value):
        self._colors = value
    @property
    def quad_verts(self):
        return self._quad_verts
    @quad_verts.setter
    def quad_verts(self,value):
        self._quad_verts = value
    @property
    def edges(self):
        return self._edges
    @edges.setter
    def edges(self,value):
        self._edges = value
    
class RenderObject:

    def __init__(self,render_model,shader):
        self.render_model = render_model
        self.shader = shader


    @property
    def render_model(self):
        return self._render_model
    @render_model.setter
    def render_model(self,value):
        self._render_model = value
    @property
    def shader(self):
        return self._shader
    @shader.setter
    def shader(self,value):
        self._shader = value

    def draw(self,viewport,position,quaternion):
        """
        Draw a cube in the 'modern' Open GL style, for post 3.1 versions of
        open GL.

        :param shader_data: compile vertex & pixel shader data for drawing a cube.
        :param filled_cube_indices: the indices to draw the 'filled' cube.
        :param outline_cube_indices: the indices to draw the 'outline' cube.
        :param rotation: the current rotations to apply.
        """
        if self.render_model == None or self.shader == None:
            return
        
        shader_data=self.shader.shader_data
        filled_cube_indices=self.shader.filled_cube_indices
        outline_cube_indices=self.shader.outline_cube_indices

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Filled cube
        GL.glDisable(GL.GL_BLEND)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glUniform4f(shader_data["constants"]["colour_mul"], 1, 1, 1, 1)
        GL.glUniform4f(shader_data["constants"]["colour_add"], 0, 0, 0, 0.0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["filled"])
        GL.glDrawElements(
            GL.GL_TRIANGLES, len(filled_cube_indices), GL.GL_UNSIGNED_INT, None
        )

        # Outlined cube
        GL.glDisable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glEnable(GL.GL_BLEND)
        GL.glUniform4f(shader_data["constants"]["colour_mul"], 0, 0, 0, 0.0)
        GL.glUniform4f(shader_data["constants"]["colour_add"], 1, 1, 1, 1.0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["outline"])
        GL.glDrawElements(GL.GL_LINES, len(outline_cube_indices), GL.GL_UNSIGNED_INT, None)

        viewport_quaternion_world = viewport.quaternion
        screen_quaternion = quaternion#.rotate_by_quat(viewport_quaternion_world)
        
        viewport_rotation_matrix = viewport_quaternion_world.rotation_matrix()
        screen_rotation_matrix = np.dot(viewport_rotation_matrix.T,
                                        screen_quaternion.rotation_matrix())

        x,y,z = np.dot(viewport_rotation_matrix.T,
                       position - viewport.position)
        shader_model = np.eye(4,4, dtype=np.float32)
        shader_model[0,:3] = -screen_rotation_matrix[1,:]
        shader_model[1,:3] = screen_rotation_matrix[2,:]
        shader_model[2,:3] = -screen_rotation_matrix[0,:]
        shader_model[:3,:3] = shader_model[:3,:3].T

        shader_model = mqm.translate(shader_model,-y,z,-x)
        
        GL.glUniformMatrix4fv(shader_data["constants"]["model"], 1, False, shader_model)

from OpenGL.GL import *
import glm
from graphics.texture import Texture
from graphics.shader import Shader
from graphics.mesh import Mesh

class RenderModel:

    def __init__(self,mesh, texture='', shader=''):
        self.model_matrix = glm.mat4(1)
        self.mesh = mesh
        self.texture = texture
        self.shader = shader

    def make_context(self):
        if self.mesh is not None: self.init_mesh()
        if self.shader is not None: self.init_shader()
        if self.mesh is not None: self.init_object()
        if self.texture is not None: self.init_texture()
        return self
    
    def removed(self):
        pass
        
    def init_mesh(self):
        pass

    def init_shader(self):
        #self.shader.initShaderFromGLSL() #done in Shader constructor
        self.MVP_ID = glGetUniformLocation(self.shader.program, "MVP")
        self.OFFSET_ID = glGetUniformLocation(self.shader.program, "OFFSET")
        self.Texture_ID =  glGetUniformLocation(self.shader.program, "myTextureSampler")


    def init_object(self):
        self.vertexbuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vertexbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.mesh.vertex_data)*4, 
            (GLfloat * len(self.mesh.vertex_data))(*self.mesh.vertex_data), GL_STATIC_DRAW)

        self.facesbufferSize = len(self.mesh.faces)

        self.facesbuffer = glGenBuffers(1)        		
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.facesbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(self.mesh.faces)*2,(GLushort * len(self.mesh.faces))(*self.mesh.faces),GL_STATIC_DRAW)

        #self.vertexLen = len(self.mesh.vertex_data)

        #self.colorbuffer = glGenBuffers(1)
        #glBindBuffer(GL_ARRAY_BUFFER, self.colorbuffer)
        #glBufferData(GL_ARRAY_BUFFER, len(self.mesh.color_data)*4, (GLfloat *
        #                                                       len(self.mesh.color_data))(*self.mesh.color_data), GL_STATIC_DRAW)
        
    def init_texture(self):
        if(self.texture.inversedVCoords):
            for index in range(0,len(self.mesh.texcoords)):
                if(index % 2):
                    self.mesh.texcoords[index] = 1.0 - self.mesh.texcoords[index]

        self.texturebuffer = self.texture.textureGLID

        self.uvbuffer  = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.uvbuffer)            
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,len(self.mesh.texcoords)*4,(GLfloat * len(self.mesh.texcoords))(*self.mesh.texcoords),GL_STATIC_DRAW)


    def update(self, new_position, new_rotation_matrix, new_scale=(1,1,1)):
        # order should be scale, rotate, translate. So trans_mat*rot_mat*scale_mat.
        rotation_4d = glm.mat4(glm.mat3(new_rotation_matrix))
        translation_4d = glm.translate(glm.mat4(1),glm.vec3(new_position))
        self.model_matrix = translation_4d*rotation_4d

    def get_MVP_matrix(self, view_matrix, projection_matrix):
        return projection_matrix * view_matrix * self.model_matrix
        
    def draw(self, view_matrix, projection_matrix):
        model_view_projection = self.get_MVP_matrix(view_matrix,projection_matrix)
        
        self.shader.begin()
        glUniformMatrix4fv(self.MVP_ID, 1, GL_FALSE,  glm.value_ptr(model_view_projection)  )

        if self.texture is not None:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texturebuffer)
            glUniform1i(self.Texture_ID, 0) 		#// Set  "myTextureSampler" sampler to use Texture Unit 0

            glEnableVertexAttribArray(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.uvbuffer)
            glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.facesbuffer)
        glDrawElements(
            GL_TRIANGLES,      # mode
            self.facesbufferSize,    #// count
            GL_UNSIGNED_SHORT, #  // type
            None          #// element array buffer offset
        )

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        self.shader.end()
        
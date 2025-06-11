try:
    import OpenGL.GL as gl
except ImportError:
    print("pyopengl missing. The GLCUBE example requires: pyopengl numpy")
    raise SystemExit
import os
import ctypes
import numpy as np
import mathquest.matrix as mqm

class Shader:
    ''' Loads, compiles and contains an OpenGL shader program. '''
    
    def __init__(self,filenames):
        ''' filenames: a list of GLSL file paths, ordered [vertex, fragment]'''
        self.paths = filenames
        self.initShaderFromGLSL()

    def initShaderFromGLSL(self):
        ''' Initialise shader from GLSL files'''
        vertex_shader_paths = [self.paths[0]]
        fragment_shader_paths = [self.paths[1]]
        vertex_shader_source_list = []
        fragment_shader_source_list = []
        if(isinstance(vertex_shader_paths,list)):
            for GLSL in vertex_shader_paths:
                absDIR =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),GLSL))
                f = open(absDIR,'rb')
                vertex_shader_source_list.append(f.read())
                f.close()
            for GLSL in fragment_shader_paths:
                absDIR =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),GLSL))
                f = open(absDIR,'rb')
                fragment_shader_source_list.append(f.read())      
                f.close()    
            self.initShader(vertex_shader_source_list,fragment_shader_source_list)

    def initShader(self, vertex_shader_source_list, fragment_shader_source_list):
        # create program
        self.program= gl.glCreateProgram()

        # vertex shader
        self.vs = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vs, vertex_shader_source_list)
        gl.glCompileShader(self.vs)
        if(gl.GL_TRUE!=gl.glGetShaderiv(self.vs, gl.GL_COMPILE_STATUS)):
            err =  gl.glGetShaderInfoLog(self.vs) 
            raise Exception(err)  
        gl.glAttachShader(self.program, self.vs)

        # fragment shader
        self.fs = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(self.fs, fragment_shader_source_list)
        gl.glCompileShader(self.fs)
        if(gl.GL_TRUE!=gl.glGetShaderiv(self.fs, gl.GL_COMPILE_STATUS)):
            err =  gl.glGetShaderInfoLog(self.fs) 
            raise Exception(err)       
        gl.glAttachShader(self.program, self.fs)

        # link program
        gl.glLinkProgram(self.program)
        if(gl.GL_TRUE!=gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)):
            err =  gl.glGetShaderInfoLog(self.vs) 
            raise Exception(err)

    def begin(self):
        if gl.glUseProgram(self.program):
            print('glUseProgram failed')

    def end(self):
        gl.glUseProgram(0)
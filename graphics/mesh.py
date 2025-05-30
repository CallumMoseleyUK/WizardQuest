try:
    import OpenGL.GL as GL
except ImportError:
    print("pyopengl missing. The GLCUBE example requires: pyopengl numpy")
    raise SystemExit
import os

class Mesh:
    ''' Container for mesh data '''
    # vertex_data = [
    #         -1.0,-1.0,-1.0,
    #         -1.0,-1.0, 1.0,
    #         -1.0, 1.0, 1.0,
    #         1.0, 1.0,-1.0,
    #         -1.0,-1.0,-1.0,
    #         -1.0, 1.0,-1.0,
    #         1.0,-1.0, 1.0,
    #         -1.0,-1.0,-1.0,
    #         1.0,-1.0,-1.0,
    #         1.0, 1.0,-1.0,
    #         1.0,-1.0,-1.0,
    #         -1.0,-1.0,-1.0,
    #         -1.0,-1.0,-1.0,
    #         -1.0, 1.0, 1.0,
    #         -1.0, 1.0,-1.0,
    #         1.0,-1.0, 1.0,
    #         -1.0,-1.0, 1.0,
    #         -1.0,-1.0,-1.0,
    #         -1.0, 1.0, 1.0,
    #         -1.0,-1.0, 1.0,
    #         1.0,-1.0, 1.0,
    #         1.0, 1.0, 1.0,
    #         1.0,-1.0,-1.0,
    #         1.0, 1.0,-1.0,
    #         1.0,-1.0,-1.0,
    #         1.0, 1.0, 1.0,
    #         1.0,-1.0, 1.0,
    #         1.0, 1.0, 1.0,
    #         1.0, 1.0,-1.0,
    #         -1.0, 1.0,-1.0,
    #         1.0, 1.0, 1.0,
    #         -1.0, 1.0,-1.0,
    #         -1.0, 1.0, 1.0,
    #         1.0, 1.0, 1.0,
    #         -1.0, 1.0, 1.0,
    #         1.0,-1.0, 1.0]

    # color_data = [ 
    #         0.583,  0.771,  0.014,
    #         0.609,  0.115,  0.436,
    #         0.327,  0.483,  0.844,
    #         0.822,  0.569,  0.201,
    #         0.435,  0.602,  0.223,
    #         0.310,  0.747,  0.185,
    #         0.597,  0.770,  0.761,
    #         0.559,  0.436,  0.730,
    #         0.359,  0.583,  0.152,
    #         0.483,  0.596,  0.789,
    #         0.559,  0.861,  0.639,
    #         0.195,  0.548,  0.859,
    #         0.014,  0.184,  0.576,
    #         0.771,  0.328,  0.970,
    #         0.406,  0.615,  0.116,
    #         0.676,  0.977,  0.133,
    #         0.971,  0.572,  0.833,
    #         0.140,  0.616,  0.489,
    #         0.997,  0.513,  0.064,
    #         0.945,  0.719,  0.592,
    #         0.543,  0.021,  0.978,
    #         0.279,  0.317,  0.505,
    #         0.167,  0.620,  0.077,
    #         0.347,  0.857,  0.137,
    #         0.055,  0.953,  0.042,
    #         0.714,  0.505,  0.345,
    #         0.783,  0.290,  0.734,
    #         0.722,  0.645,  0.174,
    #         0.302,  0.455,  0.848,
    #         0.225,  0.587,  0.040,
    #         0.517,  0.713,  0.338,
    #         0.053,  0.959,  0.120,
    #         0.393,  0.621,  0.362,
    #         0.673,  0.211,  0.457,
    #         0.820,  0.883,  0.371,
    #         0.982,  0.099,  0.879
    # ]    

    def __init__(self,filename=None):
        self.path = filename
        self.face_length = 0
        self.bNoUV = True
        self.bNoNormals = True
        if filename != None:
            self.load_from_obj(filename)

    def load_from_obj(self,fname):
        fname =  os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),fname))
        f = open(fname,"r") # in text mode

        self.vertex_data = []
        self.faces = []
        self.normals = []
        self.texcoords = []
        for line in f:
            if line.startswith('#'): continue
            items = line.split()

            if(items[0]=="v"):
                v = map(float, items[1:4])
                self.vertex_data.extend(v)
            elif(items[0]=="vn"):
                v = map(float, items[1:4])
                self.normals.extend(v)
            elif(items[0]=="vt"):
                v = map(float, items[1:3])
                self.texcoords.extend(v)
            elif(items[0]=="f"):
                item = items[1].split("/")
                self.face_length = len(item)
                if self.face_length>1:
                    self.bNoUV = item[1]==''
                    self.bNoNormals = not (self.face_length>2 or self.bNoUV)
                index = map(int,item)
                self.faces.extend(index)  
                index = map(int,items[2].split("/"))
                self.faces.extend(index)
                index = map(int,items[3].split("/"))
                self.faces.extend(index)
            elif(items[0]=="s"):               
                self.smooth = items[1] 
            elif(items[0]=="mtllib"):   
                self.referenceMaterials = items[1]
            elif(items[0]=="usemtl"):   
                self.Materials = items[1]
            else:
                print("skip unknown line : %s"%line[0:-1])
        self.to_single_index_style()

    def to_array_style(self):
        vertex_data=[]
        texcoords = []
        normals = []
        for i in range(0,len(self.faces),self.face_length):
            index = 3*(self.faces[i]-1)            
            vertex_data.extend(self.vertex_data[index:index+3])
            if self.face_length>1:
                index = 2*(self.faces[i+1]-1)
                texcoords.extend(self.texcoords[index:index+2])
                if self.face_length>2:
                    index = 3*(self.faces[i+2]-1)
                    normals.extend(self.normals[index:index+3])
        self.vertex_data = vertex_data
        self.texcoords = texcoords
        self.normals = normals
    
    def to_single_index_style(self):
        vertex_data=[]
        texcoords = []
        normals = []
        faces = []
        combinations = []
        for i in range(0,len(self.faces),self.face_length):
            point = self.faces[i:i+self.face_length]
            if(point in combinations):
                pass
            else:
                combinations.append(point)
                index = 3*(self.faces[i]-1)            
                vertex_data.extend(self.vertex_data[index:index+3])
                if self.face_length>1:
                    if not self.bNoUV:
                        index = 2*(self.faces[i+1]-1)
                        texcoords.extend(self.texcoords[index:index+2])
                        if self.face_length>2:
                            index = 3*(self.faces[i+2]-1)
                            normals.extend(self.normals[index:index+3]) 
                    else:
                        index = 2*(self.faces[i+1]-1)
                        normals.extend(self.normals[index:index+2])
            newindex = combinations.index(point)
            faces.append(newindex)
        self.vertex_data = vertex_data
        self.texcoords = texcoords
        self.normals = normals
        self.faces = faces
        

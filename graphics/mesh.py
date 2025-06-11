import os

class Mesh:
    ''' Container for mesh data '''

    def __init__(self,filename=None):
        self.path = filename
        self.face_length = 0
        self.bNoUV = True
        self.bNoNormals = True
        if filename is not None:
            self.load_from_obj(filename)

    def load_from_obj(self,fname):
        ''' Load mesh from a wavefront obj file '''
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
        

from glm import vec3
from random import randint
from urllib.request import urlretrieve

random_colors = False

class Face(object):
  def __init__(self, vA, vB, vC, color, normal):
    self.VertexA = vA
    self.VertexB = vB
    self.VertexC = vC
    self.Normal = normal
    self.Color = color

class objLoader(object):
  def __init__(self, env, objPath ="https://gist.githubusercontent.com/MaikKlein/0b6d6bb58772c13593d0a0add6004c1c/raw"):
    self.OBJUrl = objPath
    self.Environment_Properties = env
    self.heldvertices = []
    self.heldvertexnormals = []
    self.heldfaces = []

  def load(self):
    if self.OBJUrl.split("/")[0] == "models":
      try:
        file = open(self.OBJUrl)
      except:
        print(f"No valid OBJ '{self.OBJUrl}' found; exiting")
        return True
    else:
      try:
        path, headers = urlretrieve(self.OBJUrl)
        file = open(path, 'r')
      except:
        print(f"No valid OBJ at '{self.OBJUrl}' found; exiting")
        return True
    lines = file.readlines()
    for line in lines:
      #for each line in the obj, determine data type
      strings = line.split(" ")
      type = strings[int(0)]

      #convert data to proper class
      #add to applicable list if vertex or vertex normal
      if type == "v":
        vertexdata = vec3(float(strings[1]), float(strings[2]), float(strings[3]))
        self.heldvertices.append(vertexdata)
      if type == "vn":
        vertexdata = vec3(float(strings[1]), float(strings[2]), float(strings[3]))
        self.heldvertexnormals.append(vertexdata)

      #if face, calculate face normal from avg of vertex normals, then add to list of faces
      if type == "f":
        vertex1 = strings[1].split("/")
        vertex2 = strings[2].split("/")
        vertex3 = strings[3].split("/")
        color = (255,255,255)
        if random_colors:
          color = (randint(0,255), randint(0,255), randint(0,255))
        if len(strings) == 4:
          if len(vertex1) == 3:
            avgNormal = (self.heldvertexnormals[int(vertex1[2]) - 1] + self.heldvertexnormals[int(vertex2[2]) - 1] + self.heldvertexnormals[int(vertex3[2]) - 1]) / 3

            face = Face(self.heldvertices[int(vertex1[0])-1],self.heldvertices[int(vertex2[0])-1],self.heldvertices[int(vertex3[0])-1], color, avgNormal)

            self.heldfaces.append(face)
          elif len(vertex1) == 2:
            avgNormal = (self.heldvertexnormals[int(vertex1[1]) - 1] + self.heldvertexnormals[int(vertex2[1]) - 1] + self.heldvertexnormals[int(vertex3[1]) - 1]) / 3

            face = Face(self.heldvertices[int(vertex1[0])-1],self.heldvertices[int(vertex2[0])-1],self.heldvertices[int(vertex3[0])-1], color, avgNormal)

            self.heldfaces.append(face)
        elif len(strings) == 5:
          vertex4 = strings[4].split("/")
          if len(vertex1) == 3:
            avgNormal = (self.heldvertexnormals[int(vertex1[2]) - 1] + self.heldvertexnormals[int(vertex2[2]) - 1] + self.heldvertexnormals[int(vertex3[2]) - 1] + self.heldvertexnormals[int(vertex4[2]) - 1]) / 4

            face1 = Face(self.heldvertices[int(vertex1[0])-1],self.heldvertices[int(vertex2[0])-1],self.heldvertices[int(vertex3[0])-1], color, avgNormal)
            face2 = Face(self.heldvertices[int(vertex1[0])-1],self.heldvertices[int(vertex3[0])-1],self.heldvertices[int(vertex4[0])-1], color, avgNormal)

            self.heldfaces.append(face1)
            self.heldfaces.append(face2)
          elif len(vertex1) == 2:
            avgNormal = (self.heldvertexnormals[int(vertex1[1]) - 1] + self.heldvertexnormals[int(vertex2[1]) - 1] + self.heldvertexnormals[int(vertex3[1]) - 1] + self.heldvertexnormals[int(vertex4[1]) - 1]) / 4

            face1 = Face(self.heldvertices[int(vertex1[0])-1],self.heldvertices[int(vertex2[0])-1],self.heldvertices[int(vertex3[0])-1], color, avgNormal)
            face2 = Face(self.heldvertices[int(vertex1[0])-1],self.heldvertices[int(vertex3[0])-1],self.heldvertices[int(vertex4[0])-1], color, avgNormal)

            self.heldfaces.append(face1)
            self.heldfaces.append(face2)
    return False
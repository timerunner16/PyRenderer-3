import glm
from glm import vec3
from pygame.draw import polygon

class Renderer(object):
  def __init__(self, FOV, triangles, camera, screen_res, model, position, env):
    self.CameraMatrix = glm.lookAt(vec3(0,5,8), vec3(0,0,0), vec3(0,1,0))
    self.PerspectiveMatrix = glm.perspective(glm.radians(FOV),screen_res.x/screen_res.y, 0.02, 10.0)
    self.ModelMatrix = model
    self.PositionMatrix = position
    self.Triangles = triangles
    self.Camera = camera
    self.ScreenRes = screen_res
    self.Environment_Properties = env

  def __computeFaceColor(self, albedo, normal):
    angle = self.Environment_Properties['angle']
    brightness = self.Environment_Properties['brightness']
    ambient = self.Environment_Properties['ambient']
    normal_t = glm.mat3(glm.transpose(glm.inverse(self.ModelMatrix))) * normal
    diff = glm.dot(angle, normal_t)
    diff = max(diff, 0)

    #calculate color using triangle color and lighting values
    diffuse = brightness * diff
    color = (albedo[0] * (diffuse.x + ambient.x), albedo[1] * (diffuse.y + ambient.y), albedo[2] * (diffuse.z + ambient.z))
    color = tuple(map(lambda x: min(x, 255), color))
    return color
    
  def Render(self, surface):
    displays = []
    
    for t in self.Triangles:
      vA = t.VertexA
      vB = t.VertexB
      vC = t.VertexC
      
      #transform to clipping space
      vA = self.PerspectiveMatrix * self.CameraMatrix * self.PositionMatrix * self.ModelMatrix * glm.vec4(vA, 1)
      vB = self.PerspectiveMatrix * self.CameraMatrix * self.PositionMatrix * self.ModelMatrix * glm.vec4(vB, 1)
      vC = self.PerspectiveMatrix * self.CameraMatrix * self.PositionMatrix * self.ModelMatrix * glm.vec4(vC, 1)
      
      #simple view clipping
      if vA.z > 0 or vB.z > 0 or vC.z > 0:
        continue

      #transform to screen space
      vA_t = glm.vec2(vA.x/vA.z, vA.y/vA.z)
      vB_t = glm.vec2(vB.x/vB.z, vB.y/vB.z)
      vC_t = glm.vec2(vC.x/vC.z, vC.y/vC.z)

      #backface culling
      vA_bc = vec3(vA_t.x, vA_t.y, vA.z)
      vB_bc = vec3(vB_t.x, vB_t.y, vB.z)
      vC_bc = vec3(vC_t.x, vC_t.y, vC.z)
      if glm.cross(vA_bc-vB_bc, vA_bc-vC_bc).z > 0:
        continue

      depth = (vA.z + vB.z + vC.z)/3
      
      vA_t.x = vA_t.x * self.ScreenRes.x + self.ScreenRes.x/2
      vA_t.y = vA_t.y * self.ScreenRes.y + self.ScreenRes.y/2
      
      vB_t.x = vB_t.x * self.ScreenRes.x + self.ScreenRes.x/2
      vB_t.y = vB_t.y * self.ScreenRes.y + self.ScreenRes.y/2
      
      vC_t.x = vC_t.x * self.ScreenRes.x + self.ScreenRes.x/2
      vC_t.y = vC_t.y * self.ScreenRes.y + self.ScreenRes.y/2


      color = self.__computeFaceColor(t.Color, t.Normal)
      displays.append([vA_t, vB_t, vC_t, color, depth])

    displays.sort(key=lambda x: x[4])
    
    for t in displays:
      cA = t[0]
      cB = t[1]
      cC = t[2]
      Color = t[3]
      polygon(surface, Color, [(cA.x, cA.y), (cB.x, cB.y), (cC.x, cC.y)])
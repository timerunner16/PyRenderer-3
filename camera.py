import pygame
import glm
from glm import vec3

class Camera(object):
  def __init__(self, position=vec3(0,0,8), rotation=vec3(0,90,0), speed=4, rotation_speed=120, **kwargs):
    self.Position = position
    self.Rotation = rotation
    self.Speed = speed
    self.RotationSpeed = rotation_speed

  @property
  def ForwardVector(self):
    forward = vec3()
    forward.x = glm.cos(glm.radians(self.Rotation.y)) * glm.cos(glm.radians(self.Rotation.x))
    forward.y = glm.sin(glm.radians(self.Rotation.x))
    forward.z = glm.sin(glm.radians(self.Rotation.y)) * glm.cos(glm.radians(self.Rotation.x))
    return glm.normalize(forward)

  @property
  def RightVector(self):
    return glm.normalize(glm.cross(self.ForwardVector, vec3(0,1,0)))

  @property
  def UpVector(self):
    forward = self.ForwardVector
    return glm.normalize(glm.cross(forward, glm.normalize(glm.cross(forward, vec3(0,1,0)))))
  
  def Update(self, r, dt):
    inputs = pygame.key.get_pressed()

    #movement
    if inputs[pygame.K_w]:
      self.Position -= self.ForwardVector * dt * self.Speed
    if inputs[pygame.K_s]:
      self.Position += self.ForwardVector * dt * self.Speed
    if inputs[pygame.K_d]:
      self.Position -= self.RightVector * dt * self.Speed
    if inputs[pygame.K_a]:
      self.Position += self.RightVector * dt * self.Speed
    if inputs[pygame.K_q]:
      self.Position += self.UpVector * dt * self.Speed
    if inputs[pygame.K_e]:
      self.Position -= self.UpVector * dt * self.Speed

    #rotation
    if inputs[pygame.K_LEFT]:
      self.Rotation.y -= self.RotationSpeed * dt
    if inputs[pygame.K_RIGHT]:
      self.Rotation.y += self.RotationSpeed * dt
    if inputs[pygame.K_DOWN]:
      self.Rotation.x += self.RotationSpeed * dt
    if inputs[pygame.K_UP]:
      self.Rotation.x -= self.RotationSpeed * dt

    #wrap camera rotation [0-360]
    if self.Rotation.y >= 360:
      self.Rotation.y -= 360

    if self.Rotation.y < 0:
      self.Rotation.y += 360

    if self.Rotation.x > 80:
      self.Rotation.x = 80

    if self.Rotation.x < -80:
      self.Rotation.x = -80
      
    #update camera matrix in renderer properties
    r.CameraMatrix = glm.lookAt(self.Position, self.Position + self.ForwardVector, vec3(0,1,0))
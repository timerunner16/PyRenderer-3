import glm

def eul2mat4(pitch, yaw, roll):
  pitch = glm.radians(pitch)
  yaw = glm.radians(yaw)
  roll = glm.radians(roll)
  
  qx = glm.sin(roll/2) * glm.cos(pitch/2) * glm.cos(yaw/2) - glm.cos(roll/2) * glm.sin(pitch/2) * glm.sin(yaw/2)
  qy = glm.cos(roll/2) * glm.sin(pitch/2) * glm.cos(yaw/2) + glm.sin(roll/2) * glm.cos(pitch/2) * glm.sin(yaw/2)
  qz = glm.cos(roll/2) * glm.cos(pitch/2) * glm.sin(yaw/2) - glm.sin(roll/2) * glm.sin(pitch/2) * glm.cos(yaw/2)
  qw = glm.cos(roll/2) * glm.cos(pitch/2) * glm.cos(yaw/2) + glm.sin(roll/2) * glm.sin(pitch/2) * glm.sin(yaw/2)

  return glm.mat4_cast(glm.quat(qw, qx, qy, qz))
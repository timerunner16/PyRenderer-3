import pygame, sys
from pygame.locals import QUIT
import glm
from glm import vec3
from objloader import objLoader
from camera import Camera
from renderer import Renderer
from math_helper import eul2mat4
import dearpygui.dearpygui as dpg

#PROPERTIES
#model properties
objpath = "models/sphere.obj"
model_pos = glm.translate(glm.mat4(1.0), vec3(0,0,0))
model_scale = glm.scale(glm.mat4(1.0), vec3(1,1,1))
model_rot = eul2mat4(0,0,0)

#window properties
screen_res = glm.vec2(640, 480)
background_color = (6, 14, 25)

#lighting properties
env_angle = vec3(-0.4, 0.7, -0.2)
env_ambient = vec3(0.3,0.3,0.3)
env_brightness = vec3(1,1,1)

#camera properties
fov = 90
speed = 4
rot_speed = 120
start_pos = vec3(0,0,0)
start_rot = vec3(0,0,0)

#GUI
dpg.create_context()

def apply_settings():
  global objpath
  global model_pos
  global model_rot
  global model_scale
  
  global background_color
  
  global env_angle
  global env_brightness
  global env_ambient
  
  global fov
  global speed
  global rot_speed
  global start_pos
  global start_rot
  
  objpath = dpg.get_value("__input_obj")
  
  model_pos_list = dpg.get_value("__input_model_pos")
  model_pos = glm.translate(glm.mat4(1.0), vec3(model_pos_list[0],model_pos_list[1],model_pos_list[2]))
  
  model_rot_list = dpg.get_value("__input_model_rot")
  model_rot = eul2mat4(model_rot_list[0],model_rot_list[1],model_rot_list[2])
  
  model_scale_list = dpg.get_value("__input_model_scale")
  model_scale = glm.scale(glm.mat4(1.0), vec3(model_scale_list[0],model_scale_list[1],model_scale_list[2]))

  
  screen_res.x = dpg.get_value("__input_width")
  screen_res.y = dpg.get_value("__input_height")
  bg_color_list = dpg.get_value("__input_bg_color")
  background_color = (bg_color_list[0], bg_color_list[1], bg_color_list[2])

  
  env_angle_list = dpg.get_value("__input_env_angle")
  env_angle = vec3(env_angle_list[0], env_angle_list[1], env_angle_list[2])
  
  env_brightness_list = dpg.get_value("__input_env_brightness")
  env_brightness = vec3(env_brightness_list[0],env_brightness_list[1],env_brightness_list[2])
  
  env_ambient_list = dpg.get_value("__input_env_ambient")
  env_ambient = vec3(env_ambient_list[0],env_ambient_list[1],env_ambient_list[2])

  
  fov = dpg.get_value("__input_fov")
  
  speed = dpg.get_value("__input_speed_pos")
  
  rot_speed = dpg.get_value("__input_speed_rot")
  
  start_pos_list = dpg.get_value("__input_camera_pos")
  start_pos = vec3(start_pos_list[0],start_pos_list[1],start_pos_list[2])
  
  start_rot_list = dpg.get_value("__input_camera_rot")
  start_rot = vec3(start_rot_list[0],start_rot_list[1],start_rot_list[2])

with dpg.window(tag="Primary Window"):
  dpg.add_text("Press apply settings to change renderer properties.")
  dpg.add_text("Close this window to start the renderer.")
  dpg.add_button(label = "Apply Settings", callback = apply_settings)
  
  with dpg.collapsing_header(label="Model"):
    dpg.add_input_text(label = "OBJ Path", tag = "__input_obj", default_value = "models/sphere.obj")
    dpg.add_input_floatx(label = "Position", tag = "__input_model_pos", default_value = [0, 0, 0], size = 3)
    dpg.add_input_floatx(label = "Rotation", tag = "__input_model_rot", default_value = [0,0,0], min_value = 0, max_value = 360, size = 3)
    dpg.add_input_floatx(label = "Scale", tag = "__input_model_scale", default_value = [1,1,1], size = 3)
  with dpg.collapsing_header(label="Window"):
    dpg.add_input_int(label = "Width", tag = "__input_width", default_value = 640)
    dpg.add_input_int(label = "Height", tag = "__input_height", default_value = 480)
    dpg.add_input_intx(label = "Background Color", tag = "__input_bg_color", default_value = [6,14,25], min_value = 0, max_value = 255, size = 3)
  with dpg.collapsing_header(label="Lighting"):
    dpg.add_input_floatx(label = "Sun Angle", tag = "__input_env_angle", default_value = [-0.4, 0.7, -0.2], min_value = -1, max_value = 1, size = 3)
    dpg.add_input_floatx(label = "Sun Brightness", tag = "__input_env_brightness", default_value = [1,1,1], min_value = 0, max_value = 1, size = 3)
    dpg.add_input_floatx(label = "Sun Ambient", tag = "__input_env_ambient", default_value = [0.3,0.3,0.3], min_value = 0, max_value = 1, size = 3)
  with dpg.collapsing_header(label="Camera"):
    dpg.add_input_int(label = "FOV", tag = "__input_fov", default_value = 90)
    dpg.add_input_int(label = "Movement Speed", tag = "__input_speed_pos", default_value = 4)
    dpg.add_input_int(label = "Rotation Speed", tag = "__input_speed_rot", default_value = 120)
    dpg.add_input_floatx(label = "Start Position", tag = "__input_camera_pos", default_value = [0, 0, 0], size = 3)
    dpg.add_input_floatx(label = "Start Rotation", tag = "__input_camera_rot", default_value = [0, 0, 0], min_value = 0, max_value = 360, size = 3)


dpg.create_viewport(title='Renderer Properties', width = 400, height = 200)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()
dpg.destroy_context()

#SETUP RENDERER
triangles = []

tick = 0
dt = 0

model = model_rot * model_scale
camera = Camera(position=start_pos,rotation=start_rot, speed=speed,rotation_speed=rot_speed)

env = {'angle': env_angle, 'brightness': env_brightness, 'ambient': env_ambient}
renderer = Renderer(fov, triangles, camera, screen_res, model, model_pos, env)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((screen_res.x, screen_res.y))
pygame.display.set_caption(f'PySoftware Renderer v3.0 {objpath}')
clock = pygame.time.Clock()

obj = objLoader({'angle': env_angle, 'brightness': env_brightness, 'ambient': env_ambient}, objpath)
e = obj.load()

if e:
  pygame.quit()
  sys.exit()

for f in obj.heldfaces:
	triangles.append(f)
del(obj)

font = pygame.font.SysFont("arial", 24)

#MAIN LOOP
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  dt = (pygame.time.get_ticks() - tick)/1000
  tick = pygame.time.get_ticks()
  
  camera.Update(renderer, dt)

  DISPLAYSURF.fill(background_color)

  renderer.Render(DISPLAYSURF)
  
  fps = 1//dt
  displaytext = font.render(str(fps), False, (255,255,0), (40,40,40))
  DISPLAYSURF.blit(displaytext, (20,20))

  pygame.display.update()

  #clock.tick(60)
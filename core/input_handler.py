import pygame as pg


class InputHandler:
  def __init__(self) -> None:
    pg.joystick.init()
    joystick_count = pg.joystick.get_count()
    if joystick_count == 0:
      print("No joysticks detected.")
    else:
      print("joystick detected")
      self.joystick = pg.joystick.Joystick(0)
      self.joystick.init()
      print(f"joystick name: {self.joystick.get_name()}")

  def get_player_inputs(self):
    keys = pg.key.get_pressed()
    return_list = []

		### horizontal movement
    if keys[pg.K_a]:
      return_list.append('move_left') 
    if keys[pg.K_d]:
      return_list.append('move_right')
    left_stick_axis = self.joystick.get_axis(0)
    if left_stick_axis < - 0.3:
      return_list.append('move_left')
    if left_stick_axis > 0.3:
      return_list.append('move_right')

		# jump
    if keys[pg.K_SPACE]:
      return_list.append('jump')
    if self.joystick.get_button(0):
      return_list.append('jump')

    return return_list

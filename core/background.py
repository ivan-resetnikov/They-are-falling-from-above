import pygame as pg
from .constants import RENDER_SCALE


class Background:
  def __init__(self):
    self.bg = pg.image.load('assets/bg.png').convert()
    self.bgSpeed = 0.5
    self.bgBlocks = []
    self.bgSpawnCooldown = 128 - self.bgSpeed

    for y in range(12):
      for x in range(12):
        self.bgBlocks.append( [ [64 * x - self.bgSpeed, 64 * y - self.bgSpeed] ] )

  def render(self, blit_surface: pg.Surface):
    for block in self.bgBlocks:
      blit_surface.blit(self.bg, block[0])
      block[0][0] += self.bgSpeed
      block[0][1] += self.bgSpeed
      if block[0][0] > RENDER_SCALE[0] and block[0][1] > RENDER_SCALE[1]:
        self.bgBlocks.remove(block)

    if self.bgSpawnCooldown > 64 * (1 / self.bgSpeed) - 1:
      for i in range(12): 
        self.bgBlocks.append([[-64, -64 + (64 * i)]])
      for i in range(12): 
        self.bgBlocks.append([[-64 + (64 * i), -64]])
      self.bgSpawnCooldown = 0
    self.bgSpawnCooldown += 1
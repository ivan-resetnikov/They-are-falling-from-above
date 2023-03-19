import pygame as pg

from .player import colliding

from random import randint



class Enermy :
	def __init__ (self) :
		self.img = pg.image.load('assets/enermy.png').convert_alpha()

		self.pos = [randint(0, 400), -16]

		self.size = [12, 12]
		self.time = 0

		self.dead = False


	def render (self, frame, cam) :
		img = pg.transform.rotate(self.img, self.time * 3)

		frame.blit(img, (
				self.pos[0] - cam.pos[0] - (img.get_width () * 0.5),
				self.pos[1] - cam.pos[1] - (img.get_height() * 0.5)
			))


	def update (self, level) :
		if colliding(self, level) : self.dead = True

		self.pos[1] += 3

		self.time += 1
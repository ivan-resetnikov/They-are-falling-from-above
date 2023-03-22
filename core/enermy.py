import pygame as pg
from .player import colliding
from .sound  import SOUNDS
from random import uniform, randint
from .constants import DEATH_ANIM_SIZE


class Enermy :
	def __init__ (self) :
		self.img = pg.image.load('assets/enermy.png').convert_alpha()
		self.shadow = pg.image.load('assets/enermy.png').convert_alpha()
		self.shadow.fill((34, 32, 52))
		self.shadow.set_alpha(128)
		self.pos = [randint(64, 336), -16]
		self.speed = uniform(3, 4)
		self.size = [12, 10]
		self.time = 0
		self.dead = False
		self.playedDeathAnim = False
		self.deathRect = pg.Surface((16, 8)).convert_alpha()
		self.deathRect.fill((255, 255, 255))
		self.deathAnim = DEATH_ANIM_SIZE
		self.deathAnimRot = randint(0, 360)

	def render (self, frame, cam) :
		self.cam = cam
		shadow = pg.transform.rotate(self.shadow, self.time * self.speed)
		img = pg.transform.rotate(self.img, self.time * self.speed)

		frame.blit(shadow, ( self.pos[0] - cam.pos[0] - (img.get_width() * 0.5) + 2, self.pos[1] - cam.pos[1] - (img.get_height() * 0.5) + 2))
		frame.blit(img, ( self.pos[0] - cam.pos[0] - (img.get_width() * 0.5), self.pos[1] - cam.pos[1] - (img.get_height() * 0.5)))

		if self.deathAnim < DEATH_ANIM_SIZE:
			img = pg.transform.rotate(
					pg.transform.scale(
						self.deathRect,
						(
							DEATH_ANIM_SIZE - self.deathAnim,
							self.deathAnim
						)
					),
					self.deathAnimRot)
			frame.blit( img, ( self.pos[0] - img.get_width () * 0.5 - cam.pos[0], self.pos[1] - img.get_height() * 0.5 - cam.pos[1] ))

	def update(self, level, player):
		if colliding(self, level, [6, 0]):
			self.dead = True
		if colliding(self, [player], [6, 0]):
			player.dead = True
			self.dead = True

		self.pos[1] += self.speed
		self.time += 1

		if self.dead and not self.playedDeathAnim:
			self.playedDeathAnim = True
			self.deathAnim -= 1
			self.speed = 0
			self.cam.screenShake = 2
			SOUNDS['enermy']['death'].play()

		if self.dead and self.deathAnim > 0 and self.deathAnim < DEATH_ANIM_SIZE:
			self.deathAnim *= 0.6
import pygame as pg
from .player import colliding
from .sound  import SOUNDS
from random import choice


class Target :
	def __init__ (self, pos) :
		self.pos = [pos[0] + 7, pos[1] + 25]
		self.size = (18, 4)
		self.anim = 0

	def changePos (self, pos) :
		plannedPos = choice(pos)
		plannedPos = [plannedPos[0] + 7, plannedPos[1] + 25]

		while plannedPos == self.pos :
			plannedPos = choice(pos)
			plannedPos = [plannedPos[0] + 7, plannedPos[1] + 25]
		else : self.pos = plannedPos

	def update (self, player, pos, updateScore, game) :
		if colliding(self, [player], [-8, 0]) :
			self.changePos(pos)
			player.score += 1
			self.cam.screenShake = 2.5
			updateScore()
			game.scoreDisplaySize = 5
			SOUNDS['player']['score'].play()

	def render (self, frame, cam) :
		self.cam = cam

		if self.anim < 10 :
			color =  (255, 255, 255)
		elif self.anim >= 10 :
			color = (95, 205, 228)

		pg.draw.rect(
			frame,
			color,
			(
				self.pos[0] - cam.pos[0],
				self.pos[1] - cam.pos[1] + 3,
				18,
				4,
			)
		)

		self.anim += 1
		if self.anim == 20 : self.anim = 0
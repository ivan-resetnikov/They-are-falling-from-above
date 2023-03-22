import pygame as pg
from .player import colliding
import random


# target refers to the objects the player is collecting 
class Target:
	def __init__(self, pos):
		self.pos = [pos[0] + 7, pos[1] + 25]
		self.size = (18, 4)
		self.anim = 0

	def _play_sound(self, sound_name: str) -> None:
		valid_sound_names_list = ['score']
		if sound_name in valid_sound_names_list:
			sound = pg.mixer.Sound(f"assets/sounds/{sound_name}.wav")
			sound.set_volume(.5)
			sound.play()

	def changePos(self, pos):
		plannedPos = random.choice(pos)
		plannedPos = [plannedPos[0] + 7, plannedPos[1] + 25]

		while plannedPos == self.pos:
			plannedPos = random.choice(pos)
			plannedPos = [plannedPos[0] + 7, plannedPos[1] + 25]
		else: 
			self.pos = plannedPos

	def update(self, player, pos, updateScore, game):
		if colliding(self, [player], [-8, 0]):
			self.changePos(pos)
			player.score += 1
			self.cam.screenShake = 2.5
			updateScore()
			game.scoreDisplaySize = 5
			self._play_sound('score')

	def render(self, frame, cam):
		self.cam = cam

		if self.anim < 10:
			color =  (255, 255, 255)
		elif self.anim >= 10:
			color = (95, 205, 228)

		pg.draw.rect(frame, color, (self.pos[0] - cam.pos[0], self.pos[1] - cam.pos[1] + 3, 18, 4,))

		self.anim += 1
		if self.anim == 20: self.anim = 0
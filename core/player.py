from .sound import Sounds

from random import randint, uniform

import pygame as pg

Controller = {
	'speed': 0.6,

	'run_friction': 0.8,
	'brake_friction': 0.6,

	'jump_force': -5.5,
	'coyote_jump_time': 11,

	'jump_gravity' : 0.2,
	'glide_gravity': 0.08,
	'fall_gravity' : 0.6,

	'max_fall_speed' : 6.5,
}



def colliding (obj, colliders, offset=[0, 0]) :
	colliding = False

	for collider in colliders :
		if pg.Rect((obj.pos[0] - offset[0], obj.pos[1] - offset[1], obj.size[0], obj.size[1])).colliderect((collider.pos[0], collider.pos[1], collider.size[0], collider.size[1])) :
			colliding = True

	return colliding


class Player :
	def __init__ (self) :
		self.img = pg.image.load('assets/player.png').convert_alpha()

		self.shadow = pg.image.load('assets/player.png').convert_alpha()
		self.shadow.fill((34, 32, 52))

		self.shadow.set_alpha(128)

		self.pos = [198, 0]
		self.vel = [0, 0]

		self.size = (16, 16)

		self.time_since_landed = 0
		self.holding_space = False

		self.score = 0
		self.dead = False

		self.deathAnimParticles = []
		self.spawnedDeathParticles = False


	def update (self, level) :
		if not self.dead :
			self.physics(level, pg.key.get_pressed())
		
		else :
			if not self.spawnedDeathParticles :
				self.spawnedDeathParticles = True

				for _ in range(10) : self.deathAnimParticles.append(
					[
						[self.pos[0] + 8, self.pos[1] + 8],
						[uniform(-7, 7), uniform(-6, -4)],
						randint(1, 3)
					])

				Sounds['player']['death'].play()
				pg.mixer.music.fadeout(1 * 1000)

				self.pos = [198, 0]
				self.vel = [0, 0]


	def render (self, frame, cam) :
		img = pg.transform.rotate(
				pg.transform.scale(
					self.img,
					(
						self.img.get_width()  + abs(self.vel[0]) - abs(self.vel[1] * 0.5),
						self.img.get_height() + self.vel[1]
					)),

				self.vel[0] * 5)

		shadow = pg.transform.rotate(
				pg.transform.scale(
					self.shadow,
					(
						self.img.get_width()  + round(abs(self.vel[0]) + 0.5) - round(abs(self.vel[1] * 0.5)),
						self.img.get_height() + self.vel[1]
					)),

				self.vel[0] * 5)

		frame.blit(
			shadow,
			(
				self.pos[0] - cam.pos[0] - (img.get_width() * 0.5) + 2,
				self.pos[1] - cam.pos[1] + 2
			))

		frame.blit(
			img,
			(
				self.pos[0] - cam.pos[0] - (img.get_width() * 0.5),
				self.pos[1] - cam.pos[1]
			))

		for particle in self.deathAnimParticles :
			pg.draw.circle(frame, (255, 255, 255), particle[0], particle[2])

			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1]

			particle[1][0] *= 0.9
			particle[1][1] += 0.25

			if particle[0][1] > 500 : self.deathAnimParticles.remove(particle)


	def physics (self, colliders, keys) :
		### horizontal movement
		if keys[pg.K_a] : self.vel[0] -= Controller['speed']
		if keys[pg.K_d] : self.vel[0] += Controller['speed']

		self.pos[0] += self.vel[0]

		# wall colliding
		if colliding(self, colliders, [8, 0]) : self.pos[0] -= self.vel[0]

		# friction
		if keys[pg.K_a] or keys[pg.K_d] : self.vel[0] *= Controller['run_friction']
		if not keys[pg.K_a] and not keys[pg.K_d] : self.vel[0] *= Controller['brake_friction']

		### gravity
		self.pos[1] += self.vel[1]

		self.pos[1] += 1

		# landing
		if colliding(self, colliders, [8, 0]) :
			self.pos[1] -= self.vel[1]
			self.vel[1] = 0

			self.time_since_landed = Controller['coyote_jump_time']

		else :
			# gravity
			if self.vel[1] > 0 : self.vel[1] += Controller['fall_gravity']
			if self.vel[1] < 0 : self.vel[1] += Controller['jump_gravity']
			if self.vel[1] < 1 and self.vel[1] > -1 : self.vel[1] += Controller['glide_gravity']

			if self.vel[1] > Controller['max_fall_speed'] : self.vel[1] = Controller['max_fall_speed']

		self.pos[1] -= 1

		### jumping

		# coyote jump timer
		if self.time_since_landed > 0 : self.time_since_landed -= 1

		# jump
		if self.time_since_landed > 0 :
			if keys[pg.K_SPACE] and not self.holding_space :
				self.vel[1] = Controller['jump_force']
				self.holding_space = True

				self.pos[1] += self.vel[1]

				Sounds['player']['jump'].play()

		# cut jump height
		self.pos[1] += 3

		if (self.holding_space and not keys[pg.K_SPACE]) or (self.holding_space and colliding(self, colliders, [8, 0])) :
			self.vel[1] /= 3
			self.holding_space = False

		self.pos[1] -= 3
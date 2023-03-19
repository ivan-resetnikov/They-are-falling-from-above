from .sound import Sounds

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



def colliding (obj, colliders) :
	colliding = False

	for collider in colliders :
		if pg.Rect((obj.pos[0], obj.pos[1], obj.size[0], obj.size[1])).colliderect((collider.pos[0], collider.pos[1], collider.size[0], collider.size[1])) :
			colliding = True

	return colliding


class Player :
	def __init__ (self) :
		self.img = pg.image.load('assets/player.png').convert_alpha()

		self.pos = [198, 0]
		self.vel = [0, 0]

		self.size = (16, 16)

		self.time_since_landed = 0
		self.holding_space = False

		self.score = 0


	def update (self, level) :
		self.physics(level, pg.key.get_pressed())


	def render (self, frame, cam) :
		frame.blit(
			pg.transform.rotate(
				pg.transform.scale(
					self.img,
					(
						self.img.get_width() + abs(self.vel[0]),
						self.img.get_height() + self.vel[1]
					)),

				self.vel[0]*5),

			(
				self.pos[0] - cam.pos[0],
				self.pos[1] - cam.pos[1]
			))


	def physics (self, colliders, keys) :
		### horizontal movement
		if keys[pg.K_a] : self.vel[0] -= Controller['speed']
		if keys[pg.K_d] : self.vel[0] += Controller['speed']

		self.pos[0] += self.vel[0]

		# wall colliding
		if colliding(self, colliders) : self.pos[0] -= self.vel[0]

		# friction
		if keys[pg.K_a] or keys[pg.K_d] : self.vel[0] *= Controller['run_friction']
		if not keys[pg.K_a] and not keys[pg.K_d] : self.vel[0] *= Controller['brake_friction']

		### gravity
		self.pos[1] += self.vel[1]

		self.pos[1] += 1

		# landing
		if colliding(self, colliders) :
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

		if (self.holding_space and not keys[pg.K_SPACE]) or (self.holding_space and colliding(self, colliders)) :
			self.vel[1] /= 3
			self.holding_space = False

		self.pos[1] -= 3
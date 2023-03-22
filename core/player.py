import pygame as pg
import random
from .constants import CONTROLLER


def colliding (obj, colliders, offset=[0, 0]) -> bool:
	for collider in colliders :
		if pg.Rect((obj.pos[0] - offset[0], obj.pos[1] - offset[1], obj.size[0], obj.size[1])).colliderect((collider.pos[0], collider.pos[1], collider.size[0], collider.size[1])) :
			return True
	return False


class Player :
	def __init__ (self) :
		self.img_surface = pg.image.load('assets/player.png').convert_alpha()
		self.shadow_surface = pg.image.load('assets/player.png').convert_alpha()
		self.shadow_surface.fill((34, 32, 52))
		self.shadow_surface.set_alpha(128)
		self.pos = [198, 0]
		self.vel = [0, 0]
		self.size = (16, 16)
		self.time_since_landed = 0
		self.holding_space = False
		self.score = 0
		self.dead = False
		self.deathAnimParticles = []
		self.spawnedDeathParticles = False

	def _play_sound(self, sound_name: str):
		valid_sound_names_list = ['jump', 'death']
		if sound_name in valid_sound_names_list:
			sound = pg.mixer.Sound(f"assets/sounds/{sound_name}.wav")
			if sound_name == 'death':
				sound.set_volume(2)
			else:
				sound.set_volume(.25)
			sound.play()

	def update (self, level) :
		if not self.dead :
			self.physics(level, pg.key.get_pressed())
		else :
			if not self.spawnedDeathParticles :
				self.spawnedDeathParticles = True
				for _ in range(10) : self.deathAnimParticles.append(
					[
						[self.pos[0] + 8, self.pos[1] + 8],
						[random.uniform(-7, 7), random.uniform(-6, -4)],
						random.randint(1, 3)
					])
				self._play_sound('death')
				pg.mixer.music.fadeout(1 * 1000)
				self.pos = [198, 0]
				self.vel = [0, 0]

	def render (self, frame, cam) :
		img_size = ( self.img_surface.get_width() + abs(self.vel[0]) - abs(self.vel[1] * 0.5),	self.img_surface.get_height() + self.vel[1] )
		img_angle = self.vel[0] * 5
		img = pg.transform.rotate( pg.transform.scale( self.img_surface, img_size ), img_angle )

		shadow_size = ( self.img_surface.get_width()  + round(abs(self.vel[0]) + 0.5) - round(abs(self.vel[1] * 0.5)), self.img_surface.get_height() + self.vel[1] )
		shadow_angle = self.vel[0] * 5
		shadow = pg.transform.rotate( pg.transform.scale( self.shadow_surface, shadow_size), shadow_angle)

		frame.blit( shadow,( self.pos[0] - cam.pos[0] - ( img.get_width() * 0.5 ) + 2, self.pos[1] - cam.pos[1] + 2 ) )
		frame.blit( img,( self.pos[0] - cam.pos[0] - ( img.get_width() * 0.5 ), self.pos[1] - cam.pos[1] ) )

		for particle in self.deathAnimParticles :
			pg.draw.circle(frame, (255, 255, 255), particle[0], particle[2])
			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1]
			particle[1][0] *= 0.9
			particle[1][1] += 0.25
			if particle[0][1] > 500 : self.deathAnimParticles.remove(particle)

	def physics (self, colliders, keys) :
		### horizontal movement
		if keys[pg.K_a] : self.vel[0] -= CONTROLLER['speed']
		if keys[pg.K_d] : self.vel[0] += CONTROLLER['speed']

		self.pos[0] += self.vel[0]

		# wall colliding
		if colliding(self, colliders, [8, 0]):
			self.pos[0] -= self.vel[0]

		# friction
		if keys[pg.K_a] or keys[pg.K_d]: 
			self.vel[0] *= CONTROLLER['run_friction']
		if not keys[pg.K_a] and not keys[pg.K_d]:
			self.vel[0] *= CONTROLLER['brake_friction']

		### gravity
		self.pos[1] += self.vel[1]
		self.pos[1] += 1

		# landing
		if colliding(self, colliders, [8, 0]) :
			self.pos[1] -= self.vel[1]
			self.vel[1] = 0
			self.time_since_landed = CONTROLLER['coyote_jump_time']
		else :
			# gravity
			if self.vel[1] > 0 : self.vel[1] += CONTROLLER['fall_gravity']
			if self.vel[1] < 0 : self.vel[1] += CONTROLLER['jump_gravity']
			if self.vel[1] < 1 and self.vel[1] > -1 : self.vel[1] += CONTROLLER['glide_gravity']
			if self.vel[1] > CONTROLLER['max_fall_speed'] : self.vel[1] = CONTROLLER['max_fall_speed']

		self.pos[1] -= 1

		# coyote jump timer
		if self.time_since_landed > 0: 
			self.time_since_landed -= 1

		# jump
		if self.time_since_landed > 0 :
			if keys[pg.K_SPACE] and not self.holding_space:
				self.vel[1] = CONTROLLER['jump_force']
				self.holding_space = True
				self.pos[1] += self.vel[1]
				self._play_sound('jump')

		# cut jump height
		self.pos[1] += 3

		if (self.holding_space and not keys[pg.K_SPACE]) or (self.holding_space and colliding(self, colliders, [8, 0])):
			self.vel[1] /= 3
			self.holding_space = False
			
		self.pos[1] -= 3
# initialize graphics library
import pygame as pg
pg.mixer.init()
pg.font. init()
pg.      init()

from random import choice



class Game :
	def __init__ (self) :
		# config
		self.windowSize  = (800, 800)
		self.renderScale = (400, 400)
		self.title = 'Better Fall Flat!'

		self.FPS = 60

		# initialize window
		self.window = pg.display.set_mode(self.windowSize)
		self.frame  = pg.Surface(self.renderScale)
		self.clock  = pg.time.Clock()

		pg.display.set_caption(self.title)

		# initialize core components
		import core
		self.core = core


	def run (self) :
		self.onStart()

		self.running = True
		while self.running :
			for event in pg.event.get() :
				if event.type == pg.QUIT :
					self.running = False

			self.update()
			self.render()


	def initBG (self) :
		self.bg = pg.image.load('assets/bg.png').convert()
		self.bgSpeed = 0.5

		self.bgBlocks = []
		self.bgSpawnCooldown = 128 - self.bgSpeed

		for y in range(12) :
			for x in range(12) :
				self.bgBlocks.append([[64 * x - self.bgSpeed, 64 * y - self.bgSpeed]])


	def renderBG (self) :
		for block in self.bgBlocks :
			self.frame.blit(self.bg, block[0])

			block[0][0] += self.bgSpeed
			block[0][1] += self.bgSpeed

			if block[0][0] > self.renderScale[0] and block[0][1] > self.renderScale[1] :
				self.bgBlocks.remove(block)

		if self.bgSpawnCooldown > 64 * (1 / self.bgSpeed) - 1 :
			for i in range(12) : self.bgBlocks.append([[-64, -64 + (64 * i)]])
			for i in range(12) : self.bgBlocks.append([[-64 + (64 * i), -64]])

			self.bgSpawnCooldown = 0

		self.bgSpawnCooldown += 1


	def updateEnemies (self) :
		toRemove = []
		for enermy in self.enemies :
			enermy.update(self.tiles)

			if enermy.dead :
				toRemove.append(enermy)

		for enermy in toRemove : self.enemies.remove(enermy)

		if self.enermySpawnCooldown > 32 :
			self.enemies.append(self.core.Enermy())

			self.enermySpawnCooldown = 0

		self.enermySpawnCooldown += 1


	def render (self) :
		# clear frame
		self.frame.fill((0, 0, 0))

		# background
		self.renderBG()

		# level & enemies
		[tile  .render(self.frame, self.camera) for tile   in self.tiles]
		[enermy.render(self.frame, self.camera) for enermy in self.enemies]

		# target & player
		self.target.render(self.frame, self.camera)
		self.player.render(self.frame, self.camera)

		# update window
		self.window.blit(pg.transform.scale(self.frame, self.windowSize), (0, 0))
		self.clock.tick(self.FPS)
		pg.display.flip()


	def update (self) :
		# camera & player
		self.camera.update()
		self.player.update(self.tiles)

		# enermy
		self.updateEnemies()

		# target
		self.target.update(self.player, self.targetPositions)


	def onStart (self) :
		# tiles
		self.tiles, self.targetPositions = self.core.loadLevel()

		# player & camera
		self.player = self.core.Player()
		self.camera = self.core.Camera(self.player)

		# enemies
		self.enemies = []
		self.enermySpawnCooldown = 0

		# background
		self.initBG()

		# target
		self.target = self.core.Target(choice(self.targetPositions))


if __name__ == '__main__' : Game().run()
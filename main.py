import pygame as pg
import random
import math
import core


class Game :
	def __init__(self) :
		# config
		self.windowSize  = (800, 800)
		self.renderScale = (400, 400)
		self.title = 'They are falling from above!'
		self.FPS = 60

		# initialize window
		self.window = pg.display.set_mode(self.windowSize)
		self.frame  = pg.Surface(self.renderScale)
		self.clock  = pg.time.Clock()

		pg.display.set_caption(self.title)

		# initialize core components
		self.core = core

	def run(self) :
		self.onStart()

		self.running = True
		while self.running :
			for event in pg.event.get() :
				if event.type == pg.QUIT :
					self.running = False
			self.update()
			self.render()

	def initBG(self) :
		self.bg = pg.image.load('assets/bg.png').convert()
		self.bgSpeed = 0.5
		self.bgBlocks = []
		self.bgSpawnCooldown = 128 - self.bgSpeed

		for y in range(12) :
			for x in range(12) :
				self.bgBlocks.append([[64 * x - self.bgSpeed, 64 * y - self.bgSpeed]])

	def renderBG(self) :
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

	def updateEnemies(self):
		toRemove = []
		for enemy in self.enemies:
			enemy.update(self.tiles, self.player)
			if enemy.deathAnim < 1:
				toRemove.append(enemy)

		for enemy in toRemove:
			self.enemies.remove(enemy)

		if self.enemySpawnCooldown > 32 and not self.player.dead:
			self.enemies.append(self.core.enemy())
			self.enemySpawnCooldown = 0

		if not self.player.dead: 
			self.enemySpawnCooldown += 1

	def updateScore (self):
		if self.player.score > self.hiScore:
			self.hiScoreDisplaySize = 10
			self.hiScore = self.player.score

		if self.player.dead:
			self.font0 = pg.Font('assets/pixel.otf', 40)
		if self.player.dead:
			self.font1 = pg.Font('assets/pixel.otf', 20)

		if not self.player.dead:
			color = (255, 255, 255)
		else : color = (251, 242, 54)

		self.scoreText = self.font0.render(f'score: {self.player.score}', False, color)
		self.scoreTextShadow = self.font0.render(f'score: {self.player.score}', False, (34, 32, 52))

		self.hiScoreText = self.font1.render(f'hi score: {self.hiScore}', False, color)
		self.hiScoreTextShadow = self.font1.render(f'hi score: {self.hiScore}', False, (34, 32, 52))

	def renderScore (self) :
		# text
		txt_width = self.scoreText.get_width()
		txt_height = self.scoreText.get_height()
		img = pg.transform.rotate( pg.transform.scale( self.scoreText, ( txt_width + self.scoreDisplaySize, txt_height + self.scoreDisplaySize )),	math.sin(self.scoreAnim) * 5)

		# shadow
		shadow = pg.transform.rotate(
			pg.transform.scale(
				self.scoreTextShadow,
				(
					self.scoreTextShadow.get_width() + self.scoreDisplaySize,
					self.scoreTextShadow.get_height() + self.scoreDisplaySize
				)),
			math.sin(self.scoreAnim) * 5)

		# text
		hiImg = pg.transform.rotate(
			pg.transform.scale(
				self.hiScoreText,
				(
					self.hiScoreText.get_width () + self.hiScoreDisplaySize,
					self.hiScoreText.get_height() + self.hiScoreDisplaySize
				)),
			math.sin(self.scoreAnim) * 5)

		# shadow
		hiShadow = pg.transform.rotate(
			pg.transform.scale(
				self.hiScoreTextShadow,
				(
					self.hiScoreTextShadow.get_width() + self.hiScoreDisplaySize,
					self.hiScoreTextShadow.get_height() + self.hiScoreDisplaySize
				)),
			math.sin(self.scoreAnim) * 5)
		
		# score
		self.frame.blit(
			shadow,
			(
				200 - (shadow.get_width () * 0.5) + 2,
				50 - (shadow.get_height() * 0.5) + 2
			))

		self.frame.blit(
			img,
			(
				200 - (img.get_width () * 0.5),
				50 - (img.get_height() * 0.5)
			))

		# high score
		self.frame.blit(
			hiShadow,
			(
				200 - (hiShadow.get_width () * 0.5) + 2,
				100 - (hiShadow.get_height() * 0.5) + 2
			))

		self.frame.blit(
			hiImg,
			(
				200 - (hiImg.get_width () * 0.5),
				100 - (hiImg.get_height() * 0.5)
			))

		# update animations
		self.scoreAnim += 0.1
		if self.scoreAnim >= 6.28 : self.scoreAnim = 0
		self.scoreDisplaySize *= 0.8
		self.hiScoreDisplaySize *= 0.8


	def render (self) :
		# clear frame
		self.frame.fill((0, 0, 0))

		# background
		self.renderBG()

		# level & enemies
		[tile  .render(self.frame, self.camera) for tile   in self.tiles]
		[enemy.render(self.frame, self.camera) for enemy in self.enemies]

		# target & player
		self.target.render(self.frame, self.camera)
		self.player.render(self.frame, self.camera)

		# score display
		self.renderScore()

		# update window
		self.window.blit(pg.transform.scale(self.frame, self.windowSize), (0, 0))
		self.clock.tick(self.FPS)
		pg.display.flip()


	def update (self) :
		# camera & player
		self.camera.update()
		self.player.update(self.tiles)

		# enemy
		self.updateEnemies()

		# target
		self.target.update(self.player, self.targetPositions, self.updateScore, self)

		if self.player.dead and self.state == 'gameplay':
			self.state = 'dead'
			self.updateScore()
			self.core.writeToJSON('score.save', {'score': self.hiScore})

		if self.player.pos[1] > 400:
			self.player.dead = True

	def onStart (self) :
		self.tiles, self.targetPositions = self.core.loadLevel()
		self.player = self.core.Player()
		self.camera = self.core.Camera(self.player)
		self.enemies = []
		self.enemySpawnCooldown = 0
		self.initBG()
		self.target = self.core.Target(random.choice(self.targetPositions))

		# score counter
		self.scoreAnim = 0
		self.scoreDisplaySize = 0
		self.hiScoreDisplaySize = 0

		self.font0 = pg.font.Font('assets/pixel.otf', 20)
		self.font1 = pg.font.Font('assets/pixel.otf', 10)

		self.hiScore = self.core.loadFromJSON('score.save')['score']
		self.updateScore()

		pg.mixer.music.load('assets/music/music.ogg')
		pg.mixer.music.set_volume(0.2)
		pg.mixer.music.play(-1)
		self.state = 'gameplay'


if __name__ == '__main__':
	pg.mixer.init()
	pg.font.init()
	pg.init()
	Game().run()
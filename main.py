import pygame as pg
import random
import core


class Game:
	def __init__(self):
		self.windowSize = (800, 800)
		self.renderScale = (400, 400)
		self.title = 'They are falling from above!'
		self.FPS = 60
		self.enemies = []
		self.enemySpawnCooldown = 0

		# initialize window
		self.window = pg.display.set_mode(self.windowSize)
		self.frame_surface = pg.Surface(self.renderScale)
		self.clock = pg.time.Clock()

		self.core = core
		self.level_generator = self.core.LevelGenerator()
		self.level_map = self.level_generator.get_map_classic()
		self.tiles, self.targetPositions = self.loadLevel(self.level_map)
		self.player = self.core.Player()
		self.score_board = self.core.ScoreBoard(self.player)

		pg.display.set_caption(self.title)

	def loadLevel(self, level_map):
		tiles = []
		targetPos = []

		for y, line in enumerate(level_map):
			for x, char in enumerate(line):
				if char != ' ' and char != '.':
					tiles.append(self.core.Tile((x * self.core.constants.TILE_SIZE, y * self.core.constants.TILE_SIZE),))
				elif char == '.':
					targetPos.append([x * self.core.constants.TILE_SIZE, y * self.core.constants.TILE_SIZE],)

		return tiles, targetPos

	def onStart(self):
		self.camera = self.core.Camera(self.player)
		self.background = self.core.Background()
		self.target = self.core.Target(random.choice(self.targetPositions))
		self.score_board.update()
		pg.mixer.music.load('assets/music/music.ogg')
		pg.mixer.music.set_volume(0.2)
		pg.mixer.music.play(-1)

	def run(self):
		self.onStart()
		self.running = True
		while self.running:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
			self.update()
			self.render()

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

	def render(self):
		# clear frame
		self.frame_surface.fill((0, 0, 0))
		self.background.render(self.frame_surface)

		# level & enemies
		for tile in self.tiles:
			tile.render(self.frame_surface, self.camera)
		for enemy in self.enemies:
			enemy.render(self.frame_surface, self.camera)

		self.target.render(self.frame_surface, self.camera)
		self.player.render(self.frame_surface, self.camera)

		self.score_board.render(self.frame_surface)

		# update window
		self.window.blit(pg.transform.scale(self.frame_surface, self.windowSize), (0, 0))
		self.clock.tick(self.FPS)
		pg.display.flip()

	def update(self):
		self.camera.update()
		# this also handles input
		self.player.update(self.tiles)
		self.updateEnemies()
		self.target.update(self.player, self.targetPositions, self.score_board.update, self)

		if self.player.dead:
			self.score_board.update()
			self.core.writeToJSON('score.save', {'score': self.score_board.high_score})

		if self.player.pos[1] > 400:
			self.player.dead = True


if __name__ == '__main__':
	pg.mixer.init()
	pg.font.init()
	pg.init()
	Game().run()
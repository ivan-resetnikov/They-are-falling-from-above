class Camera :
	def __init__ (self, target) :
		self.pos = [0, 0]

		self.target = target


	def update (self) :
		self.pos[0] = (self.target.pos[0] - 200 + 8 - self.pos[0]) * 0.1
		self.pos[1] = (self.target.pos[1] - 200 + 8 - self.pos[1]) * 0.1
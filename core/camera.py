import random 


class Camera :
	def __init__ (self, target) :
		self.pos = [0, 0]
		self.target = target
		self.screenShake = 0

	def update (self) :
		self.pos[0] = (self.target.pos[0] - 200 + 8 - self.pos[0]) * 0.1 + random.uniform(-self.screenShake, self.screenShake)
		self.pos[1] = (self.target.pos[1] - 200 + 8 - self.pos[1]) * 0.1 + random.uniform(-self.screenShake, self.screenShake)
		self.screenShake *= 0.8
import pygame as pg



def loadSound (path:str, vol:float=0.15) :
	sound = pg.mixer.Sound('assets/sounds/' + path)
	sound.set_volume(vol)
	return sound


Sounds = {
	'player' : {
		'jump'  : loadSound('jump.wav'),
		'score' : loadSound('score.wav'),
		'death' : loadSound('death.wav')
	}
}
import pygame as pg


def loadSound (path:str, vol:float=0.25) :
	sound = pg.mixer.Sound('assets/sounds/' + path)
	sound.set_volume(vol)
	return sound


SOUNDS = {
	'player' : {
		'jump'  : loadSound('jump.wav'),
		'score' : loadSound('score.wav'),
		'death' : loadSound('death.wav', 2)
	},
	'enermy' : {
		'death' : loadSound('hit.wav', 0.5)
	}
}
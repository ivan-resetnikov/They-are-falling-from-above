import pygame as pg
from .player import Player
import math
from .file import loadFromJSON

class ScoreBoard:
  def __init__(self, player: Player):
    self.player = player
    self.font0 = pg.font.Font('assets/pixel.otf', 20)
    self.font1 = pg.font.Font('assets/pixel.otf', 10)
    self.scoreDisplaySize = 0
    self.high_score_display_size = 0
    self.scoreAnim = 0
    self.high_score = loadFromJSON('score.save')['score']

  def update(self):
    if self.player.score > self.high_score:
      self.high_score_display_size = 10
      self.high_score = self.player.score

    if self.player.dead:
      color = (251, 242, 54)
    else:
      color = (255, 255, 255)

    self.scoreText = self.font0.render(f'score: {self.player.score}', False, color)
    self.scoreTextShadow = self.font0.render(f'score: {self.player.score}', False, (34, 32, 52))

    self.high_scoreText = self.font1.render(f'hi score: {self.high_score}', False, color)
    self.high_scoreTextShadow = self.font1.render(f'hi score: {self.high_score}', False,(34, 32, 52))

  def render(self, blit_surface: pg.Surface):
    # text
    txt_width = self.scoreText.get_width()
    txt_height = self.scoreText.get_height()
    img = pg.transform.rotate( pg.transform.scale( self.scoreText, ( txt_width + self.scoreDisplaySize, txt_height + self.scoreDisplaySize )),	math.sin(self.scoreAnim) * 5)
    # shadow
    shadow = pg.transform.rotate( pg.transform.scale( self.scoreTextShadow,	( self.scoreTextShadow.get_width() + self.scoreDisplaySize, self.scoreTextShadow.get_height() + self.scoreDisplaySize )), math.sin(self.scoreAnim) * 5)
    # text
    hiImg = pg.transform.rotate( pg.transform.scale( self.high_scoreText, ( self.high_scoreText.get_width () + self.high_score_display_size, self.high_scoreText.get_height() + self.high_score_display_size )), math.sin(self.scoreAnim) * 5)
    # shadow
    hiShadow = pg.transform.rotate( pg.transform.scale( self.high_scoreTextShadow, ( self.high_scoreTextShadow.get_width() + self.high_score_display_size, self.high_scoreTextShadow.get_height() + self.high_score_display_size	)), math.sin(self.scoreAnim) * 5)
    # score
    blit_surface.blit( shadow, ( 200 - (shadow.get_width () * 0.5) + 2, 50 - (shadow.get_height() * 0.5) + 2 ))
    blit_surface.blit( img, ( 200 - (img.get_width () * 0.5), 50 - (img.get_height() * 0.5) ))
    # high score
    blit_surface.blit( hiShadow, ( 200 - (hiShadow.get_width () * 0.5) + 2, 100 - (hiShadow.get_height() * 0.5) + 2 ))
    blit_surface.blit( hiImg, ( 200 - (hiImg.get_width () * 0.5), 100 - (hiImg.get_height() * 0.5) ))
    # update animations
    self.scoreAnim += 0.1
    if self.scoreAnim >= 6.28: 
      self.scoreAnim = 0
    self.scoreDisplaySize *= 0.8
    self.high_score_display_size *= 0.8
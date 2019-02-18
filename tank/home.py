#coding: utf-8
__author__ = 'gold'
__date__ = '2019/2/17'
__time__ = '21:37'
__filename__ = 'home.py'

import pygame
from tank.constants import WINDOWWIDTH,PANEL_BOTTOM


''' the base camp class'''
class Home(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.homes = ['./images/home/home1.png', './images/home/home2.png', './images/home/home_destroyed.png']
		self.home = pygame.image.load(self.homes[0])
		self.rect = self.home.get_rect()

		# bottom is to calculate the home's position,replace it with new function.
		# self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
		self.rect.center = (WINDOWWIDTH // 2,PANEL_BOTTOM - self.rect.height // 2)
		self.alive = True

	def set_dead(self):
		'''
		this function is used to set the home to dead state
		:return:
		'''
		self.home = pygame.image.load(self.homes[-1])
		self.alive = False
#coding: utf-8
__author__ = 'gold'
__date__ = '2019/2/17'
__time__ = '21:39'
__filename__ = 'bullet.py'

'''
this file contains the bullet class
'''

import pygame
from tank.constants import WINDOWHEIGHT,WINDOWWIDTH,PANEL_LEFT,PANEL_RIGHT,PANEL_TOP,PANEL_BOTTOM

class Bullet(pygame.sprite.Sprite):
	'''
	the bullet class,any time only one bullet for the player can appear on the board,not very good.
	'''
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		#all 4 possible bullet-shape images
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']

		#the bullet direction,and set the default direction to the up
		self.direction_x, self.direction_y = 0, -1

		#load the bullet image
		self.bullet = pygame.image.load(self.bullets[0])

		#get the bullet rectange
		self.rect = self.bullet.get_rect()

		#set the bullet rect's left and right position,but why the right is 0?
		self.rect.left, self.rect.right = 0, 0

		#the speed of the bullet
		self.speed = 6

		# if the bullet can appear on the board.
		self.being = False

		#a enforced bullet which can break down the metal bricks
		self.stronger = False

	def turn(self, direction_x, direction_y):
		'''
		this function is used to show the bullet on the board.
		:param direction_x: int,
		:param direction_y: int
		:return: None
		'''
		self.direction_x, self.direction_y = direction_x, direction_y

		#the below part does loading an image from documents according to the bullet directions
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.')

	def move(self):
		'''
		move the bullet
		:return: None
		'''

		#so the Rect object has a move function to change its position
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		#parameters in above function are offset,not new position.

		#after reaching the edge of the map, then the bullet disapper.
		#but this function is not good as the edge pos are fixed, i will solve the problem
		if (self.rect.top < PANEL_TOP) or (self.rect.bottom > PANEL_BOTTOM - PANEL_TOP) or (self.rect.left < PANEL_LEFT) or (self.rect.right > PANEL_RIGHT - PANEL_LEFT):
			self.being = False
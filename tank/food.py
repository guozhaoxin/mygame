#coding: utf-8
__author__ = 'gold'
__date__ = '2019/2/17'
__time__ = '21:39'
__filename__ = 'food.py'


import pygame
import random

'''
food class,if the player capture,it will get some special skill for a given duration time.
'''
class Food(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		#kill all enemies
		self.food_boom = './images/food/food_boom.png'

		#make all enemies static for a while
		self.food_clock = './images/food/food_clock.png'

		#asign the bullet the strengthen to break down the steal brick
		self.food_gun = './images/food/food_gun.png'

		#make the base camp harder with steal brick
		# self.food_iron = './images/food/food_gun.png'
		self.food_iron = './images/food/food_iron.png'

		#give a cover to the tank for a while
		self.food_protect = './images/food/food_protect.png'

		#upgrade the tank
		self.food_star = './images/food/food_star.png'

		#increase the life count of tank by 1
		self.food_tank = './images/food/food_tank.png'

		#all food list
		self.foods = [self.food_boom, self.food_clock, self.food_gun, self.food_iron, self.food_protect, self.food_star, self.food_tank]
		self.kind = None
		self.food = None
		self.rect = None

		#judge if the food exists
		self.being = False

		#the food's life time,but what is the unit?
		# TODO
		self.time = 1000


	def generate(self,x_start = 10,x_end = 500,y_start = 100,y_end = 500):
		'''
		generate the food
		:return:
		'''
		# self.kind = random.randint(0, len(self.foods) + 1)
		self.kind = random.randint(0, len(self.foods) - 1)
		self.food = pygame.image.load(self.foods[self.kind]).convert_alpha()
		self.rect = self.food.get_rect()

		# the bottom is not very reasonable,you must exclude the home area.
		# TODO
		self.rect.left, self.rect.top = random.randint(x_start, x_end), random.randint(y_start, y_end)

		self.being = True
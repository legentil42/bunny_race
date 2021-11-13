import math
import pygame
import random
from math import *
import sys
from pygame.locals import *
pygame.init()
go_sound = pygame.mixer.Sound("go.wav")
from heli_class import ALTITUDE
class Cross:
    #VERIFIER QUE LA CROSS EST VALIDE ET SI OUI:
    instances = []
    
    width,height = 80,40
    cross_sprite = pygame.image.load('sprites/heli/cross.png')
    cross_sprite = pygame.transform.scale(cross_sprite, (width, height))
    
    def __init__(self,x,y):
        if True:

            self.x = x
            self.y = y
            self.exist = True
            self.__class__.instances.append(self)

    def draw_cross(self,screen):
        print(self.exist)
        if self.exist == True:
            screen.blit(self.__class__.cross_sprite, (self.x-self.__class__.width/2,self.y-self.__class__.height))
       # screen.blit(textsurface,(self.x-self.__class__.width/8,self.y+self.__class__.height/2))
        #print(self.x,self.y)

    def check_if_remove(self,player):
        pos_ombre_x =  player.x
        pos_ombre_y = ALTITUDE + player.y
        if sqrt((pos_ombre_x-self.x)**2 + (pos_ombre_y-self.y)**2)<=10 and self.exist == True and player.x_goal == self.x and player.y_goal == self.y - ALTITUDE:
            self.exist = False
            print("cross removed")
           
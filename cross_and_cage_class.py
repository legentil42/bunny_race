import math
import pygame
import random
from math import *
import sys
from pygame.locals import *
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
go_sound = pygame.mixer.Sound(resource_path("sounds/go.wav"))
ALTITUDE = 200
SKEW = 30
class Cross:
    #VERIFIER QUE LA CROSS EST VALIDE ET SI OUI:
    instances = []
    
    width,height = 80,40
    cross_sprite = pygame.image.load(resource_path('sprites/heli/cross.png'))
    cross_sprite = pygame.transform.scale(cross_sprite, (width, height))
    
    def __init__(self,x,y):
        if True:

            self.x = x
            self.y = y
            self.exist = True
            self.__class__.instances.append(self)

    def draw_cross(self,screen):
        
        if self.exist == True:
            screen.blit(self.__class__.cross_sprite, (self.x-self.__class__.width/2,self.y-self.__class__.height))
       # screen.blit(textsurface,(self.x-self.__class__.width/8,self.y+self.__class__.height/2))


    def check_if_remove(self,player,time_elapsed):
        pos_ombre_x =  player.x
        pos_ombre_y = ALTITUDE + player.y
        if sqrt((pos_ombre_x-self.x)**2 + (pos_ombre_y-self.y)**2)<=10 and self.exist == True and player.x_goal == self.x and player.y_goal == self.y - ALTITUDE:
            self.exist = False
            
            if player.N_cages >0:
                Cage(pos_ombre_x,pos_ombre_y)
                player.N_cages -= 1
                player.lastecart = SKEW  * cos(5*time_elapsed)
            del self.__class__.instances[self.__class__.instances.index(self)]

            
           



class Cage:
    #VERIFIER QUE LA CROSS EST VALIDE ET SI OUI:
    instances = []
    
    width,height = 100,100
    cage_sprite = pygame.image.load(resource_path('sprites/heli/cage.png'))
    cage_sprite = pygame.transform.scale(cage_sprite, (width, height))
    
    def __init__(self,x,y):
        if True:

            self.x = x
            self.y = y-ALTITUDE
            self.goal_y = y
            self.falling = True
            self.empty = True
            self.__class__.instances.append(self)

    def draw_cage(self,screen):
        if self.empty == True:
            screen.blit(self.__class__.cage_sprite, (self.x-self.__class__.width/2,self.y-self.__class__.height))


    def check_if_remove(self,bunny,player):
        pos_bunny_x =  bunny.x
        pos_bunny_y = bunny.y
        if sqrt((pos_bunny_x-self.x)**2 + (pos_bunny_y-self.y+self.__class__.height/2)**2)<=50 and self.empty == True and self.falling == False and bunny.caged == False:
            self.empty = False
            
            del self.__class__.instances[self.__class__.instances.index(self)]
            bunny.caged = True
            bunny.x = self.x
            bunny.y = self.y-self.__class__.height/2
            player.N_captured += 1

    def update_pos(self):
        if self.y >=self.goal_y:
            self.falling = False
        if self.falling == True:
            self.y += 10


class River:
    #VERIFIER QUE LA CROSS EST VALIDE ET SI OUI:
    instances = []
    
    width,height = 1700,100
    river_sprite = pygame.image.load(resource_path('sprites/river/eau _qui_coule.png'))
    river_sprite = pygame.transform.scale(river_sprite, (width, height))
    
    def __init__(self):
        if True:

            self.x = -1700+800
            self.y = 0

            self.__class__.instances.append(self)

    def draw_river(self,screen):
        self.x += 5
        if self.x>0:
            self.x = -1700+800
        screen.blit(self.__class__.river_sprite, (self.x,self.y))


class HP_bar:
    #VERIFIER QUE LA CROSS EST VALIDE ET SI OUI:
    instances = []
    
    width,height = 80,40
    states_sprites = []

    states_sprites.append(pygame.image.load(resource_path('sprites/HP_green.png')))
    states_sprites.append(pygame.image.load(resource_path('sprites/HP_yellow.png')))
    states_sprites.append(pygame.image.load(resource_path('sprites/HP_red.png')))
    states_sprites.append(pygame.image.load(resource_path('sprites/HP_black.png')))


    for liste in [states_sprites]:
        for image in liste:
            liste[liste.index(image)] = pygame.transform.scale(image, (width, height))
    
    def __init__(self):
        if True:

            self.x = 110
            self.y = 0
            self.HP = 0
            self.sprite = self.__class__.states_sprites[self.HP]
            self.__class__.instances.append(self)

    def draw_health(self,screen):
        self.sprite = self.__class__.states_sprites[self.HP]
        screen.blit(self.sprite, (self.x,self.y))
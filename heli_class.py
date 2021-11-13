import math
import pygame
import random
from math import *
import sys
from pygame.locals import *
from cross_and_cage_class import Cross
pygame.init()
go_sound = pygame.mixer.Sound("go.wav")
SKEW = 2
ALTITUDE = 200
RANDOM_COUNTER_MAX = 400
HELI_SPEDD = 200
class Heli:
    width,height = 100,100
    instances = []
    sprites_g = []
    hover_animation_speed = 0.5
    sprites_g.append(pygame.image.load('sprites/heli/H1g.png'))
    sprites_g.append(pygame.image.load('sprites/heli/H2g.png'))
    sprites_d = []
    sprites_d.append(pygame.image.load('sprites/heli/H1d.png'))
    sprites_d.append(pygame.image.load('sprites/heli/H2d.png'))

    ombre = pygame.image.load('sprites/heli/ombre.png')
    ombre = pygame.transform.scale(ombre, (width, height/3))
    for liste in [sprites_d,sprites_g]:
        for image in liste:
            liste[liste.index(image)] = pygame.transform.scale(image, (width, height))

    def __init__(self):
        self.__class__.instances.append(self)
        #traits :

        self.x = 300
        self.y = 200
        self.speed = HELI_SPEDD
        self.new_x=self.x
        self.new_y =self.y
        self.x_goal=self.x
        self.y_goal =self.y
        self.current_sprite = 0
        self.current_dir = "droite"
        self.image = self.__class__.sprites_d[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
        self.drop = False
        self.dead = False
        self.moving = False
        self.already_deleted_cross = False
        self.random_counter = RANDOM_COUNTER_MAX


    def waypoint(self):
        #("new waypoint") ajouter marqueur
        self.moving = True
        self.new_x,self.new_y = pygame.mouse.get_pos()
        self.new_y -= ALTITUDE - self.__class__.height/3
        self.random_counter = RANDOM_COUNTER_MAX
        pygame.mixer.Sound.play(go_sound)


        if len(Cross.instances)>0:
                self.x_goal = Cross.instances[0].x
                self.y_goal = Cross.instances[0].y - ALTITUDE
        

    def update(self,dt):
        if self.dead == False: 

            if self.moving == True: # tout le temps sinon?

                if self.x_goal < self.x:
                    self.current_dir = "gauche"
                else: 
                    self.current_dir = "droite"

                self.angle = math.atan2(self.y_goal-self.y,self.x_goal-self.x)

                if sqrt((self.x-self.x_goal)**2 + (self.y-self.y_goal)**2)>5:
                    if self.random_counter > 0:
                        x_random = random.randint(-SKEW,SKEW)
                        y_random = random.randint(-SKEW,SKEW)
                        self.random_counter -= abs(x_random)+abs(y_random)
                    else :
                        x_random = 0
                        y_random = 0

                    x_parcouru = cos(self.angle)*self.speed*dt + x_random
                    y_parcouru = sin(self.angle)*self.speed*dt + y_random
                    self.x = self.x +  x_parcouru
                    self.y = self.y + y_parcouru
                    
                else:
                    print("cross ateinte")

                
                if self.current_dir == "droite":
                    self.current_sprite += self.__class__.hover_animation_speed
                    if self.current_sprite >= len(self.__class__.sprites_d):
                        self.current_sprite = 0
                    self.image = self.__class__.sprites_d[int(self.current_sprite)]
                elif self.current_dir == "gauche":
                    self.current_sprite += self.__class__.hover_animation_speed
                    if self.current_sprite >= len(self.__class__.sprites_g):
                        self.current_sprite = 0
                    self.image = self.__class__.sprites_g[int(self.current_sprite)]
        
        if self.dead == True:
            pass #A FAIRE
            
    def draw_ombre(self,screen):
        screen.blit(self.__class__.ombre, (self.x-self.__class__.width/2,ALTITUDE + self.y-self.__class__.height/2))
        


    def draw_heli(self,screen,font):
        # txt_a_afficher = str(round(self.speed,1))+","+ str(round(self.wander_dist_coef,2))+","+str(round(self.wander_proba,2))
            
        # textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
        screen.blit(self.image, (self.x-self.__class__.width/2,self.y-self.__class__.height/2))
       # screen.blit(textsurface,(self.x-self.__class__.width/8,self.y+self.__class__.height/2))
        #print(self.x,self.y)

import pygame
import random
from math import *
import sys
from pygame.locals import *
TAUX_MUTATION_GLOBAL = 0.2 #pourcentage
NB_LAPIN = 10
TAUX_VAINQUEURS = 0.5
pygame.init()
jump_sound = pygame.mixer.Sound("jump.wav")
finish_sound = pygame.mixer.Sound("finish.wav")
death_sound = pygame.mixer.Sound("death.wav")

def random_dir(wave,x=None):
    bias = wave/10
    print(bias)
    k = (1-bias)**3
    if x == None:
        x = random.random()
    if x < 0.5:
        x = 2*x
        return 2*pi*(x*k)/(x*k-x+1)
    else:
        x = 2-2*x
        return 2*pi*(x*k)/(x*k-x+1)
class Bunny:

    
    width,height = 100,100
    instances = []
    sprites_g = []
    jump_animation_speed = 0.5
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_0.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_1.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_2.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_3.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_4.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_5.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_6.png'))
    sprites_g.append(pygame.image.load('sprites/bunny/bunny_g/frame_7.png'))

    sprites_d = []
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_0.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_1.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_2.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_3.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_4.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_5.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_6.png'))
    sprites_d.append(pygame.image.load('sprites/bunny/bunny_d/frame_7.png'))

    sprites_dead_d = []
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_0.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_1.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_2.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_3.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_4.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_5.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_6.png'))
    sprites_dead_d.append(pygame.image.load('sprites/bunny/dead_d/frame_7.png'))

    sprites_caged = []
    sprites_caged.append(pygame.image.load('sprites/bunny/caged_1.png'))
    sprites_caged.append(pygame.image.load('sprites/bunny/caged_2.png'))

    for liste in [sprites_d,sprites_dead_d,sprites_g,sprites_caged]:
        for image in liste:
            liste[liste.index(image)] = pygame.transform.scale(image, (width, height))


    def __init__(self,wave,desired_y = None):
        self.__class__.instances.append(self)
        #traits :
        
        self.speed = 200
        self.wander_dist_coef = 1
        self.wander_proba = 0.10

        self.x = 0
        if desired_y != None:
            self.y = desired_y
        else:
            self.y = random.randint(50,550)
        
        self.new_x=self.x
        self.new_y =self.y
        self.wander_dist = 200*self.wander_dist_coef
        self.is_wandering = False
        self.current_sprite = 0
        self.current_dir = "gauche"
        self.image = self.__class__.sprites_g[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
        self.jump_animation = False
        self.caged = False
        self.caged_timer = 0
        self.wave = wave

    def new_x_et_y(self):
        self.new_angle = random_dir(self.wave)

        self.new_dist = self.wander_dist*random.random()
        self.new_x = cos(self.new_angle)*self.new_dist+self.x
        self.new_y = sin(self.new_angle)*self.new_dist+self.y
        if self.new_x < self.x:
            self.current_dir = "gauche"
        else: 
            self.current_dir = "droite"

    def waypoint(self):
        #("new waypoint")
        self.jump_animation = True
        self.new_x_et_y()
        while self.new_x <= 0 or self.new_y >= 600 or self.new_y <= 110:
            self.new_x_et_y()

        pygame.mixer.Sound.set_volume(jump_sound,0.2)
        pygame.mixer.Sound.play(jump_sound)
        self.is_wandering = True

    def update(self,dt):
        if self.caged == False:
            if self.is_wandering:
                if sqrt((self.x-self.new_x)**2 + (self.y-self.new_y)**2)>20:
                    x_parcouru = cos(self.new_angle)*self.speed*dt
                    y_parcouru = sin(self.new_angle)*self.speed*dt
                    self.x = self.x +  x_parcouru
                    self.y = self.y + y_parcouru
                    
                else:
                    self.is_wandering = False
                    self.jump_animation = False
            
            else:
                if random.random() < self.wander_proba:
                    self.waypoint()

            if self.jump_animation == True:
                if self.current_dir == "droite":
                    self.current_sprite += self.__class__.jump_animation_speed
                    if self.current_sprite >= len(self.__class__.sprites_d):
                        self.current_sprite = 0
                    self.image = self.__class__.sprites_d[int(self.current_sprite)]
                elif self.current_dir == "gauche":
                    self.current_sprite += self.__class__.jump_animation_speed
                    if self.current_sprite >= len(self.__class__.sprites_g):
                        self.current_sprite = 0
                    self.image = self.__class__.sprites_g[int(self.current_sprite)]
            else:
                self.current_sprite = 0
                if self.current_dir == "droite":
                    self.image = self.__class__.sprites_d[self.current_sprite]
                
                elif self.current_dir == "gauche":
                    self.image = self.__class__.sprites_g[self.current_sprite]
        
        if self.caged == True:
            self.jump_animation = False
            self.caged_timer += dt
            if self.current_sprite < len(self.__class__.sprites_caged)-0.05:
                self.current_sprite += 0.05
            else:
                self.current_sprite = 0
            self.image = self.__class__.sprites_caged[int(self.current_sprite)]
            

    def draw_bunny(self,screen,font):
        # txt_a_afficher = str(round(self.speed,1))+","+ str(round(self.wander_dist_coef,2))+","+str(round(self.wander_proba,2))
        if self.caged_timer<5:
        # textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
            screen.blit(self.image, (self.x-self.__class__.width/2,self.y-self.__class__.height/2))
        else:
            del self.__class__.instances[self.__class__.instances.index(self)]
        # screen.blit(textsurface,(self.x-self.__class__.width/8,self.y+self.__class__.height/2))
        

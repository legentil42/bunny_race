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

def random_dir():
    bias = 0.1
    k = (1-bias)**3
    x = random.random()
    if x < 0.5:
        x = 2*x
        return 2*pi*(x*k)/(x*k-x+1)
    else:
        x = -2*x
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


    def __init__(self,parent1=None,parent2=None,desired_y = None,copied_bunny = None):
        self.__class__.instances.append(self)
        #traits :
        if parent1 == None:
            self.speed = 200
            self.wander_dist_coef = 1
            self.wander_proba = 0.10
            
        else:
            #decendance
            r1,r2,r3 = random.random(),random.random(),random.random()
            self.speed = parent1.speed *r1 + parent2.speed *(1-r1)
            self.wander_dist_coef = parent1.wander_dist_coef *r2 + parent2.wander_dist_coef *(1-r2)
            self.wander_proba = parent1.wander_proba *r3 + parent2.wander_proba *(1-r3)
            
            #mutation
            self.speed += self.speed * (2*random.random()-1) *TAUX_MUTATION_GLOBAL
            self.wander_dist_coef += self.wander_dist_coef * (2*random.random()-1) *TAUX_MUTATION_GLOBAL
            self.wander_proba += self.wander_proba * (2*random.random()-1) *TAUX_MUTATION_GLOBAL

            if self.speed < 0:
                self.speed = 1
            if self.wander_dist_coef < 0 :
                self.wander_dist_coef = 0.01
            if self.wander_proba < 0:
                self.wander_proba = 0.01

        self.x = 0
        if desired_y != None:
            self.y = desired_y
        else:
            self.y = random.randint(50,550)
        
        if copied_bunny != None:
            self.speed = copied_bunny.speed
            self.wander_dist_coef = copied_bunny.wander_dist_coef
            self.wander_proba = copied_bunny.wander_proba

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
        

    def new_x_et_y(self):
        self.new_angle = random_dir()

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
                    #print(sqrt((self.x-self.new_x)**2 + (self.y-self.new_y)**2))
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
        # screen.blit(textsurface,(self.x-self.__class__.width/8,self.y+self.__class__.height/2))
        #print(self.x,self.y)

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


from cross_and_cage_class import ALTITUDE
TAUX_MUTATION_GLOBAL = 0.2 #pourcentage
NB_LAPIN = 10
TAUX_VAINQUEURS = 0.5
pygame.init()
jump_sound = pygame.mixer.Sound(resource_path("sounds/jump.wav"))
finish_sound = pygame.mixer.Sound(resource_path("sounds/finish.wav"))
death_sound = pygame.mixer.Sound(resource_path("sounds/death.wav"))

def random_dir(bias,x=None):

    print(bias)
    k = (1-bias)**3
    if x == None:
        x = random.random()
    if x < 0.5:
        x = 2*x
        return -(2*pi*(x*k)/(x*k-x+1))
    else:
        x = 2-2*x
        return -(2*pi*(x*k)/(x*k-x+1))

class Bunny:
   
    pygame.display.set_mode((800, 600))
    
    width,height = 100,100
    instances = []
    sprites_g = []
    jump_animation_speed = 0.5
    sprites_white_g = []
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_0.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_1.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_2.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_3.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_4.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_5.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_6.png')))
    sprites_white_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_7.png')))

    sprites_blue_g = []
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_0.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_1.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_2.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_3.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_4.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_5.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_6.png')))
    sprites_blue_g.append(pygame.image.load(resource_path('sprites/bunny/bunny_g/frame_7.png')))


    for sprite in sprites_blue_g:
        sprite.fill((0, 0, 255, 255), special_flags=pygame.BLEND_MULT)

    sprites_g.append(sprites_white_g)
    sprites_g.append(sprites_blue_g)


    sprites_d = []
    sprites_white_d = []
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_0.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_1.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_2.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_3.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_4.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_5.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_6.png')))
    sprites_white_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_7.png')))
    
    sprites_blue_d = []
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_0.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_1.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_2.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_3.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_4.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_5.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_6.png')))
    sprites_blue_d.append(pygame.image.load(resource_path('sprites/bunny/bunny_d/frame_7.png')))


    sprites_d.append(sprites_white_d)
    eclair_width = 15
    L_zap_sprites = []
    L_zap_sprites.append(pygame.image.load(resource_path('sprites/bunny/eclair_1.png')))
    L_zap_sprites.append(pygame.image.load(resource_path('sprites/bunny/eclair_2.png')))


    
    # for image in L_zap_sprites:
    #     L_zap_sprites[L_zap_sprites.index(image)] = pygame.transform.scale(image, (eclair_width, ALTITUDE/2))


    for sprite in sprites_blue_d:
        sprite.fill((0, 0, 255, 255), special_flags=pygame.BLEND_MULT)

    sprites_d.append(sprites_blue_d)


    sprites_caged = [[],[]]
    sprites_caged[0].append(pygame.image.load(resource_path('sprites/bunny/caged_1.png')))
    sprites_caged[0].append(pygame.image.load(resource_path('sprites/bunny/caged_2.png')))


    sprites_caged[1].append(pygame.image.load(resource_path('sprites/bunny/caged_1_blue.png')))
    sprites_caged[1].append(pygame.image.load(resource_path('sprites/bunny/caged_2_blue.png')))

    for liste in [sprites_d[0],sprites_g[0],sprites_d[1],sprites_g[1],sprites_caged[0],sprites_caged[1]]:
        for image in liste:
            liste[liste.index(image)] = pygame.transform.scale(image, (width, height))


    def __init__(self,desired_color,wave,bias,desired_y = None):
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
        self.bias = bias
        self.new_x=self.x
        self.new_y =self.y
        self.color = desired_color #0 : white, 1 : blue, 2 : red
        self.wander_dist = 200*self.wander_dist_coef
        self.is_wandering = False
        self.current_sprite = 0
        self.current_dir = "gauche"
        self.image = self.__class__.sprites_g[self.color][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x,self.y]
        self.jump_animation = False
        self.caged = False
        self.caged_timer = 0
        self.wave = wave
        self.using_storm = False
        self.time_started_storm = 0
        self.used_zap = False
        self.zap_sprite_number = 0
        self.zap_sprite = self.__class__.L_zap_sprites[self.zap_sprite_number]


    def new_x_et_y(self):
        self.new_angle = random_dir(self.bias)

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

    def update(self,dt,time_elapsed,player):
        if self.caged == False :
            if self.is_wandering and self.using_storm == False:
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

            if self.using_storm == True:
                self.zap_sprite_number += 0.1
                if self.zap_sprite_number >= 2:
                    self.zap_sprite_number = 0
                self.zap_sprite = self.__class__.L_zap_sprites[int(self.zap_sprite_number)]


            if time_elapsed-self.time_started_storm > 2 and self.using_storm == True:
                self.using_storm = False
                player.zapped = False
                self.color = 0


            if self.jump_animation == True:
                if self.current_dir == "droite":
                    self.current_sprite += self.__class__.jump_animation_speed
                    if self.current_sprite >= len(self.__class__.sprites_d[self.color]):
                        self.current_sprite = 0
                    self.image = self.__class__.sprites_d[self.color][int(self.current_sprite)]
                elif self.current_dir == "gauche":
                    self.current_sprite += self.__class__.jump_animation_speed
                    if self.current_sprite >= len(self.__class__.sprites_g[self.color]):
                        self.current_sprite = 0
                    self.image = self.__class__.sprites_g[self.color][int(self.current_sprite)]
            else:
                self.current_sprite = 0
                if self.current_dir == "droite":
                    self.image = self.__class__.sprites_d[self.color][self.current_sprite]
                
                elif self.current_dir == "gauche":
                    self.image = self.__class__.sprites_g[self.color][self.current_sprite]
        
        if self.caged == True:
            if self.using_storm == True:
                player.zapped = False
            self.using_storm == False
            self.jump_animation = False
            self.caged_timer += dt
            if self.current_sprite < len(self.__class__.sprites_caged[self.color])-0.05:
                self.current_sprite += 0.05
            else:
                self.current_sprite = 0
            self.image = self.__class__.sprites_caged[self.color][int(self.current_sprite)]
            

    def draw_bunny(self,screen,font,player):
        # txt_a_afficher = str(round(self.speed,1))+","+ str(round(self.wander_dist_coef,2))+","+str(round(self.wander_proba,2))
        if self.caged_timer<5:
        # textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
            screen.blit(self.image, (self.x-self.__class__.width/2,self.y-self.__class__.height/2))
        else:
            del self.__class__.instances[self.__class__.instances.index(self)]
        if self.using_storm == True and self.caged == False:
            screen.blit(self.zap_sprite, (player.x+25-player.__class__.width/2,player.y-player.__class__.height/2))

        # screen.blit(textsurface,(self.x-self.__class__.width/8,self.y+self.__class__.height/2))
        

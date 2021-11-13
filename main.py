#%%

from bunny_class import *
from heli_class import *
from cross_and_cage_class import *

import importlib
import bunny_class
import heli_class
import cross_and_cage_class
importlib.reload(bunny_class)
importlib.reload(heli_class)
importlib.reload(cross_and_cage_class)
from bunny_class import *
from heli_class import *
from cross_and_cage_class import *
import numpy as np
import matplotlib.pyplot as plt
BLUE = [0,0,255]


def generate_x_bunnies(nb_bun):
    Bunny.instances = []
    L_des_Y = np.linspace(1,450,nb_bun)
    for i in range(nb_bun):
        if i ==0:
            P1 = Bunny(desired_y=L_des_Y[nb_bun-i-1])
        else:
            Bunny(P1,P1,desired_y=L_des_Y[nb_bun-i-1])


def find_first_cross(player):
    one_cross_exist = False
    for cross in Cross.instances:
        if cross.exist == True:
            player.moving = True
            one_cross_exist = True
            player.x_goal = Cross.instances[Cross.instances.index(cross)].x
            player.y_goal = Cross.instances[Cross.instances.index(cross)].y - ALTITUDE
            break
    if one_cross_exist == False:
        player.moving = False



def main_loop():
    # for instance in Cross.instances:
    #     del instance
    
    Cross.instances = []

    generate_x_bunnies(NB_LAPIN)

    Heli.instances = []

    player = Heli()

    bunnies_order = []
    time_elapsed = 0
    sim_finished = False


    fps = 60
    dt = 1/fps
    fpsClock = pygame.time.Clock()
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    img_fond = pygame.image.load('fond.png')

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', int(Bunny.height/7))

    # Game loop
    while len(bunnies_order)<NB_LAPIN:

    #input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  #CLIC GAUCHE
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    print("Left Mouse key was clicked")

                    player.waypoint()
                    Cross(player.new_x,player.new_y+ALTITUDE)




        find_first_cross(player)
        print(player.x_goal,player.y_goal,len(Cross.instances),player.moving)

    # Update.
        if len(bunnies_order)>=TAUX_VAINQUEURS*NB_LAPIN and sim_finished == False:
            sim_finished = True
            for bunny in Bunny.instances:
                bunny.current_sprite = 0
                bunny.dead = True
            pygame.mixer.Sound.play(death_sound)
                
    # Draw.
        screen.blit(img_fond, (0,0))
        player.draw_ombre(screen)

        for cross in Cross.instances:
            cross.check_if_remove(player)
            cross.draw_cross(screen)


        for bunny in Bunny.instances:
            if sim_finished == False:

                if bunny not in [i[0] for i in bunnies_order]:
                    bunny.update(dt)
                    bunny.draw_bunny(screen,font)
                    if bunny.x > 780:
                        pygame.mixer.Sound.play(finish_sound)
                        bunnies_order.append([bunny,time_elapsed])
                        Bunny.instances.pop(Bunny.instances.index(bunny))
                        del bunny
            
            else:
                bunny.update(dt)
                bunny.draw_bunny(screen,font)
        player.update(dt)
        player.draw_heli(screen,font)
        if sim_finished == True:      
            for bunny in Bunny.instances: 
                if bunny.current_sprite >= len(bunny.__class__.sprites_dead_d)-1:
                        pygame.quit()
                        return bunnies_order


        pygame.display.flip()
        dt = fpsClock.tick(fps)/1000
        time_elapsed += dt


  



# %%

# %%

# %%

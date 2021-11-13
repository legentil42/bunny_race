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
from cross_and_cage_class import Cage,River
import numpy as np
import matplotlib.pyplot as plt
BLUE = [0,0,255]


def adapted_y_to_print(item):
    if item.__class__ == Bunny:
        return item.y-Bunny.height/2
    if item.__class__ == Cage:
        return item.y

def generate_x_bunnies(nb_bun):
    
    L_des_Y = np.linspace(110,550,nb_bun)
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
    last_check = 0
    Cross.instances = []
    River.instances = []
    Bunny.instances = []
    generate_x_bunnies(NB_LAPIN)
    
    Heli.instances = []

    player = Heli()
    river = River()
    bunnies_order = []
    time_elapsed = 0
    sim_finished = False

    L_ordre_print = []
    fps = 60
    dt = 1/fps
    fpsClock = pygame.time.Clock()
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    img_fond = pygame.image.load('sprites/river/fond_trans.png')
    img_HUD = pygame.image.load('sprites/hud.png')
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

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
                    _,test_y = pygame.mouse.get_pos()
                    if test_y <110:
                        pygame.mixer.Sound.play(wrong_sound)
                    else:
                        player.waypoint()
                        Cross(player.new_x,player.new_y+ALTITUDE)


        find_first_cross(player)
        # print(player.x_goal,player.y_goal,len(Cross.instances),player.moving)

    # Update.
        if len(bunnies_order)>=TAUX_VAINQUEURS*NB_LAPIN and sim_finished == False:
            sim_finished = True
            for bunny in Bunny.instances:
                bunny.current_sprite = 0
                bunny.dead = True
            pygame.mixer.Sound.play(death_sound)
                
    # Draw.
        river.draw_river(screen)
        screen.blit(img_fond, (0,0))
        player.draw_ombre(screen)

        for cross in Cross.instances:
            cross.check_if_remove(player)
            cross.draw_cross(screen)

        L_ordre_print = []
        for cage in Cage.instances:
            cage.update_pos()
            for bunny in Bunny.instances:
                cage.check_if_remove(bunny)
            if cage.empty == True:
                L_ordre_print.append(cage)
        
        
        

        
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
                L_ordre_print.append(bunny)
                



        L_ordre_print = sorted(L_ordre_print,key = lambda x : adapted_y_to_print(x))

        for i in range(len(L_ordre_print)):
            if L_ordre_print[i].__class__ == Bunny:
                L_ordre_print[i].draw_bunny(screen,font)
            elif L_ordre_print[i].__class__ == Cage:
                L_ordre_print[i].draw_cage(screen)
        

        player.update(dt,time_elapsed)
        player.draw_heli(screen,font)
        if sim_finished == True:      
            for bunny in Bunny.instances: 
                if bunny.current_sprite >= len(bunny.__class__.sprites_dead_d)-1:
                        pygame.quit()
                        return bunnies_order

        screen.blit(img_HUD, (0,0))
        txt_a_afficher = str(player.N_cages) + " x"
        
        textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
        screen.blit(textsurface,(100,40))

        pygame.display.flip()
        dt = fpsClock.tick(fps)/1000
        time_elapsed += dt

        if time_elapsed-last_check > 10:
            generate_x_bunnies(10)
            player.N_cages += 10 
            last_check = time_elapsed
  




# %%

# %%

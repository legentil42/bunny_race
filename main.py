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
heli_sound = pygame.mixer.Sound("helisound.wav")
bg_music = pygame.mixer.Sound("POL-star-way-short.wav")
def adapted_y_to_print(item):
    if item.__class__ == Bunny:
        return item.y-Bunny.height/2
    if item.__class__ == Cage:
        return item.y

def generate_x_bunnies(nb_bun,bunny_wave):
    
    L_des_Y = np.linspace(110,550,nb_bun)
    for i in range(nb_bun):
        if i ==0:
            P1 = Bunny(bunny_wave,desired_y=L_des_Y[nb_bun-i-1])
        else:
            Bunny(bunny_wave,desired_y=L_des_Y[nb_bun-i-1])


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
    
    pygame.mixer.Sound.play(bg_music,-1)
    last_check_respawn = 0
    Cross.instances = []
    River.instances = []
    Bunny.instances = []
    generate_x_bunnies(NB_LAPIN,1)
    
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
    img_fond = pygame.image.load('sprites/river/fond_complet.png')
    img_HUD = pygame.image.load('sprites/hud.png')
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    game_started = False
    game_starting = False
    x_screen = -800
    bunny_wave = 0
    # Game loop
    while True: #len(bunnies_order)<NB_LAPIN
        if game_started == False:


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and game_starting == False:  #CLIC GAUCHE
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        
                        game_starting = True
                        
                        pygame.mixer.Sound.play(heli_sound)

            river.draw_river(screen)
            screen.blit(img_fond, (x_screen,0))

            if game_starting == False:
                player.x = 577
                player.y = 468
                player.draw_heli(screen,font)

            if game_starting == True:
                if player.y > 300:
                    player.y -= 2
                else:
                    player.x -= 1
                    x_screen += 5
                player.update(0,0)
                player.draw_heli(screen,font)
            if x_screen > 0:
                x_screen = 0
                game_started = True
            pygame.display.flip()
            dt = fpsClock.tick(fps)/1000

        if game_started == True:
        #input
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  #CLIC GAUCHE
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        
                        _,test_y = pygame.mouse.get_pos()
                        if test_y <100:
                            pygame.mixer.Sound.play(wrong_sound)
                        else:
                            player.waypoint()
                            Cross(player.new_x,player.new_y+ALTITUDE)


            find_first_cross(player)
            

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

            if time_elapsed-last_check_respawn > 10:
                generate_x_bunnies(10,bunny_wave)
                player.N_cages += 10 
                last_check_respawn = time_elapsed
                bunny_wave += 1
        
        print(len(Bunny.instances),len(Cage.instances),len(Cross.instances))

  




# %%
L_x = np.linspace(0,1,1000)
L_y = [random_dir(x) for x in L_x]
plt.plot(L_x,L_y)
plt.show()
# %%

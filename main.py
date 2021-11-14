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
from cross_and_cage_class import Cage,River,HP_bar
import numpy as np
import matplotlib.pyplot as plt
WAVES = [[5,0.1,1],
            [5,0.2,1],
            [5,0.4,2],
            [6,0.4,2],
            [7,0.4,4],
            [8,0.6,4],
            [9,0.6,4],
            [10,0.6,5],
            [15,0.7,5],
            [15,0.9,8]] #nb bunny, biais, dont electriques

def adapted_y_to_print(item):
    if item.__class__ == Bunny:
        return item.y-Bunny.height/2
    if item.__class__ == Cage:
        return item.y

def generate_x_bunnies(bunny_wave):
    nb_bun = WAVES[bunny_wave][0]
    bias = WAVES[bunny_wave][1]
    nb_bleu = WAVES[bunny_wave][2]
    print(nb_bun,bias,nb_bleu)
    L_des_Y = list(np.linspace(110,550,nb_bun))
    random.shuffle(L_des_Y)
    for i in range(nb_bun):
        if i < nb_bleu:
            Bunny(1,bunny_wave,bias,desired_y=L_des_Y[nb_bun-i-1])
        else:
            Bunny(0,bunny_wave,bias,desired_y=L_des_Y[nb_bun-i-1])


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
    pygame.init()

    

    # for instance in Cross.instances:
    #     del instance
    BLUE = [0,0,255]
    heli_sound = pygame.mixer.Sound("helisound.wav")
    bg_music = pygame.mixer.Sound("music.mp3")
    pygame.mixer.Sound.set_volume(bg_music,0.2)
    pygame.mixer.Sound.set_volume(heli_sound,0.4)
    pygame.mixer.Sound.play(bg_music,-1)
    last_check_respawn = 0
    Cross.instances = []
    Cage.instances = []
    River.instances = []
    Bunny.instances = []
    HP_bar.instances = []
    generate_x_bunnies(0)
    
    Heli.instances = []
    hp_bar = HP_bar()
    player = Heli()
    player.N_cages = WAVES[0][0]+1
    river = River()
    bunnies_order = []
    time_elapsed = 0
    sim_finished = False
    restart_game = False
    game_won = False

    L_ordre_print = []
    fps = 60
    dt = 1/fps
    fpsClock = pygame.time.Clock()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    img_fond = pygame.image.load('sprites/river/fond_complet.png')
    img_HUD = pygame.image.load('sprites/hud.png')
    img_HUD_2 = pygame.image.load('sprites/hud_2.png')
    img_game_over = pygame.image.load('sprites/game_over.png')
    img_game_won = pygame.image.load('sprites/game_won.png')

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    game_started = False
    game_starting = False
    x_screen = -800
    bunny_wave = 1
    # Game loop
    while restart_game == False: #len(bunnies_order)<NB_LAPIN
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
                    player.draw_ombre(screen)
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
                        if sim_finished == False:
                            _,test_y = pygame.mouse.get_pos()
                            if test_y <100:
                                pygame.mixer.Sound.play(wrong_sound)
                            else:
                                player.waypoint()
                                Cross(player.new_x,player.new_y+ALTITUDE)
                        else:
                            restart_game = True #redemarer le jeu


            find_first_cross(player)
            

            # Update.
            if hp_bar.HP >=3 and sim_finished == False:
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
                cross.check_if_remove(player,time_elapsed)
                cross.draw_cross(screen)

            L_ordre_print = []
            for cage in Cage.instances:
                cage.update_pos()
                for bunny in Bunny.instances:
                    cage.check_if_remove(bunny,player)
                if cage.empty == True:
                    L_ordre_print.append(cage)
            
            
            

            
            for bunny in Bunny.instances:
                if sim_finished == False:
                    
                    if bunny not in [i[0] for i in bunnies_order]:
                        bunny.update(dt,time_elapsed,player)
                        is_bunny_under_heli(bunny,player,time_elapsed)
                        bunny.draw_bunny(screen,font,player)

                        if bunny.x > 780:
                            pygame.mixer.Sound.play(finish_sound)
                            bunnies_order.append([bunny,time_elapsed])
                            Bunny.instances.pop(Bunny.instances.index(bunny))
                            del bunny
                            hp_bar.HP += 1
                
                else:
                    
                    bunny.update(dt,time_elapsed,player)
                    L_ordre_print.append(bunny)
                    



            L_ordre_print = sorted(L_ordre_print,key = lambda x : adapted_y_to_print(x))

            for i in range(len(L_ordre_print)):
                if L_ordre_print[i].__class__ == Bunny:
                    L_ordre_print[i].draw_bunny(screen,font,player)
                elif L_ordre_print[i].__class__ == Cage:
                    L_ordre_print[i].draw_cage(screen)
            

            player.update(dt,time_elapsed)
            player.draw_heli(screen,font)

            if sim_finished == True:
                if game_won == True: 
                    screen.blit(img_game_won,(27,142))  
                else:
                    screen.blit(img_game_over,(27,142))     
                # pygame.quit()
                # return bunnies_order

            screen.blit(img_HUD, (0,0))
            screen.blit(img_HUD_2, (600,0))
            hp_bar.draw_health(screen)
            txt_a_afficher = str(player.N_cages) + " x"
            
            textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
            screen.blit(textsurface,(100,40))

            txt_a_afficher = str(bunny_wave) + "/10"
            textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
            screen.blit(textsurface,(740,5))


            txt_a_afficher = str(player.N_captured)
            textsurface = font.render(txt_a_afficher, False, (0, 0, 0))
            screen.blit(textsurface,(760,41))



            pygame.display.flip()
            dt = fpsClock.tick(fps)/1000
            time_elapsed += dt

            if time_elapsed-last_check_respawn > 10 and  sim_finished == False and bunny_wave<=9:
                bunny_wave += 1
                generate_x_bunnies(bunny_wave)
                player.N_cages += WAVES[bunny_wave][0]+1
                last_check_respawn = time_elapsed
                
            if bunny_wave == 10 and sim_finished == False:
                free_bunny = False
                for bunny in Bunny.instances:
                    if bunny.caged == False:
                        free_bunny = True
                if free_bunny == False:
                    game_won = True
                    sim_finished = True

    pygame.quit()   
    main_loop()

main_loop()

# %%
L_x = np.linspace(0,1,1000)
L_y = [random_dir(1,x) for x in L_x]
plt.plot(L_x,L_y)
plt.show()
# %%

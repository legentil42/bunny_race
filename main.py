#%%

from bunny_class import *

import importlib
import bunny_class
importlib.reload(bunny_class)
from bunny_class import *
import numpy as np

BLUE = [0,0,255]


def generate_x_bunnies(nb_bun):
    L_des_Y = np.linspace(1,450,nb_bun)
    for i in range(nb_bun):
        if i ==0:
            P1 = Bunny(desired_y=L_des_Y[nb_bun-i-1])
        else:
            Bunny(P1,P1,desired_y=L_des_Y[nb_bun-i-1])





def generation():

    Bunny.instances = []
    generate_x_bunnies(NB_LAPIN)
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
    font = pygame.font.SysFont('Comic Sans MS', 30)

    # Game loop
    while len(bunnies_order)<NB_LAPIN:

    #input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for bunny in Bunny.instances:
                    del bunny
                Bunny.instances = []
                generate_x_bunnies(NB_LAPIN)
                bunnies_order = []
                time_elapsed = 0
                sim_finished = False
    
    # Update.
        if len(bunnies_order)>=TAUX_VAINQUEURS*NB_LAPIN and sim_finished == False:
            sim_finished = True
            for bunny in Bunny.instances:
                bunny.current_sprite = 0
                bunny.dead = True
            pygame.mixer.Sound.play(death_sound)
                
    # Draw.
        screen.blit(img_fond, (0,0))
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


        pygame.display.flip()
        dt = fpsClock.tick(fps)/1000
        time_elapsed += dt
    pygame.quit()
    return bunnies_order



generation()
# %%

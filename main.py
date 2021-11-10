#%%

from bunny_class import *

import importlib
import bunny_class
importlib.reload(bunny_class)
from bunny_class import *
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





def generation():

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
            # if event.type == pygame.MOUSEBUTTONUP:
            #     for bunny in Bunny.instances:
            #         del bunny
            #     generate_x_bunnies(NB_LAPIN)
            #     bunnies_order = []
            #     time_elapsed = 0
            #     sim_finished = False
    
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

        if sim_finished == True:      
            for bunny in Bunny.instances: 
                if bunny.current_sprite >= len(bunny.__class__.sprites_dead_d)-1:
                        pygame.quit()
                        return bunnies_order


        pygame.display.flip()
        dt = fpsClock.tick(fps)/1000
        time_elapsed += dt









def create_new_bunny_generation(best_from_last):
    Bunny.instances = []
    Bunny(copied_bunny=best_from_last[0][0])
    while len(Bunny.instances)< NB_LAPIN:
        i = random.randint(0,len(best_from_last)-1)
        j = random.randint(0,len(best_from_last)-1)
        Bunny(best_from_last[i][0],best_from_last[j][0])
        
    reasign_y_pos()

def reasign_y_pos():
    L_des_Y = np.linspace(1,450,NB_LAPIN)
    
    for i in range(len(Bunny.instances)):
        Bunny.instances[i].y = L_des_Y[i]


def do_x_generation(nb_gene):
    L_time = []
    L_mean_speed = []
    L_mean_wander_dist = []
    L_mean_wander_prob = []

    generate_x_bunnies(NB_LAPIN)
    
    for gene_i in range(nb_gene):
        best_from_gene = generation()
        create_new_bunny_generation(best_from_gene)

        
        m1=0
        m2=0
        m3=0
        for bunny in Bunny.instances:
            m1 += bunny.speed
            m2 += bunny.wander_dist_coef
            m3 += bunny.wander_proba

        L_time.append(best_from_gene[0][1])
        L_mean_speed.append(m1/NB_LAPIN)
        L_mean_wander_dist.append(m2/NB_LAPIN)
        L_mean_wander_prob.append(m3/NB_LAPIN)

    plt.scatter(list(range(nb_gene)),L_time)
    plt.plot(list(range(nb_gene)),L_time)
    plt.title("best time")
    plt.show()

    plt.scatter(list(range(nb_gene)),L_mean_speed)
    plt.plot(list(range(nb_gene)),L_mean_speed)
    plt.title("L_mean_speed")
    plt.show()

    plt.scatter(list(range(nb_gene)),L_mean_wander_dist)
    plt.plot(list(range(nb_gene)),L_mean_wander_dist)
    plt.title("L_mean_wander_dist")
    plt.show()

    plt.scatter(list(range(nb_gene)),L_mean_wander_prob)
    plt.plot(list(range(nb_gene)),L_mean_wander_prob)
    plt.title("L_mean_wander_prob")
    plt.show()


# %%

# %%

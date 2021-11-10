#%%

from bunny_class import *

import importlib
import bunny_class
importlib.reload(bunny_class)
from bunny_class import *
import numpy as np

BLUE = [0,0,255]



Bunny.instances = []



 
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

fps = 60
dt = 1/fps
fpsClock = pygame.time.Clock()
 
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
img_fond = pygame.image.load('fond.png')


def generate_x_bunnies(nb_bun):
    L_des_Y = np.linspace(1,450,nb_bun)
    for i in range(nb_bun):
        if i ==0:
            P1 = Bunny(desired_y=L_des_Y[nb_bun-i-1])
        else:
            Bunny(P1,P1,desired_y=L_des_Y[nb_bun-i-1])

generate_x_bunnies(5)
# Game loop.
while True:

  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            for bunny in Bunny.instances:
                del bunny
            Bunny.instances = []
            generate_x_bunnies(5)
  
  # Update.
  
  # Draw.
    screen.blit(img_fond, (0,0))
    for bunny in Bunny.instances: 
        bunny.update(dt)
        bunny.draw_bunny(screen,font)


    pygame.display.flip()
    dt = fpsClock.tick(fps)/1000

# %%

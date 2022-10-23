import pygame 
from SimulationClasses import *
import sys

pygame.init()

from SimulationClasses import *

screen = None
clock = pygame.time.Clock()

def read_scenario(file_path:str):
    global screen
    with open(file_path,"r") as f:

        lines = f.readlines()

        screen_height = int(lines[0])
        height = int(lines[1])
        

        pedestrians = lines[2][:-1]
        pedestrians = pedestrians.split(" ")
        pedestrians = [pedestrian[1:-1].split(",") for pedestrian in pedestrians]
        for i in range(len(pedestrians)):
            pedestrians[i] = [int(x) for x in pedestrians[i]]
        print(pedestrians)
        targets = lines[3][:-1]
        targets = targets.split(" ")
        targets = [target[1:-1].split(",") for target in targets]
        for i in range(len(targets)):
            targets[i] = [int(x) for x in targets[i]]

        try: 
            obstacles = lines[4][:-1]
            obstacles = obstacles.split(" ")
        except Exception: obstacles = [] 
        obstacles = [obstacle[1:-1].split(",") for obstacle in obstacles]
        for i in range(len(obstacles)):
            obstacles[i] = [int(x) for x in obstacles[i]]

        screen = pygame.display.set_mode((screen_height,screen_height))               
        ps = []
        obs = []
    

        for i in pedestrians:
            ps.append(Cell(i[0],i[1],Type.PEDESTRIAN,screen_height//height,screen))
        
        for i in targets:
            t = Cell(i[0],i[1],Type.TARGET,screen_height//height,screen)

        for i in obstacles:
            obs.append(Cell(i[0],i[1],Type.OBSTACLE,screen_height//height,screen))

        return ps, t, obs

    




ps, t, obs = read_scenario("Exercise 1/scen1.scn")



while not ps[0].check_collision(t):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    screen.fill((0,0,0))

    for p in ps:
        p.draw()
    
    t.draw()
    
    for o in obs:
        o.draw()

    pygame.display.update()
    clock.tick(10)
    
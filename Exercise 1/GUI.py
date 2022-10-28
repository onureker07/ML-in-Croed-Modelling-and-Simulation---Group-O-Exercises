import pygame
from torch import randint 
from SimulationClasses import *
from random import randint, choice
import sys

pygame.init()

screen = None
clock = pygame.time.Clock()
number_of_cell = 0
simulation_world = World()


def read_scenario(file_path:str):
    global number_of_cell
    global screen, simulation_world
    with open(file_path,"r") as f:

        lines = f.readlines()

        screen_height = int(lines[0])
        height = int(lines[1])
        number_of_cell = height
        Cell.edge = height

        pedestrians = lines[2][:-1]
        pedestrians = pedestrians.split(" ")
        pedestrians = [pedestrian[1:-1].split(",") for pedestrian in pedestrians]
        for i in range(len(pedestrians)):
            pedestrians[i] = [int(x) for x in pedestrians[i]]

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
            obstacles[i] = (int(obstacles[i][0]),int(obstacles[i][1]))
        obstacles = list(set(obstacles))

        screen = pygame.display.set_mode((screen_height,screen_height))               
        ps = []
        obs = []
    
        id = 1
        for i in pedestrians:
            temp_cell = Cell(i[0],i[1],Type.PEDESTRIAN,screen_height//height,screen,id,randint(4,80),choice([Sex.FEMALE,Sex.FEMALE]))
            ps.append(temp_cell)
            simulation_world.add_cell(temp_cell)
        
        for i in targets:
            t = Cell(i[0],i[1],Type.TARGET,screen_height//height,screen)
            simulation_world.add_cell(t)

        for i in obstacles:
            temp_cell = Cell(i[0],i[1],Type.OBSTACLE,screen_height//height,screen)
            obs.append(temp_cell)
            simulation_world.add_cell(temp_cell)

        return ps, t, obs

    




ps, t, obs = read_scenario("Exercise 1/scen1.scn")



optimal_paths = {}
for p in ps:
    optimal_path = []
    current = (t.x, t.y)
    dijkstra = p.dijkstra(number_of_cell) 
    optimal_path.append(current)
    while current != (p.x,p.y):
        optimal_path.insert(0,dijkstra[current])
        current = dijkstra[current]

    optimal_paths[p] = optimal_path[1:]


frame_count = 0
to_start = False
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if i.type == pygame.MOUSEBUTTONUP:
            to_start = not to_start

    frame_count+=1
    screen.fill((0,0,0))

    if to_start:
        for p in ps:
            try:
                to_move = abs(p.x - optimal_paths[p][0][0]) + abs(p.y - optimal_paths[p][0][1])
                speed = p.person.speed if to_move == 1 else p.person.speed/1.4
                frame_to_move = round(1/speed *  100) #FPS
                if frame_count!=0 and frame_count%frame_to_move==0:
                    p.move(optimal_paths[p][0][0],optimal_paths[p][0][1])
                    del optimal_paths[p][0]

            except: pass
        

    for p in ps:
        p.draw()

    t.draw()
    for o in obs:
        o.draw()

    pygame.display.update()
    clock.tick(100)
    
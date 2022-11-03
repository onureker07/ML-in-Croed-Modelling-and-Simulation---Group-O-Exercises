import pygame
import sys
from random import randint, choice, random
from math import ceil

from SimulationClasses import *

"""
This module is respınsble for reading scenario and implementation of simulation loop.
Python Version: 3.9
"""


"""
Below is initializations needed for simulation.
screen and number_of_cell is not assigned and yet to assigned later. It is here to make it global variable.
Clock variable is used for fixed FPS.
"""
pygame.init()
screen = None
clock = pygame.time.Clock()
number_of_cell = 0
simulation_world = World()


def read_scenario(file_path:str) -> tuple[list[Cell], Cell, list[Cell]]: 
    """A function that reads .scn file and creates simulation participants

    Args:
        file_path (str): Relative or absolute path of .scn file

    Returns:
        list[Cell]: Pedestrians created as a list of Cell objects
        Cell: Target created as a Cell object
        list[Cell]: Obstacles created as a list of Cell objects
    """
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
            temp_cell = Cell(i[0],i[1],Type.PEDESTRIAN,screen_height//height,screen,id,randint(4,80),choice([Sex.FEMALE,Sex.MALE]),random()*0.5+3)
            ps.append(temp_cell)
            simulation_world.add_cell(temp_cell)
            id+=1
        
        for i in targets:
            t = Cell(i[0],i[1],Type.TARGET,screen_height//height,screen)
            simulation_world.add_cell(t)

        for i in obstacles:
            temp_cell = Cell(i[0],i[1],Type.OBSTACLE,screen_height//height,screen)
            obs.append(temp_cell)
            simulation_world.add_cell(temp_cell)

    return ps, t, obs

    

ps, t, obs = read_scenario("Exercise 1\\Scenarios\\"+input()) #The file path that is wanted to simulate 


"""
optimal_paths contains the data of the path that djikstra algorithm return for every pedestrian.
Below is the initialization of optimal_paths variable.
"""
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

"""
working_frame(int): Frame count while simulation is working. It is needed to move pedestrians according to their speed.
to_start(bool): Whether simulation is working or paused at the moment
average_speed, average_travel_speed, distances: These three variables calculates the data to verbose for RiMEA Test 4.
"""
working_frame = 0
to_start = False
average_speed = 0
average_travel_speed = 0
distances = {per:0 for per in ps}

#Simulation Loop
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:#Quitting of application window
            #print("Average speed:", average_speed/24) #Verbose for RiMEA Test 4
            #print("Average travel speed:", average_travel_speed/24)
            pygame.quit()
            sys.exit()

        if i.type == pygame.MOUSEBUTTONUP:#Changing of to_start variable when mouse is clicked
            to_start = not to_start

    screen.fill((0,0,0)) #Screen is filled black for empty cells

    if not ps: to_start = False #When there is no pedestrians to move, simulation stops

    if to_start: #If the simulation is working...
        for p in ps:
            try:
                to_move = abs(p.x - optimal_paths[p][0][0]) + abs(p.y - optimal_paths[p][0][1]) #Diagonal or Straight
                speed = p.person.speed if to_move == 1 else p.person.speed/1.4 #Multiply speed with 1.4 (sqrt(2)) if move is diagonal
                frame_to_move = ceil(1/speed *  100) #Number of frames to move pedestrians according to their speed

                if working_frame!=0 and working_frame%frame_to_move==0:#For every frame_to_move time steps, move the pedestrian.
                    #distances[p] += 1 if to_move==1 else 1.4 #Needed for verbose
                    if p.move(optimal_paths[p][0][0],optimal_paths[p][0][1]): #If move is successful, delete the coordinate from the path
                        del optimal_paths[p][0]

            except Exception as e: #When pedestrian reach target, remove (absorb) it.
                #print(e) #Verbose for exception
                #average_speed += p.person.speed #Needed for RiMEA Test 4 verbose
                #average_travel_speed += distances[p] / (working_frame/100)
                ps.remove(p)
                p.simulation_world.pedestrians.remove(p)
        
        working_frame += 1
        
    #Below is visualization of simulation
    for p in ps:
        p.draw()

    t.draw()
    for o in obs:
        o.draw()

    pygame.display.update()
    clock.tick(100) #FPS


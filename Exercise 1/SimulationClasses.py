from enum import Enum
import sys
from tkinter.messagebox import NO
import pygame

class Type(Enum):
    PEDESTRIAN = 1,
    OBSTACLE = 2,
    TARGET = 3
class Sex(Enum):
    MALE = 1,
    FEMALE = 2

class World:
    def __init__(self) -> None:
        self.pedestrians = []
        self.target = ()
        self.obstacles = []   

    def add_cell(self,cell):
        if cell.type == Type.PEDESTRIAN: self.pedestrians.append(cell)
        elif cell.type == Type.OBSTACLE: self.obstacles.append(cell)
        elif cell.type == Type.TARGET: self.target = cell

        cell.simulation_world = self

class Person():
    def __init__(self,ID,age,sex,speed=0) -> None:
        self.ID = ID
        self.age = age
        self.sex = sex
        if speed: self.speed = speed
        else:
            speed = -0.000001 * (age ** 4) + 0.0001912 * (age **3 ) - 0.0135042 * age * age + 0.384056 * age + 0.1792454
            if self.sex == Sex.MALE: self.speed = speed
            else: self.speed = speed * 0.9

class Cell:
    
    edge = 0

    def __init__(self,x:int,y:int,type:Type, size:int, screen, ID = 0, age = 0, sex = None):
        self.x = x
        self.y = y
        self.type = type
        self.size = size 
        self.screen = screen
        if self.type == Type.PEDESTRIAN:
            self.person = Person(ID,age,sex)

    def draw(self,):
        if self.type == Type.OBSTACLE:
            pygame.draw.rect(self.screen, (255,255,255), (self.x*self.size,self.y*self.size,self.size,self.size))
        elif self.type == Type.PEDESTRIAN:
            pygame.draw.rect(self.screen, (0,255,0), (self.x*self.size,self.y*self.size,self.size,self.size))
        elif self.type == Type.TARGET:
            pygame.draw.rect(self.screen, (255,0,0), (self.x*self.size,self.y*self.size,self.size,self.size))
        
    def move(self,x,y):
        if self.type != Type.PEDESTRIAN: raise Exception("Cells other than pedestrian cannot move")
        else:
            print("ID: ", self.person.ID, "Sex: ", self.person.sex,"Age: ",self.person.age,"Speed: ", self.person.speed ,"Move from ",(self.x,self.y)," to ", (x,y))
            if (x,y) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] or (x,y) not in [(pedestrian.x, pedestrian.y) for pedestrian in self.simulation_world.predestrians]:
                self.x = x
                self.y = y


    def check_collision(self,cell): 
        if self.x == cell.x and self.y == cell.y: return True
        return False
    
    def dijkstra(self,number_of_cell):
        distance = {}
        parent = {}
        all_cell = []
        
        #Listing all nodes
        for i in range(number_of_cell):
            for j in range(number_of_cell):
                all_cell.append((i,j))
                distance[(i,j)] = sys.maxsize
                parent[(i,j)] = None
            
        distance[(self.x,self.y)] = 0

        while all_cell:
            current = min(all_cell,key=distance.get)
            all_cell.remove(current)
            for neighbor, dist in self.neighbours(current[0],current[1]).items():
                cost = distance[current] + dist
                if cost < distance[neighbor]:
                    distance[neighbor] = cost
                    parent[neighbor] = current
        return parent






    def neighbours(self,x:int, y:int):
        neighs = {}
        #Up Down Right Left
        if x>0:
            neighs[(x-1,y)] = 1 if (x-1,y) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        if y>0:
            neighs[(x,y-1)] = 1 if (x,y-1) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        if y<Cell.edge-1:
            neighs[(x,y+1)] = 1 if (x,y+1) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        if x<Cell.edge-1:
            neighs[(x+1,y)] = 1 if (x+1,y) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        #Diagonals
        if x>0 and y>0:
            neighs[(x-1,y-1)] = 1.4 if (x-1,y-1) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        if y<Cell.edge-1 and x>0:
            neighs[(x-1,y+1)] = 1.4 if (x-1,y+1) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        
        if y>0 and x<Cell.edge-1:
            neighs[(x+1,y-1)] = 1.4 if (x+1,y-1) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize

        if x<Cell.edge-1 and y<Cell.edge-1:
            neighs[(x+1,y+1)] = 1.4 if (x+1,y+1) not in [(obstacle.x, obstacle.y) for obstacle in self.simulation_world.obstacles] else sys.maxsize
        return neighs
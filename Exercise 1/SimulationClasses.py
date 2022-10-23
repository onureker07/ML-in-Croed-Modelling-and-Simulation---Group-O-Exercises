from enum import Enum
from msilib.schema import Error
from matplotlib.sankey import UP

import pygame

class Type(Enum):
    EMPTY = 0,
    PEDESTRIAN = 1,
    OBSTACLE = 2,
    TARGET = 3



class Cell:
    def __init__(self,x:int,y:int,type:Type, size:int, screen):
        self.x = x
        self.y = y
        self.type = type
        self.size = size 
        self.screen = screen

    def draw(self,):
        if self.type == Type.OBSTACLE:
            pygame.draw.rect(self.screen, (255,255,255), (self.x*self.size,self.y*self.size,self.size,self.size))
        elif self.type == Type.PEDESTRIAN:
            pygame.draw.rect(self.screen, (0,255,0), (self.x*self.size,self.y*self.size,self.size*10,self.size*10))
        elif self.type == Type.TARGET:
            pygame.draw.rect(self.screen, (255,0,0), (self.x*self.size,self.y*self.size,self.size,self.size))
        
    def move(self,up,down,left,right):
        if self.type != Type.PEDESTRIAN: raise Error("Cells other than pedestrian cannot move")
        else: 
            if up: self.y -= 1
            if down: self.y += 1
            if left: self.x -= 1
            if right: self.x+=1

    def check_collision(self,cell): 
        if self.x == cell.x and self.y == cell.y: return True
        return False
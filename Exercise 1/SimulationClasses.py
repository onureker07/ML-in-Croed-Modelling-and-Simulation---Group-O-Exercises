from enum import Enum
import sys
import pygame

class Type(Enum):
    """
        Enumaration class for Cell Types
    """
    PEDESTRIAN = 1,
    OBSTACLE = 2,
    TARGET = 3

class Sex(Enum):
    """
        Enumaration class for the sex of the person
    """
    MALE = 1,
    FEMALE = 2

class Person():
    """This class keeps data about pedestrians.
    """
    def __init__(self,ID:int,age:int,sex:Sex,speed=0.0) -> None:
        """_summary_

        Args:
            ID (int): ID assigned for the person. ID is used for verbose
            age (int): Age of the person
            sex (Sex): Sex of the person
            speed (float): _description_. If no value is given, it will be calculated according to age.
        """
        self.ID = ID
        self.age = age
        self.sex = sex
        if speed: self.speed = speed
        else:
            speed = -0.000001 * (age ** 4) + 0.0001912 * (age **3 ) - 0.0135042 * age * age + 0.384056 * age + 0.1792454
            if self.sex == Sex.MALE: self.speed = speed
            else: self.speed = speed * 0.9

class Cell:
    """This class represents the Cell in the automaton.
    """
    edge = 0 #static value which represents the number of cell in the edge of the simulation world

    def __init__(self,x:int,y:int,type:Type, size:int, screen:pygame.Surface, ID = 0, age = 0, sex:Sex = None,speed=0) -> None:
        """Initalization of the Cell class

        Args:
            x (int): x coordinate of the Cell
            y (int): y coordinate of the Cell
            type (Type): Type of the cell, which is one of Pedestrian, Obstacle or Target
            size (int): Size of the cell
            screen (pygame.Surface): Screen that this cell is to be simulated in.
            ID (int): ID of the cell. It is neccassary only if the Cell contains pedestrian.
            age (int): Age of the cell. It is neccassary only if the Cell contains pedestrian.
            sex (Sex): Sex of the cell. It is neccassary only if the Cell contains pedestrian.
            speed (int): Speed of the cell. It is neccassary only if the Cell contains pedestrian.
        """
        self.x = x
        self.y = y
        self.type = type
        self.size = size 
        self.screen = screen
        if self.type == Type.PEDESTRIAN:
            self.person = Person(ID,age,sex,speed)

    def draw(self,)->None:
        """
        Visualization of the cell
        """
        if self.type == Type.OBSTACLE:
            pygame.draw.rect(self.screen, (255,255,255), (self.x*self.size,self.y*self.size,self.size,self.size))
        elif self.type == Type.PEDESTRIAN:
            pygame.draw.rect(self.screen, (0,255,0), (self.x*self.size,self.y*self.size,self.size,self.size))
        elif self.type == Type.TARGET:
            pygame.draw.rect(self.screen, (255,0,0), (self.x*self.size,self.y*self.size,self.size,self.size))
        
    def move(self,x:int,y:int)->bool:
        """Move function that functions only if the cell is Pedestrian

        Args:
            x (int): x coordinate to move
            y (int): y coordinate to move

        Raises:
            Exception: Exception is raised if Cell is not Pedestrian

        Returns:
            bool: whether move is successful
        """
        if self.type != Type.PEDESTRIAN: raise Exception("Cells other than pedestrian cannot move")
        else:
            #print("ID: ", self.person.ID, "Sex: ", self.person.sex,"Age: ",self.person.age,"Speed: ", self.person.speed ,"Move from ",(self.x,self.y)," to ", (x,y)) #Verbose
            if all([x != pedestrian.x or y!= pedestrian.y for pedestrian in self.simulation_world.pedestrians]) and all([x != obstacle.x or y!= obstacle.y for obstacle in self.simulation_world.obstacles]):
                self.x = x
                self.y = y
                return True
            else: 
                return False

    def check_collision(self,cell) -> bool:
        """Function that check collision between this cell and the cell given

        Args:
            cell (Cell): Cell to check collison with

        Returns:
            bool: Whether two cell is collide or not
        """
        if self.x == cell.x and self.y == cell.y: return True
        return False
    
    def dijkstra(self,number_of_cell:int) -> dict:
        """Classical Dijkstra algorithm that finds shortest path from the self to all other cell

        Args:
            number_of_cell (int): Number of cell

        Returns:
            dict: Mapping from cell coordinate to its parent's cell coordinate
        """
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

    def neighbours(self,x:int, y:int) -> dict:
        """A function that finds all possible neighbours of the corresponding coordinate

        Args:
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell

        Returns:
            dict: Keys are neighbouring coordinates and values are distances.
        """
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

class World:
    """This class is a container class that keeps data about simulations accordingly (pedestrians, target, obstacles).
    """
    def __init__(self) -> None:
        """Initialization function of the World
        """
        self.pedestrians = []
        self.target = ()
        self.obstacles = []   

    def add_cell(self,cell:Cell) -> None:
        """A function to add a cell to simulation world acordingly

        Args:
            cell (Cell): An object from Cell class to add 
        """
        if cell.type == Type.PEDESTRIAN: self.pedestrians.append(cell)
        elif cell.type == Type.OBSTACLE: self.obstacles.append(cell)
        elif cell.type == Type.TARGET: self.target = cell

        cell.simulation_world = self




    
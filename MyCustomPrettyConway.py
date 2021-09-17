from functools import lru_cache, wraps,reduce
import time
from typing import Callable, Set, Tuple
import sys
#import threading
from TestArrayUICreator import MakeTestCaseForConway
from enum import Enum
import os
import json
def make_chunks(array,num_of_chunks): 
    """>>> for strings:
     f"{sep}".join(string[i:i+at_each] for i in range(starting_from, len(string), +at_each)) """
    for ix in range(0,len(array),num_of_chunks):
        yield array[ix:ix+num_of_chunks]

def DefaultObjectMethod(DOC=True,DEBUG=False):#TODO generalization and debugging
    def DefaultObjectMethod_decorator(func):#! THIS IS CALLED A CLOSURE
        @wraps(func) #*avoid getting some attributes overriden!
        def func_wrapper(*args,**kwargs):

            if DOC:#!print DOCSTRING
                print(func.__doc__,end="\n\n") 

            return func(*args,**kwargs)

        return func_wrapper #?default
    return DefaultObjectMethod_decorator

print("\n")
#*Rules:
#* Underpopulation; 1. Any live cell with less than 2 neighbours dies
#* Overpopulation; 2. Any live cell with more than 3 neighbours dies
#* Next generation; 3. Any live cell with 2 or 3 neighbours remains unchanged
#* Birth; 4. Any dead cell with 3 neighbours becomes alive
#! dead or alive - > alive if MooresNeighbours == 3
#! alive -> alive elif MooresNeighbours == 2
#! dead or alive -> dead else 

class Symbols(Enum):
    dead = u"⬜"
    alive = u"⬛"
    newborn = u"🟩"
    dying = u"🟥"

#USE_COLORS = True
class Cell(object):
    
    OLDEST_EVER = int()
    deadColor,aliveColor = Symbols.dead.value,Symbols.alive.value
    newbornColor,dyingColor = Symbols.newborn.value,Symbols.dying.value


    def __init__(self,cellValue,cellAge=0):#TODO,cellAge=None,cellStrength=None WITH GT LT EQ):
        self.isAlive = bool(cellValue)
        self.age = ((cellAge+1) if self.isAlive else 0)

        self.cellColor = (Cell.aliveColor if self.isAlive else Cell.deadColor)
        self.cellUpdateColor = self.cellColor#*TEMP

        self.CELL_COLOR_USED = self.cellColor#*TEMP used in repr()

    def __call__(self,*,useColors:bool):
        if useColors:
            self.CELL_COLOR_USED = self.cellUpdateColor
        else:
            self.CELL_COLOR_USED = self.cellColor
        

    def isBorn(self):
        self.isAlive = True
        self.age = 1
        
        self.cellUpdateColor = Cell.newbornColor
        
        self.cellColor = Cell.aliveColor
        
    def hasDied(self):
        Cell.OLDEST_EVER = max(Cell.OLDEST_EVER,self.age)
        self.isAlive = False
        self.age = 0
        
        self.cellUpdateColor = Cell.dyingColor
        
        self.cellColor = Cell.deadColor
    
    def hasSurvived(self):
        Cell.OLDEST_EVER = max(Cell.OLDEST_EVER,self.age)
        self.isAlive = True
        self.age += 1
        
        self.cellUpdateColor = Cell.aliveColor
        
        self.cellColor = Cell.aliveColor

    def __repr__(self): 
        return self.CELL_COLOR_USED

    def __str__(self): return ("Alive" if self.isAlive else "Dead")

    def __bool__(self): return (True if self.isAlive else False)
    

    

def map2DGrid(grid,Function:Callable): return [list(map(Function,row)) for row in grid]

class Grid1D(object):
    def __init__(self,grid,elementsType):
        if not bool(grid):
            raise Exception("Empty grid input!")
        try:
            grid = list(map(lambda el: elementsType(el),[el for row in grid for el in row]))
        except TypeError as already1Darray:

            grid = list(map(lambda el: elementsType(el),grid))
        
        self.grid = grid

    def __setitem__(self,elementIx,value):
        self.grid[elementIx] = value
 
    def __getitem__(self,elementIx):
        return self.grid[elementIx] 
        #! TODO USE ITERED GENERATOR YIELDING HERE SINCE IT IS APPROX 356725% less time-complex than regular array-returning functions (SEE UNIT TEST AND BENCHMARK FILE)
        #TODO AND IN A SIMPLIFIED NON-COLORED VERY FAST VERSION  ---> accessable_Board would only be a list of alive coords
class Board(Grid1D):

    #TODO create a board buffer class method

    #TODO access preknown organisms in the json here ? 
    def __init__(self, board):
        super().__init__(grid=board,elementsType=Cell)
        self.board = self.grid#inherited all meaningful dunders,reprs and functionalities

        self.max_size = len(self.board)
        self.board_res = self.max_size**0.5 #TODO eventually, make it work for non square boards
        assert self.board_res**2 == float(self.max_size)#!Check if square TEMP

    def __reversed__(self,reverseVertical:bool = True,reverseHorizontal:bool=True):
        temp_board = list(make_chunks(self.board,num_of_chunks=self.board_res))
        temp_board = (temp_board[::-1] if reverseVertical else temp_board)

        horizontal_slice_obj = (slice(None,None,-1) if reverseHorizontal else slice(None)) #*Nice
        
        for layer in temp_board:
            yield layer[horizontal_slice_obj]


#DEBUG
print(*Board.__mro__,sep="\n\tV\n",end="\n\n\n")


class Game:
    NUM_OF_GAME_INSTANCES = int()

    @staticmethod
    def init_generations():

        num_of_generations = -1
        def counter():

            nonlocal num_of_generations
            num_of_generations += 1
            return num_of_generations
        return counter
    
    def __init__(self,*,board,RESOLUTION):#TODO add rule set param
        #if not isinstance(board,Board):

        self.Board = Board(board)
        
        self.RES = RESOLUTION
        self.maxsize = RESOLUTION**2 #max 1d ix
        
        self.generationsCounter = Game.init_generations()
        self.generationsCounter()

        self.CURRENT_GEN_OVERALL = int()

    def updateBoardState(self,newGameState):#TODO
        return

    def getNumberOfCurrentSimulations(cls):
        return cls.NUM_OF_GAME_INSTANCES

    @DefaultObjectMethod(DOC=False)
    def getCurrentGeneration(self):
        return self.CURRENT_GEN_OVERALL

    @classmethod
    def DEBUGSetParameters(cls, **kwargs):#DEBUG ONLY
        for param, value in kwargs.items():
            setattr(cls, f"DEBUG_{param}", value)



#!-----------------
def register_organism_in_json(copiedCustomString):
    organismName = input("\u001b[7mName the organism that will be stored in the JSON:\u001b[0m\u001b[1m\u001b[31m\t");sys.stdout.write("\u001b[0m")
    readable_sprite = copiedCustomString[:-1].split(" \n")
    
    n = len(readable_sprite)
    readable_sprite[0] = readable_sprite[0][1:] ; readable_sprite[n-1] = readable_sprite[n-1][:n+1]
    

    newOrganismSprite = [list(map(lambda i: int(i),sprite_layer.split(" "))) for sprite_layer in readable_sprite]
    return newOrganismSprite
    with open(r'known-organisms-classified.json',"r+") as file:
        json_data = json.load(file)
        #json_newOrganism = json.dumps(newOrganismSprite,ensure_ascii=False)
        #json_data["CustomSavedOrganisms"].append({organismName:newOrganismSprite})
        json_data["CustomSavedOrganisms"].update({organismName:newOrganismSprite})
        file.seek(0)
        json.dump(json_data,file)#TODO FIX THIS FIX THIS FIX THIS FIX THIS FIX THIS FIX THIS
    # json_file.write(f"\"{organismName}\":{json_newOrganism}")
    # json_file.close()

def customization_copied_input_to_storable_array(stringCopied):
    DEBUG = register_organism_in_json(stringCopied)
    count = 0
    normal_length = len(DEBUG[0])
    for row in DEBUG[::-1]:
        count += 1
        if count == 1:
            print((normal_length-len(row))*[0] + row,end=",\n")
        else:
            print(row,end=",\n")
#TODO           MAKE A TRANS FUNCTION THAT TRANSFORMS ORGANISM STORED ARRAYS INTO an array of the coordinates/CellIx of the alive coordinates + its RES/max_size

#TODO           MAKE A FUNCTION THAT CREATES BASIC ORGANISMS KNOWN IN THEORY, BASED ON THE RELATIVE SCALE NxN RECEIVED IN INPUT

#customization_copied_input_to_storable_array(s)

TEST_CASE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#!------------------------------------------
prompt_style,input_style = u"\u001b[47;1m\u001b[30;1m",u"\u001b[0m\t\u001b[36m"

NUMBER_OF_GENERATIONS_SIMULATED = int(input(f"{prompt_style} Enter number of generations/game loops desired:{input_style}"));sys.stdout.write("\u001b[0m")
BOARD_SIZE = int(input(f"{prompt_style} Enter a N for a NxN board size:{input_style}"));sys.stdout.write("\u001b[0m")
while 1:
    organism_selection = input(f"{prompt_style} Enter C for Custom organism OR Enter E to select an Existing organisms:{input_style}");sys.stdout.write("\u001b[0m")
    if organism_selection in ["C","c"]:
        TEST_CASE = MakeTestCaseForConway(BOARD_SIZE,BOARD_SIZE)
        #TODO register_organism_in_json() #TODO BECAUSE WE WANT TO SAVE WITH RELATIVE N, THE MOST ENTRIES
        break
    elif organism_selection in ["E","e"]:
        #!TEST_CASE = register_organism_in_json()
        
        break
    else:
        print("\rBad entry, not a valid organism selection mode!",flush=True,end="")

_GAME = Game(board=TEST_CASE,RESOLUTION=BOARD_SIZE)

#//print([(ix,repr(cell)) for ix,cell in enumerate(_GAME.Board[:])],sep="\n",end="\n\t\u001b[1mINITIAL INPUT\u001b[0m\n\n")



#!------------------------------------------

def coordsToCellIx(rowIx,colIx,_Game:Game=_GAME) -> int: return _Game.RES*rowIx + colIx
def cellIxToCoords(cellIx,_Game:Game=_GAME) -> Tuple[int,int]: return divmod(cellIx,_Game.RES)


def countMooreNeighbors(cellIx,_Game:Game=_GAME):
    y,x = cellIxToCoords(cellIx)
    numOfNeighbors = 0
    # while numOfNeighbors <= 3:
    if (y-1 >= 0 and x-1 >= 0) and _Game.Board[coordsToCellIx(y-1,x-1)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y-1,x-1)}")

    if (y-1 >= 0) and _Game.Board[coordsToCellIx(y-1,x)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y-1,x)}")

    if (y-1 >= 0 and x+1 < _Game.RES) and _Game.Board[coordsToCellIx(y-1,x+1)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y-1,x+1)}")

    if (x-1 >= 0) and _Game.Board[coordsToCellIx(y,x-1)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbordsfds {coordsToCellIx(y,x-1)}")

    if (x+1 <  _Game.RES) and _Game.Board[coordsToCellIx(y,x+1)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y,x+1)}")

    if (y+1 <  _Game.RES and x-1 >= 0) and _Game.Board[coordsToCellIx(y+1,x-1)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y+1,x-1)}")

    if (y+1 <  _Game.RES) and _Game.Board[coordsToCellIx(y+1,x)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y+1,x)}")

    #print(coordsToCellIx(y+1,x+1),end=f"x:{x} y:{y} _Game.RES:{_Game.RES} THIS IS THE MISTAKE\n")
    if (y+1 <  _Game.RES and x+1 <  _Game.RES) and _Game.Board[coordsToCellIx(y+1,x+1)].isAlive:
        numOfNeighbors += 1
        #print(f"{cellIx} has neighbor {coordsToCellIx(y+1,x+1)}")

        # break

    return numOfNeighbors



def gameLogic(useColors:bool,_Game:Game=_GAME):#TODO implement different rule sets
    newGameStateBuffer = Game(board=_Game.Board,RESOLUTION=BOARD_SIZE) #! Check this later but this applies rule set simulatnously for a given generation
    #TODO use numpy bitarray interface! in classmethod of Board newGeneration to temp reset State
    
    for cellIx,cell in enumerate(_Game.Board):#TODO IMPLEMENT COROUTINE FOR MULTIPLE ROWS AT A TIME IN GOLANG
        neighbors = countMooreNeighbors(cellIx)

        if cell.isAlive:
            if neighbors < 2:#? Underpopulation
                newGameStateBuffer.Board[cellIx].hasDied()
                
               # newBoardBuffer.Board[cellIx].isAlive = False

            elif neighbors > 3: #? Overpopulation
                newGameStateBuffer.Board[cellIx].hasDied()
                newGameStateBuffer.Board[cellIx](useColors=useColors)
                #newBoardBuffer.Board[cellIx].isAlive = False
            elif neighbors == 2 or neighbors == 3: #?Survival
                newGameStateBuffer.Board[cellIx].hasSurvived()
                newGameStateBuffer.Board[cellIx](useColors=useColors)
               # newBoardBuffer.Board[cellIx].isAlive = True

        else: #*Dead 
            if neighbors == 3:#? Reproduction
                newGameStateBuffer.Board[cellIx].isBorn()
                newGameStateBuffer.Board[cellIx](useColors=useColors)
                #newBoardBuffer.Board[cellIx].isAlive = True
            #else it is still dead
    return newGameStateBuffer

#!------------------------------------------

def printBoard(_Game:Game=_GAME,generationTimeLength=0.5,isAnimated=True,ShowStateChange=True):#* MY EPIC PRINT ! : D 
    
    newGameState = gameLogic(useColors=False)
    newGameStateColored = gameLogic(useColors=ShowStateChange)

    if ShowStateChange == False:
        generationTimeLength //= 2


    #* VERY IMPORTANT LINE; calls closure and inc inner func generation
    #its like a _Game.generations += 1
    current_generation = _Game.generationsCounter()
    _Game.CURRENT_GEN_OVERALL = current_generation
    
    for gameState in [newGameStateColored,newGameState]:
        _board= gameState.Board[:]

        boardPrint = iter(make_chunks(list(map(repr,_board)),num_of_chunks= gameState.RES))#*Nice
        store_linesToPrint = []
        try:
            while 1:
                #print(*next(boardPrint))
                store_linesToPrint.append("".join(next(boardPrint)))
        except StopIteration as endOfPrint:
            
            if isAnimated == True: sys.stdout.write(f"\u001b[2J\u001b[{1000}D\u001b[{BOARD_SIZE+1}A")
            print("\n\b" + "\n\b".join(store_linesToPrint) + "\n",end="")


            print(f"\rGeneration: {current_generation}",flush=True,end="")
            time.sleep(generationTimeLength)

            sys.stdout.flush()

    _Game.Board = newGameState.Board #? Update new Board State
    #print("\n" + _Game.getCurrentGeneration()) #? Working with closure !



def main():
    global NUMBER_OF_GENERATIONS_SIMULATED
    
    while NUMBER_OF_GENERATIONS_SIMULATED:
        NUMBER_OF_GENERATIONS_SIMULATED -= 1
        printBoard(_Game=_GAME,generationTimeLength=0.1,isAnimated=True,ShowStateChange=True)

if __name__ == "__main__":
    time.sleep(4)#!WAITING FOR PYGAME TO CLOSE
    main()
    

#!------------------------------------------



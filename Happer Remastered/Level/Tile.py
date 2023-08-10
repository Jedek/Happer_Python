import pygame
from pygame.locals import *
from Settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):        
        super().__init__()
        
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.Surface((self.width,self.height))
        self.surface.fill((255,0,0))
        self.rect = self.surface.get_rect()
        
        # self.contents = None
        
        # reserving neighbours        
        self.neighbour = [None,None,None,None]
        
        self.name = "Undefined"
    
    """def populate(self, pawn):
        self.contents = pawn
        
    def dePopulate(self):
        self.contents = None
    
    def isPopulated(self):
        if self.contents == None:
            return False
        else:
            return True"""

    def setName(self, string):
        self.name = string
    
    def setNeighbor(self, tile, direction):
        print("Test: ", self.name, " setting neighbor at", direction)
        
        self.neighbour[direction] = tile
        
        match direction:
            case DIRECTION.UP:
                if tile.neighbour[DIRECTION.DOWN] == None or tile.neighbour[DIRECTION.DOWN] != self:
                    tile.setNeighbor(self, DIRECTION.DOWN)
            case DIRECTION.DOWN:
                if tile.neighbour[DIRECTION.UP] == None or tile.neighbour[DIRECTION.UP] != self:
                    tile.setNeighbor(self, DIRECTION.UP)
            case DIRECTION.LEFT:
                if tile.neighbour[DIRECTION.RIGHT] == None or tile.neighbour[DIRECTION.RIGHT] != self:
                    tile.setNeighbor(self, DIRECTION.RIGHT)
            case DIRECTION.RIGHT:
                if tile.neighbour[DIRECTION.LEFT] == None or tile.neighbour[DIRECTION.LEFT] != self:
                    tile.setNeighbor(self, DIRECTION.LEFT)
            
        
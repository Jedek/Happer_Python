import pygame
from pygame.locals import *
from Settings import *
from Objects.Pawns.Pawn import Pawn

class Wall(Pawn):
        def __init__(self):        
            super().__init__()
            self.movable = True
            self.setColor()
        
        def setPosition(self, tile):
            if self.movable == True or self.currentTile == None:
                super().setPosition(tile)
            else: 
                print("Wall can't move")
                
        
        def setColor(self):
            if self.movable:
                self.surface.fill((255,255,0))
            else:
                self.surface.fill((0,0,0))
        
        def move(self, key):
            print("moving wall towards direction ", key)
            destinationTile = self.currentTile.neighbour[key]
            if destinationTile != None:
                self.setPosition(destinationTile)
        pass
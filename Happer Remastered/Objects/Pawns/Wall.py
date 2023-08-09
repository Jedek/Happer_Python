import pygame
from pygame.locals import *
from Objects.Pawns.Pawn import Pawn

class Wall(Pawn):
        def __init__(self):        
            super().__init__()
            self.movable = True
            self.setColor()
        
        def setPosition(self, tile):
            if(self.movable):
                super().setPosition(tile)
            else:
                print("Cant move this")
        
        def setColor(self):
            if self.movable:
                self.surface.fill((255,255,0))
            else:
                self.surface.fill((0,0,0))
        
        pass
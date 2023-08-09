import pygame
from pygame.locals import *
from Objects.Pawns.Pawn import Pawn

class Player(Pawn):
        def __init__(self):        
            super().__init__()
            self.radius = 30
            
        def draw(self, screen):
            pygame.draw.circle(screen, (0,0,0), (self.rect.center), self.radius)
            
        pass
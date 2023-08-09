import pygame
from pygame.locals import *

class Wall(pygame.sprite.Sprite):
        def __init__(self):        
            super().__init__()
            self.width = 75
            self.height = 75
            self.surface = pygame.Surface((self.width,self.height))
            self.rect = self.surface.get_rect()
            self.movable = True
            
            if self.movable:
                self.surface.fill((255,255,0))
            else:
                self.surface.fill((0,0,0))
        
        def setPosition(self, tile):
            self.currentTile = tile
            self.rect.center = self.currentTile.rect.center
        
        
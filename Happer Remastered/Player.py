import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
        def __init__(self):        
            super().__init__()
            self.radius = 30
        
        def setPosition(self, tile):
            self.currentTile = tile
            self.x = self.currentTile.rect.x + (self.currentTile.width/2)
            self.y = self.currentTile.rect.y + (self.currentTile.height/2)
            
        def draw(self, screen):
            pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.radius)
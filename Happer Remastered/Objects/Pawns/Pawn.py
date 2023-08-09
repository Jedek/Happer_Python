import pygame
from Settings import *

class Pawn(pygame.sprite.Sprite):
    '''
    classdocs
    '''
    def __init__(self):
        super().__init__()
        self.currentTile = None
        
        self.width = 75
        self.height = 75
        self.surface = pygame.Surface((self.width,self.height))
        self.rect = self.surface.get_rect()
        
        
    def setPosition(self, tile):
        self.currentTile = tile
        self.rect.center = tile.rect.center
        
        
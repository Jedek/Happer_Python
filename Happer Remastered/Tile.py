import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):        
        super().__init__()
        
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.Surface((self.width,self.height))
        self.surface.fill((255,0,0))
        self.rect = self.surface.get_rect()
        self.populated = False
    
    def populate(self, pawn):
        self.contents = pawn
        self.populated = True
        
        print(self.name, " is populated")
    
    def isPopulated(self):
        return self.populated
    
    def dePopulate(self):
        self.object = None
        self.populated = False
    
    def setName(self, string):
        self.name = string
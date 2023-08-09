import pygame
from pygame.locals import *
from Tile import Tile
from Player import Player
from Wall import Wall
import random

class Board(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.width = WIDTH
        self.height = HEIGHT
        self.font = pygame.font.SysFont('Arial', 25)
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0,255,0))
        self.rect = self.surface.get_rect()
        self.tiles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        
        self.player = Player()
         
    def generateLevel(self):   
        
        self.tilemap = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
        ]
                 
        self.mapWidth = len(self.tilemap[0])
        self.mapHeight = len(self.tilemap)
        
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                tile = Tile(100, 100)
                tile.setName("Tile {} of {}".format(x,y))
                tile.x = x 
                tile.y = y 
                tile.rect.x = (tile.width*x) + x
                tile.rect.y = (tile.height*y) + y
                self.tiles.add(tile)
                self.tilemap[y][x] = tile
                
    def spawnPlayer(self):
        randomTile = self.tiles.sprites()[random.randint(0, len(self.tiles))-1]
        self.player.setPosition(randomTile)
        randomTile.populate(self.player)

    def addWalls(self):
        randomTile = self.tiles.sprites()[random.randint(0, len(self.tiles))]
        
        print("Putting wall in tile " + randomTile.name)
        if randomTile.isPopulated() == False:
            wall = Wall()
            wall.setPosition(randomTile)
            randomTile.populate(wall)
            self.walls.add(wall)

    def draw(self,screen):
        for tile in self.tiles:
            screen.blit(tile.surface, tile.rect)
            screen.blit(self.font.render(tile.name, True, (0,0,0)), (tile.rect.x, tile.rect.y))
        
        for wall in self.walls:
            screen.blit(wall.surface, (wall.rect.x, wall.rect.y))
        
        self.player.draw(screen)
    
    def movePlayer(self, x, y):
        
        currentTile = self.player.currentTile
        newX = currentTile.x + x
        newY = currentTile.y + y
        
        try:
            newTile = self.tilemap[newY][newX]
            if newTile.isPopulated() == False:
                self.player.setPosition(newTile)
                newTile.populate(self.player)
                currentTile.dePopulate()
        except:
            print("Exception occurred. Probably out of bounds")
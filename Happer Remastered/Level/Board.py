import pygame
from pygame.locals import *
from Level.Tile import Tile
from Objects.Pawns.Player import Player
from Objects.Pawns.Wall import Wall
import random
from Settings import *
from types import SimpleNamespace

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
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
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
                
                if x > 0:
                    newX = x-1
                    leftNeighbor = self.tilemap[y][newX]
                    tile.setNeighbor(leftNeighbor, DIRECTION.LEFT)
                
                if y > 0:
                    newY = y-1
                    topNeighbor = self.tilemap[newY][x]
                    tile.setNeighbor(topNeighbor, DIRECTION.UP)
        
    def spawnPlayer(self):
        randomTile = self.tiles.sprites()[random.randint(0, len(self.tiles))-1]
        self.player.setPosition(randomTile)
        randomTile.populate(self.player)

    def addWalls(self):
        randomTile = self.tiles.sprites()[random.randint(0, len(self.tiles))]
        
        if randomTile.isPopulated() == False:
            wall = Wall()
            wall.setPosition(randomTile)
            randomTile.populate(wall)
            self.walls.add(wall)
            print("Putting wall in tile " + wall.currentTile.name)

    def convertWalls(self):
        print("Converting walls")
        for wall in self.walls:
            if wall.movable == True:
                wall.movable = False
            else:
                wall.movable = True
                
            wall.setColor()
                

    def draw(self,screen):
        for tile in self.tiles:
            screen.blit(tile.surface, tile.rect)
            screen.blit(self.font.render(tile.name, True, (0,0,0)), (tile.rect.x, tile.rect.y))
        
        for wall in self.walls:
            screen.blit(wall.surface, (wall.rect.x, wall.rect.y))
        
        self.player.draw(screen)
    
    def movePlayer(self, key):
        currentTile = self.player.currentTile
        newTile = None
        movePlayer = False
        
        newTile = currentTile.neighbour[key]              
        
        if newTile != None:
            if newTile.isPopulated() == False:
                movePlayer = True
            else:
                wall = newTile.contents
                if isinstance(wall, Wall):
                    print("There is a wall here!")
                    if wall.movable:
                        print("Wall can be moved!")
                        wallCurrentTile = wall.currentTile
                        bumpedTile = wallCurrentTile.neighbour[key]
                        wall.setPosition(bumpedTile)
                        wallCurrentTile.dePopulate()
                        bumpedTile.populate(wall)
                    else:
                        print("Wall cant be moved...")
        
        if movePlayer:
            self.player.setPosition(newTile)
            newTile.populate(self)
            currentTile.dePopulate()
                    

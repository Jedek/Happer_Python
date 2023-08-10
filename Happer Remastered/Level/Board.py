import pygame
from pygame.locals import *
from Level.Tile import Tile
from Objects.Pawns.Player import Player
from Objects.Pawns.Wall import Wall
import random
from Settings import *
from types import SimpleNamespace
from pickle import TRUE, NONE

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
        
        self.wallBacklog = []
         
    def generateLevel(self):   
        
        self.tiles.empty()
        self.walls.empty()
        
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
        
        wall1 = Wall()
        wall2 = Wall()
        wall3 = Wall()
        wall3.movable = False
        
        wall1.setPosition(self.tilemap[2][2])
        wall2.setPosition(self.tilemap[3][2])
        wall3.setPosition(self.tilemap[2][5])
        
        self.walls.add(wall1)
        self.walls.add(wall2)
        self.walls.add(wall3)
        
    def spawnPlayer(self):
        randomTile = self.tiles.sprites()[random.randint(0, len(self.tiles))-1]
        self.player.setPosition(randomTile)

    def addWalls(self):
        randomTile = self.tiles.sprites()[random.randint(0, len(self.tiles))-1]
        placeWall = True
        
        for wall in self.walls:
            if wall.currentTile == randomTile:
                placeWall = False
        
        if placeWall:
            wall = Wall()
            wall.setPosition(randomTile)
            self.walls.add(wall)
            print("Putting wall in tile " + wall.currentTile.name)
            return False
        else:
            return self.addWalls()

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
            wall.setColor()
            screen.blit(wall.surface, (wall.rect.x, wall.rect.y))
        
        self.player.draw(screen)
    
    def movePlayer(self, key):
        currentTile = self.player.currentTile
        movePlayer = True
        newTile = currentTile.neighbour[key]              
        
        print("Key is ", key)
        for wall in self.walls:
            if wall.currentTile == newTile:
                if wall.movable:
                    movePlayer = self.pushWall(wall, key)
                else:
                    movePlayer = False
                    
        if self.player.pushing == False:
            """Determine the opposite direction of the player. Determine if in the very next opposite tile there is a wall. Pull that wall."""
            
            match key:
                case DIRECTION.UP:
                    oppositeKey = DIRECTION.DOWN
                case DIRECTION.DOWN:
                    oppositeKey = DIRECTION.UP
                case DIRECTION.LEFT:
                    oppositeKey = DIRECTION.RIGHT
                case DIRECTION.RIGHT:
                    oppositeKey = DIRECTION.LEFT
            
            print("Opposite key is ", oppositeKey)
            oppositeTile = self.player.currentTile.neighbour[oppositeKey]
            
            for wall in self.walls:
                if wall.currentTile == oppositeTile:
                    if wall.movable:
                        print("Sending wall to direction ", oppositeKey)
                        self.pullWall(wall, key)
                    else:
                        movePlayer = False 
                        
        if movePlayer and newTile != None:
            self.player.setPosition(newTile)
    
    def pullWall(self, wall, key):
        playerNextMove = self.player.currentTile.neighbour[key]
        validMove = True
        
        for otherWall in self.walls:
            if otherWall.currentTile == playerNextMove and otherWall.movable == False:
                validMove = False
            
        if validMove:
            wall.move(key)
            return True
        else:
            return False
    
    def pushWall(self, wall, key, available = False):
        if available == True:
            print("Moving wall on ", wall.currentTile.name, " to ", wall.currentTile.neighbour[key].name)
            wall.move(key)
            return True
        else:
            destination = wall.currentTile.neighbour[key]
            if destination != None:
                for nextWall in self.walls:
                    if nextWall.currentTile == destination:
                        if nextWall.movable:
                            moveWall = self.pushWall(nextWall, key)
                            if moveWall:
                                wall.move(key)
                                return True
                            else: return False
                        else:
                            return False
                return self.pushWall(wall, key, True)
        return False
    
    def playerPulling(self):
        
        keys = pygame.key.get_pressed()
        if keys[K_c]:
            self.player.pushing = False
        else:
            self.player.pushing = True
                    

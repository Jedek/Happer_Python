import pygame
from pygame.locals import *
from Level.Board import *
from Settings import *

class Game:
    HEIGHT = 600
    WIDTH = 800
    SIZE = WIDTH, HEIGHT
    

    def __init__(self):
        pygame.init()
        self.running = True
        self.board = Board(Game.WIDTH, Game.HEIGHT)
        self.board.generateLevel()        
        self.board.spawnPlayer()
        self.screen = pygame.display.set_mode(((self.board.mapWidth*100), (self.board.mapHeight*100)))
        
        pygame.display.set_caption("Game")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        self.board.movePlayer(DIRECTION.UP)
                    if event.key == K_DOWN:
                        self.board.movePlayer(DIRECTION.DOWN)
                    if event.key == K_LEFT:
                        self.board.movePlayer(DIRECTION.LEFT)
                    if event.key == K_RIGHT:
                        self.board.movePlayer(DIRECTION.RIGHT)
                    if event.key == K_SPACE:
                        self.board.addWalls()
                    if event.key == K_t:
                        self.board.convertWalls()
                    if event.key == K_F5:
                        self.board.generateLevel()
                        self.board.spawnPlayer()
                    
            self.board.draw(self.screen)
            self.board.playerPulling()
            pygame.display.update()
        pygame.quit()

game = Game()
game.run()      

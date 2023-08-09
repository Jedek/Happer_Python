import pygame
from pygame.locals import *
from Board import Board

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
                        self.board.movePlayer(0, -1)
                    if event.key == K_DOWN:
                        self.board.movePlayer(0, 1)
                    if event.key == K_LEFT:
                        self.board.movePlayer(-1, 0)
                    if event.key == K_RIGHT:
                        self.board.movePlayer(1, 0)
                    if event.key == K_SPACE:
                        self.board.addWalls()

            self.board.draw(self.screen)
            pygame.display.update()
        pygame.quit()

game = Game()
game.run()      

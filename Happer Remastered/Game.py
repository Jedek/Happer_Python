import pygame as pg
from pygame.locals import *

from utils import Dimension, Buttons
from Level.board import Board

class Application:
    def __init__(self):
        self.caption = "Happer Remastered"
        self.window = pg.display.set_mode((Dimension.SCREEN_WIDTH.value, Dimension.SCREEN_HEIGHT.value))
        self.board = Board(self.window)
    
    def run(self):
        
        pg.display.set_caption(self.caption)
        self.board.draw_board()
        pg.display.flip()
        running = True
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_r:
                        self.board.recreate_obstacles()
                    if event.key == K_UP:
                        self.board.move_player(Buttons.UP.value)
                    if event.key == K_DOWN:
                        self.board.move_player(Buttons.DOWN.value)
                    if event.key == K_LEFT:
                        self.board.move_player(Buttons.LEFT.value)
                    if event.key == K_RIGHT:
                        self.board.move_player(Buttons.RIGHT.value)
        pg.quit()

app = Application()
app.run()
import pygame as pg
from pygame.locals import *

from utils import Dimension, Buttons
from Level.board import Board
from Objects.pawn import Pawn
from pathfinder import PathFinder

class Application:
    def __init__(self):
        self.caption = "Happer Remastered"
        self.window = pg.display.set_mode((Dimension.SCREEN_WIDTH.value, Dimension.SCREEN_HEIGHT.value))
        self.board = Board(self.window)
        self.path_finder = PathFinder(self.window)
        
        self.time_interval = 750
        self.timer_event = pg.USEREVENT+1
    
    def run(self):
        
        pg.display.set_caption(self.caption)
        pg.display.flip()
        self.board.draw_board()
       
        running = True
        
        print(self.board.board_matrix)
        pg.time.set_timer(self.timer_event, self.time_interval)
        self.test_interval = 0
        
        while running:
            #self.board.enemy.draw_path_to_player()
            self.board.enemy.find_path_to_player(self.board.player, self.board.board_matrix)
            self.board.is_enemy_defeated()
            for event in pg.event.get():
                if event.type == self.timer_event:
                    self.board.enemy.move_to_player()
                    self.board.draw_board()
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
                
                if event.type == pg.MOUSEBUTTONUP and event.button == Buttons.MOUSE_LEFT.value:
                    self.choose_square()

                if event.type == pg.MOUSEBUTTONUP and event.button == Buttons.MOUSE_RIGHT.value:
                    self.clear_board()
        pg.quit()
    
    def choose_square(self):
        clicked_square_pos = Pawn.convert_to_board_coordinates(pg.mouse.get_pos())
        clicked_square = Pawn(*clicked_square_pos)
        if self.board.is_square_empty(clicked_square.x, clicked_square.y):
            self.path_finder.set_point(clicked_square)
    
    def clear_board(self):
        """
        Removes the found path and selected squares from the board.
        Board is redrawn

        :return: None
        """
        self.path_finder.reset()
        self.board.draw_board()

app = Application()
app.run()
from typing import List

import pygame as pg
import numpy as np

from Objects.pawn import Pawn
from utils import Colors
from pathfinder import PathFinder

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Enemy(Pawn):
    
    def __init__(self, x: int, y: int, window: pg.Surface):
        super().__init__(x, y, Colors.RED.value)
        
        self.window = window
        self.path = None
        
    def find_path_to_player(self, player, matrix: np.ndarray):
        self.start_square = self
        self.end_square = player
        
        grid = Grid(matrix=matrix)
        start = grid.node(*self.start_square.board_coordinates)
        end = grid.node(*self.end_square.board_coordinates)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        self.path_able_to_find = False
        path_squares = [Pawn(*path_point, Colors.GRAY.value) for path_point in path[1:-1]]
        self.path = path_squares
    
    def draw_path_to_player(self):
        if self.path != None:
            for path_square in self.path:
                if path_square != self:
                    if path_square != self.end_square:
                        path_square.draw(self.window)
    
    def move_to_player(self):
        if self.path != None:
            if self.board_coordinates != self.end_square.board_coordinates:
                if len(self.path) > 0:
                    self.move(self.path[0].x, self.path[0].y)
            else:
                print("Found him!")
        
        
        
        
        
    
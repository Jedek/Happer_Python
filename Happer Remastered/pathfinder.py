from typing import List

import pygame as pg
import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from utils import Colors
from Objects.pawn import Pawn


class PathFinder:
    def __init__(self, window: pg.Surface):
        """
         Creates a new ``PathFinder`` instance.
        """
        self.start_square = None
        self.end_square = None
        self.window = window
        self.path_able_to_find = False
    
    
    
    def set_point(self, clicked_square: Pawn):
        """
        Sets the starting or ending square of the path. The starting square will be set first, then the end square.

        :param clicked_square: clicked square by user
        :return: None
        """

        if self.start_square is None:
            self.start_square = clicked_square
            self.start_square.color =  Colors.GREEN.value
        elif self.end_square is None and self.start_square != clicked_square:
            self.end_square = clicked_square
            self.end_square.color = Colors.RED.value
            self.path_able_to_find = True

    def reset(self):
        """
        Deletes chosen squares.

        :return: None
        """
        self.start_square = self.end_square = None

    def draw_squares(self):
        """
        if start or end square is not None, it is drawn.
        :return: None
        """
        if self.start_square is not None:
            self.start_square.draw(self.window)

        if self.end_square is not None:
            self.end_square.draw(self.window)

    def find_path(self, matrix: np.ndarray) -> List[Pawn]:
        """
        Finds path between start and end square using A star algorithm.

        :return: founded path
        """
        grid = Grid(matrix=matrix)
        start = grid.node(*self.start_square.board_coordinates)
        end = grid.node(*self.end_square.board_coordinates)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        self.path_able_to_find = False
        path_squares = [Pawn(*path_point, Colors.GRAY.value) for path_point in path[1:-1]]
        return path_squares

    def draw_path(self, path_squares: List[Pawn]):
        for path_square in path_squares:
            path_square.draw(self.window)
            pg.time.delay(100)

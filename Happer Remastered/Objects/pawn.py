import pygame as pg

from typing import Tuple

from utils import Dimension, Colors


class Pawn:
    """
    Class for representing pawns on the board
    """
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = [0, 0, 0]):
        """
         Creates a new ``pawn`` instance.
        """
        self.x, self.y, self.color = x, y, color

    @property
    def window_coordinates(self) -> Tuple[int, int]:
        """
        Transform board coordinates of pawn to window coordinates

        :return: coordinates of top left corner of pawn
        """
        return self.x * Dimension.SQUARE_WIDTH.value, self.y * Dimension.SQUARE_HEIGHT.value

    @staticmethod
    def convert_to_board_coordinates(position: Tuple[int, int]) -> Tuple[int, int]:
        x, y = position
        x = min(x // Dimension.SQUARE_WIDTH.value, Dimension.board_width() - 1)
        y = min(y // Dimension.SQUARE_HEIGHT.value, Dimension.board_height() - 1)

        return x, y

    @property
    def board_coordinates(self) -> Tuple[int, int]:
        return self.x, self.y

    def draw(self, window: pg.Surface):
        """
        Full fill pawn with given color.

        :param window: window created by pygame
        :param color: color in RGB format
        :return: None
        """
        shifted_window_coordinates = tuple(coord + 1 for coord in self.window_coordinates)
        rect = (shifted_window_coordinates, (Dimension.SQUARE_WIDTH.value - 1, Dimension.SQUARE_HEIGHT.value - 1))
        pg.draw.rect(window, self.color, rect)

        pg.display.update(rect)
    
    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Pawn):
            return self.board_coordinates == other.board_coordinates
        return NotImplemented

    def __hash__(self):
        return hash(self.board_coordinates)
    
    

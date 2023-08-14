import pygame as pg
from Objects.pawn import Pawn
from utils import Colors
from typing import Tuple

class Obstacle(Pawn):
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, Colors.BLACK.value)
        self.is_movable = False
    
    def toggle_movable(self):
        if self.is_movable:
            self.is_movable = False
            self.color = Colors.BLACK.value
        else:
            self.is_movable = True
            self.color = Colors.YELLOW.value
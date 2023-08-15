import random
from typing import List

import numpy as np
import pygame as pg

from utils import Dimension, Colors, Buttons
from Objects.pawn import Pawn
from Objects.enemy import Enemy
from Objects.obstacle import Obstacle


class Board:
    """
    A class representing a chess-like board but with different size: 10x10, instead of classic 8x8.

    ...

    Attributes
    ----------

    window: pygame.Surface
        Pygame object for representing images.
    board_matrix: numpy.ndarray
        array 10x10 representing state of board .
        1 represents empty square and 0 represent obstacle.

    """
    def __init__(self, window: pg.Surface):
        """
         Creates a new ``Board`` instance.

        Parameters
        ----------
            window : pygame.Surface
                Pygame object for representing images.
        """
        self.window = window
        self.board_matrix = np.full(Dimension.board_size(), 1)
        self.maximum_obstacles_on_board = 10
        self.maximum_walls_on_board = 20
        self.pawns = list()
        self.player = self.create_player()
        self.enemy = self.create_enemy()
        
        self.create_obstacles()

    def draw_board(self):
        """
        All elements of board are drawn.

        :return: None
        """
        self.window.fill(Colors.WHITE.value)
        self.draw_lines()
        self.draw_pawns()
        self.draw_actors()

    def draw_lines(self):
        """
        Draws lines on the board, the first and last lines are not drawn because these lines are the ends of the screen

        :return: None
        """
        for x_cord in range(0, Dimension.SCREEN_WIDTH.value, Dimension.SQUARE_WIDTH.value):
            pg.draw.line(self.window, Colors.BLACK.value, (x_cord, 0), (x_cord, Dimension.SCREEN_HEIGHT.value))

        for y_cord in range(0, Dimension.SCREEN_HEIGHT.value, Dimension.SQUARE_HEIGHT.value):
            pg.draw.line(self.window, Colors.BLACK.value, (0, y_cord), (Dimension.SCREEN_WIDTH.value, y_cord))

        pg.display.update()
    
    def draw_actors(self):
        self.player.draw(self.window)
        self.enemy.draw(self.window)
    
    def draw_pawns(self):
        """
        Obstacles created by self.create_obstacles are drawn on self.windows as a black rectangles.

        :return: None
        """
        for pawn in self.pawns:
            pawn.draw(self.window)

    def create_obstacles(self) -> List[Pawn]:
        """
        Function creates from 1 to 10 obstacles with random coordinates.
        The self.matrix is modified to reflect the changes to on the board

        :return: list of obstacles coordinates
        :rtype: list
        """
        obstacles_number = random.randint(7, self.maximum_obstacles_on_board)
        walls_number = random.randint(10, self.maximum_walls_on_board)
        total_number = obstacles_number + walls_number
        
        # Generate obstacles first
        while len(self.pawns) < obstacles_number:

            obstacle_x_pos = random.randint(0, Dimension.board_width() - 1)
            obstacle_y_pos = random.randint(0, Dimension.board_height() - 1)
            obstacle = Obstacle(obstacle_x_pos, obstacle_y_pos)
            if obstacle not in self.pawns:
                self.board_matrix[obstacle_y_pos][obstacle_x_pos] = 0
                self.pawns.append(obstacle)
        
        #then generate walls
        while len(self.pawns) < total_number:
            obstacle_x_pos = random.randint(0, Dimension.board_width() - 1)
            obstacle_y_pos = random.randint(0, Dimension.board_height() - 1)
            obstacle = Obstacle(obstacle_x_pos, obstacle_y_pos)
            obstacle.toggle_movable()
            if obstacle not in self.pawns:
                self.board_matrix[obstacle_y_pos][obstacle_x_pos] = 0
                self.pawns.append(obstacle)
            

    def is_square_empty(self, x, y) -> bool:
        """
        Checks if clicked square is not obstacle and it's possible to start/end path here.

        :param clicked_square: A square of board which user clicked.
        :return: true if square is not obstacle, otherwise false
        """
        empty = True
        for pawn in self.pawns:
            if pawn.x == x and pawn.y == y:
                empty = False

        if hasattr(self, "enemy") and self.enemy.x == x and self.enemy.y == y:
            empty = False

        return empty
        #return target_square not in self.obstacles
    
    def is_within_bounds(self, x: int, y: int):
        if x in range(0, len(self.board_matrix[0])) and y in range(0, len(self.board_matrix)):
            return True
        else:
            return False
    
    
    def recreate_obstacles(self):
        """
        Creates new state of board with different number of obstacles and their positions.

        :return: None
        """
        self.board_matrix = np.full(Dimension.board_size(), 1)
        self.pawns = list()
        self.create_obstacles()
        self.draw_board()
    
    def create_player(self):
        
        #player_x_pos = random.randint(0, Dimension.board_width() - 1)
        #player_y_pos = random.randint(0, Dimension.board_height() - 1)
        player = Pawn(0, 0, Colors.ORANGE.value)
        
        return player
    
    def create_enemy(self):
        enemy_x_pos = random.randint(0, Dimension.board_width() - 1)
        enemy_y_pos = random.randint(0, Dimension.board_height() - 1)
        
        if self.is_square_empty(enemy_x_pos, enemy_y_pos):
            return Enemy(enemy_x_pos, enemy_y_pos, self.window)
        else:
            return self.create_enemy()
    
    def move_player(self, direction):
        player_x = self.player.x
        player_y = self.player.y
        
        move_player = False
        
        match direction:
            case Buttons.UP.value:
                "move up"
                player_y-=1              
            case Buttons.DOWN.value:
                "move down"
                player_y+=1
            case Buttons.LEFT.value:
                "move left"
                player_x-=1
            case Buttons.RIGHT.value:
                "move right"
                player_x+=1
        
        
        if self.is_square_empty(player_x, player_y):
            if self.is_within_bounds(player_x, player_y):
                move_player = True
        else:
            for pawn in self.pawns:
                if pawn.x == player_x and pawn.y == player_y:
                    if pawn.is_movable:
                        self.move_obstacle(pawn, direction)
                               
        if move_player: 
            self.player.move(player_x, player_y)
            self.draw_board()
        
    def move_obstacle(self, obstacle, direction, available = False):
        target_x = obstacle.x
        target_y = obstacle.y
    
        match direction:
            case Buttons.UP.value:
                "move up"
                target_y-=1              
            case Buttons.DOWN.value:
                "move down"
                target_y+=1
            case Buttons.LEFT.value:
                "move left"
                target_x-=1
            case Buttons.RIGHT.value:
                "move right"
                target_x+=1   
        
        if available == True:
            if self.is_square_empty(target_x, target_y) and self.is_within_bounds(target_x, target_y):
                self.board_matrix[obstacle.y][obstacle.x] = 1
                self.board_matrix[target_y][target_x] = 0
                obstacle.move(target_x, target_y)
                self.draw_board()
                return True
        else:
            for next_obstacle in self.pawns:
                if next_obstacle.x == target_x and next_obstacle.y == target_y:
                    if next_obstacle.is_movable:
                        self.move_obstacle(next_obstacle, direction)
            
            self.move_obstacle(obstacle, direction, True)
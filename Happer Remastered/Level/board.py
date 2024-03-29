import random
from typing import List

import numpy as np
import pygame as pg
import csv

from utils import Dimension, Colors, Buttons, Levels
from Objects.pawn import Pawn
from Objects.enemy import Enemy
from Objects.obstacle import Obstacle
from ast import Num


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
        self.maximum_obstacles_on_board = 100
        self.maximum_walls_on_board = 100
        
        self.level = Levels.LEVEL_1.value
        
        self.pawns = list()
        self.generate_level()


    def draw_board(self):
        """
        All elements of board are drawn.

        :return: None
        """
        self.window.fill(Colors.WHITE.value)
        self.draw_lines()
        self.draw_pawns()
        self.draw_actors()
        pg.display.update()

    def draw_lines(self):
        """
        Draws lines on the board, the first and last lines are not drawn because these lines are the ends of the screen

        :return: None
        """
        for x_cord in range(0, Dimension.SCREEN_WIDTH.value, Dimension.SQUARE_WIDTH.value):
            pg.draw.line(self.window, Colors.BLACK.value, (x_cord, 0), (x_cord, Dimension.SCREEN_HEIGHT.value))

        for y_cord in range(0, Dimension.SCREEN_HEIGHT.value, Dimension.SQUARE_HEIGHT.value):
            pg.draw.line(self.window, Colors.BLACK.value, (0, y_cord), (Dimension.SCREEN_WIDTH.value, y_cord))
    
    def draw_actors(self):
        self.player.draw(self.window)
        self.enemy.draw(self.window)
    
    def draw_pawns(self):
        """
        Pawns created by self.create_pawns are drawn on self.windows as a black/yellow rectangles.

        :return: None
        """
        for pawn in self.pawns:
            pawn.draw(self.window)

    def generate_level(self) -> List[Pawn]:
        """
        Create walls and obstacles based on the maximum settings (set in initialisation)
        The self.matrix is modified to reflect the changes to on the board

        :return: list of obstacles coordinates
        :rtype: list
        """
        
        with open(self.level, newline='') as csvfile:
            tile_map = csv.reader(csvfile, delimiter=',', quotechar='|')
            
            x_pos = 0
            y_pos = 0
            
            for y in tile_map:
                x_pos = 0
                for x in y:
                    obstacle = None
                    if x == "1":
                        obstacle = Obstacle(x_pos, y_pos)
                    
                    if x == "W":
                        obstacle = Obstacle(x_pos, y_pos)
                        obstacle.toggle_movable()
                    
                    if x == "P":
                        self.player = self.spawn_player(x_pos, y_pos)
                    
                    if x == "E":
                        self.enemy = self.spawn_enemy(x_pos, y_pos)
                                        
                    if obstacle != None:
                        if obstacle not in self.pawns:
                            self.board_matrix[y_pos, x_pos] = 0
                            self.pawns.append(obstacle)
                            
                    x_pos+=1
                y_pos+=1
                
        
        """obstacles_number = random.randint(7, self.maximum_obstacles_on_board)
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
                self.pawns.append(obstacle)"""
            

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
        """
        Check to see if pawns are within the range of the grid. We don't want them to move off the screen right now.
        
        :param x: x coordinate integer
        :param y: y coordinate integer
        """
        if x in range(0, len(self.board_matrix[0])) and y in range(0, len(self.board_matrix)):
            return True
        else:
            return False
    
    def is_enemy_defeated(self):
        """
        Check to see if the enemy pawn is surrounded by walls/obstacles. If they are, enemy is dead.
        """
        number_of_squares = 0
        
        squares_to_check = list()
        squares_to_check.append(Pawn(self.enemy.x+1, self.enemy.y))
        squares_to_check.append(Pawn(self.enemy.x-1, self.enemy.y))
        squares_to_check.append(Pawn(self.enemy.x, self.enemy.y+1))
        squares_to_check.append(Pawn(self.enemy.x, self.enemy.y-1))
        
        for square in squares_to_check:
            if self.is_square_empty(square.x, square.y) == False:
                number_of_squares += 1
        
        if number_of_squares > 2:
            print("Enemy is defeated!")
    
    def recreate_obstacles(self):
        """
        Creates new state of board with different number of obstacles and their positions.

        :return: None
        """
        self.board_matrix = np.full(Dimension.board_size(), 1)
        self.pawns = list()
        self.create_obstacles()
        self.draw_board()
    
    def spawn_player(self, x: int, y: int):
        """
        Generate the player and put it on the board. If the square is already occupied, try again
        
        Note: Maybe create_player and create_enemy can be combined??
        """
        #player_x_pos = random.randint(0, Dimension.board_width() - 1)
        #player_y_pos = random.randint(0, Dimension.board_height() - 1)
        
        if self.is_square_empty(x, y):
            return Pawn(x, y, Colors.ORANGE.value)
        else:
            return self.create_player()
    
    def spawn_enemy(self, x: int, y: int):
        """
        Generate the enemy and place him on the board. If the square is already occupied, try again
        """
        #enemy_x_pos = random.randint(0, Dimension.board_width() - 1)
        #enemy_y_pos = random.randint(0, Dimension.board_height() - 1)
        
        if self.is_square_empty(x, y):
            return Enemy(x, y, self.window)
        else:
            return self.create_enemy()
    
    def move_player(self, direction):
        """
        Move the player in the direction given. Only empty squares can be moved into and if the player moves into a wall,
        the walls are moved recursively
        
        :param direction: the direction based on keyboard presses
        """
        move_player = False
        is_pulling = self.is_player_pulling()
        
        player_direction_coordinates = self.determine_direction_coordinates(direction, self.player)
        player_x = player_direction_coordinates[0]
        player_y = player_direction_coordinates[1] 
        
        if self.is_square_empty(player_x, player_y):
            if self.is_within_bounds(player_x, player_y):
                move_player = True
        else:
            for pawn in self.pawns:
                if pawn.x == player_x and pawn.y == player_y:
                    if pawn.is_movable:
                        self.move_obstacle(pawn, direction)
                               
        if move_player: 
            if is_pulling:
                opposite_direction = self.get_opposite_direction(direction)
                opposite_direction_coordinates = self.determine_direction_coordinates(opposite_direction, self.player)
                
                for pawn in self.pawns:
                    if pawn.x == opposite_direction_coordinates[0] and pawn.y == opposite_direction_coordinates[1]:
                        if pawn.is_movable:
                            self.player.move(player_x, player_y)
                            self.move_obstacle(pawn, direction)
            else:
                self.player.move(player_x, player_y)
                
            self.draw_board()
    
    def is_player_pulling(self):
        pressed_key = pg.key.get_pressed()
        
        if pressed_key[pg.K_LCTRL]:
            return True
        else:
            return False
        
    def move_obstacle(self, obstacle, direction, available = False):
        """
        Move the obstacles(walls), recursively checking if there's further walls to move
        
        :param obstacle: the obstacle that should be moved
        :param direction: the direction based on keyboard presses
        :param available: Remains falls until the recursive check has been done, after which the wall is moved
        """
        obstacle_direction = self.determine_direction_coordinates(direction, obstacle)
        target_x = obstacle_direction[0]
        target_y = obstacle_direction[1]
        
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
    
    def determine_direction_coordinates(self, direction, pawn: Pawn):
        x = pawn.x
        y = pawn.y
        
        match direction:
            case Buttons.UP.value:
                "move up"
                y-=1              
            case Buttons.DOWN.value:
                "move down"
                y+=1
            case Buttons.LEFT.value:
                "move left"
                x-=1
            case Buttons.RIGHT.value:
                "move right"
                x+=1
                
        return (x, y)
    
    def get_opposite_direction(self, direction):
        match direction:
            case Buttons.UP.value:
                "move up"
                direction = Buttons.DOWN.value         
            case Buttons.DOWN.value:
                "move down"
                direction = Buttons.UP.value
            case Buttons.LEFT.value:
                "move left"
                direction = Buttons.RIGHT.value
            case Buttons.RIGHT.value:
                "move right"
                direction = Buttons.LEFT.value
                
        return direction
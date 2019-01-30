'''
Ian Magnusson
CS5001
Homework 6
November 18th, 2018
'''
'''
Player
	attributes:
	- color, a string, name of stone color
	- move_coordinates, a pair of ints for row and column

	methods:
	- __init__(string), initialize with color
	- set_click(int, int), converts cartesian to row, column and stores
	- make_move(Board), returns False if invalid, otherwise True by
	  checking legal moves stored in Board, uses move_coordinates,
          invokes Board methods to update Board state
'''

from graphics import coords_to_tile
import board


class Player:
    def __init__(self, color):
        self.color = color
        self.move_coordinates = (0,0)

    def set_click(self, x, y):
        self.move_coordinates = coords_to_tile(x,y)

    def make_move(self, game_board):
        game_board.place(self.color, self.move_coordinates)

        # TODO detect legal moves
        return True

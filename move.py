'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''

ROW = "row"
COL = "col"
DIAG = "diag"
SKEW = "skew"

EMPTY = [0, 0]


class Move:
    def __init__(self, coord):
        '''
        :param coord: an int pair, row and col coord of move
        does: constructs an empty Move
        '''

        # set coord
        self.__coord = coord

        # num stones flipped (excludes move stone, itself)
        self.__num_flip = 0

        # range of stones flipped in sequence (num left, num right)
        self.__flip_bounds = {
            ROW : EMPTY,
            COL : EMPTY,
            DIAG : EMPTY,
            SKEW : EMPTY
        }

    def __eq__(self, other):
        '''
        :param other: a move obj, to compare
        :return: a bool, true if same coords, else false
        '''
        return self.__coord == other.__coord

    def __str__(self):
        '''
        :return: a string, displays move data for debugging
        '''
        ret_val = "flip: " + str(self.__num_flip) + " "
        for key in self.__flip_bounds:
            ret_val += str(self.__flip_bounds[key])
        return ret_val

    def set_bound(self, direc, bounds):
        '''
        :param direc: a string, indicating row/col/diag/skew
        :param bounds: an int pair, num to flip before and after move in seq
        :return: an int, 1 new legal move, -1 new illegal move, 0 no change
        '''

        # record starting legality for move count tracking
        start_state = self.is_legal()

        # skip if no change
        if bounds == self.__flip_bounds[direc]:
            return 0

        # record change in num_flip
        self.__num_flip += sum(bounds) - sum(self.__flip_bounds[direc])

        # update flip bound
        self.__flip_bounds[direc] = bounds

        # if legality change track for counting in board
        return self.is_legal() - start_state

    def get_bound(self, direc):
        '''
        :param direc: a string, indicating row/col/diag/skew
        :return: an int pair, bounds, num to flip before and after move in seq
        '''
        return self.__flip_bounds[direc]

    def get_coord(self):
        '''
        :return: an int pair, row and col coord of move
        '''
        return self.__coord

    def get_num_flip(self):
        '''
        :return: an int, number of disks this move will flip
        '''
        return self.__num_flip

    def is_legal(self):
        '''
        :return: True if any flipped, False otherwise
        '''
        return bool(self.__num_flip)

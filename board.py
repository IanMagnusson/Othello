'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''

import move

# constants
EMPTY = ''
P1 = 'black'
P2 = 'white'
PLAYERS = [P1, P2]

# note changes in direction names must be reflected in move dictionary keys
DIRECTIONS = ["row", "col", "diag", "skew"]
STONES = "stones"

class Board:
    def __init__(self, n, matrix = None, cur_player = P1):
        '''
        :param n: an int, num of columns and rows in board
        :param matrix: list of str lists, manual board set up for testing
        :param cur_player: string, manual start player for testing
        does: initializes default board and moves for each player
        '''
        # validate input
        if not (n % 2 == 0 and n > 2):
            print("Error: bad GameState initialization")

        self.__n = n
        self.__cur_player = cur_player


        # dictionary to track stones per player
        self.__num_stones = {
            P1 : 0,
            P2 : 0
        }

        # set stones matrix
        new_stones = []
        self.__stones = [[]]
        if matrix is None:
            new_stones = self.__default_start()
        else:
            new_stones = self.__custom_start(matrix)

        # dictionary of move matrices
        self.__moves = {
            P1 : self.__build_move_matrix(),
            P2 : self.__build_move_matrix()
        }
        # dictionary of lists of legal moves for each player
        self.__legal_moves = {
            P1 : [],
            P2 : []
        }
        # update moves for starting stones
        self.__update_moves(new_stones)

    def __getitem__(self, item):
        '''
        :param item: a pair of ints, coords of a stone to check
        :return: a string, the color of the stone at given coords
        '''
        return self.__stones[item[0]][item[1]]

    def get_n(self):
        '''
        :return: an int, board size
        '''
        return self.__n

    def get_moves(self, player):
        '''
        :param player: a string, player color
        :return: a list of move objects, all the legal moves for player
        '''
        return self.__legal_moves[player]

    def cur_player_num_moves(self):
        '''
        :return: an int, num of current player legal moves
        '''
        return len(self.__legal_moves[self.__cur_player])

    def next_player_num_moves(self):
        '''
        :return: an int, num of next player legal moves
        '''
        # get next player name
        p = PLAYERS[(PLAYERS.index(self.__cur_player) + 1) % len(PLAYERS)]
        return len(self.__legal_moves[p])

    def cur_player_any_moves(self):
        '''
        :return: a bool, True if current player has legal moves, False otherwise
        '''
        return bool(self.cur_player_num_moves())

    def next_player_any_moves(self):
        '''
        :return: a bool, True if next player has legal moves, False otherwise
        '''
        return bool(self.next_player_num_moves())

    def valid_move(self, coord):
        '''
        :param coord: a pair of ints, tile coordinates for desired move
        :return: True if current player legal move, otherwise false
        '''
        # if invalid row and column, illegal move
        if not (0 <= coord[0] < self.__n and 0 <= coord[1] < self.__n):
            return False

        return self.__moves[self.__cur_player][coord[0]][coord[1]].is_legal()

    def place(self, coord):
        '''
        :param coord: a pair of ints, row and column of target tile
        :return: a list of int pairs, row and col of changed tiles for graphics
        does: executes move at coord, flips stones, updates moves
        note: assumes input coords have already been validated by valid_move
        '''

        # build list of new or changed stones
        new_stones = [coord] + self.__flip_list(coord, self.__cur_player)

        # update all changed/new stones
        for stone in new_stones:
            self.__stones[stone[0]][stone[1]] = self.__cur_player

        # update concerned moves for all changed/new stones
        self.__update_moves(new_stones)

        # update current player stone count
        self.__num_stones[self.__cur_player] += len(new_stones)

        # update current player to next player
        self.next_turn()

        # update next player stone count (now that they are cur_player)
        self.__num_stones[self.__cur_player] -= len(new_stones) - 1

        return new_stones

    def next_turn(self):
        '''
        does: advances to cur_player to next player
        '''
        # update current player to next player
        i = (PLAYERS.index(self.__cur_player) + 1) % len(PLAYERS)
        self.__cur_player = PLAYERS[i]

    def get_cur_player(self):
        '''
        :return: a string, current player color
        '''
        return self.__cur_player

    def get_total_stones(self):
        '''
        :return: an int, number of stones on board
        '''
        return self.__num_stones[P1] + self.__num_stones[P2]

    def get_scores(self):
        '''
        :return: an int pair, p1 score, p2 score
        '''
        return(self.__num_stones[P1], self.__num_stones[P2])

    ################private methods###################

    def __update_moves(self, new_stones):
        '''
        :param new_stones: a list of int pairs, coords of new/changed stones
        does: updates all move sequences of a given direction that contain
              the coordinates of the given stones
        '''

        # update moves in all the changed sequences in each direction
        for direc in DIRECTIONS:
            # get indices of changed sequences
            idxs = {self.__get_seq_idx(direc, coord) for coord in new_stones}

            # for each changed sequence...
            for seq_idx in idxs:
                stone_seq = self.__get_seq(STONES, direc, seq_idx)

                # recalc move bounds move in seq for each player
                for player in PLAYERS:
                    moves = self.__get_seq(player, direc, seq_idx)
                    move_bounds = self.__check_moves(player, stone_seq)

                    # set bounds in this direc for each move in seq
                    for i in range(len(moves)):
                        move_change = moves[i].set_bound(direc, move_bounds[i])

                        # update legal move lists
                        if move_change == 1:
                            self.__legal_moves[player].append(moves[i])
                        elif move_change == -1:
                            self.__legal_moves[player].remove(moves[i])

    def __check_moves(self, player, seq):
        '''
        :param player: a string, player stone value
        :param seq: a list of strings, a row/column/diag/skew of stones
        :return: a list of int pairs, move bounds for each position in seq
        '''

        # initialize bounds list
        ret_val = [[0, 0] for i in range(len(seq))]

        state = 0
        last_empty = 0
        last_color = 0

        for i in range(len(seq)):
            # initial state, seek until empty or color
            if state == 0:
                if seq[i] == EMPTY:
                    last_empty = i
                    state = 1
                elif seq[i] == player:
                    last_color = i
                    state = 2

            # empty found, seeking color, track last empty
            elif state == 1:
                if seq[i] == player:
                    # if anything b/t last empty and color, legal move
                    if i - last_empty > 1:
                        ret_val[last_empty][1] = (i - 1) - last_empty
                    last_color = i
                    state = 2
                elif seq[i] == EMPTY:
                    last_empty = i

            # color found, seeking empty, track last color
            elif state == 2:
                if seq[i] == EMPTY:
                    # if anything b/t last color and empty, legal move
                    if i - last_color > 1:
                        ret_val[i][0] = (i - 1) - last_color
                    last_empty = i
                    state = 1
                elif seq[i] == player:
                    last_color = i

        return ret_val

    def __flip_list(self, coord, player):
        '''
        :param coord: an int pair, row and column nums of a move
        :param player: a string, player key
        :return: a list of int pairs, coords for all stones flipped by move
        '''
        flips = []

        for direc in DIRECTIONS:
            # retrieve sequence index and position for move, and flip bounds
            seq_idx = self.__get_seq_idx(direc, coord)
            pos = self.__coord_to_seq_pos(direc, seq_idx, coord)
            bounds = self.__moves[player][coord[0]][coord[1]].get_bound(direc)

            # get coords for negative offsets from first bound
            for i in range(1, bounds[0] + 1):
                flips.append(self.__seq_pos_to_coord(direc, seq_idx, pos - i))

            # get coords for positive offsets from second bound
            for i in range(1, bounds[1] + 1):
                flips.append(self.__seq_pos_to_coord(direc, seq_idx, pos + i))

        return flips

    def __get_seq_idx(self, direc, coord):
        '''
        :param direc: a string, indicating row/col/diag/skew
        :param coord: an int pair, coord of stone to look up
        :return: an ints, index of sequence containing coord
        note: row and col nums start at 0, diag and skew nums are 0 for main
              diag/skew, positive above and negative below
        '''
        # row
        if direc == DIRECTIONS[0]:
            return coord[0]
        # col
        elif direc == DIRECTIONS[1]:
            return coord[1]
        # diag
        elif direc == DIRECTIONS[2]:
            return coord[1] - coord[0]
        # skew
        elif direc == DIRECTIONS[3]:
            return (self.__n - 1) - (coord[0] + coord[1])

        else:
            print("error in Board.__get_seq_idx")

    def __get_seq(self, target, direc, seq_idx):
        '''
        :param target: a string, indicating the target matrix
        :param direc: a string, indicating row/col/diag/skew
        :param seq_idx: index of the sequence to retrieve
        :return: a list of matrix elements, a seq at idx in direc
        note: sequences read left to right except cols read top to bottom
        '''
        # set target matrix
        if target == STONES:
            matrix = self.__stones
        elif target in PLAYERS:
            matrix = self.__moves[target]
        else:
            print("error in Board.__get_seq")

        # build list of elements using coord lookup for each pos in seq
        ret_val = []
        # row or col
        if direc in DIRECTIONS[:2]:
            for i in range(self.__n):
                coord = self.__seq_pos_to_coord(direc, seq_idx, i)
                ret_val.append(matrix[coord[0]][coord[1]])
        # diag or skew
        else:
            for i in range(self.__n - abs(seq_idx)):
                coord = self.__seq_pos_to_coord(direc, seq_idx, i)
                ret_val.append(matrix[coord[0]][coord[1]])

        return ret_val

    def __seq_pos_to_coord(self, direc, seq_idx, pos):
        '''
        :param direc: a string, indicating row/col/diag/skew
        :param seq_idx: an int, index of the sequence to lookup
        :param pos: an int, the position within the sequence
        :return: an int pair, row and col coord of specified position
        '''

        # row
        if direc == DIRECTIONS[0]:
            return (seq_idx, pos)

        # col
        elif direc == DIRECTIONS[1]:
            return (pos, seq_idx)

        # diag
        elif direc == DIRECTIONS[2]:
            if seq_idx > 0:
                return (pos, pos + seq_idx)
            else:
                return (pos - seq_idx, pos)

        # skew
        elif direc == DIRECTIONS[3]:
            if seq_idx > 0:
                return (((self.__n - 1) - seq_idx) - pos, pos)
            else:
                return ((self.__n - 1) - pos, pos - seq_idx)

    def __coord_to_seq_pos(self, direc, seq_idx, coord):
        '''
        :param direc: a string, indicating row/col/diag/skew
        :param seq_idx: an int, index of the seq containing the coords
        :param coord: an int pair, row and column coords
        :return: an int, a position within a sequence in the given direc
        '''
        # row
        if direc == DIRECTIONS[0]:
            return coord[1]

        # col
        elif direc == DIRECTIONS[1]:
            return coord[0]

        # diag
        elif direc == DIRECTIONS[2]:
            if seq_idx > 0:
                return coord[1] - seq_idx
            else:
                return coord[1]

        # skew
        elif direc == DIRECTIONS[3]:
            if seq_idx > 0:
                return coord[1]
            else:
                return coord[1] + seq_idx

    def __custom_start(self, matrix):
        '''
        :param matrix: list of str lists, manual board set up for testing
        :return: a list of int pairs, coords of all new stones
        '''
        n = self.__n
        new_stones = []

        # emplace matrix
        self.__stones = matrix

        # identify non empty stones, count by color, track coords
        for i in range(n):
            for j in range(n):
                if self.__stones[i][j] == P1:
                    self.__num_stones[P1] += 1
                    new_stones.append((i,j))
                elif self.__stones[i][j] == P2:
                    self.__num_stones[P2] += 1
                    new_stones.append((i,j))

        return new_stones

    def __default_start(self):
        '''
        :return: a list of int pairs, coords of all new stones
        does: sets up board with default start
        '''
        n = self.__n
        p1_stones = [(n // 2, n // 2), (n // 2 - 1, n // 2 - 1)]
        p2_stones = [(n // 2 - 1, n // 2), (n // 2, n // 2 - 1)]

        # init empty matrix
        self.__stones = [[EMPTY for i in range(n)] for j in range(n)]

        # place starting stones
        for coord in p1_stones:
            self.__stones[coord[0]][coord[1]] = P1
        for coord in p2_stones:
            self.__stones[coord[0]][coord[1]] = P2

        # update stone counts
        self.__num_stones[P1] += len(p1_stones)
        self.__num_stones[P2] += len(p2_stones)

        return p1_stones + p2_stones

    def __build_move_matrix(self):
        '''
        :return: a list of list of move objects with coordinates set
        '''
        ret_val = []
        for i in range(self.__n):
            l = []
            for j in range(self.__n):
                l.append(move.Move((i, j)))
            ret_val.append(l)
        return ret_val

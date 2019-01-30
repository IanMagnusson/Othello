'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''
'''
NOTE: experimental AI, prototype lacks full optimization for efficiency
also use with board sizes smaller than 6X6 will have undefined behavior
'''


import board
import copy

# constant
THRESHOLD = .50


def pick_move(b):
    '''
    :param b: a board object
    :return: an int pair, coords of the selected move
    note: board must have valid moves for current player
    '''
    n = b.get_n()

    # endgame if board at least threshold percent full
    is_endgame = (b.get_total_stones() / (n**1)) > THRESHOLD

    # build lists of moves sorted by position
    moves = b.get_moves(b.get_cur_player())
    corners = []
    edges = []
    neutral = []
    edge_adjs = []
    corner_adjs = []
    for move in moves:
        coord = move.get_coord()
        if is_corner(coord, n):
            corners.append(move)
        elif is_edge(coord, n):
            edges.append(move)
        elif is_neutral(coord, n):
            neutral.append(move)
        elif not is_corner_adj(coord, n):
            edge_adjs.append(move)
        else:
            corner_adjs.append(move)

    # select move with best outcome from best available position.
    if corners:
        return best_outcome(b, corners, is_endgame)

    elif edges:
        return best_outcome(b, edges, is_endgame)

    elif neutral:
        return best_outcome(b, neutral, is_endgame)

    elif edge_adjs:
        return best_outcome(b, edge_adjs, is_endgame)

    elif corner_adjs:
        return best_outcome(b, corner_adjs, is_endgame)
    else:
        print("an error occurred in ai.pick_move")


def best_outcome(b, move_list, is_endgame):
    '''
    :param b: a board object
    :param move_list: a list of legal moves to assess
    :param is_endgame: a bool, True if endgame tresh passed
    :return: an int pair, row and col coords of the best move
    note: in endgame chooses move with max disks flipped, before endgame
          chooses move with max player moves - opponent moves
    '''
    # track currently found best
    best = move_list[0]

    # if endgame find highest number of disk flips
    if is_endgame:
        for i in range(1, len(move_list)):
            if move_list[i].get_num_flip() > best.get_num_flip():
                best = move_list[i]

    # if not endgame maximize player moves - opponent moves
    else:
        # store best num to avoid expensive recalculation
        best_num = calc_net_moves(b, best)
        for i in range(1, len(move_list)):
            new_num = calc_net_moves(b, move_list[i])
            if new_num > best_num:
                best = move_list[i]
                best_num = new_num

    return best.get_coord()


def calc_net_moves(b, move):
    '''
    :param b: a board object, will copy and use for analysis
    :param move: a move object to test
    :return: an int, player moves - opponent moves after play
    note: this is an experimental feature, further work needed for efficiency
    '''
    duplicate = copy.deepcopy(b)

    # test move on board copy
    duplicate.place(move.get_coord())

    # place has caused cur player to advance so reverse request
    return duplicate.next_player_num_moves() - duplicate.cur_player_num_moves()


def is_corner(coord, n):
    '''
    :param coord: an int pair, row and col coords
    :param n: an int, size of board
    :return: a bool, True if coord is corner, else false
    '''
    corners = [(0, 0), (n-1, 0), (0, n-1), (n-1, n-1)]
    return coord in corners


def is_edge(coord, n):
    '''
    :param coord: an int pair, row and col coords
    :param n: an int, size of board
    :return: a bool, True if coord is edge and not adj to corner, else false
    '''
    if coord[0] == 0 and 1 < coord[1] < n-2:
        return True
    elif 1 < coord[0] < n-2 and coord[1] == 0:
        return True
    elif coord[0] == n-1 and 1 < coord[1] < n-2:
        return True
    elif 1 < coord[0] < n-2 and coord[1] == n-1:
        return True
    else:
        return False


def is_neutral(coord, n):
    '''
    :param coord: an int pair, row and col coords
    :param n: an int, size of board
    :return: a bool, True if coord not in outer 2 rings of coords, else false
    '''
    return 1 < coord[0] < n-2 and 1 < coord[1] < n-2


def is_corner_adj(coord, n):
    '''
    :param coord: an int pair, row and col coords
    :param n: an int, size of board
    :return: a bool, True if coord adjacent to corner, else false
    '''
    corner_adjs = [(0,1), (1, 0), (1,1),
                   (0, n-2), (1, n-1), (1, n-2),
                   (n-2, 0), (n-1, 1), (n-2, 1),
                   (n-2, n-1), (n-1, n-2), (n-2, n-2)]
    return coord in corner_adjs

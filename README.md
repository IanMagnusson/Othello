# Othello
```
Ian Magnusson
CS5001
November 18th, 2018

This is the final project for a class in CS fundamentals thru intesive python development.
The base assignment was to implement the board game othello and an AI that randomly picks
legal moves. I chose to push farther and performance-optimized the computation of legal moves
by storing unchanged information and only updating move information that had been changed by
a given move. This also allowed me to develop a more advanced AI that selects moves based both
on board position and outcomes on stones flipped and number of future moves opened.

----Othello design----

CLASSES:

GameState
	
	A class that mediates board information, player input, graphics, and AI. Serves
	many of the functions that would otherwise fall into main in Othello.py but for
	the assignment constraint of using turtle.onscreenclick. To use simply initialize
	an instance and call human more with click coordinates, and internal calls will 
	handle the rest.
	
     |  Methods defined here:
     |  
     |  __init__(self)
     |      initializes board and displays
     |  
     |  human_move(self, x, y)
     |      :parameters x and y, ints, cartesian coordinates provided by
     |       turtle.onscreenclick
     |      does: processes move if legal and hands over to comp, if illegal move
     |       waits for valid human move, if no legal human moves skips, if no
     |       moves remaining on board invokes ending
	
Board

	A class that tracks stone locations and legal moves. Move information is stored in
	matricies of Move objects that are designed to performance optimize both the lookup
	and updating of legal moves as compared to computing them on the fly on stone placement.
	This takes advantage of the fact that legal moves are only changed when a stone in the
	same row, column, diagonal, or skew diagonal is also changed.
	
     |  Methods defined here:
     |  
     |  __getitem__(self, item)
     |      :param item: a pair of ints, coords of a stone to check
     |      :return: a string, the color of the stone at given coords
     |  
     |  __init__(self, n, matrix=None, cur_player='black')
     |      :param n: an int, num of columns and rows in board
     |      :param matrix: list of str lists, manual board set up for testing
     |      :param cur_player: string, manual start player for testing
     |      does: initializes default board and moves for each player
     |  
     |  cur_player_any_moves(self)
     |      :return: a bool, True if current player has legal moves, False otherwise
     |  
     |  cur_player_num_moves(self)
     |      :return: an int, num of current player legal moves
     |  
     |  get_cur_player(self)
     |      :return: a string, current player color
     |  
     |  get_moves(self, player)
     |      :param player: a string, player color
     |      :return: a list of move objects, all the legal moves for player
     |  
     |  get_n(self)
     |      :return: an int, board size
     |  
     |  get_scores(self)
     |      :return: an int pair, p1 score, p2 score
     |  
     |  get_total_stones(self)
     |      :return: an int, number of stones on board
     |  
     |  next_player_any_moves(self)
     |      :return: a bool, True if next player has legal moves, False otherwise
     |  
     |  next_player_num_moves(self)
     |      :return: an int, num of next player legal moves
     |  
     |  next_turn(self)
     |      does: advances to cur_player to next player
     |  
     |  place(self, coord)
     |      :param coord: a pair of ints, row and column of target tile
     |      :return: a list of int pairs, row and col of changed tiles for graphics
     |      does: executes move at coord, flips stones, updates moves
     |      note: assumes input coords have already been validated by valid_move
     |  
     |  valid_move(self, coord)
     |      :param coord: a pair of ints, tile coordinates for desired move
     |      :return: True if current player legal move, otherwise false

Move
	A class storing information on a single legal move. Tracks location, number of
	stones flipped if this move is played, and the extent in each direction of stones
	to be flipped.
	
     |  Methods defined here:
     |  
     |  __eq__(self, other)
     |      :param other: a move obj, to compare
     |      :return: a bool, true if same coords, else false
     |  
     |  __init__(self, coord)
     |      :param coord: an int pair, row and col coord of move
     |      does: constructs an empty Move
     |  
     |  __str__(self)
     |      :return: a string, displays move data for debugging
     |  
     |  get_bound(self, direc)
     |      :param direc: a string, indicating row/col/diag/skew
     |      :return: an int pair, bounds, num to flip before and after move in seq
     |  
     |  get_coord(self)
     |      :return: an int pair, row and col coord of move
     |  
     |  get_num_flip(self)
     |      :return: an int, number of disks this move will flip
     |  
     |  is_legal(self)
     |      :return: True if any flipped, False otherwise
     |  
     |  set_bound(self, direc, bounds)
     |      :param direc: a string, indicating row/col/diag/skew
     |      :param bounds: an int pair, num to flip before and after move in seq
     |      :return: an int, 1 new legal move, -1 new illegal move, 0 no change




AI module
	
	These functions consititue an othello AI that prioritizes positions (corners,
	then edges, then neutral positions in the middle, then dangerous spaces adjacent
	to edges, and finally spaces adjacent to corners), and it also looks into the outcome
	of the move for the next board. It judges the outcome differently before and after a
	threshold of how full the board is. In the early game it attempts to maximize the
	number of its own moves open minus the number of the humans moves. In the end game
	it gets aggressive and picks moves that flip the most stones.
	
	Future development: output a probability distribution of all possible moves instead of
	a single determined pick. This distribution would be weighted by parameters that could
	be optimized with ML. This would require defining some kind of a reward function (a way
	to judge the desirability of an outcome board state).
	

	FUNCTIONS
    best_outcome(b, move_list, is_endgame)
        :param b: a board object
        :param move_list: a list of legal moves to assess
        :param is_endgame: a bool, True if endgame tresh passed
        :return: an int pair, row and col coords of the best move
        note: in endgame chooses move with max disks flipped, before endgame
              chooses move with max player moves - opponent moves
    
    calc_net_moves(b, move)
        :param b: a board object, will copy and use for analysis
        :param move: a move object to test
        :return: an int, player moves - opponent moves after play
        note: this is an experimental feature, further work needed for efficiency
    
    is_corner(coord, n)
        :param coord: an int pair, row and col coords
        :param n: an int, size of board
        :return: a bool, True if coord is corner, else false
    
    is_corner_adj(coord, n)
        :param coord: an int pair, row and col coords
        :param n: an int, size of board
        :return: a bool, True if coord adjacent to corner, else false
    
    is_edge(coord, n)
        :param coord: an int pair, row and col coords
        :param n: an int, size of board
        :return: a bool, True if coord is edge and not adj to corner, else false
    
    is_neutral(coord, n)
        :param coord: an int pair, row and col coords
        :param n: an int, size of board
        :return: a bool, True if coord not in outer 2 rings of coords, else false
    
    pick_move(b)
        :param b: a board object
        :return: an int pair, coords of the selected move
        note: board must have valid moves for current player
	

Graphics module

	Functions to render an othello game in turtle graphics and covert between
	cartesian coordinate and row, column cordinate systems.

	FUNCTIONS
    coords_to_tile(x, y, n)
        :param x: an int, cartesian coord
        :param y: an int, cartesian coord
        :param n: an int, number of tiles per side
        :return: returns a pair of ints, row and column coords
    
    display(board, n)
        :param board: a Board object to be displayed
        :param n: an int, size of board
        does: draw entire board and all stones
    
    draw_board(n)
        Function: draw_board
        Parameters: n, an int for # of squares
        Returns: nothing
        Does: Draws an nxn board with a green background
        note: this is starter code not by Ian
    
    draw_lines(turt, n)
        note: this is starter code not by Ian
    
    draw_stone(color, tile, n)
        :param color: a string, name of color to draw circle
        :param coord: a pair of ints, row and col coords for stone draw
        :param n: an int, size of board
        :return: none
    
    get_base_coords(n)
        :param n: an int, number of tiles per side
        :return: a pair of ints, coords of top left corner
    
    tile_to_coords(row, column, n)
        :param row: an int, row coord
        :param column: an int, column coord
        :param n: an int, number of tiles per side
        :return: returns a pair of ints, x and y cartesian coords

	
PSEUDOCODE FOR Board.__check_moves:
# this method handles the efficient updating of legal moves information
# for every row, column, diagonal, or skew diagonal (here refered to as
# sequences)

check that sequence has more than one color in it and at least one empty tile

for color in colors:
	iterate thru tiles until empty or color found
	if empty:
		enter state1
	if color:
		enter state2

state1:
	iterate until color position, saving last empty position
	if end of sequence before color:
		no new move, proceed to next color in colors
	
	if both positions exist and are not adjacent:
		record last empty as move and pos b/t as tiles flipped
		enter state2

	if positions are adjacent:
		no new move, just enter state2

state2:
	iterate until empty position, saving last color position
	if end of sequence before empty:
		no new move, proceed to next color in colors
	
	if both positions exist and are not adjacent:
		record empty pos as move and pos b/t as tiles flipped
		enter state1

	if positions are adjacent:
		no new move, just enter state1
  
```

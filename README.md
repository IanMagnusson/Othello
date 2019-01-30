# Othello
Ian Magnusson
CS5001
Homework 6
November 18th, 2018


notes on AI design:

- Did you attempt to make your computer player very smart -- i.e., do something more clever than just pick a random legal move?

Yes, in it's current state it prioritizes positions (corners, then edges, then neutral positions in the middle, then dangerous spaces adjacent to edges, and finally spaces adjacent to corners), and it also looks into the outcome of the move for the next board. It judges the outcome differently before and after a threshold of how full the board is. In the early game it attempts to maximize the number of its own moves open minus the number of the humans moves. In the end game it gets aggressive and picks moves that flip the most stones.

- If so, were you able to accomplish this? Is your computer player as smart as you would like?

I realized late in the process just how hard it would be to test the AI, because the amount of work it takes to manually test any but the most simple and contrived boards. Nevertheless to the best of my ability to test it, seems to be behaving as predicted. I'm less certain that these are actually the best possible strategies. Originally I had hoped to create a more general approach that would parameterize the AI's behavior on the basis of general features. The idea was to make a framework that I could later approach with ML techniques to optimize the parameters of the AI's behavior. Sadly I have had to choose between learning the math I would need for that and focusing on the more pressing math studies in Discrete Structures. I still believe that I have made a good Othello platform that efficiently computes changes in board state without having to touch all objects.

- How did you determine which piece to play next?  Tell us about your “pick next move” algorithm.

pick_move sorts the current players moves into lists based on the different categories of positions. It then take the best available category and assesses each move in the category on the basis of an outcome evaluation. This evaluation differs based on the previously discussed threshold state. In the end game state the algorithm simply queries each move for how many stones it will flip (something it already tracks every time it is updated). In the beginning game state the algorithm is considerably less efficient. It makes a deep copy of the board and tests each move and then counts the resulting moves that are then available. This could be made more efficient by using the test board of the selected move to continue playing on rather than having to compute the selected move twice (once for testing and again on the main play board). I choose to focus my efforts on efficiency in the underlying board platform rather than in the experimental AI, however, as I believe I will be better prepared to work on the AI in the future. 

- How often did your computer program beat you, or your friends, or whoever tested it out for you?

After I got the AI to its current state I was unable to beat it for a while, and I still only beat it every now and then. Its deterministic behavior would make it vulnerable to an opponent with more time to consider moves.

- How would you improve it in the future?

I would precede as originally planned and find a way to output a probability distribution of all possible moves instead of a single determined pick. This distribution would be weighted by parameters that could be optimized with ML. This would require defining some kind of a reward function (ie a way to judge the desirability of an outcome board state). This seems like the most interesting problem to solve as the game of Othello is small enough that it is possible to Brute force with enough time.


----Othello design----

CLASSES:

GameState
	attributes:
	- game_board, a Board object, the main game space
	- comp_turn, a bool, True if computer's turn, False if human's turn

	methods:
	- __init__(int), initialize with board size; note requires even n value 
	- human_move(int, int), used with onscreen click. it attempts human move
	  until valid click, then invokes computer move. Human skipped if no 
	  valid moves and if neither have moves left invokes end condition and
	  score file i/o
	- computer_move(), uses AI module to select and play a move and then invoke
	  human_move (within onscreen click), skips comp turn if they have no valid
	  moves left. and if neither have moves left invokes end condition and
	  score file i/o

Board
	attributes:
	- stones, a list of lists of strings, stone colors or '' for empty
	- human_moves, a matrix of Move objects for human
	- comp_moves, a matrix of Move objects for the computer
	
	methods:
	- __init__(list of list of strings), initialize w/ color matrix,
	  this will first build a matrix of stone color strings and then
	  build Moves dictionary with colors as keys and matrices of
	  Moves as values. Moves will be computed using the check_moves
	  method on each row/column/diag containing a non-empty tile.
	- __getitem__(self, a pair of ints), return stone color at coords

	- process_move(string, pair of ints), execute move for color
	  designated by string and at coordinates given by pair of ints.
	  Checks if valid (returns True if yes, else False). Adds stone at
	  given coordinates and flips stones designated by corresponding Move
	  object. Tracks rows/columns/diags with new or flipped stones and
	  calls check_moves on each of these to update moves dictionary.

	- check_moves(list of stones, list of moves), updates Moves for a
	  given row, column, diagonal, or skew diagonal based on its sequence
	  of stones and empty tiles (see check_moves pseudocode below)

	# return lists containing a given sequence of Moves or stone colors
	- get_move_row(int, color)
	- get_move_column(int, color)
	- get_move_diagonal(int, color)
	- get_move_skew_diagonal(int, color)
	- get_stone_row(int)
	- get_stone_column(int)
	- get_stone_diagonal(int)
	- get_stone_skew_diagonal(int)

	- deep_copy(), returns Board object with copied values (for AI)

Move
	attributes:
	- legal, a bool (True if any coordinates in will_flip)
	- coordinates, a pair of ints, row and column of possible move
	- num_flip, an int, number of disks this move will flip
	- will_flip, a dictionary with "row", "column", "diagonal", and
	  "skew diagonal" as keys and values for each as a pair of indexes
	  for the range of stones that will change color 
	
	methods:
	- __eq__(self, pair of ints), compares with coordinate pair
	- set_flip(string, (int, int)), set will_flip[string] to given range,
	  if set to no flips in this direction, checks if any flips left, if
	  none left then set illegal.

AI module
	functions:
	- pick_move(Board, string), given a Board object and a color name
	  evaluates moves in Board by invoking helper functions, selects
	  highest rank move.
	- evaluate_positions(Board, string), returns a list of ranks
	  corresponding to each move of the given color, weighted to 
	  prioritize corners, then edges and avoid tiles adjacent to corners,
	  then tiles adjacent to edges.
	- evaluate_outcomes(Board, string), returns a list of ranks
	  corresponding to each move of the given color, weighted to 
	  minimum disks flipped, until board fill threshold is reached and
	  to maximize the number of moves the comp has over the player,
	  this is achieved by deep copying the Board and recording the
	  outcomes after testing each move. (If time allows I will implement
	  this to go to an arbitrary depth of future moves).	

Graphics module
	functions:
	- display(Board), renders the current board state in turtle graphics
	- draw_board(int), code from instructor
	- draw_lines(turtle, int), code from instructor
	- draw_circle(string, pair of ints), draws a stone of given color 
	  at coords
	- coords_to_tile(int, int, int), maps cartesian coordinates
	  onto row/column coordinates given num rows/columns
	- tile_to_coords(int, int, int), expands row and column coords to
	  cartesian coordinates in the middle of the specified tile, given
	  the number of rows/columns
	
PSEUDOCODE FOR Board.check_moves:
# note that this algorithm works for an arbitrary number of colors

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

DRIVER:
	# note: because of onscreenclick driver is very short and I have
	#	also included driver like method gamestate.attempt_move

main():
	- initialize GameState object with board size, colors, first player
	 is human and second player is comp
	- display starting board
	- call onscreen click with gamestate.attempt_move and prevent
	 window from closing with turtle.done method.

gamestate.attempt_move(x, y):
	- convert cartesian coords to row and column pair
	- attempt move, if illegal do not advance to next player
	- if no moves left, announce scores and winner, invoke score i/o
	- if move legal, invoke board.process_move, render board, and then
	 turn off click and invoke comp move (comp move will render again
 	 after it finishes and turn human player click back on. If no valid
	 human moves after comp move, human turn is skipped)

WISHLIST:
- board state saves and loads
- AI war gaming to arbitrary depth of future moves (tree data structure?)
- investigate possibility of storing move rank in move and only recomputing
  move ranks when they are changed

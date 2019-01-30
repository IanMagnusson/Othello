'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''

import turtle

# constants

SQUARE = 50
HALF_SQUARE = SQUARE / 2
STONE_SIZE = 20


def coords_to_tile(x, y, n):
    '''
    :param x: an int, cartesian coord
    :param y: an int, cartesian coord
    :param n: an int, number of tiles per side
    :return: returns a pair of ints, row and column coords
    '''
    # normalize to origin at top left
    base = get_base_coords(n)
    x = x - base[0]
    y = y - base[1]

    # reflect over x axis
    y = -y

    # map to tiles
    row = int(y // SQUARE)
    column = int(x // SQUARE)

    return [row, column]


def tile_to_coords(row, column, n):
    '''
    :param row: an int, row coord
    :param column: an int, column coord
    :param n: an int, number of tiles per side
    :return: returns a pair of ints, x and y cartesian coords
    '''
    # expand to middle of range mapped to tile
    x = column * SQUARE + SQUARE / 2
    y = row * SQUARE + SQUARE / 2

    # reflect over x axis
    y = -y

    # normalize to origin in center
    base = get_base_coords(n)
    x = x + base[0]
    y = y + base[1]

    return [x, y]


def get_base_coords(n):
    '''
    :param n: an int, number of tiles per side
    :return: a pair of ints, coords of top left corner
    '''
    base_x = -(n * (SQUARE / 2))
    base_y = n * (SQUARE / 2)
    return (base_x, base_y)


def display(board, n):
    '''
    :param board: a Board object to be displayed
    :param n: an int, size of board
    does: draw entire board and all stones
    '''

    draw_board(n)

    # for each non-empty tile, draw a stone of the appropriate color
    for row in range(n):
        for column in range(n):
            color = board[(row, column)]
            if color:
                # draw circle at cartesian coordinates using conversion func
                draw_stone(color, (row, column), n)


def draw_stone(color, tile, n):
    '''
    :param color: a string, name of color to draw circle
    :param coord: a pair of ints, row and col coords for stone draw
    :param n: an int, size of board
    :return: none
    '''

    # convert to cartesian coordinates
    coord = tile_to_coords(tile[0], tile[1], n)

    # offset coords because circle is drawn from edge
    coord[1] = coord[1] - STONE_SIZE

    # setup turtle
    turt = turtle.Turtle()
    turt.ht()
    turt.speed(0)
    turt.color(color)

    # draw circle at coords
    turt.penup()
    turt.goto(*coord)
    turt.begin_fill()
    turt.circle(STONE_SIZE)
    turt.end_fill()


def draw_board(n):
    ''' Function: draw_board
        Parameters: n, an int for # of squares
        Returns: nothing
        Does: Draws an nxn board with a green background
        note: this is starter code not by Ian
    '''

    turtle.setup(n * SQUARE + SQUARE, n * SQUARE + SQUARE)
    turtle.screensize(n * SQUARE, n * SQUARE)
    turtle.bgcolor('white')

    # Create the turtle to draw the board
    othello = turtle.Turtle()
    othello.penup()
    othello.speed(0)
    othello.hideturtle()

    # Line color is black, fill color is green
    othello.color("black", "forest green")

    # Move the turtle to the upper left corner
    corner = -n * SQUARE / 2
    othello.setposition(corner, corner)

    # Draw the green background
    othello.begin_fill()
    for i in range(4):
        othello.pendown()
        othello.forward(SQUARE * n)
        othello.left(90)
    othello.end_fill()

    # Draw the horizontal lines
    for i in range(n + 1):
        othello.setposition(corner, SQUARE * i + corner)
        draw_lines(othello, n)

    # Draw the vertical lines
    othello.left(90)
    for i in range(n + 1):
        othello.setposition(SQUARE * i + corner, corner)
        draw_lines(othello, n)


def draw_lines(turt, n):
    '''note: this is starter code not by Ian
    '''
    turt.pendown()
    turt.forward(SQUARE * n)
    turt.penup()

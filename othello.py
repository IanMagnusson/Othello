'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''

import turtle
import gamestate


def main():
    # launch game
    game = gamestate.GameState()

    # process moves on click, exits when no moves left
    turtle.onscreenclick(game.human_move)

    # do not close turtle window until program exit
    turtle.done()

main()

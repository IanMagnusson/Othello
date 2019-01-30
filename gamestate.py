'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''
import time
import board
import graphics
import turtle
import ai

# constants
N = 8
SCORES_FILENAME = "scores.txt"

class GameState:
    def __init__(self):
        '''
        initializes board and displays
        '''
        self.board = board.Board(N)

        # display turtle graphics first time
        graphics.display(self.board, N)

    def human_move(self, x, y):
        '''
        :parameters x and y, ints, cartesian coordinates provided by
         turtle.onscreenclick
        does: processes move if legal and hands over to comp, if illegal move
         waits for valid human move, if no legal human moves skips, if no
         moves remaining on board invokes ending
        '''
        # convert cartesian coords to row and column pair
        tile = graphics.coords_to_tile(x, y, N)

        # handle no valid moves
        if not self.board.cur_player_any_moves():
            if not self.board.next_player_any_moves():
                self.__ending()
                return
            else:
                # pass without stone placement
                self.board.next_turn()
                self.__comp_move()
                return

        # validate move, if illegal do not advance to next player
        if not self.board.valid_move(tile):
            return

        self.__execute_move(tile)

        # turn success, comp next
        self.__comp_move()
        return

    def __comp_move(self):
        '''
        does: deactivates click until passing control back to human, if no
         legal comp moves skips to human, if no moves remaining on board
         invokes ending, otherwise invokes AI to choose move and execute and
         then passes control back to human.
        '''

        # announce turn
        print("\nComputer turn\n")

        # uncomment for patronizing AI personality
        # time.sleep(1)
        # print("... thinking ...\n")
        # time.sleep(1)

        # deactivate human control
        turtle.onscreenclick(None)

        # handle no valid moves
        if not self.board.cur_player_any_moves():
            if not self.board.next_player_any_moves():
                self.__ending()
                return
            else:
                # pass without stone placement
                self.board.next_turn()
                turtle.onscreenclick(self.human_move)
                print("Human turn\nClick to advance play!!")
                return

        # select a move
        tile = ai.pick_move(self.board)

        self.__execute_move(tile)

        # turn success, human next
        turtle.onscreenclick(self.human_move)
        print("Human turn\nClick to advance play!!")
        return

    def __execute_move(self, coord):
        '''
        :param coord: an int pair, row and column coord of move to execute
        does: executes move, and draws changes to screen
        '''
        # select a move, execute, track changed stones for graphics
        cur_player = self.board.get_cur_player()
        new_stones = self.board.place(coord)

        # draw changed stones
        for stone in new_stones:
            graphics.draw_stone(cur_player, stone, N)

    def __ending(self):
        '''
        does: announces winner, scores for both players, saves score to file
        '''
        # deactivate human control
        turtle.onscreenclick(None)

        scores = self.board.get_scores()
        if scores[0] > scores[1]:
            print("Human win, long live Sarah Connor!!")
        else:
            print("Computer wins, go back in time and practice othello more!")

        print("Human scored", scores[0])
        print("Computer scored", scores[1])

        player_name = input("Enter your name for posterity\n")
        self.__write_scores(SCORES_FILENAME, player_name, scores[0])

        exit(1)

    def __write_scores(self, filename, player_name, score):
        '''
        parameter:  a string specifying the filename containing a list of words
                    a string specifying the players name to be recorded
                    an int specifying the score to be recorded
        note: this code is from an earlier assignment also written by Ian
        '''
        try:
            # open for read and write
            outfile = open(filename, "a+")

            # read first line
            outfile.seek(0)
            high = outfile.readline().split()

            # if first line valid and lower than new score, prepend new score
            if len(high) > 1 and high[-1].isdigit() and int(high[-1]) < score:
                # copy existing, clear, write new score, append copy
                outfile.seek(0)
                copy = outfile.read()
                outfile.truncate(0)
                outfile.write(player_name + ' ' + str(score) + '\n' + copy)

            # otherwise append score to end of data
            else:
                outfile.seek(0, 2)
                outfile.write(player_name + ' ' + str(score) + '\n')

            outfile.close()
        except OSError:
            print("Error writing file: %s" % filename)

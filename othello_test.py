'''
Ian Magnusson
CS5001
Homework 7
December 2nd, 2018
'''

'''
NOTES ON TESTING:
the problem space for this program is not within the scope of manual testing
testing of every last case. I have focused on testing top level methods for
all desired behaviors across a sampling of possible cases. I have not tested
 getters and setters and utility funcs that are fully embedded in other tested
  functions. I also have not tested the functions in gamestate as that is
  effectively the driver (with the exception of write file which is identical
  to its implementation in HW5 where it is throughout unittessted.
'''

import unittest
import ai
import board
import move
import graphics



FOUR_START_B =    ["flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                    "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                    "flip: 1 [0, 0][0, 1][0, 0][0, 0]",
                    "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                    "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                    "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                    "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                    "flip: 1 [1, 0][0, 0][0, 0][0, 0]",
                    "flip: 1 [0, 1][0, 0][0, 0][0, 0]",
                    "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                   "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                   "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                   "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                   "flip: 1 [0, 0][1, 0][0, 0][0, 0]",
                   "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                   "flip: 0 [0, 0][0, 0][0, 0][0, 0]"]
FOUR_START_W = ["flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 1 [0, 0][0, 1][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 1 [0, 1][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 1 [1, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]",
                "flip: 1 [0, 0][1, 0][0, 0][0, 0]",
                "flip: 0 [0, 0][0, 0][0, 0][0, 0]"]

class AITest(unittest.TestCase):
    def test_pick_move(self):
        # only one move
        matrix = [['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', 'white', 'black', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (3,2))

        # edge adj or neutral -> neutral
        matrix = [['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', 'white', 'black', 'white', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (3,5))

        # edge adj or corner adj -> edge adj
        matrix = [['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', 'white', '', '', '', '', ''],
                  ['', '', 'white', 'black', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)

        # neutral or edge -> edge
        self.assertEqual(ai.pick_move(b), (3,1))
        matrix = [['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', 'white', '', '', '', ''],
                  ['', '', '', 'black', '', '', '', ''],
                  ['', '', '', 'white', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (7,3))

        # corner or edge -> corner
        matrix = [['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', 'white', ''],
                  ['', '', '', '', '', 'black', '', ''],
                  ['', '', '', '', '', '', 'white', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (7,7))

        # all options -> corner
        matrix = [['', 'black', '', '', '', '', '', ''],
                  ['', 'white', '', '', '', '', 'white', ''],
                  ['', '', '', '', '', 'black', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', 'black', 'white', '', '', ''],
                  ['', 'black', '', '', '', 'black', 'white', ''],
                  ['', 'white', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (0,7))

        # net moves 2 or 0 -> 2
        matrix = [['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', 'white', '', '', '', '', ''],
                  ['', '', '', 'white', 'black', '', '', ''],
                  ['', '', '', '', 'white', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (3,2))

        # past game threshold; flip 2 or 1 -> flip 2
        matrix = [['white', 'white', 'white', 'white',
                   'white', 'white', 'white', 'white'],
                  ['white', 'white', 'white', 'white',
                   'white', 'white', 'white', 'white'],
                  ['white', 'white', 'white', 'white',
                   'white', 'white', 'white', 'white'],
                  ['white', 'white', 'white', 'white',
                   'white', 'white', 'white', 'white'],
                  ['', '', 'black', 'white', 'white', '', '', ''],
                  ['', '', 'white', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]
        b = board.Board(8, matrix)
        self.assertEqual(ai.pick_move(b), (4,5))



class BoardTest(unittest.TestCase):
    def test_init(self):
        b = board.Board(4)

        self.assertEqual(b._Board__stones,
                         [['', '', '', ''],
                          ['', 'black', 'white', ''],
                          ['', 'white', 'black', ''],
                          ['', '', '', '']])
        i = 0
        for line in b._Board__moves["black"]:
            for j in range(len(line)):
                self.assertEqual(str(line[j]), FOUR_START_B[i])
                i+=1

        i = 0
        for line in b._Board__moves["white"]:
            for j in range(len(line)):
                self.assertEqual(str(line[j]), FOUR_START_W[i])
                i+=1

        expected = [(1, 0), (2, 3), (0, 1), (3, 2)]
        white_moves = b._Board__legal_moves["white"]
        for i in range(len(white_moves)):
            self.assertEqual(white_moves[i].get_coord(), expected[i])

        black_moves = b._Board__legal_moves["black"]
        expected = [(1, 3), (2, 0), (3, 1), (0, 2)]
        for i in range(len(black_moves)):
            self.assertEqual(black_moves[i].get_coord(), expected[i])

        matrix = [['black', 'white', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', '', '']]

        b = board.Board(8, matrix)
        self.assertEqual(len(b._Board__legal_moves['white']), 0)
        self.assertEqual(len(b._Board__legal_moves['black']), 1)
        coord = b._Board__legal_moves['black'][0].get_coord()
        self.assertEqual(coord, (0, 2))

    def test_valid_move(self):
        matrix = [['', '', '', ''],
                ['', 'black', 'white', ''],
                ['', '', '', ''],
                ['', '', '', '']]
        b = board.Board(4, matrix)
        self.assertTrue(b.valid_move((1,3)))
        self.assertFalse(b.valid_move((1,0)))

        b = board.Board(4, matrix, 'white')
        self.assertTrue(b.valid_move((1,0)))

    def test_place(self):
        matrix = [['', '', '', ''],
                ['', 'black', '', ''],
                ['', 'white', '', ''],
                ['', '', '', '']]
        b = board.Board(4, matrix)
        b.place((3,1))
        self.assertEqual(b._Board__stones,
                         [['', '', '', ''],
                        ['', 'black', '', ''],
                        ['', 'black', '', ''],
                        ['', 'black', '', '']])
        self.assertFalse(b.cur_player_any_moves())
        self.assertFalse(b.next_player_any_moves())

        matrix = [['', '', '', ''],
                ['', 'black', '', ''],
                ['', '', 'white', ''],
                ['', '', '', '']]
        b = board.Board(4, matrix)
        b.place((3,3))
        self.assertEqual(b._Board__stones,
                         [['', '', '', ''],
                        ['', 'black', '', ''],
                        ['', '', 'black', ''],
                        ['', '', '', 'black']])
        self.assertFalse(b.cur_player_any_moves())
        self.assertFalse(b.next_player_any_moves())

        matrix = [['', '', '', ''],
                ['', 'white', '', ''],
                ['', '', 'black', ''],
                ['', '', '', '']]
        b = board.Board(4, matrix)
        b.place((0,0))
        self.assertEqual(b._Board__stones,
                         [['black', '', '', ''],
                        ['', 'black', '', ''],
                        ['', '', 'black', ''],
                        ['', '', '', '']])
        self.assertFalse(b.cur_player_any_moves())
        self.assertFalse(b.next_player_any_moves())
        matrix = [['', '', '', ''],
                ['', '', '', 'black'],
                ['', '', 'white', ''],
                ['', '', 'white', 'black']]
        b = board.Board(4, matrix)
        b.place((3,1))
        self.assertEqual(b._Board__stones,
                         [['', '', '', ''],
                        ['', '', '', 'black'],
                        ['', '', 'black', ''],
                        ['', 'black', 'black', 'black']])
        self.assertFalse(b.cur_player_any_moves())
        self.assertFalse(b.next_player_any_moves())

    def test_next_turn(self):
        b = board.Board(16)
        b.next_turn()
        self.assertEqual(b.get_cur_player(), "white")
        b.next_turn()
        self.assertEqual(b.get_cur_player(), "black")


class MoveTest(unittest.TestCase):
    def test_init(self):
        m = move.Move((1, 1))
        self.assertEqual(m._Move__coord, (1,1))
        self.assertEqual(m._Move__num_flip, 0)
        self.assertEqual(m._Move__flip_bounds,
                         {"row":[0, 0],"col":[0, 0],
                          "diag":[0, 0],"skew":[0, 0]} )

    def test_eq(self):
        m1 = move.Move((10, 5))
        m2 = move.Move((10, 5))
        self.assertEqual(m1, m1)
        self.assertEqual(m1, m2)

    def test_str(self):
        m = move.Move((6, 10))
        self.assertEqual(str(m), 'flip: 0 [0, 0][0, 0][0, 0][0, 0]')

    def test_set_bound(self):
        m = move.Move((8, 12))
        ret = m.set_bound("row", [2,1])
        self.assertEqual(m._Move__num_flip, 3)
        self.assertEqual(ret, 1)
        ret = m.set_bound("row", [2,1])
        self.assertEqual(m._Move__num_flip, 3)
        self.assertEqual(ret, 0)
        ret = m.set_bound("row", [2,2])
        self.assertEqual(m._Move__num_flip, 4)
        self.assertEqual(ret, 0)
        ret = m.set_bound("col", [4,0])
        self.assertEqual(m._Move__num_flip, 8)
        self.assertEqual(ret, 0)
        ret = m.set_bound("row", [0,0])
        self.assertEqual(m._Move__num_flip, 4)
        self.assertEqual(ret, 0)
        ret = m.set_bound("col", [0,0])
        self.assertEqual(m._Move__num_flip, 0)
        self.assertEqual(ret, -1)

class GraphicsTest(unittest.TestCase):
    def test_coords_to_tile(self):
        self.assertEqual(graphics.coords_to_tile(-100, 100, 4), [0, 0])
        self.assertEqual(graphics.coords_to_tile(-50, 50, 4), [1, 1])
        self.assertEqual(graphics.coords_to_tile(0, 0, 4), [2, 2])
        self.assertEqual(graphics.coords_to_tile(100, 100, 4), [0, 4])
        self.assertEqual(graphics.coords_to_tile(100, -100, 4), [4, 4])
        self.assertEqual(graphics.coords_to_tile(-100, -100, 4), [4, 0])
        self.assertEqual(graphics.coords_to_tile(-25, 25, 1), [0, 0])
        self.assertEqual(graphics.coords_to_tile(75, -75, 3), [3, 3])

    def test_tile_to_coords(self):
        self.assertEqual(graphics.tile_to_coords(0,0,4), [-75.0, 75.0])
        self.assertEqual(graphics.tile_to_coords(1,1,4), [-25.0, 25.0])
        self.assertEqual(graphics.tile_to_coords(2,2,4), [25.0, -25.0])
        self.assertEqual(graphics.tile_to_coords(0,4,4), [125.0, 75.0])
        self.assertEqual(graphics.tile_to_coords(4,4,4), [125.0, -125.0])
        self.assertEqual(graphics.tile_to_coords(4,0,4), [-75.0, -125.0])
        self.assertEqual(graphics.tile_to_coords(0,0,1), [0.0, 0.0])
        self.assertEqual(graphics.tile_to_coords(3,3,3), [100.0, -100.0])

def main():
    unittest.main(verbosity=3)


main()

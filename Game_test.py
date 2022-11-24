from game_backend import *
import unittest

class TestGame(unittest.TestCase):

    def test_init(self):
        b=Backgam()
        self.assertEqual(len(b.spots), 24, msg="Error: Incorrect number of spots on the game board.")
        self.assertEqual(b.NUM_PIECES, 20, msg="Error: Incorrect number of starting pieces on the game board.")
        for spot in b.spots:
            self.assertIsInstance(spot, Game_triangle, msg="Error: incorrect triangle class used.")
        self.assertIsInstance(b.bar, Game_bar, msg="Error: incorrect bar class used.")
        self.assertIsInstance(b.trough_comp, Game_trough, msg="Error: incorrect trough class for computer")
        self.assertIsInstance(b.trough_user, Game_trough, msg="Error: incorrect trough class for user")
        self.assertEqual(len(b.spots),24)

        #b.print_board()

        # Make sure the right pieces are in the right spots at set up
        for i in range(24):
            if i == 0:
                self.assertEqual(b.spots[i].get_player(), 0, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 2, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 5:
                self.assertEqual(b.spots[i].get_player(), 1, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 5, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 7:
                self.assertEqual(b.spots[i].get_player(), 1, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 3, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 11:
                self.assertEqual(b.spots[i].get_player(), 0, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 5, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 12:
                self.assertEqual(b.spots[i].get_player(), 1, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 5, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 16:
                self.assertEqual(b.spots[i].get_player(), 0, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 3, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 18:
                self.assertEqual(b.spots[i].get_player(), 0, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 5, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            elif i == 23:
                self.assertEqual(b.spots[i].get_player(), 1, msg="Error: place_pieces(); Incorrect player on spot " + str(i))
                self.assertEqual(b.spots[i].get_num_pieces(), 2, msg="Error: place_pieces(); Incorrect number of pieces on spot " + str(i))
            else:
                self.assertEqual(b.spots[i].get_player(), -1, msg="Error: place_pieces(); Empty spot " + str(i) + " should not have a player")
                self.assertEqual(b.spots[i].get_num_pieces(), 0, msg="Error: place_pieces(); Empty spot " + str(i) + " has pieces on it")

    def test_find_valid_moves(self):
        b = Backgam()
        actual = Backgam.find_valid_moves(b, 0, 2)
        expected = [[0,2,0], [11,13,0], [16,18,0], [18,20,0]]
        self.assertEqual(actual, expected)
        actual = Backgam.find_valid_moves(b, 0, 4)
        expected = [[0,4,0], [11,15,0], [16,20,0], [18,22,0]]
        self.assertEqual(actual, expected)
        b.move_piece(0, 4, 0)
        b.move_piece(7, 4, 1)
        b.move_piece(5, 4, 1)
        actual = Backgam.find_valid_moves(b, 0, 5)
        expected = []
        self.assertEqual(actual, expected)
        actual = Backgam.find_valid_moves(b, 0, 4)
        expected = [[-1, 3, 0]]
        self.assertEqual(actual, expected)
        actual = Backgam.find_valid_moves(b, 1, 4)
        expected = [[4, 0, 1], [5, 1, 0], [7, 3, 0], [12, 8, 0], [23, 19, 0]]
        self.assertEqual(actual, expected)
        b.move_piece(4, 3, 1)
        b.move_piece(-1, 3, 0)
        actual = Backgam.find_valid_moves(b, 1, 6)
        expected = []
        self.assertEqual(actual, expected)
        actual = Backgam.find_valid_moves(b, 1, 2)
        expected = [[-1, 22, 0]]
        self.assertEqual(actual, expected)
        actual = Backgam.find_valid_moves(b, 1, 5)
        expected = [[-1, 19, 0]]
        self.assertEqual(actual, expected)


    def test_move_piece(self):
        b = Backgam()
        # Move a piece from spot 0 to spot 1
        b.move_piece(0, 1, 0)
        self.assertEqual(b.spots[1].get_num_pieces(), 1)
        self.assertEqual(b.spots[1].get_player(), 0)
        self.assertEqual(b.spots[0].get_num_pieces(), 1)
        self.assertEqual(b.spots[0].get_player(), 0)
    
    def test_finish_piece(self):
        b=Backgam()
        b.finish_piece(0, 0)
        self.assertEqual(b.trough_user.num_pieces, 1)
        self.assertEqual(b.spots[0].get_num_pieces(), 1)
    
    def test_bump(self):
        b = Backgam()
        # Make a few moves to put a piece by itself
        b.move_piece(0, 4, 0)
        b.move_piece(7, 4, 1)
        self.assertEqual(b.bar.num_user_pieces, 1)
        b.move_piece(5, 4, 1)
        self.assertEqual(b.bar.num_user_pieces, 1)
    
    def check_for_win(self):
        b = Backgam()
        for i in range(15):
            b.trough_comp.add_piece(1)
        self.assertEqual(b.check_for_win(), 1)
        b = Backgam()
        for i in range(5):
            b.trough_comp.add_piece(1)
            b.trough_user.add_piece(0)
        self.assertEqual(b.check_for_win(), None)
        b = Backgam()
        for i in range(15):
            b.trough_user.add_piece(0)
        for i in range(5):
            b.trough_comp.add_piece(1)
        self.assertEqual(b.check_for_win(), 0)

    def test_initial_placement(self):
        b=Backgam()
        self.assertEqual(b.spots[0].player, 0)
        self.assertEqual(b.spots[0].num_pieces, 2)
        self.assertEqual(b.spots[5].player, 1)
        self.assertEqual(b.spots[5].num_pieces, 5)
        self.assertEqual(b.spots[7].player, 1)
        self.assertEqual(b.spots[7].num_pieces, 3)
        self.assertEqual(b.spots[11].player, 0)
        self.assertEqual(b.spots[11].num_pieces, 5)
        self.assertEqual(b.spots[12].player, 1)
        self.assertEqual(b.spots[12].num_pieces, 5)
        self.assertEqual(b.spots[16].player, 0)
        self.assertEqual(b.spots[16].num_pieces, 3)
        self.assertEqual(b.spots[18].player, 0)
        self.assertEqual(b.spots[18].num_pieces, 5)
        self.assertEqual(b.spots[23].player, 1)
        self.assertEqual(b.spots[23].num_pieces, 2)

    def test_computer_move(self):
        b=Backgam()
        # testing easy difficulty moves
        actual = b.computer_move(1, 4)
        b.move_piece(23, 19, 1)
        expected = [23, 19, 0]
        self.assertEqual(actual, expected)
        b.move_piece(11, 15, 0)
        actual = b.computer_move(1, 4)
        expected = [19, 15, 1]
        self.assertEqual(actual, expected)
        b.move_piece(19, 15, 1)
        b.move_piece(0, 6, 0)
        actual = b.computer_move(1, 3)
        expected = [23, 20, 0]
        self.assertEqual(actual, expected)
        b.move_piece(23, 20, 1)
        b.move_piece(6, 10, 0)
        actual = b.computer_move(1, 5)
        expected = [15, 10, 1]
        self.assertEqual(actual, expected)
        
        # Testing medium difficulty moves
        actual = b.computer_move(2, 5)
        expected = [20, 15, 0]
        self.assertEqual(actual, expected)
        b.move_piece(20, 15, 1)

        actual = b.computer_move(2, 2)
        expected = [12, 10, 1]
        self.assertEqual(actual, expected)
        b.move_piece(12, 10, 1)
        
        actual = b.computer_move(2, 2)
        expected = [12, 10, 0]
        self.assertEqual(actual, expected)
        b.move_piece(12, 10, 1)

        actual = b.computer_move(2, 2)
        expected = [15, 13, 0]
        self.assertEqual(actual, expected)

        # testing hardest difficulty
        actual = b.computer_move(3, 2)
        expected = [7, 5, 0]
        self.assertEqual(actual, expected)

        b.move_piece(7, 3, 1)
        b.move_piece(0, 3, 0)

        # testing movement from bar
        actual = b.computer_move(3, 4)
        expected = [-1, 20, 0]
        self.assertEqual(actual, expected)

        b.move_piece(7, 6, 1)
        b.move_piece(3, 6, 0)
        b.move_piece(18, 20, 0)
        
        actual = b.computer_move(3, 4)
        expected = [-1, 20, 1]
        self.assertEqual(actual, expected)

        b.move_piece(18, 20, 0)
        actual = b.computer_move(3, 4)
        expected = None
        self.assertEqual(actual, expected)

        b.print_board()

if __name__ == "__main__":
    unittest.main()

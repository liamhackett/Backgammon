from operator import truediv

class Game_trough:
    MAX_PIECES = 15
    def __init__(self):
        self.num_pieces = 0
    
    def add_piece(self):
        if(self.num_pieces < self.MAX_PIECES):
            self.num_pieces += 1
    
    def check_filled(self):
        if(self.num_pieces == self.MAX_PIECES):
            return True
        else:
            return False
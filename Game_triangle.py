class Game_triangle:
    # player=0 for user, player=1 for computer, player= -1 for empty
    def __init__(self, num_pieces, player):
        self.num_pieces = num_pieces
        self.player = player
    
    def get_num_pieces(self):
        return self.num_pieces
    
    def get_player(self):
        return self.player

    def add_piece(self, id):
        if (self.player == id or self.player == -1):
            self.num_pieces += 1
            self.player = id
    
    def remove_piece(self):
        self.num_pieces -= 1
        if(self.num_pieces == 0):
            self.player = -1
    
    def swap_pieces(self):
        if(self.player == 1):
            self.player = 0
        else:
            self.player = 1


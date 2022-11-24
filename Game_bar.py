class Game_bar:
    def __init__(self, num_comp_pieces, num_user_pieces):
        self.num_comp_pieces = num_comp_pieces
        self.num_user_pieces = num_user_pieces
    def add_piece(self, player_id):
        if(player_id == 1):
            self.num_comp_pieces += 1
        else:
            self.num_user_pieces += 1
    def remove_piece(self, player_id):
        if(player_id == 1):
            self.num_comp_pieces -= 1
        else:
            self.num_user_pieces -= 1

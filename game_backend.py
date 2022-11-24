# Backgam class
# Includes functions for playing a valid game of Backgammon
# Includes functions for keeping track of player scores and pieces
# from asyncio.windows_events import NULL
from Game_bar import Game_bar
from Game_trough import Game_trough
from Game_triangle import Game_triangle
import random

class Backgam():

    # initialize game board setup
    def __init__(self):
        #Initialize variables
        self.NUM_PIECES = 20
        self.spots = list()
        self.bar = Game_bar(0, 0)
        self.trough_comp = Game_trough()
        self.trough_user = Game_trough()
        self.GAME_OVER = 0
        self.WINNER = None

        for x in range(24):
            self.spots.append(Game_triangle(0,-1))
        
        self.spots = self.place_pieces(self.spots)

    #Helper method for __init__ method
    #Places the pieces in their initial setup on the board
    def place_pieces(self, triangles):
        triangles[0].player = 0
        triangles[0].num_pieces = 2

        triangles[5].player = 1
        triangles[5].num_pieces = 5

        triangles[7].player = 1
        triangles[7].num_pieces = 3

        triangles[11].player = 0
        triangles[11].num_pieces = 5

        triangles[12].player = 1
        triangles[12].num_pieces = 5

        triangles[16].player = 0
        triangles[16].num_pieces = 3

        triangles[18].player = 0
        triangles[18].num_pieces = 5

        triangles[23].player = 1
        triangles[23].num_pieces = 2

        return triangles

    # Params id: The id of a player
    # returns the spots that are occupied by that player
    def get_occupied_spaces(self, id):
        occuppied = list()
        for i in range(0, len(self.spots)):
            if(self.spots[i].get_player() == id):
                occuppied.append(i)
        return occuppied

    # Params: end, the location to move to
    # returns -1 if not valid, 0 if valid but not kill, 1 if valid and a kill
    def is_valid_move(self, end, id):
        if end > 23:
            return -1
        if(self.spots[end].get_player() == id or self.spots[end].get_num_pieces() == 0):
            return 0
        elif(self.spots[end].get_player() != id or self.spots[end].get_num_pieces() == 1):
            return 1
        else:
            return -1

    # Params id: the id of the player who just rolled
    #    roll: the # on one of the die
    # findValidMoves
    # Takes in the player ID (0 for user, 1 for computer)
    # Returns a list of valid moves that the player can make
    # end spot is -1 if it is the trough
    def find_valid_moves(self, id, roll):
        # contains lists of the start index, end index
        valid_moves = list()
        available_moves = list()
        # Find the spots occuppied by player with ID
        occupied = self.get_occupied_spaces(id)

        trough_ready = True
        # check to see if every piece is in the home base
        for spot in occupied:
            # user's home base in 18-23
            if(id == 0):
                if spot not in range(18, 24):
                    trough_ready = False
            else:
                if spot not in range(0, 6):
                    trough_ready = False
        
        if(trough_ready):
            for spot in occupied:
                if(id == 0):
                    if(24 - spot <= roll):
                        valid_moves.append([spot, -1, 0])
                else:
                    if(spot - roll <= 0):
                        valid_moves.append([spot, -1, 0]) 

        # find every spot that meets one of these conditions:
        # 1. Has no pieces occupying it
        # 2. Has one piece of the opposite player occupying it
        # 3. Has any number of pices of the same player occupying it
        
        
        for i in range(0, len(self.spots)):
            # spot has no pieces occupying it
            if(self.spots[i].get_num_pieces() == 0):
                available_moves.append(i)
            # spot has one piece of the opposite player occupying it
            elif(self.spots[i].get_player() != id and self.spots[i].get_num_pieces() == 1):
                available_moves.append(i)
            # Has any number of pices of the same player occupying it
            elif(self.spots[i].get_player() == id):
                available_moves.append(i)
                
        if((self.bar.num_user_pieces == 0 and id == 0) or (self.bar.num_comp_pieces == 0 and id == 1)):
            # And the spot must meet both of those conditions:
            # - spot needs to be in the right direction 
            # - spot needs to be the same distance as the dice roll
            for spot_index in available_moves:
                for start_spot in occupied:
                    if(id == 0):
                        if((spot_index == start_spot + roll) and ([start_spot, spot_index, -1] not in valid_moves)):
                            # check to see if the move is a bump
                            if(self.spots[spot_index].get_player() == 1 and self.spots[spot_index].get_num_pieces() == 1):
                                valid_moves.append([start_spot, spot_index, 1])    
                            else:
                                valid_moves.append([start_spot, spot_index, 0])
                    elif(id == 1):
                        if((spot_index == start_spot - roll) and ([start_spot, spot_index, -1] not in valid_moves)):
                            # check to see if the move is a bump
                            if(self.spots[spot_index].get_player() == 0 and self.spots[spot_index].get_num_pieces() == 1):
                                valid_moves.append([start_spot, spot_index, 1])    
                            else:
                                valid_moves.append([start_spot, spot_index, 0])
        
        # the player has pieces on the bar
        else:
            # If id == 0, There must be spots open between 0 and 5
            if(id == 0):
                for spot in range(0, 6):
                    if((spot in available_moves) and (spot == roll - 1)):
                        if(self.spots[spot].get_player() == 1 and self.spots[spot].get_num_pieces() == 1):
                            valid_moves.append([-1, spot, 1])    
                        else:
                            valid_moves.append([-1, spot, 0])
            # elif id == 1, There must be spots open between 18 and 23
            elif(id == 1):
                for spot in range(18, 24):
                    if((spot in available_moves) and (spot == 24 - roll)):
                        if(self.spots[spot].get_player() == 0 and self.spots[spot].get_num_pieces() == 1):
                            valid_moves.append([-1, spot, 1])    
                        else:
                            valid_moves.append([-1, spot, 0])

        return valid_moves


    # Params start: The spot index where the piece is getting moved from
    #          end: The spot index where the piece will be moved to
    #           id: The player id of the piece that is getting moved
    # Decrements the num pieces value for the start spot
    # increments the num pieces value for the end spot
    # if a piece is getting moved to the bar, change the player of the spot but keep the number of pieces as 1
    def move_piece(self, start, end, id):
        if(end == -1):
            self.finish_piece(start, id)
        else:
            if(start == -1):
                self.bar.remove_piece(id)
            else:
                self.spots[start].remove_piece()
            if(self.spots[end].get_player() == id or self.spots[end].get_player() == -1):
                self.spots[end].add_piece(id)
            else:
                self.bump(end, id)

    # Params start: the index of the spot to remove the finished piece from
    #           id: The player id of the piece that is getting finished
    # Decrements the num pieces value for start spot
    # increments the num pieces value for the trough associated with the id (0 for computer, 1 for user)
    def finish_piece(self, start, id):
        self.spots[start].remove_piece()
        if id == 0:
            self.trough_user.add_piece()
        elif id == 1:
            self.trough_comp.add_piece()

    # Params id: the player that is bumping a piece of the other player to the bar
    #       spot: The spot where the piece is getting bumped from
    # Decrements the num pieces value for start spot
    # increments the piece count on the bar for that player
    def bump(self, spot, id):
        self.spots[spot].swap_pieces()
        if(id == 0):
            self.bar.add_piece(1)
        else:
            self.bar.add_piece(0)
        
    # checks to see if a trough is full
    # updates the WINNER variable of the Backgam object: 0 for computer, 1 for user
    # returns the id of the winner, or None if there is no winner
    def check_for_win(self):
        if self.trough_comp.check_filled():
            self.WINNER = 0
            self.GAME_OVER = 1
        elif self.trough_user.check_filled():
            self.WINNER = 1
            self.GAME_OVER = 1
        return self.WINNER

    # dice roll 
    # returns two random numbers between 1 and 6
    def roll_dice(self):
        return [random.randrange(1,6), random.randrange(1,6)]

    # computer move
    # returns a move [start, end] based on the game difficulty
    # easy (1): first selects the move that kills a user piece, otherwise selects the move that moves the farthest amount of spaces
    # medium (2): first tries to cover any comp pieces that are by themselves, otherwise selects the move that kills a user piece, otherwise selects the move that moves the farthest amount of spaces
    # hard (3): first tries to cover any comp pieces that are by themselves, otherwise selects a move that gets it into its home base,
    # otherwise selects the move that moves the farthest and lands on a comp occupied spot, otherwise selects the move that kills a user piece,
    # otherwise moves the farthest back piece that is able to be moved
    def computer_move(self, difficulty, roll):
        occupied_comp = self.get_occupied_spaces(1)
        occupied_user = self.get_occupied_spaces(0)
        valid_moves = self.find_valid_moves(1, roll)
        kill_move = list()
        farthest_kill = 0
        farthest_move = list()
        farthest_no_kill = 23
        farthest_back = 0
        result_move = list()
        if not valid_moves:
            return None
        # if needs to move chip off bar
        if(self.bar.num_comp_pieces > 0):
            for move in valid_moves:
                if move[2] == 1:
                    return move
                elif self.spots[move[1]] in occupied_comp:
                    return move
                farthest_move = move
            return farthest_move

        # if needs to move chips to the trough
        elif(valid_moves[0][1] == -1):
            # try to move any chip that is alone
            farthest_move = valid_moves[0]
            for move in valid_moves:
                if self.spots[move[0]].get_num_pieces() == 1:
                    # try to move to trough
                    if move[1] == -1:
                        return move
                    # Try to cover a piece that is alone
                    elif self.spots[move[1]].get_num_pieces() == 1:
                        result_move = move
                    # try to kill user piece 
                    elif move[2] == 1:
                        kill_move = move
                    # find the farthest back piece
                    elif move[0] > farthest_move[0]:
                        farthest_move = move
                    
            if(result_move):
                return result_move
            elif(kill_move):
                return kill_move
            elif(farthest_move):
                return farthest_move
            # there's pieces that are alone
            else:
                for move in valid_moves:
                    # try to move to trough
                    if move[1] == -1:
                        return move
                    # Try to cover a piece that is alone
                    elif self.spots[move[1]].get_num_pieces() == 1:
                        result_move = move
                    # try to kill user piece 
                    elif move[2] == 1:
                        kill_move = move
                    # find the farthest back piece
                    elif move[0] > farthest_move[0]:
                        farthest_move = move
                if(result_move):
                    return result_move
                elif(kill_move):
                    return kill_move
                elif(farthest_move):
                    return farthest_move


        else:
            # easiest difficulty
            if(difficulty == 1):
                # find the farthest move
                for move in valid_moves:
                    # Check for a move that kills a user piece and see which one is the furthest back
                    if move[1] in occupied_user and move[0] > farthest_kill:
                        kill_move = move
                        farthest_kill = move[0]
                    # farthest move is not a kill
                    # move the piece that is furthest from the base
                    elif move[0] > farthest_back and move[0] > 5:
                        farthest_move = move
                        farthest_back = move[0]
                # farthest move is a kill
                if kill_move:
                    return kill_move
                if not farthest_move:
                    farthest_no_kill = 23
                    for move in valid_moves:
                        # make a move that gets a piece closer or into the base
                        if move[1] < farthest_no_kill:
                            farthest_move = move
                            farthest_no_kill = move[1]
                return farthest_move
            # medium difficulty
            elif(difficulty == 2 or difficulty == 3):
                # Finds a computer piece that is by itself (unprotected) and find a way to cover it
                for move in valid_moves:
                    if(move[1] in occupied_comp):
                        if self.spots[move[1]].get_num_pieces() == 1 and move[1] < farthest_no_kill:
                            farthest_move = move
                            farthest_no_kill = move[1]
                if farthest_move:
                    return farthest_move
                # Finds a computer piece that is by itself (unprotected) and find a way to move it
                for move in valid_moves:
                    if(move[1] in occupied_comp):
                        if self.spots[move[0]].get_num_pieces() == 1 and move[0] > farthest_back:
                            farthest_move = move
                            farthest_back = move[0]
                if farthest_move:
                    return farthest_move

                # if the difficulty is medium and there were no singular computer pieces to cover, find a move based on the 
                # easiest difficulty's logic
                elif(difficulty == 2):
                    return self.computer_move(1, roll)
                # hardest difficulty
                else:
                    # select a move that brings a piece to it's home base
                    for move in valid_moves:
                        # move ends in home base
                        if move[1] in range(0, 6):
                            # checks to see if moving the piece will expose a computer chip
                            # and if the start spot is in the base already
                            if self.spots[move[0]].get_num_pieces() != 2 and move[0] not in range (0, 6):
                                return move
                    # otherwise select the move that moves the farthest and lands on a comp occupied spot
                    for move in valid_moves:
                        if move[0] > farthest_back and move[0] > 5 and move[1] in occupied_comp:
                            farthest_move = move
                            farthest_back = move[0]
                    if farthest_move:
                        return farthest_move
                    else:
                        # otherwise call the medium difficulty logic
                        return self.computer_move(2, roll)

                    


    # Function print_board: 
    #       Displays a simplified version of the board for CLI use
    def print_board(self):
        row_count = 1
        max_pieces = 0
        for i in range(23):
            if(self.spots[i].get_num_pieces() > max_pieces):
                max_pieces = self.spots[i].get_num_pieces()
        print(" ")
        
        print("Bar: ", end="")
        if(self.bar.num_user_pieces == 0 and self.bar.num_comp_pieces == 0):
            print("empty", end="")
        for i in range(self.bar.num_comp_pieces):
            print("X", end=" ")
        for i in range(self.bar.num_user_pieces):
            print("O", end=" ")
        print(" ")
        
        print("- - - - - - | - - - - - -")
        while(row_count <= max_pieces):
            for i in range(11, -1, -1):
                if(self.spots[i].get_num_pieces() >= row_count):
                    if(self.spots[i].get_player() == 1):
                        print("X", end=" ") 
                    elif(self.spots[i].get_player() == 0):
                        print("O", end=" ")
                else:
                    print(" ", end=" ")
                if(i == 6):
                    print("|", end=" ")
                   
            row_count += 1
            print(" ")
        print("            |            ")
        row_count -= 1
        while(row_count >= 1):
            for i in range(12, 24):
                if(self.spots[i].get_num_pieces() >= row_count):
                    if(self.spots[i].get_player() == 1):
                        print("X", end=" ") 
                    elif(self.spots[i].get_player() == 0):
                        print("O", end=" ")
                else:
                    print(" ", end=" ")
                if(i == 17):
                    print("|", end=" ")
            row_count -= 1
            print(" ")

        print("- - - - - - | - - - - - -")
        print("User trough: ", end="")
        if(self.trough_user.num_pieces == 0):
            print("empty", end="")
        for i in range(self.trough_user.num_pieces):
            print("O", end=" ")
        print(" ")

        print("Comp trough: ", end="")
        if(self.trough_comp.num_pieces == 0):
            print("empty", end="")
        for i in range(self.trough_comp.num_pieces):
            print("X", end=" ")
        print(" ")

            
    

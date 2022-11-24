from hashlib import sha3_384
import unittest
import pygame
from pygame.locals import (BUTTON_LEFT, K_ESCAPE, KEYDOWN, K_SPACE, QUIT)
from triangle import *
from button import Button
from chip import Chip
from game_backend import *
class Display:
    # initialize display
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600

        pale_brown = (152, 118, 84)
        tuscan_brown = (111, 78, 55)
        white = (255, 255, 255)
        red = (255, 0, 0)
        self.blue = (0, 0, 255)

        self.rolls = []
        self.game = Backgam()
        self.must_roll = True
        self.selected_chip = list()
        self.valid_moves = list()
        self.comp_no_moves = False
        self.roll_once = False
        self.game_over = False

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Backgammon")
        pygame.Surface.fill(self.screen, (92, 64, 51))

        self.player_chips = list()
        self.computer_chips = list()

        for i in range(0, len(self.game.spots)):
            if self.game.spots[i].get_num_pieces() > 0:
                top_y = [52, 96, 140, 184, 228, 272]
                bottom_y = [549, 505, 461, 417, 373, 329]
                if i <= 5:
                    x = 694 - 53.3333333 * i
                elif i > 5 and i < 12:
                    x = 334 - (i - 6) * 53.333333
                elif i > 11 and i < 18:
                    x = 67.33333333 + (i - 12) * 53.333333
                elif i >= 18:
                    x = 427.33333333 + (i - 18) * 53.333333
                if(self.game.spots[i].get_player() == 0):
                    color = white
                else:
                    color = (255, 0, 0)
                if i < 12:
                    for j in range(0, self.game.spots[i].get_num_pieces()):
                        # draw the chip at the triangle's x value and in increasing y val
                        piece = Chip(color, 22, x, top_y[j], self.screen, self.game.spots[i].get_player(), i)
                        if( self.game.spots[i].get_player() == 0):
                            self.player_chips.append(piece)
                        else:
                            self.computer_chips.append(piece)
                else:
                    for j in range(0, self.game.spots[i].get_num_pieces()):
                        piece = Chip(color, 22, x, bottom_y[j], self.screen, self.game.spots[i].get_player(), i)
                        if( self.game.spots[i].get_player() == 0):
                            self.player_chips.append(piece)
                        else:
                            self.computer_chips.append(piece)

        # initialize triangles list
        self.triangles=[]
        for i in range(24):
            self.triangles.append(Triangle(0,-1, i,(tuscan_brown if (i<12 and i%2==0) or (i>=12 and i%2==1) else pale_brown)))
        
        # create help button
        self.button = Button((193, 154, 107), 5, 575, 40, 20, self.screen)
        self.display_text("Help", (10, 576), 14, white)

        self.reset = Button((193, 154, 107), 48, 575, 45, 20, self.screen)
        self.display_text("Reset", (51, 576), 14, white)

        # create roll dice button
        self.button_roll = Button((193, 154, 107), 355, 575, 50, 20, self.screen)

        # create difficulty buttons
        self.difficulty = 1

        self.diff_1 = Button((153, 114, 67), 110, 5, 20, 20, self.screen)
        self.diff_2 = Button((193, 154, 107), 140, 5, 20, 20, self.screen)
        self.diff_3 = Button((193, 154, 107), 170, 5, 20, 20, self.screen)

        self.player_trough = pygame.Rect((735,310), (50, 250))
        self.player_trough_valid = False
        self.computer_trough =  pygame.Rect((735, 40), (50, 250))

        self.num_trough_player = 0
        self.num_trough_comp = 0

        self.num_bar_p = 0
        self.num_bar_c = 0

        self.num_moves = 2
        
    # function draw_background()
    #       draws the board and all the pieces, buttons and text
    def draw_background(self):
        camel = (193, 154, 107)
        white = (255, 255, 255)
       
        # draw rectangles for each half of the board
        pygame.draw.rect(self.screen, camel, pygame.Rect((self.WIDTH/20, self.HEIGHT/20), (self.WIDTH*0.8/2, self.HEIGHT*.9)))
        pygame.draw.rect(self.screen, camel, pygame.Rect((self.WIDTH/20 + (self.WIDTH*0.9/2), self.HEIGHT/20), (self.WIDTH*0.8/2, self.HEIGHT*.9)))
        # draw trough rectangles
        if self.player_trough_valid:
            pygame.draw.rect(self.screen, (242, 210, 150), self.player_trough)
        else:
            pygame.draw.rect(self.screen, camel, self.player_trough)
        pygame.draw.rect(self.screen, camel, self.computer_trough)

        # draw triangles 
        for i in range(len(self.triangles)):
            self.triangles[i].draw(self.screen)

        # chips on triangles
        for i in range(0, len(self.game.spots)):
            if self.game.spots[i].get_num_pieces() > 0:
                top_y = [52, 96, 140, 184, 228, 272]
                bottom_y = [549, 505, 461, 417, 373, 329]
                if i <= 5:
                    x = 694 - 53.3333333 * i
                elif i > 5 and i < 12:
                    x = 334 - (i - 6) * 53.333333
                elif i > 11 and i < 18:
                    x = 67.33333333 + (i - 12) * 53.333333
                elif i >= 18:
                    x = 427.33333333 + (i - 18) * 53.333333
                if i < 12:
                    j = 0
                    for chip in self.player_chips:
                        if chip.index == i:
                            # draw the chip at the triangle's x value and in increasing y val
                            chip.coords = (x, top_y[j])
                            chip.draw_chip()
                            #self.display_text(str(chip.index), (x, top_y[j]), 10, (0, 0, 0))
                            if(j < 4):
                                j += 1
                    j = 0
                    for chip in self.computer_chips:
                        if chip.index == i:
                            # draw the chip at the triangle's x value and in increasing y val
                            chip.coords = (x, top_y[j])
                            chip.draw_chip()
                            if(j < 4):
                                j += 1
                else:
                    j = 0
                    for chip in self.player_chips:
                        if chip.index == i:
                            # draw the chip at the triangle's x value and in increasing y val
                            chip.coords = (x, bottom_y[j])
                            chip.draw_chip()
                            #self.display_text(str(chip.index), (x, bottom_y[j]), 10, (0, 0, 0))
                            if(j< 4):
                                j += 1
                    j = 0
                    for chip in self.computer_chips:
                        if chip.index == i:
                            # draw the chip at the triangle's x value and in increasing y val
                            chip.coords = (x, bottom_y[j])
                            chip.draw_chip()
                            if(j < 4):
                                j += 1

        # draw chips on bar
        if self.game.bar.num_comp_pieces > 0 or self.game.bar.num_user_pieces > 0:
            y_vals_c = [344, 388, 432, 476, 520, 564] # note: add 44 on top or bottom to get more positions
            y_vals_p = [300, 256, 212, 168, 124, 80, 36]
            j = 0
            for chip in self.player_chips:
                if(chip.bar):
                    chip.coords = (380, y_vals_p[j])
                    chip.draw_chip()
                    j += 1
            j = 0
            for chip in self.computer_chips:
                
                if(chip.bar):
                    chip.coords = (380, y_vals_c[j])
                    chip.color = (255, 0, 0)
                    chip.draw_chip()
                    j += 1

        # draw chips in trough
        if self.game.trough_comp.num_pieces > 0 or self.game.trough_user.num_pieces > 0:
            for i in range(0, self.game.trough_comp.num_pieces):
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect((735, 40+(250/15*i)), (50, 250/15)))
            for i in range(0, self.game.trough_user.num_pieces):
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((735,561-(250/15)*(i+1)), (50, 250/15)))

        # draw the buttons
        self.button.draw()
        self.reset.draw()
        self.button_roll.draw()
        self.display_text("Help", (10, 576), 14, white)
        self.display_text("Reset", (51, 576), 14, white)
        self.display_text("Roll", (367, 576), 15, white)

        self.display_text("Difficulty", (40, 6), 16, white)

        self.diff_1.draw()
        self.diff_2.draw()
        self.diff_3.draw()

        self.display_text("1", (115, 6), 16, white)
        self.display_text("2", (146, 6), 16, white)
        self.display_text("3", (176, 6), 16, white)

        if self.must_roll:
            self.error_message("Please roll the dice", 310)
        elif self.comp_no_moves:
            self.error_message("The computer has no moves! Your turn", 250)
        elif self.roll_once:
            self.error_message("You can only roll once, choose a move", 250)

    # function main_screen
    #       recreates the main screen after the user returns from the help menu
    def main_screen(self):
        pygame.init()
        white = (255, 255, 255)
        self.WIDTH = 800
        self.HEIGHT = 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Backgammon")
        pygame.Surface.fill(self.screen, (92, 64, 51))
        
        self.button = Button((193, 154, 107), 5, 575, 40, 20, self.screen)
        self.button.draw()
        self.display_text("Help", (10, 576), 14, white)

    # function: help_screen
    #   creates and displays the help screen menu
    def help_screen(self):
        pygame.init()
        white = (255, 255, 255)
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.Surface.fill(self.screen, (92, 64, 51))
        
        # Rules Displayed on the Help screen
        self.display_text("Welcome to Backgammon!", (310, 10), 16, (255, 255, 255))
        self.display_text("Rule 1: A chip may be moved only to an open spot (one that is not occupied by two or more opposing checkers)", (10, 40), 15, (255, 255, 255))
        self.display_text("Rule 2: The numbers on the two dice constitute separate moves. For example, if a player rolls 5 and 3, they may move", (10, 70), 15, (255, 255, 255))
        self.display_text("one chip five spaces to an open point and another chip three spaces to an open point, or they may move one", (10, 90), 15, (255, 255, 255))
        self.display_text("chip a total of eight spaces to an open point, but only if the intermediate point (either three or five spaces", (10, 110), 15, (255, 255, 255))
        self.display_text("from the starting point) is also open.", (10, 130), 15, (255, 255, 255))
        self.display_text("Rule 3: If a player rolls doubles they play the numbers shown on the dice twice. A roll of two six's allows the", (10, 160), 15, (255, 255, 255))
        self.display_text("player has four sixes to use.", (10, 180), 15, (255, 255, 255))
        self.display_text("Rule 4: A player must use both numbers of a roll if this is legally possible. When neither number can be used,", (10, 210), 15, (255, 255, 255))
        self.display_text("the player loses their turn.", (10, 230), 15, (255, 255, 255))
        self.display_text("Rule 5: If a player lands on a space with only one of the opponents chip, the opponents chip gets removed from the", (10, 260), 15, (255, 255, 255))
        self.display_text("table and placed on the bar in the middle. During the opponents turn they have to try and put the chip back in the", (10, 280), 15, (255, 255, 255))
        self.display_text("game in an open spot (one that is not occupied by two or more opposing checkers) within their opponents home board.", (10, 300), 15, (255, 255, 255))
        self.display_text("If they are unable to do this within their turn the player loses their turn. ", (10, 320), 15, (255, 255, 255))
        self.display_text("Rule 6: Once a player has moved all of their chips into their home board they can begin playing to take the chips off", (10, 350), 15, (255, 255, 255))
        self.display_text("of the board. To take a chip off of the board the player has to roll the number that cooresponds to the space that a chip", (10, 370), 15, (255, 255, 255))
        self.display_text("resides. If there is no chip on the space that cooresponds to the number rolled the player must make a legal move using", (10, 390), 15, (255, 255, 255))
        self.display_text("a chip on a space further back from the number rolled. A player wins by getting all of his chips off of the board.", (10, 410), 15, (255, 255, 255))

        self.button.draw()
        self.display_text("Back", (10, 576), 14, white)

        pygame.display.set_caption("Help")


    # Function: display_text
    # params: self, 
    #         the text to be displayed, 
    #         the top left coordinate of the text,
    #         the font size
    #         the text color
    # This function displays the given text at the given coordinates
    def display_text(self, text, topLeft, font_size, color):
        font = pygame.font.SysFont("Arial", font_size)
        self.img = font.render(text, True, color)
        self.img = font.render(text, True, color)
        rect = self.img.get_rect()
        rect.topleft = topLeft
        rect.size=self.img.get_size()
        self.screen.blit(self.img, rect)


    # Function: error_message
    # params: self,
    #         message, the text to be displayed
    # Method to display textual error messages in the center of the screen.
    def error_message(self, message, x):
        self.display_text(message, (x, 6), 16, (255, 255, 255))


    # Function: move_chip
    # params: self, the mouse position
    # moves the chip to a new triangle based on how many chips are on the space
    def move_chip(self, mouse_pos):
        # make sure there is a chip selected 
        if not self.selected_chip:
            return None

        computer_turn = False
        start = self.selected_chip[0].index
        # if user is selecting the trough
        if self.player_trough.collidepoint(mouse_pos) and ([start, -1, 0] in self.valid_moves or [start, 24, 0] in self.valid_moves):
            self.game.move_piece(self.selected_chip[0].index, -1, 0)
            self.player_chips[self.selected_chip[1]].index = 24
            self.player_chips[self.selected_chip[1]].selected = False
            self.player_chips.pop(self.selected_chip[1])
            self.selected_chip = list()
            self.player_trough_valid = False
            roll = 24 - start

            if self.num_trough_player == 15:
                self.has_won()

            # if the move made uses less than both of the rolls then remove the minimum roll 
            
            if len(self.rolls) > 2:
                if roll > self.rolls[0]:
                    self.rolls.pop(0)
                    self.rolls.pop(0)
                    if(roll > self.rolls[0] * 2):
                        self.rolls.pop(0)
                    if(roll == self.rolls[0] * 4):
                        self.rolls.pop(0)
                else:
                    self.rolls.pop(0)
            elif(len(self.rolls) > 1):
                if roll in self.rolls:
                    del(self.rolls[self.rolls.index(roll)])
                elif roll > self.rolls[0] and roll > self.rolls[1]:
                    self.rolls = list()
                elif(roll == self.rolls[0] + self.rolls[1]):
                    self.rolls = list()
                elif(roll < min(self.rolls[0], self.rolls[1])):
                    self.rolls.remove(min(self.rolls[0], self.rolls[1]))
                elif(roll <= self.rolls[0] and roll > self.rolls[1]):
                    self.rolls.remove(self.rolls[0])
                elif(roll <= self.rolls[1] and roll > self.rolls[0]):
                    self.rolls.remove(self.rolls[0])
            else:
                for r in self.rolls:
                    if roll <= r:
                        self.rolls.remove(r)
                        break
            
                
        # Get the selected triangle
        else: 
            for j in range(len(self.triangles)):
                if self.triangles[j].collidepoint(mouse_pos) and ([start, j, 0] in self.valid_moves or [start, j, 1] in self.valid_moves):
                
                    if(start == -1):
                        self.player_chips[self.selected_chip[1]].bar = False
                    self.game.move_piece(self.selected_chip[0].index, j, 0)
                    self.player_chips[self.selected_chip[1]].index = j
                    #print(self.player_chips[self.selected_chip[1]].index)
                    self.player_chips[self.selected_chip[1]].selected = False
                    self.selected_chip = list()
                    self.player_trough_valid = False

                    # if the move was a kill, move the computer piece to bar
                    for chip in self.computer_chips:
                        if chip.index == j:
                            chip.index = -1
                            chip.bar = True
                            self.game.spots[j].player = 0

                    roll = j - start

                    # remove the roll(s) used
                    if len(self.rolls)>2:
                        self.rolls=self.rolls[:len(self.rolls)-(roll)//self.rolls[0]]
                    elif roll in self.rolls:
                        del(self.rolls[self.rolls.index(roll)])
                    else:
                        self.rolls=[]
        
        if not self.valid_moves:
            computer_turn = True
            self.rolls = []
        elif not self.rolls:
            computer_turn = True
        self.game.print_board()

        pygame.display.flip()

        # if both rolls have been used up, call the computer move function
        if computer_turn:
            self.computer_turn()
            self.computer_turn()
    
    # function computer_turn:
    #   finds and completes a move for the computer
    def computer_turn(self):
        pygame.time.delay(500)
        move = self.game.computer_move(self.difficulty, random.randint(1, 6))
        if move is None:
            self.comp_no_moves = True
            
        elif move[1] == -1:
            c = ""
            for chip in self.computer_chips:
                if chip.index == move[0]:
                    c = chip
                    
            self.game.finish_piece(move[0],1)
            
            try:
                c.coords=(0,0)
                c.index=999
                self.num_trough_comp = c.draw_trough(self.num_trough_comp)
            except:
                self.error_message("Invalid Move", 335)
                print("Invalid move")
        else:
            for chip in self.computer_chips:
                if chip.index == move[0]:
                    # move the computer piece
                    self.game.move_piece(move[0], move[1], 1)
                    if move[0] == -1:
                        chip.bar = False
                    chip.index = move[1]
                    # if there was a kill, move the user piece to the bar
                    if(move[2] == 1):
                        for u_chip in self.player_chips:
                            if u_chip.index == move[1]:
                                u_chip.index = -1
                                u_chip.bar = True
                                self.game.spots[move[1]].player = 1
                    break
        self.draw_background()
        pygame.display.flip()
      

    # Function: select
    # params: self, the mouse position
    # this function loops through the chip and selects them if they have been clicked
    def select(self, mouse_pos):
        if not self.rolls:
            self.must_roll = True
        elif not self.game_over:
            
            # reset all of the triangles to invalid
            for tri in self.triangles:
                tri.valid = False
            self.player_trough_valid = False

            already_selected=False
            # check to see if the chip was already selected
            for i in range(len(self.player_chips)):
                if self.player_chips[i].selected:
                    already_selected=True
            
            sel = ""

            # loop through the chips
            for i in range(len(self.player_chips)):
                # if a chip has been clicked and has not been selected yet
                if self.player_chips[i].collidepoint(mouse_pos) and not self.player_chips[i].selected and not already_selected:
                    self.selected_chip = [self.player_chips[i], i]
                    self.player_chips[i].selected = True
                    sel = self.player_chips[i].index
                    print("i:", i)
                elif self.player_chips[i].collidepoint(mouse_pos) and self.player_chips[i].selected:
                    self.selected_chip = list()
                    self.player_chips[i].selected = False
            
            # reset the valid moves based on the the selected chip if the rolls are filled
            if self.rolls and sel != "":
                self.show_valid_moves(self.rolls, sel)
        pygame.display.flip()
        
    

    # Function: help_button
    # params: self, the mouse positon, bool help(true on the help screen, false on the main screen)
    # returns: help to keep track of which screen the user is on
    def help_button(self, mouse_pos, help):
        # if the help button is clicked and on the main screen go to the help screen
        if self.button.button.collidepoint(mouse_pos) and not(help):
                self.help_screen()
                help = True
        # if the back button is clicked and on the help screen go back to the main screen
        elif self.button.button.collidepoint(mouse_pos) and help:
                self.main_screen()
                self.draw_background()
                pygame.display.flip()
                help = False
        return help
    

    # 0 don't draw any dice
    # 1 draw one dice
    # 2 draw two dice
    def roll_button(self, mouse_pos):
        # call backend roll function and modify the global variables
        # call the display dice function
        if self.button_roll.button.collidepoint(mouse_pos):
            self.comp_no_moves = False
            if not self.rolls:
                self.must_roll = False
                self.rolls = self.game.roll_dice()
                if self.rolls[0] == self.rolls[1]:
                    self.rolls += []+self.rolls
                    self.num_moves = 4
                # print(self.rolls)
            else:
                self.roll_once = True
            
    # function restart
    #       reinitializes the game from the beginning
    def restart(self, mouse_pos):
        if self.reset.button.collidepoint(mouse_pos):
                self.__init__()
                self.draw_background()
                self.game = Backgam()
                self.rolls = []
                pygame.display.flip()
    
    # function set_difficulty
    #       sets the difficulty for the game
    #       param: mouse_pos, the position of the mouse when the user clicks
    def set_difficulty(self, mouse_pos):
        pressed = (153, 114, 67)
        unpressed = (193, 154, 107)
        if self.diff_1.button.collidepoint(mouse_pos):
            self.diff_1.color = pressed
            self.diff_2.color = unpressed
            self.diff_3.color = unpressed
            self.difficulty = 1
        elif self.diff_2.button.collidepoint(mouse_pos):
            self.diff_2.color = pressed
            self.diff_1.color = unpressed
            self.diff_3.color = unpressed
            self.difficulty = 2
        elif self.diff_3.button.collidepoint(mouse_pos):
            self.diff_3.color = pressed
            self.diff_1.color = unpressed
            self.diff_2.color = unpressed
            self.difficulty = 3
        
    # function dice
    #       Displays the dice on the screen
    #       param: rolls, the list of numbers on the dice
    def dice(self, rolls):
        if(rolls):
            roll_helper=[[],[],[],[],[],[]]
            roll_helper[rolls[0]-1].append([self.WIDTH*13/20, self.HEIGHT/2-self.WIDTH/40])
            pygame.draw.rect(self.screen, (250,250,250), pygame.Rect((self.WIDTH*13/20, self.HEIGHT/2-self.WIDTH/40), (self.WIDTH/20, self.WIDTH/20)))
            if(len(rolls) > 1):
                pygame.draw.rect(self.screen, (250,250,250), pygame.Rect((self.WIDTH*15/20, self.HEIGHT/2-self.WIDTH/40), (self.WIDTH/20, self.WIDTH/20)))
                roll_helper[rolls[1]-1].append([self.WIDTH*15/20, self.HEIGHT/2-self.WIDTH/40])
            if(len(rolls) > 2):
                pygame.draw.rect(self.screen, (250,250,250), pygame.Rect((self.WIDTH*11/20, self.HEIGHT/2-self.WIDTH/40), (self.WIDTH/20, self.WIDTH/20)))
                roll_helper[rolls[2]-1].append([self.WIDTH*11/20, self.HEIGHT/2-self.WIDTH/40])
            if(len(rolls) > 3):
                pygame.draw.rect(self.screen, (250,250,250), pygame.Rect((self.WIDTH*17/20, self.HEIGHT/2-self.WIDTH/40), (self.WIDTH/20, self.WIDTH/20)))
                roll_helper[rolls[3]-1].append([self.WIDTH*17/20, self.HEIGHT/2-self.WIDTH/40])
            

            for i in range(len(roll_helper)):
                for j in roll_helper[i]:
                    if i==0:
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/40, j[1]+self.WIDTH/40), self.WIDTH/200)
                    if i==1:
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                    if i==2:
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/40, j[1]+self.WIDTH/40), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                    if i==3:
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                    if i==4:
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/40, j[1]+self.WIDTH/40), self.WIDTH/200)
                    if i==5:
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH*3/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH/80, j[1]+self.WIDTH*2/80), self.WIDTH/200)
                        pygame.draw.circle(self.screen, (0,0,0), (j[0]+self.WIDTH*3/80, j[1]+self.WIDTH*2/80), self.WIDTH/200)
                    
        pygame.display.flip()

    # function show_valid_moves
    #       finds the valid moves that the player could make based on the chip they selected
    #       modifies the triangles array to set triangles as "valid"
    #       params: rolls, the roll of the dice
    #               loc, the location of the selected chip
    def show_valid_moves(self, rolls, loc):
        self.game.valid_moves=[] 
        print("Loc:", loc)
        self.player_trough_valid = False
        for i in range(len(self.triangles)):
            self.triangles[i].valid=False
        
        valid=[]
        totest=[]
        for i in range(len(rolls)):
            totest.append([[]+rolls,rolls[i],loc,rolls[i]])
        for i in range(len(rolls)):
            curr=[]+totest
            totest=[]
            
            for prob in curr:
                movies=self.game.find_valid_moves(0,prob[1])
                for movie in movies:
                    if movie[0]==loc:
                        valid.append(movie[1])
                        self.valid_moves.append(movie)
                        roll=prob[0][:prob[0].index(prob[3])]+prob[0][prob[0].index(prob[3])+1:]
                        for r in roll:
                            totest.append([roll,prob[1]+r,movie[1],r])
            
        if self.game.bar.num_user_pieces==0 or loc==-1:
            for i in valid:
                if(i != -1):
                    self.triangles[i].valid=True
                else:
                    self.player_trough_valid = True
            
        for i in range(len(self.triangles)):
            if self.triangles[i].valid==True:
                return True
        return False

    def has_won(self):
        if self.num_trough_player == 15:
            self.game_over = True
            pygame.draw.rect(self.screen, (50,230,50), pygame.Rect((self.WIDTH/6, 2*self.HEIGHT/5), (2*self.WIDTH/3, self.HEIGHT/5)))
            self.display_text("Congratulations! You Win!", (160, 280), 40, (255, 255, 255))
        elif self.num_trough_comp == 15:
            self.game_over = True
            pygame.draw.rect(self.screen, (230,50,50), pygame.Rect((self.WIDTH/4, 2*self.HEIGHT/5), (self.WIDTH/2, self.HEIGHT/5)))
            self.display_text("Computer Wins!", (230, 280), 45, (255, 255, 255))


# function main
#       event monitor to run game play and interface interactions
def main():
    d = Display()  
    d.rolls=[]
    running = True
    help = False

    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if not help:
                pygame.Surface.fill(d.screen, (92, 64, 51))
                d.draw_background()
                d.has_won()
                d.dice(d.rolls)
            if(event.type == pygame.MOUSEBUTTONUP):
                d.roll_once = False
                mouse_pos = pygame.mouse.get_pos()
                
                help = d.help_button(mouse_pos, help)

                d.roll_button(mouse_pos)

                d.move_chip(mouse_pos)

                d.restart(mouse_pos)
        
            if(event.type == pygame.MOUSEBUTTONDOWN):
                mouse_pos = pygame.mouse.get_pos()
                d.select(mouse_pos)

                d.set_difficulty(mouse_pos)

            elif event.type == QUIT:
                running = False

main()

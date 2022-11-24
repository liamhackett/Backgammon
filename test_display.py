import unittest
import pygame
from pygame.locals import (BUTTON_LEFT, K_ESCAPE, KEYDOWN, K_SPACE, QUIT)
from triangle import *
from button import Button
from chip import Chip
from game_backend import *
from display import *

# class TestDisplay
#       Child of display, used to initialize the board at the end of the game in order
#       to test the functionality of moving pieces into the troughs
class TestDisplay(Display):
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600

        pale_brown = (152, 118, 84)
        tuscan_brown = (111, 78, 55)
        white = (255, 255, 255)
        red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.game_over = False
        self.rolls = []
        self.game = Backgam()

        # Move all the user pieces to the end
        self.game.move_piece(0, 19, 0)
        self.game.move_piece(0, 19, 0)
        self.game.move_piece(11, 19, 0)
        self.game.move_piece(11, 19, 0)
        self.game.move_piece(11, 20, 0)
        self.game.move_piece(11, 20, 0)
        self.game.move_piece(11, 20, 0)
        self.game.move_piece(16, 21, 0)
        self.game.move_piece(16, 21, 0)
        self.game.move_piece(16, 21, 0)

        # move all the computer pieces to the end
        self.game.move_piece(23, 1, 1)
        self.game.move_piece(23, 1, 1)
        self.game.move_piece(12, 2, 1)
        self.game.move_piece(12, 2, 1)
        self.game.move_piece(12, 2, 1)
        self.game.move_piece(12, 2, 1)
        self.game.move_piece(12, 3, 1)
        self.game.move_piece(7, 3, 1)
        self.game.move_piece(7, 3, 1)
        self.game.move_piece(7, 4, 1)

        self.game.print_board()

        self.computer_no_moves = False
        self.roll_once = False
        self.must_roll = True
        self.selected_chip = list()
        self.valid_moves = list()

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
        
        self.computer_trough =  pygame.Rect((735, 40), (50, 250))

        self.num_trough_player = 0
        self.num_trough_comp = 0
        self.player_trough_valid = False
        self.num_bar_p = 0
        self.num_bar_c = 0

        self.num_moves = 2

def main():
    d = TestDisplay()  
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
                mouse_pos = pygame.mouse.get_pos()
                
                help = d.help_button(mouse_pos, help)
                
                d.roll_button(mouse_pos)

                d.move_chip(mouse_pos)

                #d.move_to_player_trough(mouse_pos)

                d.restart(mouse_pos)
        
            if(event.type == pygame.MOUSEBUTTONDOWN):
                mouse_pos = pygame.mouse.get_pos()
                d.select(mouse_pos)

                d.set_difficulty(mouse_pos)

            elif event.type == QUIT:
                running = False

main()


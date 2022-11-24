import pygame
from chip import Chip

WIDTH = 800
HEIGHT = 600

class Triangle:
    def __init__(self, num_pieces, player, location, color):
        self.num_pieces = num_pieces
        self.player = player
        self.location = location
        self.pos=(12-location if location<12 else location-11)
        self.orientation=(-1 if location<12 else 1)
        self.clicked=False
        self.hovered=False
        self.valid=False
        self.points=[]
        self.base_color=color
        self.color=color
        width=(WIDTH*.8)/12
        height=(HEIGHT)*9/20
        pos=self.pos
        orientation=self.orientation
        self.points.append((pos*WIDTH*.8/12+(WIDTH/20 if pos<=6 else WIDTH/10),(HEIGHT/20 if orientation==-1 else HEIGHT-HEIGHT/20)))
        self.points.append((pos*WIDTH*.8/12-width+(WIDTH/20 if pos<=6 else WIDTH/10),(HEIGHT/20 if orientation==-1 else HEIGHT-HEIGHT/20)))
        self.points.append((pos*WIDTH*.8/12-width/2+(WIDTH/20 if pos<=6 else WIDTH/10),(height if orientation==-1 else HEIGHT-height)))
        self.border=[]
        self.border.append((pos*WIDTH*.8/12+5+(WIDTH/20 if pos<=6 else WIDTH/10),(HEIGHT/20 if orientation==-1 else HEIGHT-HEIGHT/20)))
        self.border.append((pos*WIDTH*.8/12-5-width+(WIDTH/20 if pos<=6 else WIDTH/10),(HEIGHT/20 if orientation==-1 else HEIGHT-HEIGHT/20)))
        self.border.append((pos*WIDTH*.8/12-width/2+(WIDTH/20 if pos<=6 else WIDTH/10),(height+5 if orientation==-1 else HEIGHT-height-5)))

        
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
    
    def draw(self, screen):
        # draw the triangle first
        if self.valid:
            self.color=(150,150,150)
        else:
            self.color=self.base_color
        if self.hovered:
            pygame.draw.polygon(surface=screen, color=(0,0,0), points=self.border)
        pygame.draw.polygon(surface=screen, color=(self.color[0],self.color[1],self.color[2]),points=self.points)



    def collidepoint(self, mouse_pos):
        y=mouse_pos[1]
        x=mouse_pos[0]
        points=self.points
        m01=(points[0][1]-points[1][1])/(points[0][0]-points[1][0])
        b01=points[0][1]-m01*points[0][0]
        m12=(points[1][1]-points[2][1])/(points[1][0]-points[2][0])
        b12=points[1][1]-m12*points[1][0]
        m02=(points[0][1]-points[2][1])/(points[0][0]-points[2][0])
        b02=points[0][1]-m02*points[0][0]
        if self.orientation == 1:
            if y<=m01*x+b01 and y>=m12*x+b12 and y>=m02*x+b02:
                if self.clicked:
                    self.clicked=False
                else: 
                    self.clicked=True
                return True
        elif self.orientation == -1:
            if y>=m01*x+b01 and y<=m12*x+b12 and y<=m02*x+b02:
                if self.clicked:
                    self.clicked=False
                else: 
                    self.clicked=True
                return True
        return False

    def hover(self, mouse_pos):
        y=mouse_pos[1]
        x=mouse_pos[0]
        points=self.points
        m01=(points[0][1]-points[1][1])/(points[0][0]-points[1][0])
        b01=points[0][1]-m01*points[0][0]
        m12=(points[1][1]-points[2][1])/(points[1][0]-points[2][0])
        b12=points[1][1]-m12*points[1][0]
        m02=(points[0][1]-points[2][1])/(points[0][0]-points[2][0])
        b02=points[0][1]-m02*points[0][0]
        if self.orientation == 1:
            if y<=m01*x+b01 and y>=m12*x+b12 and y>=m02*x+b02:
                if self.hovered:
                    self.hovered=False
                else: 
                    self.hovered=True
                return True
        elif self.orientation == -1:
            if y>=m01*x+b01 and y<=m12*x+b12 and y<=m02*x+b02:
                if self.hovered:
                    self.hovered=False
                else: 
                    self.hovered=True
                return True
        return False    
    

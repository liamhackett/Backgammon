from cv2 import sqrt
import pygame

# Height for each chip position in the top set of triangles 52, 96. 140, 184, 228
# Height for each chip position in the bottom set of triangles 373, 417, 461, 505, 549

class Chip(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y, screen, id, index):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.coords = (x, y)
        self.radius = radius
        self.selected = False
        self.id = id
        self.trough = False
        self.bar = False
        self.index = index
        self.sel_color = (200, 200, 200)

    def draw_chip(self):
        if not self.trough:
            if self.selected:
                pygame.draw.circle(self.screen, self.sel_color, self.coords, self.radius)
            else:
                pygame.draw.circle(self.screen, self.color, self.coords, self.radius)
        else:
            self.draw_trough(self.num)

    def draw(self, color):
        self.color = color
        pygame.draw.circle(self.screen, color, self.coords, self.radius)
        
    def move(self, x, y):
        self.coords = (x, y)
        pygame.draw.circle(self.screen, self.color, self.coords, self.radius)
             
    def move_bar(self, coords):
        self.coords = coords
        pygame.draw.circle(self.screen, self.color, self.coords, self.radius)
    
    def move(self, start, end, triangles):
        top_y = [52, 96, 140, 184, 228]
        bottom_y = [549, 505, 461, 417, 373]
        if start>end and self.id == 0:
            self.x = triangles[end].points[0][0]-26
            if triangles[end].orientation == -1:
                self.y =  top_y[min(triangles[end].num_pieces,4)]
                self.coords = (self.x, self.y)
            elif triangles[end].orientation == 1:
                self.y =  bottom_y[min(triangles[end].num_pieces,4)]
                self.coords = (self.x, self.y)
            triangles[start].num_pieces-=1
            triangles[end].num_pieces+=1
            pygame.draw.circle(self.screen, self.color, self.coords, self.radius)
        elif self.id == 0 and self.bar:
            self.x = triangles[end].points[0][0]-26
            self.y =  top_y[min(triangles[end].num_pieces,4)]
            self.coords = (self.x, self.y)
            triangles[end].num_pieces+=1
            pygame.draw.circle(self.screen, self.color, self.coords, self.radius)
        else:
            print("Can't go backwards")
            

    def collidepoint(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]

        if x >= (self.coords[0] + self.radius) or x <= (self.coords[0] - self.radius):
            return False
        if y >= (self.coords[1] + self.radius) or y <= (self.coords[1] - self.radius):
            return False
        return True
    
    def is_overlapping(self, other):
        return sqrt((other.coords[0] - self.coords[0])*(other.coords[0] - self.coords[0]) + (other.coords[1] - self.coords[1])*(other.coords[1] - self.coords[1]) <= self.coords[0] + self.radius)
    
    
    def draw_trough(self, num_in_trough):
        self.num = num_in_trough
        if self.id == 0:
            pygame.draw.rect(self.screen, self.color, pygame.Rect((735,561-(250/15)*(num_in_trough+1)), (50, 250/15)))
            num_in_trough +=1
            return num_in_trough
        if self.id == 1:  
            self.trough = True
            pygame.draw.rect(self.screen, self.color, pygame.Rect((735, 40+(250/15*num_in_trough)), (50, 250/15)))
            num_in_trough +=1
            return num_in_trough

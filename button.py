import pygame

class Button:  
    def __init__(self,color, x, y, length, width, screen):
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.screen = screen
        self.button = pygame.Rect(self.x, self.y, self.length, self.width)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.button)
        

    
    
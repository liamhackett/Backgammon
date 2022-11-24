from triangle import *

import pygame

from pygame.locals import(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, KEYUP)

WIDTH = 800
HEIGHT = 600

import unittest

class TestBlocks(unittest.TestCase):

    def test_triangle(self):
        t=Triangle(0,-1,12,(25,25,25))
        self.assertEqual(t.base_color,(25,25,25))
        self.assertEqual(t.points,[(1*WIDTH*.8/12+WIDTH/20,HEIGHT/20),(1*WIDTH*.8/12-(WIDTH*.8)/12+WIDTH/20,HEIGHT/20),(1*WIDTH*.8/12-(WIDTH*.8)/12/2+WIDTH/20,(HEIGHT)*9/20)])
        t=Triangle(0,-1,18,(25,25,25))
        self.assertEqual(t.base_color,(25,25,25))
        self.assertEqual(t.points,[(7*WIDTH*.8/12+WIDTH/10,HEIGHT/20),(7*WIDTH*.8/12-(WIDTH*.8)/12+WIDTH/10,HEIGHT/20),(7*WIDTH*.8/12-(WIDTH*.8)/12/2+WIDTH/10,(HEIGHT)*9/20)])
        t=Triangle(0,-1,11,(25,25,25))
        self.assertEqual(t.base_color,(25,25,25))
        self.assertEqual(t.points,[(1*WIDTH*.8/12+WIDTH/20,HEIGHT-HEIGHT/20),(1*WIDTH*.8/12-(WIDTH*.8)/12+WIDTH/20,HEIGHT-HEIGHT/20),(1*WIDTH*.8/12-(WIDTH*.8)/12/2+WIDTH/20,HEIGHT-(HEIGHT)*9/20)])
        t=Triangle(0,-1,5,(25,25,25))
        self.assertEqual(t.base_color,(25,25,25))
        self.assertEqual(t.points,[(7*WIDTH*.8/12+WIDTH/10,HEIGHT-HEIGHT/20),(7*WIDTH*.8/12-(WIDTH*.8)/12+WIDTH/10,HEIGHT-HEIGHT/20),(7*WIDTH*.8/12-(WIDTH*.8)/12/2+WIDTH/10,HEIGHT-(HEIGHT)*9/20)])

unittest.main()
    

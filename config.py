
try:
    import sys, os, platform, random
    import pygame
    from pygame.locals import *
except:
    print("No PyGame installation found!")

# screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_RECT = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)   # screen dimensions

# colors
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
YELLOW   = (255, 255,   0)
GREEN    = (0,   255,   0)
NEO      = (153, 185, 163)
#NEO      = (199, 209, 204)
#NEO      = (182, 211, 194)
#NEO      = (156, 189, 168)

# keyboard keys
DIRECT_DICT = {K_LEFT : 0x01, K_RIGHT : 0x02, K_UP : 0x04, K_DOWN : 0x08, K_SPACE : 0x10}

# pirates
(TANK1, TANK2, TANK3, TANK4, TANK5, TANK6) = range(1,7)

# user define events
(DUMMY_EVENT, ATTACK_PLAYER, PLAYER_RESTART, TANK_EXIT, SCORE, NEW_WAVE, BONUS_LEVEL, GAME_OVER) = range(USEREVENT+1, USEREVENT+9)

# misc constants
FPS = 30    # frames per second
FONT = 'freesansbold.ttf'
FONT_PATH = FONT
CAPTION = "PyRipOff - Esc: quit"
HIGHSCORE = 'highscore.txt'

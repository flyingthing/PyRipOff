
from config import *
import math
import pickle


# return distance between two obj
def getDistance(x1, y1, x2, y2):
    return math.hypot(abs(x1 - x2), abs(y1 - y2))

# return degree angle between 0-360
def getAngle(x1, y1, x2, y2):
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise)   # get the angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360      # adjust for a right-facing sprite
    return int(angle)               # Return value is 0 for right, 90 for up, 180 for left, and 270 for down

# return slope of angle
def getSlope(angle):
    if angle % 15 == 0:
        return {  0: (1, 0),
             15: ((math.sqrt(6)+math.sqrt(2))/4, -(math.sqrt(6)-math.sqrt(2))/4),
             30: (math.sqrt(3)/2, -1/2),
             45: (math.sqrt(2)/2, -math.sqrt(2)/2),
             60: (1/2, -math.sqrt(3)/2),
             75: ((math.sqrt(6)-math.sqrt(2))/4, -(math.sqrt(6)+math.sqrt(2))/4),
             90: (0, -1),
            105: ((-math.sqrt(6)+math.sqrt(2))/4, -(math.sqrt(6)+math.sqrt(2))/4),
            120: (-1/2, -(math.sqrt(3)/2)),
            135: (-(math.sqrt(2)/2), -(math.sqrt(2)/2)),
            150: (-math.sqrt(3)/2, -1/2),
            165: (-(math.sqrt(6)+math.sqrt(2))/4, -(math.sqrt(6)-math.sqrt(2))/4),
            180: (-1, 0),
            195: (-(math.sqrt(6)+math.sqrt(2))/4, (math.sqrt(6)-math.sqrt(2))/4),
            210: (-math.sqrt(3)/2, 1/2),
            225: (-math.sqrt(2)/2, math.sqrt(2)/2),
            240: (-1/2, math.sqrt(3)/2),
            255: (-(math.sqrt(6)-math.sqrt(2))/4, (math.sqrt(6)+math.sqrt(2))/4),
            270: (0, 1),
            285: ((math.sqrt(6)-math.sqrt(2))/4, (math.sqrt(6)+math.sqrt(2))/4),
            300: (1/2, math.sqrt(3)/2),
            315: (math.sqrt(2)/2, math.sqrt(2)/2),
            330: (math.sqrt(3)/2, 1/2),
            345: ((math.sqrt(6)+math.sqrt(2))/4, (math.sqrt(6)-math.sqrt(2))/4)
            }[angle]
    else:
        return math.cos(angle), math.sin(angle)

def getHighScore():
    highscore = 0
    try:
        with open(HIGHSCORE,'rb') as file:
            highscore = pickle.load(file)
    except IOError as e:
        # doesn't exists
        pass

    return highscore

def topScore(score):
    try:
        with open(HIGHSCORE,'wb') as file:
            pickle.dump(score, file)
    except IOError as e:
        # doesn't exits
        pass

# use subsurface from screen???
def convertNum2Image(num, digitImages, plusflg = False):
        width = 23
        height = 23
        offset = 0
        numwidth = _numwidth(num, plusflg)
        surface = pygame.Surface((numwidth, height))
        if plusflg == True:
            image = digitImages["plus"]
            surface.blit(image, (offset, 0), None, pygame.BLEND_MAX)
            offset = image.get_rect().width

        strnum = str(num)
        if num == 0:
            strnum = "00"

        for c in strnum:
            digit = int(c)
            image = digitImages[digit]
            surface.blit(image,(offset,0), None, pygame.BLEND_MAX)
            offset += image.get_rect().width

        return surface

def _numwidth(num, flg):
    width = 0
    if num == 0:
        width = 23
    for c in str(num):
        if c == '1':
            width += 9
        else:
            width += 23

    if flg == True:
        width += 23

    return width


# simple class that print to the screen
class TextPrint:

    def __init__(self, screen):
        self.reset(0,0)
        self.font = pygame.font.Font(None, 18)
        self.color = WHITE
        self.screen = screen

    def prnt(self, text):
        textBitmap = self.font.render(text, True, self.color)
        self.screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def prntcenterx(self, text, y = None):
        textBitmap = self.font.render(text, True, self.color)
        width, height = textBitmap.get_size()
        x = int(SCREEN_WIDTH/2) - int(width/2)
        if y == None:
            y = self.y
        self.screen.blit(textBitmap, [x, y])

    def setfontsize(self, size):
        self.font = pygame.font.Font(None, size)
        self.line_height = size

    def setcolor(self, color):
        self.color = color

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.line_height = 18
        self.font = pygame.font.Font(None,18)

class gameFPS(pygame.sprite.Sprite):
    def __init__(self,color=BLACK):
        super(gameFPS,self).__init__()
        self.clock = 0
        self.color = color
        self.toggle = 0
        self.fps = ""

    def toggleDisplay(self):
        self.toggle = 1 - 0

    def update(self):
        color = BLACK
        if self.toggle == 1:
            self.color = NEO
        else:
            self.color = BLACK
        #self.fps = "FPS: {:.2f}".format(self.clock)
        self.fps = "FPS: " + str(self.clock)
        #text = Text(FONT,12,fps,color,SCREEN_WIDTH - 90, SCREEN_HEIGHT - BORDERTHICKNESS)
        #self.image = text.surface
        #self.rect = text.rect

    def draw(self, screen):
        #super(gameFPS,self).draw(screen)
        textPrint = TextPrint(screen)
        textPrint.color = self.color
        textPrint.prnt(self.fps)
        pass

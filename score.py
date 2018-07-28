from config import *
from animate import *
from utils import *

""" sample scoring
TANK POINTS    # SCORE
1      10      2=20
2      20      2=60
3      30      2=120
4      40      2=200
5      50      2=300
6      60      2=420
BONUS LEVEL +10
1      20      3=480
2      30      3=570
3      40      3=690
4      50      3=840
5      60      3=1020
6      70      3=1230
BONUS LEVEL +20
1      30      3=1320  
"""

_digitImages = {}

class Score(animateObj):
    def __init__(self, score, top):
        super(Score, self).__init__()

        self.top = top
        self.score = score

        for i in [0,1,2,3,4,5,6,7,8,9]:
            src = "./images/" + str(i) + ".png"
            image = pygame.image.load(src).convert_alpha()
            _digitImages[i] = image

        src = "./images/plus.png"
        image = pygame.image.load(src).convert_alpha()
        _digitImages["plus"] = image

    def killpirate(self, tank):
        self.score += (Bonus.points * tank)

    def getScore(self):
        return self.score

    def update(self):
        pass

    def draw(self, screen):
        surface = convertNum2Image(self.score, _digitImages)
        left = int(SCREEN_WIDTH/2) - int(surface.get_width()/2)
        rect = pygame.Rect(left, self.top, surface.get_width(), surface.get_height())
        screen.blit(surface, rect, None, pygame.BLEND_MAX)


class Bonus(animateObj):
    points = 10

    @staticmethod
    def nextlevel():
        Bonus.points += 10

    @staticmethod
    def curlevel():
        return Bonus.points

    def __init__(self):
        super(Bonus, self).__init__()

        src = "./images/bonuslevel.png"
        self.image = pygame.image.load(src).convert_alpha()

    def update(self):
        pass

    def draw(self,screen):
        x = int(SCREEN_WIDTH/2) #- int(self.rect.width/2)
        y = int(SCREEN_HEIGHT/2) #- int(self.rect.height/2)
        rect = self.image.get_rect()
        rect.centerx = x
        rect.centery = y
        screen.blit(self.image, rect, None, pygame.BLEND_MAX)

        surface = convertNum2Image(Bonus.points, _digitImages, True)
        left = int(SCREEN_WIDTH / 2) - int(surface.get_width()/2)
        top = rect.bottom + 10
        rect = pygame.Rect(left, top, surface.get_width(), surface.get_height())
        screen.blit(surface, rect, None, pygame.BLEND_MAX)
import config
from collections import deque
from animate import *
from utils import *
from canister import *
from spline import *
from ai import *

class pirate(animateObj):
    grp = pygame.sprite.Group()

    @staticmethod
    def getGroup():
        return pirate.grp

    @staticmethod
    def clrGroup():
        pirate.grp.empty()

    def __init__(self, tank):
        super(pirate, self).__init__()

        src = "./images/tank" + str(tank) + ".png"

        image = pygame.image.load(src).convert_alpha()
        self.rotatedimages = {}
        for degree in range(0,360,15):
            # rotate a copy of the image
            rotatedSurf = pygame.transform.rotate(image, degree)
            self.rotatedimages[degree] = rotatedSurf
        self.restart()
        pirate.grp.add(self)
        self.target = None
        self.dx = 0
        self.dy = 0
        self.spline = Spline()
        self.coors = []
        self.indx = 0
        self.angle = 0
        self.exitangle = 0
        self.hookit = False
        self.ai = AIState()
        self.targetq = deque()

    def restart(self):
        self.x = int(random.random() * 640)
        if random.randrange(0,2) == 0:
            self.y = -10
            self.angle = 270
        else:
            self.y = 490
            self.angle = 90

        self.image = self.rotatedimages[self.angle]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def rotateangle(self, angle):
        rotatedSurf = pygame.transform.rotate(self.rotatedimages[0], angle)
        self.image = rotatedSurf
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def rotate_counterclockwise(self):
        self.rotate(15)

    def rotate_clockwise(self):
        self.rotate(345)

    def rotate(self, angle):
        self.angle += angle
        self.angle = self.angle % 360
        #print(self.angle)
        self.rotateangle(self.angle)

    def update(self):
        pass

    def mov(self):
        flg = True
        if self.indx < len(self.coors):
            if len(self.targetq) >= 18:
                x,y = self.targetq.popleft()
                self.target.rect.center = (x, y)
            else:
                pass
            self.angle, self.x, self.y  = self.coors[self.indx]
            self.rotateangle(self.angle)
            #self.y = self.coors[self.indx][1]
            #self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            if self.hookit == True:
                self.targetq.append((self.x,self.y))
            self.indx += 1
        else:
            if len(self.targetq) > 0:
                x, y = self.targetq.popleft()
                self.target.rect.center = (x, y)
            else:
                flg = False
        return flg

    def hook_it(self):
        stat = False
        if self.angle != self.exitangle:
            self.rotate(15)
        else:
            stat = True
            self.hookit = True
        return stat

    def draw(self, screen):
        super(pirate, self).draw(screen)

        if self.hookit == True:
            pygame.draw.line(screen, NEO, (self.rect.centerx, self.rect.centery), (self.target.rect.centerx, self.target.rect.centery), 2 )

        """
        i = 0
        for cp in self.spline.ControlPoints:
            #pygame.draw.circle(screen, [RED, YELLOW, GREEN][i % 3], (int(cp[0]), int(cp[1])), 4)
            i = i+1
        """

        if len(self.spline.ControlPoints) >= 3:
            finalpoints = self.spline.wayPoints()






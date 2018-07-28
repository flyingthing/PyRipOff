import config
from animate import *
from utils import *

cannonshotimage = None

class player(animateObj):
    def __init__(self, screen):
        super(player, self).__init__()

        self.screen = screen
        src = "./images/player.png"
        image = pygame.image.load(src).convert_alpha()
        self.rotatedimages = {}
        for degree in range(0,360,15):
            # rotate a copy of the image
            rotatedSurf = pygame.transform.rotate(image, degree)
            self.rotatedimages[degree] = rotatedSurf
        self.restart()

        src = "./images/cannonshot.png"
        global cannonshotimage
        cannonshotimage = pygame.image.load(src).convert_alpha()


    def restart(self):
        self.x = 640 - 100
        self.y = 480 - 480 / 3 - 10
        self.angle = 180
        self.image = self.rotatedimages[self.angle]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def rotate_counterclockwise(self):
        self.rotate(15)

    def rotate_clockwise(self):
        self.rotate(345)

    def rotate(self, angle):
        self.angle += angle
        self.angle = self.angle % 360
        self.image = self.rotatedimages[self.angle]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        pass

    def mov(self):
        dx, dy = getSlope(self.angle)
        #super(player,self).mov(dx * 4, dy * 4)

        # test if player moves outside of boundary
        if self.screen.get_rect().contains(self.rect) == False:
            if self.angle == 0:
                pass
            elif self.angle > 0 and self.angle < 90:
                self.angle = 90
                self.rotate(0)
                super(player, self).mov(dx * 4, dy * 4)
            elif self.angle == 90:
                pass
            elif self.angle > 90 and self.angle < 180:
                self.angle = 180
                self.rotate(0)
                super(player, self).mov(dx * 4, dy * 4)
            elif self.angle == 180:
                pass
            elif self.angle > 180 and self.angle < 270:
                self.angle = 270
                self.rotate(0)
                super(player, self).mov(dx * 4, dy * 4)
            elif self.angle == 270:
                pass
            elif self.angle > 270 and self.angle < 360:
                self.angle = 0
                self.rotate(0)
                super(player, self).mov(dx * 4, dy * 4)
        else:
            super(player, self).mov(dx * 4, dy * 4)



class cannonshot(animateObj):
    def __init__(self, angle, x, y):
        super(cannonshot, self).__init__(x,y)
        self.image = cannonshotimage
        dx, dy = getSlope(angle)
        self.dx = dx * 8
        self.dy = dy * 8
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        pass

    def mov(self,x=0,y=0):
        super(cannonshot,self).mov(self.dx, self.dy)
        if 0 >= self.rect.centerx:
            self.kill()
        elif self.rect.centerx > SCREEN_WIDTH:
            self.kill()
        elif 0 >= self.rect.centery:
            self.kill()
        elif self.rect.centery > SCREEN_HEIGHT:
            self.kill()



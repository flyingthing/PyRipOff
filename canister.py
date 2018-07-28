import config
from animate import *

class canister(animateObj):
    def __init__(self, direction, x, y, callback, images):
        super(canister, self).__init__(x,y,callback)
        for i in range(0, len(images)):
            self.images.append(images[i])
        self.addpattern("pulse", [0,0,0,0,1,1,1,1])
        self.setpattern("pulse")
        self.rect = self.images[0].get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.tagged = False

    def rotate(self, angle):
        for i in range(0, len(self.images)):
            rotatedSurf = pygame.transform.rotate(self.images[i], angle)
            self.images[i] = rotatedSurf

    def draw(self, screen):
        super(canister,self).draw(screen)
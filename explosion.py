import config
from animate import *

class explodsion(animateObj):
    def __init__(self, x, y, callback, images, flg, pattern):
        super(explodsion,self).__init__(x,y,callback)
        angle = 0
        if flg == True:
            angle = [0,90,180,270][random.randrange(0,4)]
        for i in range(0, len(images)):
            image = pygame.transform.rotate(images[i], angle)
            self.images.append(image)

        self.addpattern("expl", pattern)
        self.setpattern("expl")
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.center = (x,y)

class playerExplode(explodsion):
    def __init__(self, x, y, callback, images):
        super(playerExplode, self).__init__(x, y, callback, images, False, [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15] )

class pirateExplode(explodsion):
    def __init__(self, x, y, callback, images):
        super(pirateExplode, self).__init__(x, y, callback, images, False, [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10] )

class playerpirateCollision(explodsion):
    def __init__(self, flg, x, y, callback, images):
        super(playerpirateCollision, self).__init__(x, y, callback, images, flg, [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14])


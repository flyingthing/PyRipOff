from config import *

class animateObj(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, callback=None):
        super(animateObj, self).__init__()
        self.x = x
        self.y = y
        self.index = 0
        self.image = None
        self.images = []
        self.patterndictionary = {}
        self.pattern = []
        self.rect = None
        self.callback = callback
        self.patternkey = None

    def addpattern(self, name, array):
        self.patterndictionary.update({name: array})

    def setpattern(self, pattern):
        self.pattern = self.patterndictionary[pattern]
        if self.image is None:
            self.image = self.images[self.pattern[0]]
        self.patternkey = pattern

    def update(self):
        self.index += 1
        if self.index >= len(self.pattern):
            if self.callback is not None:
                self.callback(self)
            self.index = 0
        self.image = self.images[self.pattern[self.index]]

    def draw(self, screen):
        #if self.rect != None:
        screen.blit(self.image, self.rect, None, pygame.BLEND_MAX)

    def mov(self, x, y):
        self.x += x
        self.y += y
        self.rect.center = (self.x, self.y)

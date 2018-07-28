from config import *
from game import *
from utils import *

GAME_STATES = ["Play"]  # game states

screen = None
highscore = None

# handles our game states(screens)
class GameState:
    def __init__(self):
        self.lastscreen = None

        # prepare pygame environment
        os.environ['SDL_VIDEO_CENTERED'] = '1'      # center the screen
        pygame.init()
        pygame.display.set_caption(CAPTION)
        pygame.mouse.set_visible(0)
        pygame.font.init()

        global screen
        screen = pygame.display.set_mode(SCREEN_RECT.size)

        # if platform.system() == "Windows":
        #icon = pygame.image.load(imagefiles['icon']).convert_alpha()
        #pygame.display.set_icon(icon)

        self.sprites = pygame.sprite.Group()
        self.keys = pygame.key.get_pressed()

        # game states
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        self.score = Score(0, int(SCREEN_HEIGHT / 2) - 70)

        # check for highscore file
        highscore = 0
        if os.path.isfile(HIGHSCORE) == False:
            topScore(highscore)
        else:
            highscore = getHighScore()

        top = int(SCREEN_HEIGHT) - 60
        self.topScore = Score(highscore, top)


    def start(self):
        self.sprites.empty()
        self.keys = pygame.key.get_pressed()

        src = "./images/RipOff.png"
        image1 = pygame.image.load(src).convert_alpha()
        rect = image1.get_rect()
        rect.centerx = int(SCREEN_WIDTH/2)
        rect.centery = int(SCREEN_HEIGHT/4)
        #self.sprites.add(image1)

        pirates = []
        canisters = []
        canisterImages = []

        self.ai = None

        self.player = player(screen)

        for i in range(1,3):
            src = "./images/canister" + str(i) + ".png"
            image = pygame.image.load(src).convert_alpha()
            canisterImages.append(image)

        # init canisters
        centerx = int(SCREEN_WIDTH / 2)
        centery = int(SCREEN_HEIGHT / 2)
        for d, x, y in [("L", -20, 0), ("R", 20, 0), ("L", -25, -25), ("R", 25, -25), ("L", -25, 25), ("R", 25, 25),
                            ("L", 0, -15), ("R", 0, 15)]:
            fuel = canister(d, centerx + x, centery + y, None, canisterImages)
            if d == "L":
                    fuel.rotate(180)
            self.sprites.add(fuel)
            canisters.append(fuel)

        for num in range(1, 3):
            tank = pirate(TANK1)
            pirates.append(tank)
            self.sprites.add(tank)
        self.ai = ai(self.player, pirates, canisters)

        self.sprites.add(self.topScore)

        toggle = 1
        pygame.time.set_timer(DUMMY_EVENT, 500)  # blink timer

        # ready to print
        textPrint = TextPrint(screen)
        textPrint.color = NEO
        while True:
            # EVENT PROCESSING STEP
            for e in pygame.event.get():  # User did something
                if e.type == pygame.QUIT or self.keys[K_ESCAPE]: # user clicked close
                    pygame.time.set_timer(DUMMY_EVENT, 0)
                    pygame.quit()
                    sys.exit()
                elif e.type in (KEYUP, KEYDOWN):
                    self.keys = pygame.key.get_pressed()
                    if self.keys[K_SPACE]:
                        pygame.time.set_timer(DUMMY_EVENT, 0)   # kill timer
                        gs.go("play")
                    elif self.keys[K_F1]:
                        pygame.time.set_timer(DUMMY_EVENT, 0)   # kill timer
                        self.lastscreen = "start"
                        gs.go("how2play")
                elif e.type == DUMMY_EVENT:
                    toggle = 1 - toggle
                elif e.type == TANK_EXIT:
                    tank = e.tank
                    fuel = tank.target
                    fuel.kill()
                    canisters.remove(fuel)
                    pirates.remove(tank)
                    tank.kill()
                    tmp = len(canisters)
                    if len(canisters) > 0:
                        if len(pirates) == 0:
                            for num in range(1, 3):
                                tank = pirate(TANK1)
                                pirates.append(tank)
                                self.sprites.add(tank)
                            self.ai = ai(self.player, pirates, canisters)


            # clear the screen
            screen.fill(BLACK)

            if toggle == 1:
                textPrint.prntcenterx("How To Play: F1    Start Game: SPACEBAR", SCREEN_HEIGHT - 20)

            y = rect.bottom + 10
            textPrint.prntcenterx(u"\u00A9" + " 1980 Cinematronics Inc.", y)
            screen.blit(image1, rect, None, pygame.BLEND_MAX)

            if self.ai != None:
                self.ai.action()

            for sprite in self.sprites:
                sprite.draw(screen)

            # update sprites
            self.sprites.update()

            # update the screen with what we've drawn.
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)  # maintain frame rate

    def gameover(self):
        self.saveHighScore()
        textPrint = TextPrint(screen)
        self.sprites.empty()
        self.keys = pygame.key.get_pressed()
        self.sprites.add(self.score)
        self.sprites.add(self.topScore)

        toggle = 1
        pygame.time.set_timer(DUMMY_EVENT, 500)  # timer

        done = False
        while done == False:
            # event processing
            for e in pygame.event.get():  # User did something
                if e.type == pygame.QUIT or self.keys[K_ESCAPE]: # If user clicked close
                    pygame.time.set_timer(DUMMY_EVENT, 0)
                    done = True  # Flag that we are done so we exit this loop
                elif e.type in (KEYUP, KEYDOWN):
                    self.keys = pygame.key.get_pressed()
                    if self.keys[K_SPACE]:
                        pygame.time.set_timer(DUMMY_EVENT, 0)
                        gs.go("play")
                        pass
                elif e.type == DUMMY_EVENT:
                    #pygame.time.set_timer(NEW_WAVE, 0)  # kill timer
                    toggle = 1 - toggle

            # clear the screen
            screen.fill(BLACK)


            for sprite in self.sprites:
                sprite.draw(screen)

            textPrint.reset(0,0)
            textPrint.setcolor(NEO)
            if toggle == 1:
                textPrint.prntcenterx("Start Game: SPACEBAR", SCREEN_HEIGHT - 20, )

            # update the screen with what we've drawn.
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)  # maintain frame rate
        pygame.quit()
        sys.exit()

    def how2play(self):
        src = "./images/RipOff.png"
        image1 = pygame.image.load(src).convert_alpha()
        rect = image1.get_rect()
        rect.x = 10
        rect.y = 40


        toggle = 1
        pygame.time.set_timer(DUMMY_EVENT, 500)  # blink timer
        self.keys = pygame.key.get_pressed()
        textPrint = TextPrint(screen)
        textPrint.color = NEO
        while True:
            # event processing
            for e in pygame.event.get():  # user did something
                if e.type == pygame.QUIT: # user clicked close
                    pygame.time.set_timer(DUMMY_EVENT, 0)   # kill timer
                    pygame.quit()
                    sys.exit()
                elif e.type == KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                    if self.keys[K_ESCAPE]:
                        pygame.quit()
                        sys.exit()
                    else:
                        gs.go(self.lastscreen)
                elif e.type == DUMMY_EVENT:
                    #pygame.time.set_timer(NEW_WAVE, 0)  # kill timer
                    toggle = 1 - toggle

            # redraw sprites
            screen.fill(Color('black'))

            screen.blit(image1, rect, None, pygame.BLEND_MAX)

            textPrint.reset(320,40)
            textPrint.setcolor(NEO)
            textPrint.prnt("SCORE POINTS BY SHOOTING PIRATES.")
            textPrint.prnt("PIRATE VALUES ADVANCE WHEN ONE FULL WAVE")
            textPrint.prnt("IS DESTROYED.  DESTROYING ALL SIX CLASSES")
            textPrint.prnt("OF PIRATES ADDS TEN POINTS TO BONUS LEVEL.")

            textPrint.prnt("")
            textPrint.prnt("GAME IS OVER WHEN ALL FUEL CANISTERS" )
            textPrint.prnt("HAVE BEEN RIPPED-OFF.")

            textPrint.setfontsize(32)
            textPrint.prnt("")
            #.setcolor(WHITE)
            textPrint.prntcenterx("Player Controls")
            textPrint.setfontsize(18)
            #textPrint.print("")
            textPrint.reset(230,230)
            textPrint.prnt("UP ARROW KEY - Move Forward")
            textPrint.prnt("LEFT ARROW KEY - Rotate Left")
            textPrint.prnt("RIGHT ARROW KEY - Rotate Right")
            textPrint.prnt("SPACEBAR KEY - Fire Cannon")
            textPrint.prnt("F1 KEY - Pause game")
            textPrint.prnt("F2 KEY - Toggle frames-per-second display")
            textPrint.prnt("ESC KEY - Quit game")

            textPrint.setcolor(NEO)

            if toggle == 1:
                textPrint.prntcenterx("Press Any Key to Exit", SCREEN_HEIGHT - 20)

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def saveHighScore(self):
        score = self.score.getScore()
        if score > self.topScore.getScore():
            topScore(score)
            self.topScore.score = score


    def play(self):
        game = Game(screen, self.score)
        game.run()
        self.go("gameover")

    def go(self, gamestate):
        if hasattr(self, gamestate):
            getattr(self, gamestate)()


if __name__ == "__main__":
    gs = GameState()
    gs.go("start")
    pygame.quit()
    sys.exit()


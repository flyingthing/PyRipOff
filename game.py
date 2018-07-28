from config import *
from player import *
from pirate import *
from explosion import *
from canister import *
from ai import *
from score import *

class Game:
    def __init__(self, screen, score):
        self.screen = screen
        self.done = False
        self.movdir = 0
        self.sprites = pygame.sprite.Group()
        self.cannonshots = pygame.sprite.Group()
        self.player = player(screen)
        self.bonus = Bonus()
        self.score = score
        self.keys = pygame.key.get_pressed()

        self.pirates = []
        self.canisters = []
        self.pirateExplImages = []
        self.playerExplImages = []
        self.playerpirateExplImages = []
        self.canisterImages = []
        self.ai = None
        self.wave = [TANK1,TANK2,TANK3,TANK4,TANK5,TANK6]
        self.waveindx = 0
        self.tank = 0
        self.gamefps = gameFPS(GREEN)

        for i in range(1,12):
            src = "./images/pirateExpl" + str(i) + ".png"
            image = pygame.image.load(src).convert_alpha()
            self.pirateExplImages.append(image)

        for i in range(1,17):
            src = "./images/playerExpl" + str(i) + ".png"
            image = pygame.image.load(src).convert_alpha()
            self.playerExplImages.append(image)

        for i in range(1,16):
            src = "./images/collisionExpl" + str(i) + ".png"
            image = pygame.image.load(src).convert_alpha()
            self.playerpirateExplImages.append(image)

        for i in range(1,3):
            src = "./images/canister" + str(i) + ".png"
            image = pygame.image.load(src).convert_alpha()
            self.canisterImages.append(image)

    def process_events(self):
        for e in pygame.event.get():
            if e.type == QUIT or self.keys[K_ESCAPE]:
                self.done = True
                pygame.quit()
                sys.exit()
            elif e.type == GAME_OVER:
                #self.sprites.add(self.score)
                self.player.kill()
                self.done = True
            elif e.type in (KEYUP, KEYDOWN):
                self.keys = pygame.key.get_pressed()
                if self.keys[K_F1]:
                    self.gamePause()
                if self.keys[K_F2]:
                    self.gamefps.toggleDisplay()
                if e.type == KEYDOWN:
                    if e.key in DIRECT_DICT:
                        self.movdir |= DIRECT_DICT[e.key]
                elif e.type == KEYUP:
                    if e.key in DIRECT_DICT:
                        self.movdir &= ~DIRECT_DICT[e.key]
            elif e.type == PLAYER_RESTART:
                pygame.time.set_timer(PLAYER_RESTART,0) # kill timer
                self.player.restart()
                self.sprites.add(self.player)

            elif e.type == TANK_EXIT:
                self.delpirate(e.tank)
                pass

            elif e.type == NEW_WAVE:
                pygame.time.set_timer(NEW_WAVE, 0)  # kill timer
                self.score.kill()
                self.newwave()

            elif e.type == BONUS_LEVEL:
                pygame.time.set_timer(BONUS_LEVEL, 0)   # kill timer
                self.bonus.kill()
                self.newwave()
                Bonus.nextlevel()

            elif e.type == ATTACK_PLAYER:
                #print("ATTACK PLAYER")
                self.ai.attackPlayer(e.tank)
                pass

            elif e.type == pygame.ACTIVEEVENT:
                if e.state == 6:
                    if e.gain == 0:
                        self.on_minimize()
                    else:
                        self.on_restore()
            else:
                #print("UNKNOWN EVENT")
                #print(e.type)
                #print(pygame.event.event_name(e.type))
                pass

    # window restore - resume game
    def on_restore(self):
        pass

    # window minimize - pause game
    def on_minimize(self):
        flg = True
        while flg == True:
            for e in pygame.event.get():
                if e.type == pygame.ACTIVEEVENT:
                    if e.state == 6:
                        if e.gain != 0:
                            flg = False
        pygame.event.clear((KEYUP, KEYDOWN))
        pygame.key.get_pressed()
        pygame.event.get()
        pass

    def gamePause(self):
        msg = "GAME PAUSE", "Press F1 To Continue"
        textPrint = TextPrint(self.screen)
        textPrint.setcolor(NEO)

        tmpsurface = self.screen.copy()

        toggle = 1
        pygame.time.set_timer(DUMMY_EVENT, 500)  # timer

        pause = True
        while pause:
            for e in pygame.event.get():
                keys = pygame.key.get_pressed()
                if e.type == QUIT or keys[K_ESCAPE]:
                    pygame.time.set_timer(DUMMY_EVENT, 0)  # kill timer
                    pygame.quit()
                    sys.exit()
                elif keys[K_F1]:
                    pygame.time.set_timer(DUMMY_EVENT, 0)  # kill timer
                    pause = False
                    break
                elif e.type == DUMMY_EVENT:
                    toggle = 1 - toggle

            self.screen.fill(BLACK)
            self.screen.blit(tmpsurface, [0, 0])

            if toggle:
                textPrint.setfontsize(64)
                textPrint.prntcenterx("GAME PAUSE", 240)
                textPrint.setfontsize(18)
                textPrint.prntcenterx("Press F1 To Continue", 290)
            pygame.display.flip()

        pygame.event.clear((KEYUP, KEYDOWN))
        pygame.key.get_pressed()
        pygame.event.get()

    def run(self):
        self.initCanisters()

        # keep track of time
        clock = pygame.time.Clock()
        timer = pygame.time.get_ticks()
        cooldown = 300

        self.waveindx = 0
        pygame.time.set_timer(NEW_WAVE, 1000)  # 1sec   random delay???

        self.sprites.add(self.player)
        pirate.clrGroup()

        self.sprites.add(self.gamefps)

        Bonus.points = 10
        self.done = False
        while not self.done:
            #gameFPS.clock = pygame.time.Clock().get_fps()
            now = pygame.time.get_ticks()
            self.process_events()
            if self.done:
                break

            if self.movdir & DIRECT_DICT[K_SPACE]:
                if now - timer > cooldown:  # fire cannon only if cooldown
                    if self.sprites.has(self.player):   # is player on-screen?
                        shot = cannonshot(self.player.angle, self.player.rect.centerx, self.player.rect.centery)
                        self.sprites.add(shot)
                        self.cannonshots.add(shot)
                        timer = now
                self.movdir &= ~DIRECT_DICT[K_SPACE]

            if self.movdir & DIRECT_DICT[K_LEFT]:
                self.player.rotate_counterclockwise()

            if self.movdir & DIRECT_DICT[K_RIGHT]:
                self.player.rotate_clockwise()

            if self.movdir & (DIRECT_DICT[K_UP]):
                self.player.mov()

            if self.ai != None:
                self.ai.action()

            for sprite in self.sprites:
                if type(sprite) == cannonshot:
                    sprite.mov()

            # check object collisions
            self.checkCollisions()

            # redraw sprites
            self.screen.fill(Color('black'))
            for sprite in self.sprites:
                sprite.draw(self.screen)

            # update sprites
            self.sprites.update()

            pygame.display.flip()
            clock.tick(FPS) # maintain frame rate
            gameFPS.clock = clock.get_fps()

    def delpirate(self, tank):
        if tank.target:
            canister = tank.target
            self.canisters.remove(canister)
            canister.kill()
        self.pirates.remove(tank)
        tank.kill()
        if len(self.canisters) == 0:
            event = pygame.event.Event(GAME_OVER)
            pygame.event.post(event)
        else:
            self.chknewwave()

    def chknewwave(self):
        if len(self.pirates) == 0:
            if self.waveindx < len(self.wave):
                self.sprites.add(self.score)
                pygame.time.set_timer(NEW_WAVE, 2000)  # 1sec   random delay???
            else:
                self.newlevel()
        pass

    def newwave(self):
        max = 3
        if Bonus.points > 10:
            max = 4
        self.tank = self.wave[self.waveindx]
        for num in range(1, max):
            tank = pirate(self.tank)
            self.pirates.append(tank)
            self.sprites.add(tank)
        self.ai = ai(self.player, self.pirates, self.canisters)
        self.waveindx += 1

    def newlevel(self):
        self.waveindx = 0
        self.sprites.add(self.bonus)
        pygame.time.set_timer(BONUS_LEVEL, 2000)  # 1sec   random delay???

    def checkCollisions(self):
        # check player cannon-fire collision with pirate(s)
        collidedict = pygame.sprite.groupcollide(self.cannonshots, pirate.getGroup(), False, False)
        if collidedict:
            for cannon in collidedict.keys():
                cannon.kill()
                for value in collidedict.values():
                    for tank in value:
                        if type(tank) is pirate:
                            def callback(sprite):
                                sprite.kill()
                                self.chknewwave()

                            expl = pirateExplode(tank.rect.centerx, tank.rect.centery, callback, self.pirateExplImages)
                            self.sprites.add(expl)
                            self.score.killpirate(self.tank)    # self.waveindx
                            if tank.target:
                                tank.target.tagged = False

                            # look at this!...why does remove fail?
                            indx = self.pirates.index(tank)
                            if (indx >= 0):
                                self.pirates.remove(tank)
                            else:
                                pass
                            tank.kill()

        # check player collision with pirates
        if self.sprites.has(self.player) == True:
            collide = pygame.sprite.spritecollideany(self.player, pirate.getGroup())
            if collide:
                if type(collide) is pirate:
                    def callbackpirate(sprite):
                        sprite.kill()
                        self.chknewwave()
                    def callbackplayer(sprite):
                        sprite.kill()
                        # delay 1.5-2 sec before player reset
                        pygame.time.set_timer(PLAYER_RESTART, random.randrange(1500,2000))

                    if collide.target:
                        collide.target.tagged = False
                    self.pirates.remove(collide)
                    self.player.kill()
                    collide.kill()
                    self.score.killpirate(self.tank)
                    expl = playerpirateCollision(False, collide.rect.centerx, collide.rect.centery, callbackpirate, self.playerpirateExplImages)
                    self.sprites.add(expl)
                    expl = playerpirateCollision(True, self.player.rect.centerx, self.player.rect.centery, callbackplayer, self.playerpirateExplImages)
                    self.sprites.add(expl)


    def initCanisters(self):
        centerx = int(SCREEN_WIDTH/2)
        centery = int(SCREEN_HEIGHT/2)
        for d,x,y in [("L",-20,0), ("R", 20, 0), ("L",-25,-25), ("R",25,-25), ("L",-25,25), ("R",25,25), ("L",0,-15), ("R",0,15)]:
            fuel = canister(d, centerx + x, centery + y, None, self.canisterImages)
            if d == "L":
                fuel.rotate(180)
            self.sprites.add(fuel)
            self.canisters.append(fuel)
from config import *
from player import *
from pirate import *
from canister import *
from utils import *
import pytweening

class ai():
    def __init__(self, player, pirates, canisters):
        self.player = player
        self.pirates = pirates
        self.canisters = canisters

        for pirate in self.pirates:
            pirate.ai = AIState()
            canister = self.__findCanister(pirate, canisters)
            if canister:
                self.__setCourse(pirate, canister)
                pirate.target = canister
                pirate.ai.new_state(State_GOGETIT)
                self.__setCourse(pirate, pirate.target)
            else:
                self.attackPlayer(pirate)

    def action(self):
        for pirate in self.pirates:
            pirate.ai.action(pirate)
            pass

    def attackPlayer(self, pirate):
        pirate.target = self.player
        self.__setCourse(pirate, self.player)
        pirate.ai.new_state(State_Attack)

    def __mov(self, pirate):
        if pirate.target:
            #if pygame.sprite.collide_circle(pirate.target, pirate):
            grp = pygame.sprite.GroupSingle(pirate.target)
            if pygame.sprite.spritecollide(pirate, grp, False, pygame.sprite.collide_circle_ratio(0.75)):
                print("GOT IT")
            else:
                pirate.mov()

                if pirate.x > SCREEN_WIDTH:
                    self.__setCourse(pirate, pirate.target.x, pirate.target.y)
                elif pirate.x < 0:
                    self.__setCourse(pirate, pirate.target.x, pirate.target.y)
                elif pirate.y > SCREEN_HEIGHT:
                    self.__setCourse(pirate, pirate.target.x, pirate.target.y)
                elif pirate.y < 0:
                    self.__setCourse(pirate, pirate.target.x, pirate.target.y)


    def __findCanister(self, pirate, canisters):
        target = None
        prev_distance = 1000
        for canister in canisters:
            if canister.tagged == False:
                distance = getDistance(canister.rect.centerx, canister.rect.centery, pirate.rect.centerx, pirate.rect.centery)
                if distance < prev_distance:
                    prev_distance = distance
                    target = canister
        if target:
            target.tagged = True
        return target

    def __setCourse(self, pirate, target):
        angle = getAngle(pirate.rect.centerx, pirate.rect.centery, target.rect.centerx, target.rect.centery)
        rotatedSurf = pygame.transform.rotate(pirate.rotatedimages[0], angle)
        pirate.image = rotatedSurf

        dx, dy = getSlope(angle)
        if 0 <= angle <= 89:
            dx, dy = abs(dx), -abs(dy)
        elif 90 <= angle <= 179:
            dx, dy = -abs(dx), -abs(dy)
        elif 180 <= angle <= 269:
            dx, dy = -abs(dx), abs(dy)
        else:
            dx, dy = abs(dx), abs(dy)

        pirate.dx = dx
        pirate.dy = dy

        pirate.spline.ControlPoints.append((pirate.rect.centerx, pirate.rect.centery))

        x = int(random.random() * 640)
        y = 0
        if random.randrange(0, 2) == 0:
            y = -10
        else:
            y = 490

        pirate.spline.ControlPoints.append((x, y))

        z = 0
        if random.randrange(0,2) == 0:
            z = 1
        else:
            z = -1

        if y < 0:
            x = 320 + (int(random.random() * 100)  * z)
            y = 240 - int(random.random() * 100)
        else:
            x = 320 + (int(random.random() * 100)  * z)
            y = 240 + (int(random.random() * 100))
        pirate.spline.ControlPoints.append((x,y))

        pirate.spline.ControlPoints.append((target.rect.centerx, target.rect.centery))

        finalpoints = pirate.spline.wayPoints()

        for n in range(len(finalpoints)-1):
            x1, y1 = finalpoints[n][0], finalpoints[n][1]
            x2, y2 = finalpoints[n+1][0], finalpoints[n+1][1]
            angle = getAngle(x1,y1,x2,y2)
            self.__tween(pirate,x1,y1,x2,y2, angle)

    def __tween(self, pirate, x1, y1, x2, y2, angle):
        points = pytweening.getLine(x1,y1,x2,y2)
        for point in points:
            pirate.coors.append((angle,point[0],point[1]))
        del pirate.coors[-1]


class AIState:
    def __init__(self):
        pass

    def new_state(self,state):
        self.__class__ = state

    def action(self, x):
        raise NotImplementedError()

class State_GOGETIT(AIState):
    def action(self, pirate):
        if pirate.target:
            # if pygame.sprite.collide_circle(pirate.target, pirate):
            grp = pygame.sprite.GroupSingle(pirate.target)
            if pygame.sprite.spritecollide(pirate, grp, False, pygame.sprite.collide_circle_ratio(0.9)):
                self.new_state(State_HOOKIT)
                pirate.exitangle = pirate.angle + 180
                pirate.exitangle %= 360
            else:
                pirate.mov()
                pirate.mov()
                pirate.mov()

class State_HOOKIT(AIState):
    def action(self, pirate):
        if pirate.hook_it() == True:
            self.new_state(State_RUNFORIT)

class State_RUNFORIT(AIState):
    def action(self, pirate):
        #self.new_state(State_GOGETIT)
        pirate.mov()
        pirate.mov()
        pirate.mov()
        if 0 < pirate.x > SCREEN_WIDTH:
            event = pygame.event.Event(TANK_EXIT, tank=pirate)
            pygame.event.post(event)
            self.new_state(State_TANKEXIT)
        elif 0 < pirate.y > SCREEN_HEIGHT:
            event = pygame.event.Event(TANK_EXIT, tank=pirate)
            pygame.event.post(event)

class State_TANKEXIT(AIState):
    def action(self,pirate):
        pass

class State_Attack(AIState):
    def action(self,pirate):
        flg1 = pirate.mov()
        flg2 = pirate.mov()
        flg3 = pirate.mov()
        if (flg1 == False) or (flg2 == False) or (flg3 == False):
            event = pygame.event.Event(ATTACK_PLAYER, tank=pirate)
            pygame.event.post(event)

import math

from .. import constants
from ..constants import tileSize
from .entity import Actor
from . import physics
from .stateMachine import State, StateMachine
from .projectile import Projectile


class Enemy(Actor):
    stompable = True
    slashable = False
    hasGravity = True
    contactDamage = constants.contactDamage
    kind = "enemy"

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.hp = 1
        self.direction = -1
        self.machine = StateMachine(self)
        self.spawnX = float(x)
        self.spawnY = float(y)

    def initialState(self):
        return None

    def stepGround(self, world, speed):
        self.vx = speed * self.direction
        self.vy += constants.gravity
        if self.vy > constants.maxFallSpeed:
            self.vy = constants.maxFallSpeed
        physics.moveHorizontal(self, world.level, world.colliders)
        if (self.direction > 0 and self.onWallRight) or (self.direction < 0 and self.onWallLeft):
            self.direction *= -1
            self.vx = 0.0
        wasOnGround = self.onGround
        physics.moveVertical(self, world.level, world.colliders)
        physics.resolveSlope(self, world.level, wasOnGround)
        self.facing = self.direction
        if self.onGround:
            aheadX = self.x + (self.w + 1 if self.direction > 0 else -1)
            col = int(aheadX // tileSize)
            row = int((self.y + self.h + 2) // tileSize)
            if not world.level.solidAt(col, row) and not world.level.oneWayAt(col, row) and not world.level.slopeAt(col, row):
                self.direction *= -1

    def playerDistance(self, world):
        return abs(world.player.centerX - self.centerX)

    def playerVerticalDistance(self, world):
        return abs(world.player.centerY - self.centerY)

    def facePlayer(self, world):
        self.direction = 1 if world.player.centerX >= self.centerX else -1

    def update(self, world):
        if self.machine.current is None:
            self.machine.setInitial(self.initialState(), world)
        self.machine.update(world)

    def onStomped(self, world):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
        world.spawnBurst("stomp", self.centerX, self.centerY, 6)

    def onSlashed(self, world):
        self.hp = 0
        self.alive = False
        world.spawnBurst("stomp", self.centerX, self.centerY, 8)


class PatrolState(State):
    name = "patrol"

    def update(self, owner, world):
        owner.stepGround(world, constants.enemySpeed)
        return None


class Beetle(Enemy):
    kind = "beetle"
    slashable = True

    def initialState(self):
        return "patrol"

    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.machine.addState(PatrolState())


class ChaserPatrol(State):
    name = "patrol"
    detectRange = 90.0
    detectHeight = 40.0

    def update(self, owner, world):
        owner.stepGround(world, constants.enemySpeed)
        if owner.playerDistance(world) < self.detectRange and owner.playerVerticalDistance(world) < self.detectHeight:
            return "chase"
        return None


class ChaseState(State):
    name = "chase"
    loseRange = 160.0

    def onEnter(self, owner, world):
        world.spawnBurst("alert", owner.centerX, owner.top - 4, 3)

    def update(self, owner, world):
        owner.facePlayer(world)
        owner.stepGround(world, constants.chaserSpeed)
        if owner.playerDistance(world) > self.loseRange:
            return "patrol"
        return None


class Chaser(Enemy):
    kind = "chaser"
    slashable = True

    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.hp = 2
        self.machine.addState(ChaserPatrol()).addState(ChaseState())

    def initialState(self):
        return "patrol"


class FlyerHover(State):
    name = "hover"
    detectRange = 120.0

    def update(self, owner, world):
        owner.hoverPhase += 0.08
        owner.x += owner.direction * constants.flyerSpeed
        owner.y = owner.baseY + math.sin(owner.hoverPhase) * 14.0
        box = owner.aabb
        blockedRight = owner.direction > 0 and physics.touchingSolidSide(owner, world.level, world.colliders, 1)
        blockedLeft = owner.direction < 0 and physics.touchingSolidSide(owner, world.level, world.colliders, -1)
        if blockedRight or blockedLeft or owner.x < owner.patrolMin or owner.x > owner.patrolMax:
            owner.direction *= -1
            owner.x = min(max(owner.x, owner.patrolMin), owner.patrolMax)
        owner.facing = owner.direction
        if owner.playerDistance(world) < self.detectRange:
            return "pursue"
        return None


class FlyerPursue(State):
    name = "pursue"
    loseRange = 190.0

    def update(self, owner, world):
        target = world.player
        dx = target.centerX - owner.centerX
        dy = target.centerY - owner.centerY
        distance = math.hypot(dx, dy) or 1.0
        owner.x += (dx / distance) * constants.flyerSpeed * 1.4
        owner.y += (dy / distance) * constants.flyerSpeed * 1.4
        owner.baseY = owner.y
        owner.facing = 1 if dx >= 0 else -1
        owner.direction = owner.facing
        if owner.playerDistance(world) > self.loseRange:
            return "hover"
        return None


class Flyer(Enemy):
    kind = "flyer"
    hasGravity = False
    stompable = True

    def __init__(self, x, y):
        super().__init__(x, y, 16, 14)
        self.baseY = float(y)
        self.hoverPhase = 0.0
        self.patrolMin = float(x) - 48.0
        self.patrolMax = float(x) + 48.0
        self.machine.addState(FlyerHover()).addState(FlyerPursue())

    def initialState(self):
        return "hover"


class ShooterIdle(State):
    name = "idle"
    detectRange = 150.0

    def update(self, owner, world):
        if owner.cooldown > 0:
            owner.cooldown -= 1
        if owner.playerDistance(world) < self.detectRange and owner.cooldown == 0:
            owner.facePlayer(world)
            return "aim"
        return None


class ShooterAim(State):
    name = "aim"
    windup = 18

    def update(self, owner, world):
        owner.facePlayer(world)
        if self.timeGuard(owner):
            return "fire"
        return None

    def timeGuard(self, owner):
        return owner.machine.timeInState >= self.windup


class ShooterFire(State):
    name = "fire"

    def onEnter(self, owner, world):
        target = world.player
        dx = target.centerX - owner.centerX
        dy = target.centerY - owner.centerY
        distance = math.hypot(dx, dy) or 1.0
        speed = constants.projectileSpeed
        projectile = Projectile(
            owner.centerX - 3,
            owner.centerY - 3,
            (dx / distance) * speed,
            (dy / distance) * speed,
            owner="enemy",
            damage=1,
        )
        world.spawnProjectile(projectile)
        world.playSound("shoot", owner.centerX)
        owner.cooldown = constants.shooterCooldown

    def update(self, owner, world):
        return "idle"


class Shooter(Enemy):
    kind = "shooter"
    hasGravity = True
    stompable = True

    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.hp = 2
        self.cooldown = 0
        self.machine.addState(ShooterIdle()).addState(ShooterAim()).addState(ShooterFire())

    def initialState(self):
        return "idle"

    def update(self, world):
        if self.hasGravity:
            self.vx = 0.0
            self.vy += constants.gravity
            if self.vy > constants.maxFallSpeed:
                self.vy = constants.maxFallSpeed
            physics.moveVertical(self, world.level, world.colliders)
        super().update(world)


enemyFactory = {
    "beetle": Beetle,
    "chaser": Chaser,
    "flyer": Flyer,
    "shooter": Shooter,
}


def spawnEnemy(spawn):
    factory = enemyFactory.get(spawn.kind, Beetle)
    return factory(spawn.x, spawn.y)

from .. import constants
from .entity import Actor
from .geometry import Aabb, sign
from . import physics
from .inventory import Inventory


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, 12, 16)
        self.maxHp = constants.playerMaxHp
        self.hp = self.maxHp
        self.iframes = 0
        self.coyoteTimer = 0
        self.jumpBufferTimer = 0
        self.airJumps = constants.maxAirJumps
        self.dashTimer = 0
        self.dashCooldown = 0
        self.wallStickTimer = 0
        self.wallSliding = False
        self.onLadder = False
        self.jumpHeldPrev = False
        self.attackTimer = 0
        self.attackCooldown = 0
        self.inventory = Inventory()
        self.score = 0
        self.berries = 0
        self.spawnX = float(x)
        self.spawnY = float(y)

    def hurtBox(self):
        return self.aabb.inflated(-1.0, 0.0)

    def isInvulnerable(self):
        return self.iframes > 0 or self.dashTimer > 0

    def isAttacking(self):
        return self.attackTimer > 0

    def attackBox(self):
        top = self.centerY - constants.attackHeight * 0.5
        if self.facing > 0:
            return Aabb(self.right, top, constants.attackReach, constants.attackHeight)
        return Aabb(self.left - constants.attackReach, top, constants.attackReach, constants.attackHeight)

    def handleAttack(self, world, command):
        if self.attackTimer > 0:
            self.attackTimer -= 1
        if self.attackCooldown > 0:
            self.attackCooldown -= 1
        if command.attack and self.attackCooldown == 0:
            self.attackTimer = constants.attackFrames
            self.attackCooldown = constants.attackCooldownFrames
            world.playSound("slash", self.centerX)

    def setCheckpoint(self, x, y):
        self.spawnX = float(x)
        self.spawnY = float(y)

    def respawn(self):
        self.x = self.spawnX
        self.y = self.spawnY
        self.vx = 0.0
        self.vy = 0.0
        self.iframes = constants.iframesOnHit
        self.dashTimer = 0
        self.attackTimer = 0
        self.alive = True

    def takeDamage(self, amount, sourceX, world):
        if self.isInvulnerable() or not self.alive:
            return False
        self.hp -= amount
        self.iframes = constants.iframesOnHit
        away = sign(self.centerX - sourceX) or self.facing
        self.vx = constants.knockbackX * away
        self.vy = constants.knockbackY
        self.dashTimer = 0
        world.playSound("hurt", self.centerX)
        world.spawnBurst("hurt", self.centerX, self.centerY, 8)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            world.playSound("die", self.centerX)
        return True

    def heal(self, amount):
        self.hp = min(self.maxHp, self.hp + amount)

    def update(self, world, command):
        if not self.alive:
            return
        if self.iframes > 0:
            self.iframes -= 1
        if self.dashCooldown > 0:
            self.dashCooldown -= 1
        self.handleAttack(world, command)

        terrain = world.level
        platforms = world.colliders

        self.updateLadder(world, command, terrain)
        if self.onLadder:
            self.moveOnLadder(world, command, terrain, platforms)
            return

        self.applyHorizontal(command)
        self.updateTimers(command, terrain, platforms)
        self.handleDash(world, command)
        if self.dashTimer > 0:
            self.runDash(world, terrain, platforms)
            return
        self.handleJump(world, command, platforms)
        self.applyGravity(command)
        self.applyWallSlide(command, terrain, platforms)

        physics.moveHorizontal(self, terrain, platforms)
        wasOnGround = self.onGround
        physics.moveVertical(self, terrain, platforms, dropThrough=self.wantsDropThrough(command))
        physics.resolveSlope(self, terrain, wasOnGround)

        if self.onGround:
            self.airJumps = constants.maxAirJumps
            self.coyoteTimer = constants.coyoteFrames
        self.jumpHeldPrev = command.jumpHeld

    def wantsDropThrough(self, command):
        return command.down and command.jump

    def applyHorizontal(self, command):
        axis = command.moveAxis
        topSpeed = constants.runSpeed if command.run else constants.moveSpeed
        accel = constants.moveAccel if self.onGround else constants.airAccel
        if axis != 0:
            self.vx += accel * axis
            self.facing = axis
            if self.vx > topSpeed:
                self.vx = topSpeed
            if self.vx < -topSpeed:
                self.vx = -topSpeed
        else:
            damping = constants.friction if self.onGround else constants.airFriction
            self.vx *= damping
            if abs(self.vx) < 0.1:
                self.vx = 0.0

    def updateTimers(self, command, terrain, platforms):
        if self.coyoteTimer > 0:
            self.coyoteTimer -= 1
        if self.jumpBufferTimer > 0:
            self.jumpBufferTimer -= 1
        if command.jump and not command.down:
            self.jumpBufferTimer = constants.jumpBufferFrames
        if self.wallStickTimer > 0:
            self.wallStickTimer -= 1

    def handleDash(self, world, command):
        if command.dash and self.dashCooldown == 0 and self.dashTimer == 0:
            direction = command.moveAxis or self.facing
            self.facing = direction
            self.dashTimer = constants.dashFrames
            self.dashCooldown = constants.dashCooldownFrames
            self.vx = constants.dashSpeed * direction
            self.vy = 0.0
            world.playSound("dash", self.centerX)
            world.spawnBurst("dash", self.centerX, self.centerY, 6)

    def runDash(self, world, terrain, platforms):
        self.dashTimer -= 1
        self.vy = 0.0
        physics.moveHorizontal(self, terrain, platforms)
        wasOnGround = self.onGround
        physics.moveVertical(self, terrain, platforms)
        physics.resolveSlope(self, terrain, wasOnGround)
        if self.onGround:
            self.airJumps = constants.maxAirJumps
            self.coyoteTimer = constants.coyoteFrames

    def handleJump(self, world, command, platforms):
        if command.down:
            return
        touchLeft = physics.touchingSolidSide(self, world.level, platforms, -1)
        touchRight = physics.touchingSolidSide(self, world.level, platforms, 1)
        onWall = (touchLeft or touchRight) and not self.onGround

        if self.jumpBufferTimer > 0:
            if self.onGround or self.coyoteTimer > 0:
                self.vy = constants.jumpVelocity
                self.jumpBufferTimer = 0
                self.coyoteTimer = 0
                world.playSound("jump", self.centerX)
                world.spawnBurst("jump", self.centerX, self.bottom, 4)
            elif onWall:
                awayDir = 1 if touchLeft else -1
                self.vx = constants.wallJumpVelocityX * awayDir
                self.vy = constants.wallJumpVelocityY
                self.facing = awayDir
                self.jumpBufferTimer = 0
                self.wallStickTimer = 0
                world.playSound("jump", self.centerX)
            elif self.airJumps > 0:
                self.vy = constants.doubleJumpVelocity
                self.airJumps -= 1
                self.jumpBufferTimer = 0
                world.playSound("doubleJump", self.centerX)
                world.spawnBurst("jump", self.centerX, self.centerY, 6)

        if self.jumpHeldPrev and not command.jumpHeld and self.vy < 0:
            self.vy *= constants.jumpCutMultiplier

    def applyGravity(self, command):
        pull = constants.gravity
        cap = constants.fastFallSpeed if command.down and not self.onGround else constants.maxFallSpeed
        self.vy += pull
        if self.vy > cap:
            self.vy = cap

    def applyWallSlide(self, command, terrain, platforms):
        self.wallSliding = False
        if self.onGround or self.vy <= 0:
            return
        touchLeft = physics.touchingSolidSide(self, terrain, platforms, -1)
        touchRight = physics.touchingSolidSide(self, terrain, platforms, 1)
        pressingIntoWall = (command.left and touchLeft) or (command.right and touchRight)
        if pressingIntoWall:
            self.wallSliding = True
            self.wallStickTimer = constants.wallStickFrames
            if self.vy > constants.wallSlideSpeed:
                self.vy = constants.wallSlideSpeed

    def updateLadder(self, world, command, terrain):
        onLadderTile = physics.overlapsLadder(self, terrain)
        if not onLadderTile:
            self.onLadder = False
            return
        if command.up or command.down:
            self.onLadder = True
        if self.onLadder and self.onGround and command.down and not onLadderTile:
            self.onLadder = False

    def moveOnLadder(self, world, command, terrain, platforms):
        climbSpeed = 1.4
        self.vy = command.verticalAxis * climbSpeed
        self.vx = command.moveAxis * (constants.moveSpeed * 0.6)
        if command.jump:
            self.onLadder = False
            self.vy = constants.jumpVelocity * 0.7
            return
        physics.moveHorizontal(self, terrain, platforms)
        physics.moveVertical(self, terrain, platforms)
        if self.onGround and command.verticalAxis >= 0:
            self.onLadder = False
        if not physics.overlapsLadder(self, terrain):
            self.onLadder = False

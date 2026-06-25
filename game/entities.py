import pygame

from .constants import (
    tileSize,
    gravity,
    maxFallSpeed,
    moveAccel,
    moveSpeed,
    friction,
    jumpVelocity,
    enemySpeed,
)


class Entity:
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.width = width
        self.height = height
        self.onGround = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def moveAndCollideX(self, world):
        self.x += self.vx
        box = self.rect()
        for tile in world.solidCellsOverlapping(box):
            if box.colliderect(tile):
                if self.vx > 0:
                    self.x = tile.left - self.width
                elif self.vx < 0:
                    self.x = tile.right
                self.vx = 0.0
                box = self.rect()

    def moveAndCollideY(self, world):
        self.y += self.vy
        self.onGround = False
        box = self.rect()
        for tile in world.solidCellsOverlapping(box):
            if box.colliderect(tile):
                if self.vy > 0:
                    self.y = tile.top - self.height
                    self.onGround = True
                elif self.vy < 0:
                    self.y = tile.bottom
                self.vy = 0.0
                box = self.rect()

        if not self.onGround and self.vy >= 0:
            footSensor = pygame.Rect(int(self.x), int(self.y) + self.height, self.width, 1)
            for tile in world.solidCellsOverlapping(footSensor):
                if footSensor.colliderect(tile):
                    self.y = tile.top - self.height
                    self.vy = 0.0
                    self.onGround = True
                    break


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 12, 16)
        self.facing = 1
        self.alive = True

    def update(self, world, moveInput):
        if moveInput.left:
            self.vx -= moveAccel
            self.facing = -1
        if moveInput.right:
            self.vx += moveAccel
            self.facing = 1
        if not moveInput.left and not moveInput.right:
            self.vx *= friction
            if abs(self.vx) < 0.1:
                self.vx = 0.0
        if self.vx > moveSpeed:
            self.vx = moveSpeed
        if self.vx < -moveSpeed:
            self.vx = -moveSpeed

        if moveInput.jump and self.onGround:
            self.vy = jumpVelocity

        self.vy += gravity
        if self.vy > maxFallSpeed:
            self.vy = maxFallSpeed

        self.moveAndCollideX(world)
        self.moveAndCollideY(world)


class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.direction = -1
        self.alive = True

    def update(self, world):
        self.vx = enemySpeed * self.direction
        self.moveAndCollideX(world)
        if self.vx == 0.0:
            self.direction *= -1

        self.vy += gravity
        if self.vy > maxFallSpeed:
            self.vy = maxFallSpeed
        self.moveAndCollideY(world)

        if self.onGround:
            aheadX = self.x + (self.width if self.direction > 0 else -1)
            aheadCol = int(aheadX) // tileSize
            belowRow = int(self.y + self.height + 1) // tileSize
            if not world.solidAt(aheadCol, belowRow):
                self.direction *= -1


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def rect(self):
        return pygame.Rect(self.x, self.y, tileSize, tileSize)

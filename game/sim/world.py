import random

from .. import constants
from ..constants import tileSize
from .level import loadLevel
from .player import Player
from .enemies import spawnEnemy
from .items import Collectible
from .movingPlatform import MovingPlatform
from .particles import ParticleSystem
from .audio import AudioBus
from .camera import Camera
from . import physics


class World:
    def __init__(self, levelSource, rng=None):
        self.level = loadLevel(levelSource)
        self.rng = rng if rng is not None else random.Random(9001)
        self.player = Player(*self.level.playerSpawn)
        self.enemies = [spawnEnemy(spawn) for spawn in self.level.enemies]
        self.items = [Collectible.fromSpawn(spawn) for spawn in self.level.items]
        self.platforms = [MovingPlatform.fromSpawn(spawn) for spawn in self.level.platforms]
        self.projectiles = []
        self.particles = ParticleSystem(rng=self.rng)
        self.audio = AudioBus()
        self.camera = Camera(
            constants.viewWidth,
            constants.viewHeight,
            self.level.pixelWidth(),
            self.level.pixelHeight(),
        )
        self.camera.focusOn(self.player.centerX, self.player.centerY)
        self.score = 0
        self.coins = 0
        self.lives = constants.startingLives
        self.frame = 0
        self.gameOver = False
        self.completed = False
        self.active = True
        self.activatedCheckpoints = set()

    def playSound(self, name, x=None):
        self.audio.play(name, x)

    def spawnBurst(self, preset, x, y, count=None):
        self.particles.emit(preset, x, y, count)

    def spawnProjectile(self, projectile):
        self.projectiles.append(projectile)

    def step(self, command):
        if not self.active:
            return
        self.frame += 1
        self.audio.tick()

        for platform in self.platforms:
            platform.update()
        self.carryRider(self.player)

        self.player.update(self, command)

        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self)

        for projectile in self.projectiles:
            if projectile.alive:
                projectile.update(self)

        self.resolveEnemyCollisions()
        self.resolveProjectileCollisions()
        self.resolveItemCollisions()
        self.resolveHazards()
        self.resolveCheckpoints()
        self.resolveExit()

        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        self.projectiles = [proj for proj in self.projectiles if proj.alive]

        for item in self.items:
            item.update()
        self.particles.update()

        self.handlePlayerDeath()
        self.camera.update(self.player.centerX, self.player.centerY)

    def carryRider(self, rider):
        platform = rider.groundPlatform
        if platform is not None and platform in self.platforms:
            rider.x += platform.deltaX
            rider.y += platform.deltaY

    def resolveEnemyCollisions(self):
        if not self.player.alive:
            return
        playerBox = self.player.hurtBox()
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            if not playerBox.intersects(enemy.hurtBox()):
                continue
            fallingOnto = (
                enemy.stompable
                and self.player.vy > 0.0
                and (self.player.bottom - enemy.top) < enemy.h * 0.7
                and self.player.centerY < enemy.centerY
            )
            if fallingOnto:
                enemy.onStomped(self)
                self.player.vy = constants.stompBounce
                self.player.airJumps = constants.maxAirJumps
                self.player.score += 100
                self.score += 100
                self.playSound("stomp", enemy.centerX)
                self.camera.addShake(6, 1.5)
            elif not self.player.isInvulnerable():
                self.player.takeDamage(enemy.contactDamage, enemy.centerX, self)
                self.camera.addShake(10, 2.5)

    def resolveProjectileCollisions(self):
        if not self.player.alive:
            return
        playerBox = self.player.hurtBox()
        for projectile in self.projectiles:
            if not projectile.alive or projectile.owner != "enemy":
                continue
            if playerBox.intersects(projectile.aabb):
                projectile.alive = False
                if not self.player.isInvulnerable():
                    self.player.takeDamage(projectile.damage, projectile.centerX, self)
                    self.camera.addShake(8, 2.0)

    def resolveItemCollisions(self):
        if not self.player.alive:
            return
        playerBox = self.player.aabb
        for item in self.items:
            if item.collected:
                continue
            if playerBox.intersects(item.aabb):
                item.collect(self.player, self)

    def resolveHazards(self):
        if not self.player.alive:
            return
        damage = physics.hazardOverlap(self.player, self.level)
        if damage > 0 and not self.player.isInvulnerable():
            self.player.takeDamage(damage, self.player.centerX, self)
            self.camera.addShake(10, 2.5)

    def resolveCheckpoints(self):
        for index, point in enumerate(self.level.checkpoints):
            if index in self.activatedCheckpoints:
                continue
            checkpointBox = self.level.rectFor(int(point[0] // tileSize), int(point[1] // tileSize))
            if self.player.aabb.intersects(checkpointBox):
                self.activatedCheckpoints.add(index)
                self.player.setCheckpoint(point[0], point[1])
                self.playSound("checkpoint", point[0])
                self.spawnBurst("pickup", point[0] + tileSize * 0.5, point[1], 6)

    def resolveExit(self):
        if self.level.exit is None or self.completed:
            return
        exitCol = int(self.level.exit[0] // tileSize)
        exitRow = int(self.level.exit[1] // tileSize)
        exitBox = self.level.rectFor(exitCol, exitRow)
        if self.player.alive and self.player.aabb.intersects(exitBox):
            self.completed = True
            self.playSound("levelComplete", self.level.exit[0])

    def handlePlayerDeath(self):
        fellOut = self.player.top > self.level.pixelHeight() + tileSize * 2
        if fellOut and self.player.alive:
            self.player.alive = False
            self.playSound("die", self.player.centerX)
        if self.player.alive:
            return
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.gameOver = True
            self.active = False
            return
        self.player.hp = self.player.maxHp
        self.player.respawn()
        self.projectiles = []
        self.camera.focusOn(self.player.centerX, self.player.centerY)

import pygame

from ..constants import tileSize
from ..sim.tiles import AIR
from .theme import (
    bufferWidth,
    bufferHeight,
    renderScale,
    skyTop,
    skyBottom,
    hillFar,
    hillNear,
    cloudColor,
)
from .art import buildSprites
from .hud import Hud


class Renderer:
    def __init__(self, sprites=None):
        self.sprites = sprites if sprites is not None else buildSprites()
        self.hud = Hud()
        self.buffer = pygame.Surface((bufferWidth, bufferHeight))
        self.sky = self.buildSky()

    def buildSky(self):
        surf = pygame.Surface((bufferWidth, bufferHeight))
        for y in range(bufferHeight):
            blend = y / bufferHeight
            color = (
                int(skyTop[0] + (skyBottom[0] - skyTop[0]) * blend),
                int(skyTop[1] + (skyBottom[1] - skyTop[1]) * blend),
                int(skyTop[2] + (skyBottom[2] - skyTop[2]) * blend),
            )
            pygame.draw.line(surf, color, (0, y), (bufferWidth, y))
        return surf

    def drawParallax(self, offsetX):
        self.buffer.blit(self.sky, (0, 0))
        for hillX in (40, 220, 430, 620, 820):
            screenX = hillX - offsetX // 2 % 900
            pygame.draw.ellipse(self.buffer, hillFar, (screenX, bufferHeight - 52, 140, 80))
            pygame.draw.ellipse(self.buffer, hillNear, (screenX + 22, bufferHeight - 44, 96, 64))
        for cloudX in (90, 260, 470, 640, 820):
            screenX = cloudX - offsetX // 3 % 900
            pygame.draw.ellipse(self.buffer, cloudColor, (screenX, 26, 46, 20))
            pygame.draw.ellipse(self.buffer, cloudColor, (screenX + 18, 18, 40, 24))

    def drawTiles(self, world, offsetX, offsetY):
        level = world.level
        firstCol = max(0, offsetX // tileSize)
        lastCol = min(level.cols, (offsetX + bufferWidth) // tileSize + 1)
        firstRow = max(0, offsetY // tileSize)
        lastRow = min(level.rows, (offsetY + bufferHeight) // tileSize + 1)
        for row in range(firstRow, lastRow):
            for col in range(firstCol, lastCol):
                name = level.collision[row][col]
                if name == AIR:
                    continue
                sprite = self.sprites.get(name)
                if sprite is None:
                    continue
                self.buffer.blit(sprite, (col * tileSize - offsetX, row * tileSize - offsetY))

    def drawItems(self, world, offsetX, offsetY):
        for item in world.items:
            if item.collected:
                continue
            sprite = self.sprites.get(item.kind)
            if sprite is None:
                continue
            bob = -2 if (item.bob and int(item.bobPhase * 2) % 2 == 0) else 0
            self.buffer.blit(sprite, (int(item.x) - offsetX, int(item.y) - offsetY + bob))

    def drawEnemies(self, world, offsetX, offsetY):
        for enemy in world.enemies:
            if not enemy.alive:
                continue
            sprite = self.sprites.get(enemy.kind, self.sprites["goomba"])
            if enemy.facing > 0:
                sprite = pygame.transform.flip(sprite, True, False)
            self.buffer.blit(sprite, (int(enemy.x) - offsetX, int(enemy.y) - offsetY))

    def drawProjectiles(self, world, offsetX, offsetY):
        for projectile in world.projectiles:
            if not projectile.alive:
                continue
            x = int(projectile.centerX) - offsetX
            y = int(projectile.centerY) - offsetY
            pygame.draw.circle(self.buffer, (255, 160, 60), (x, y), 3)
            pygame.draw.circle(self.buffer, (255, 240, 180), (x, y), 1)

    def drawParticles(self, world, offsetX, offsetY):
        for particle in world.particles.particles:
            x = int(particle.x) - offsetX
            y = int(particle.y) - offsetY
            self.buffer.fill(particle.color, (x, y, particle.size, particle.size))

    def drawPlayer(self, world, offsetX, offsetY):
        player = world.player
        if not player.alive:
            return
        if player.iframes > 0 and player.iframes % 6 < 3:
            return
        sprite = self.sprites["player"]
        if player.facing < 0:
            sprite = pygame.transform.flip(sprite, True, False)
        self.buffer.blit(sprite, (int(player.x) - 2 - offsetX, int(player.y) - offsetY))

    def renderWorld(self, world):
        offsetX, offsetY = world.camera.offset()
        self.drawParallax(offsetX)
        self.drawTiles(world, offsetX, offsetY)
        self.drawItems(world, offsetX, offsetY)
        self.drawProjectiles(world, offsetX, offsetY)
        self.drawEnemies(world, offsetX, offsetY)
        self.drawParticles(world, offsetX, offsetY)
        self.drawPlayer(world, offsetX, offsetY)
        return self.buffer

    def present(self, world, mode=None):
        self.renderWorld(world)
        scaled = pygame.transform.scale(
            self.buffer, (bufferWidth * renderScale, bufferHeight * renderScale)
        )
        self.hud.draw(scaled, world)
        if mode in ("menu", "paused", "gameover", "complete", "victory"):
            self.hud.drawOverlay(scaled, mode)
        return scaled

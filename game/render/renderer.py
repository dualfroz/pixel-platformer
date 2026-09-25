import math

import pygame

from ..constants import tileSize, attackFrames, attackReach
from ..sim.tiles import AIR, isSolidName
from . import theme
from .theme import bufferWidth, bufferHeight, renderScale
from .art import buildSprites
from .propArt import doorSurface, floatingSlabSurface, exitFrameCount
from .backdrop import Backdrop
from .hud import Hud


class Renderer:
    def __init__(self, sprites=None):
        self.sprites = sprites if sprites is not None else buildSprites()
        self.hud = Hud()
        self.buffer = pygame.Surface((bufferWidth, bufferHeight))
        self.backdrop = Backdrop(bufferWidth, bufferHeight)
        self.slabCache = {}
        self.doorCache = {}

    def slabSprite(self, platform):
        size = (int(platform.w), int(platform.h))
        if size not in self.slabCache:
            self.slabCache[size] = floatingSlabSurface(*size)
        return self.slabCache[size]

    def doorSprite(self, door):
        key = (int(door.w), int(door.h), door.open)
        if key not in self.doorCache:
            self.doorCache[key] = doorSurface(*key)
        return self.doorCache[key]

    def tileSprite(self, level, col, row, name):
        if name == "ground" and not isSolidName(level.tileNameAt(col, row - 1)):
            return self.sprites["groundTop"]
        return self.sprites.get(name)

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
                sprite = self.tileSprite(level, col, row, name)
                if sprite is None:
                    continue
                self.buffer.blit(sprite, (col * tileSize - offsetX, row * tileSize - offsetY))

    def drawGlow(self, name, centerX, centerY, pulse=1.0):
        glow = self.sprites[name]
        if pulse != 1.0:
            size = max(2, int(glow.get_width() * pulse))
            glow = pygame.transform.smoothscale(glow, (size, size))
        self.buffer.blit(glow, (int(centerX - glow.get_width() / 2), int(centerY - glow.get_height() / 2)))

    def drawExit(self, world, offsetX, offsetY):
        if world.level.exit is None:
            return
        exitX = int(world.level.exit[0]) - offsetX
        exitY = int(world.level.exit[1]) - offsetY
        frames = self.sprites["exitFrames"]
        pulse = 1.0 + 0.08 * math.sin(world.frame * 0.08)
        self.drawGlow("portalGlow", exitX + tileSize / 2, exitY + 2, pulse)
        self.buffer.blit(frames[(world.frame // 6) % exitFrameCount], (exitX, exitY - tileSize))

    def drawCheckpoints(self, world, offsetX, offsetY):
        for index, point in enumerate(world.level.checkpoints):
            x = int(point[0]) - offsetX
            y = int(point[1]) - offsetY
            if index in world.activatedCheckpoints:
                pulse = 1.0 + 0.12 * math.sin(world.frame * 0.15 + index)
                self.drawGlow("lanternGlow", x + 8, y + 5, pulse)
                self.buffer.blit(self.sprites["checkpointLit"], (x, y))
                if (world.frame // 5 + index) % 3:
                    self.buffer.set_at((x + 7, y + 4), theme.lanternCore)
            else:
                self.buffer.blit(self.sprites["checkpointIdle"], (x, y))

    def drawDoors(self, world, offsetX, offsetY):
        for door in world.doors:
            self.buffer.blit(self.doorSprite(door), (int(door.x) - offsetX, int(door.y) - offsetY))

    def drawPlatforms(self, world, offsetX, offsetY):
        for platform in world.platforms:
            startX = platform.fromX + platform.w / 2 - offsetX
            startY = platform.fromY + platform.h / 2 - offsetY
            endX = platform.toX + platform.w / 2 - offsetX
            endY = platform.toY + platform.h / 2 - offsetY
            steps = max(1, int(math.hypot(endX - startX, endY - startY) // 8))
            for step in range(steps + 1):
                amount = step / steps
                dotX = int(startX + (endX - startX) * amount)
                dotY = int(startY + (endY - startY) * amount)
                self.buffer.set_at((dotX, dotY), theme.trackColor)
        for platform in world.platforms:
            self.buffer.blit(self.slabSprite(platform), (int(platform.x) - offsetX, int(platform.y) - offsetY))

    def drawItems(self, world, offsetX, offsetY):
        for item in world.items:
            if item.collected:
                continue
            sprite = self.sprites.get(item.kind)
            if sprite is None:
                continue
            bob = -2 if (item.bob and int(item.bobPhase * 2) % 2 == 0) else 0
            x = int(item.x) - offsetX
            y = int(item.y) - offsetY + bob
            if item.kind == "berry":
                self.drawGlow("berryGlow", x + 8, y + 9, 1.0 + 0.15 * math.sin(item.bobPhase * 2))
            self.buffer.blit(sprite, (x, y))

    def drawEnemies(self, world, offsetX, offsetY):
        for enemy in world.enemies:
            if not enemy.alive:
                continue
            sprite = self.sprites.get(enemy.kind, self.sprites["beetle"])
            if enemy.facing > 0:
                sprite = pygame.transform.flip(sprite, True, False)
            self.buffer.blit(sprite, (int(enemy.x) - offsetX, int(enemy.y) - offsetY))

    def drawProjectiles(self, world, offsetX, offsetY):
        for projectile in world.projectiles:
            if not projectile.alive:
                continue
            x = int(projectile.centerX) - offsetX
            y = int(projectile.centerY) - offsetY
            pygame.draw.circle(self.buffer, theme.emberMid, (x, y), 3)
            pygame.draw.circle(self.buffer, theme.emberLight, (x, y), 1)

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

    def drawSlash(self, world, offsetX, offsetY):
        player = world.player
        if not player.alive or not player.isAttacking():
            return
        progress = min(1.0, (attackFrames - player.attackTimer + 1) / attackFrames * 1.6)
        centerX = int(player.centerX) - offsetX
        centerY = int(player.centerY) - offsetY
        radius = int(attackReach + player.w / 2)
        sweep = math.pi * 0.9
        if player.facing > 0:
            angles = (sweep / 2 - sweep * progress, sweep / 2)
        else:
            angles = (math.pi - sweep / 2, math.pi - sweep / 2 + sweep * progress)
        arcRect = pygame.Rect(centerX - radius, centerY - radius, radius * 2, radius * 2)
        pygame.draw.arc(self.buffer, theme.slashTrail, arcRect.inflate(-5, -5), angles[0], angles[1], 2)
        pygame.draw.arc(self.buffer, theme.slashColor, arcRect, angles[0], angles[1], 2)

    def renderWorld(self, world):
        offsetX, offsetY = world.camera.offset()
        self.backdrop.draw(self.buffer, offsetX, world.frame)
        self.drawExit(world, offsetX, offsetY)
        self.drawTiles(world, offsetX, offsetY)
        self.drawDoors(world, offsetX, offsetY)
        self.drawCheckpoints(world, offsetX, offsetY)
        self.drawPlatforms(world, offsetX, offsetY)
        self.drawItems(world, offsetX, offsetY)
        self.drawProjectiles(world, offsetX, offsetY)
        self.drawEnemies(world, offsetX, offsetY)
        self.drawParticles(world, offsetX, offsetY)
        self.drawPlayer(world, offsetX, offsetY)
        self.drawSlash(world, offsetX, offsetY)
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

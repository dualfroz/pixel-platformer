import math
import random

import pygame

from . import theme
from .propArt import glowDisc


def blendColor(first, second, amount):
    return tuple(int(a + (b - a) * amount) for a, b in zip(first, second))


def periodicHeight(x, period, waves):
    return sum(amplitude * math.sin(math.tau * (x * frequency / period) + phase) for amplitude, frequency, phase in waves)


class Backdrop:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sky = self.buildSky()
        self.clouds = self.buildClouds(560)
        self.ridges = self.buildRidges(480)
        self.forestFar = self.buildForest(400, theme.forestMid, 34, 58, 7, 31)
        self.mist = self.buildMist()
        self.forestNear = self.buildForest(352, theme.forestNear, 18, 46, 5, 47)

    def buildSky(self):
        surf = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            blend = y / (self.height - 1)
            if blend < 0.55:
                color = blendColor(theme.skyTop, theme.skyMiddle, blend / 0.55)
            else:
                color = blendColor(theme.skyMiddle, theme.skyBottom, (blend - 0.55) / 0.45)
            pygame.draw.line(surf, color, (0, y), (self.width, y))
        rng = random.Random(7)
        for _ in range(46):
            x = rng.randrange(self.width)
            y = rng.randrange(int(self.height * 0.45))
            surf.set_at((x, y), blendColor(theme.starColor, theme.skyTop, y / (self.height * 0.5)))
        moonX = int(self.width * 0.78)
        moonY = 30
        surf.blit(glowDisc(30, theme.moonGlow), (moonX - 30, moonY - 30))
        pygame.draw.circle(surf, theme.moonColor, (moonX, moonY), 11)
        for spot, radius in (((moonX - 4, moonY - 2), 2), ((moonX + 3, moonY + 4), 3), ((moonX + 5, moonY - 5), 1)):
            pygame.draw.circle(surf, theme.moonShade, spot, radius)
        return surf

    def buildClouds(self, period):
        surf = pygame.Surface((period, 70), pygame.SRCALPHA)
        rng = random.Random(19)
        for index in range(7):
            x = index * period // 7 + rng.randrange(20)
            y = 12 + rng.randrange(44)
            length = 50 + rng.randrange(70)
            for copyX in (x, x - period):
                pygame.draw.ellipse(surf, (*theme.cloudShade, 120), (copyX + 6, y + 2, length, 6))
                pygame.draw.ellipse(surf, (*theme.cloudColor, 150), (copyX, y, length - 8, 5))
                pygame.draw.ellipse(surf, (*theme.cloudColor, 110), (copyX + length // 3, y - 3, length // 2, 5))
        return surf

    def buildRidges(self, period):
        bandHeight = 110
        surf = pygame.Surface((period, bandHeight), pygame.SRCALPHA)
        waves = ((14, 2, 0.4), (9, 5, 1.7), (4, 11, 0.2))
        points = [(x, 40 + periodicHeight(x, period, waves)) for x in range(0, period + 1, 4)]
        pygame.draw.polygon(surf, theme.ridgeFar, points + [(period, bandHeight), (0, bandHeight)])
        pygame.draw.lines(surf, theme.ridgeFarLight, False, points)
        for x, y in points[::5]:
            pygame.draw.line(surf, theme.ridgeFarLight, (x, y + 3), (x + 3, y + 10))
        return surf

    def buildForest(self, period, color, minHeight, maxHeight, spacing, seed):
        bandHeight = maxHeight + 30
        surf = pygame.Surface((period, bandHeight), pygame.SRCALPHA)
        rng = random.Random(seed)
        pygame.draw.rect(surf, color, (0, bandHeight - 26, period, 26))
        x = 0
        while x < period:
            treeHeight = rng.randint(minHeight, maxHeight)
            for copyX in (x, x - period, x + period):
                self.drawPine(surf, copyX, bandHeight - 22, treeHeight, color)
            x += spacing + rng.randrange(spacing * 2)
        return surf

    def drawPine(self, surf, x, baseY, height, color):
        halfWidth = max(3, height // 4)
        tiers = 4
        for tier in range(tiers):
            tierTop = baseY - height + tier * height // (tiers + 1)
            tierBottom = tierTop + height // 2
            spread = halfWidth * (tier + 2) // (tiers + 1)
            pygame.draw.polygon(surf, color, [(x, tierTop), (x + spread, tierBottom), (x - spread, tierBottom)])
        pygame.draw.rect(surf, color, (x - 1, baseY - height // 3, 2, height // 3 + 4))

    def buildMist(self):
        surf = pygame.Surface((self.width, 40), pygame.SRCALPHA)
        red, green, blue, alpha = theme.mistColor
        for y in range(40):
            strength = alpha * math.sin(math.pi * y / 39)
            pygame.draw.line(surf, (red, green, blue, int(strength)), (0, y), (self.width, y))
        return surf

    def blitBand(self, target, band, shift, y):
        period = band.get_width()
        x = -int(shift % period)
        while x < self.width:
            target.blit(band, (x, y))
            x += period

    def draw(self, target, offsetX, frame):
        target.blit(self.sky, (0, 0))
        self.blitBand(target, self.clouds, offsetX * 0.12 + frame * 0.08, 8)
        self.blitBand(target, self.ridges, offsetX * 0.2, self.height - self.ridges.get_height())
        self.blitBand(target, self.forestFar, offsetX * 0.35, self.height - self.forestFar.get_height() + 6)
        target.blit(self.mist, (0, self.height - 70))
        self.blitBand(target, self.forestNear, offsetX * 0.55, self.height - self.forestNear.get_height() + 14)

import math

import pygame

from ..constants import tileSize
from . import theme

exitFrameCount = 6


def lanternSurface(lit):
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.rect(surf, theme.lanternStoneDark, (3, 13, 10, 3))
    pygame.draw.rect(surf, theme.lanternStone, (4, 13, 8, 1))
    pygame.draw.rect(surf, theme.lanternStone, (6, 8, 4, 5))
    pygame.draw.line(surf, theme.lanternStoneDark, (9, 8), (9, 12))
    pygame.draw.rect(surf, theme.lanternStone, (3, 1, 10, 2))
    pygame.draw.rect(surf, theme.lanternStoneDark, (4, 7, 8, 1))
    glass = theme.lanternOn if lit else theme.lanternOff
    pygame.draw.rect(surf, glass, (5, 3, 6, 4))
    pygame.draw.line(surf, theme.lanternStoneDark, (8, 3), (8, 6))
    pygame.draw.line(surf, theme.lanternStone, (4, 3), (4, 6))
    pygame.draw.line(surf, theme.lanternStone, (11, 3), (11, 6))
    surf.set_at((8, 0), theme.lanternStone)
    if lit:
        surf.set_at((6, 4), theme.lanternCore)
        surf.set_at((6, 5), theme.lanternCore)
        surf.set_at((10, 4), theme.lanternCore)
    else:
        surf.set_at((6, 4), theme.lanternStoneDark)
    return surf


def archFrame():
    width = tileSize
    height = tileSize * 2
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, theme.portalStone, (0, 0, width, 14))
    pygame.draw.rect(surf, theme.portalStone, (0, 7, width, height - 7))
    pygame.draw.ellipse(surf, theme.portalInner, (3, 3, width - 6, 10))
    pygame.draw.rect(surf, theme.portalInner, (3, 8, width - 6, height - 10))
    pygame.draw.line(surf, theme.portalStoneDark, (width - 1, 7), (width - 1, height - 1))
    pygame.draw.line(surf, theme.portalStoneDark, (2, 9), (2, height - 2))
    pygame.draw.rect(surf, theme.portalStoneDark, (0, height - 2, width, 2))
    surf.set_at((7, 1), theme.portalLight)
    surf.set_at((8, 1), theme.portalLight)
    for y in (12, 20, 27):
        surf.set_at((0, y), theme.mossLight)
        surf.set_at((15, y - 3), theme.mossDark)
    return surf


def portalFrames():
    frames = []
    base = archFrame()
    for index in range(exitFrameCount):
        surf = base.copy()
        phase = index / exitFrameCount
        for y in range(5, tileSize * 2 - 3):
            shimmer = math.sin((y / 5.0 - phase) * math.tau)
            if shimmer > 0.55:
                left = 4 if y > 8 else 5
                right = tileSize - 5 if y > 8 else tileSize - 6
                pygame.draw.line(surf, theme.portalLight, (left, y), (right, y))
            elif shimmer > 0.1:
                surf.set_at((5 + (y + index) % 6, y), theme.portalLight)
        frames.append(surf)
    return frames


def doorSurface(width, height, opened):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    if opened:
        pygame.draw.rect(surf, theme.doorwayShadow, (2, 0, width - 4, height))
        pygame.draw.rect(surf, theme.doorBand, (0, 0, 2, height))
        pygame.draw.rect(surf, theme.doorBand, (width - 2, 0, 2, height))
        pygame.draw.rect(surf, theme.doorBand, (0, 0, width, 2))
        pygame.draw.rect(surf, theme.doorWoodDark, (2, 2, 3, height - 2))
        pygame.draw.line(surf, theme.doorWood, (3, 2), (3, height - 1))
        return surf
    pygame.draw.rect(surf, theme.doorWood, (0, 0, width, height))
    for x in range(4, width, 4):
        pygame.draw.line(surf, theme.doorWoodDark, (x, 1), (x, height - 1))
    pygame.draw.rect(surf, theme.doorBand, (0, 0, width, height), 1)
    for bandY in (3, height - 6):
        pygame.draw.rect(surf, theme.doorBand, (0, bandY, width, 3))
        pygame.draw.line(surf, theme.doorBandLight, (1, bandY), (width - 2, bandY))
        for rivetX in (2, width - 3):
            surf.set_at((rivetX, bandY + 1), theme.doorBandLight)
    lockY = height // 2 - 3
    pygame.draw.rect(surf, theme.doorBand, (width // 2 - 3, lockY, 6, 7))
    pygame.draw.rect(surf, theme.doorLock, (width // 2 - 2, lockY + 1, 4, 5))
    surf.set_at((width // 2 - 1, lockY + 2), theme.doorwayShadow)
    surf.set_at((width // 2, lockY + 2), theme.doorwayShadow)
    pygame.draw.line(surf, theme.doorwayShadow, (width // 2 - 1, lockY + 3), (width // 2 - 1, lockY + 4))
    return surf


def floatingSlabSurface(width, height):
    surf = pygame.Surface((width, height + 3), pygame.SRCALPHA)
    pygame.draw.rect(surf, theme.runeBase, (0, 0, width, height))
    pygame.draw.rect(surf, theme.runeDark, (0, 0, width, height), 1)
    pygame.draw.line(surf, theme.runeLight, (1, 2), (width - 2, 2))
    pygame.draw.rect(surf, theme.grassMid, (0, 0, width, 2))
    for x in range(1, width, 3):
        surf.set_at((x, 0), theme.grassLight)
    for x in range(5, width - 3, 9):
        surf.set_at((x, 2), theme.mossDark)
        surf.set_at((x + 1, 3), theme.mossDark)
    for centerX in range(8, width, 16):
        glyphY = height // 2 + 1
        pygame.draw.line(surf, theme.runeGlow, (centerX - 2, glyphY), (centerX + 2, glyphY))
        pygame.draw.line(surf, theme.runeGlow, (centerX, glyphY - 2), (centerX, glyphY + 2))
    glow = pygame.Surface((width - 4, 3), pygame.SRCALPHA)
    glow.fill((*theme.runeGlow, 90))
    surf.blit(glow, (2, height))
    pygame.draw.line(surf, theme.runeGlow, (3, height), (width - 4, height))
    return surf


def glowDisc(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    red, green, blue, alpha = color
    for ring in range(radius, 0, -1):
        strength = alpha * (1.0 - ring / radius) + 4
        pygame.draw.circle(surf, (red, green, blue, int(min(255, strength))), (radius, radius), ring)
    return surf


def buildPropSprites():
    return {
        "checkpointIdle": lanternSurface(False),
        "checkpointLit": lanternSurface(True),
        "lanternGlow": glowDisc(14, theme.lanternGlow),
        "berryGlow": glowDisc(8, theme.berryGlow),
        "exitFrames": portalFrames(),
        "portalGlow": glowDisc(18, (*theme.portalLight, 40)),
    }

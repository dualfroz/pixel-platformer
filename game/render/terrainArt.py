import random

import pygame

from ..constants import tileSize
from . import theme


def speckle(surf, rect, colors, count, seed):
    rng = random.Random(seed)
    left, top, width, height = rect
    for _ in range(count):
        surf.set_at((left + rng.randrange(width), top + rng.randrange(height)), rng.choice(colors))


def mossyStoneBody(surf, top, seed):
    surf.fill(theme.stoneMid, (0, top, tileSize, tileSize - top))
    for index, rowTop in enumerate(range(top, tileSize, 8)):
        rowBottom = min(rowTop + 8, tileSize) - 1
        pygame.draw.line(surf, theme.stoneLight, (0, rowTop), (tileSize - 1, rowTop))
        pygame.draw.line(surf, theme.stoneCrack, (0, rowBottom), (tileSize - 1, rowBottom))
        jointX = 5 if index % 2 == 0 else 11
        pygame.draw.line(surf, theme.stoneCrack, (jointX, rowTop), (jointX, rowBottom))
        pygame.draw.line(surf, theme.stoneLight, (jointX + 1, rowTop + 1), (jointX + 1, rowBottom - 1))
    speckle(surf, (0, top, tileSize, tileSize - top), (theme.stoneDark, theme.stoneLight), 10, seed)
    speckle(surf, (0, top, tileSize, tileSize - top), (theme.mossLight, theme.mossDark), 7, seed + 1)


def groundTopSurface():
    surf = pygame.Surface((tileSize, tileSize))
    mossyStoneBody(surf, 4, 11)
    pygame.draw.rect(surf, theme.grassMid, (0, 0, tileSize, 4))
    pygame.draw.line(surf, theme.grassDark, (0, 4), (tileSize - 1, 4))
    for x in (1, 4, 7, 9, 13):
        surf.set_at((x, 0), theme.grassLight)
        surf.set_at((x, 1), theme.grassLight)
    for x, depth in ((2, 7), (3, 6), (8, 8), (12, 6), (13, 7)):
        pygame.draw.line(surf, theme.grassDark, (x, 5), (x, depth))
        surf.set_at((x, depth), theme.mossDark)
    return surf


def groundSurface():
    surf = pygame.Surface((tileSize, tileSize))
    mossyStoneBody(surf, 0, 23)
    return surf


def soilSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill(theme.soilMid)
    for y, shift in ((4, 0), (11, 3)):
        for x in range(tileSize):
            wave = y + (1 if (x + shift) % 7 < 3 else 0)
            surf.set_at((x, wave), theme.soilDark)
            surf.set_at((x, wave + 1), theme.soilDark)
            surf.set_at((x, wave - 1), theme.soilLight)
    speckle(surf, (0, 0, tileSize, tileSize), (theme.soilPebble, theme.soilDark), 9, 41)
    for point in ((9, 6), (10, 7), (10, 8), (11, 9), (12, 9)):
        surf.set_at(point, theme.rootColor)
    return surf


def slateSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill(theme.slateMid)
    pygame.draw.line(surf, theme.slateLight, (0, 0), (tileSize - 1, 0))
    pygame.draw.line(surf, theme.slateLight, (0, 0), (0, tileSize - 1))
    pygame.draw.line(surf, theme.slateDark, (0, tileSize - 1), (tileSize - 1, tileSize - 1))
    pygame.draw.line(surf, theme.slateDark, (tileSize - 1, 0), (tileSize - 1, tileSize - 1))
    pygame.draw.lines(surf, theme.slateDark, False, [(4, 3), (6, 6), (5, 9), (8, 12)])
    speckle(surf, (1, 1, tileSize - 2, tileSize - 2), (theme.slateLight, theme.slateDark), 8, 53)
    return surf


def runeBlockSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill(theme.runeBase)
    pygame.draw.rect(surf, theme.runeDark, (0, 0, tileSize, tileSize), 1)
    pygame.draw.line(surf, theme.runeLight, (1, 1), (tileSize - 2, 1))
    pygame.draw.line(surf, theme.runeLight, (1, 1), (1, tileSize - 2))
    pygame.draw.line(surf, theme.runeDark, (2, tileSize - 2), (tileSize - 2, tileSize - 2))
    pygame.draw.line(surf, theme.runeDark, (tileSize - 2, 2), (tileSize - 2, tileSize - 2))
    glyph = [(8, 4), (11, 8), (8, 12), (5, 8)]
    pygame.draw.polygon(surf, theme.runeGlow, glyph, 1)
    pygame.draw.line(surf, theme.runeGlow, (8, 6), (8, 10))
    surf.set_at((8, 8), theme.slashColor)
    for x in (3, 4, 9, 12):
        surf.set_at((x, 0), theme.mossLight)
    surf.set_at((3, 1), theme.mossDark)
    surf.set_at((12, 1), theme.mossDark)
    return surf


def logPlatformSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.rect(surf, theme.barkMid, (0, 2, tileSize, 5))
    pygame.draw.line(surf, theme.barkLight, (0, 3), (tileSize - 1, 3))
    pygame.draw.line(surf, theme.barkDark, (0, 6), (tileSize - 1, 6))
    for x in (3, 10):
        pygame.draw.line(surf, theme.barkDark, (x, 4), (x + 2, 4))
    pygame.draw.rect(surf, theme.mossDark, (0, 1, tileSize, 1))
    pygame.draw.rect(surf, theme.grassMid, (0, 0, tileSize, 1))
    for x in (2, 6, 11, 14):
        surf.set_at((x, 0), theme.grassLight)
    for x, depth in ((4, 9), (12, 8)):
        pygame.draw.line(surf, theme.grassDark, (x, 7), (x, depth))
    return surf


def plankSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.line(surf, theme.ropeColor, (0, 1), (tileSize - 1, 1))
    pygame.draw.rect(surf, theme.plankLight, (0, 2, tileSize, 4))
    pygame.draw.line(surf, theme.plankDark, (0, 5), (tileSize - 1, 5))
    for x in (0, 8):
        pygame.draw.line(surf, theme.plankDark, (x, 2), (x, 5))
        surf.set_at((x + 3, 2), theme.ropeColor)
    return surf


def thornSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.rect(surf, theme.thornDark, (0, 12, tileSize, 4))
    for base in (1, 6, 11):
        pygame.draw.polygon(surf, theme.thornDark, [(base, 13), (base + 2, 4), (base + 4, 13)])
        pygame.draw.line(surf, theme.thornLight, (base + 2, 4), (base + 2, 9))
    for point in ((4, 10), (9, 9), (14, 11), (0, 9)):
        surf.set_at(point, theme.thornLight)
    return surf


def emberSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill(theme.emberDark)
    pygame.draw.rect(surf, theme.emberMid, (0, 0, tileSize, 6))
    for x in range(tileSize):
        surf.set_at((x, 0 if x % 6 < 3 else 1), theme.emberLight)
    for spot in ((3, 9), (10, 7), (13, 12), (6, 13)):
        surf.set_at(spot, theme.emberLight)
    return surf


def vineLadderSurface(top):
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.rect(surf, theme.barkMid, (3, 0, 2, tileSize))
    pygame.draw.rect(surf, theme.barkMid, (11, 0, 2, tileSize))
    for y in (2, 7, 12):
        pygame.draw.rect(surf, theme.barkLight, (3, y, 10, 2))
        pygame.draw.line(surf, theme.barkDark, (3, y + 2), (12, y + 2))
    for point in ((2, 4), (13, 9), (2, 14), (13, 1)):
        surf.set_at(point, theme.leafColor)
    if top:
        pygame.draw.rect(surf, theme.barkLight, (1, 0, 14, 2))
        surf.set_at((1, 0), theme.grassLight)
        surf.set_at((14, 0), theme.grassLight)
    return surf


def slopeSurface(ascendRight):
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    body = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    mossyStoneBody(body, 0, 67 if ascendRight else 71)
    mask = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    if ascendRight:
        points = [(0, tileSize), (tileSize, 0), (tileSize, tileSize)]
    else:
        points = [(0, 0), (tileSize, tileSize), (0, tileSize)]
    pygame.draw.polygon(mask, (255, 255, 255, 255), points)
    body.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(body, (0, 0))
    for x in range(tileSize):
        edgeY = tileSize - 1 - x if ascendRight else x
        for depth, color in ((0, theme.grassLight), (1, theme.grassMid), (2, theme.grassMid), (3, theme.grassDark)):
            y = edgeY + depth
            if 0 <= y < tileSize:
                surf.set_at((x, y), color)
    return surf


def buildTerrainSprites():
    return {
        "groundTop": groundTopSurface(),
        "ground": groundSurface(),
        "dirt": soilSurface(),
        "stone": slateSurface(),
        "brick": runeBlockSurface(),
        "platform": logPlatformSurface(),
        "woodOneWay": plankSurface(),
        "spike": thornSurface(),
        "lava": emberSurface(),
        "ladder": vineLadderSurface(False),
        "ladderTop": vineLadderSurface(True),
        "slopeRight": slopeSurface(True),
        "slopeLeft": slopeSurface(False),
    }

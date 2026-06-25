import pygame

from .constants import tileSize

transparent = (0, 0, 0, 0)

playerPalette = {
    "r": (216, 40, 0),
    "s": (252, 188, 140),
    "h": (100, 52, 16),
    "o": (32, 56, 236),
    "k": (0, 0, 0),
    "y": (247, 213, 29),
}

playerPattern = [
    "................",
    "....rrrrrr......",
    "...rrrrrrrrr....",
    "...hhhssskss....",
    "..hshsssksss....",
    "..hhhssssksss...",
    "..hhsssssssss...",
    "....sssssss.....",
    "...rrrrrrrr.....",
    "..rrrrrrrrrr....",
    ".ssrroooorrss...",
    ".ssrooooooorss..",
    "...ooyooyoo.....",
    "...oooooooo.....",
    "...ooo..ooo.....",
    "..hhh....hhh....",
]

goombaPalette = {
    "d": (60, 30, 10),
    "m": (150, 75, 30),
    "w": (255, 255, 255),
    "k": (0, 0, 0),
    "f": (20, 12, 8),
}

goombaPattern = [
    "................",
    ".....dddddd.....",
    "...ddmmmmmmdd...",
    "..dmmmmmmmmmmd..",
    ".dmmmmmmmmmmmmd.",
    ".dmmwwmmmmwwmmd.",
    ".dmmwkmmmmwkmmd.",
    ".dmmwwmmmmwwmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmmmmmmmmmmd.",
    "..dmmmmmmmmmmd..",
    "...dmmmmmmmmd...",
    "....dddddddd....",
    "...ff....ff.....",
    "..ffff..ffff....",
    "................",
]


def patternSurface(pattern, palette):
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    for y, line in enumerate(pattern):
        for x, code in enumerate(line):
            if code == ".":
                continue
            surf.set_at((x, y), palette[code])
    return surf


def coinSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (200, 160, 20), (3, 1, 10, 14))
    pygame.draw.ellipse(surf, (247, 213, 29), (4, 2, 8, 12))
    pygame.draw.rect(surf, (255, 245, 170), (6, 4, 1, 8))
    return surf


def groundSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill((198, 100, 29))
    pygame.draw.rect(surf, (222, 140, 80), (0, 0, tileSize, 4))
    pygame.draw.line(surf, (120, 60, 15), (0, tileSize - 1), (tileSize - 1, tileSize - 1))
    pygame.draw.line(surf, (120, 60, 15), (tileSize - 1, 0), (tileSize - 1, tileSize - 1))
    for spot in ((4, 8), (11, 6), (7, 12), (13, 11)):
        surf.set_at(spot, (150, 74, 18))
    return surf


def brickSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill((181, 94, 41))
    mortar = (74, 38, 18)
    pygame.draw.line(surf, mortar, (0, 0), (tileSize - 1, 0))
    pygame.draw.line(surf, mortar, (0, 8), (tileSize - 1, 8))
    pygame.draw.line(surf, mortar, (8, 1), (8, 7))
    pygame.draw.line(surf, mortar, (0, 9), (0, tileSize - 1))
    pygame.draw.line(surf, mortar, (15, 9), (15, tileSize - 1))
    return surf


def platformSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill((217, 164, 65))
    pygame.draw.rect(surf, (150, 100, 30), (0, 0, tileSize, tileSize), 1)
    pygame.draw.rect(surf, (247, 213, 29), (2, 2, tileSize - 4, 3))
    for spot in ((2, 2), (13, 2), (2, 13), (13, 13)):
        surf.set_at(spot, (90, 58, 18))
    return surf


def pipeSurface(top, leftSide):
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill((0, 168, 0))
    if leftSide:
        pygame.draw.rect(surf, (128, 232, 128), (2, 0, 3, tileSize))
        pygame.draw.line(surf, (0, 96, 0), (0, 0), (0, tileSize - 1))
    else:
        pygame.draw.rect(surf, (72, 200, 72), (8, 0, 3, tileSize))
        pygame.draw.rect(surf, (0, 96, 0), (13, 0, 3, tileSize))
    if top:
        pygame.draw.rect(surf, (0, 200, 0), (0, 0, tileSize, 6))
        pygame.draw.rect(surf, (0, 96, 0), (0, 0, tileSize, 6), 1)
        if leftSide:
            pygame.draw.rect(surf, (160, 255, 160), (2, 1, 3, 4))
    return surf


def buildSprites():
    return {
        "player": patternSurface(playerPattern, playerPalette),
        "goomba": patternSurface(goombaPattern, goombaPalette),
        "coin": coinSurface(),
        "ground": groundSurface(),
        "brick": brickSurface(),
        "platform": platformSurface(),
        "pipeTL": pipeSurface(True, True),
        "pipeTR": pipeSurface(True, False),
        "pipeBL": pipeSurface(False, True),
        "pipeBR": pipeSurface(False, False),
    }

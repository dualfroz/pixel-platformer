import pygame

from ..constants import tileSize
from .theme import tileFallback

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

chaserPalette = {
    "d": (40, 8, 60),
    "m": (150, 40, 170),
    "w": (255, 240, 120),
    "k": (0, 0, 0),
}

chaserPattern = [
    "................",
    "....k......k....",
    "...kmk....kmk...",
    "...dmmkkkkmmd...",
    "..dmmmmmmmmmmd..",
    ".dmmwwmmmmwwmmd.",
    ".dmmwkmmmmwkmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmkkkkkkmmmd.",
    ".dmmmkwwwwkmmmd.",
    "..dmmmmmmmmmmd..",
    "...dmmmmmmmmd...",
    "....dmmmmmmd....",
    "...dd.dd.dd.d...",
    "..dd..dd..dd....",
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


def flyerSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (60, 160, 210), (4, 4, 8, 8))
    pygame.draw.ellipse(surf, (140, 220, 255), (5, 5, 6, 5))
    pygame.draw.polygon(surf, (200, 240, 255), [(0, 4), (4, 6), (4, 10)])
    pygame.draw.polygon(surf, (200, 240, 255), [(15, 4), (11, 6), (11, 10)])
    surf.set_at((6, 7), (0, 0, 0))
    surf.set_at((9, 7), (0, 0, 0))
    return surf


def shooterSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.rect(surf, (70, 90, 90), (3, 4, 10, 10))
    pygame.draw.rect(surf, (110, 140, 140), (4, 5, 8, 4))
    pygame.draw.rect(surf, (200, 60, 40), (6, 9, 4, 3))
    pygame.draw.rect(surf, (40, 50, 50), (2, 13, 12, 2))
    return surf


def coinSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (200, 160, 20), (3, 1, 10, 14))
    pygame.draw.ellipse(surf, (247, 213, 29), (4, 2, 8, 12))
    pygame.draw.rect(surf, (255, 245, 170), (6, 4, 1, 8))
    return surf


def gemSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (60, 220, 200), [(8, 1), (14, 6), (8, 15), (2, 6)])
    pygame.draw.polygon(surf, (160, 255, 240), [(8, 1), (11, 6), (8, 8), (5, 6)])
    return surf


def keySurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.circle(surf, (240, 210, 60), (6, 6), 4)
    pygame.draw.circle(surf, (60, 40, 10), (6, 6), 2)
    pygame.draw.rect(surf, (240, 210, 60), (6, 8, 2, 6))
    pygame.draw.rect(surf, (240, 210, 60), (8, 12, 3, 2))
    return surf


def heartSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.circle(surf, (224, 48, 64), (5, 6), 3)
    pygame.draw.circle(surf, (224, 48, 64), (10, 6), 3)
    pygame.draw.polygon(surf, (224, 48, 64), [(2, 7), (14, 7), (8, 14)])
    pygame.draw.circle(surf, (255, 150, 160), (5, 5), 1)
    return surf


def solidTile(color, topColor):
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill(color)
    pygame.draw.rect(surf, topColor, (0, 0, tileSize, 3))
    pygame.draw.line(surf, (0, 0, 0), (tileSize - 1, 0), (tileSize - 1, tileSize - 1))
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
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.rect(surf, (217, 164, 65), (0, 0, tileSize, 6))
    pygame.draw.rect(surf, (247, 213, 29), (1, 0, tileSize - 2, 2))
    pygame.draw.line(surf, (150, 100, 30), (0, 6), (tileSize - 1, 6))
    return surf


def spikeSurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    for base in (0, 5, 10):
        pygame.draw.polygon(surf, (210, 214, 224), [(base, 15), (base + 3, 4), (base + 6, 15)])
        pygame.draw.polygon(surf, (150, 156, 170), [(base + 3, 15), (base + 4, 8), (base + 5, 15)])
    return surf


def lavaSurface():
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill((200, 60, 20))
    pygame.draw.rect(surf, (255, 150, 40), (0, 0, tileSize, 4))
    for spot in ((3, 8), (9, 6), (12, 11)):
        surf.set_at(spot, (255, 220, 120))
    return surf


def ladderSurface(top):
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    rail = (150, 100, 50)
    pygame.draw.rect(surf, rail, (3, 0, 2, tileSize))
    pygame.draw.rect(surf, rail, (11, 0, 2, tileSize))
    for y in (2, 7, 12):
        pygame.draw.rect(surf, (190, 140, 80), (3, y, 10, 2))
    if top:
        pygame.draw.rect(surf, (190, 140, 80), (1, 0, 14, 2))
    return surf


def slopeSurface(ascendRight):
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    if ascendRight:
        points = [(0, tileSize), (tileSize, 0), (tileSize, tileSize)]
    else:
        points = [(0, 0), (tileSize, tileSize), (0, tileSize)]
    pygame.draw.polygon(surf, (150, 74, 18), points)
    pygame.draw.polygon(surf, (222, 140, 80), points, 1)
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
    return surf


def buildSprites():
    sprites = {
        "player": patternSurface(playerPattern, playerPalette),
        "goomba": patternSurface(goombaPattern, goombaPalette),
        "chaser": patternSurface(chaserPattern, chaserPalette),
        "flyer": flyerSurface(),
        "shooter": shooterSurface(),
        "coin": coinSurface(),
        "gem": gemSurface(),
        "key": keySurface(),
        "heart": heartSurface(),
        "ground": solidTile((198, 100, 29), (222, 140, 80)),
        "dirt": solidTile((120, 72, 40), (150, 96, 56)),
        "stone": solidTile((110, 110, 128), (150, 150, 168)),
        "brick": brickSurface(),
        "platform": platformSurface(),
        "woodOneWay": platformSurface(),
        "spike": spikeSurface(),
        "lava": lavaSurface(),
        "ladder": ladderSurface(False),
        "ladderTop": ladderSurface(True),
        "slopeRight": slopeSurface(True),
        "slopeLeft": slopeSurface(False),
        "pipeTL": pipeSurface(True, True),
        "pipeTR": pipeSurface(True, False),
        "pipeBL": pipeSurface(False, True),
        "pipeBR": pipeSurface(False, False),
    }
    for name, color in tileFallback.items():
        sprites.setdefault(name, solidTile(color, color))
    return sprites

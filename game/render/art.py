import pygame

from ..constants import tileSize
from . import theme
from .terrainArt import buildTerrainSprites
from .propArt import buildPropSprites

playerPalette = {
    "k": (34, 22, 30),
    "o": (230, 118, 40),
    "d": (160, 70, 26),
    "c": (250, 232, 200),
    "u": (120, 214, 232),
    "b": (92, 58, 36),
    "g": (40, 170, 150),
    "t": (22, 112, 104),
    "v": (150, 140, 84),
    "y": (255, 214, 92),
}

playerPattern = [
    "......k...k.....",
    ".....kdk.kdk....",
    ".....kuubuuok...",
    ".....kooooook...",
    ".....koookoook..",
    ".....koccccccck.",
    ".kk...kcccccck..",
    "kook..kooccok...",
    "kcook.ggggggg...",
    "kccook.tvvcvvk..",
    ".kccooovvbccvok.",
    "..kcooovbvccvvk.",
    "...kkkbbbybbbk..",
    ".......ood.ood..",
    ".......odd.odd..",
    "......bbbb.bbbb.",
]

beetlePalette = {
    "k": (20, 18, 30),
    "s": (40, 92, 70),
    "m": (70, 150, 96),
    "h": (170, 230, 150),
    "e": (255, 196, 64),
    "l": (60, 44, 34),
}

beetlePattern = [
    "................",
    "................",
    "......kkkkk.....",
    "....kkhhmmmkk...",
    "...khhmmmmmmmk..",
    "..khmmmmmmmmmsk.",
    "..khmmmmmmmmmsk.",
    "k.kmmmmmmmmmmsk.",
    ".kkmmmmmmmmmssk.",
    "..kmmmmmmmmsssk.",
    ".kkkkkkkkkkkkkk.",
    "kekkllllllllllk.",
    "kkkllllllllllk..",
    ".kkkkkkkkkkkkk..",
    "..l..l..l..l....",
    ".l..l..l..l.....",
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


def berrySurface():
    surf = pygame.Surface((tileSize, tileSize), pygame.SRCALPHA)
    pygame.draw.line(surf, theme.barkDark, (8, 1), (8, 3))
    pygame.draw.polygon(surf, theme.leafColor, [(8, 2), (11, 0), (13, 1), (10, 3)])
    for centerX, centerY in ((8, 6), (5, 11), (11, 11)):
        pygame.draw.circle(surf, theme.berryShade, (centerX, centerY), 3)
        pygame.draw.circle(surf, theme.berryBody, (centerX - 1, centerY - 1), 2)
        surf.set_at((centerX - 1, centerY - 2), theme.berryLight)
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


def flatTile(color):
    surf = pygame.Surface((tileSize, tileSize))
    surf.fill(color)
    return surf


def buildSprites():
    sprites = {
        "player": patternSurface(playerPattern, playerPalette),
        "beetle": patternSurface(beetlePattern, beetlePalette),
        "chaser": patternSurface(chaserPattern, chaserPalette),
        "flyer": flyerSurface(),
        "shooter": shooterSurface(),
        "berry": berrySurface(),
        "gem": gemSurface(),
        "key": keySurface(),
        "heart": heartSurface(),
    }
    sprites.update(buildTerrainSprites())
    sprites.update(buildPropSprites())
    for name, color in theme.tileFallback.items():
        sprites.setdefault(name, flatTile(color))
    return sprites

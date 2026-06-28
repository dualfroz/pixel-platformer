import os

import pygame

from ..constants import viewWidth, viewHeight
from ..sim.inputCommand import InputCommand
from ..sim.gameState import Game, PLAYING
from ..sim.builtinLevels import buildAll
from .renderer import Renderer
from .theme import renderScale
from .audioBackend import buildAudioSink


def readInput(pressed, edges):
    return InputCommand(
        left=pressed[pygame.K_LEFT] or pressed[pygame.K_a],
        right=pressed[pygame.K_RIGHT] or pressed[pygame.K_d],
        up=pressed[pygame.K_UP] or pressed[pygame.K_w],
        down=pressed[pygame.K_DOWN] or pressed[pygame.K_s],
        jump=pygame.K_SPACE in edges or pygame.K_z in edges,
        jumpHeld=pressed[pygame.K_SPACE] or pressed[pygame.K_z],
        dash=pygame.K_LSHIFT in edges or pygame.K_x in edges,
        run=pressed[pygame.K_LSHIFT],
        attack=pygame.K_c in edges,
        pause=pygame.K_ESCAPE in edges or pygame.K_p in edges,
        confirm=pygame.K_RETURN in edges or pygame.K_SPACE in edges,
    )


def attachAudio(game):
    if game.world is not None:
        game.world.audio.setSink(buildAudioSink())


def runPlay():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((viewWidth * renderScale, viewHeight * renderScale))
    pygame.display.set_caption("Pixel Platformer")
    clock = pygame.time.Clock()

    renderer = Renderer()
    game = Game(buildAll())
    audioSink = buildAudioSink()

    running = True
    lastMode = None
    while running:
        edges = set()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                edges.add(event.key)
        pressed = pygame.key.get_pressed()
        command = readInput(pressed, edges)
        game.update(command)

        if game.world is not None and game.mode == PLAYING and lastMode != PLAYING:
            game.world.audio.setSink(audioSink)
        lastMode = game.mode

        world = game.world
        if world is not None:
            frame = renderer.present(world, None if game.mode == PLAYING else game.mode)
        else:
            frame = renderer.present(_placeholderWorld(game), game.mode)
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def _placeholderWorld(game):
    game.startLevel(0)
    return game.world


def runScreenshot(path, frames):
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    pygame.font.init()

    levels = buildAll()
    game = Game(levels)
    game.start()
    for frame in range(frames):
        command = InputCommand(right=12 <= frame < 40, jump=frame in (14, 30), jumpHeld=14 <= frame < 20)
        game.update(command)

    renderer = Renderer()
    surface = renderer.present(game.world, None)
    pygame.image.save(surface, path)
    pygame.quit()
    print("wrote %s (%dx%d)" % (path, surface.get_width(), surface.get_height()))

import pytest

from tests.support import makeLevel
from game.sim.level import PlatformSpawn
from game.sim.world import World
from game.sim.movingPlatform import MovingPlatform
from game.sim.inputCommand import InputCommand


def buildPlatformWorld(spawn):
    level = makeLevel([
        " p        ",
        "          ",
        "          ",
        "          ",
        "XXXXXXXXXX",
    ])
    level.platforms.append(spawn)
    return World(level)


def test_platformOscillatesBetweenEndpoints():
    platform = MovingPlatform(16, 32, 48, 8, 80, 32, 4.0)
    seen = []
    for _ in range(60):
        platform.update()
        seen.append(platform.x)
    assert max(seen) <= 80.0 + 1e-6
    assert min(seen) >= 16.0 - 1e-6
    assert platform.direction in (-1, 1)


def seatOnPlatform(world):
    platform = world.platforms[0]
    world.player.x = platform.x + 6
    world.player.y = platform.y - world.player.h
    world.player.vx = 0.0
    world.player.vy = 0.0
    for _ in range(6):
        world.step(InputCommand())
    return platform


def test_playerCarriedHorizontallyByPlatform():
    world = buildPlatformWorld(PlatformSpawn(16, 48, 48, 8, 160, 48, 1.0))
    platform = seatOnPlatform(world)
    assert world.player.onGround
    assert world.player.groundPlatform is not None
    playerStart = world.player.x
    platformStart = platform.x
    for _ in range(10):
        world.step(InputCommand())
    playerDelta = world.player.x - playerStart
    platformDelta = platform.x - platformStart
    assert abs(platformDelta) > 4.0
    assert playerDelta == pytest.approx(platformDelta, abs=0.6)


def test_playerCarriedVerticallyByPlatform():
    world = buildPlatformWorld(PlatformSpawn(16, 60, 48, 8, 16, 20, 1.0))
    platform = seatOnPlatform(world)
    assert world.player.groundPlatform is not None
    playerStart = world.player.y
    platformStart = platform.y
    for _ in range(8):
        world.step(InputCommand())
    playerDelta = world.player.y - playerStart
    platformDelta = platform.y - platformStart
    assert abs(platformDelta) > 3.0
    assert playerDelta == pytest.approx(platformDelta, abs=0.9)

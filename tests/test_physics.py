import pytest

from game import constants
from tests.support import makeWorld, stepWorld, settle
from game.sim.inputCommand import InputCommand


def test_gravityAppliesWhenAirborne():
    world = makeWorld([
        "      ",
        " p    ",
        "      ",
        "      ",
        "XXXXXX",
    ])
    world.step(InputCommand())
    assert world.player.vy == pytest.approx(constants.gravity)


def test_playerLandsOnGround():
    world = makeWorld([
        "      ",
        " p    ",
        "      ",
        "XXXXXX",
    ])
    settle(world, 40)
    player = world.player
    assert player.onGround
    assert player.vy == 0.0
    assert player.bottom == pytest.approx(48.0)


def test_fallSpeedIsCapped():
    tall = ["          "] * 40
    tall[1] = " p        "
    tall.append("XXXXXXXXXX")
    world = makeWorld(tall)
    maxSeen = 0.0
    for _ in range(35):
        world.step(InputCommand())
        maxSeen = max(maxSeen, world.player.vy)
    assert maxSeen <= constants.maxFallSpeed + 1e-6
    assert maxSeen == pytest.approx(constants.maxFallSpeed)


def test_wallBlocksHorizontalMovement():
    world = makeWorld([
        "   #",
        " p #",
        "XXXX",
    ])
    stepWorld(world, 40, right=True, run=True)
    player = world.player
    wallLeft = 3 * constants.tileSize
    limit = wallLeft - player.w
    assert player.x <= limit + 0.01
    assert player.vx == 0.0
    assert player.onWallRight


def test_ceilingStopsUpwardMovement():
    world = makeWorld([
        "XXXX",
        "    ",
        " p  ",
        "XXXX",
    ])
    hitCeiling = False
    world.step(InputCommand(jump=True, jumpHeld=True))
    for _ in range(12):
        world.step(InputCommand(jumpHeld=True))
        if world.player.onCeiling:
            hitCeiling = True
            assert world.player.top >= constants.tileSize - 0.01
    assert hitCeiling

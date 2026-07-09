import pytest

from game import constants
from tests.support import makeWorld
from game.sim.inputCommand import InputCommand


def test_landsOnOneWayFromAbove():
    world = makeWorld([
        " p    ",
        "      ",
        "======",
        "      ",
        "XXXXXX",
    ])
    for _ in range(30):
        world.step(InputCommand())
    player = world.player
    assert player.onGround
    assert player.bottom == pytest.approx(2 * constants.tileSize)


def test_passesThroughOneWayFromBelow():
    world = makeWorld([
        "      ",
        "======",
        "      ",
        " p    ",
        "XXXXXX",
    ])
    minY = world.player.y
    world.step(InputCommand(jump=True, jumpHeld=True))
    for _ in range(16):
        world.step(InputCommand(jumpHeld=True))
        minY = min(minY, world.player.y)
    assert minY < constants.tileSize


def test_dropThroughOneWay():
    world = makeWorld([
        " p    ",
        "      ",
        "======",
        "      ",
        "XXXXXX",
    ])
    for _ in range(30):
        world.step(InputCommand())
    assert world.player.bottom == pytest.approx(2 * constants.tileSize)
    for _ in range(30):
        world.step(InputCommand(down=True, jump=True))
    assert world.player.bottom == pytest.approx(4 * constants.tileSize)


def test_downWithoutJumpKeepsPlayerOnOneWay():
    world = makeWorld([
        " p    ",
        "      ",
        "======",
        "      ",
        "XXXXXX",
    ])
    for _ in range(30):
        world.step(InputCommand())
    for _ in range(20):
        world.step(InputCommand(down=True))
    assert world.player.bottom == pytest.approx(2 * constants.tileSize)

import pytest

from game import constants
from tests.support import makeWorld
from game.sim.inputCommand import InputCommand


ladderLevel = [
    "  H  ",
    "  H  ",
    "  H  ",
    "XXXXX",
]


def seatOnLadder(world):
    world.player.x = 2 * constants.tileSize
    world.player.y = 2 * constants.tileSize
    world.player.vy = 0.0


def test_climbLadderReducesHeight():
    world = makeWorld(ladderLevel)
    seatOnLadder(world)
    startY = world.player.y
    for _ in range(8):
        world.step(InputCommand(up=True))
    assert world.player.onLadder
    assert world.player.y < startY - 6.0


def test_ladderHoverIgnoresGravity():
    world = makeWorld(ladderLevel)
    seatOnLadder(world)
    for _ in range(6):
        world.step(InputCommand(up=True))
    restingY = world.player.y
    for _ in range(6):
        world.step(InputCommand())
    assert world.player.y == pytest.approx(restingY, abs=0.5)


def test_leavingLadderTileDropsClimbState():
    world = makeWorld(ladderLevel)
    seatOnLadder(world)
    world.step(InputCommand(up=True))
    assert world.player.onLadder
    world.player.x = 0.0
    world.step(InputCommand())
    assert not world.player.onLadder

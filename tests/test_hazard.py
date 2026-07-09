from game import constants
from tests.support import makeWorld
from game.sim.inputCommand import InputCommand


spikeLevel = [
    "     ",
    "  p  ",
    "^^^^^",
    "XXXXX",
]

safeLevel = [
    "     ",
    "  p  ",
    "     ",
    "XXXXX",
]


def test_spikesDamagePlayer():
    world = makeWorld(spikeLevel)
    for _ in range(12):
        world.step(InputCommand())
    assert world.player.hp <= world.player.maxHp - 2
    assert world.player.iframes > 0


def test_noHazardKeepsFullHealth():
    world = makeWorld(safeLevel)
    for _ in range(12):
        world.step(InputCommand())
    assert world.player.hp == world.player.maxHp


def test_iframesPreventDoubleHit():
    world = makeWorld(spikeLevel)
    for _ in range(3):
        world.step(InputCommand())
    hpAfterFirst = world.player.hp
    world.step(InputCommand())
    assert world.player.hp == hpAfterFirst
    assert world.player.hp < world.player.maxHp

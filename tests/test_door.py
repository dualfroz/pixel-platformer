from game.constants import tileSize
from tests.support import makeLevel, makeWorld
from game.sim.world import World
from game.sim.inputCommand import InputCommand
from game.sim.level import levelFromDict, levelToAscii
from game.sim.saveLoad import captureState, applyState
from game.sim.builtinLevels import buildCavern


def walkRight(world, frames):
    for _ in range(frames):
        world.step(InputCommand(right=True))


def corridor(middle):
    return [
        "SSSSSSSSSSSSS",
        "S     |     S",
        "S" + middle + "S",
        "SSSSSSSSSSSSS",
    ]


def test_closedDoorBlocksPlayerWithoutKey():
    world = makeWorld(corridor(" p   |   E "))
    door = world.doors[0]
    walkRight(world, 90)
    assert not door.open
    assert world.player.right <= door.x + 1e-6
    assert not world.completed


def test_keyOpensDoorAndIsConsumed():
    world = makeWorld(corridor(" p k |   E "))
    door = world.doors[0]
    walkRight(world, 120)
    assert door.open
    assert world.player.inventory.keys == 0
    assert door not in world.colliders
    assert world.completed


def test_oneKeyOpensOneDoor():
    world = makeWorld([
        "SSSSSSSSSSSSS",
        "S    |  |   S",
        "S pk |  |  ES",
        "SSSSSSSSSSSSS",
    ])
    first, second = world.doors
    walkRight(world, 120)
    assert first.open
    assert not second.open
    assert first.x + first.w <= world.player.x
    assert world.player.right <= second.x + 1e-6
    assert not world.completed


def test_standingOnDoorDoesNotOpenIt():
    world = makeWorld([
        "   p   ",
        "   |   ",
        "   |   ",
        "XXXXXXX",
    ])
    door = world.doors[0]
    world.player.inventory.add("key")
    for _ in range(20):
        world.step(InputCommand())
    assert world.player.onGround
    assert world.player.bottom == door.y
    assert not door.open
    assert world.player.inventory.keys == 1


def test_doorBlocksEnemies():
    world = makeWorld(corridor("p  b |     "))
    beetle = world.enemies[0]
    beetle.direction = 1
    door = world.doors[0]
    turned = False
    for _ in range(80):
        world.step(InputCommand())
        assert beetle.right <= door.x + 1e-6
        turned = turned or beetle.direction < 0
    assert turned


def test_doorCellsMergeVertically():
    level = makeLevel(corridor(" p   |   E "))
    assert len(level.doors) == 1
    door = level.doors[0]
    assert (door.x, door.y, door.w, door.h) == (6 * tileSize, tileSize, tileSize, 2 * tileSize)


def test_doorsSurviveJsonAndAscii():
    lines = corridor(" p k |   E ")
    level = makeLevel(lines)
    restored = levelFromDict(level.asDict())
    assert [door.asDict() for door in restored.doors] == [door.asDict() for door in level.doors]
    assert levelToAscii(restored) == [line.rstrip() for line in lines]


def test_openDoorSurvivesSnapshot():
    lines = corridor(" p k |   E ")
    world = makeWorld(lines)
    walkRight(world, 60)
    assert world.doors[0].open
    snapshot = captureState(world)

    fresh = makeWorld(lines)
    assert not fresh.doors[0].open
    applyState(fresh, snapshot)
    assert fresh.doors[0].open
    assert fresh.doors[0] not in fresh.colliders


def test_cavernHasLockedExitRoom():
    level = buildCavern()
    assert len(level.doors) >= 1
    keys = [spawn for spawn in level.items if spawn.kind == "key"]
    assert len(keys) >= len(level.doors)
    world = World(level)
    walkRight(world, 1)
    assert all(not door.open for door in world.doors)

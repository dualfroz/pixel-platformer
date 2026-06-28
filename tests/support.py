from game.sim.level import parseAscii
from game.sim.world import World
from game.sim.inputCommand import InputCommand


def makeLevel(lines, name="test"):
    return parseAscii(name, lines)


def makeWorld(lines, name="test"):
    return World(parseAscii(name, lines))


def command(**kwargs):
    return InputCommand(**kwargs)


def stepWorld(world, times=1, **kwargs):
    cmd = InputCommand(**kwargs)
    for _ in range(times):
        world.step(cmd)
    return world


def settle(world, times=30):
    for _ in range(times):
        world.step(InputCommand())
    return world

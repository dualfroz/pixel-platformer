import math
import sys

from .constants import tileSize
from .sim.world import World
from .sim.inputCommand import InputCommand
from .sim.builtinLevels import buildMeadow
from .sim.gameState import Game, MENU, PLAYING, PAUSED
from .sim import physics


def groundSurfaceY(level):
    for row in range(level.rows):
        for col in range(level.cols):
            if level.solidAt(col, row):
                return row * tileSize
    return level.pixelHeight()


def penetratesSolid(world):
    shrunk = world.player.aabb.inflated(-0.75, -0.75)
    for tileBox in physics.solidTilesOverlapping(world.level, shrunk):
        if shrunk.intersects(tileBox):
            return True
    return False


def driveInput(world, frame, heading):
    player = world.player
    jump = frame % 22 == 0 or player.onWallLeft or player.onWallRight
    dash = frame % 75 == 0
    command = InputCommand(
        left=heading < 0,
        right=heading > 0,
        jump=jump,
        jumpHeld=(frame % 22) < 10,
        dash=dash,
        run=True,
    )
    return command


def runSmoke(totalFrames=640):
    world = World(buildMeadow())
    floorTop = groundSurfaceY(world.level)
    heading = 1
    stats = {
        "stomps": 0,
        "maxBottom": world.player.bottom,
        "minHp": world.player.hp,
        "damageTaken": 0,
        "berries": 0,
        "framesRun": 0,
    }
    previousScoreFromStomp = 0
    previousHp = world.player.hp

    for frame in range(totalFrames):
        if world.player.onWallRight and heading > 0:
            heading = -1
        elif world.player.onWallLeft and heading < 0:
            heading = 1
        if frame % 160 == 159:
            heading *= -1

        command = driveInput(world, frame, heading)
        world.step(command)
        stats["framesRun"] += 1

        player = world.player
        if not math.isfinite(player.x) or not math.isfinite(player.y):
            raise AssertionError("player position not finite at frame %d" % frame)
        if not (0 <= player.hp <= player.maxHp):
            raise AssertionError("hp %d out of range at frame %d" % (player.hp, frame))
        if player.alive and world.active and penetratesSolid(world):
            raise AssertionError("player penetrated solid tile at frame %d" % frame)
        if player.alive and world.active and player.bottom > floorTop + tileSize * 4 + 2:
            raise AssertionError("player fell through floor at frame %d bottom=%.1f" % (frame, player.bottom))
        if player.bottom > world.level.pixelHeight() + tileSize * 3:
            raise AssertionError("player left world at frame %d" % frame)

        if player.hp < previousHp:
            stats["damageTaken"] += previousHp - player.hp
        previousHp = player.hp if player.alive else player.maxHp
        stats["maxBottom"] = max(stats["maxBottom"], player.bottom)
        stats["minHp"] = min(stats["minHp"], player.hp)

    stats["berries"] = world.berries
    stats["enemiesLeft"] = len(world.enemies)
    stats["enemiesStart"] = len(world.level.enemies)
    stats["score"] = world.score
    stats["sounds"] = world.audio.totalEmitted
    stats["lives"] = world.lives
    stats["gameOver"] = world.gameOver
    stats["floorTop"] = floorTop
    return stats


def checkFsm():
    game = Game([buildMeadow()])
    transitions = []
    assert game.mode == MENU
    game.update(InputCommand(confirm=True))
    assert game.mode == PLAYING
    transitions.append("menu->playing")
    for _ in range(30):
        game.update(InputCommand(right=True))
    game.update(InputCommand(pause=True))
    assert game.mode == PAUSED
    transitions.append("playing->paused")
    game.update(InputCommand(pause=True))
    assert game.mode == PLAYING
    transitions.append("paused->playing")
    return transitions


def main():
    stats = runSmoke()
    fsm = checkFsm()
    print("SMOKE RESULT")
    print("  frames run          : %d" % stats["framesRun"])
    print("  enemies start/left  : %d / %d" % (stats["enemiesStart"], stats["enemiesLeft"]))
    print("  score               : %d" % stats["score"])
    print("  berries collected   : %d" % stats["berries"])
    print("  damage taken (hp)   : %d" % stats["damageTaken"])
    print("  min hp / lives      : %d / %d" % (stats["minHp"], stats["lives"]))
    print("  max player.bottom   : %.1f (floorTop=%d)" % (stats["maxBottom"], stats["floorTop"]))
    print("  sound events        : %d" % stats["sounds"])
    print("  fsm transitions     : %s" % ", ".join(fsm))
    print("INVARIANTS HELD: hp in range, no solid penetration, no fall-through, positions finite")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

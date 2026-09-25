from game import constants
from tests.support import makeWorld, settle
from game.sim.inputCommand import InputCommand


def arenaWorld(enemyChar):
    world = makeWorld([
        "                        ",
        "                        ",
        "  p                   %s " % enemyChar,
        "XXXXXXXXXXXXXXXXXXXXXXXX",
    ])
    settle(world, 2)
    return world


def placeInFront(world, enemy, gap):
    player = world.player
    enemy.y = player.bottom - enemy.h
    if player.facing > 0:
        enemy.x = player.right + gap
    else:
        enemy.x = player.left - gap - enemy.w


def swingSounds(world):
    return [event.name for event in world.audio.events].count("slash")


def test_attackDefeatsBeetleInFront():
    world = arenaWorld("b")
    beetle = world.enemies[0]
    placeInFront(world, beetle, 4)
    world.step(InputCommand(attack=True))
    assert not beetle.alive
    assert world.enemies == []
    assert world.player.hp == world.player.maxHp
    assert world.score == 100


def test_attackDefeatsChaserInOneSwing():
    world = arenaWorld("c")
    chaser = world.enemies[0]
    assert chaser.hp == 2
    placeInFront(world, chaser, 4)
    world.step(InputCommand(attack=True))
    assert not chaser.alive


def test_attackMissesEnemyBehind():
    world = arenaWorld("b")
    beetle = world.enemies[0]
    placeInFront(world, beetle, 4)
    world.player.facing = -1
    world.step(InputCommand(attack=True))
    assert beetle.alive


def test_attackMissesEnemyOutOfReach():
    world = arenaWorld("b")
    beetle = world.enemies[0]
    placeInFront(world, beetle, constants.attackReach + 6)
    world.step(InputCommand(attack=True))
    assert beetle.alive


def test_attackLeavesShooterAlive():
    world = arenaWorld("s")
    shooter = world.enemies[0]
    placeInFront(world, shooter, 2)
    world.step(InputCommand(attack=True))
    assert shooter.alive
    assert shooter.hp == 2


def test_attackNeedsTheFlag():
    world = arenaWorld("b")
    beetle = world.enemies[0]
    placeInFront(world, beetle, 4)
    world.step(InputCommand())
    assert beetle.alive
    assert not world.player.isAttacking()


def test_attackCooldownBlocksSecondSwing():
    world = arenaWorld("b")
    beetle = world.enemies[0]
    world.step(InputCommand(attack=True))
    assert swingSounds(world) == 1
    for _ in range(constants.attackFrames):
        world.step(InputCommand())
    assert not world.player.isAttacking()
    assert world.player.attackCooldown > 0

    placeInFront(world, beetle, 4)
    world.step(InputCommand(attack=True))
    assert beetle.alive
    assert swingSounds(world) == 1

    beetle.x = world.level.pixelWidth() - 2 * constants.tileSize
    while world.player.attackCooldown > 0:
        world.step(InputCommand())
    placeInFront(world, beetle, 4)
    world.step(InputCommand(attack=True))
    assert swingSounds(world) == 2
    assert not beetle.alive


def test_swingLastsAttackFrames():
    world = arenaWorld("b")
    world.step(InputCommand(attack=True))
    active = 0
    while world.player.isAttacking():
        active += 1
        world.step(InputCommand())
    assert active == constants.attackFrames

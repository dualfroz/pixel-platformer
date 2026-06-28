import pytest

from game import constants
from tests.support import makeWorld, settle
from game.sim.inputCommand import InputCommand


ledgeLevel = [
    "        ",
    "        ",
    " p      ",
    "XXX     ",
]

flatLevel = [
    " p      ",
    "        ",
    "XXXXXXXX",
]

wallLevel = [
    "    #",
    "    #",
    "    #",
    "    #",
    "XXXXX",
]


def walkOffLedge(world):
    for _ in range(40):
        world.step(InputCommand(right=True, run=True))
        if not world.player.onGround:
            return True
    return False


def test_coyoteJumpKeepsAirJump():
    world = makeWorld(ledgeLevel)
    assert walkOffLedge(world)
    world.step(InputCommand(right=True, jump=True, jumpHeld=True))
    player = world.player
    assert player.vy == pytest.approx(constants.jumpVelocity + constants.gravity)
    assert player.airJumps == constants.maxAirJumps


def test_afterCoyoteExpiresJumpIsDoubleJump():
    world = makeWorld(ledgeLevel)
    assert walkOffLedge(world)
    for _ in range(constants.coyoteFrames + 2):
        world.step(InputCommand())
    world.step(InputCommand(jump=True, jumpHeld=True))
    player = world.player
    assert player.airJumps == 0
    assert player.vy == pytest.approx(constants.doubleJumpVelocity + constants.gravity)


def test_doubleJumpConsumesAirJump():
    world = makeWorld(flatLevel)
    settle(world, 20)
    world.step(InputCommand(jump=True, jumpHeld=True))
    assert world.player.vy < 0
    assert world.player.airJumps == constants.maxAirJumps
    for _ in range(3):
        world.step(InputCommand(jumpHeld=True))
    world.step(InputCommand(jump=True, jumpHeld=True))
    assert world.player.airJumps == 0
    assert world.player.vy == pytest.approx(constants.doubleJumpVelocity + constants.gravity)


def test_jumpBufferFiresOnLanding():
    world = makeWorld(flatLevel)
    player = world.player
    player.airJumps = 0
    player.coyoteTimer = 0
    player.onGround = False
    player.y = 2 * constants.tileSize - player.h - 5.0
    world.step(InputCommand(jump=True))
    minVy = 0.0
    grounded = False
    for _ in range(14):
        world.step(InputCommand())
        grounded = grounded or world.player.onGround
        minVy = min(minVy, world.player.vy)
    assert grounded
    assert minVy == pytest.approx(constants.jumpVelocity + constants.gravity)


def test_noBufferNoRejump():
    world = makeWorld(flatLevel)
    player = world.player
    player.airJumps = 0
    player.coyoteTimer = 0
    player.onGround = False
    player.y = 2 * constants.tileSize - player.h - 5.0
    minVy = 0.0
    for _ in range(14):
        world.step(InputCommand())
        minVy = min(minVy, world.player.vy)
    assert minVy >= 0.0


def test_dashLaunchesAndCoolsDown():
    world = makeWorld(flatLevel)
    settle(world, 20)
    world.step(InputCommand(right=True, dash=True))
    player = world.player
    assert player.vx == pytest.approx(constants.dashSpeed)
    assert player.dashTimer == constants.dashFrames - 1
    assert player.vy == 0.0
    assert player.dashCooldown > 0


def test_wallSlideClampsFallSpeed():
    world = makeWorld(wallLevel)
    player = world.player
    player.x = 4 * constants.tileSize - player.w
    player.y = constants.tileSize
    player.vy = 5.0
    player.onGround = False
    world.step(InputCommand(right=True))
    assert player.wallSliding
    assert player.vy == pytest.approx(constants.wallSlideSpeed)


def test_noWallSlideWhenNotPressingIntoWall():
    world = makeWorld(wallLevel)
    player = world.player
    player.x = 4 * constants.tileSize - player.w
    player.y = constants.tileSize
    player.vy = 5.0
    player.onGround = False
    world.step(InputCommand(left=True))
    assert not player.wallSliding
    assert player.vy > constants.wallSlideSpeed


def test_wallJumpPushesAway():
    world = makeWorld(wallLevel)
    player = world.player
    player.x = 4 * constants.tileSize - player.w
    player.y = constants.tileSize
    player.vy = 2.0
    player.onGround = False
    world.step(InputCommand(right=True, jump=True, jumpHeld=True))
    assert player.vx == pytest.approx(-constants.wallJumpVelocityX)
    assert player.vy == pytest.approx(constants.wallJumpVelocityY + constants.gravity)


def test_variableJumpCutReducesRise():
    holdWorld = makeWorld(flatLevel)
    settle(holdWorld, 20)
    holdWorld.step(InputCommand(jump=True, jumpHeld=True))
    holdWorld.step(InputCommand(jumpHeld=True))
    holdVy = holdWorld.player.vy

    cutWorld = makeWorld(flatLevel)
    settle(cutWorld, 20)
    cutWorld.step(InputCommand(jump=True, jumpHeld=True))
    cutWorld.step(InputCommand(jumpHeld=False))
    cutVy = cutWorld.player.vy

    assert holdVy < -6.0
    assert cutVy > -4.0
    assert cutVy > holdVy

import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

pygame.init()
pygame.font.init()

from game.level import buildLevel, buildTestLevel
from game.world import World, MoveInput


def testLanding():
    world = World(buildLevel())
    startY = world.player.y
    startOnGround = world.player.onGround
    trail = []
    for _ in range(40):
        world.step(MoveInput())
        trail.append(world.player.y)
    endOnGround = world.player.onGround
    settleDelta = max(trail[-5:]) - min(trail[-5:])
    ok = (not startOnGround) and endOnGround and settleDelta < 0.5
    print(
        "landing: startAir=%s startY=%.1f endOnGround=%s endY=%.1f settleDelta=%.2f -> %s"
        % (not startOnGround, startY, endOnGround, trail[-1], settleDelta, "PASS" if ok else "FAIL")
    )
    return ok


def testWallBlocks():
    world = World(buildTestLevel())
    for _ in range(15):
        world.step(MoveInput())
    wallLeft = 5 * 16
    limit = wallLeft - world.player.width
    for _ in range(30):
        world.step(MoveInput(right=True))
    endX = world.player.x
    ok = endX <= limit + 0.01 and world.player.vx == 0.0
    print(
        "wallBlock: playerX=%.1f wallLeft=%d limit=%d vx=%.2f -> %s"
        % (endX, wallLeft, limit, world.player.vx, "PASS" if ok else "FAIL")
    )
    return ok


def testStomp():
    world = World(buildLevel())
    if not world.enemies:
        print("stomp: no enemies -> FAIL")
        return False
    enemy = world.enemies[0]
    enemy.alive = True
    world.player.x = enemy.x
    world.player.y = enemy.y - world.player.height + 5
    world.player.vy = 3.0
    world.resolveEnemies()
    ok = (not enemy.alive) and world.player.vy < 0 and world.score == 100
    print(
        "stomp: enemyAlive=%s bounceVy=%.2f score=%d -> %s"
        % (enemy.alive, world.player.vy, world.score, "PASS" if ok else "FAIL")
    )
    return ok


def testCoinPickup():
    world = World(buildLevel())
    coin = world.coins[0]
    world.player.x = coin.x
    world.player.y = coin.y
    world.resolveCoins()
    ok = coin.collected and world.coinCount == 1 and world.score == 200
    print(
        "coin: collected=%s coinCount=%d score=%d -> %s"
        % (coin.collected, world.coinCount, world.score, "PASS" if ok else "FAIL")
    )
    return ok


def main():
    results = [testLanding(), testWallBlocks(), testStomp(), testCoinPickup()]
    pygame.quit()
    allOk = all(results)
    print("ALL: %s" % ("PASS" if allOk else "FAIL"))
    sys.exit(0 if allOk else 1)


if __name__ == "__main__":
    main()

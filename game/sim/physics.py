import math

from ..constants import tileSize
from .geometry import Aabb

slopeStick = 6.0
groundProbe = 2.0


def bodyAabb(actor):
    return Aabb(actor.x, actor.y, actor.w, actor.h)


def cellRange(box):
    leftCol = int(math.floor(box.left / tileSize))
    rightCol = int(math.floor((box.right - 1e-6) / tileSize))
    topRow = int(math.floor(box.top / tileSize))
    bottomRow = int(math.floor((box.bottom - 1e-6) / tileSize))
    return leftCol, rightCol, topRow, bottomRow


def solidTilesOverlapping(terrain, box):
    leftCol, rightCol, topRow, bottomRow = cellRange(box)
    hits = []
    for row in range(topRow, bottomRow + 1):
        for col in range(leftCol, rightCol + 1):
            if terrain.solidAt(col, row):
                hits.append(terrain.rectFor(col, row))
    return hits


def oneWayTilesOverlapping(terrain, box):
    leftCol, rightCol, topRow, bottomRow = cellRange(box)
    hits = []
    for row in range(topRow, bottomRow + 1):
        for col in range(leftCol, rightCol + 1):
            if terrain.oneWayAt(col, row):
                hits.append(terrain.rectFor(col, row))
    return hits


def slopeSurfaceY(col, row, sampleX, kind):
    tileLeft = col * tileSize
    tileTop = row * tileSize
    localX = sampleX - tileLeft
    if localX < 0.0:
        localX = 0.0
    elif localX > tileSize:
        localX = float(tileSize)
    if kind == "ascendRight":
        return tileTop + (tileSize - localX)
    return tileTop + localX


def moveHorizontal(actor, terrain, platforms):
    actor.x += actor.vx
    box = bodyAabb(actor)
    actor.onWallLeft = False
    actor.onWallRight = False
    for tileBox in solidTilesOverlapping(terrain, box):
        if box.intersects(tileBox):
            if actor.vx > 0:
                actor.x = tileBox.left - actor.w
                actor.onWallRight = True
            elif actor.vx < 0:
                actor.x = tileBox.right
                actor.onWallLeft = True
            actor.vx = 0.0
            box = bodyAabb(actor)
    for platform in platforms:
        if platform.oneWay:
            continue
        platformBox = platform.aabb
        if box.intersects(platformBox):
            if actor.vx > 0:
                actor.x = platformBox.left - actor.w
                actor.onWallRight = True
            elif actor.vx < 0:
                actor.x = platformBox.right
                actor.onWallLeft = True
            actor.vx = 0.0
            box = bodyAabb(actor)


def moveVertical(actor, terrain, platforms, dropThrough=False):
    prevBottom = actor.y + actor.h
    actor.y += actor.vy
    box = bodyAabb(actor)
    actor.onGround = False
    actor.onCeiling = False
    actor.groundPlatform = None

    for tileBox in solidTilesOverlapping(terrain, box):
        if box.intersects(tileBox):
            if actor.vy > 0:
                actor.y = tileBox.top - actor.h
                actor.onGround = True
            elif actor.vy < 0:
                actor.y = tileBox.bottom
                actor.onCeiling = True
            actor.vy = 0.0
            box = bodyAabb(actor)

    if actor.vy >= 0 and not dropThrough:
        for tileBox in oneWayTilesOverlapping(terrain, box):
            top = tileBox.top
            if prevBottom <= top + 1.0 and box.bottom >= top and box.right > tileBox.left and box.left < tileBox.right:
                actor.y = top - actor.h
                actor.vy = 0.0
                actor.onGround = True
                box = bodyAabb(actor)

    for platform in platforms:
        platformBox = platform.aabb
        if platform.oneWay:
            if actor.vy >= 0 and not dropThrough:
                top = platformBox.top
                horizontal = box.right > platformBox.left and box.left < platformBox.right
                if prevBottom <= top + 1.0 and box.bottom >= top and horizontal:
                    actor.y = top - actor.h
                    actor.vy = 0.0
                    actor.onGround = True
                    actor.groundPlatform = platform
                    box = bodyAabb(actor)
        else:
            if box.intersects(platformBox):
                if actor.vy > 0:
                    actor.y = platformBox.top - actor.h
                    actor.onGround = True
                    actor.groundPlatform = platform
                elif actor.vy < 0:
                    actor.y = platformBox.bottom
                    actor.onCeiling = True
                actor.vy = 0.0
                box = bodyAabb(actor)


def resolveSlope(actor, terrain, wasOnGround):
    box = bodyAabb(actor)
    sampleX = box.centerX
    col = int(math.floor(sampleX / tileSize))
    topRow = int(math.floor((box.top - tileSize) / tileSize))
    bottomRow = int(math.floor((box.bottom + slopeStick) / tileSize))
    for row in range(topRow, bottomRow + 1):
        kind = terrain.slopeAt(col, row)
        if not kind:
            continue
        surfaceY = slopeSurfaceY(col, row, sampleX, kind)
        if surfaceY <= box.top:
            continue
        gap = surfaceY - box.bottom
        penetrating = gap <= 0.0 and gap >= -float(tileSize) - slopeStick
        clinging = wasOnGround and 0.0 < gap <= slopeStick
        if actor.vy >= 0.0 and (penetrating or clinging):
            actor.y = surfaceY - actor.h
            actor.vy = 0.0
            actor.onGround = True
            return True
    return False


def touchingSolidSide(actor, terrain, platforms, direction):
    probe = Aabb(
        actor.x + (actor.w if direction > 0 else -groundProbe),
        actor.y + 2.0,
        groundProbe,
        actor.h - 4.0,
    )
    for tileBox in solidTilesOverlapping(terrain, probe):
        if probe.intersects(tileBox):
            return True
    for platform in platforms:
        if platform.oneWay:
            continue
        if probe.intersects(platform.aabb):
            return True
    return False


def hasGroundBelow(actor, terrain, platforms):
    probe = Aabb(actor.x + 1.0, actor.y + actor.h, actor.w - 2.0, groundProbe)
    for tileBox in solidTilesOverlapping(terrain, probe):
        if probe.intersects(tileBox):
            return True
    for tileBox in oneWayTilesOverlapping(terrain, probe):
        if probe.intersects(tileBox):
            return True
    for platform in platforms:
        if probe.intersects(platform.aabb):
            return True
    return False


def overlapsLadder(actor, terrain):
    box = bodyAabb(actor)
    leftCol, rightCol, topRow, bottomRow = cellRange(box)
    for row in range(topRow, bottomRow + 1):
        for col in range(leftCol, rightCol + 1):
            if terrain.ladderAt(col, row):
                return True
    return False


def hazardOverlap(actor, terrain):
    box = bodyAabb(actor).inflated(-1.0, -1.0)
    leftCol, rightCol, topRow, bottomRow = cellRange(box)
    worstDamage = 0
    for row in range(topRow, bottomRow + 1):
        for col in range(leftCol, rightCol + 1):
            if terrain.hazardAt(col, row):
                worstDamage = max(worstDamage, terrain.hazardDamageAt(col, row))
    return worstDamage

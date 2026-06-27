import json
import os

from ..constants import tileSize
from .geometry import Aabb
from .tiles import (
    AIR,
    asciiToTile,
    tileToAscii,
    asciiEntities,
    tileRegistry,
)


class EntitySpawn:
    __slots__ = ("kind", "x", "y", "meta")

    def __init__(self, kind, x, y, meta=None):
        self.kind = kind
        self.x = float(x)
        self.y = float(y)
        self.meta = meta if meta is not None else {}

    def asDict(self):
        record = {"kind": self.kind, "x": self.x, "y": self.y}
        if self.meta:
            record["meta"] = self.meta
        return record


class PlatformSpawn:
    __slots__ = ("x", "y", "w", "h", "toX", "toY", "speed", "oneWay")

    def __init__(self, x, y, w, h, toX, toY, speed, oneWay=False):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.toX = float(toX)
        self.toY = float(toY)
        self.speed = float(speed)
        self.oneWay = bool(oneWay)

    def asDict(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "toX": self.toX,
            "toY": self.toY,
            "speed": self.speed,
            "oneWay": self.oneWay,
        }


class Level:
    def __init__(self, name, collision, background=None, foreground=None):
        self.name = name
        self.collision = collision
        self.rows = len(collision)
        self.cols = len(collision[0]) if collision else 0
        self.background = background
        self.foreground = foreground
        self.playerSpawn = (tileSize, tileSize)
        self.enemies = []
        self.items = []
        self.checkpoints = []
        self.platforms = []
        self.exit = None

    def pixelWidth(self):
        return self.cols * tileSize

    def pixelHeight(self):
        return self.rows * tileSize

    def inBounds(self, col, row):
        return 0 <= col < self.cols and 0 <= row < self.rows

    def tileNameAt(self, col, row):
        if row < 0 or row >= self.rows:
            return AIR
        if col < 0 or col >= self.cols:
            return AIR
        return self.collision[row][col]

    def defAt(self, col, row):
        return tileRegistry[self.tileNameAt(col, row)]

    def solidAt(self, col, row):
        if col < 0 or col >= self.cols:
            return True
        if row < 0 or row >= self.rows:
            return False
        return tileRegistry[self.collision[row][col]].solid

    def oneWayAt(self, col, row):
        return self.defAt(col, row).oneWay

    def hazardAt(self, col, row):
        return self.defAt(col, row).hazard

    def ladderAt(self, col, row):
        return self.defAt(col, row).ladder

    def slopeAt(self, col, row):
        return self.defAt(col, row).slope

    def hazardDamageAt(self, col, row):
        return self.defAt(col, row).damage

    def rectFor(self, col, row):
        return Aabb(col * tileSize, row * tileSize, tileSize, tileSize)

    def setTile(self, col, row, name):
        if self.inBounds(col, row):
            self.collision[row][col] = name

    def asDict(self):
        record = {
            "name": self.name,
            "tileSize": tileSize,
            "cols": self.cols,
            "rows": self.rows,
            "layers": {"collision": self.collision},
            "playerSpawn": list(self.playerSpawn),
            "enemies": [spawn.asDict() for spawn in self.enemies],
            "items": [spawn.asDict() for spawn in self.items],
            "checkpoints": [list(point) for point in self.checkpoints],
            "platforms": [platform.asDict() for platform in self.platforms],
            "exit": list(self.exit) if self.exit else None,
        }
        if self.background is not None:
            record["layers"]["background"] = self.background
        if self.foreground is not None:
            record["layers"]["foreground"] = self.foreground
        return record


def parseAscii(name, rows):
    width = max((len(row) for row in rows), default=0)
    padded = [row.ljust(width) for row in rows]
    collision = [[AIR for _ in range(width)] for _ in padded]
    level = Level(name, collision)
    for rowIndex, line in enumerate(padded):
        for colIndex, char in enumerate(line):
            if char in asciiToTile:
                collision[rowIndex][colIndex] = asciiToTile[char]
            elif char in asciiEntities:
                kind = asciiEntities[char]
                px = colIndex * tileSize
                py = rowIndex * tileSize
                if kind == "playerSpawn":
                    level.playerSpawn = (px, py)
                elif kind == "checkpoint":
                    level.checkpoints.append((px, py))
                elif kind == "exit":
                    level.exit = (px, py)
                elif kind in ("coin", "gem", "key", "heart"):
                    level.items.append(EntitySpawn(kind, px, py))
                else:
                    level.enemies.append(EntitySpawn(kind, px, py))
    if level.exit is None and level.checkpoints:
        level.exit = level.checkpoints[-1]
    return level


def levelToAscii(level):
    lines = []
    entityAt = {}
    for spawn in level.enemies + level.items:
        col = int(round(spawn.x / tileSize))
        row = int(round(spawn.y / tileSize))
        entityAt[(col, row)] = spawn.kind
    spx, spy = level.playerSpawn
    entityAt[(int(round(spx / tileSize)), int(round(spy / tileSize)))] = "playerSpawn"
    for point in level.checkpoints:
        entityAt[(int(round(point[0] / tileSize)), int(round(point[1] / tileSize)))] = "checkpoint"
    if level.exit:
        entityAt[(int(round(level.exit[0] / tileSize)), int(round(level.exit[1] / tileSize)))] = "exit"
    kindToChar = {value: key for key, value in asciiEntities.items()}
    for rowIndex in range(level.rows):
        chars = []
        for colIndex in range(level.cols):
            key = (colIndex, rowIndex)
            name = level.collision[rowIndex][colIndex]
            if name != AIR:
                chars.append(tileToAscii.get(name, "?"))
            elif key in entityAt:
                chars.append(kindToChar[entityAt[key]])
            else:
                chars.append(" ")
        lines.append("".join(chars).rstrip())
    return lines


def levelFromDict(record):
    collision = record["layers"]["collision"]
    background = record["layers"].get("background")
    foreground = record["layers"].get("foreground")
    level = Level(record.get("name", "unnamed"), collision, background, foreground)
    level.playerSpawn = tuple(record.get("playerSpawn", (tileSize, tileSize)))
    for enemy in record.get("enemies", []):
        level.enemies.append(EntitySpawn(enemy["kind"], enemy["x"], enemy["y"], enemy.get("meta")))
    for item in record.get("items", []):
        level.items.append(EntitySpawn(item["kind"], item["x"], item["y"], item.get("meta")))
    level.checkpoints = [tuple(point) for point in record.get("checkpoints", [])]
    for platform in record.get("platforms", []):
        level.platforms.append(
            PlatformSpawn(
                platform["x"],
                platform["y"],
                platform["w"],
                platform["h"],
                platform["toX"],
                platform["toY"],
                platform["speed"],
                platform.get("oneWay", False),
            )
        )
    exitPoint = record.get("exit")
    level.exit = tuple(exitPoint) if exitPoint else None
    return level


def saveLevelJson(level, path):
    with open(path, "w", encoding="ascii") as handle:
        json.dump(level.asDict(), handle, indent=2)


def loadLevelJson(path):
    with open(path, "r", encoding="ascii") as handle:
        record = json.load(handle)
    return levelFromDict(record)


def loadLevel(source):
    if isinstance(source, Level):
        return source
    if isinstance(source, dict):
        return levelFromDict(source)
    if isinstance(source, (list, tuple)):
        return parseAscii("ascii", list(source))
    if isinstance(source, str) and os.path.isfile(source):
        return loadLevelJson(source)
    raise ValueError("unsupported level source: %r" % (source,))

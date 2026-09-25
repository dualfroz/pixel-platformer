from .geometry import Aabb


class DoorSpawn:
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

    def asDict(self):
        return {"x": self.x, "y": self.y, "w": self.w, "h": self.h}


class Door:
    oneWay = False

    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.open = False

    @property
    def aabb(self):
        return Aabb(self.x, self.y, self.w, self.h)

    @classmethod
    def fromSpawn(cls, spawn):
        return cls(spawn.x, spawn.y, spawn.w, spawn.h)


def mergeDoorCells(cells, tileSize):
    spawns = []
    for col, row in sorted(cells):
        last = spawns[-1] if spawns else None
        if last is not None and last.x == col * tileSize and last.y + last.h == row * tileSize:
            last.h += tileSize
        else:
            spawns.append(DoorSpawn(col * tileSize, row * tileSize, tileSize, tileSize))
    return spawns

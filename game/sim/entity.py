import itertools

from .geometry import Aabb

_idCounter = itertools.count(1)


class Actor:
    def __init__(self, x, y, w, h):
        self.id = next(_idCounter)
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 1
        self.onGround = False
        self.onCeiling = False
        self.onWallLeft = False
        self.onWallRight = False
        self.groundPlatform = None
        self.alive = True
        self.removed = False

    @property
    def aabb(self):
        return Aabb(self.x, self.y, self.w, self.h)

    @property
    def centerX(self):
        return self.x + self.w * 0.5

    @property
    def centerY(self):
        return self.y + self.h * 0.5

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    def hurtBox(self):
        return self.aabb

    def kill(self):
        self.alive = False

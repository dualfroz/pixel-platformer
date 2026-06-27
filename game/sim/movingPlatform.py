from .geometry import Aabb


class MovingPlatform:
    def __init__(self, x, y, w, h, toX, toY, speed, oneWay=False):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.fromX = float(x)
        self.fromY = float(y)
        self.toX = float(toX)
        self.toY = float(toY)
        self.speed = float(speed)
        self.oneWay = bool(oneWay)
        self.progress = 0.0
        self.direction = 1
        self.deltaX = 0.0
        self.deltaY = 0.0

    @property
    def aabb(self):
        return Aabb(self.x, self.y, self.w, self.h)

    def spanLength(self):
        dx = self.toX - self.fromX
        dy = self.toY - self.fromY
        return (dx * dx + dy * dy) ** 0.5

    def update(self):
        span = self.spanLength()
        prevX = self.x
        prevY = self.y
        if span == 0.0:
            self.deltaX = 0.0
            self.deltaY = 0.0
            return
        step = self.speed / span
        self.progress += step * self.direction
        if self.progress >= 1.0:
            self.progress = 1.0
            self.direction = -1
        elif self.progress <= 0.0:
            self.progress = 0.0
            self.direction = 1
        self.x = self.fromX + (self.toX - self.fromX) * self.progress
        self.y = self.fromY + (self.toY - self.fromY) * self.progress
        self.deltaX = self.x - prevX
        self.deltaY = self.y - prevY

    @classmethod
    def fromSpawn(cls, spawn):
        return cls(spawn.x, spawn.y, spawn.w, spawn.h, spawn.toX, spawn.toY, spawn.speed, spawn.oneWay)

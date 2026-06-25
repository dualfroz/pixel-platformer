import math


class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def copy(self):
        return Vec2(self.x, self.y)

    def set(self, x, y):
        self.x = float(x)
        self.y = float(y)
        return self

    def add(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def scale(self, factor):
        return Vec2(self.x * factor, self.y * factor)

    def length(self):
        return math.hypot(self.x, self.y)

    def lengthSq(self):
        return self.x * self.x + self.y * self.y

    def normalized(self):
        mag = self.length()
        if mag == 0.0:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / mag, self.y / mag)

    def distanceTo(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def asTuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return "Vec2(%.3f, %.3f)" % (self.x, self.y)


class Aabb:
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

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

    @property
    def centerX(self):
        return self.x + self.w * 0.5

    @property
    def centerY(self):
        return self.y + self.h * 0.5

    @property
    def center(self):
        return Vec2(self.centerX, self.centerY)

    def copy(self):
        return Aabb(self.x, self.y, self.w, self.h)

    def moved(self, dx, dy):
        return Aabb(self.x + dx, self.y + dy, self.w, self.h)

    def intersects(self, other):
        return (
            self.left < other.right
            and self.right > other.left
            and self.top < other.bottom
            and self.bottom > other.top
        )

    def touches(self, other):
        return (
            self.left <= other.right
            and self.right >= other.left
            and self.top <= other.bottom
            and self.bottom >= other.top
        )

    def containsPoint(self, px, py):
        return self.left <= px <= self.right and self.top <= py <= self.bottom

    def overlapArea(self, other):
        overlapX = min(self.right, other.right) - max(self.left, other.left)
        overlapY = min(self.bottom, other.bottom) - max(self.top, other.top)
        if overlapX <= 0.0 or overlapY <= 0.0:
            return 0.0
        return overlapX * overlapY

    def inflated(self, marginX, marginY):
        return Aabb(
            self.x - marginX,
            self.y - marginY,
            self.w + marginX * 2.0,
            self.h + marginY * 2.0,
        )

    def asTuple(self):
        return (self.x, self.y, self.w, self.h)

    def asIntRect(self):
        return (int(self.x), int(self.y), int(self.w), int(self.h))

    def __repr__(self):
        return "Aabb(%.2f, %.2f, %.2f, %.2f)" % (self.x, self.y, self.w, self.h)


def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def sign(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def approach(current, target, delta):
    if current < target:
        return min(current + delta, target)
    return max(current - delta, target)

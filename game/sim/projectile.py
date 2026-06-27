from .. import constants
from .entity import Actor
from . import physics


class Projectile(Actor):
    def __init__(self, x, y, vx, vy, owner="enemy", damage=1):
        super().__init__(x, y, 6, 6)
        self.vx = vx
        self.vy = vy
        self.owner = owner
        self.damage = damage
        self.life = constants.projectileLife
        self.gravityScale = 0.0

    def update(self, world):
        self.life -= 1
        if self.life <= 0:
            self.alive = False
            return
        if self.gravityScale:
            self.vy += constants.gravity * self.gravityScale
        self.x += self.vx
        self.y += self.vy
        box = self.aabb
        for tileBox in physics.solidTilesOverlapping(world.level, box):
            if box.intersects(tileBox):
                self.alive = False
                world.spawnBurst("spark", self.centerX, self.centerY, 4)
                return
        if self.centerX < -32 or self.centerX > world.level.pixelWidth() + 32:
            self.alive = False

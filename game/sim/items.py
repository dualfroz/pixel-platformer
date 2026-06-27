from ..constants import tileSize
from .geometry import Aabb

itemDefs = {
    "coin": {"score": 100, "size": 12, "bob": True},
    "gem": {"score": 500, "size": 12, "bob": True},
    "key": {"score": 50, "size": 12, "bob": False},
    "heart": {"score": 0, "size": 14, "bob": True, "heal": 2},
}


class Collectible:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = float(x)
        self.y = float(y)
        self.collected = False
        definition = itemDefs.get(kind, itemDefs["coin"])
        self.size = definition["size"]
        self.score = definition["score"]
        self.heal = definition.get("heal", 0)
        self.bob = definition.get("bob", False)
        self.bobPhase = 0.0

    @property
    def aabb(self):
        pad = (tileSize - self.size) * 0.5
        return Aabb(self.x + pad, self.y + pad, self.size, self.size)

    def update(self):
        if self.bob:
            self.bobPhase = (self.bobPhase + 0.15) % 6.2831853

    def collect(self, player, world):
        if self.collected:
            return
        self.collected = True
        player.score += self.score
        world.score += self.score
        if self.kind == "coin":
            player.coins += 1
            world.coins += 1
        elif self.heal:
            player.heal(self.heal)
        player.inventory.add(self.kind)
        world.playSound("pickup", self.x)
        world.spawnBurst("pickup", self.x + tileSize * 0.5, self.y + tileSize * 0.5, 5)

    @classmethod
    def fromSpawn(cls, spawn):
        return cls(spawn.kind, spawn.x, spawn.y)

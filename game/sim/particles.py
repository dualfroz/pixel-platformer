import math
import random

particlePresets = {
    "jump": {"count": 4, "color": (230, 230, 230), "life": 16, "spread": 1.2, "gravity": 0.1, "up": -0.5},
    "dash": {"count": 6, "color": (120, 200, 255), "life": 14, "spread": 1.6, "gravity": 0.0, "up": 0.0},
    "stomp": {"count": 6, "color": (200, 120, 60), "life": 18, "spread": 2.0, "gravity": 0.2, "up": -1.0},
    "pickup": {"count": 5, "color": (247, 213, 29), "life": 20, "spread": 1.4, "gravity": -0.05, "up": -1.2},
    "hurt": {"count": 8, "color": (220, 40, 40), "life": 22, "spread": 2.2, "gravity": 0.15, "up": -1.5},
    "spark": {"count": 4, "color": (255, 220, 120), "life": 10, "spread": 2.4, "gravity": 0.0, "up": 0.0},
    "alert": {"count": 3, "color": (255, 80, 80), "life": 16, "spread": 0.6, "gravity": -0.1, "up": -1.4},
    "dust": {"count": 3, "color": (200, 190, 160), "life": 12, "spread": 1.0, "gravity": 0.05, "up": -0.2},
}


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "maxLife", "color", "gravity", "size")

    def __init__(self, x, y, vx, vy, life, color, gravity, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.maxLife = life
        self.color = color
        self.gravity = gravity
        self.size = size

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    @property
    def fade(self):
        return max(0.0, self.life / self.maxLife)


class ParticleSystem:
    def __init__(self, rng=None, cap=512):
        self.particles = []
        self.rng = rng if rng is not None else random.Random(1234)
        self.cap = cap

    def emit(self, preset, x, y, count=None):
        config = particlePresets.get(preset, particlePresets["dust"])
        emitCount = count if count is not None else config["count"]
        for _ in range(emitCount):
            if len(self.particles) >= self.cap:
                break
            angle = self.rng.uniform(0, math.tau)
            magnitude = self.rng.uniform(0.2, config["spread"])
            vx = math.cos(angle) * magnitude
            vy = math.sin(angle) * magnitude + config["up"]
            life = int(config["life"] * self.rng.uniform(0.7, 1.1))
            size = self.rng.randint(1, 2)
            self.particles.append(Particle(x, y, vx, vy, life, config["color"], config["gravity"], size))

    def update(self):
        survivors = []
        for particle in self.particles:
            particle.update()
            if particle.alive:
                survivors.append(particle)
        self.particles = survivors

    def clear(self):
        self.particles = []

    def __len__(self):
        return len(self.particles)

import pytest

from game.sim import physics
from game.sim.entity import Actor


class FakeSlopeTerrain:
    def __init__(self, slopes):
        self.slopes = slopes

    def slopeAt(self, col, row):
        return self.slopes.get((col, row))


def test_slopeSurfaceAscendRight():
    assert physics.slopeSurfaceY(0, 0, 0, "ascendRight") == pytest.approx(16.0)
    assert physics.slopeSurfaceY(0, 0, 16, "ascendRight") == pytest.approx(0.0)
    assert physics.slopeSurfaceY(0, 0, 8, "ascendRight") == pytest.approx(8.0)


def test_slopeSurfaceAscendLeft():
    assert physics.slopeSurfaceY(0, 0, 0, "ascendLeft") == pytest.approx(0.0)
    assert physics.slopeSurfaceY(0, 0, 16, "ascendLeft") == pytest.approx(16.0)


def test_resolveSlopeSnapsPenetratingActor():
    terrain = FakeSlopeTerrain({(0, 0): "ascendRight"})
    actor = Actor(2, -6, 12, 16)
    actor.vy = 1.0
    snapped = physics.resolveSlope(actor, terrain, wasOnGround=False)
    assert snapped
    assert actor.onGround
    assert actor.bottom == pytest.approx(physics.slopeSurfaceY(0, 0, actor.centerX, "ascendRight"))
    assert actor.vy == 0.0


def test_walkingUpSlopeGainsHeight():
    terrain = FakeSlopeTerrain({(0, 0): "ascendRight"})
    actor = Actor(0, 0, 12, 16)
    actor.vy = 1.0
    physics.resolveSlope(actor, terrain, wasOnGround=False)
    lowBottom = actor.bottom
    actor.x = 6
    actor.vy = 1.0
    physics.resolveSlope(actor, terrain, wasOnGround=True)
    assert actor.bottom < lowBottom


def test_resolveSlopeClingsWhenDescending():
    terrain = FakeSlopeTerrain({(0, 0): "ascendLeft"})
    actor = Actor(2, 0, 12, 16)
    surface = physics.slopeSurfaceY(0, 0, actor.centerX, "ascendLeft")
    actor.y = surface - actor.h - 3.0
    actor.vy = 0.5
    snapped = physics.resolveSlope(actor, terrain, wasOnGround=True)
    assert snapped
    assert actor.onGround
    assert actor.bottom == pytest.approx(surface)

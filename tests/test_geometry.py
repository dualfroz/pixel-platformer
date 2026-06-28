import pytest

from game.sim.geometry import Vec2, Aabb, clamp, sign, approach


def test_aabbIntersectsOverlapping():
    a = Aabb(0, 0, 10, 10)
    b = Aabb(5, 5, 10, 10)
    assert a.intersects(b)
    assert b.intersects(a)


def test_aabbDoesNotIntersectSeparated():
    a = Aabb(0, 0, 10, 10)
    b = Aabb(20, 0, 10, 10)
    assert not a.intersects(b)


def test_aabbTouchingEdgeIsNotOverlap():
    a = Aabb(0, 0, 10, 10)
    b = Aabb(10, 0, 10, 10)
    assert not a.intersects(b)
    assert a.touches(b)


def test_aabbOverlapArea():
    a = Aabb(0, 0, 10, 10)
    b = Aabb(5, 5, 10, 10)
    assert a.overlapArea(b) == pytest.approx(25.0)
    assert a.overlapArea(Aabb(100, 100, 5, 5)) == 0.0


def test_aabbContainsAndEdges():
    box = Aabb(4, 6, 8, 10)
    assert box.left == 4 and box.right == 12
    assert box.top == 6 and box.bottom == 16
    assert box.centerX == pytest.approx(8.0)
    assert box.containsPoint(8, 10)
    assert not box.containsPoint(100, 10)


def test_aabbInflated():
    box = Aabb(10, 10, 4, 4)
    grown = box.inflated(2, 3)
    assert grown.left == 8 and grown.right == 16
    assert grown.top == 7 and grown.bottom == 17


def test_vecArithmetic():
    a = Vec2(3, 4)
    assert a.length() == pytest.approx(5.0)
    assert a.add(Vec2(1, 1)).asTuple() == (4.0, 5.0)
    assert a.sub(Vec2(3, 4)).asTuple() == (0.0, 0.0)
    assert a.scale(2).asTuple() == (6.0, 8.0)
    normalized = a.normalized()
    assert normalized.length() == pytest.approx(1.0)


def test_vecDistanceAndZeroNormalize():
    assert Vec2(0, 0).distanceTo(Vec2(3, 4)) == pytest.approx(5.0)
    assert Vec2(0, 0).normalized().asTuple() == (0.0, 0.0)


def test_helpers():
    assert clamp(5, 0, 3) == 3
    assert clamp(-1, 0, 3) == 0
    assert clamp(2, 0, 3) == 2
    assert sign(-4) == -1 and sign(4) == 1 and sign(0) == 0
    assert approach(0, 10, 3) == 3
    assert approach(10, 0, 3) == 7
    assert approach(1, 2, 5) == 2

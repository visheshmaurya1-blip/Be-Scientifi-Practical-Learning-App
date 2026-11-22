import pytest
from bescientific.labs.models import GravityModel, FrictionModel, BounceModel, MODELS


def test_gravity_heavy_and_light_land_together():
    r = GravityModel().run_to_completion()
    assert r["heavy"] is not None and r["light"] is not None
    assert abs(r["heavy"] - r["light"]) < 0.05          # equal fall time without air


def test_gravity_higher_drop_takes_longer():
    low, high = GravityModel(), GravityModel()
    low.set_param("height", 100.0)
    high.set_param("height", 300.0)
    assert high.run_to_completion()["heavy"] > low.run_to_completion()["heavy"]


def test_friction_ordering_ice_wood_rough():
    d = {}
    for s in ("ice", "wood", "rough"):
        m = FrictionModel()
        m.set_param("surface", s)
        d[s] = m.run_to_completion()["distance"]
    assert d["ice"] > d["wood"] > d["rough"]
    assert d["rough"] < 5.0                              # grips: effectively does not slide


def test_bounce_height_grows_with_elasticity():
    h = {}
    for e in (0.0, 0.4, 0.9):
        m = BounceModel()
        m.set_param("elasticity", e)
        h[e] = m.run_to_completion()["bounce_height"]
    assert h[0.0] < 5.0 < h[0.4] < h[0.9]
    assert h[0.9] < 300.0 + 1.0                           # never above the drop height


def test_models_are_resettable_and_expose_shapes():
    for name, cls in MODELS.items():
        m = cls()
        assert m.shapes()
        m.run_to_completion()
        assert m.finished
        m.reset()
        assert not m.finished and m.t == 0.0

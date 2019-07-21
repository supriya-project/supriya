import pickle

import supriya


def test_01():
    old_session = supriya.Session()
    new_session = pickle.loads(pickle.dumps(old_session))
    old_bundles = old_session.to_osc_bundles()
    new_bundles = new_session.to_osc_bundles()
    assert old_bundles == new_bundles


def test_02():
    old_session = supriya.Session()
    group = old_session.add_group(offset=5)
    group.add_synth(offset=10, duration=10)
    new_session = pickle.loads(pickle.dumps(old_session))
    old_bundles = old_session.to_osc_bundles()
    new_bundles = new_session.to_osc_bundles()
    assert old_bundles == new_bundles

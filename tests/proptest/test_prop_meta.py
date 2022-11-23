from dataclasses import dataclass

import hypothesis
import hypothesis.strategies as st

from tests.proptest import get_control_test_groups, hp_global_settings

hp_settings = hypothesis.settings(hp_global_settings)


@dataclass
class SampleMeta:

    val_bool: bool
    val_int: int
    val_float: float = 0.0
    val_text: str = ""


@st.composite
def st_test_strategy(draw) -> SampleMeta:

    sample = SampleMeta(draw(st.booleans()), draw(st.integers()))

    sample.val_float = draw(st.floats(allow_infinity=False, allow_nan=False))
    sample.val_text = draw(st.text())

    return sample


@get_control_test_groups()
@st.composite
def st_test_strategy_control_group(draw) -> SampleMeta:

    sample = SampleMeta(draw(st.booleans()), draw(st.integers()))

    sample.val_float = draw(st.floats(allow_infinity=False, allow_nan=False))
    sample.val_text = draw(st.text())

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(sample=st_test_strategy())
def test_composite_strategy_01(sample):

    assert isinstance(sample, SampleMeta)
    assert isinstance(sample.val_bool, bool)
    assert isinstance(sample.val_int, int)
    assert isinstance(sample.val_float, float)
    assert isinstance(sample.val_text, str)


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_test_strategy_control_group())
def test_composite_strategy_02(strategy):

    assert isinstance(strategy, tuple)
    assert len(strategy) == 2
    control, test = strategy
    assert isinstance(control, list)
    assert isinstance(test, list)
    assert len(control) >= 1
    assert len(test) >= 1
    assert all(isinstance(_, SampleMeta) for _ in control + test)
    assert all(isinstance(_.val_bool, bool) for _ in control + test)
    assert all(isinstance(_.val_int, int) for _ in control + test)
    assert all(isinstance(_.val_float, float) for _ in control + test)
    assert all(isinstance(_.val_text, str) for _ in control + test)

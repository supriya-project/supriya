import pytest

from supriya.mixers import Session
from supriya.mixers.mixers import Mixer


@pytest.fixture
def session() -> Session:
    return Session()


@pytest.fixture
def mixer(session: Session) -> Mixer:
    return session.mixers[0]

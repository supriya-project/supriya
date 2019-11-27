from supriya.xdaw import Application


def test_1():
    application = Application()
    assert len(application.contexts) == 0
    assert application.status == Application.Status.OFFLINE

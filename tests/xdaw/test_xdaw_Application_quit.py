from supriya.xdaw import Application


def test_1():
    application = Application.new()
    application.boot()
    application.quit()
    assert application.status == Application.Status.OFFLINE
    assert application.primary_context.provider is None

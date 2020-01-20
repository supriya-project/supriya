from supriya.xdaw import Application, Context


def test_1():
    """
    Add one context
    """
    application = Application()
    context = application.add_context()
    assert isinstance(context, Context)
    assert list(application.contexts) == [context]
    assert context.application is application
    assert context.graph_order == (3, 0)
    assert context.parent is application.contexts
    assert context.provider is None


def test_2():
    """
    Add two contexts
    """
    application = Application()
    context_one = application.add_context()
    context_two = application.add_context()
    assert list(application.contexts) == [context_one, context_two]
    assert context_one.application is application
    assert context_one.graph_order == (3, 0)
    assert context_one.parent is application.contexts
    assert context_one.provider is None
    assert context_two.application is application
    assert context_two.graph_order == (3, 1)
    assert context_two.parent is application.contexts
    assert context_two.provider is None


def test_3():
    """
    Add one context, boot, add second context
    """
    application = Application()
    context_one = application.add_context()
    application.boot()
    context_two = application.add_context()
    assert list(application.contexts) == [context_one, context_two]
    assert context_one.graph_order == (3, 0)
    assert context_one.parent is application.contexts
    assert context_one.provider is not None
    assert context_one.provider.server.is_running
    assert context_two.graph_order == (3, 1)
    assert context_two.parent is application.contexts
    assert context_two.provider is not None
    assert context_two.provider.server.is_running
    assert context_one.provider is not context_two.provider

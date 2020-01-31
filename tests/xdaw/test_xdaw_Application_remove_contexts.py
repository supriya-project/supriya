from supriya.xdaw import Application


def test_1():
    """
    Remove one context
    """
    application = Application()
    context = application.add_context()
    application.remove_contexts(context)
    assert list(application.contexts) == []
    assert context.application is None
    assert context.graph_order == ()
    assert context.parent is None
    assert context.provider is None


def test_2():
    """
    Remove two contexts
    """
    application = Application()
    context_one = application.add_context()
    context_two = application.add_context()
    application.remove_contexts(context_one, context_two)
    assert list(application.contexts) == []
    assert context_one.application is None
    assert context_one.graph_order == ()
    assert context_one.parent is None
    assert context_one.provider is None
    assert context_two.application is None
    assert context_two.graph_order == ()
    assert context_two.parent is None
    assert context_two.provider is None


def test_3():
    """
    Remove first context, leaving second untouched
    """
    application = Application()
    context_one = application.add_context()
    context_two = application.add_context()
    application.remove_contexts(context_one)
    assert list(application.contexts) == [context_two]
    assert context_one.application is None
    assert context_one.graph_order == ()
    assert context_one.parent is None
    assert context_one.provider is None
    assert context_two.application is application
    assert context_two.graph_order == (3, 0)
    assert context_two.parent is application.contexts
    assert context_two.provider is None


def test_4():
    """
    Boot, remove first context, leaving second untouched
    """
    application = Application()
    context_one = application.add_context()
    context_two = application.add_context()
    application.boot()
    provider_one = context_one.provider
    provider_two = context_two.provider
    application.remove_contexts(context_one)
    assert list(application.contexts) == [context_two]
    assert context_one.application is None
    assert context_one.graph_order == ()
    assert context_one.parent is None
    assert context_one.provider is None
    assert context_two.application is application
    assert context_two.graph_order == (3, 0)
    assert context_two.parent is application.contexts
    assert context_two.provider is not None
    assert not provider_one.server.is_running
    assert provider_two.server.is_running

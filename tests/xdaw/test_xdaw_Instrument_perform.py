from supriya.xdaw import Application, Instrument


def application():
    application = Application()
    context = application.add_context(name="Context")
    context.add_track(name="Track")
    application.boot()
    yield application
    application.quit()


def test_1():
    application.boot()
    track = application.primary_context["Track"]
    instrument = track.add_device(Instrument, synthdef=dc_instrument_synthdef_factory)

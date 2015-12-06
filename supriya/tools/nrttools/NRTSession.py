class NRTSession(object):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def get_group(self):
        from supriya.tools import nrttools
        node = nrttools.NRTGroup(nrtid=nrt_id)

    def get_synth(self, synthdef, **kwargs):
        from supriya.tools import nrttools
        node = nrttools.NRTSynth(nrt_id=nrt_id, synthdef=synthdef, **kwargs)


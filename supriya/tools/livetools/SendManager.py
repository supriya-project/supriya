from supriya.tools.livetools.Send import Send


class SendManager:

    ### INITIALIZER ###

    def __init__(self, track):
        self._track = track

    ### SPECIAL METHODS ###

    def __call__(self, track_name, initial_gain=0.):
        if track_name in self.track._outgoing_sends:
            send = self.track._outgoing_sends[track_name]
            send(initial_gain)
            return send
        source_track = self._track
        target_track = self._track.mixer[track_name]
        send = Send(
            source_track,
            target_track,
            initial_gain=initial_gain,
            )
        source_track._outgoing_sends[track_name] = send
        target_track._incoming_sends[source_track.name] = send
        if self.mixer.is_allocated:
            send._allocate()
        return send

    def __getitem__(self, target_track_name):
        return self.track._outgoing_sends[target_track_name]

    def __setitem__(self, target_track_name, gain):
        self(target_track_name, gain)

    ### PUBLIC PROPERTIES ###

    @property
    def mixer(self):
        return self.track.mixer

    @property
    def track(self):
        return self._track

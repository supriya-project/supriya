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
        return self.track.add_send(track_name, initial_gain=initial_gain)

    def __getitem__(self, target_track_name):
        return self.track._outgoing_sends[target_track_name]

    def __iter__(self):
        return iter(self.track._outgoing_sends)

    def __len__(self):
        return len(self.track._outgoing_sends)

    def __setitem__(self, target_track_name, gain):
        self(target_track_name, gain)

    ### PUBLIC PROPERTIES ###

    @property
    def mixer(self):
        return self.track.mixer

    @property
    def track(self):
        return self._track

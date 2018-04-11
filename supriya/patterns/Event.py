import abc
import collections
import uuid
import supriya.utils
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Event(SupriyaValueObject):
    """
    An abstract event.

    ::

        >>> supriya.patterns.NoteEvent(
        ...     amplitude=0.9,
        ...     duration=10.5,
        ...     frequency=443,
        ...     panning=0.75,
        ...     )
        NoteEvent(
            amplitude=0.9,
            delta=10.5,
            duration=10.5,
            frequency=443,
            panning=0.75,
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_delta',
        '_settings',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        delta=None,
        **settings
        ):
        self._delta = delta
        self._settings = {
            key: value for key, value in settings.items()
            if not (key.startswith('_') and value is None)
        }

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._settings.__getitem__(item)

    ### PRIVATE METHODS ###

    def _expand(
        self,
        settings,
        synthdef,
        uuids,
        realtime=True,
        synth_parameters_only=False,
        ):
        settings = settings.copy()
        for key, value in settings.items():
            if isinstance(value, uuid.UUID) and value in uuids:
                value = uuids[value]
                if isinstance(value, dict):
                    value = sorted(value)[0]
                if not isinstance(value, collections.Sequence):
                    value = [value]
                settings[key] = value
        maximum_length = 1
        unexpanded_settings = {}
        for key, value in settings.items():
            if isinstance(value, collections.Sequence):
                maximum_length = max(len(value), maximum_length)
                unexpanded_settings[key] = value
            else:
                unexpanded_settings[key] = [value]
        expanded_settings = []
        for i in range(maximum_length):
            settings = {}
            for key, value in unexpanded_settings.items():
                settings[key] = value[i % len(value)]
            expanded_settings.append(settings)
        if synth_parameters_only:
            for i, dictionary in enumerate(expanded_settings):
                expanded_settings[i] = {
                    key: value for key, value in dictionary.items()
                    if key in synthdef.parameter_names
                    }
        return expanded_settings

    @abc.abstractmethod
    def _perform_nonrealtime(
        self,
        session,
        uuids,
        offset,
        ):
        raise NotImplementedError

    @abc.abstractmethod
    def _perform_realtime(
        self,
        index=0,
        node_id_allocator=None,
        timestamp=0,
        uuids=None,
        ):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def as_dict(self):
        _, _, kwargs = supriya.utils.get_object_vars(self)
        return kwargs

    def get(self, item, default=None):
        return self._settings.get(item, default)

    ### PUBLIC PROPERTIES ###

    @property
    def delta(self):
        if self._delta is None:
            return self.get('duration')
        return self._delta

    @property
    def settings(self):
        return self._settings

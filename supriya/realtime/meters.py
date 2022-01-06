import supriya.system
from supriya import utils
from supriya.system import SupriyaObject


class Meters(SupriyaObject):
    """
    Server meters.

    ::

        >>> import json, supriya, time
        >>> server = supriya.Server().boot(
        ...     input_bus_channel_count=2,
        ...     output_bus_channel_count=2,
        ... )
        >>> meters = server.meters.allocate()
        >>> time.sleep(1)
        >>> print(json.dumps(meters.to_dict(), indent=4))
        {
            "server_meters": {
                "input_meter_levels": [
                    {
                        "peak": ...,
                        "rms": ...
                    },
                    {
                        "peak": ...,
                        "rms": ...
                    }
                ],
                "output_meter_levels": [
                    {
                        "peak": 0.0,
                        "rms": 0.0
                    },
                    {
                        "peak": 0.0,
                        "rms": 0.0
                    }
                ]
            }
        }

    ::

        >>> meters.free()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_input_meter_callback",
        "_input_meter_peak_levels",
        "_input_meter_rms_levels",
        "_input_meter_synth",
        "_output_meter_callback",
        "_output_meter_peak_levels",
        "_output_meter_rms_levels",
        "_output_meter_synth",
        "_server",
    )

    ### INITIALIZER ###

    def __init__(self, server):
        self._server = server
        self._input_meter_callback = None
        self._input_meter_peak_levels = None
        self._input_meter_rms_levels = None
        self._input_meter_synth = None
        self._output_meter_callback = None
        self._output_meter_peak_levels = None
        self._output_meter_rms_levels = None
        self._output_meter_synth = None

    ### PRIVATE METHODS ###

    def _handle_input_levels(self, message):
        contents = message.contents[2:]
        peak_levels = []
        rms_levels = []
        for peak, rms in utils.group_iterable_by_count(contents, 2):
            peak_levels.append(peak)
            rms_levels.append(rms)
        self._input_meter_peak_levels = tuple(peak_levels)
        self._input_meter_rms_levels = tuple(rms_levels)

    def _handle_output_levels(self, message):
        contents = message.contents[2:]
        peak_levels = []
        rms_levels = []
        for peak, rms in utils.group_iterable_by_count(contents, 2):
            peak_levels.append(peak)
            rms_levels.append(rms)
        self._output_meter_peak_levels = tuple(peak_levels)
        self._output_meter_rms_levels = tuple(rms_levels)

    ### PUBLIC METHODS ###

    def allocate(self):
        import supriya.osc
        import supriya.realtime

        self._input_meter_callback = self.server.osc_protocol.register(
            pattern=self.input_meter_command, procedure=self._handle_input_levels
        )
        self._output_meter_callback = self.server.osc_protocol.register(
            pattern=self.output_meter_command, procedure=self._handle_output_levels
        )
        input_meter_synthdef = self.input_meter_synthdef
        output_meter_synthdef = self.output_meter_synthdef
        self._input_meter_synth = supriya.realtime.Synth(input_meter_synthdef)
        self._output_meter_synth = supriya.realtime.Synth(output_meter_synthdef)
        self._input_meter_synth.allocate(
            add_action=supriya.AddAction.ADD_TO_HEAD,
            node_id_is_permanent=True,
            target_node=self.server.root_node,
        )
        self._output_meter_synth.allocate(
            add_action=supriya.AddAction.ADD_TO_TAIL,
            node_id_is_permanent=True,
            target_node=self.server.root_node,
        )
        return self

    def free(self):
        self.server.osc_protocol.unregister(self._input_meter_callback)
        self.server.osc_protocol.unregister(self._output_meter_callback)
        self._input_meter_synth.free()
        self._output_meter_synth.free()
        self._input_meter_callback = None
        self._output_meter_callback = None
        self._input_meter_synth = None
        self._output_meter_synth = None

    @staticmethod
    def make_meter_synthdef(channel_count=1, command_name="/reply", initial_bus=0):
        import supriya.synthdefs
        import supriya.ugens

        with supriya.synthdefs.SynthDefBuilder() as builder:
            source = supriya.ugens.In.ar(bus=initial_bus, channel_count=channel_count)
            supriya.ugens.SendPeakRMS.kr(
                command_name=command_name, peak_lag=1, reply_rate=20, source=source
            )
        synthdef = builder.build()
        return synthdef

    def notify(self, topic, event):
        if topic == "server-quitting":
            self.free()

    def to_dict(self):
        if not self.is_allocated:
            raise supriya.exceptions.NotAllocated(self)
        input_meter_levels, output_meter_levels = [], []
        for peak, rms in zip(
            self._input_meter_peak_levels or [], self._input_meter_rms_levels or []
        ):
            input_meter_levels.append(dict(peak=peak, rms=rms))
        for peak, rms in zip(
            self._output_meter_peak_levels or [], self._output_meter_rms_levels or []
        ):
            output_meter_levels.append(dict(peak=peak, rms=rms))
        result = {
            "server_meters": {
                "input_meter_levels": input_meter_levels,
                "output_meter_levels": output_meter_levels,
            }
        }
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def input_count(self):
        return self.server.options.input_bus_channel_count

    @property
    def is_allocated(self):
        return self.server is not None and self._input_meter_synth in self.server

    @property
    def output_count(self):
        return self.server.options.output_bus_channel_count

    @property
    def input_meter_command(self):
        return "/meter.inputs"

    @property
    def input_meter_synthdef(self):
        return self.make_meter_synthdef(
            channel_count=self.server.options.input_bus_channel_count,
            initial_bus=self.server.options.output_bus_channel_count,
            command_name=self.input_meter_command,
        )

    @property
    def output_meter_command(self):
        return "/meter.outputs"

    @property
    def output_meter_synthdef(self):
        return self.make_meter_synthdef(
            channel_count=self.server.options.output_bus_channel_count,
            initial_bus=0,
            command_name=self.output_meter_command,
        )

    @property
    def server(self):
        return self._server

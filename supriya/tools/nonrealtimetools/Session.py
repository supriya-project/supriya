# -*- encoding: utf-8 -*-
import hashlib
import os
import shutil
import struct
import subprocess
import tempfile
from abjad.tools import mathtools
from abjad.tools import timespantools
from supriya.tools import osctools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import soundfiletools
from supriya.tools import timetools
from supriya.tools.osctools.OscMixin import OscMixin


class Session(OscMixin):
    r'''A non-realtime session.

    ::

        >>> from supriya.tools import nonrealtimetools
        >>> session = nonrealtimetools.Session()

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> builder = synthdeftools.SynthDefBuilder(frequency=440)
        >>> with builder:
        ...     out = ugentools.Out.ar(
        ...         source=ugentools.SinOsc.ar(
        ...             frequency=builder['frequency'],
        ...             )
        ...         )
        ...
        >>> synthdef = builder.build()

    ::

        >>> synth_a = session.add_synth(0, 10, synthdef=synthdef)
        >>> synth_b = session.add_synth(5, 15, synthdef=synthdef, frequency=443)
        >>> synth_c = session.add_synth(0, 15, synthdef=synthdef, frequency=666)

    ::

        >>> with session.at(7.5):
        ...     synth_a['frequency'] = 880
        ...     synth_b['frequency'] = 990
        ...

    ::

        >>> for osc_bundle in session.to_osc_bundles():
        ...     osc_bundle
        ...
        OscBundle(
            timestamp=0.0,
            contents=(
                OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 9c4eb4778dc0faf39459fa8a5cd45c19\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01C\xdc\x00\x00\x00\x00\x00\x01\tfrequency\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                OscMessage('/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1000, 0, 0),
                OscMessage('/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1001, 0, 0, 'frequency', 666),
                )
            )
        OscBundle(
            timestamp=5.0,
            contents=(
                OscMessage('/s_new', '9c4eb4778dc0faf39459fa8a5cd45c19', 1002, 0, 0, 'frequency', 443),
                )
            )
        OscBundle(
            timestamp=10.0,
            contents=(
                OscMessage('/n_free', 1000),
                )
            )
        OscBundle(
            timestamp=15.0,
            contents=(
                OscMessage('/n_free', 1001),
                OscMessage('/n_free', 1002),
                )
            )

    ::

        >>> print(session)
        size 552
           0   00 00 01 68  23 62 75 6e  64 6c 65 00  00 00 00 00   |...h#bundle.....|
          16   00 00 00 00  00 00 00 bc  2f 64 5f 72  65 63 76 00   |......../d_recv.|
          32   2c 62 00 00  00 00 00 a9  53 43 67 66  00 00 00 02   |,b......SCgf....|
          48   00 01 20 39  63 34 65 62  34 37 37 38  64 63 30 66   |.. 9c4eb4778dc0f|
          64   61 66 33 39  34 35 39 66  61 38 61 35  63 64 34 35   |af39459fa8a5cd45|
          80   63 31 39 00  00 00 01 00  00 00 00 00  00 00 01 43   |c19............C|
          96   dc 00 00 00  00 00 01 09  66 72 65 71  75 65 6e 63   |........frequenc|
         112   79 00 00 00  00 00 00 00  03 07 43 6f  6e 74 72 6f   |y.........Contro|
         128   6c 01 00 00  00 00 00 00  00 01 00 00  01 06 53 69   |l.............Si|
         144   6e 4f 73 63  02 00 00 00  02 00 00 00  01 00 00 00   |nOsc............|
         160   00 00 00 00  00 00 00 ff  ff ff ff 00  00 00 00 02   |................|
         176   03 4f 75 74  02 00 00 00  02 00 00 00  00 00 00 ff   |.Out............|
         192   ff ff ff 00  00 00 00 00  00 00 01 00  00 00 00 00   |................|
         208   00 00 00 00  00 00 00 40  2f 73 5f 6e  65 77 00 00   |.......@/s_new..|
         224   2c 73 69 69  69 00 00 00  39 63 34 65  62 34 37 37   |,siii...9c4eb477|
         240   38 64 63 30  66 61 66 33  39 34 35 39  66 61 38 61   |8dc0faf39459fa8a|
         256   35 63 64 34  35 63 31 39  00 00 00 00  00 00 03 e8   |5cd45c19........|
         272   00 00 00 01  00 00 00 00  00 00 00 50  2f 73 5f 6e   |...........P/s_n|
         288   65 77 00 00  2c 73 69 69  69 73 69 00  39 63 34 65   |ew..,siiisi.9c4e|
         304   62 34 37 37  38 64 63 30  66 61 66 33  39 34 35 39   |b4778dc0faf39459|
         320   66 61 38 61  35 63 64 34  35 63 31 39  00 00 00 00   |fa8a5cd45c19....|
         336   00 00 03 e9  00 00 00 01  00 00 00 00  66 72 65 71   |............freq|
         352   75 65 6e 63  79 00 00 00  00 00 02 9a  00 00 00 64   |uency..........d|
         368   23 62 75 6e  64 6c 65 00  00 00 00 05  00 00 00 00   |#bundle.........|
         384   00 00 00 50  2f 73 5f 6e  65 77 00 00  2c 73 69 69   |...P/s_new..,sii|
         400   69 73 69 00  39 63 34 65  62 34 37 37  38 64 63 30   |isi.9c4eb4778dc0|
         416   66 61 66 33  39 34 35 39  66 61 38 61  35 63 64 34   |faf39459fa8a5cd4|
         432   35 63 31 39  00 00 00 00  00 00 03 ea  00 00 00 01   |5c19............|
         448   00 00 00 00  66 72 65 71  75 65 6e 63  79 00 00 00   |....frequency...|
         464   00 00 01 bb  00 00 00 24  23 62 75 6e  64 6c 65 00   |.......$#bundle.|
         480   00 00 00 0a  00 00 00 00  00 00 00 10  2f 6e 5f 66   |............/n_f|
         496   72 65 65 00  2c 69 00 00  00 00 03 e8  00 00 00 28   |ree.,i.........(|
         512   23 62 75 6e  64 6c 65 00  00 00 00 0f  00 00 00 00   |#bundle.........|
         528   00 00 00 14  2f 6e 5f 66  72 65 65 00  2c 69 69 00   |..../n_free.,ii.|
         544   00 00 03 e9  00 00 03 ea                             |........|

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_input_bus_group',
        '_audio_output_bus_group',
        '_buses',
        '_input_count',
        '_output_count',
        '_session_moments',
        '_synths',
        )

    ### INITIALIZER ###

    def __init__(self, input_count=0, output_count=2):
        from supriya.tools import nonrealtimetools

        input_count = int(input_count or 0)
        assert 0 <= input_count
        self._input_count = input_count

        output_count = int(output_count or 0)
        assert 0 <= output_count
        self._output_count = output_count

        audio_input_bus_group = None
        if self._input_count:
            audio_input_bus_group = nonrealtimetools.AudioInputBusGroup(self)
        self._audio_input_bus_group = audio_input_bus_group

        audio_output_bus_group = None
        if self._output_count:
            audio_output_bus_group = nonrealtimetools.AudioOutputBusGroup(self)
        self._audio_output_bus_group = audio_output_bus_group

        self._buses = set()
        self._session_moments = []
        self._synths = timetools.TimespanCollection()

    ### PRIVATE METHODS ###

    def _build_node_id_mapping(self):
        from supriya.tools import nonrealtimetools
        prototype = (nonrealtimetools.Synth,)
        mapping = {}
        allocator = servertools.NodeIdAllocator()
        for timespan in sorted(self._synths):
            if not isinstance(timespan, prototype):
                continue
            elif timespan in mapping:
                continue
            mapping[timespan] = allocator.allocate_node_id()
        return mapping

    def _build_command(
        self,
        output_filename,
        input_filename=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        **kwargs
        ):
        r'''Builds non-realtime rendering command.

        ::

            >>> session._build_command('output.aiff')
            'scsynth -N {} _ output.aiff 44100 aiff int24'

        '''
        parts = ['scsynth', '-N', '{}']
        if input_filename:
            parts.append(os.path.expanduser(input_filename))
        else:
            parts.append('_')
        parts.append(os.path.expanduser(output_filename))
        parts.append(str(int(sample_rate)))
        header_format = soundfiletools.HeaderFormat.from_expr(header_format)
        parts.append(header_format.name.lower())  # Must be lowercase.
        sample_format = soundfiletools.SampleFormat.from_expr(sample_format)
        parts.append(sample_format.name.lower())  # Must be lowercase.
        server_options = servertools.ServerOptions(**kwargs)
        server_options = server_options.as_options_string(realtime=False)
        if server_options:
            parts.append(server_options)
        command = ' '.join(parts)
        return command

    def _build_event_offset_mapping(self):
        from supriya.tools import nonrealtimetools
        mapping = {}
        for session_object, events in self._events.items():
            for timestep, payload in events:
                if timestep not in mapping:
                    mapping[timestep] = {}, {}
                bus_events, synth_events = mapping[timestep]
                if isinstance(session_object, nonrealtimetools.Bus):
                    bus_events[session_object] = payload
                elif isinstance(session_object, nonrealtimetools.Synth):
                    synth_events[session_object] = payload
        return mapping

    def _collect_synth_requests(self, request_mapping, id_mapping):
        synths = sorted(self._synths, key=lambda x: (x, id_mapping[x]))
        for synth in synths:
            items = synth._collect_requests(id_mapping).items()
            for timestep, synth_requests in items:
                requests = request_mapping.setdefault(timestep, [])
                requests.extend(synth_requests)
        return request_mapping

    def _collect_synthdef_requests(self, request_mapping):
        from supriya.tools import nonrealtimetools
        prototype = (nonrealtimetools.Synth,)
        synthdefs_to_offsets = {}
        for simultaneity in self._synths.iterate_simultaneities():
            start_events = set(simultaneity.start_timespans)
            for start_event in start_events:
                if not isinstance(start_event, prototype):
                    continue
                synthdef = start_event.synthdef
                if synthdef in synthdefs_to_offsets:
                    continue
                synthdefs_to_offsets[synthdef] = start_event.start_offset
        offsets_to_synthdefs = {}
        for synthdef, offset in synthdefs_to_offsets.items():
            if offset not in offsets_to_synthdefs:
                offsets_to_synthdefs[offset] = []
            offsets_to_synthdefs[offset].append(synthdef)
        for timestep, synthdefs in offsets_to_synthdefs.items():
            synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
            request = requesttools.SynthDefReceiveRequest(
                synthdefs=synthdefs,
                )
            requests = request_mapping.setdefault(timestep, [])
            requests.append(request)
        return request_mapping

    def _process_requests(self, offset, requests):
        timestamp = float(offset)
        osc_bundles = []
        if requests:
            osc_messages = [_.to_osc_message(with_textual_osc_command=True)
                for _ in requests]
            osc_bundle = osctools.OscBundle(timestamp, osc_messages)
            osc_bundles.append(osc_bundle)
        return osc_bundles

    def _process_terminal_event(self, final_timestep, timespan):
        osc_bundles = []
        if timespan is not None:
            prototype = (mathtools.Infinity(), mathtools.NegativeInfinity)
            if timespan.stop_offset not in prototype and \
                final_timestep < timespan.stop_offset:
                osc_bundle = osctools.OscBundle(
                    timestamp=float(timespan.stop_offset),
                    contents=[osctools.OscMessage(0)],
                    )
                osc_bundles.append(osc_bundle)
        return osc_bundles

    def _process_timespan_mask(self, timespan):
        if timespan is not None:
            assert isinstance(timespan, timespantools.Timespan)
            synths = timespantools.TimespanInventory(self._synths)
            original_timespan = synths.timespan
            synths = synths & timespan
            if timespan.start_offset not in (
                mathtools.Infinity(), mathtools.NegativeInfinity):
                translation = timespan.start_offset - \
                    original_timespan.start_offset
                synths = synths.translate(translation)
            session = type(self)()
            session._synths.insert(synths[:])
        else:
            session = self
        return session

    ### PUBLIC METHODS ###

    def at(self, timestep):
        from supriya.tools import nonrealtimetools
        session_moment = nonrealtimetools.SessionMoment(
            session=self,
            timestep=timestep,
            )
        return session_moment

    def add_bus(self, calculation_rate=None):
        from supriya.tools import nonrealtimetools
        bus = nonrealtimetools.Bus(self, calculation_rate=calculation_rate)
        self._buses.add(bus)
        return bus

    def add_bus_group(self, bus_count=1, calculation_rate=None):
        from supriya.tools import nonrealtimetools
        bus_group = nonrealtimetools.BusGroup(
            self,
            bus_count=bus_count,
            calculation_rate=calculation_rate,
            )
        for bus in bus_group:
            self._buses.add(bus)
        return bus_group

    def add_synth(
        self,
        start_offset=None,
        stop_offset=None,
        synthdef=None,
        add_action=None,
        **synth_kwargs
        ):
        from supriya.tools import nonrealtimetools
        synth = nonrealtimetools.Synth(
            self,
            start_offset=start_offset,
            stop_offset=stop_offset,
            synthdef=synthdef,
            add_action=add_action,
            **synth_kwargs
            )
        self._synths.insert(synth)
        return synth

    def render(
        self,
        output_filename,
        input_filename=None,
        timespan=None,
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        debug=False,
        **kwargs
        ):
        datagram = self.to_datagram(timespan=timespan)
        md5 = hashlib.md5()
        md5.update(datagram)
        md5 = md5.hexdigest()
        temp_directory_path = tempfile.mkdtemp()
        file_path = os.path.join(temp_directory_path, '{}.osc'.format(md5))
        with open(file_path, 'wb') as file_pointer:
            file_pointer.write(datagram)
        command = self._build_command(
            output_filename,
            input_filename=None,
            sample_rate=sample_rate,
            header_format=header_format,
            sample_format=sample_format,
            **kwargs
            )
        command = command.format(file_path)
        exit_code = subprocess.call(command, shell=True)
        if debug:
            return exit_code, file_path
        else:
            shutil.rmtree(temp_directory_path)
            return exit_code, None

    def to_datagram(self, timespan=None):
        osc_bundles = self.to_osc_bundles(timespan=timespan)
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack('>i', size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b''.join(datagrams)
        return datagram

    def to_osc_bundles(self, timespan=None):
        osc_bundles = []
        session = self._process_timespan_mask(timespan)
        id_mapping = session._build_node_id_mapping()
        request_mapping = {}
        request_mapping = self._collect_synthdef_requests(request_mapping)
        request_mapping = self._collect_synth_requests(request_mapping, id_mapping)
        for timestep, requests in sorted(request_mapping.items()):
            osc_bundles += self._process_requests(timestep, requests)
        osc_bundles += self._process_terminal_event(timestep, timespan)
        return osc_bundles

    ### PUBLIC PROPERTIES ###

    @property
    def audio_input_bus_group(self):
        return self._audio_input_bus_group

    @property
    def audio_output_bus_group(self):
        return self._audio_output_bus_group

    @property
    def input_count(self):
        return self._input_count

    @property
    def output_count(self):
        return self._output_count

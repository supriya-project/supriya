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
from supriya.tools.osctools.OscMixin import OscMixin
from supriya.tools.timetools.TimespanCollection import TimespanCollection


class Session(TimespanCollection, OscMixin):
    r'''A non-realtime session.

    ::

        >>> from supriya.tools import nrttools
        >>> session = nrttools.Session()

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

        >>> synth_one = nrttools.Synth(0, 10, synthdef=synthdef)
        >>> synth_two = nrttools.Synth(5, 15, synthdef=synthdef, frequency=443)
        >>> synth_three = nrttools.Synth(0, 15, synthdef=synthdef, frequency=666)
        >>> session.insert([synth_one, synth_two, synth_three])

    ::

        >>> for osc_bundle in session.to_osc_bundles():
        ...     osc_bundle
        ...
        OscBundle(
            timestamp=0.0,
            contents=(
                OscMessage(5, bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 9c4eb4778dc0faf39459fa8a5cd45c19\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01C\xdc\x00\x00\x00\x00\x00\x01\tfrequency\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                OscMessage(9, '9c4eb4778dc0faf39459fa8a5cd45c19', 1000, 1, 0),
                OscMessage(9, '9c4eb4778dc0faf39459fa8a5cd45c19', 1001, 1, 0, 'frequency', 666),
                )
            )
        OscBundle(
            timestamp=5.0,
            contents=(
                OscMessage(9, '9c4eb4778dc0faf39459fa8a5cd45c19', 1002, 1, 0, 'frequency', 443),
                )
            )
        OscBundle(
            timestamp=10.0,
            contents=(
                OscMessage(11, 1000),
                )
            )
        OscBundle(
            timestamp=15.0,
            contents=(
                OscMessage(11, 1001, 1002),
                )
            )

    ::

        >>> print(session)
        size 528
           0   00 00 01 5c  23 62 75 6e  64 6c 65 00  00 00 00 00   |...\#bundle.....|
          16   00 00 00 00  00 00 00 b8  00 00 00 05  2c 62 00 00   |............,b..|
          32   00 00 00 a9  53 43 67 66  00 00 00 02  00 01 20 39   |....SCgf...... 9|
          48   63 34 65 62  34 37 37 38  64 63 30 66  61 66 33 39   |c4eb4778dc0faf39|
          64   34 35 39 66  61 38 61 35  63 64 34 35  63 31 39 00   |459fa8a5cd45c19.|
          80   00 00 01 00  00 00 00 00  00 00 01 43  dc 00 00 00   |...........C....|
          96   00 00 01 09  66 72 65 71  75 65 6e 63  79 00 00 00   |....frequency...|
         112   00 00 00 00  03 07 43 6f  6e 74 72 6f  6c 01 00 00   |......Control...|
         128   00 00 00 00  00 01 00 00  01 06 53 69  6e 4f 73 63   |..........SinOsc|
         144   02 00 00 00  02 00 00 00  01 00 00 00  00 00 00 00   |................|
         160   00 00 00 ff  ff ff ff 00  00 00 00 02  03 4f 75 74   |.............Out|
         176   02 00 00 00  02 00 00 00  00 00 00 ff  ff ff ff 00   |................|
         192   00 00 00 00  00 00 01 00  00 00 00 00  00 00 00 00   |................|
         208   00 00 00 3c  00 00 00 09  2c 73 69 69  69 00 00 00   |...<....,siii...|
         224   39 63 34 65  62 34 37 37  38 64 63 30  66 61 66 33   |9c4eb4778dc0faf3|
         240   39 34 35 39  66 61 38 61  35 63 64 34  35 63 31 39   |9459fa8a5cd45c19|
         256   00 00 00 00  00 00 03 e8  00 00 00 01  00 00 00 00   |................|
         272   00 00 00 4c  00 00 00 09  2c 73 69 69  69 73 69 00   |...L....,siiisi.|
         288   39 63 34 65  62 34 37 37  38 64 63 30  66 61 66 33   |9c4eb4778dc0faf3|
         304   39 34 35 39  66 61 38 61  35 63 64 34  35 63 31 39   |9459fa8a5cd45c19|
         320   00 00 00 00  00 00 03 e9  00 00 00 01  00 00 00 00   |................|
         336   66 72 65 71  75 65 6e 63  79 00 00 00  00 00 02 9a   |frequency.......|
         352   00 00 00 60  23 62 75 6e  64 6c 65 00  00 00 00 05   |...`#bundle.....|
         368   00 00 00 00  00 00 00 4c  00 00 00 09  2c 73 69 69   |.......L....,sii|
         384   69 73 69 00  39 63 34 65  62 34 37 37  38 64 63 30   |isi.9c4eb4778dc0|
         400   66 61 66 33  39 34 35 39  66 61 38 61  35 63 64 34   |faf39459fa8a5cd4|
         416   35 63 31 39  00 00 00 00  00 00 03 ea  00 00 00 01   |5c19............|
         432   00 00 00 00  66 72 65 71  75 65 6e 63  79 00 00 00   |....frequency...|
         448   00 00 01 bb  00 00 00 20  23 62 75 6e  64 6c 65 00   |....... #bundle.|
         464   00 00 00 0a  00 00 00 00  00 00 00 0c  00 00 00 0b   |................|
         480   2c 69 00 00  00 00 03 e8  00 00 00 24  23 62 75 6e   |,i.........$#bun|
         496   64 6c 65 00  00 00 00 0f  00 00 00 00  00 00 00 10   |dle.............|
         512   00 00 00 0b  2c 69 69 00  00 00 03 e9  00 00 03 ea   |....,ii.........|

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_session_moments',
        )

    ### INITIALIZER ###

    def __init__(self, timespans=None):
        TimespanCollection.__init__(self, timespans=timespans)
        self._session_moments = []

    ### PRIVATE METHODS ###

    def _build_node_id_mapping(self):
        from supriya.tools import nrttools
        prototype = (nrttools.Synth,)
        mapping = {}
        allocator = servertools.NodeIdAllocator()
        for timespan in sorted(self):
            if not isinstance(timespan, prototype):
                continue
            elif timespan in mapping:
                continue
            mapping[timespan] = allocator.allocate_node_id()
        return mapping

    def _build_synthdef_receive_offset_mapping(self):
        from supriya.tools import nrttools
        prototype = (nrttools.Synth,)
        synthdefs_to_offsets = {}
        for simultaneity in self.iterate_simultaneities():
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
        return offsets_to_synthdefs

    def _process_requests(self, offset, requests):
        osc_messages = []
        for request in requests:
            osc_message = request.to_osc_message()
            osc_messages.append(osc_message)
        timestamp = float(offset)
        osc_bundles = []
        if requests:
            osc_messages = [_.to_osc_message() for _ in requests]
            osc_bundle = osctools.OscBundle(timestamp, osc_messages)
            osc_bundles.append(osc_bundle)
        return osc_bundles

    def _process_start_events(self, start_events, node_id_mapping):
        from supriya.tools import nrttools
        requests = []
        for start_event in sorted(start_events):
            if not isinstance(start_event, nrttools.Synth):
                continue
            request = start_event.get_start_request(node_id_mapping)
            requests.append(request)
        return requests

    def _process_stop_events(self, stop_events, node_id_mapping):
        from supriya.tools import nrttools
        requests = []
        if stop_events:
            free_ids = []
            gate_ids = []
            for stop_event in stop_events:
                if not isinstance(stop_event, nrttools.Synth):
                    continue
                parameter_names = stop_event.synthdef.parameter_names
                if 'gate' in parameter_names:
                    gate_ids.append(node_id_mapping[stop_event])
                else:
                    free_ids.append(node_id_mapping[stop_event])
            if free_ids:
                free_ids.sort()
                request = requesttools.NodeFreeRequest(node_ids=free_ids)
                requests.append(request)
            if gate_ids:
                for node_id in sorted(gate_ids):
                    request = requesttools.NodeSetRequest(node_id, gate=0)
                    requests.append(request)
        return requests

    def _process_synthdef_events(self, offset, synthdef_mapping):
        requests = []
        synthdefs = sorted(synthdef_mapping.get(offset, []),
            key=lambda x: x.anonymous_name)
        if synthdefs:
            request = requesttools.SynthDefReceiveRequest(
                synthdefs=synthdefs,
                )
            requests.append(request)
        return requests

    def _process_terminal_event(self, all_offsets, timespan):
        osc_bundles = []
        if timespan is not None:
            prototype = (mathtools.Infinity(), mathtools.NegativeInfinity)
            if timespan.stop_offset not in prototype and \
                all_offsets[-1] < timespan.stop_offset:
                osc_bundle = osctools.OscBundle(
                    timestamp=float(timespan.stop_offset),
                    contents=[osctools.OscMessage(0)],
                    )
                osc_bundles.append(osc_bundle)
        return osc_bundles

    def _process_timespan_mask(self, timespan):
        if timespan is not None:
            assert isinstance(timespan, timespantools.Timespan)
            session = timespantools.TimespanInventory(self)
            original_timespan = session.timespan
            session = session & timespan
            if timespan.start_offset not in (
                mathtools.Infinity(), mathtools.NegativeInfinity):
                translation = timespan.start_offset - \
                    original_timespan.start_offset
                session = session.translate(translation)
            session = type(self)(timespans=session[:])
        else:
            session = self
        return session

    ### PUBLIC METHODS ###

    def at(self, timestep):
        from supriya.tools import nrttools
        session_moment = nrttools.SessionMoment(
            session=self,
            timestep=timestep,
            )
        return session_moment

    def build_command(
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

            >>> session.build_command('output.aiff')
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
        command = self.build_command(
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
        node_mapping = session._build_node_id_mapping()
        synthdef_mapping = session._build_synthdef_receive_offset_mapping()
        all_offsets = session.all_offsets
        for offset in all_offsets:
            simultaneity = session.get_simultaneity_at(offset)
            start_events = set(simultaneity.start_timespans)
            stop_events = set(simultaneity.stop_timespans)
            stop_events.difference_update(start_events)
            requests = self._process_synthdef_events(offset, synthdef_mapping)
            requests += self._process_start_events(start_events, node_mapping)
            requests += self._process_stop_events(stop_events, node_mapping)
            osc_bundles += self._process_requests(
                simultaneity.start_offset, requests)
        osc_bundles += self._process_terminal_event(all_offsets, timespan)
        return osc_bundles

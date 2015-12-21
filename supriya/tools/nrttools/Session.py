# -*- encoding: utf-8 -*-
import hashlib
import os
import shutil
import struct
import subprocess
import tempfile
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

        >>> synth_one = nrttools.Synth(synthdef, 0, 10)
        >>> synth_two = nrttools.Synth(synthdef, 5, 15, frequency=443)
        >>> synth_three = nrttools.Synth(synthdef, 0, 15, frequency=666)
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
        size 512
           0   23 62 75 6e  64 6c 65 00  83 aa 7e 80  00 00 00 00   |#bundle...~.....|
          16   00 00 00 b8  00 00 00 05  2c 62 00 00  00 00 00 a9   |........,b......|
          32   53 43 67 66  00 00 00 02  00 01 20 39  63 34 65 62   |SCgf...... 9c4eb|
          48   34 37 37 38  64 63 30 66  61 66 33 39  34 35 39 66   |4778dc0faf39459f|
          64   61 38 61 35  63 64 34 35  63 31 39 00  00 00 01 00   |a8a5cd45c19.....|
          80   00 00 00 00  00 00 01 43  dc 00 00 00  00 00 01 09   |.......C........|
          96   66 72 65 71  75 65 6e 63  79 00 00 00  00 00 00 00   |frequency.......|
         112   03 07 43 6f  6e 74 72 6f  6c 01 00 00  00 00 00 00   |..Control.......|
         128   00 01 00 00  01 06 53 69  6e 4f 73 63  02 00 00 00   |......SinOsc....|
         144   02 00 00 00  01 00 00 00  00 00 00 00  00 00 00 ff   |................|
         160   ff ff ff 00  00 00 00 02  03 4f 75 74  02 00 00 00   |.........Out....|
         176   02 00 00 00  00 00 00 ff  ff ff ff 00  00 00 00 00   |................|
         192   00 00 01 00  00 00 00 00  00 00 00 00  00 00 00 3c   |...............<|
         208   00 00 00 09  2c 73 69 69  69 00 00 00  39 63 34 65   |....,siii...9c4e|
         224   62 34 37 37  38 64 63 30  66 61 66 33  39 34 35 39   |b4778dc0faf39459|
         240   66 61 38 61  35 63 64 34  35 63 31 39  00 00 00 00   |fa8a5cd45c19....|
         256   00 00 03 e8  00 00 00 01  00 00 00 00  00 00 00 4c   |...............L|
         272   00 00 00 09  2c 73 69 69  69 73 69 00  39 63 34 65   |....,siiisi.9c4e|
         288   62 34 37 37  38 64 63 30  66 61 66 33  39 34 35 39   |b4778dc0faf39459|
         304   66 61 38 61  35 63 64 34  35 63 31 39  00 00 00 00   |fa8a5cd45c19....|
         320   00 00 03 e9  00 00 00 01  00 00 00 00  66 72 65 71   |............freq|
         336   75 65 6e 63  79 00 00 00  00 00 02 9a  23 62 75 6e   |uency.......#bun|
         352   64 6c 65 00  83 aa 7e 85  00 00 00 00  00 00 00 4c   |dle...~........L|
         368   00 00 00 09  2c 73 69 69  69 73 69 00  39 63 34 65   |....,siiisi.9c4e|
         384   62 34 37 37  38 64 63 30  66 61 66 33  39 34 35 39   |b4778dc0faf39459|
         400   66 61 38 61  35 63 64 34  35 63 31 39  00 00 00 00   |fa8a5cd45c19....|
         416   00 00 03 ea  00 00 00 01  00 00 00 00  66 72 65 71   |............freq|
         432   75 65 6e 63  79 00 00 00  00 00 01 bb  23 62 75 6e   |uency.......#bun|
         448   64 6c 65 00  83 aa 7e 8a  00 00 00 00  00 00 00 0c   |dle...~.........|
         464   00 00 00 0b  2c 69 00 00  00 00 03 e8  23 62 75 6e   |....,i......#bun|
         480   64 6c 65 00  83 aa 7e 8f  00 00 00 00  00 00 00 10   |dle...~.........|
         496   00 00 00 0b  2c 69 69 00  00 00 03 e9  00 00 03 ea   |....,ii.........|

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

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

    ### PUBLIC METHODS ###

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
            'scsynth -N {} _ output.aiff 41000 aiff int24'

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
        sample_rate=44100,
        header_format=soundfiletools.HeaderFormat.AIFF,
        sample_format=soundfiletools.SampleFormat.INT24,
        debug=False,
        **kwargs
        ):
        datagram = self.to_datagram()
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
            sample_rate=44100,
            header_format=soundfiletools.HeaderFormat.AIFF,
            sample_format=soundfiletools.SampleFormat.INT24,
            **kwargs
            )
        command = command.format(file_path)
        exit_code = subprocess.call(command, shell=True)
        if debug:
            return exit_code, file_path
        else:
            shutil.rmtree(temp_directory_path)
            return exit_code, None

    def to_datagram(self):
        osc_bundles = self.to_osc_bundles()
        datagrams = []
        for osc_bundle in osc_bundles:
            datagram = osc_bundle.to_datagram(realtime=False)
            size = len(datagram)
            size = struct.pack('>i', size)
            datagrams.append(size)
            datagrams.append(datagram)
        datagram = b''.join(datagrams)
        return datagram

    def to_osc_bundles(self):
        from supriya.tools import nrttools
        osc_bundles = []
        node_id_mapping = self._build_node_id_mapping()
        synthdef_mapping = self._build_synthdef_receive_offset_mapping()
        for offset in self.all_offsets:
            simultaneity = self.get_simultaneity_at(offset)
            requests = []
            start_events = set(simultaneity.start_timespans)
            stop_events = set(simultaneity.stop_timespans)
            stop_events.difference_update(start_events)
            synthdefs = sorted(synthdef_mapping.get(offset, []),
                key=lambda x: x.anonymous_name)
            if synthdefs:
                request = requesttools.SynthDefReceiveRequest(
                    synthdefs=synthdefs,
                    )
                requests.append(request)
            for start_event in sorted(start_events):
                if not isinstance(start_event, nrttools.Synth):
                    continue
                event_requests = start_event.get_start_requests(
                    node_id_mapping)
                requests.extend(event_requests)
            if stop_events:
                node_ids = []
                for stop_event in stop_events:
                    if not isinstance(start_event, nrttools.Synth):
                        continue
                    node_ids.append(node_id_mapping[stop_event])
                node_ids.sort()
                request = requesttools.NodeFreeRequest(node_ids=node_ids)
                requests.append(request)
            osc_messages = []
            for request in requests:
                osc_message = request.to_osc_message()
                osc_messages.append(osc_message)
            timestamp = float(simultaneity.start_offset)
            if requests:
                osc_messages = [_.to_osc_message() for _ in requests]
                osc_bundle = osctools.OscBundle(timestamp, osc_messages)
                osc_bundles.append(osc_bundle)
        return osc_bundles

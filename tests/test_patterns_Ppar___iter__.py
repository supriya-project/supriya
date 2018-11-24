import pytest
import uqbar.strings
import supriya.patterns


pattern_01 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=supriya.patterns.Pseq([1001, 1002, 1003], 1),
        )
    ]
)


pattern_02 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=supriya.patterns.Pseq([1001, 1002], 1),
        ),
        supriya.patterns.Pmono(
            amplitude=1.0,
            duration=0.75,
            frequency=supriya.patterns.Pseq([2001, 2002, 2003], 1),
        ),
    ]
)


pattern_03 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=supriya.patterns.Pseq([1001, 1002, 1003], 1),
        ),
        supriya.patterns.Pbind(
            amplitude=1.0, duration=0.75, frequency=supriya.patterns.Pseq([], 1)
        ),
    ]
)


pattern_04 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbus(
            supriya.patterns.Pbind(
                amplitude=1.0,
                duration=0.75,
                frequency=supriya.patterns.Pseq([1001, 1002, 1003], 1),
            )
        )
    ]
)


pattern_05 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbus(
            supriya.patterns.Pbind(
                amplitude=1.0,
                duration=1.0,
                frequency=supriya.patterns.Pseq([1001, 1002], 1),
            )
        ),
        supriya.patterns.Pbus(
            supriya.patterns.Pmono(
                amplitude=1.0,
                duration=0.75,
                frequency=supriya.patterns.Pseq([2001, 2002, 2003], 1),
            )
        ),
    ]
)


pattern_06 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pgpar(
            [
                [
                    supriya.patterns.Pbind(
                        delta=10,
                        duration=10,
                        frequency=supriya.patterns.Pseq([1001, 1002, 1003]),
                    ),
                    supriya.patterns.Pbind(
                        delta=12,
                        duration=10,
                        frequency=supriya.patterns.Pseq([2001, 2002, 2003]),
                    ),
                ]
            ]
        ),
        supriya.patterns.Pgpar(
            [
                [
                    supriya.patterns.Pbind(
                        delta=10,
                        duration=10,
                        frequency=supriya.patterns.Pseq([3001, 3002]),
                    ),
                    supriya.patterns.Pbind(
                        delta=12,
                        duration=10,
                        frequency=supriya.patterns.Pseq([4001, 4002]),
                    ),
                ]
            ]
        ),
    ]
)


def test___iter___01():
    events = list(pattern_01)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        '''
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1002,
            uuid=UUID('B'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1003,
            uuid=UUID('C'),
            )
        '''
    )


def test___iter___02():
    events = list(pattern_02)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        '''
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2001,
            is_stop=False,
            uuid=UUID('B'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.25,
            duration=0.75,
            frequency=2002,
            is_stop=False,
            uuid=UUID('B'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.5,
            duration=1.0,
            frequency=1002,
            uuid=UUID('C'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2003,
            uuid=UUID('B'),
            )
        '''
    )


def test___iter___03():
    events = list(pattern_03)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        '''
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1002,
            uuid=UUID('B'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1003,
            uuid=UUID('C'),
            )
        '''
    )


def test___iter___04():
    events = list(pattern_04)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        '''
        CompositeEvent(
            events=(
                BusEvent(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=2,
                    uuid=UUID('A'),
                    ),
                GroupEvent(
                    uuid=UUID('B'),
                    ),
                SynthEvent(
                    add_action=AddAction.ADD_AFTER,
                    amplitude=1.0,
                    fade_time=0.25,
                    in_=UUID('A'),
                    synthdef=<SynthDef: system_link_audio_2>,
                    target_node=UUID('B'),
                    uuid=UUID('C'),
                    ),
                ),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=1001,
            out=UUID('A'),
            target_node=UUID('B'),
            uuid=UUID('D'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=1002,
            out=UUID('A'),
            target_node=UUID('B'),
            uuid=UUID('E'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=1003,
            out=UUID('A'),
            target_node=UUID('B'),
            uuid=UUID('F'),
            )
        CompositeEvent(
            events=(
                SynthEvent(
                    is_stop=True,
                    uuid=UUID('C'),
                    ),
                NullEvent(
                    delta=0.25,
                    ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('B'),
                    ),
                BusEvent(
                    calculation_rate=None,
                    channel_count=None,
                    is_stop=True,
                    uuid=UUID('A'),
                    ),
                ),
            is_stop=True,
            )
        '''
    )


def test___iter___05():
    events = list(pattern_05)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        '''
        CompositeEvent(
            events=(
                BusEvent(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=2,
                    uuid=UUID('A'),
                    ),
                GroupEvent(
                    uuid=UUID('B'),
                    ),
                SynthEvent(
                    add_action=AddAction.ADD_AFTER,
                    amplitude=1.0,
                    fade_time=0.25,
                    in_=UUID('A'),
                    synthdef=<SynthDef: system_link_audio_2>,
                    target_node=UUID('B'),
                    uuid=UUID('C'),
                    ),
                ),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            out=UUID('A'),
            target_node=UUID('B'),
            uuid=UUID('D'),
            )
        CompositeEvent(
            events=(
                BusEvent(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=2,
                    uuid=UUID('E'),
                    ),
                GroupEvent(
                    uuid=UUID('F'),
                    ),
                SynthEvent(
                    add_action=AddAction.ADD_AFTER,
                    amplitude=1.0,
                    fade_time=0.25,
                    in_=UUID('E'),
                    synthdef=<SynthDef: system_link_audio_2>,
                    target_node=UUID('F'),
                    uuid=UUID('G'),
                    ),
                ),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2001,
            is_stop=False,
            out=UUID('E'),
            target_node=UUID('F'),
            uuid=UUID('H'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.25,
            duration=0.75,
            frequency=2002,
            is_stop=False,
            out=UUID('E'),
            target_node=UUID('F'),
            uuid=UUID('H'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.5,
            duration=1.0,
            frequency=1002,
            out=UUID('A'),
            target_node=UUID('B'),
            uuid=UUID('I'),
            )
        NoteEvent(
            amplitude=1.0,
            delta=0.5,
            duration=0.75,
            frequency=2003,
            out=UUID('E'),
            target_node=UUID('F'),
            uuid=UUID('H'),
            )
        CompositeEvent(
            delta=0.25,
            events=(
                SynthEvent(
                    is_stop=True,
                    uuid=UUID('C'),
                    ),
                NullEvent(
                    delta=0.25,
                    ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('B'),
                    ),
                BusEvent(
                    calculation_rate=None,
                    channel_count=None,
                    is_stop=True,
                    uuid=UUID('A'),
                    ),
                ),
            is_stop=True,
            )
        CompositeEvent(
            events=(
                SynthEvent(
                    is_stop=True,
                    uuid=UUID('G'),
                    ),
                NullEvent(
                    delta=0.25,
                    ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('F'),
                    ),
                BusEvent(
                    calculation_rate=None,
                    channel_count=None,
                    is_stop=True,
                    uuid=UUID('E'),
                    ),
                ),
            is_stop=True,
            )
        '''
    )


def test___iter___06():
    events = list(pattern_06)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        '''
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('A'),
                    ),
                ),
            )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=1001,
            target_node=UUID('A'),
            uuid=UUID('B'),
            )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=2001,
            target_node=UUID('A'),
            uuid=UUID('C'),
            )
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('D'),
                    ),
                ),
            )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=3001,
            target_node=UUID('D'),
            uuid=UUID('E'),
            )
        NoteEvent(
            delta=10.0,
            duration=10,
            frequency=4001,
            target_node=UUID('D'),
            uuid=UUID('F'),
            )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=1002,
            target_node=UUID('A'),
            uuid=UUID('G'),
            )
        NoteEvent(
            delta=2.0,
            duration=10,
            frequency=3002,
            target_node=UUID('D'),
            uuid=UUID('H'),
            )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=2002,
            target_node=UUID('A'),
            uuid=UUID('I'),
            )
        NoteEvent(
            delta=8.0,
            duration=10,
            frequency=4002,
            target_node=UUID('D'),
            uuid=UUID('J'),
            )
        NoteEvent(
            delta=4.0,
            duration=10,
            frequency=1003,
            target_node=UUID('A'),
            uuid=UUID('K'),
            )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=2003,
            target_node=UUID('A'),
            uuid=UUID('L'),
            )
        CompositeEvent(
            delta=12.0,
            events=(
                NullEvent(
                    delta=0.25,
                    ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('D'),
                    ),
                ),
            is_stop=True,
            )
        CompositeEvent(
            events=(
                NullEvent(
                    delta=0.25,
                    ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('A'),
                    ),
                ),
            is_stop=True,
            )
        '''
    )

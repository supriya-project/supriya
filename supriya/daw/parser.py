# type: ignore
# flake8: noqa
"""
Parses LilyPond-like syntax into a clip.

::

    >>> from supriya.daw.parser import parse

::

    >>> parse("c1")
    Clip(
        notes=IntervalTree(
            intervals=[
                Note(start_offset=0.0, stop_offset=1.0, pitch=60, velocity=100.0),
                ],
            ),
        )

::

    >>> parse("c4 d e f")
    Clip(
        notes=IntervalTree(
            intervals=[
                Note(start_offset=0.0, stop_offset=0.25, pitch=60, velocity=100.0),
                Note(start_offset=0.25, stop_offset=0.5, pitch=62, velocity=100.0),
                Note(start_offset=0.5, stop_offset=0.75, pitch=64, velocity=100.0),
                Note(start_offset=0.75, stop_offset=1.0, pitch=65, velocity=100.0),
                ],
            ),
        )

::

    >>> parse("c'8 d' e' f' g' a' b' c''")
    Clip(
        notes=IntervalTree(
            intervals=[
                Note(start_offset=0.0, stop_offset=0.125, pitch=72, velocity=100.0),
                Note(start_offset=0.125, stop_offset=0.25, pitch=74, velocity=100.0),
                Note(start_offset=0.25, stop_offset=0.375, pitch=76, velocity=100.0),
                Note(start_offset=0.375, stop_offset=0.5, pitch=77, velocity=100.0),
                Note(start_offset=0.5, stop_offset=0.625, pitch=79, velocity=100.0),
                Note(start_offset=0.625, stop_offset=0.75, pitch=81, velocity=100.0),
                Note(start_offset=0.75, stop_offset=0.875, pitch=83, velocity=100.0),
                Note(start_offset=0.875, stop_offset=1.0, pitch=84, velocity=100.0),
                ],
            ),
        )

::

    >>> parse("c4. d8 e4 ~8 f")
    Clip(
        notes=IntervalTree(
            intervals=[
                Note(start_offset=0.0, stop_offset=0.375, pitch=60, velocity=100.0),
                Note(start_offset=0.375, stop_offset=0.5, pitch=62, velocity=100.0),
                Note(start_offset=0.5, stop_offset=0.875, pitch=64, velocity=100.0),
                Note(start_offset=0.875, stop_offset=1.0, pitch=65, velocity=100.0),
                ],
            ),
        )

::

    >>> parse("{ { <c fs>4 r8 q } ~8 q4 } ~8")
    Clip(
        notes=IntervalTree(
            intervals=[
                Note(start_offset=0.0, stop_offset=0.25, pitch=60, velocity=100.0),
                Note(start_offset=0.0, stop_offset=0.25, pitch=66, velocity=100.0),
                Note(start_offset=0.375, stop_offset=0.625, pitch=60, velocity=100.0),
                Note(start_offset=0.375, stop_offset=0.625, pitch=66, velocity=100.0),
                Note(start_offset=0.625, stop_offset=1.0, pitch=60, velocity=100.0),
                Note(start_offset=0.625, stop_offset=1.0, pitch=66, velocity=100.0),
                ],
            ),
        )

::

    >>> parse("2/3 { c d e } 4/5 { ~8 g8 a b c' } ")
    Clip(
        notes=IntervalTree(
            intervals=[
                Note(start_offset=0.0, stop_offset=0.16666666666666666, pitch=60, velocity=100.0),
                Note(start_offset=0.16666666666666666, stop_offset=0.3333333333333333, pitch=62, velocity=100.0),
                Note(start_offset=0.3333333333333333, stop_offset=0.6, pitch=64, velocity=100.0),
                Note(start_offset=0.6, stop_offset=0.7, pitch=67, velocity=100.0),
                Note(start_offset=0.7, stop_offset=0.8, pitch=69, velocity=100.0),
                Note(start_offset=0.8, stop_offset=0.9, pitch=71, velocity=100.0),
                Note(start_offset=0.9, stop_offset=1.0, pitch=72, velocity=100.0),
                ],
            ),
        )

"""

from collections import deque
from fractions import Fraction
from typing import List, NamedTuple, Optional, Tuple, Union

from sly import Lexer, Parser

from supriya.daw import Clip, Note


def parse(text):
    components = ClipParser().parse(ClipLexer().tokenize(text))
    # convert components into flat list of leaves, and tie durations, populate deque
    leaves = deque()
    for component in components:
        if isinstance(component, Container):
            leaves.extend(component.to_leaves())
        else:
            leaves.append(component)
    initial_offset = 0
    current_leaf = None
    next_leaf = None
    notes = []
    while leaves:
        next_leaf = leaves.popleft()
        if current_leaf is None:
            if not isinstance(next_leaf, Leaf):
                raise ValueError("Cannot start with a tie")
            current_leaf = next_leaf
            continue
        if isinstance(next_leaf, Leaf):
            new_notes, initial_offset = current_leaf.to_notes(initial_offset)
            notes.extend(new_notes)
            current_leaf = next_leaf
            next_leaf = None
        else:
            current_leaf = Leaf(
                pitches=current_leaf.pitches, duration=current_leaf.duration + next_leaf
            )
    if isinstance(current_leaf, Leaf):
        new_notes, _ = current_leaf.to_notes(initial_offset)
        notes.extend(new_notes)
    return Clip(notes=notes)


class Leaf(NamedTuple):
    pitches: List[int]
    duration: Fraction

    def to_notes(self, initial_offset=0):
        notes = []
        final_offset = initial_offset + self.duration
        for pitch in self.pitches:
            note = Note(
                start_offset=float(initial_offset),
                stop_offset=float(final_offset),
                pitch=pitch,
            )
            notes.append(note)
        return notes, final_offset


class Container(NamedTuple):
    multiplier: Optional[Tuple]
    components: List[Union[Leaf, "Container", Fraction]]

    def to_leaves(self, multiplier=1):
        leaves = []
        multiplier *= self.multiplier
        for i, component in enumerate(self.components):
            if isinstance(component, Leaf):
                leaves.append(
                    Leaf(
                        duration=component.duration * multiplier,
                        pitches=component.pitches,
                    )
                )
            elif isinstance(component, Container):
                leaves.extend(component.to_leaves(multiplier=multiplier))
            else:
                leaves.append(multiplier * component)
        return leaves


def name_to_midi(name):
    midi = {"c": 60, "d": 62, "e": 64, "f": 65, "g": 67, "a": 69, "b": 71}[name[0]]
    if len(name) > 1:
        if name[-1] == "f":
            midi -= 1
        elif name[-1] == "s":
            midi += 1
    return midi


class ClipLexer(Lexer):
    ignore = " \t"
    ignore_newline = r"\n+"

    CHORD_CLOSE = ">"
    CHORD_OPEN = "<"
    CHORD_REPEAT = "q"
    DOT = "\\."
    FRACTION = "[1-9][0-9]*/[1-9][0-9]*"
    CONTAINER_CLOSE = "\\}"
    CONTAINER_OPEN = "\\{"
    NAME = "[a-g][sf]*"
    NUMBER = "[1-9][0-9]*"
    OCTAVE_DOWN = ","
    OCTAVE_UP = "'"
    REST = "r"
    TIE = "~"

    tokens = {
        "CHORD_CLOSE",
        "CHORD_OPEN",
        "CHORD_REPEAT",
        "DOT",
        "FRACTION",
        "CONTAINER_CLOSE",
        "CONTAINER_OPEN",
        "NAME",
        "NUMBER",
        "OCTAVE_DOWN",
        "OCTAVE_UP",
        "REST",
        "TIE",
    }


class ClipParser(Parser):
    start = "top"
    tokens = ClipLexer.tokens

    def __init__(self):
        self._previous_pitches = (60, 64, 67)
        self._previous_duration = Fraction(1, 4)

    @_("")
    def empty(self, p):
        pass

    @_("DOT", "dots DOT")
    def dots(self, p):
        if len(p) == 1:
            return 1
        return p[0] + 1

    @_("NUMBER", "NUMBER dots")
    def duration(self, p):
        duration = Fraction(1, int(p[0]))
        if len(p) > 1:
            durations = []
            for i in range(p[1] + 1):
                durations.append(
                    Fraction(duration.numerator, duration.denominator * pow(2, i))
                )
            duration = sum(durations)
        self._previous_duration = duration
        return duration

    @_("OCTAVE_DOWN", "octaves_down OCTAVE_DOWN")
    def octaves_down(self, p):
        if len(p) == 1:
            return 1
        return p[0] + 1

    @_("OCTAVE_UP", "octaves_up OCTAVE_UP")
    def octaves_up(self, p):
        if len(p) == 1:
            return 1
        return p[0] + 1

    @_("NAME")
    def pitch(self, p):
        return name_to_midi(p[0])

    @_("NAME octaves_up")
    def pitch(self, p):
        return name_to_midi(p[0]) + (12 * p[1])

    @_("NAME octaves_down")
    def pitch(self, p):
        return name_to_midi(p[0]) - (12 * p[1])

    @_("pitch", "pitches pitch")
    def pitches(self, p):
        if len(p) == 1:
            return [p[0]]
        p[0].append(p[1])
        return p[0]

    @_("CHORD_OPEN pitches CHORD_CLOSE")
    def chord_pitches(self, p):
        self._previous_pitches = tuple(p[1])
        return p[1]

    @_("chord_pitches duration", "chord_pitches")
    def chord(self, p):
        pitches = tuple(p[0])
        duration = self._previous_duration if len(p) == 1 else p[1]
        return Leaf(pitches=pitches, duration=duration)

    @_("pitch duration", "pitch")
    def note(self, p):
        pitches = (p[0],)
        duration = self._previous_duration if len(p) == 1 else p[1]
        return Leaf(pitches=pitches, duration=duration)

    @_("REST duration", "REST")
    def rest(self, p):
        pitches = ()
        duration = self._previous_duration if len(p) == 1 else p[1]
        return Leaf(pitches=pitches, duration=duration)

    @_("CHORD_REPEAT duration", "CHORD_REPEAT")
    def repeat(self, p):
        pitches = self._previous_pitches
        duration = self._previous_duration if len(p) == 1 else p[1]
        return Leaf(pitches=pitches, duration=duration)

    @_("TIE duration")
    def tie(self, p):
        return p[1]

    @_("chord", "note", "rest", "repeat", "tie")
    def leaf(self, p):
        return p[0]

    @_("leaf", "container", "tuplet")
    def component(self, p):
        return p[0]

    @_("component", "components component")
    def components(self, p):
        if len(p) == 1:
            return [p[0]]
        p[0].append(p[1])
        return p[0]

    @_("CONTAINER_OPEN components CONTAINER_CLOSE")
    def container(self, p):
        return Container(components=p[1], multiplier=1)

    @_("FRACTION container")
    def tuplet(self, p):
        return Container(multiplier=Fraction(p[0]), components=p[1].components)

    @_("components")
    def top(self, p):
        return p[0]

    @_("empty")
    def top(self, p):
        return []

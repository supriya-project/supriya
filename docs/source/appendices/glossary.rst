:status: under-construction

Glossary
========

..  self-criticism::

    These docs are still under construction.

..  glossary::
    :sorted:

    add action
        A directive, passed when creating or moving a :term:`node`, which says
        where the node should be placed in the :term:`node tree` relative to a
        target node: at the :term:`head` or :term:`tail` of a target
        :term:`group`, or immediately before or after a target node. Also
        available are actions that replace the target.

    ADSR
        An :term:`envelope` with four stages: :term:`attack`, :term:`decay`,
        :term:`sustain` and :term:`release`. The first three stages begin when
        the envelope is triggered, while the release stage begins when the
        trigger ends (e.g. when a key is let go).

    allocate
        To set aside sections of memory in a program to be used to store
        variables, and instances of structures and classes.

    allocator
        An object which hands out and reclaims identifiers or regions of memory
        so that no two clients of the allocator receive the same one. Supriya
        uses allocators to lease :term:`node <ID, node>`, :term:`buffer <ID,
        buffer>` and :term:`bus <ID, bus>` IDs.

    amplitude
        The maximum extent of a vibration or oscillation, measured from the
        position of equilibrium.

        See: :term:`decibels`

    amplitude modulation
        A synthesis technique in which the :term:`amplitude` of one signal (the
        carrier) is varied by another signal (the modulator). At audible
        modulation rates it adds sidebands to the carrier's spectrum, while at
        sub-audio rates it produces the effect known as tremolo.

    async
    async/await
        In computer programming, the async/await pattern is a syntactic feature
        of many programming languages that allows an asynchronous, non-blocking
        function to be structured in a way similar to an ordinary synchronous
        function. It is semantically related to the concept of a coroutine and
        is often implemented using similar techniques, and is primarily
        intended to provide opportunities for the program to execute other code
        while waiting for a long-running, asynchronous task to complete,
        usually represented by promises or similar data structures.

    attack
        The first stage of an :term:`envelope`: the time taken for a sound to
        rise from silence to its peak :term:`amplitude`.

    audio rate
        A :term:`calculation rate` where one value is generated for each sample
        in the :term:`sample block <block, of samples>`.

    block, of samples
        A group of consecutive :term:`samples <sample>` computed together as a
        unit by a :term:`unit generator <UGen>`, rather than one at a time. In
        :term:`scsynth`, :term:`audio rate` signals are calculated one block at
        a time, and :term:`control rate` signals once per block.

    block, of IDs
        A contiguous run of :term:`IDs <ID>` allocated together, such as the
        IDs of the buses in a :term:`bus group <group, of buses>` or the
        buffers in a :term:`buffer group <group, of buffers>`.

    block size
        The size of a block of samples

    bit depth
        The number of bits of information in each sample, directly
        corresponding to the resolution of each sample.

    buffer
        An array of sample data, used - for example - for sound files, delay
        lines, convolution reverb, wavetable synthesis, window functions etc.

    bundle, OSC
        A collection of :term:`OSC` :term:`messages <message, OSC>` and
        :term:`bundles <bundle, OSC>` whose effects must happen simultaneously
        at a given timestamp.

    bus
        In audio engineering, a bus is a signal path which can be used to sum
        individual audio signal paths together.

    calculation rate
        The rate at which values are calculated by a :term:`unit generator
        <UGen>` or :term:`bus`.

        See: :term:`audio rate`, :term:`control rate`, :term:`demand rate`,
        :term:`scalar rate`

    cent
        A logarithmic unit of measure used for musical intervals, which divides
        the :term:`octave` into 12 :term:`semitones <semitone>` of 100 cents
        each in :term:`twelve-tone equal temperament <equal temperament,
        twelve-tone>`.

    channel
        One of the independent streams of :term:`samples <sample>` which make
        up an audio signal, e.g. the left and right channels of a stereo
        signal. :term:`Buffers <buffer>` and :term:`buses <bus>` can be single-
        or multi-channel.

    client
        A program that sends :term:`requests <request>` to a :term:`server` and
        handles its :term:`responses <response>`. In :term:`SuperCollider`'s
        architecture, :term:`sclang` and :term:`Supriya` are clients of
        :term:`scsynth`.

    clock
        A source of time which schedules events, whether a wall clock that
        tracks real time or a musical clock which advances according to a
        tempo.

    control
        A named parameter of a :term:`SynthDef` whose value can be set when a
        :term:`synth` is created, changed while the synth is running, or
        mapped to a control :term:`bus`.

    control rate
        A :term:`calculation rate` where one value is generated per :term:`sample
        block <block, of samples>`.

    decay
        The stage of an :term:`envelope` following the :term:`attack`, in which
        :term:`amplitude` falls from its peak to the :term:`sustain` level.
        More broadly, the gradual fading of a sound.

    decibels
        A unit used to measure the intensity of a sound by comparing it with a
        given level on a logarithmic scale; a degree of loudness.

        See: :term:`amplitude`

    default group
        A :term:`group`.

    demand rate
        A :term:`calculation rate` where one value is generated each time the
        connected :py:class:`~supriya.ugens.demand.Demand` :term:`UGen` is
        :term:`triggered <trigger>`.

    depth
        The distance of a :term:`node` from the :term:`root` of a :term:`tree`,
        i.e. the number of edges between them. The root has a depth of zero.

    depth-first
        A way of traversing a :term:`tree` or :term:`graph` which follows each
        branch as far as it will go before backtracking. :term:`scsynth`
        executes its :term:`node tree` depth-first, from :term:`head` to
        :term:`tail`.

    directed graph
    digraph
        A :term:`graph` in which edges have orientations.

    envelope
        A description of how a sound changes over time, typically
        :term:`amplitude`, via a curve joining the successive peaks of a
        modulated wave.

        See: :term:`envelope generator`

    envelope generator
        A :term:`unit generator <UGen>` which produces an :term:`envelope` as a
        control signal, typically to shape the :term:`amplitude` of a sound
        over time.

    equal temperament, twelve-tone
        The musical system that divides the :term:`octave` into 12 parts, all
        of which are equally tempered (equally spaced) on a logarithmic scale,
        with a ratio equal to the 12th root of 2 (12√2 ≈ 1.05946), whose
        resulting smallest interval, 1⁄12 the width of an octave, is called a
        :term:`semitone` or half step.

    event, from a pattern
        A single musical occurrence, such as a note or a rest, represented as a
        collection of named values (e.g. :term:`frequency`, duration,
        :term:`amplitude`) produced by a :term:`pattern`.

    FFT
        A fast Fourier transform

    filter
        A device or algorithm that selectively attenuates or boosts parts of a
        signal's :term:`frequency` spectrum, e.g. a low-pass filter which lets
        lower frequencies through and reduces higher ones.

    fluent interface
        In software engineering, an object-oriented API whose design relies
        extensively on method chaining.

    frame
        A data record that contains the :term:`samples <sample>` for all of the
        :term:`channels <channel>` available in an audio signal.

    free
        To release something previously :term:`allocated <allocate>`, such as a
        :term:`node`, :term:`buffer` or :term:`bus`, so that its resources or
        :term:`ID` can be used again.

    frequency
        The rate at which something occurs or is repeated over a particular
        period of time or in a given sample; the rate at which a vibration
        occurs that constitutes a wave, either in a material (as in sound
        waves), or in an electromagnetic field (as in radio waves and light),
        usually measured per second.

        See: :term:`Hertz`

    frequency domain
        The analysis of mathematical functions or signals with respect to
        frequency, rather than time.

        See: :term:`time domain`

    frequency modulation
        A synthesis technique in which the :term:`frequency` of one
        :term:`oscillator` (the carrier) is varied by the output of another
        (the modulator). At audio rates it generates complex, harmonic or
        inharmonic spectra from just two oscillators.

    grain
        A very short snippet of sound, typically between 1 and 100 milliseconds
        long and shaped by a :term:`window`, used as the building block of
        :term:`granular synthesis`.

    granular synthesis
        A synthesis technique in which sound is built from many overlapping
        :term:`grains <grain>`, produced either from a :term:`buffer` of
        recorded audio or from a synthesized waveform.

    graph
        In mathematics, and more specifically in graph theory, a graph is a
        structure amounting to a set of objects in which some pairs of the
        objects are in some sense "related"; the objects correspond to
        mathematical abstractions called vertices (also called :term:`nodes
        <node>` or points) and each of the related pairs of vertices is called
        an edge (also called link or line).

    GraphViz
        An open source graph visualization software package, which renders
        descriptions of :term:`graphs <graph>` as diagrams. :term:`Supriya` can
        use it to draw :term:`SynthDefs <SynthDef>`.

    group
        A :term:`node` which contains an ordered list of other nodes, its
        children, which may be :term:`synths <synth>` or other groups. Groups
        let you treat a number of nodes as a single unit: you can move, pause
        or free them all at once.

    group, of buffers
        A contiguous :term:`block of IDs <block, of IDs>` for a number of
        :term:`buffers <buffer>` allocated together.

    group, of buses
        A contiguous :term:`block of IDs <block, of IDs>` for a number of
        :term:`buses <bus>` allocated together, often to carry the
        :term:`channels <channel>` of a multi-channel signal.

    head
        The first position in a :term:`group`'s list of children. A node placed
        at a group's head executes before all of that group's other children.

    header format
        The file format used to wrap the audio data in a sound file, e.g. AIFF,
        WAV, FLAC or NeXT/Sun (AU), which describes how to interpret the file's
        :term:`sample format` and :term:`sample rate`.

    Hertz
        The :term:`SI` unit of frequency, equal to one cycle per second.

        See: :term:`frequency`

    ID
        A number which uniquely identifies an object, such as a :term:`node`,
        :term:`buffer` or :term:`bus`, among others of its kind inside a
        :term:`server`.

    ID, buffer
        The integer which identifies a :term:`buffer` inside a :term:`server`,
        used by :term:`UGens <UGen>` and :term:`requests <request>` to refer to
        it.

    ID, bus
        The integer which identifies a :term:`bus` inside a :term:`server`.
        Audio and control buses have separate ID spaces.

    ID, node
        The integer which identifies a :term:`node` inside a :term:`server`,
        used by :term:`requests <request>` to address it.

    IFFT
        An inverse fast Fourier transform

    lag
        A smoothing process which makes a signal approach a new value
        gradually, rather than jumping to it instantly, with a time constant
        controlling how long it takes. Often used to prevent audible clicks
        when a :term:`control` changes abruptly.

    latency
        In computing, the delay before a transfer of data begins following an
        instruction for its transfer.

    message, MIDI
        A unit of :term:`MIDI` data, consisting of a status byte, which
        identifies its type and :term:`channel`, followed by zero or more data
        bytes. Examples include note-on, note-off and control change messages.

    message, OSC
        The basic unit of :term:`OSC` data, consisting of an address pattern
        (e.g. ``/s_new``) followed by a list of typed arguments.

    MIDI
        A technical standard that describes a communications protocol, digital
        interface, and electrical connectors that connect a wide variety of
        electronic musical instruments, computers, and related audio devices
        for playing, editing and recording music.

        See: https://en.wikipedia.org/wiki/MIDI

    multi-channel expansion
        In :term:`SuperCollider`, the behavior by which a :term:`UGen` given an
        array of values for an input will automatically be duplicated, one copy
        for each element, yielding a multi-:term:`channel` output.

    MUSIC-N
        A family of computer music programs and programming languages descended
        from or influenced by MUSIC, a program written by Max Mathews in 1957
        at Bell Labs, which was the first computer program for generating
        digital audio waveforms through direct synthesis.

    node
    vertex
        In graph theory, the fundamental unit of which graphs are formed.

    node tree
        The tree of :term:`nodes <node>` that make up a :term:`server`'s
        synthesis state, with :term:`groups <group>` as branches, :term:`synths
        <synth>` as leaves, and the :term:`root node` at the top. It determines
        the order in which synths execute.

    non-realtime
        Relating to a mode of operation where audio is rendered to a file as
        fast as the computer can manage, rather than as it is played back, so
        that processing is not limited by the demands of :term:`realtime`
        performance.

    Nyquist limit
        The highest :term:`frequency` which can be represented in a digitally
        sampled signal without aliasing: half of the :term:`sample rate`.

    OSC
        Open Sound Control, an open, transport-independent, message-based
        protocol developed for communication among computers, sound
        synthesizers, and other multimedia devices.

        :term:`SuperCollider` :term:`clients <client>` and :term:`servers
        <server>` communicate via OSC.

        See: https://opensoundcontrol.stanford.edu/

    octave
        The interval between one musical pitch and another with double its
        :term:`frequency`.

    oscillator
        A signal generator that produces a sinusoidal or non-sinusoidal signal
        of some particular :term:`frequency`.

    output proxy
        In :term:`Supriya`, an object representing a single output
        :term:`channel` of a multi-output :term:`UGen`, so that each output can
        be wired to other UGens individually.

    parent
        The :term:`group` that directly contains a given :term:`node`. Every
        node except the :term:`root node` has exactly one parent.

    parentage
        The chain of :term:`parents <parent>` leading from a given :term:`node`
        up to the :term:`root node`.

    pattern
        An object which describes a sequence of values, or of :term:`events
        <event, from a pattern>`, in a lazy, declarative way, leaving the
        details of generating them to when the pattern is iterated or played.

    phase
        The relationship in time between the successive states or cycles of an
        oscillating or repeating system (such as an alternating electric
        current or a light or sound wave) and either a fixed reference point or
        the states or cycles of another system with which it may or may not be
        in synchrony.

    phase vocoder
        A type of vocoder-purposed algorithm which can interpolate information
        present in the frequency and time domains of audio signals by using
        phase information extracted from a frequency transform.

    proxy
        A client-side object which stands in for a resource that lives
        somewhere else, such as a :term:`node`, :term:`buffer` or :term:`bus`
        inside a running :term:`server`.

    pseudorandom number generator
        An algorithm for generating a sequence of numbers whose properties
        approximate the properties of sequences of random numbers.

    pure unit generator
        A :term:`unit generator <UGen>` which does not have any side effects,
        e.g. accessing (and therefore modifying the state of) a :term:`random
        number generator`; typically an :term:`oscillator`.

    PV Chain
        A :term:`phase vocoder` :term:`UGen` which operates on blocks of
        :term:`frequency` and :term:`phase` data in order to perform spectral
        analysis or transformations.

    Python
        An interpreted high-level general-purpose programming language whose
        design philosophy emphasizes code readability with its use of
        significant indentation, and whose language constructs as well as
        object-oriented approach aim to help programmers write clear, logical
        code for small and large-scale projects.

        See: https://www.python.org/

    random number generator
        A process which generates a sequence of numbers or symbols that cannot
        be reasonably predicted better than by a random chance.

        See :term:`pseudorandom number generator`

    random seed
        A value used to initialize a pseudorandom number generator.

    realtime
        Relating to a system in which input data is processed within
        milliseconds so that it is available virtually immediately as feedback,
        e.g., in a missile guidance or airline booking system.

    release
        The final stage of an :term:`envelope`, in which :term:`amplitude`
        falls from the :term:`sustain` level to silence after a note ends. In
        :term:`SuperCollider`, also used to describe fading out a :term:`synth`
        before freeing it.

    repr
        Short for "representation": the string Python produces for an object
        via the built-in ``repr()`` function, intended to be useful when
        inspecting or debugging, and also the form used when objects are echoed
        in an interactive session.

    request
        A command sent by a :term:`client` to a :term:`server`, such as
        creating a :term:`synth` or setting a :term:`control`, encoded as an
        :term:`OSC` :term:`message <message, OSC>`.

    response
        A message sent by a :term:`server` back to a :term:`client`, either in
        reply to a :term:`request` or to notify it that something happened,
        such as a :term:`node` having been created.

    root
        The topmost :term:`vertex` of a :term:`rooted graph` or :term:`tree`,
        from which all of the other vertices can be reached.

    root node
        The :term:`group` at the top of a :term:`server`'s :term:`node tree`,
        with an :term:`ID <ID, node>` of 0, which contains all other nodes.

    rooted graph
        A (typically :term:`directed <digraph>`) :term:`graph` in which one
        :term:`vertex` has been distinguished as the root.

    sample
        A unit of audio data; a single digital measurement of an analog audio
        source.

    sample format
        The binary representation of a :term:`sample`, e.g. 16-bit signed
        integers or 32-bit floating-point.

    sample rate
        The average number of :term:`samples <sample>` obtained in one second.

    scalar rate
        A :term:`calculation rate`, sometimes called "constant" or
        "initialization" rate, where the value is calculated only once
        regardless of input.

    sclang
        The :term:`SuperCollider` language.

    scsynth
        The :term:`SuperCollider` server.

    semitone
        The interval between two adjacent notes in a 12-tone scale, equal to
        100 :term:`cents <cent>` in twelve-tone equal temperament.

    SI
        The international system of units of measurement, from the French
        `Système International`.

    signal
        A representation of sound, typically using either a changing level of
        electrical voltage for analog signals, or a series of binary numbers
        for digital signals.

    state machine
        An abstract model of computation which is always in exactly one of a
        finite number of states, and which changes between them in response to
        inputs.

    state transition
        The change of a :term:`state machine` from one state to another, as
        triggered by an input or event.

    supernova
        An alternative :term:`SuperCollider` server implementation that
        utilizes parallel processing.

    server
        A program which waits for, and carries out, :term:`requests <request>`
        from one or more :term:`clients <client>`. In :term:`SuperCollider`,
        the synthesis engine :term:`scsynth` is a server.

    session
        A bounded period of interaction with a :term:`server`, from when it is
        booted to when it quits.

    spatialization
        The process of placing sounds in a perceived space, e.g. by panning
        between loudspeaker :term:`channels <channel>`, or by modelling
        distance, reflections and head-related cues.

    Sphinx
        A documentation generator which converts reStructuredText into HTML and
        other formats, and which is used to build these docs.

    subtree
        A :term:`node` of a :term:`tree`, together with all of its descendants.
        In a :term:`node tree`, for example, a :term:`group` and everything
        inside it.

    SuperCollider
        An environment and programming language originally released in 1996 by
        James McCartney for real-time audio synthesis and algorithmic
        composition, which has since evolved into a system used and further
        developed by both scientists and artists working with sound.

        See: https://supercollider.github.io/

    Supriya
        A :term:`Python` API for :term:`SuperCollider`.

    sustain
        The stage of an :term:`envelope` during which :term:`amplitude` holds
        steady for as long as a note is held, between the :term:`decay` and
        :term:`release` stages.

    synth
        Short for :term:`synthesizer`; in :term:`SuperCollider`, an instance of
        a :term:`SynthDef`.

    SynthDef
        A :term:`graph` of :term:`unit generators <UGen>`.

    synthesizer
        An electronic musical instrument, typically operated by a keyboard,
        producing a wide variety of sounds by generating and combining signals
        of different frequencies.

    tail
        The last position in a :term:`group`'s list of children. A node placed
        at a group's tail executes after all of that group's other children.

    TCP
        Transmission Control Protocol, a communications standard that enables
        application programs and computing devices to exchange messages over a
        network, designed to send packets across the internet and ensure the
        successful delivery of data and messages over networks.

    time domain
        The analysis of mathematical functions, physical signals or time series
        data (e.g. environmental or economic), with respect to time.

        See: :term:`frequency domain`

    tree
        In graph theory, a tree is an undirected :term:`graph` in which any two
        :term:`vertices <node>` are connected by exactly one path, or
        equivalently a connected acyclic undirected graph; the various kinds of
        data structures referred to as trees in computer science have
        underlying graphs that are trees in graph theory, although such data
        structures are generally rooted trees.

        See: :term:`rooted graph`

    trigger
        A signal or event that tells something to start happening, e.g. a
        transition from non-positive to positive in a signal which fires an
        :term:`envelope` or a :term:`demand rate` :term:`UGen`.

    UDP
        User Datagram Protocol, a lightweight data transport protocol that
        works on top of IP, providing a mechanism to detect corrupt data in
        packets, but which does not attempt to solve other problems that arise
        with packets, such as lost or out of order packets.

    UGen
        A unit generator, the basic formal units in many :term:`MUSIC-N-style
        <MUSIC-N>` computer music programming languages, which form the
        building blocks for designing synthesis and signal processing
        algorithms.

    wavetable synthesis
        A synthesis technique in which an :term:`oscillator` reads repeatedly
        through a table of stored waveform :term:`samples <sample>`, often
        sweeping between several waveforms to evolve the timbre.

    window
        A function which is zero outside of a chosen interval and tapers toward
        its edges, used to shape a short segment of a signal, e.g. to fade
        :term:`grains <grain>` in and out or to reduce artifacts when applying
        an :term:`FFT`.

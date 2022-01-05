Glossary
========

.. glossary::
   :sorted:

   add action
      TBD

   ADSR
      TBD

   allocate
      To set aside sections of memory in a program to be used to store
      variables, and instances of structures and classes.

   allocator
      TBD

   amplitude
      The maximum extent of a vibration or oscillation, measured from the
      position of equilibrium.

      See: :term:`decibels`

   amplitude modulation
      TBD

   async
   async/await
      In computer programming, the async/await pattern is a syntactic feature
      of many programming languages that allows an asynchronous, non-blocking
      function to be structured in a way similar to an ordinary synchronous
      function. It is semantically related to the concept of a coroutine and is
      often implemented using similar techniques, and is primarily intended to
      provide opportunities for the program to execute other code while waiting
      for a long-running, asynchronous task to complete, usually represented by
      promises or similar data structures.

   attack
      TBD

   audio rate
      A :term:`calculation rate` where one value is generated for each sample
      in the :term:`sample block <block, of samples>`.

   block, of samples
      TBD

   block, of IDs
      TBD

   block size
      The size of a block of samples

   bit depth
      The number of bits of information in each sample, directly corresponding
      to the resolution of each sample.

   buffer
      An array of sample data, used - for example - for sound files, delay
      lines, convolution reverb, wavetable synthesis, window functions etc.

   bundle, OSC
      A collection of :term:`OSC` :term:`messages <message, OSC>` and
      :term:`bundles <bundle, OSC>` whose effects must happen simultaneously at
      a given timestamp.

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
      the :term:`octave` into 12 :term:`semitones <semitone>` of 100 cents each
      in :term:`twelve-tone equal temperament <equal temperament, twelve-tone>`.

   channel
      TBD

   client
      TBD

   clock
      TBD

   control
      TBD

   control rate
      A :term:`calculation rate` where one value is generated per :term:`sample
      block <block, of samples>`.

   decay
      TBD

   decibels
      A unit used to measure the intensity of a sound by comparing it with a
      given level on a logarithmic scale; a degree of loudness.

      See: :term:`amplitude`

   default group
      A :term:`group`.

   demand rate
      A :term:`calculation rate` where one value is generated each time the
      connected :py:class:`~supriya.ugens.demand.Demand` :term:`UGen` is :term:`triggered <trigger>`.

   depth
      TBD

   depth-first
      TBD

   directed graph
   digraph
      A :term:`graph` in which edges have orientations.

   envelope
      A description of how a sound changes over time, typically
      :term:`amplitude`, via a curve joining the successive peaks of a
      modulated wave.

      See: :term:`envelope generator`

   envelope generator
      TBD

   equal temperament, twelve-tone
      The musical system that divides the :term:`octave` into 12 parts, all of
      which are equally tempered (equally spaced) on a logarithmic scale, with
      a ratio equal to the 12th root of 2 (12√2 ≈ 1.05946), whose resulting
      smallest interval, 1⁄12 the width of an octave, is called a
      :term:`semitone` or half step.

   event, from a pattern
      TBD

   FFT
      A fast Fourier transform

   filter
      TBD

   fluent interface
      In software engineering, an object-oriented API whose design relies
      extensively on method chaining.

   frame
      A data record that contains the :term:`samples <sample>` for all of the
      :term:`channels <channel>` available in an audio signal.

   free
      TBD

   frequency
      The rate at which something occurs or is repeated over a particular
      period of time or in a given sample; the rate at which a vibration occurs
      that constitutes a wave, either in a material (as in sound waves), or in
      an electromagnetic field (as in radio waves and light), usually measured
      per second.

      See: :term:`Hertz`

   frequency domain
      The analysis of mathematical functions or signals with respect to
      frequency, rather than time.

      See: :term:`time domain`

   frequency modulation
      TBD

   grain
      TBD

   granular synthesis
      TBD

   graph
      In mathematics, and more specifically in graph theory, a graph is a
      structure amounting to a set of objects in which some pairs of the
      objects are in some sense "related"; the objects correspond to
      mathematical abstractions called vertices (also called :term:`nodes
      <node>` or points) and each of the related pairs of vertices is called an
      edge (also called link or line).

   GraphViz
      TBD

   group
      TBD

   group, of buffers
      TBD

   group, of buses
      TBD

   head
      TBD

   header format
      TBD

   Hertz
      The :term:`SI` unit of frequency, equal to one cycle per second.

      See: :term:`frequency`

   ID
      TBD

   ID, buffer
      TBD

   ID, bus
      TBD

   ID, node
      TBD

   IFFT
      An inverse fast Fourier transform

   lag
      TBD

   latency
      In computing, the delay before a transfer of data begins following an
      instruction for its transfer.

   message, MIDI
      TBD

   message, OSC
      TBD

   MIDI
      A technical standard that describes a communications protocol, digital
      interface, and electrical connectors that connect a wide variety of
      electronic musical instruments, computers, and related audio devices for
      playing, editing and recording music.

      See: https://en.wikipedia.org/wiki/MIDI

   moment, non-realtime
      TBD

   multi-channel expansion
      TBD

   MUSIC-N
      A family of computer music programs and programming languages descended
      from or influenced by MUSIC, a program written by Max Mathews in 1957 at
      Bell Labs, which was the first computer program for generating digital
      audio waveforms through direct synthesis.

   node
   vertex
      In graph theory, the fundamental unit of which graphs are formed.

   node tree
      TBD

   non-realtime
      TBD

   Nyquist limit
      TBD

   OSC
      Open Sound Control, an open, transport-independent, message-based
      protocol developed for communication among computers, sound synthesizers,
      and other multimedia devices.

      :term:`SuperCollider` :term:`clients <client>` and :term:`servers
      <server>` communicate via OSC.

      See: http://opensoundcontrol.org/spec-1_0

   octave
      The interval between one musical pitch and another with double its
      :term:`frequency`.

   oscillator
      A signal generator that produces a sinusoidal or non-sinusoidal signal of
      some particular :term:`frequency`.

   output proxy
      TBD

   parent
      TBD

   parentage
      TBD

   pattern
      TBD

   phase
      The relationship in time between the successive states or cycles of an
      oscillating or repeating system (such as an alternating electric current
      or a light or sound wave) and either a fixed reference point or the
      states or cycles of another system with which it may or may not be in
      synchrony.

   phase vocoder
      A type of vocoder-purposed algorithm which can interpolate information
      present in the frequency and time domains of audio signals by using phase
      information extracted from a frequency transform.

   proxy
      TBD

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
      design philosophy emphasizes code readability with its use of significant
      indentation, and whose language constructs as well as object-oriented
      approach aim to help programmers write clear, logical code for small and
      large-scale projects.

      See: https://www.python.org/

   random number generator
      A process which generates a sequence of numbers or symbols that cannot be
      reasonably predicted better than by a random chance.
      
      See :term:`pseudorandom number generator`

   random seed
      A value used to initialize a pseudorandom number generator.

   realtime
      Relating to a system in which input data is processed within milliseconds
      so that it is available virtually immediately as feedback, e.g., in a
      missile guidance or airline booking system.

   release
      TBD

   repr
      TBD

   request
      TBD

   response
      TBD

   root
      TBD

   root node
      TBD

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
      "initialization" rate, where the value is calculated only once regardless
      of input.

   sclang
      The :term:`SuperCollider` language.

   scsynth
      The :term:`SuperCollider` server.

   semitone
      The interval between two adjacent notes in a 12-tone scale, equal to 100
      :term:`cents <cent>` in twelve-tone equal temperament.

   SI
      The international system of units of measurement, from the French
      `Système International`.

   signal
      A representation of sound, typically using either a changing level of
      electrical voltage for analog signals, or a series of binary numbers for
      digital signals. 

   state, non-realtime
      TBD

   state machine
      TBD

   state transition
      TBD

   supernova
      An alternative :term:`SuperCollider` server implementation that utilizes
      parallel processing.

   server
      TBD

   session
      TBD

   spatialization
      TBD

   Sphinx
      TBD

   subtree
      TBD

   SuperCollider
      An environment and programming language originally released in 1996 by
      James McCartney for real-time audio synthesis and algorithmic
      composition, which has since evolved into a system used and further
      developed by both scientists and artists working with sound.

      See: https://supercollider.github.io/

   Supriya
      A :term:`Python` API for :term:`SuperCollider`.

   sustain
      TBD

   synth
      Short for :term:`synthesizer`; in :term:`SuperCollider`, an instance of a
      :term:`SynthDef`.

   SynthDef
      A :term:`graph` of :term:`unit generators <UGen>`.

   synthesizer
      An electronic musical instrument, typically operated by a keyboard,
      producing a wide variety of sounds by generating and combining signals of
      different frequencies.

   tail
      TBD

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
      data structures referred to as trees in computer science have underlying
      graphs that are trees in graph theory, although such data structures are
      generally rooted trees.

      See: :term:`rooted graph`

   trigger
      TBD

   UDP
      User Datagram Protocol, a lightweight data transport protocol that works
      on top of IP, providing a mechanism to detect corrupt data in packets,
      but which does not attempt to solve other problems that arise with
      packets, such as lost or out of order packets.

   UGen
      A unit generator, the basic formal units in many :term:`MUSIC-N-style
      <MUSIC-N>` computer music programming languages, which form the building
      blocks for designing synthesis and signal processing algorithms.

   wavetable synthesis
      TBD

   window
      TBD

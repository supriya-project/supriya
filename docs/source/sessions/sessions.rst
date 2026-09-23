:icon: octicons/beaker-16

Sessions
========

.. important::

   This is a provisional, *labs* feature.

   Sessions will likely change extensively over the coming months and years.

.. self-criticism::

   Under construction.

Supriya's Sessions provide higher-level affordances for building DAW-like
applications, such as mixing boards, trackers, live performance environments,
headless installations, etc. inspired by patterns found in commercial software
like Reaper and Ableton Live.

Each session represents a tree of components: mixers, tracks (including
sub-tracks), and devices (including audio effects and instruments). A mixer
represents a set of tracks running on a single synthesis context, while a track
represents a single audio stream (typically for a single sound element within a
mix) and potentially a submix of other child tracks. Devices provide high level
wrappers around discrete changes to an audio signal, adding to or modifying
their track's sound element in the mix.

A session can manage multiple mixers at once, each performed on a separate
server process. Sessions, mixers and tracks support heterogenous channel counts
and will up- or down-mix when sending or receiving audio to other components.

Session components manage their server state through a process called
"reconciliation", inspired by IaC tools like Terraform. They attempt to
reconcile their desired state against their last known state of changes applied
against the server.

Lifecycle
---------

Instantiate a session with::

    >>> session = supriya.Session()

Like servers, sessions are initially *offline*::

    >>> session

To bring a session, and all of its child components online, boot the session::

    >>> await session.boot()

Quit a running session::

    >>> await session.quit()

Inspection
----------

Any component in a session can be inspected.

Let's create a simple session - one mixer and two tracks, with a send from the
second track to the first - and inspect the various component's properties::

    >>> session = supriya.Session()
    >>> await session.boot()
    >>> mixer = await session.add_mixer(name="Mixer")
    >>> track_one = await mixer.add_track(name="Track One")
    >>> track_two = await mixer.add_track(name="Track Two")
    >>> send = await track_two.add_send(target=track_one)

We can walk the component tree depth-first with ``Component.walk()``::

    >>> for component in session.walk():
    ...     print(component)
    ...

We'll use this iteration to help inspect each component's various properties.

Components properties
`````````````````````

Every component has a *numeric ID*::

    >>> for component in session.walk():
    ...     print(component, component.id)
    ...

Every component also has a "nested" and "numeric" *address*::

    >>> for component in session.walk():
    ...     print(component)
    ...     print("   ", component.address)
    ...     print("   ", component.numeric_address)
    ...

Every component that's part of a session's tree has references to that
*session*, to the *mixer* it's housed under, and to the synthesis *context*
it's currently using (if any)::

    >>> for component in session.walk():
    ...     print(component)
    ...     print("   ", component.session)
    ...     print("   ", component.mixer)
    ...     print("   ", component.context)
    ...

Components know about their *parent* component (if any), and to their *children*::

    >>> for component in session.walk():
    ...     print(component)
    ...     print("   ", component.parent)
    ...     print("   ", component.children)
    ...

They also know about their *graph order*, a tuple of integers describing the index
of a component in its parent, its parent's index in *its* parent, etc.::

    >>> for component in session.walk():
    ...     print(component)
    ...     print("   ", component.graph_order)
    ...

Finally, most component's can be explicitly named, and their *names* inspected::

    >>> for component in session.walk():
    ...     print(component)
    ...     print("   ", component.name)
    ...

Dumping component trees
```````````````````````

We can dump the session's component tree::

    >>> print(session.dump_components())

We can also dump the session's *server* tree, which is an annotated variation
of the standard ``AsyncServer.query_tree()`` output::

    >>> print(await session.dump_tree())

.. info::

    The first line in the output is a representation of the synthesis context
    that the dumped tree is running under. A session can host multiple
    synthesis contexts at once, and a session's server tree output will reflect
    each of them.

Nodes in the ``dump_tree()`` output are annotated with the component's *nested*
address by default, but can we request *numeric* annotations or no annotations
at all::

    >>> print(await session.dump_tree(annotation_style="numeric"))
    >>> print(await session.dump_tree(annotation_style=None))

.. hint::

    Numeric and null annotations are useful when writing unit tests that
    involve moving or deleting component subtrees because nested addresses can
    change during deletion or other mutations, while numeric addresses won't.

Finding components
``````````````````

Components can be looked up in a session via their nested address::

    >>> session["mixers[0]"]
    >>> session["mixers[0].tracks[0]"]
    >>> session["mixers[0].tracks[1]"]
    >>> session["mixers[0].tracks[1].sends[0]"]

Mutation
--------

Modifying a session's component tree.

Implications for locking.

Adding components
`````````````````

- Session.add_mixer()
- TrackContainer.add_track()
- DeviceContainer.add_device()

Adding devices
``````````````

- More about adding devices.
- Audio effects
- Instruments
- Polyphony

Deleting components
```````````````````

- Mixer.delete()
- Track.delete()
- Device.delete()

Moving components
`````````````````

- Track.move()
- Device.move()

Grouping components
```````````````````

- TrackContainer.group_tracks()
- Track.ungroup()

Managing contexts
`````````````````

- Session.contexts
- Session.add_context()
- Session.set_mixer_context()
- Session.delete_context()

Routing
-------

TODO: Implications for feedback.

Inputs and outputs
``````````````````

- Track.input
- Track.output
- Track.set_output()
- Track.set_input()

Sends
`````

- Track.add_send()
- TrackSend.postfader
- TrackSend.delete

Gain
````

- Mixer.parameters["gain"]
- Track.parameters["gain"]
- TrackSend.parameters["gain"]

Monitoring
``````````

- Track.input_levels
- Track.output_levels
- Mixer.input_levels
- Mixer.output_levels

Up- and down-mixing
```````````````````

- Component.channel_count
- Component.effective_channel_count
- Session.set_channel_count()
- Mixer.set_channel_count()
- Track.set_channel_count()

Muting and soloing
``````````````````

- Track.set_muted()
- Track.set_soloed()
- Track.is_muted
- Track.is_soloed
- Track.is_active

Extension
---------

Configuring devices
```````````````````

Configuring audio effects
`````````````````````````

Configuring instruments
```````````````````````

Writing new devices
```````````````````

Reconciliation
``````````````

Specs
`````

Performance
-----------

Performance events
``````````````````

Input devices
`````````````

Bindings
````````

Patterns
````````

Transport
`````````

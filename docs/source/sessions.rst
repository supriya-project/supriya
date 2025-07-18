Sessions
========

Supriya's Sessions provide higher-level affordances for building DAW-like
applications, such as mixing boards, trackers, live performance environments,
headless installations, etc. inspired by patterns found in commercial software
like Reaper and Ableton Live.

Each session holds a tree of components: mixers, tracks (including sub-tracks),
and devices (including audio effects and instruments). A mixer represents a set
of tracks running on a single synthesis context, while a track represents a
single audio stream (typically for a single sound element within a mix) and
potentially a submix of other child tracks. Devices provide high level wrappers
around discrete changes to an audio signal, adding to or modifying their
track's sound element in the mix.

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

Components properties
`````````````````````

- Component.id
- Component.address
- Component.nested_address
- Component.session
- Component.mixer
- Component.context
- Component.parent
- Component.children
- Component.graph_order

Dumping session states
``````````````````````

- Component.dump_components()
- Component.dump_tree()

Finding components
``````````````````

- Session.__getitem__()

Mutation
--------

Modifying a session's component tree.

Implications for locking.

Adding components
`````````````````

- Session.add_mixer()
- TrackContainer.add_track()
- DeviceContainer.add_device()

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

Connection
----------

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

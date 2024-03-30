Nodes
=====

SuperCollider's :term:`scsynth` server processes audio by traversaing a
:term:`tree` of :term:`nodes <node>`. Nodes in the tree can be either
:term:`groups <group>` - which *group* together other nodes - or :term:`synths
<synth>` - which perform some kind of audio processing.

During every :term:`sample block <block, of samples>` the server visits each
node in its tree in :term:`depth-first` order, starting from the :term:`root
node`, and performs their audio logic. This traversal order makes the
*position* of those nodes relative to one another significant (*was the reverb
performed before or after the sample was played?*).  Nodes can be added or
removed from the server at any point while online, allowing you to manipulate
the audio processing :term:`graph` dynamically.

While :term:`scsynth`'s nodes "live" inside the server, Supriya provides
:term:`proxy <proxy>` classes for manipulating and inspecting them in Python.

Let's dig in...

Lifecycle
---------

Nodes can only be added to running servers, so let's create one and boot it::

    >>> server = supriya.Server().boot()

.. note::

   :py:class:`Scores <supriya.contexts.nonrealtime.Score>` are neither online
   nor offline, so you can add nodes to them whenever you like.

Creating groups
```````````````

Create a group, and print its :term:`repr` to the terminal::

    >>> group_one = server.add_group()
    >>> group_one

The :term:`repr` shows the group's type (``Group``), its :term:`ID <ID, node>`
(``1000``), and indicates it has been allocated (``+``).

Positioning
```````````

Let's add another group. Groups can be added relative to other groups::

    >>> group_two = group_one.add_group()

Where was the second group added? Query the server to see::

    >>> print(server.query_tree())

The second group (``1001``) was added *within* the first (``1000``), which
seems obvious in retrospect. Let's add a third group to the first, and query
the server's node tree again::

    >>> group_three = group_one.add_group()
    >>> print(server.query_tree())

The third group (``1002``) was - *again* - added within the first (``1000``), but
appears *before* the second (``1001``).

By default, adding nodes to a group adds them to the :term:`head` of the group,
rather than the :term:`tail` (which is identical behavior to :term:`sclang`).
When adding nodes to the :term:`node tree`, every node must be added relative
to another node - before, after, at the beginning (the head) or at the end (the
tail) - and we can control that relative position with an :term:`add action`.

Supriya implements :term:`add actions <add action>` as the enumeration
:py:class:`~supriya.enums.AddAction`::

    >>> for x in supriya.AddAction: x
    ...

Use :py:class:`~supriya.enums.AddAction` to position new groups relative to the
first::

    >>> group_four = group_one.add_group(add_action=supriya.AddAction.ADD_AFTER)
    >>> print(server.query_tree())
    >>> group_five = group_one.add_group(add_action=supriya.AddAction.ADD_BEFORE)
    >>> print(server.query_tree())
    >>> group_six = group_one.add_group(add_action=supriya.AddAction.ADD_TO_HEAD)
    >>> print(server.query_tree())
    >>> group_seven = group_one.add_group(add_action=supriya.AddAction.ADD_TO_TAIL)
    >>> print(server.query_tree())
    >>> group_eight = group_one.add_group(add_action=supriya.AddAction.REPLACE)
    >>> print(server.query_tree())

.. note::

    Supriya will attempt to coerce a variety of inputs into a valid
    :py:class:`~supriya.enums.AddAction`::

        >>> for x in [None, 0, "ADD_TO_HEAD", "add_to_head", "add to head"]:
        ...     supriya.AddAction.from_expr(x)
        ...

    This allows you to specify the :term:`add action` via a string, saving a
    few keystrokes::

        >>> server.add_group(add_action="add to head")

.. note::

    When using :term:`supernova` as your server executable, you can create
    _parallel_ groups by specifying ``parallel=True`` in any call you would use
    to create a group::

        >>> server.add_group(parallel=True)

    Parallel groups will process their child nodes via multiple threads.
    Because the order of node processing within a parallel group is
    non-deterministic they're best suited for summing together signals rather
    than processing in-place.

Creating synths
```````````````

Now, reset the server, then create a synth, and print its :term:`repr` to the
terminal::

    >>> server.reset()
    >>> with server.at():
    ...     with server.add_synthdefs(supriya.default):
    ...         synth = server.add_synth(supriya.default)
    ...
    >>> synth

The :term:`repr` shows the synths's type (``Synth``), its :term:`ID <ID, node>`
(``1000``), its :term:`SynthDef` name (``default``), and indicates it has been
allocated (``+``). We discuss synth definitions in depth :doc:`later
<../synthdefs>`, but suffice it to say a :term:`SynthDef` represents a
graph of operators that do audio processing. If that sounds fractally like what
we're already discussing, you're not wrong. It's graphs all the way down.

So far we've only used the "default" SynthDef, which generates a simple stereo
sawtooth wave. Let's create two more.

This SynthDef generates a continuous train of clicks::

    >>> with supriya.SynthDefBuilder(amplitude=0.5, frequency=1.0, out=0) as builder:
    ...     impulse = supriya.ugens.Impulse.ar( 
    ...         frequency=builder["frequency"],
    ...     )
    ...     source = impulse * builder["amplitude"]
    ...     out = supriya.ugens.Out.ar(
    ...         bus=builder["out"],
    ...         source=[source, source],
    ...     )
    ...
    >>> ticker_synthdef = builder.build(name="ticker")

This SynthDef reads audio from a bus, reverberates it, then writes back the
wet audio mixed with the dry::

    >>> with supriya.SynthDefBuilder(damping=0.5, mix=0.5, out=0, room_size=0.5) as builder:
    ...     in_ = supriya.ugens.In.ar(
    ...         bus=builder["out"],
    ...         channel_count=2,
    ...     )
    ...     reverb = supriya.ugens.FreeVerb.ar(
    ...         damping=builder["damping"],
    ...         mix=builder["mix"],
    ...         room_size=builder["room_size"],
    ...         source=in_,
    ...     ) 
    ...     out = supriya.ugens.ReplaceOut.ar(
    ...         bus=builder["out"],
    ...         source=reverb,
    ...     )
    ...
    >>> reverb_synthdef = builder.build(name="reverb")
  
Create a synth using the "ticker" SynthDef, replacing the "default" synth we
just created::

    >>> with server.at():
    ...     with server.add_synthdefs(ticker_synthdef):
    ...         synth.add_synth(ticker_synthdef, frequency=4, add_action="replace")
    ...

Then create a second synth using the "reverb" SynthDef, positioning it after
the previous synth with an ``ADD_TO_TAIL`` :term:`add action`::

    >>> with server.at():
    ...     with server.add_synthdefs(reverb_synthdef):
    ...         server.add_synth(reverb_synthdef, add_action="add_to_tail")
    ... 

Note the order of the two synths (you can tell by their SynthDef names), and
how the reverberation kicks in when you instantiate the second synth::

    >>> print(server.query_tree())

.. note::

    Supriya keeps track of which SynthDefs have already been allocated, and
    will automatically allocate them for you when you add synths to the server.
    If you need precise timing, make sure to pre-allocate the SynthDefs.

    See :doc:`../synthdefs` and :doc:`../osc` for more details.

Deleting
````````

Reset the server for a clean slate, then add a synth::

    >>> server.reset()

::

    >>> with server.at():
    ...     with server.add_synthdefs(supriya.default):
    ...         synth = server.add_synth(supriya.default)
    ...

.. book::
    :hide:

    >>> server.sync()  # wait for synthdefs to load

You can remove a node from the server by :term:`freeing <free>` it::

    >>> synth.free()

Note how the audio cuts off abruptly. Freeing nodes terminates them immediately
without any fade-out.

Now add another synth and :term:`release` it::

    >>> synth = server.add_synth(supriya.default)
    >>> synth.free()

Some synths can be :term:`released <release>`, depending on their
:term:`SynthDef`, and will fade out before freeing themselves automatically
from the server. By convention with :term:`sclang`, synths with a ``gate``
control can be released, although it's up to the author of the :term:`SynthDef`
to guarantee they behave as expected.

Groups can also be freed::

    >>> group = server.add_group()
    >>> group.free()

Inspection
----------

Reset the server for a clean slate::

    >>> server.reset()

... then create a group and add three synths to it::

    >>> with server.at():
    ...     group = server.add_group()
    ...     with server.add_synthdefs(supriya.default):
    ...         synth_a = group.add_synth(supriya.default, frequency=333)
    ...         synth_b = group.add_synth(supriya.default, frequency=444)
    ...         synth_c = group.add_synth(supriya.default, frequency=555)
    ...

.. book::
    :hide:

    >>> server.sync()  # wait for synthdefs to load

Every node has a ``id_`` and a reference to its context::

    >>> group.id_, group.context
    >>> synth_a.id_, synth_a.context
    >>> synth_b.id_, synth_b.context
    >>> synth_c.id_, synth_c.context

.. book::
    :hide:

    >>> server.sync()

Position
````````

Nodes know about their position in the :term:`node tree`.

.. caution::

    This position information is cached on our realtime context based off of
    the various ``/n_go`` and ``/n_end`` messages sent back by :term:`scsynth`,
    so must be taken with a grain of salt - it may be stale by the time you act
    upon it.

The synths we created know that the group we (also) created is their :term:`parent`::

    >>> synth_a.parent

And they know the entire :term:`parentage` between themself and their :term:`root`::

    >>> for node in synth_a.parentage:
    ...     node
    ...

Likewise, the group we created knows about its children::

    >>> for node in group.children:
    ...     node
    ...

Querying controls
`````````````````

We can query each synth's ``frequency`` and ``amplitude``::

    >>> synth_a.get("frequency", "amplitude")
    >>> synth_b.get("frequency", "amplitude")
    >>> synth_c.get("frequency", "amplitude")

Interaction
-----------

Reset the server for a clean slate::

    >>> server.reset()

... then add a group, a *ticker* synth and a *reverb* synth using the two
:term:`SynthDefs <SynthDef>` we defined earlier::

    >>> with server.at():
    ...     group = server.add_group()
    ...     with server.add_synthdefs(ticker_synthdef, reverb_synthdef):
    ...         ticker_synth = group.add_synth(ticker_synthdef)
    ...         reverb_synth = group.add_synth(reverb_synthdef, add_action="add_to_tail")
    ...

.. book::
    :hide:

    >>> server.sync()  # wait for synthdefs to load

Note the click train emitted by the *ticker* synth and the reverberation added
by the *reverb* synth. 

Now we'll interact with these three nodes to modify their sound ...

Moving
``````

Nodes can be moved relative to other nodes, using the same :term:`add actions
<add action>` used when allocating nodes.

Move the *reverb* synth to the :term:`head` of its parent group - *before* the
*ticker* synth - and notice how the click train's reverberation dies out::

    >>> reverb_synth.move(group, "add_to_head")
    >>> print(server.query_tree())

Now move the *reverb* synth *after* the *ticker* synth, and listen to the
reverberation return::

    >>> reverb_synth.move(ticker_synth, "add_after")
    >>> print(server.query_tree())

Setting controls
````````````````

Setting controls on nodes via :py:meth:`~supriya.contexts.entities.Node.set`.

Change the *ticker* synth's frequency control to ``1`` :term:`Hertz`, clicking
once every second::

    >>> ticker_synth.set(frequency=1)

Change the *reverb* synth's "room-size" control to ``0.1`` to reduce the size
of the simulated reverb space::

    >>> reverb_synth.set(room_size=0.1)

Multiple controls can be set on a synth simultaneously. Let's create a long
bright reverb by changing both the reverb's *room size* and its *damping*::

    >>> reverb_synth.set(damping=0.1, room_size=0.95)

Because groups are aware of their child synths' controls, we can set the
control of any of their children by setting it on the group.

Let's set the frequency of the *ticker* synth's click train by setting
``frequency`` on the parent group::

    >>> group.set(frequency=10.0)

The group does not *actually have* a ``frequency`` control - it just propagates
the control setting to any synth in its :term:`subtree`.

Query the node tree to see the control settings::

    >>> print(server.query_tree())

Pausing
```````

Nodes can be paused and unpaused. Paused synths perform no audio processing,
and all children of paused groups are considered paused.

Let's pause the *ticker* synth, and notice how the click train stops::

    >>> ticker_synth.pause()

You can still hear the reverberation from the *reverb* synth since it wasn't
paused.

Unpause the *ticker* synth to resume the click train::

    >>> ticker_synth.unpause()

Now let's pause the *ticker* and *reverb* synths' parent group::

    >>> group.pause()

Notice how audio is completely silenced, both the *ticker*'s click train and
the *reverb*'s reverberation.

Unpause the parent group to resume audio processing::

    >>> group.unpause()

Configuration
-------------

The maximum number of nodes available in a context is controlled by its options.

- Options.maximum_node_count
- Options.initial_node_id

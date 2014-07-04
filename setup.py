#!/usr/bin/env python

import sys
from distutils.core import setup
from distutils.version import StrictVersion

install_requires = [
    'abjad',
    'pexpect',
    'pytest',
    'rtmidi-python',
    'sphinx',
    'tox',
    ]
version = '.'.join(str(x) for x in sys.version_info[:3])
if StrictVersion(version) < StrictVersion('3.4.0'):
    install_requires.append('enum34')
if StrictVersion(version) < StrictVersion('3.3.0'):
    install_requires.append('funcsigs')

long_description = '''
supriya
=======

A Python interface to SuperCollider.

Tested and compatible with Python 2.7, 3.3 and 3.4.

Installation
------------

To install, simply clone **supriya** and run the included `setup.py`:

::

    ~$ git clone https://github.com/josiah-wolf-oberholtzer/supriya.git
    ~$ cd supriya
    supriya$ sudo python setup.py install

To run the test suite:

::

    supriya$ tox

Dependencies
------------

Make sure that SuperCollider is installed, and that `scsynth` is available from
the command-line.

Python dependencies for all Python versions:

- abjad
- pexpect
- pytest
- rtmidi-python
- sphinx
- tox

On Python 2.7:

- funcsigs
- enum34

On Python 3.3:

- enum34

Example
-------

Import packages from **supriya**:

::

    >>> from supriya import servertools
    >>> from supriya import synthdeftools
    >>> from supriya import ugentools

Boot the SuperCollider server:

::

    >>> server = servertools.Server()
    >>> server.boot()
    <Server: udp://127.0.0.1:57751, 8i8o>

Create and allocate a group:

::

    >>> group = servertools.Group().allocate()

Make a synthesizer definition and send it to the server:

::

    >>> synthdef_builder = synthdeftools.SynthDefBuilder(
    ...     amplitude=0.0,
    ...     frequency=440.0,
    ...     )
    >>> sin_osc = ugentools.SinOsc.ar(
    ...     frequency=synthdef_builder['frequency'],
    ...     )
    >>> sin_osc *= synthdef_builder['amplitude']
    >>> out = ugentools.Out.ar(
    ...     bus=(0, 1),
    ...     source=sin_osc,
    ...     )
    >>> synthdef_builder.add_ugen(out)
    >>> synthdef = synthdef_builder.build().allocate(sync=True)

Create a synthesizer with the previously defined synthesizer definition, and
allocate it on the server as a child of the previously created group:

::

    >>> synth = servertools.Synth(synthdef)
    >>> synth.allocate(target_node=group)
    <Synth: 1001>

Query the server's node tree:

::

    >>> response = server.query_remote_nodes(include_controls=True)
    >>> print(response)
    NODE TREE 0 group
        1 group
            1000 group
                1001 f1c3ea5063065be20688f82b415c1108
                    amplitude: 0.0, frequency: 440.0

Quit the server:

::

    >>> server.quit()
    <Server: offline>

'''

setup(
    author='Josiah Wolf Oberholtzer',
    author_email='josiah.oberholtzer@gmail.com',
    description='A Python API for SuperCollider',
    install_requires=install_requires,
    license='GPL',
    long_description=long_description,
    name='supriya',
    packages=('supriya',),
    url='https://github.com/josiah-wolf-oberholtzer/supriya',
    version='0.1',
    )

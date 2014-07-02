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

setup(
    author='Josiah Wolf Oberholtzer',
    author_email='josiah.oberholtzer@gmail.com',
    description='A Python API for SuperCollider',
    install_requires=install_requires,
    license='GPL',
    name='supriya',
    packages=('supriya',),
    url='https://github.com/josiah-wolf-oberholtzer/supriya',
    version='0.1',
    )

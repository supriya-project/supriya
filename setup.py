#!/usr/bin/env python

import os
import sys
import setuptools
from distutils.version import StrictVersion

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

install_requires = [
    'abjad',
    'pexpect',
    'pytest',
    'six',
    'sphinx>=1.3.1',
    'sphinx_rtd_theme',
    'tornado',
    'tox',
    ]
version = '.'.join(str(x) for x in sys.version_info[:3])
if StrictVersion(version) < StrictVersion('3.4.0'):
    install_requires.append('enum34')
if StrictVersion(version) < StrictVersion('3.3.0'):
    install_requires.append('funcsigs')

if not on_rtd:
    install_requires.extend([
        'numpy',
        'python-rtmidi',
        'wavefile',
        ])

with open('README.rst', 'r') as file_pointer:
    long_description = file_pointer.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Artistic Software',
    'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
    ]

entry_points = {
    'console_scripts': [
        'supriya = supriya.tools.systemtools.run_supriya:run_supriya'
        ],
    }

keywords = [
    'audio',
    'dsp',
    'music composition',
    'scsynth',
    'supercollider',
    'synthesis',
    ]


if __name__ == '__main__':
    setuptools.setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        classifiers=classifiers,
        description='A Python API for SuperCollider',
        entry_points=entry_points,
        include_package_data=True,
        install_requires=install_requires,
        keywords=keywords,
        license='MIT',
        long_description=long_description,
        name='supriya',
        packages=['supriya'],
        url='https://github.com/josiah-wolf-oberholtzer/supriya',
        version='0.1',
        zip_safe=False,
        )

#!/usr/bin/env python
import sys
import setuptools
from distutils.version import StrictVersion

install_requires = [
    'PyYAML',
    'appdirs',
    'abjad == 2.21',
    'cython',
    'numpy',
    'pytest-timeout >= 1.2.0',
    'pytest >= 3.0.0',
    'python-rtmidi',
    'sphinx >= 1.5.0',
    'sphinx_rtd_theme >= 0.3.0',
    'tornado',
    'tqdm',
    'uqbar >= 0.2.5',
    'wavefile',
    ]
version = '.'.join(str(x) for x in sys.version_info[:3])
if StrictVersion(version) < StrictVersion('3.4.0'):
    install_requires.append('enum34')
    install_requires.append('pathlib2')

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
        'supriya = supriya.tools.commandlinetools.run_supriya:run_supriya',
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

#!/usr/bin/env python
import pathlib
import sys
from distutils.version import LooseVersion

import setuptools

package_name = "supriya"


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / package_name / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


version = read_version()

install_requires = ["PyYAML", "appdirs", "tqdm", "uqbar >= 0.4.1"]

if LooseVersion(sys.version.split()[0]) < LooseVersion("3.7.0"):
    install_requires.append("dataclasses")

extras_require = {
    "accelerated": ["cython"],
    "ipython": [
        "jupyter",
        "jupyter_contrib_nbextensions",
        "jupyter_nbextensions_configurator",
        "rise",
    ],
    "midi": ["python-rtmidi"],
    "wave": ["wavefile"],
    "test": [
        "black",
        "flake8",
        "isort",
        "mypy >= 0.720",
        "pytest >= 5.0.0",
        "pytest-cov >= 2.7.1",
        "pytest-helpers-namespace >= 2019.1.8",
        "pytest-mock",
        "pytest-rerunfailures >= 7.0",
        "pytest-timeout >= 1.3.3",
    ],
}

with open("README.rst", "r") as file_pointer:
    long_description = file_pointer.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Artistic Software",
    "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
]

entry_points = {"console_scripts": ["supriya = supriya.cli.run_supriya:run_supriya"]}

keywords = [
    "audio",
    "dsp",
    "music composition",
    "scsynth",
    "supercollider",
    "synthesis",
]


if __name__ == "__main__":
    setuptools.setup(
        author="Josiah Wolf Oberholtzer",
        author_email="josiah.oberholtzer@gmail.com",
        classifiers=classifiers,
        description="A Python API for SuperCollider",
        entry_points=entry_points,
        extras_require=extras_require,
        include_package_data=True,
        install_requires=install_requires,
        keywords=keywords,
        license="MIT",
        long_description=long_description,
        name="supriya",
        packages=["supriya"],
        url="https://github.com/josiah-wolf-oberholtzer/supriya",
        version=version,
        zip_safe=False,
    )

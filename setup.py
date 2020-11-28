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

install_requires = ["PyYAML", "appdirs", "tqdm", "uqbar >= 0.5.1"]

if LooseVersion(sys.version.split()[0]) < LooseVersion("3.7.0"):
    install_requires.append("dataclasses")

extras_require = {
    "cython": ["cython"],
    "ipython": [
        "jupyter",
        "jupyter_contrib_nbextensions",
        "jupyter_nbextensions_configurator",
        "rise",
    ],
    "test": [
        "black == 19.10b0",  # Trailing comma behavior in 20.x needs work
        "flake8",
        "isort",
        "mypy >= 0.720",
        "pytest >= 5.4.0",
        "pytest-asyncio >= 0.14.0",
        "pytest-cov >= 2.10.0",
        "pytest-helpers-namespace >= 2019.1.8",
        "pytest-mock",
        "pytest-rerunfailures >= 9.0",
        "pytest-timeout >= 1.4.0",
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
        extras_require=extras_require,
        include_package_data=True,
        install_requires=install_requires,
        keywords=keywords,
        license="MIT",
        long_description=long_description,
        name=package_name,
        packages=[package_name],
        url=f"https://github.com/josiah-wolf-oberholtzer/{package_name}",
        version=version,
        zip_safe=False,
    )

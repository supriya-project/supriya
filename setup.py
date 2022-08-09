#!/usr/bin/env python
import pathlib
import platform

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / "supriya" / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


extensions = [
    Extension(
        "supriya.intervals.IntervalTreeDriverEx",
        language="c",
        sources=["supriya/intervals/IntervalTreeDriverEx.pyx"],
    )
]

if platform.system() != "Windows":
    extensions.append(
        Extension(
            "supriya.realtime.shm",
            include_dirs=[
                "vendor",
                "vendor/TLSF-2.4.6/src",
                "vendor/supercollider/common",
            ],
            language="c++",
            libraries=["rt"] if platform.system() == "Linux" else [],
            sources=["supriya/realtime/shm.pyx"],
        )
    )

if __name__ == "__main__":
    setup(
        ext_modules=cythonize(extensions),
        packages=find_packages(include=["supriya", "supriya.*"])
        + ["supriya.assets.audio", "supriya.assets.audio.birds"],
        version=read_version(),
    )

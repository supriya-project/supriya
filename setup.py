#!/usr/bin/env python
import setuptools

install_requires = [
    "PyYAML",
    "abjad == 3.0.0",
    "appdirs",
    "cython",
    "numpy",
    "python-rtmidi",
    "tornado",
    "tqdm",
    "uqbar >= 0.2.16",
    "wavefile",
]

extras_require = {
    "ipython": ["jupyter", "rise"],
    "test": [
        "black",
        "flake8",
        "isort",
        "mypy >= 0.660",
        "pytest >= 4.1.0",
        "pytest-cov >= 2.6.0",
        "pytest-helpers-namespace >= 2019.1.8",
        "pytest-rerunfailures >= 6.0",
        "pytest-timeout >= 1.3.0",
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
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Artistic Software",
    "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
]

entry_points = {
    "console_scripts": [
        "supriya = supriya.tools.commandlinetools.run_supriya:run_supriya"
    ]
}

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
        version="0.1",
        zip_safe=False,
    )

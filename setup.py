#!/usr/bin/env python
import pathlib
import platform

from setuptools import Extension, setup

package_name = "supriya"


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / package_name / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


if __name__ == "__main__":
    setup(
        author="Josiah Wolf Oberholtzer",
        author_email="josiah.oberholtzer@gmail.com",
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: MacOS",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Artistic Software",
            "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        ],
        description="A Python API for SuperCollider",
        extras_require={
            "docs": [
                "jinja2 < 3.1.0",  # sphinx-immaterial imports Markup from jinja2, not markupsafe
                "librosa",
                "matplotlib >= 3.3.0",
                "sphinx-design",
                "sphinx-immaterial",
                "sphinx-immaterial @ git+https://git@github.com/josiah-wolf-oberholtzer/sphinx-immaterial@main#egg=sphinx-immaterial",
                "sphinxext-opengraph",
            ],
            "ipython": [
                "jupyter",
                "jupyter_contrib_nbextensions",
                "jupyter_nbextensions_configurator",
                "rise",
            ],
            "test": [
                "black",
                "flake8 >= 5.0.0",
                "isort >= 5.10.0",
                "librosa >= 0.9.0",
                "matplotlib >= 3.3.0",
                "mypy >= 0.971",
                "pytest >= 7.0.0",
                "pytest-asyncio >= 0.19.0",
                "pytest-cov",
                "pytest-helpers-namespace",
                "pytest-mock",
                "pytest-rerunfailures",
                "pytest-timeout",
                "types-PyYAML",
                "types-docutils",
            ],
        },
        ext_modules=[
            Extension(
                "supriya.realtime.shm",
                include_dirs=[
                    "vendor",
                    "vendor/TLSF-2.4.6/src",
                    "vendor/supercollider/common",
                ],
                language="c++",
                libraries=["rt"] if platform.system() == "Linux" else [],
                optional=True,
                sources=["supriya/realtime/shm.pyx"],
            )
        ],
        include_package_data=True,
        install_requires=[
            "Cython >= 0.29.0",
            "PyYAML >= 5.4.0",
            "platformdirs >= 2.4.0",
            "tqdm >= 4.59.0",
            "uqbar >= 0.5.7",
            'typing-extensions; python_version<"3.8"',
        ],
        keywords=[
            "audio",
            "dsp",
            "music composition",
            "scsynth",
            "supercollider",
            "synthesis",
        ],
        license="MIT",
        long_description=pathlib.Path("README.md").read_text(),
        long_description_content_type="text/markdown",
        name=package_name,
        packages=[package_name],
        url=f"https://github.com/josiah-wolf-oberholtzer/{package_name}",
        version=read_version(),
        zip_safe=False,
    )

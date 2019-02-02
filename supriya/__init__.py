import appdirs  # type: ignore
import configparser  # noqa
import pathlib  # noqa
import pyximport  # type: ignore

pyximport.install(language_level=3)

output_path = pathlib.Path(appdirs.user_cache_dir("supriya", "supriya"))
if not output_path.exists():
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except IOError:
        pass

config = configparser.ConfigParser()
config.read_dict({"core": {"editor": "vim", "scsynth": "scsynth"}})
config_path = pathlib.Path(appdirs.user_config_dir("supriya", "supriya"))
config_path = config_path / "supriya.cfg"
if not config_path.exists():
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w") as file_pointer:
            config.write(file_pointer, True)
    except IOError:
        pass
with config_path.open() as file_pointer:
    config.read_file(file_pointer)

del appdirs
del configparser
del pathlib
del pyximport


def import_structured_package(path, namespace, remove=True, verbose=False):
    import importlib
    import inspect
    import pathlib
    import traceback

    package_path = pathlib.Path(path).resolve().absolute()
    if not package_path.is_dir():
        package_path = package_path.parent()
    # Determine the package import path
    root_path = package_path
    while (root_path.parent / "__init__.py").exists():
        root_path = root_path.parent
    relative_path = package_path.relative_to(root_path)
    package_import_path = ".".join((root_path.name,) + relative_path.parts)
    if verbose:
        print(package_import_path)
    # Find importable modules and import their nominative object
    for module_path in sorted(package_path.iterdir()):
        if verbose:
            print("    {}".format(module_path))
        if module_path.is_dir():
            if verbose:
                print("        Skipping...")
            continue
        else:
            if module_path.suffix not in (".py", ".pyx"):
                if verbose:
                    print("        Skipping...")
                continue
            module_name = module_path.with_suffix("").name
            if module_name == "__init__":
                if verbose:
                    print("        Skipping...")
                continue
        module_import_path = package_import_path + "." + module_name
        if verbose:
            print("        Importing {}:{}".format(module_import_path, module_name))
        module = importlib.import_module(module_import_path)
        try:
            namespace[module_name] = getattr(module, module_name)
        except AttributeError:
            if verbose:
                print("Failed:", module_path)
                traceback.print_exc()
    # Delete this function from the namespace
    this_name = inspect.currentframe().f_code.co_name
    if remove and this_name in namespace:
        del (namespace[this_name])


from supriya._version import __version__, __version_info__  # noqa
from supriya.enums import AddAction, CalculationRate  # noqa
from supriya import utils  # noqa
from supriya.midi import Device  # noqa
from supriya.live import Application, Mixer  # noqa
from supriya.nonrealtime import Session  # noqa
from supriya.realtime import (  # noqa
    Buffer,
    BufferGroup,
    Bus,
    BusGroup,
    Group,
    Server,
    Synth,
)
from supriya.soundfiles import (  # noqa
    HeaderFormat,
    SampleFormat,
    SoundFile,
)
from supriya.synthdefs import (  # noqa
    DoneAction,
    Envelope,
    Parameter,
    ParameterRate,
    Range,
    SynthDef,
    SynthDefBuilder,
    SynthDefFactory,
)
from supriya.system import Assets, Bindable, Binding, bind  # noqa
from supriya.soundfiles import Say  # noqa
from supriya.io import graph, play, render  # noqa
from supriya import assets  # noqa

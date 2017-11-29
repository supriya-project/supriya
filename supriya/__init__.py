import pyximport
pyximport.install()
del(pyximport)


def import_structured_package(
    path,
    namespace,
    remove=True,
    verbose=False,
    ):
    import importlib
    import inspect
    import pathlib
    import traceback
    package_path = pathlib.Path(path).resolve().absolute()
    if not package_path.is_dir():
        package_path = package_path.parent()
    # Determine the package import path
    root_path = package_path
    while (root_path.parent / '__init__.py').exists():
        root_path = root_path.parent
    relative_path = package_path.relative_to(root_path)
    package_import_path = '.'.join((root_path.name,) + relative_path.parts)
    if verbose:
        print(package_import_path)
    # Find importable modules and import their nominative object
    for module_path in sorted(package_path.iterdir()):
        if verbose:
            print(' ' * 3, module_path)
        if module_path.is_dir():
            if verbose:
                print(' ' * 7, 'Skipping...')
            continue
        else:
            if module_path.suffix not in ('.py', '.pyx'):
                if verbose:
                    print(' ' * 7, 'Skipping...')
                continue
            module_name = module_path.with_suffix('').name
            if module_name == '__init__':
                if verbose:
                    print(' ' * 7, 'Skipping...')
                continue
        module_import_path = package_import_path + '.' + module_name
        if verbose:
            print(' ' * 7, '{}:{}'.format(module_import_path, module_name))
        module = importlib.import_module(module_import_path)
        try:
            namespace[module_name] = getattr(module, module_name)
        except AttributeError:
            if verbose:
                print('Failed:', module_path)
                traceback.print_exc()
    # Delete this function from the namespace
    this_name = inspect.currentframe().f_code.co_name
    if remove and this_name in namespace:
        del(namespace[this_name])


from supriya import utils  # noqa
from supriya.tools.miditools import Device  # noqa
from supriya.tools.livetools import Application, Mixer  # noqa
from supriya.tools.nonrealtimetools import Session  # noqa
from supriya.tools.servertools import (  # noqa
    AddAction,
    Buffer,
    BufferGroup,
    Bus,
    BusGroup,
    Group,
    Server,
    Synth,
    )
from supriya.tools.soundfiletools import (  # noqa
    HeaderFormat,
    SampleFormat,
    SoundFile,
    play,
    render,
    )
from supriya.tools.synthdeftools import (  # noqa
    CalculationRate,
    DoneAction,
    Envelope,
    Parameter,
    ParameterRate,
    Range,
    SynthDef,
    SynthDefBuilder,
    SynthDefFactory,
    )
from supriya.tools.systemtools import (  # noqa
    Assets,
    Bindable,
    Binding,
    DirectoryChange,
    Enumeration,
    Profiler,
    RedirectedStreams,
    SupriyaConfiguration,
    TestCase,
    Timer,
    bind,
    )
from supriya.tools.wrappertools import (  # noqa
    Say,
    )
from abjad.tools.topleveltools import (  # noqa
    graph,
    )
from supriya import synthdefs  # noqa
from supriya.tools import *  # noqa

__version__ = 0.1

supriya_configuration = SupriyaConfiguration()
del SupriyaConfiguration

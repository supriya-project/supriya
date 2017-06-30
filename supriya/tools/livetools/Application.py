import pathlib
import re
import yaml


class Application:

    def __init__(self, manifest, logger=None):
        import supriya
        if isinstance(manifest, dict):
            self._manifest = manifest
        else:
            manifest = pathlib.Path(manifest)
            if not manifest.suffix:
                manifest = manifest.with_suffix('.yml')
            if not manifest.is_absolute():
                manifest = (
                    pathlib.Path(supriya.__path__[0]) /
                    'assets' /
                    'applications' /
                    manifest
                    )
            with open(str(manifest)) as file_pointer:
                self._manifest = yaml.load(file_pointer)
        self._buffers = self._setup_buffers()
        self._device = self._setup_device()
        self._mixer = self._setup_mixer()
        self._bindings = self._setup_bindings()
        self._server = supriya.Server.get_default_server()

    ### PRIVATE METHODS ###

    def _lookup(self, name):
        current_object = self
        match = re.match(r'^(\w+)$', name)
        if match:
            name = match.group()
            if name.isdigit():
                name = int(name)
            try:
                return current_object[name]
            except (IndexError, KeyError):
                return getattr(current_object, name)
        match = re.match(r'^(\w+)([:.][\w]+)*', name)
        if not match:
            raise KeyError
        group = match.groups()[0]
        current_object = current_object[group]
        name = name[len(group):]
        for substring in re.findall('([:.][\\w]+)', name):
            operator, name = substring[0], substring[1:]
            if name.isdigit():
                name = int(name)
            if operator == ':':
                current_object = current_object[name]
            elif operator == '.':
                current_object = getattr(current_object, name)
        return current_object

    def _setup_buffers(self):
        pass

    def _setup_device(self):
        pass

    def _setup_bindings(self):
        pass

    ### PUBLIC METHODS ###

    def boot(self):
        self.server.boot()
        self.mixer.allocate()
        self.device.open_port()

    ### PUBLIC PROPERTIES ###

    @property
    def bindings(self):
        return self._bindings

    @property
    def buffers(self):
        return self._buffers

    @property
    def device(self):
        return self._device

    @property
    def mixer(self):
        return self._mixer

    @property
    def manifest(self):
        return self._manifest

    @property
    def server(self):
        return self._server

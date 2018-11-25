import copy
import importlib
import pathlib
import re
import traceback

import supriya.patterns
import supriya.realtime
import supriya.system


class Application:
    def __init__(self, manifest=None, logger=None, overrides=None):
        import supriya

        manifest = manifest or {}
        if isinstance(manifest, dict):
            manifest = copy.deepcopy(manifest)
            if overrides:
                manifest = supriya.system.YAMLLoader.merge(manifest, overrides)
            self._manifest = manifest
        else:
            path = self._lookup_file_paths(str(manifest))[0]
            manifest = supriya.system.YAMLLoader.load(str(path), overrides=overrides)
            self._manifest = manifest["application"]
        self._setup_buffers()
        self._setup_devices()
        self._setup_mixer()
        self._setup_bindings()
        self._server = supriya.Server.get_default_server()

    ### PRIVATE METHODS ###

    def _allocate_buffers(self):
        for name in self._buffer_names_to_buffer_groups:
            buffer_group = self._buffer_names_to_buffer_groups[name]
            file_paths = self._buffer_names_to_file_paths[name]
            for buffer_, file_path in zip(buffer_group, file_paths):
                buffer_.allocate_from_file(str(file_path))

    def _build_context_namespaces(self, spec):
        namespaces = {}
        namespaces_spec = spec.get("namespaces", {})
        for namespace_name, namespace_path in namespaces_spec.items():
            namespaces[namespace_name] = self._lookup_nested_object(
                object_=self, name=namespace_path
            )
        return namespaces

    def _build_pattern_namespaces(self, slot):
        buffers = {
            name: buffer_group[:]
            for name, buffer_group in self._buffer_names_to_buffer_groups.items()
        }
        return {"args": slot.bindable_namespace, "buffers": buffers}

    @classmethod
    def _lookup_file_paths(cls, path):
        match = re.match("([\w]+:)?(.+)", path)
        if not match:
            raise ValueError
        module_name, path = match.groups()
        if module_name:
            module_name = module_name[:-1]
            module = importlib.import_module(module_name)
            root_path = pathlib.Path(module.__path__[0]) / "assets"
        else:
            root_path = pathlib.Path(".")
        if (root_path / path).exists():
            return [root_path / path]
        return sorted(root_path.glob(path))

    @classmethod
    def _lookup_importable_object(cls, name):
        match = re.match("\w+(\.\w+)+:\w+", name)
        if not match:
            raise ValueError
        module_path, _, name = name.partition(":")
        module = importlib.import_module(module_path)
        return getattr(module, name)

    @classmethod
    def _lookup_nested_object(cls, object_, name, namespaces=None):
        current_object = object_
        match = re.match(r"^(\w+)$", name)
        if match:
            name = match.group()
            if name.isdigit():
                name = int(name)
            try:
                return current_object[name]
            except (IndexError, KeyError):
                return getattr(current_object, name)
        if name.startswith("$"):
            name = name[1:]
        match = re.match(r"^(\w+)([:.][\w]+)*", name)
        if not match:
            raise KeyError
        group = match.groups()[0]
        if namespaces and group in namespaces:
            current_object = namespaces[group]
        else:
            try:
                current_object = current_object[group]
            except (KeyError, TypeError):
                current_object = getattr(current_object, group)
        name = name[len(group) :]
        for substring in re.findall("([:.][\\w]+)", name):
            operator, name = substring[0], substring[1:]
            if name.isdigit():
                name = int(name)
            if operator == ":":
                current_object = current_object[name]
            elif operator == ".":
                current_object = getattr(current_object, name)
        return current_object

    def _setup_binding(self, context, context_spec, target_name, bind_spec):
        try:
            target = context[target_name]
        except KeyError:
            target = getattr(context, target_name)
        target_range = None
        if isinstance(bind_spec, dict):
            source_name = bind_spec["source"]
            target_range = bind_spec.get("range")
        else:
            source_name = bind_spec
        assert source_name.startswith("$")
        namespaces = self._build_context_namespaces(context_spec)
        try:
            source = self._lookup_nested_object(
                self, source_name[1:], namespaces=namespaces
            )
        except Exception:
            print(source_name)
            raise
        binding = supriya.system.bind(source, target, target_range=target_range)
        self._bindings.add(binding)

    def _setup_bindings(self):
        self._bindings = set()
        mixer_spec = self.manifest.get("mixer", {})
        bind_specs = mixer_spec.get("bind") or {}
        for target_name, bind_spec in bind_specs.items():
            self._setup_binding(self.mixer, mixer_spec, target_name, bind_spec)
        for track_spec in mixer_spec.get("tracks", []):
            track = self._mixer[track_spec["name"]]
            bind_specs = track_spec.get("bind") or {}
            for target_name, bind_spec in bind_specs.items():
                self._setup_binding(track, track_spec, target_name, bind_spec)
            slot_specs = track_spec.get("slots") or []
            for slot_spec in slot_specs:
                slot = track[slot_spec["name"]]
                for target_name, bind_spec in slot_spec.get("bind", {}).items():
                    self._setup_binding(slot, slot_spec, target_name, bind_spec)
            send_specs = track_spec.get("sends") or []
            for send_spec in send_specs:
                target_name = send_spec.get("name")
                bind_spec = send_spec.get("bind")
                self._setup_binding(track.send, send_spec, target_name, bind_spec)

    def _setup_buffers(self):
        self._buffer_names_to_buffer_groups = {}
        self._buffer_names_to_file_paths = {}
        buffer_specs = self.manifest.get("buffers") or []
        for buffer_spec in buffer_specs:
            name = buffer_spec["name"]
            if name in self._buffer_names_to_buffer_groups:
                raise ValueError(buffer_spec)
            path = buffer_spec["path"]
            file_paths = tuple(self._lookup_file_paths(path))
            if not file_paths:
                continue
            buffer_group = supriya.realtime.BufferGroup(len(file_paths))
            self._buffer_names_to_buffer_groups[name] = buffer_group
            self._buffer_names_to_file_paths[name] = file_paths

    def _setup_devices(self):
        import supriya.midi

        self._devices = {}
        device_specs = self.manifest.get("devices") or []
        for device_spec in device_specs:
            name, path = device_spec["name"], device_spec["path"]
            if name in self._devices:
                raise ValueError(device_spec)
            manifest_path = self._lookup_file_paths(path)[0]
            self._devices[name] = supriya.midi.Device(
                manifest_path, overrides=device_spec.get("overrides")
            )

    def _setup_mixer(self):
        import supriya.live

        manifest = self.manifest.get("mixer", {})
        channel_count = int(manifest.get("channel_count", 2))
        cue_channel_count = int(manifest.get("cue_channel_count", 2))
        self._mixer = supriya.live.Mixer(channel_count, cue_channel_count)
        track_specs = manifest.get("tracks") or []
        for track_spec in track_specs:
            if track_spec["name"] not in ("master", "cue"):
                channel_count = track_spec.get("channel_count")
                self._mixer.add_track(track_spec["name"], channel_count)
        for track_spec in manifest.get("tracks", []):
            track = self._mixer[track_spec["name"]]
            slot_specs = track_spec.get("slots") or []
            for slot_spec in slot_specs:
                self._setup_slot(track, slot_spec)
            send_specs = track_spec.get("sends") or []
            for send_spec in send_specs:
                self._setup_send(track, send_spec)

    def _setup_send(self, track, send_spec):
        send_name = send_spec["name"]
        track.send(send_name)

    def _setup_slot(self, track, slot_spec):
        slot_name = slot_spec["name"]
        slot_type = slot_spec["type"]
        assert slot_type in ("synth", "auto", "trigger")
        slot_synthdef = slot_spec.get("synthdef")
        if slot_synthdef:
            slot_synthdef = self._lookup_importable_object(slot_synthdef)
        slot_args = slot_spec.get("args") or {}
        if slot_type == "trigger":
            maximum_replicas = slot_spec.get("maximum_replicas")
            if maximum_replicas:
                slot_args["maximum_replicas"] = int(maximum_replicas)
        if slot_type == "synth":
            method = track.add_synth_slot
        elif slot_type == "auto":
            method = track.add_auto_pattern_slot
        elif slot_type == "trigger":
            method = track.add_trigger_pattern_slot
        slot = method(name=slot_name, synthdef=slot_synthdef, **slot_args)
        if slot_type in ("auto", "trigger"):
            pattern = slot_spec.get("pattern")
            assert pattern is not None
            pattern = supriya.patterns.Pattern.from_dict(
                pattern, namespaces=self._build_pattern_namespaces(slot)
            )

    ### PUBLIC METHODS ###

    def boot(self):
        self.server.boot()
        self._allocate_buffers()
        self.mixer.allocate()
        try:
            for device in self.devices.values():
                device.open_port()
        except Exception:
            traceback.print_exc()
            for device in self.devices.values():
                device.open_port(virtual=True)
        return self

    def quit(self):
        self.server.quit()
        for device in self.devices.values():
            device.close_port()
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def bindings(self):
        return self._bindings

    @property
    def buffers(self):
        return self._buffer_names_to_buffer_groups

    @property
    def devices(self):
        return self._devices

    @property
    def mixer(self):
        return self._mixer

    @property
    def manifest(self):
        return self._manifest

    @property
    def server(self):
        return self._server

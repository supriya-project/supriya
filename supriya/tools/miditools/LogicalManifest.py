import collections
from supriya.tools import systemtools
from supriya.tools.miditools.LogicalControl import LogicalControl
from supriya.tools.miditools.View import View


class LogicalManifest:

    ### INITIALIZER ###

    def __init__(self, device):
        self._device = device
        device_manifest = self._device._device_manifest['device']
        manifest = device_manifest['logical_controls']
        self._node_templates = self._linearize_manifest(manifest)
        for key, value in self._node_templates.items():
            print(key, value)
        self._node_instances = {}
        self._node_instances['root'] = [View(name='root')]
        self._dependents = {}
        for parentage_string, node_template in self._node_templates.items():
            parents = self._node_instances[parentage_string.rpartition(':')[0]]
            if 'children' in node_template:
                if 'modal' in node_template:
                    nodes = self._build_modal_view(node_template, parents)
                elif node_template.get('mode') == 'mutex':
                    nodes = self._build_mutex_view(node_template, parents)
                else:
                    nodes = self._build_view(node_template, parents)
            elif 'physical_control' in node_template:
                nodes = self._build_physical_controls(node_template, parents)
            else:
                raise Exception(parentage_string, node_template)
            self._node_instances[parentage_string] = nodes
        self.rebuild_visibility_mapping()

    ### PRIVATE METHODS ###

    def _build_modal_view(self, node_template, parents):
        nodes = []
        toggle_id = 'root:{}'.format(node_template['modal'])
        all_toggles = self._node_instances[toggle_id]
        for parent, toggles in zip(parents, all_toggles):
            modal_view = View(name=node_template['name'], visible=True)
            parent.add_child(modal_view)
            for i, toggle in enumerate(toggles.children.values()):
                view = View(
                    name=i,
                    visible=i == 0,
                    )
                nodes.append(view)
                modal_view.add_child(view)
                self._dependents.setdefault(toggle, []).append(view)
        return nodes

    def _build_mutex_view(self, node_template, parents):
        nodes = []
        physical_controls = []
        physical_control_ids = node_template['children']
        for physical_control_id in physical_control_ids:
            physical_controls.extend(
                self.device.physical_manifest.get_controls_by_name(
                    physical_control_id))
        for parent in parents:
            view = View(name=node_template['name'], mode='mutex')
            nodes.append(view)
            parent.add_child(view)
            for i, physical_control in enumerate(physical_controls):
                control = LogicalControl(
                    name=i,
                    mode='toggle',
                    physical_control=physical_control,
                    )
                if i == 0:
                    control.value = 1.0
                view.add_child(control)
        return nodes

    def _build_view(self, node_template, parents):
        pass

    def _build_physical_controls(self, node_template, parents):
        nodes = []
        physical_controls = []
        physical_control_ids = node_template['physical_control']
        if isinstance(physical_control_ids, str):
            physical_control_ids = [physical_control_ids]
        for physical_control_id in physical_control_ids:
            physical_controls.extend(
                self.device.physical_manifest.get_controls_by_name(
                    physical_control_id))
        for parent in parents:
            for i, physical_control in enumerate(physical_controls, 1):
                if 'name' in node_template:
                    if node_template['name']:
                        name = node_template['name']
                        if len(physical_controls) > 1:
                            name = '{}_{}'.format(name, i)
                    else:
                        name = i - 1
                else:
                    name = physical_control.name
                mode = node_template.get('mode')
                logical_control = LogicalControl(
                    mode=mode,
                    name=name,
                    physical_control=physical_control,
                    )
                nodes.append(logical_control)
                parent.add_child(logical_control)
        return nodes

    def _linearize_manifest(self, manifest):
        trellis = systemtools.Trellis()
        entries_by_parentage = {}
        self._recurse_manifest(
            entries_by_parentage=entries_by_parentage,
            manifest=manifest,
            parentage=('root',),
            trellis=trellis,
            )
        templates = collections.OrderedDict()
        for parentage_string in trellis:
            if parentage_string == 'root':
                continue
            templates[parentage_string] = entries_by_parentage[parentage_string]
        return templates

    def _recurse_manifest(
        self,
        entries_by_parentage,
        manifest,
        parentage,
        trellis,
        ):
        for entry in manifest:
            entry_name = entry.get('name') or entry.get('physical_control')
            assert entry_name
            entry_parentage = parentage + (entry_name,)
            entry_parentage_string = ':'.join(entry_parentage)
            assert entry_parentage_string not in entries_by_parentage
            entries_by_parentage[entry_parentage_string] = entry
            if parentage:
                parentage_string = ':'.join(parentage)
                trellis.add(
                    parentage_string,
                    entry_parentage_string,
                    )
            else:
                trellis.add(entry_parentage_string)
            if 'modal' in entry:
                trellis.add(
                    'root:{}'.format(entry.get('modal')),
                    entry_parentage_string,
                    )
            children = entry.get('children', [])
            if entry.get('mode') != 'mutex':
                self._recurse_manifest(
                    entries_by_parentage=entries_by_parentage,
                    manifest=children,
                    parentage=entry_parentage,
                    trellis=trellis,
                    )

    ### PUBLIC METHODS ###

    def rebuild_visibility_mapping(self):
        mapping = collections.OrderedDict()
        for logical_control in self.root_view.yield_visible_controls():
            physical_control = logical_control.physical_control
            assert physical_control not in mapping
            mapping[physical_control] = logical_control
        self._visibility_mapping = mapping
        return mapping

    ### PUBLIC PROPERTIES ###

    @property
    def device(self):
        return self._device

    @property
    def dependents(self):
        return self._dependents

    @property
    def root_view(self):
        return self._node_instances['root'][0]

    @property
    def visibility_mapping(self):
        return self._visibility_mapping

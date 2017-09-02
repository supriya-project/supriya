import copy
import jinja2
import pathlib
import yaml


class YAMLLoader:

    @classmethod
    def load(cls, path, overrides=None):
        path = pathlib.Path(path)
        with path.open() as file_pointer:
            string = file_pointer.read()
        manifest = yaml.load(string)
        if 'extends' in manifest:
            extends_path = pathlib.Path(manifest['extends'])
            if not extends_path.is_absolute():
                extends_path = path.parent / extends_path
            extends_manifest = cls.load(extends_path)
            manifest = cls.merge(extends_manifest, manifest)
        manifest = cls.resolve_templating(manifest)
        if overrides:
            return cls.merge(manifest, overrides)
        return manifest

    @classmethod
    def merge(cls, old, new):
        for key in new:
            if key not in old:
                old[key] = new[key]
            else:
                old[key] = cls.merge(old[key], new[key])
        return old

    @classmethod
    def resolve_templating(cls, manifest, template_variables=None):
        template_variables = (template_variables or {}).copy()
        manifest = copy.copy(manifest)
        if isinstance(manifest, dict):
            if '$templating' in manifest:
                local_template_variables = manifest.pop('$templating') or {}
                for key, value in local_template_variables.items():
                    value = str(value)
                    local_template_variables[key] = jinja2.Template(value).render(
                        template_variables)
                template_variables.update(local_template_variables)
            for name, entry in manifest.items():
                manifest[name] = cls.resolve_templating(entry, template_variables)
        elif isinstance(manifest, list):
            for i, entry in enumerate(manifest):
                manifest[i] = cls.resolve_templating(entry, template_variables)
        elif isinstance(manifest, str) and template_variables:
            manifest = jinja2.Template(manifest).render(template_variables)
        return manifest

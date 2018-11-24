import importlib
import pathlib


class ProjectManager:
    @staticmethod
    def import_section_objects(section, file_path, namespace):
        section_path = pathlib.Path(file_path).parent
        root_path = section_path.parent
        for path in sorted(section_path.iterdir()):
            if not path.is_dir():
                continue
            elif not (path / "__init__.py").exists():
                continue
            elif not (path / "definition.py").exists():
                continue
            name = path.name
            path = path / "definition"
            path_parts = (root_path.name,) + path.relative_to(root_path).parts
            module_path = ".".join(path_parts)
            module = importlib.import_module(module_path)
            member = getattr(module, section)
            namespace[name] = member

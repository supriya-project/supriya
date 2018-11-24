import os
import pathlib
import sys
import yaml
import uqbar.io
import uqbar.strings
from supriya.cli.ProjectPackageScript import ProjectPackageScript


class ManageProjectScript(ProjectPackageScript):
    """
    Manages project packages.

    ::

        sjv project --help

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = "project"
    short_description = "manage project packages"

    ### PRIVATE METHODS ###

    def _handle_clean(self):
        here = pathlib.Path.cwd()
        renders_path = (self.inner_project_path / "renders").relative_to(here)
        print("Cleaning {} ...".format(renders_path))
        for file_path in sorted(renders_path.iterdir()):
            if file_path.name.startswith("."):
                continue
            file_path.unlink()
            print("    Cleaned {}".format(file_path))

    def _handle_new(
        self,
        title,
        composer_email=None,
        composer_github=None,
        composer_library=None,
        composer_name=None,
        composer_website=None,
        force=False,
    ):
        print("Creating project package {!r}...".format(title))
        package_name = uqbar.strings.to_snake_case(title)
        outer_target_path = pathlib.Path(package_name).absolute()
        if outer_target_path.exists() and not force:
            message = "    Directory {!s} already exists."
            message = message.format(package_name)
            print(message)
            sys.exit(1)
        inner_target_path = outer_target_path.joinpath(package_name)
        boilerplate_path = self._get_boilerplate_path()
        outer_source_path = boilerplate_path.joinpath("example_project")
        inner_source_path = outer_source_path.joinpath("example_project")
        metadata = {
            "project_package_name": package_name,
            "composer_email": composer_email,
            "composer_full_name": composer_name,
            "composer_github_username": composer_github,
            "composer_library_package_name": composer_library,
            "title": title,
        }
        for path in self._copy_tree(
            outer_source_path, outer_target_path, recurse=False
        ):
            if path.is_file() and path.suffix == ".jinja":
                self._template_file(path, **metadata)
                path.rename(path.with_suffix(""))
        for path in self._copy_tree(inner_source_path, inner_target_path, recurse=True):
            if path.is_file() and path.suffix == ".jinja":
                self._template_file(path, **metadata)
                path.rename(path.with_suffix(""))
        self._setup_paths(inner_target_path)
        self._make_project_settings_yaml(
            inner_target_path,
            composer_email=composer_email,
            composer_github=composer_github,
            composer_library=composer_library,
            composer_name=composer_name,
            composer_website=composer_website,
            title=title,
        )
        print("    Created {path!s}{sep}".format(path=package_name, sep=os.path.sep))

    def _handle_prune(self):
        here = pathlib.Path.cwd()
        renders_path = (self.inner_project_path / "renders").relative_to(here)
        print("Pruning {} ...".format(renders_path))
        md5s = set()
        for file_path in sorted(self.inner_project_path.glob("**/render.yml")):
            with open(str(file_path), "r") as file_pointer:
                render_yml = yaml.load(file_pointer.read())
                md5s.add(render_yml["render"])
                if render_yml["source"]:
                    md5s.update(render_yml["source"])
        for file_path in sorted(renders_path.iterdir()):
            if file_path.name.startswith("."):
                continue
            if file_path.with_suffix("").name in md5s:
                continue
            file_path.unlink()
            print("    Pruned {}".format(file_path))

    @classmethod
    def _make_project_settings_yaml(
        cls,
        inner_project_path,
        composer_email=None,
        composer_github=None,
        composer_library=None,
        composer_name=None,
        composer_website=None,
        title=None,
    ):
        import supriya.realtime

        server_options = supriya.realtime.ServerOptions()
        server_options = server_options.as_dict()
        project_settings = dict(
            server_options=server_options,
            composer=dict(
                email=composer_email,
                github=composer_github,
                library=composer_library,
                name=composer_name,
                website=composer_website,
            ),
            title=title,
        )
        project_settings_yaml = yaml.dump(
            project_settings, default_flow_style=False, indent=4
        )
        project_settings_path = inner_project_path.joinpath("project-settings.yml")
        with open(str(project_settings_path), "w") as file_pointer:
            file_pointer.write(project_settings_yaml)

    def _process_args(self, args):
        if args.new:
            self._handle_new(
                composer_email=args.composer_email,
                composer_github=args.composer_github,
                composer_library=args.composer_library,
                composer_name=args.composer_name,
                composer_website=args.composer_website,
                force=args.force,
                title=args.new,
            )
            return
        self._setup_paths(args.project_path)
        with uqbar.io.DirectoryChange(str(self.outer_project_path)):
            if args.clean:
                self._handle_clean()
            if args.prune:
                self._handle_prune()

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group("actions")
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            "--new", "-N", help="create a new project", metavar="TITLE"
        )
        action_group.add_argument(
            "--prune",
            "-P",
            action="store_true",
            help="prune out stale render artifacts",
        )
        action_group.add_argument(
            "--clean", "-C", action="store_true", help="clean out all render artifacts"
        )

        new_group = parser.add_argument_group("--new options")
        new_group.add_argument("--composer-name", default="A Composer", metavar="NAME")
        new_group.add_argument(
            "--composer-email", default="composer@email.com", metavar="EMAIL"
        )
        new_group.add_argument(
            "--composer-github", default="composer", metavar="GITHUB_USERNAME"
        )
        new_group.add_argument(
            "--composer-library", default="library", metavar="LIBRARY_NAME"
        )
        new_group.add_argument(
            "--composer-website", default="www.composer.com", metavar="WEBSITE"
        )

        common_group = parser.add_argument_group("common options")
        common_group.add_argument(
            "--force", "-f", action="store_true", help="force overwriting"
        )
        common_group.add_argument(
            "--project-path",
            "-p",
            metavar="project",
            help="project path or package name",
            default=os.path.curdir,
        )

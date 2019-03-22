from supriya.cli import ProjectManager, ProjectSettings

project_manager = ProjectManager()
project_settings = ProjectSettings.from_python_module(__file__)

del ProjectManager, ProjectSettings

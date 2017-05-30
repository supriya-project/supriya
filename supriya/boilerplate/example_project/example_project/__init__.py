# -*- encoding: utf-8 -*-
from supriya.tools.commandlinetools import ProjectSettings, ProjectManager

project_manager = ProjectManager()
project_settings = ProjectSettings.from_python_module(__file__)

del ProjectManager, ProjectSettings

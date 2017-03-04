# -*- encoding: utf-8 -*-
import os
from supriya.tools.commandlinetools import ProjectSettings


project_settings = ProjectSettings(os.path.join(
    os.path.dirname(__file__),
    'project-settings.yml',
    ))

del os
del ProjectSettings

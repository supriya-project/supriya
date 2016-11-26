# -*- coding: utf-8 -*-
# tools first, materials second, segments last:
# makes it possible for materials to import tools;
# makes it possible for segments to import both materials and tools.
from {score_package_name} import tools
from {score_package_name} import materials
from {score_package_name} import segments

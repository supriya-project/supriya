"""
Version information.

- Major version is last two digits of the current year.
- Minor version is the month as a digit.
- Patch / beta tag is the number of releases during that month.

This follows black's versioning scheme.
"""
__version_info__ = (22, "8b1")
__version__ = ".".join(str(x) for x in __version_info__)

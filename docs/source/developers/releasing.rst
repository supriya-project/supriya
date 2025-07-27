Releasing
=========

Supriya is published to PyPI at https://pypi.org/project/supriya/.

Versioning scheme
`````````````````

Supriya uses a ``YY.MbX`` version scheme, e.g. ``25.6b1``, where ``YY`` is the
last two digits of the current year (making the strong assumption that she
won't make it past the end of the 21st century), ``M`` is the ordinal of the
current month and ``X`` is the number of previous releases that month.

I don't use semantic versioning because of the cognitive overhead of
determining what sorts of changes count as breaking, patches, etc.

The version information is stored in :github-blob:`supriya/_version.py
<supriya/_version.py>` as a tuple so that it's available by Supriya after
installation, and by :github-blob:`setup.py <setup.py>` during installation
(but without needed to import Supriya directly).

Drafting releases
`````````````````

To cut a new release run the ``Release`` GitHub Actions pipeline at
https://github.com/supriya-project/supriya/actions/workflows/release.yml.

This will bump the current version number in :github-blob:`supriya/_version.py
<supriya/_version.py>` and cut a draft of a new release in GitHub.

Publishing releases
```````````````````

Once a draft release in GitHub has been published, the publishing pipeline will
automatically kickoff at
https://github.com/supriya-project/supriya/actions/workflows/publish.yml.

This pipeline builds the Sphinx docs, build Supriya's wheels and source
distributions, publishes the distributions to PyPI and then syncs the newly
built documentation with GitHub pages.

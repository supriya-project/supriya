Developer overview
==================

Contributing
____________

Supriya accepts contributions on `GitHub`_.

When fixing bugs, fork the repository and open a pull request against it.

When suggesting features, please open an issue or start a discussion on
`GitHub`_ before opening a pull request. Just like with Python itself, not
everything needs to be part of the base project. If the feature is deemed worth
adding to the base project, proceed like opening a bug: fork the repo and open
a pull request.

See the following sections for more detailed guidance on developing Supriya
itself.

..  editorial::

    `I`_ am *exceedingly* disinterested in helping package Supriya for random
    Linux distributions. *Please* just install Supriya from `PyPI`_. There's no
    reason to package it up for Arch, etc. That just creates a graveyard of
    unmaintained ancient packages which - if anyone even notices them - can
    become a burden for me.

Tooling
-------

Supriya provides a ``Makefile`` with targets for common local development tasks:

..  shell::
    :cwd: ..
    :rel: ..
    :user: josephine
    :host: laptop

    make

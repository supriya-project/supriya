#!/usr/bin/env python
import setuptools


if __name__ == '__main__':
    setuptools.setup(
        author='{composer_full_name}',
        author_email='{composer_email}',
        install_requires=(
            'supriya',
            ),
        name='{score_package_name}',
        packages=(
            '{score_package_name}',
            ),
        url='https://github.com/{composer_github_username}/{score_package_name}',
        version='0.1',
        zip_safe=False,
        )

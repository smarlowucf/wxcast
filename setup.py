#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wxcast: A Python API and cli to collect weather information.
#
# Copyright (C) 2017 Sean Marlow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'requests',
]

test_requirements = [
    'nose',
]

setup(
    name='wxcast',
    version='0.2.0',
    description="An SDK and command line utilities to collect weather information.",
    long_description=readme + '\n\n' + history,
    author="Sean Marlow",
    author_email='sean.marlow@suse.com',
    url='https://github.com/smarlowucf/wxcast',
    packages=[
        'wxcast',
    ],
    package_dir={'wxcast':
                 'wxcast'},
    entry_points={
        'console_scripts': [
            'wxcast=wxcast.cli:main'
        ]
    },
    include_package_data=True,
    package_data={'ipa': ['nws.pem']},
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='wxcast',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

#!/usr/bin/python3
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

with open('README.adoc') as readme_file:
    readme = readme_file.read()

with open('CHANGES.adoc') as changes_file:
    changes = changes_file.read()

requirements = [
    'certifi',
    'Click>=6.0',
    'geopy',
    'requests',
]

test_requirements = [
    'pytest',
]

setup(
    name='wxcast',
    version='1.0.6',
    description='A CLI utility for retrieving weather information.',
    long_description=readme + '\n\n' + changes,
    author="Sean Marlow",
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
    install_requires=requirements,
    license='GPLv3+',
    zip_safe=False,
    keywords='wxcast',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

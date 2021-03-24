#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# wxcast: A Python API and cli to collect weather information.
#
# Copyright (c) 2021 Sean Marlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGES.md') as changes_file:
    changes = changes_file.read()

requirements = [
    'certifi',
    'Click>=6.0',
    'geopy',
    'requests',
    'metar'
]

test_requirements = [
    'flake8',
    'pytest',
    'pytest-cov',
    'vcrpy'
]

setup(
    name='wxcast',
    version='1.4.0',
    description='A CLI utility for retrieving weather information.',
    long_description=readme + '\n\n' + changes,
    long_description_content_type="text/markdown",
    author="Sean Marlow",
    url='https://github.com/smarlowucf/wxcast',
    packages=[
        'wxcast',
    ],
    package_dir={
        'wxcast': 'wxcast'
    },
    entry_points={
        'console_scripts': [
            'wxcast=wxcast.cli:main'
        ]
    },
    install_requires=requirements,
    extras_require={
        'test': test_requirements,
    },
    license='GPLv3+',
    zip_safe=False,
    keywords='wxcast',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    test_suite='tests',
    tests_require=test_requirements
)

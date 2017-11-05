#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'requests>=2.18',
    'PyYAML>=3.12',
]

setup_requirements = []

test_requirements = []

setup(
    name='jr_tools',
    version='0.3.0',
    description="A collection of tools to handle Jasper Reports with python",
    long_description=readme + '\n\n' + history,
    author="Erick Navarro",
    author_email='erick@navarro.io',
    url='https://github.com/erickgnavar/jasper-reports-tools',
    packages=find_packages(include=['jr_tools']),
    entry_points={
        'console_scripts': [
            'jr_tools=jr_tools.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='jr_tools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

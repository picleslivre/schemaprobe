#!/usr/bin/env python
import sys
import re
from setuptools import setup, Extension

import schemaprobe


version = schemaprobe.__version__

install_requires = [
    'jsonschema',
    'requests',
]
tests_require = install_requires[:]

PY2 = sys.version_info[0] == 2
if PY2:
    tests_require.append('mock')


setup(
    name="schemaprobe",
    version=version,
    description="Platform for testing JSON-based RESTful API resources.",
    author="Gustavo Fonseca",
    author_email="gustavo@gfonseca.net",
    license="BSD",
    url="http://github.com/picleslivre/schemaprobe/",
    py_modules=["schemaprobe"],
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite="tests",
)

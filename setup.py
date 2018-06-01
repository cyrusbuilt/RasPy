#!/usr/bin/env python

import sys
from io import open
from setuptools import setup, find_packages
from raspy import RASPY_FRAMEWORK_VER


if sys.version_info < (2, 7):
    print("ERROR: python version < 2.7 is not supported.")
    sys.exit(1)

install_requires = [
    'pyee',
    'tornado',
    'psutil',
    'spidev'
]

setup(
    name='raspy',
    version=RASPY_FRAMEWORK_VER,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'doc': ['sphinx', 'sphinxjp.themes.basicstrap', 'sphinx-bootstrap-theme'],
        'tests': ['nose2']
    },
    description='Raspberry Pi Framework for Python',
    long_description=open('README.md', encoding='utf-8').read(),
    url='https://github.com/cyrusbuilt/raspy',
    author='CyrusBuilt',
    author_email='cyrusbuilt@gmail.com',
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    exclude_package_data={'': ['.gitignore']},
    classifiers={
        "Programming Language :: Python :: 2",
        "Topic :: Scientific/Engineering"
    }
)

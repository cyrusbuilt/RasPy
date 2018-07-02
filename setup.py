#!/usr/bin/env python

import platform
import sys
import time
from io import open
from setuptools import setup, find_packages
from raspy import RASPY_FRAMEWORK_VER


if sys.version_info < (2, 7):
    print("ERROR: python version < 2.7 is not supported.")
    sys.exit(1)

if platform.system() != "Linux":
    msg = "WARNING: This library intended to be installed on a Linux-based"
    msg += " Raspberry Pi. Installation may fail.\n"
    print(msg)
    time.sleep(3)

install_requires = [
    'pyee',
    'tornado',
    'psutil',
    'spidev',
    'smbus2'
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
    },
    keywords=['python', 'raspberrypi', 'linux']
)

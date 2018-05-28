#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='RasPy',
    version='0.1',
    description='Raspberry Pi Framework for Python',
    url='',
    author='CyrusBuilt',
    author_email='cyrusbuilt@gmail.com',
    license='GPLv2',
    zip_safe=False,
    packages=[
        'RasPy'
    ],
    package_dir={

    },
    cmdclass={

    }
)

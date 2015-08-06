#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='flask-apploader',
    version='0.0.1.dev1',
    url='http://github.com/sycdan/flask-apploader',
    description="Load all the submodules within a Flask app's dir.",
    long_description=read('README.md'),
    author='Dan Stace',
    author_email='dstace@gmail.com',
    license='MIT',
    packages=['flask_apploader'],
    install_requires=['six'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)

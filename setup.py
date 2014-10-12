#!/usr/bin/env python

from setuptools import setup

setup(name='drift',
      version='0.0.1',
      description='Utility for tracking upstream changes in Git and Gerrit',
      author='Tom Cammann',
      author_email='cammann.tom@gmail.com   ',
      packages=['drift'],
      install_requires=['gitpython>=0.3.2.RC1'])

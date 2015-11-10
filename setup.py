#!/usr/bin/env python

from distutils.core import setup

setup(name='TMB',
      version='0.1',
      description='TDF Monitoring Bot',
      author='Alexander Werner',
      author_email='alex@documentfoundation.org',
      url='https://github.com/tdf/tmb',
      packages=['tmb',],
      install_requires = ['python-telegram-bot',],
     )
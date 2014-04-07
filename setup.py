#!/usr/bin/env python

import os
from setuptools import setup

__author__ = 'David Béal <david.beal@akretion.com>'
__version__ = '0.1.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	# Basic package information.
	name = 'coliposte',
	version = __version__,

	# Packaging options.
	include_package_data = True,

	# Package dependencies.
	#install_requires = [],

	# Metadata for PyPI.
	author = 'David Béal',
	author_email = 'david.beal@akretion.com',
	license = 'GNU AGPL-3',
	url = 'http://github.com/akretion/coliposte',
    packages=['coliposte'],
	keywords = 'laposte fr coliposte label',
	description = 'A library to generation carrier label with LaPoste Fr.',
	long_description = read('README'),
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU Affero General Public License v3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Internet :: WWW/HTTP :: ?????',
		'Topic :: Internet'
	]
)

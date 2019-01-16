#!/usr/bin/env python
"""
Flask-MM-GeoIP
--------------

A Flask-ified geolocation extension using the MaxMind GeoIP2 module.
"""

from __future__ import print_function
import codecs
import os
from setuptools import setup, find_packages

appname = 'Flask-MM-GeoIP2'
pkgname = appname.lower().replace('-','_')
metadata_relpath = '{}/metadata.py'.format(pkgname)

with open(metadata_relpath) as fh:
    metadata = {}
    exec(fh.read(), globals(), metadata)

def read(fn):
    with codecs.open(fn, 'r', 'utf-8') as fh:
        contents = fh.read()
    return contents

setup(
    name=appname,
    version=metadata['__version__'],
    description=__doc__,
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.md')),
    packages=find_packages(),
    install_requires=[
        'Flask>=1.0.2',
        'geoip2>=2.9.0',
    ],
    author='Daniel Hoover',
    author_email='lx@t0xic.com',
    url='https://github.com/TheOneTrueLX/flask-mm-geoip2',
    license='BSD',
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
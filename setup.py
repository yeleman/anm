#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import setuptools

setuptools.setup(
    name='anm',
    version=__import__('anm').__version__,
    license='GNU Lesser General Public License (LGPL), Version 3',

    install_requires=['SQLAlchemy>=0.6.6','pysqlite'],
    provides=['anm'],

    description='Budget Management G.U.I',
    long_description=open('README.rst').read(),

    url='http://github.com/yeleman/anm',

    packages=['anm'],

    classifiers=[
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
        'Programming Language :: Python',
    ],
)

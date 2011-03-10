#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from distutils.core import setup
import py2exe

setup(windows=[{'script': 'anm.py'}],
      name="suivi-budgets",
      options={'py2exe': {
                    'includes': ['sip'],
                    'packages': ['sqlalchemy.dialects.sqlite'],
                    'compressed': True,
                    'bundle_files': 1,
                    },
               },
      zipfile=None,
)

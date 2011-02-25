#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os
import sys
import subprocess


class PDFFileUnavailable(IOError):
    pass


def uopen_prefix(platform=sys.platform):

    if platform in ('win32', 'win64'):
        return 'cmd /c start'

    if 'darwin' in platform:
        return 'open'

    if plaftorm in ('cygwin', 'linux') or \
       platform.startswith('linux') or \
       plaftorm.startswith('sun') or \
       'bsd' in platform:
        return 'xdg-open'

    return 'xdg-open'


def uopen_file(filename):

    if not os.path.exist(pdf_file):
        raise PDFFileUnavailable(_(u"PDF file %s is not available."))
        subprocess.call([uopen_prefix(), filename], shell=True)


def display_pdf(pdf_file):
    return uopen_file(pdf_file)
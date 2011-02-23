#!/usr/bin/python
# encoding=utf-8
# maintainer: rgaudin

import os
import sys
import subprocess

''' actions include
    * update: update POT file from code
    * merge: merge locale with POT file
    * compile: gen MO file
    * new: create new lang stub
    * all: update, merge and compile
    * '''

try:
    ACTION = sys.argv[1].lower()
except:
    ACTION = 'all'
try:
    LOCALE = sys.argv[2].lower()
except:
    LOCALE = 'fr'

TOOLS_DIR = os.path.realpath(os.path.dirname(__file__))
ROOT_DIR = os.path.realpath(os.path.join(TOOLS_DIR, '..', 'anm'))
LOCALE_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'locale'))


def package_version():
    return '0.1'


def exec_cmd(cmd):
    print cmd
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
                              shell=True).communicate()[0]
    return output


def update_(locale=None):
    version = package_version()

    dirs = ('', 'ui')
    dirs_str = []
    for dir_ in dirs:
        dirs_str.append('%s/*.py' % os.path.join(ROOT_DIR, dir_))

    cmd = 'xgettext --no-wrap --sort-by-file --default-domain=anm ' \
          '--copyright-holder="yɛlɛman s.à.r.l" --package-name="anm" ' \
          '--package-version="%s" ' \
          '--msgid-bugs-address=bugs@yeleman.com ' \
          '--language=Python --keyword=_ --add-comments ' \
          '--output=anm.pot ' % version + ' '.join(dirs_str)
    return exec_cmd(cmd)


def merge_(locale):
    return exec_cmd('msgmerge --update --no-wrap --sort-by-file ' \
                    '%s/LC_MESSAGES/anm.po anm.pot' % locale)


def compile_(locale):
    return exec_cmd('msgfmt --output-file=%s/LC_MESSAGES/anm.mo ' \
                   '%s/LC_MESSAGES/anm.po' % (locale, locale))


def new_(locale):
    return exec_cmd('msginit --locale=%s --no-wrap ', \
                    '--output-file=%s/LC_MESSAGES/anm.po ' \
                    '--input=anm.pot' % (locale, locale))


def all_(locale):
    print update_(locale)
    print merge_(locale)
    print compile_(locale)
    return ''


def main():

    # change to locale/ folder
    os.chdir(LOCALE_DIR)

    if ACTION in ('update', 'merge', 'compile', 'new', 'all'):
        func = eval('%s_' % ACTION)
        print func(LOCALE)
    else:
        print "wrong action."
        exit(1)

if __name__ == '__main__':
    main()

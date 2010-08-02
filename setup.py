#!/usr/bin/python -tt

""" Setup """

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PKG = open('debian/changelog').readline().split(' ')[0]

setup(name=PKG,
    description='Enterprise address book',
    version=open('debian/changelog').readline().split(' ')[1][1:-1],
    license='GPL 2',
    packages=['meabook.database', 'meabook.parsers', 'meabook.ui', \
        'meabook.renderers', 'meabook', 'meabook.ui.fremantle_ui'],
    package_dir={'meabook': ''},
    data_files = [
        ('/usr/share/dbus-1/services', ['maemo/%s.service' % PKG]),
        ('/usr/share/applications/hildon', ['maemo/%s.desktop' % PKG]),
        ('/usr/share/icons/hicolor/48x48/apps/', \
            ['./maemo/icons/48x48/%s.png' % PKG]),
        ('/usr/share/icons/hicolor/64x64/apps/', \
            ['./maemo/icons/64x64/%s.png' % PKG]),
        ('/usr/share/locale/ru/LC_MESSAGES', ['./i18n/ru/meabook.mo']),
        ('/usr/share/locale/ru_RU/LC_MESSAGES', ['./i18n/ru/meabook.mo']),
        ('/usr/share/locale/en/LC_MESSAGES', ['./i18n/en/meabook.mo']),
        ('/usr/share/locale/en_EN/LC_MESSAGES', ['./i18n/en/meabook.mo'])
    ])

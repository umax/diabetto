#!/usr/bin/python -tt

""" Setup """

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PKG = open('debian/changelog').readline().split(' ')[0]

setup(name=PKG,
    description='Diabetto food calculator',
    version=open('debian/changelog').readline().split(' ')[1][1:-1],
    license='GPL 2',
    packages=['diabetto.ui', 'diabetto.ui.diablo_ui', 'diabetto'],
    package_dir={'diabetto': ''},
    data_files = [
        ('/usr/share/dbus-1/services', ['maemo/%s.service' % PKG]),
        ('/usr/share/applications/hildon', ['maemo/%s.desktop' % PKG]),
        #('/usr/share/icons/hicolor/48x48/apps/', \
        #    ['./maemo/icons/48x48/%s.png' % PKG]),
        #('/usr/share/icons/hicolor/64x64/apps/', \
        #    ['./maemo/icons/64x64/%s.png' % PKG]),
        ('/usr/share/locale/ru/LC_MESSAGES', ['./i18n/ru/diabetto.mo']),
        ('/usr/share/locale/ru_RU/LC_MESSAGES', ['./i18n/ru/diabetto.mo']),
        ('/usr/share/diabetto', ['./rcfile'])
    ])

#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _
from diabetto.ui.diablo_ui.common import create_button
from diabetto.ui.diablo_ui.products import ProductsWidget


class MainWidget:
    def __init__(self, controller):
        self.controller = controller
        self.fullscreen = False

        # create widgets
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(800, 480)
        window.connect('destroy', self.exit_cb)
        window.connect('key-press-event', self.window_keypress_cb)
        switcher = gtk.Notebook()
        switcher.set_show_tabs(False)
        window.add(switcher)
        products_button = create_button(_('Products'), \
            self.create_products_widget_cb, 70, 70)
        composition_button = create_button(_('Composition'), \
            self.create_composition_widget_cb, 70, 70)
        exit_button = create_button(_('Exit'), self.exit_cb, 70, 70)
        table = gtk.Table(rows=1, columns=3, homogeneous=False)
        table.attach(products_button, 0, 1, 0, 1)
        table.attach(composition_button, 1, 2, 0, 1)
        table.attach(exit_button, 2, 3, 0, 1)
        switcher.append_page(table)

        # make widgets as attributes
        self.window = window
        self.switcher = switcher

    def start(self):
        gtk.rc_parse('/usr/share/diabetto/rcfile')
        self.window.show_all()
        #self.window.fullscreen()
        gtk.main()


    # callbacks
    def exit_cb(self, event):
        gtk.main_quit()

    def window_keypress_cb(self, widget, event, *args):
        if event.keyval == gtk.keysyms.F6:
            if self.fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
            self.fullscreen = not self.fullscreen

    def create_products_widget_cb(self, widget):
        ProductsWidget(self.controller, self.switcher, self.window)

    def create_composition_widget_cb(self, widget):
        pass

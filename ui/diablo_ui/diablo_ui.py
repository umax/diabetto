#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _
from diabetto.constants import *


class DiabloDiabetto:
    def __init__(self, controller):
        self.controller = controller
        self.page = None
        self.treeview = None
        self.mode = CATEGORIES_MODE
        self.window, self.switcher = self._create_ui()
        self._create_main_page()

    def start(self):
        self.window.show_all()
        gtk.main()

    def exit(self, event):
        gtk.main_quit()

    def _create_ui(self):
        """Creates program UI."""

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(800, 480)
        window.connect('destroy', self.exit)
        switcher = gtk.Notebook()
        window.add(switcher)
        return window, switcher

    def _create_main_page(self):
        """Creates widgets on Main page."""

        products_button = gtk.Button(_('Products'))
        products_button.connect('clicked', self.create_products_page_cb)
        eat_button = gtk.Button(_('Eat'))
        eat_button.connect('clicked', self.create_eat_page_cb)
        exit_button = gtk.Button(_('Exit'))
        exit_button.connect('clicked', self.exit)
        table = gtk.Table(rows=1, columns=3, homogeneous=True)
        table.attach(products_button, 0, 1, 0, 1)
        table.attach(eat_button, 1, 2, 0, 1)
        table.attach(exit_button, 2, 3, 0, 1)
        self.page = self.switcher.append_page(table, gtk.Label('Menu'))
        self.switcher.set_current_page(self.page)

    def _set_treeview_content(self, content):
        """Sets TreeView content."""

        # clear TextView content
        for column in self.treeview.get_columns():
            self.treeview.remove_column(column)

        if self.mode == CATEGORIES_MODE:
            column = gtk.TreeViewColumn(_('Categories'))
            self.treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('width', 800)
            column.pack_start(cell, False)
            column.add_attribute(cell, 'text', 0)
            column.set_sort_column_id(0)
        else:
            column1 = gtk.TreeViewColumn(_('Product'))
            column2 = gtk.TreeViewColumn(_('Uglevodi'))
            column3 = gtk.TreeViewColumn(_('Index'))
            column4 = gtk.TreeViewColumn(_('Category'))
            self.treeview.append_column(column1)
            self.treeview.append_column(column2)
            self.treeview.append_column(column3)
            self.treeview.append_column(column4)
            cell = gtk.CellRendererText()
            cell.set_property('width', 200)
            column1.pack_start(cell, False)
            column1.add_attribute(cell, 'text', 0)
            column1.set_sort_column_id(0)
            column2.pack_start(cell, False)
            column2.add_attribute(cell, 'text', 1)
            column3.pack_start(cell, False)
            column3.add_attribute(cell, 'text', 2)
            column4.pack_start(cell, False)
            column4.add_attribute(cell, 'text', 4)

        self.treeview.set_model(content)


    # callbacks
    def create_products_page_cb(self, widget):
        """Creates widgets for products and categories."""

        table = gtk.Table(rows=3, columns=6)
        categories_button = gtk.Button(_('Categories'))
        categories_button.set_size_request(-1, 70)
        categories_button.connect('clicked', self.show_categories_cb)
        products_button = gtk.Button(_('Products'))
        products_button.set_size_request(-1, 70)
        products_button.connect('clicked', self.show_products_cb)
        menu_button = gtk.Button(_('Menu'))
        menu_button.set_size_request(-1, 70)
        menu_button.connect('clicked', self.show_menu_cb)
        add_button = gtk.Button(_('Add'))
        add_button.set_size_request(-1, 70)
        add_button.connect('clicked', self.add_cb)
        remove_button = gtk.Button(_('Remove'))
        remove_button.set_size_request(-1, 70)
        remove_button.connect('clicked', self.remove_cb)
        edit_button = gtk.Button(_('Edit'))
        edit_button.set_size_request(-1, 70)
        self.treeview = gtk.TreeView()
        self.treeview.connect('row-activated', self.on_treeview_double_click_cb)
        table.attach(categories_button, 0, 2, 0, 1, yoptions=gtk.SHRINK)
        table.attach(products_button, 2, 4, 0, 1, yoptions=gtk.SHRINK)
        table.attach(menu_button, 4, 6, 0, 1, yoptions=gtk.SHRINK)
        table.attach(self.treeview, 0, 6, 1, 2, yoptions=gtk.EXPAND|gtk.FILL)
        table.attach(add_button, 0, 2, 2, 3, yoptions=gtk.SHRINK)
        table.attach(edit_button, 2, 4, 2, 3, yoptions=gtk.SHRINK)
        table.attach(remove_button, 4, 6, 2, 3, yoptions=gtk.SHRINK)
        table.show_all()
        self.page = self.switcher.append_page(table, gtk.Label('Products'))
        self.switcher.set_current_page(self.page)
        self.show_categories_cb(None)   # shows categories at startup

    def create_eat_page_cb(self, widget):
        pass

    def show_menu_cb(self, widget):
        """Shows main menu."""

        self.switcher.remove_page(self.page)
        self.page = 0

    def show_categories_cb(self, widget):
        """Shows all categories."""

        self.mode = CATEGORIES_MODE
        # cname, cid
        liststore = gtk.ListStore(str, int)
        for cname, cid in self.controller.get_categories():
            liststore.append([cname, cid])
        self._set_treeview_content(liststore)

    def show_products_cb(self, widget):
        """Shows all products."""

        self.mode = PRODUCTS_MODE
        # pname, pu, pi, pid, cname, cid
        liststore = gtk.ListStore(str, int, int, int, str, int)
        for pname, pu, pi, pid, cname, cid in self.controller.get_products():
            liststore.append([pname, pu, pi, pid, cname, cid])
        self._set_treeview_content(liststore)

    def on_treeview_double_click_cb(self, widget, row, column):
        """Emits when user double clicks on TreeView item."""

        if self.mode == CATEGORIES_MODE:
            model = self.treeview.get_model()
            cid = model[row[0]][1]
            self.mode = PRODUCTS_MODE
            # pname, pu, pi, pid, cname, cid
            liststore = gtk.ListStore(str, int, int, int, str, int)
            for pname, pu, pi, pid, cname, cid in self.controller.get_products(cid):
                liststore.append([pname, pu, pi, pid, cname, cid])
            self._set_treeview_content(liststore)

    def add_cb(self, widget):
        """Adds new category or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        print model[iterator][0]

    def remove_cb(self, widget):
        """Removes category or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        if self.mode == CATEGORIES_MODE:
            cid = model[iterator][1]
            print cid
        else:
            pid = model[iterator][3]
            print pid
       
    def edit_cb(self, widget):
        """Edits category or product."""
        
        model, iterator = self.treeview.get_selection().get_selected()

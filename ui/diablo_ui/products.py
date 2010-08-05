#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import pango
from gettext import gettext as _
from diabetto.constants import *
from diabetto.ui.diablo_ui.common import create_button
from diabetto.ui.diablo_ui.dialogs import show_question_dialog, \
    show_add_category_dialog, show_add_product_dialog


class ProductsWidget:
    def __init__(self, controller, switcher, toplevel_window):
        self.switcher = switcher
        self.controller = controller
        self.window = toplevel_window
        self.page = None
        self.treeview = None
        self.mode = CATEGORIES_MODE

        # create widgets
        vbox = gtk.VBox()
        top_table = gtk.Table(rows=1, columns=7, homogeneous=True)
        bottom_table = gtk.Table(rows=1, columns=3, homogeneous=True)
        #table = gtk.Table(rows=3, columns=6, homogeneous=False)
        categories_button = create_button(_('Categories'), \
            self.show_categories_cb)
        products_button = create_button(_('Products'), self.show_products_cb)
        menu_button = create_button(_('Menu'), self.show_menu_cb)
        add_button = create_button(_('Add'), self.add_cb)
        remove_button = create_button(_('Remove'), self.remove_cb)
        edit_button = create_button(_('Edit'), self.edit_cb)
        self.treeview = gtk.TreeView()
        self.treeview.connect('row-activated', self.on_treeview_double_click_cb)
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_name('scrolled_window')
        scrolled_window.set_border_width(2)
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        scrolled_window.add_with_viewport(self.treeview)
        top_table.attach(categories_button, 0, 3, 0, 1)
        top_table.attach(products_button, 3, 6, 0, 1)
        top_table.attach(menu_button, 6, 7, 0, 1)
        bottom_table.attach(add_button, 0, 1, 0, 1)
        bottom_table.attach(edit_button, 1, 2, 0, 1)
        bottom_table.attach(remove_button, 2, 3, 0, 1)
        vbox.pack_start(top_table, expand=False)
        vbox.pack_start(scrolled_window)
        vbox.pack_start(bottom_table, expand=False)
        vbox.show_all()
        self.page = self.switcher.append_page(vbox)
        self.switcher.set_current_page(self.page)

        # show categories at startup
        self.show_categories_cb(None)

    def _set_treeview_content(self, content):
        """Sets TreeView content."""

        # clear TextView content
        for column in self.treeview.get_columns():
            self.treeview.remove_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('font-desc', pango.FontDescription( \
                'Nokia Sans 24'))
        cell.set_property('height', 70)

        if self.mode == CATEGORIES_MODE:
            column = gtk.TreeViewColumn(_('Categories'))
            self.treeview.append_column(column)
            column.pack_start(cell, False)
            column.add_attribute(cell, 'text', 0)
            column.set_sort_column_id(0)
        else:
            def float_to_str(column, cell, model, iterator, index):
                cell.set_property('text', str(model[iterator][index]))
                return

            column1 = gtk.TreeViewColumn(_('Product'))
            column1.set_expand(True)
            column1.set_alignment(0.5)
            column2 = gtk.TreeViewColumn(_('Carbohydrates'))
            column2.set_expand(True)
            column2.set_alignment(0.5)
            column3 = gtk.TreeViewColumn(_('Index'))
            column3.set_expand(True)
            column3.set_alignment(0.5)
            column4 = gtk.TreeViewColumn(_('Category'))
            column4.set_expand(True)
            column4.set_alignment(0.5)
            self.treeview.append_column(column1)
            self.treeview.append_column(column2)
            self.treeview.append_column(column3)
            self.treeview.append_column(column4)
            column1.pack_start(cell, False)
            column1.add_attribute(cell, 'text', 0)
            column1.set_sort_column_id(0)
            column2.pack_start(cell, False)
            column2.add_attribute(cell, 'text', 1)
            column2.set_cell_data_func(cell, float_to_str, 1)
            column3.pack_start(cell, False)
            column3.add_attribute(cell, 'text', 2)
            column3.set_cell_data_func(cell, float_to_str, 2)
            column4.pack_start(cell, False)
            column4.add_attribute(cell, 'text', 4)

        self.treeview.set_model(content)


    # callbacks
    def show_menu_cb(self, widget):
        """Shows main menu."""

        self.switcher.remove_page(self.page)
        del self

    def show_categories_cb(self, widget):
        """Shows all categories."""

        self.mode = CATEGORIES_MODE
        # cname, cid
        liststore = gtk.ListStore(str, int)
        for cname, cid in self.controller.get_categories():
            liststore.append([cname.capitalize(), cid])
        self._set_treeview_content(liststore)

    def show_products_cb(self, widget):
        """Shows all products."""

        self.mode = PRODUCTS_MODE
        # pname, pu, pi, pid, cname, cid
        liststore = gtk.ListStore(str, float, float, int, str, int)
        for pname, pu, pi, pid, cname, cid in self.controller.get_products():
            liststore.append([pname.capitalize(), pu, pi, pid, \
                cname.capitalize(), cid])
        self._set_treeview_content(liststore)

    def on_treeview_double_click_cb(self, widget, row, column):
        """Emits when user double clicks on TreeView item."""

        if self.mode == CATEGORIES_MODE:
            model = self.treeview.get_model()
            cid = model[row[0]][1]
            self.mode = PRODUCTS_MODE
            # pname, pu, pi, pid, cname, cid
            liststore = gtk.ListStore(str, float, float, int, str, int)
            for pname, pu, pi, pid, cname, cid in \
                self.controller.get_products(cid):
                liststore.append([pname.capitalize(), pu, pi, pid, \
                    cname.capitalize(), cid])
            self._set_treeview_content(liststore)

    def add_cb(self, widget):
        """Adds new category or product."""

        if self.mode == CATEGORIES_MODE:
            cname = show_add_category_dialog(self.window)
            if cname:
                self.controller.add_category(cname)
                self.show_categories_cb(None)
        else:
            pname, pu, pi, cid = show_add_product_dialog(self.window, \
                self.controller.get_categories())
            if pname:
                self.controller.add_product(pname, pu, pi, cid)
                self.show_products_cb(None)

    def remove_cb(self, widget):
        """Removes category or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        if self.mode == CATEGORIES_MODE:
            try:
                cid = model[iterator][1]
            except: # no category is selected
                return
            else:
                if show_question_dialog(self.window, _('Category removing'), \
                    _('Do you want to remove selected category?')):
                    self.controller.remove_category(cid)
                    self.show_categories_cb(None)
        else:
            try:
                pid = model[iterator][3]
            except: # no product is selected
                return
            else:
                if show_question_dialog(self.window, _('Product removing'), \
                    _('Do you want to remove selected product?')):
                    self.controller.remove_product(pid)
                    self.show_products_cb(None)

    def edit_cb(self, widget):
        """Edits category or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        if self.mode == CATEGORIES_MODE:
            try:
                cname, cid = model[iterator][0], model[iterator][1]
            except: # no category is selected
                return
            else:
                new_cname = show_add_category_dialog(self.window, cname)
                if new_cname:
                    self.controller.update_category(new_cname, cid)
                    self.show_categories_cb(None)
        else:
            try:
                pname, pu, pi, pid, cid = model[iterator][0], \
                    model[iterator][1], model[iterator][2], \
                    model[iterator][3], model[iterator][5]
            except: # no product is selected
                return
            else:
                pname, pu, pi, cid = show_add_product_dialog(self.window,  \
                    self.controller.get_categories(), (pname, pu, pi, cid))
                if pname:
                    self.controller.update_product(pname, pu, pi, pid, cid)
                    self.show_products_cb(None)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import pango
from gettext import gettext as _
from diabetto.constants import *
from diabetto.ui.diablo_ui.common import create_button, \
    cell_capitalizer, cell_float_to_str, create_column
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
        categories_button = create_button(_('Categories'), \
            self.show_categories_cb)
        products_button = create_button(_('Products'), self.show_products_cb)
        menu_button = create_button(None, self.show_menu_cb, \
            stock=gtk.STOCK_GO_BACK)
        add_button = create_button(_('Add'), self.add_cb, stock=gtk.STOCK_ADD)
        remove_button = create_button(_('Remove'), self.remove_cb, \
            stock=gtk.STOCK_DELETE)
        edit_button = create_button(_('Edit'), self.edit_cb, \
            stock=gtk.STOCK_EDIT)
        self.treeview = gtk.TreeView()
        self.treeview.set_headers_visible(True)
        self.treeview.connect('row-activated', self.on_treeview_double_click_cb)
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_name('scrolled_window')
        scrolled_window.set_border_width(2)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.add_with_viewport(self.treeview)
        top_table.attach(categories_button, 0, 3, 0, 1)
        top_table.attach(products_button, 3, 6, 0, 1)
        top_table.attach(menu_button, 6, 7, 0, 1)
        bottom_table.attach(add_button, 0, 1, 0, 1)
        bottom_table.attach(edit_button, 1, 2, 0, 1)
        bottom_table.attach(remove_button, 2, 3, 0, 1)
        vbox.pack_start(top_table, expand=False)
        separator = gtk.HSeparator()
        separator.set_size_request(-1, 1)
        vbox.pack_start(separator, expand=False)
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
            column = create_column(_('Categories'), cell, 0, \
                cell_func=cell_capitalizer)
            column.set_sort_column_id(0)
            self.treeview.append_column(column)
        else:
            column1 = create_column(_('Product'), cell, 0, \
                cell_func=cell_capitalizer)
            column1.set_sort_column_id(0)
            column2 = create_column(_('Carbohydrates'), cell, 1, \
                cell_func=cell_float_to_str)
            column3 = create_column(_('Index'), cell, 2, \
                cell_func=cell_float_to_str)
            column4 = create_column(_('Category'), cell, 4, \
                cell_func=cell_capitalizer)
            for column in (column1, column2, column3, column4):
                self.treeview.append_column(column)

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
        for category in self.controller.get_categories():
            liststore.append(category)
        self._set_treeview_content(liststore)

    def show_products_cb(self, widget, cid=None):
        """Shows all products."""

        self.mode = PRODUCTS_MODE
        # pname, pu, pi, pid, cname, cid
        liststore = gtk.ListStore(str, float, float, int, str, int)
        for product in self.controller.get_products(cid):
            liststore.append(product)
        self._set_treeview_content(liststore)

    def on_treeview_double_click_cb(self, widget, row, column):
        """Emits when user double clicks on TreeView item."""

        if self.mode == CATEGORIES_MODE:
            model = self.treeview.get_model()
            cid = model[row[0]][1]
            self.show_products_cb(None, cid)

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

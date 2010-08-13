#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import pango
from gettext import gettext as _
from diabetto.constants import *
from diabetto.ui.diablo_ui.common import create_button, \
    cell_capitalizer, cell_float_to_str, create_column
from diabetto.ui.diablo_ui.dialogs import show_question_dialog, \
    show_add_composition_dialog, show_add_product_to_composition_dialog


class CompositionsWidget:
    def __init__(self, controller, switcher, toplevel_window):
        self.switcher = switcher
        self.controller = controller
        self.window = toplevel_window
        self.treeview = None
        self.compid = None
        self.page = None
        self.mode = COMPOSITIONS_MODE

        # create widgets
        vbox = gtk.VBox()
        top_table = gtk.Table(rows=1, columns=7, homogeneous=True)
        bottom_table = gtk.Table(rows=1, columns=3, homogeneous=True)
        self.info_label = gtk.Label()
        self.menu_button = create_button(None, self.show_menu_cb, \
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
        top_table.attach(self.info_label, 0, 6, 0, 1)
        top_table.attach(self.menu_button, 6, 7, 0, 1)
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

        # show compositions at startup
        self._show_compositions()

    def _set_treeview_content(self, content):
        """Sets TreeView content."""

        # clear TextView content
        for column in self.treeview.get_columns():
            self.treeview.remove_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('font-desc', pango.FontDescription( \
                'Nokia Sans 22'))
        cell.set_property('height', 70)

        if self.mode == COMPOSITIONS_MODE:
            # content (str, float, int, float, int)
            # compname, carbohydrates, chunks, carbohydrates per chunk, compid
            column1 = create_column(_('Composition'), cell, 0, \
                cell_func=cell_capitalizer)
            column2 = create_column(_('Bread unit'), cell, 1, \
                cell_func=cell_float_to_str)
            column3 = create_column(_('Chunks'), cell, 2)
            column4 = create_column(_('Bread unit per chunk'), cell, 3, \
                cell_func=cell_float_to_str)
            for column in (column1, column2, column3, column4):
                self.treeview.append_column(column)
        else:
            # content (str, int, int)
            # productname, productweight, productid
            column1 = create_column(_('Product'), cell, 0, \
                cell_func=cell_capitalizer)
            column2 = create_column(_('Weight'), cell, 1)
            for column in (column1, column2):
                self.treeview.append_column(column)

        self.treeview.set_model(content)
        content.set_sort_column_id(0, gtk.SORT_ASCENDING)


    def _show_compositions(self):
        """Shows existing compositions."""

        self.mode = COMPOSITIONS_MODE

        # compname, carbohydrates, chunks, carbohydrates per chunk, compid
        liststore = gtk.ListStore(str, float, int, float, int)
        for composition in self.controller.get_compositions():
            liststore.append(composition)
        self._set_treeview_content(liststore)

        # update widgets
        self.info_label.set_text( \
            '%s: %s' % (_('Compositions number'), len(liststore)))
        #self.menu_button.set_label(_('Menu'))

    def _show_products_in_composition(self):
        """Shows products for composition."""

        # productname, productweight, productid
        liststore = gtk.ListStore(str, int, int)
        for content in self.controller.get_composition_content(self.compid):
            liststore.append(content)
        self._set_treeview_content(liststore)

        # update widgets
        self.info_label.set_text( \
            '%s: %s' % (_('Products number'), len(liststore)))
        #self.menu_button.set_label(_('Back'))


    # callbacks
    def show_menu_cb(self, widget):
        """Shows main menu."""

        if self.mode == COMPOSITIONS_MODE:
            self.switcher.remove_page(self.page)
            del self
        else:
            self._show_compositions()

    def on_treeview_double_click_cb(self, widget, row, column):
        """
        Emits when user double clicks on TreeView item.
        Shows composition content.
        """

        if self.mode == COMPOSITIONS_MODE:
            self.mode = COMPOSITION_MODE
            model = self.treeview.get_model()
            self.compid, chunks = model[row[0]][4], model[row[0]][2]
            self._show_products_in_composition()

    def add_cb(self, widget):
        """Adds new composition or product to composition."""

        if self.mode == COMPOSITIONS_MODE:
            compname, chunks = show_add_composition_dialog(self.window)
            if compname:
                self.controller.add_composition(compname, chunks)
                self._show_compositions()
        else:
            pid, pweight = show_add_product_to_composition_dialog( \
                self.window, self.controller)
            if pweight is not None:
                self.controller.add_product_to_composition( \
                    self.compid, pid, pweight)
            self._show_products_in_composition()

    def remove_cb(self, widget):
        """Removes composition or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        if self.mode == COMPOSITIONS_MODE:
            try:
                compid = model[iterator][4]
            except: # no composition is selected
                return
            else:
                if show_question_dialog(self.window, \
                    _('Composition removing'), \
                    _('Do you want to remove selected composition?')):
                    self.controller.remove_composition(compid)
                    self._show_compositions()
        else:
            try:
                pid = model[iterator][2]
            except: # no product is selected
                return
            else:
                if show_question_dialog(self.window, _('Product removing'), \
                    _('Do you want to remove selected product from composition?')):
                    self.controller.remove_product_from_composition( \
                        self.compid, pid)
                    self._show_products_in_composition()

    def edit_cb(self, widget):
        """Edits composition or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        if self.mode == COMPOSITIONS_MODE:
            try:
                row = model[iterator]
                compname, chunks, compid = row[0], row[2], row[4]
            except: # no composition is selected
                return
            else:
                compname, chunks = show_add_composition_dialog( \
                    self.window, (compname, chunks))
                if compname:
                    self.controller.update_composition(compid, compname, chunks)
                    self._show_compositions()
        else:
            try:
                row = model[iterator]
                pname, pweight, pid = row[0], row[1], row[2]
            except: # no product is selected
                return
            else:
                pid, pweight = show_add_product_to_composition_dialog( \
                    self.window, self.controller, (pname, pweight, pid))
                if pweight is not None:
                    self.controller.update_product_in_composition( \
                        self.compid, pid, pweight)
                    self._show_products_in_composition()

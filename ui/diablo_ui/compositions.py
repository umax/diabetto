#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import pango
from gettext import gettext as _
from diabetto.constants import *
from diabetto.ui.diablo_ui.common import create_button
from diabetto.ui.diablo_ui.dialogs import show_question_dialog, \
    show_add_product_dialog, show_add_composition_dialog


class CompositionsWidget:
    def __init__(self, controller, switcher, toplevel_window):
        self.switcher = switcher
        self.controller = controller
        self.window = toplevel_window
        self.treeview = None
        self.page = None
        self.chunks = 3
        self.mode = COMPOSITIONS_MODE

        # create widgets
        vbox = gtk.VBox()
        top_table = gtk.Table(rows=1, columns=7, homogeneous=True)
        bottom_table = gtk.Table(rows=1, columns=3, homogeneous=True)
        self.chunks_label = gtk.Label( \
           '%s: %s' % (_('Chunks'), str(self.chunks)))
        self.increase_button = gtk.Button('+')
        self.decrease_button = gtk.Button('-')
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
        top_table.attach(self.decrease_button, 0, 2, 0, 1)
        top_table.attach(self.chunks_label, 2, 4, 0, 1)
        top_table.attach(self.increase_button, 4, 6, 0, 1)
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

        # show compositions at startup
        self._show_compositions()

    def _set_treeview_content(self, content):
        """Sets TreeView content."""

        def float_to_str(column, cell, model, iterator, index):
            cell.set_property('text', str(model[iterator][index]))
            return

        # clear TextView content
        for column in self.treeview.get_columns():
            self.treeview.remove_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('font-desc', pango.FontDescription( \
                'Nokia Sans 24'))
        cell.set_property('height', 70)

        if self.mode == COMPOSITIONS_MODE:
            # content (str,float,int,float,int)
            # compname, carbohydrates, chunks, carbohydrates per chunk, compid
            column1 = gtk.TreeViewColumn(_('Composition'))
            column1.set_alignment(0.5)
            column1.set_expand(True)
            column1.pack_start(cell, False)
            column1.add_attribute(cell, 'text', 0)
            column1.set_sort_column_id(0)
            column2 = gtk.TreeViewColumn(_('Carbohydrates'))
            column2.set_alignment(0.5)
            column2.set_expand(True)
            column2.pack_start(cell, False)
            column2.add_attribute(cell, 'text', 1)
            column2.set_cell_data_func(cell, float_to_str, 1)
            column3 = gtk.TreeViewColumn(_('Chunks'))
            column3.set_alignment(0.5)
            column3.set_expand(True)
            column3.pack_start(cell, False)
            column3.add_attribute(cell, 'text', 2)
            column4 = gtk.TreeViewColumn(_('Carbohydrates per chunk'))
            column4.set_alignment(0.5)
            column4.set_expand(True)
            column4.pack_start(cell, False)
            column4.add_attribute(cell, 'text', 3)
            column4.set_cell_data_func(cell, float_to_str, 3)
            self.treeview.append_column(column1)
            self.treeview.append_column(column2)
            self.treeview.append_column(column3)
            self.treeview.append_column(column4)
        else:
            # content (str,int,int)
            # productname, productweight, productid
            column1 = gtk.TreeViewColumn(_('Product'))
            column1.set_expand(True)
            column1.set_alignment(0.5)
            column1.pack_start(cell, False)
            column1.add_attribute(cell, 'text', 0)
            column1.set_sort_column_id(0)
            column2 = gtk.TreeViewColumn(_('Weight'))
            column2.set_expand(True)
            column2.set_alignment(0.5)
            column2.pack_start(cell, False)
            column2.add_attribute(cell, 'text', 1)
            self.treeview.append_column(column1)
            self.treeview.append_column(column2)

        self.treeview.set_model(content)

    def _show_compositions(self):
        """Shows existing compositions."""

        self.mode = COMPOSITIONS_MODE

        # compname, carbohydrates, chunks, carbohydrates per chunk, compid
        liststore = gtk.ListStore(str, float, int, float, int)
        for compname, carb, chunks, carb_per_chunk, compid in \
            self.controller.get_compositions():
            liststore.append([compname.capitalize(), carb, chunks, \
                carb_per_chunk, compid])
        self._set_treeview_content(liststore)

        # hide unnecessary widget
        self.increase_button.hide()
        self.decrease_button.hide()
        self.chunks_label.set_text('%s: %s' % (_('Compositions number'), \
            len(liststore)))


    # callbacks
    def show_menu_cb(self, widget):
        """Shows main menu."""

        self.switcher.remove_page(self.page)
        del self

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
        """Adds new composition or product to composition."""

        if self.mode == COMPOSITIONS_MODE:
            compname, chunks = show_add_composition_dialog(self.window)
            if compname:
                self.controller.add_composition(compname, chunks)
                self._show_compositions()
        else:
            pname, pu, pi, cid = show_add_product_dialog(self.window, \
                self.controller.get_categories())
            if pname:
                self.controller.add_product(pname, pu, pi, cid)
                self.show_products_cb(None)

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
                pid = model[iterator][3]
            except: # no product is selected
                return
            else:
                if show_question_dialog(self.window, _('Product removing'), \
                    _('Do you want to remove selected product?')):
                    self.controller.remove_product(pid)
                    self.show_products_cb(None)

    def edit_cb(self, widget):
        """Edits composition or product."""

        model, iterator = self.treeview.get_selection().get_selected()
        if self.mode == COMPOSITIONS_MODE:
            try:
                compname, chunks, compid = model[iterator][0], \
                    model[iterator][2], model[iterator][4]
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

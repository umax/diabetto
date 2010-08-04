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
        #self.window.fullscreen()
        gtk.main()

    def exit(self, event):
        gtk.main_quit()

    def _create_ui(self):
        """Creates program UI."""

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.resize(800, 480)
        window.connect('destroy', self.exit)
        switcher = gtk.Notebook()
        switcher.set_show_tabs(False)
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
            column2 = gtk.TreeViewColumn(_('Carbohydrates'))
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

    # dialogs
    def show_question_dialog(self, title, question):
        """Shows Question dialog."""

        dialog = gtk.Dialog(title=title, parent=self.window, buttons=( \
            _('Yes'), gtk.RESPONSE_YES, _('No'), gtk.RESPONSE_NO))
        label = gtk.Label(question)
        label.show()
        dialog.vbox.pack_start(label)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            return True
        return False

    def show_add_category_dialog(self, data=None):
        """Shows AddCategory dialog."""

        dialog = gtk.Dialog(title=_('Add new category'), parent=self.window, \
            buttons=(_('Add'), gtk.RESPONSE_OK, _('Cancel'), \
            gtk.RESPONSE_CANCEL))
        # creating widgets
        table = gtk.Table(rows=1, columns=2, homogeneous=False)
        table.set_col_spacings(10)
        cname_label = gtk.Label(_('Category name'))
        cname_entry = gtk.Entry()
        if data:
            cname_entry.set_text(data)
        # packing widgets
        table.attach(cname_label, 0, 1, 0, 1)
        table.attach(cname_entry, 1, 2, 0, 1)
        dialog.vbox.pack_start(table)
        dialog.vbox.show_all()
        response = dialog.run()
        cname = cname_entry.get_text()
        dialog.destroy()
        if response == gtk.RESPONSE_OK and cname:
            return cname
        return None

    def show_add_product_dialog(self, data=None):
        """Shows AddProduct dialog."""

        dialog = gtk.Dialog(title=_('Add new product'), parent=self.window, \
            buttons=(_('Add'), gtk.RESPONSE_OK, _('Cancel'), \
            gtk.RESPONSE_CANCEL))
        # creating widgets
        table = gtk.Table(rows=4, columns=2, homogeneous=False)
        table.set_col_spacings(10)
        table.set_row_spacings(4)
        pname_label = gtk.Label(_('Product name'))
        pname_entry = gtk.Entry()
        pu_label = gtk.Label(_('Carbohydrates'))
        pu_entry = gtk.Entry()
        pi_label = gtk.Label(_('Index'))
        pi_entry = gtk.Entry()
        category_label = gtk.Label(_('Category'))
        # populating category list
        liststore = gtk.ListStore(str, int)
        for cname, cid in self.controller.get_categories():
            liststore.append([cname, cid])
        combobox = gtk.ComboBox(liststore)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell, False)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_active(0)
        # cheking for edit mode
        if data is not None: # edit mode
            pname_entry.set_text(data[0])
            pu_entry.set_text(str(data[1]))
            pi_entry.set_text(str(data[2]))
            for index in range(len(liststore)):
                if liststore[index][1] == data[3]:
                    combobox.set_active(index)
                    break
        # packing widgets
        table.attach(pname_label, 0, 1, 0, 1)
        table.attach(pname_entry, 1, 2, 0, 1)
        table.attach(pu_label, 0, 1, 1, 2)
        table.attach(pu_entry, 1, 2, 1, 2)
        table.attach(pi_label, 0, 1, 2, 3)
        table.attach(pi_entry, 1, 2, 2, 3)
        table.attach(category_label, 0, 1, 3, 4)
        table.attach(combobox, 1, 2, 3, 4)
        dialog.vbox.pack_start(table)
        dialog.vbox.show_all()
        response = dialog.run()
        # getting values
        pname = pname_entry.get_text()
        pu = pu_entry.get_text()
        pi = pi_entry.get_text()
        model, active = combobox.get_model(), combobox.get_active()
        cid = model[active][1]
        dialog.destroy()
        if response == gtk.RESPONSE_OK and pname:
            return pname, pu, pi, cid
        return None, None, None, None


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
        edit_button.connect('clicked', self.edit_cb)
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
        if self.mode == CATEGORIES_MODE:
            cname = self.show_add_category_dialog()
            if cname:
                self.controller.add_category(cname)
                self.show_categories_cb(None)
        else:
            pname, pu, pi, cid = self.show_add_product_dialog()
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
                if self.show_question_dialog(_('Category removing'), \
                    _('Do you want to remove selected category?')):
                    self.controller.remove_category(cid)
                    self.show_categories_cb(None)
        else:
            try:
                pid = model[iterator][3]
            except: # no product is selected
                return
            else:
                if self.show_question_dialog(_('Product removing'), \
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
                new_cname = self.show_add_category_dialog(cname)
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
                pname, pu, pi, cid = self.show_add_product_dialog( \
                    (pname, pu, pi, cid))
                if pname:
                    self.controller.update_product(pname, pu, pi, pid, cid)
                    self.show_products_cb(None)

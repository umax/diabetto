#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _


def show_question_dialog(parent, title, question):
    """Shows Question dialog."""

    dialog = gtk.Dialog(title=title, parent=parent, buttons=( \
        _('Yes'), gtk.RESPONSE_YES, _('No'), gtk.RESPONSE_NO))
    label = gtk.Label('\n' + question + '\n')
    dialog.vbox.pack_start(label)
    dialog.vbox.show_all()
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
        return True
    return False


def show_add_category_dialog(parent, data=None):
    """Shows AddCategory dialog."""

    dialog = gtk.Dialog(parent=parent)
    if data is None:
        dialog.add_button(_('Add'), gtk.RESPONSE_OK)
        dialog.set_title(_('Add new category'))
    else:
        dialog.add_button(_('Modify'), gtk.RESPONSE_OK)
        dialog.set_title(_('Modify category'))
    dialog.add_button(_('Cancel'), gtk.RESPONSE_CANCEL)

    # creating widgets
    table = gtk.Table(rows=1, columns=2, homogeneous=True)
    table.set_border_width(8)
    table.set_col_spacings(10)
    cname_label = gtk.Label(_('Category name'))
    cname_entry = gtk.Entry()
    cname_entry.set_name('entry_widget')
    if data:
        cname_entry.set_text(data)
    # packing widgets
    table.attach(cname_label, 0, 1, 0, 1)
    table.attach(cname_entry, 1, 2, 0, 1, ypadding=gtk.EXPAND|gtk.FILL)
    dialog.vbox.pack_start(table, padding=8)
    dialog.vbox.show_all()
    response = dialog.run()
    cname = cname_entry.get_text()
    dialog.destroy()
    if response == gtk.RESPONSE_OK and cname:
        return cname
    return None


def show_add_product_dialog(parent, categories, data=None):
    """Shows AddProduct dialog."""

    dialog = gtk.Dialog(parent=parent)
    if data is None:
        dialog.add_button(_('Add'), gtk.RESPONSE_OK)
        dialog.set_title(_('Add new product'))
    else:
        dialog.add_button(_('Modify'), gtk.RESPONSE_OK)
        dialog.set_title(_('Modify product'))
    dialog.add_button(_('Cancel'), gtk.RESPONSE_CANCEL)
    # creating widgets
    table = gtk.Table(rows=4, columns=2, homogeneous=True)
    table.set_border_width(8)
    table.set_col_spacings(10)
    table.set_row_spacings(8)
    pname_label = gtk.Label(_('Product name'))
    pname_entry = gtk.Entry()
    pname_entry.set_name('entry_widget')
    pu_label = gtk.Label(_('Carbohydrates'))
    pu_entry = gtk.Entry()
    pu_entry.set_name('entry_widget')
    pi_label = gtk.Label(_('Index'))
    pi_entry = gtk.Entry()
    pi_entry.set_name('entry_widget')
    category_label = gtk.Label(_('Category'))
    # populating category list
    liststore = gtk.ListStore(str, int)
    for cname, cid in categories:
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
    table.attach(pname_entry, 1, 2, 0, 1, xoptions=gtk.EXPAND|gtk.FILL)
    table.attach(pu_label, 0, 1, 1, 2)
    table.attach(pu_entry, 1, 2, 1, 2, xoptions=gtk.EXPAND|gtk.FILL)
    table.attach(pi_label, 0, 1, 2, 3)
    table.attach(pi_entry, 1, 2, 2, 3, xoptions=gtk.EXPAND|gtk.FILL)
    table.attach(category_label, 0, 1, 3, 4)
    table.attach(combobox, 1, 2, 3, 4, xoptions=gtk.EXPAND|gtk.FILL)
    dialog.vbox.pack_start(table, expand=True)
    dialog.vbox.show_all()
    response = dialog.run()
    # getting values
    pname = pname_entry.get_text()
    try:
        pu = float(pu_entry.get_text().replace(',', '.'))
        pi = float(pi_entry.get_text().replace(',', '.'))
    except:
        dialog.destroy()
        return None, None, None, None
    model, active = combobox.get_model(), combobox.get_active()
    cid = model[active][1]
    dialog.destroy()
    if response == gtk.RESPONSE_OK and pname:
        return pname, pu, pi, cid
    return None, None, None, None



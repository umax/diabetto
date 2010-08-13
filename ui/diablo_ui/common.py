#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk


def create_button(caption, callback, width=-1, height=70, stock=None):
    """Creates customized button."""

    button = gtk.Button()
    if stock is not None:
        hbox = gtk.HBox(False, 0)
        image = gtk.image_new_from_stock(stock, gtk.ICON_SIZE_LARGE_TOOLBAR)
        hbox.pack_start(image)
        if caption is not None:
            label = gtk.Label(caption)
            label.set_justify(gtk.JUSTIFY_LEFT)
            hbox.pack_start(label)
        button.add(hbox)
    else:
        button.set_label(caption)
    button.set_size_request(width, height)
    button.set_focus_on_click(False)
    button.connect('clicked', callback)
    return button


def cell_float_to_str(column, cell, model, iterator, index):
    """Formats float number."""

    cell.set_property('text', '%.2f' % model[iterator][index])
    return


def cell_capitalizer(column, cell, model, iterator, index):
    """Capitalizes cell text."""

    cell.set_property('text', \
        model[iterator][index].decode('utf-8').capitalize())
    return


def create_column(title, cell, index, alignment=0.5, cell_func=None):
    """Creates customized TreeView column."""

    column = gtk.TreeViewColumn(title)
    column.set_alignment(alignment)
    column.set_expand(True)
    column.pack_start(cell, False)
    column.add_attribute(cell, 'text', index)
    if cell_func is not None:
        column.set_cell_data_func(cell, cell_func, index)
    return column


def create_combobox(items=[], active_item_id=None):
    """Creates combobox and populates it."""

    liststore = gtk.ListStore(str, int)
    for item in items:
        liststore.append(item)
    combobox = gtk.ComboBox(liststore)
    cell = gtk.CellRendererText()
    combobox.pack_start(cell, False)
    combobox.add_attribute(cell, 'text', 0)
    if active_item_id is None:
        combobox.set_active(0)
    else:
        for index in range(len(liststore)):
            if liststore[index][1] == active_item_id:
                combobox.set_active(index)
                break
    return combobox



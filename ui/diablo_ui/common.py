#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk


def create_button(caption, callback, width=-1, height=70):
    """Creates customized button."""

    button = gtk.Button(caption)
    button.set_size_request(width, height)
    button.connect('clicked', callback)
    return button


def cell_float_to_str(column, cell, model, iterator, index):
    """Formats float number."""

    cell.set_property('text', str(model[iterator][index]))
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



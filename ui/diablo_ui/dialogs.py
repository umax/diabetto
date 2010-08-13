#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _
from diabetto.ui.diablo_ui.common import create_combobox


def show_question_dialog(parent, title, question):
    """Shows Question dialog."""

    dialog = gtk.Dialog(title=title, parent=parent, buttons=( \
        _('Yes'), gtk.RESPONSE_YES, _('No'), gtk.RESPONSE_NO), \
        flags=gtk.DIALOG_NO_SEPARATOR)
    label = gtk.Label('\n' + question + '\n')
    image = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION, \
        gtk.ICON_SIZE_DIALOG)
    hbox = gtk.HBox(False, 8)
    hbox.pack_start(image)
    hbox.pack_start(label, padding=4)
    dialog.vbox.pack_start(hbox)
    dialog.vbox.show_all()
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
        return True
    return False


def show_error_dialog(parent, title, text):
    """Shows Error dialog."""

    dialog = gtk.Dialog(title=title, parent=parent, buttons=( \
        _('Ok'), gtk.RESPONSE_OK), flags=gtk.DIALOG_NO_SEPARATOR)
    label = gtk.Label('\n' + text + '\n')
    image = gtk.image_new_from_stock(gtk.STOCK_DIALOG_ERROR, \
        gtk.ICON_SIZE_DIALOG)
    hbox = gtk.HBox(False, 8)
    hbox.pack_start(image)
    hbox.pack_start(label, padding=4)
    dialog.vbox.pack_start(hbox)
    dialog.vbox.show_all()
    response = dialog.run()
    dialog.destroy()


def show_add_composition_dialog(parent, data=None):
    """
    Shows AddComposition dialog.
    data: (compname, chunks)
    """

    dialog = gtk.Dialog(parent=parent, flags=gtk.DIALOG_NO_SEPARATOR)
    if data is None:
        dialog.add_button(_('Add'), gtk.RESPONSE_OK)
        dialog.set_title(_('Add new composition'))
    else:
        dialog.add_button(_('Modify'), gtk.RESPONSE_OK)
        dialog.set_title(_('Modify composition'))
    dialog.add_button(_('Cancel'), gtk.RESPONSE_CANCEL)

    # creating widgets
    table = gtk.Table(rows=2, columns=2, homogeneous=True)
    table.set_border_width(8)
    table.set_col_spacings(10)
    compname_label = gtk.Label(_('Composition name'))
    compname_entry = gtk.Entry()
    compname_entry.set_name('entry_widget')
    chunks_label = gtk.Label(_('Chunks'))
    chunks_entry = gtk.Entry()
    chunks_entry.set_name('entry_widget')
    chunks_entry.set_text('3')

    # checking for edit mode
    if data:
        compname_entry.set_text(data[0])
        chunks_entry.set_text(str(data[1]))

    # packing widgets
    table.attach(compname_label, 0, 1, 0, 1)
    table.attach(compname_entry, 1, 2, 0, 1, ypadding=gtk.EXPAND|gtk.FILL)
    table.attach(chunks_label, 0, 1, 1, 2)
    table.attach(chunks_entry, 1, 2, 1, 2, ypadding=gtk.EXPAND|gtk.FILL)
    dialog.vbox.pack_start(table, padding=8)
    dialog.vbox.show_all()
    response = dialog.run()
    compname = compname_entry.get_text()
    if response == gtk.RESPONSE_OK:
        try:
            chunks = int(chunks_entry.get_text())
            if chunks == 0:
                chunks = 3
        except:
            pass
        else:
            dialog.destroy()
            return compname, chunks
    dialog.destroy()
    return None, None


def show_add_product_to_composition_dialog(parent, controller, data=None):
    """
    Shows AddProductToCompositions dialog.
    data: (pname, pweight, pid)
    """

    def on_change_category_cb(widget, controller, pcombobox):
        """Emits when user changes category."""

        cmodel, active = widget.get_model(), widget.get_active()
        cid = cmodel[active][1]
        pmodel = pcombobox.get_model()
        pmodel.clear()
        for product in controller.get_products_by_category(cid):
            pmodel.append(product)
        pcombobox.set_active(0)


    dialog = gtk.Dialog(parent=parent, flags=gtk.DIALOG_NO_SEPARATOR)
    if data is None:
        dialog.add_button(_('Add'), gtk.RESPONSE_OK)
        dialog.set_title(_('Add new product to composition'))
    else:
        dialog.add_button(_('Modify'), gtk.RESPONSE_OK)
        dialog.set_title(_('Modify product in composition'))
    dialog.add_button(_('Cancel'), gtk.RESPONSE_CANCEL)

    # creating widgets
    table = gtk.Table(rows=3, columns=2, homogeneous=True)
    table.set_border_width(8)
    table.set_col_spacings(10)
    cname_label = gtk.Label(_('Category name'))
    pname_label = gtk.Label(_('Product name'))
    pweight_label = gtk.Label(_('Product weight'))
    pweight_entry = gtk.Entry()
    pweight_entry.set_text('0')
    pweight_entry.set_name('entry_widget')

    # cheking for edit mode
    if data is not None:
        pweight, pid = data[1], data[2]
        pweight_entry.set_text(str(pweight))
        cid = controller.get_product_category(pid)
        ccombobox = create_combobox(controller.get_categories(), cid)
        pcombobox = create_combobox(controller.get_products_by_category(cid), \
            pid)
        ccombobox.set_sensitive(False)
        pcombobox.set_sensitive(False)
    else:
        pcombobox = create_combobox(controller.get_products_list())
        ccombobox = create_combobox(controller.get_categories())
        ccombobox.connect('changed', on_change_category_cb, controller, \
            pcombobox)
        on_change_category_cb(ccombobox, controller, pcombobox)

    # packing widgets
    table.attach(cname_label, 0, 1, 0, 1)
    table.attach(ccombobox, 1, 2, 0, 1, ypadding=gtk.EXPAND|gtk.FILL)
    table.attach(pname_label, 0, 1, 1, 2)
    table.attach(pcombobox, 1, 2, 1, 2, ypadding=gtk.EXPAND|gtk.FILL)
    table.attach(pweight_label, 0, 1, 2, 3)
    table.attach(pweight_entry, 1, 2, 2, 3, ypadding=gtk.EXPAND|gtk.FILL)
    dialog.vbox.pack_start(table, padding=8)
    dialog.vbox.show_all()
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        try:
            pweight = int(pweight_entry.get_text())
            model, active = pcombobox.get_model(), pcombobox.get_active()
            pid = model[active][1]
        except:
            pass
        else:
            dialog.destroy()
            return pid, pweight
    dialog.destroy()
    return None, None


def show_add_category_dialog(parent, data=None):
    """Shows AddCategory dialog."""

    dialog = gtk.Dialog(parent=parent, flags=gtk.DIALOG_NO_SEPARATOR)
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


def show_add_product_dialog(parent, categories, data=None, \
    selected_category_id=None):
    """Shows AddProduct dialog."""

    dialog = gtk.Dialog(parent=parent, flags=gtk.DIALOG_NO_SEPARATOR)
    if data is None:
        dialog.add_button(_('Add'), gtk.RESPONSE_OK)
        dialog.set_title(_('Add new product'))
    else:
        dialog.add_button(_('Modify'), gtk.RESPONSE_OK)
        dialog.set_title(_('Modify product'))
    dialog.add_button(_('Cancel'), gtk.RESPONSE_CANCEL)

    # creating widgets
    table = gtk.Table(rows=3, columns=2, homogeneous=True)
    table.set_border_width(8)
    table.set_col_spacings(10)
    table.set_row_spacings(8)
    pname_label = gtk.Label(_('Product name'))
    pname_entry = gtk.Entry()
    pname_entry.set_name('entry_widget')
    pu_label = gtk.Label(_('Carbohydrates'))
    pu_entry = gtk.Entry()
    pu_entry.set_name('entry_widget')
    #pi_label = gtk.Label(_('Index'))
    #pi_entry = gtk.Entry()
    #pi_entry.set_name('entry_widget')
    category_label = gtk.Label(_('Category'))

    combobox = create_combobox(categories, selected_category_id)

    # cheking for edit mode
    if data is not None: # edit mode
        pname_entry.set_text(data[0])
        pu_entry.set_text(str(data[1]))
        #pi_entry.set_text(str(data[2]))
        model = combobox.get_model()
        for index in range(len(model)):
            if model[index][1] == data[3]:
                combobox.set_active(index)
                break

    # packing widgets
    table.attach(pname_label, 0, 1, 0, 1)
    table.attach(pname_entry, 1, 2, 0, 1, xoptions=gtk.EXPAND|gtk.FILL)
    table.attach(pu_label, 0, 1, 1, 2)
    table.attach(pu_entry, 1, 2, 1, 2, xoptions=gtk.EXPAND|gtk.FILL)
    # temporary disable pi widgets
    #table.attach(pi_label, 0, 1, 2, 3)
    #table.attach(pi_entry, 1, 2, 2, 3, xoptions=gtk.EXPAND|gtk.FILL)
    #table.attach(category_label, 0, 1, 3, 4)
    #table.attach(combobox, 1, 2, 3, 4, xoptions=gtk.EXPAND|gtk.FILL)

    table.attach(category_label, 0, 1, 2, 3)
    table.attach(combobox, 1, 2, 2, 3, xoptions=gtk.EXPAND|gtk.FILL)
    dialog.vbox.pack_start(table, expand=True)
    dialog.vbox.show_all()
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        pname = pname_entry.get_text()
        try:
            pu = float(pu_entry.get_text().replace(',', '.'))
            #pi = float(pi_entry.get_text().replace(',', '.'))
            pi = 1.0
        except:
            pass
        else:
            model, active = combobox.get_model(), combobox.get_active()
            cid = model[active][1]
            dialog.destroy()
            return pname, pu, pi, cid
    dialog.destroy()
    return None, None, None, None

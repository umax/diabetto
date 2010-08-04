#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gtk


def create_button(caption, callback, width=-1, height=70):
    button = gtk.Button(caption)
    button.set_size_request(width, height)
    button.connect('clicked', callback)
    return button


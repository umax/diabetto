#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gtk

# fixme
IMAGE_PATH = '/usr/share/diabetto/images'


def create_button(image_name, callback, width=-1, height=70):
    button = gtk.Button()
    button.set_size_request(width, height)
    image = gtk.image_new_from_file(os.path.join(IMAGE_PATH, image_name))
    button.set_image(image)
    button.connect('clicked', callback)
    return button


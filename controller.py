"""
Diabetto controller class
"""

from gettext import gettext as _


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.start()

    def stop(self):
        """Exit the program."""

        self.model.close()

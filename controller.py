"""
Diabetto controller class
"""

from gettext import gettext as _


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view(self)
        self.view.start()

    def stop(self):
        """Exit the program."""

        self.model.close()

    def get_categories(self):
        return self.model.get_categories()

    def get_products(self, cid=None):
        result = []
        for product in self.model.get_products(cid):
            cname, cid = self.model.get_category_by_id(product[3])
            result.append([product[0], product[1], product[2], product[4], \
                cname, cid])
        return result

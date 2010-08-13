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
        """Gets all categories."""

        return self.model.get_categories()

    def get_products(self, cid=None):
        """Gets all products or products for selected category."""

        result = []
        for product in self.model.get_products(cid):
            cname, cid = self.model.get_category_by_id(product[3])
            result.append([product[0], product[1], product[2], product[4], \
                cname, cid])
        return result

    def get_product_category(self, pid):
        """Gets product category for selected product."""

        return self.model.get_product_category(pid)

    def get_products_by_category(self, cid):
        """Gets all products for selected category."""

        return self.model.get_products_by_category(cid)

    def get_products_list(self):
        """Gets product list."""

        return [(pname, pid) for pname, pu, pi, cid, pid in \
            self.model.get_products(None)]

    def get_composition_content(self, compid):
        """Gets all composition products."""

        model = self.model # accelerate database operations
        result = []
        for pid, pweight in model.get_composition_content(compid):
            pname, pu, pi = model.get_product_by_id(pid)
            result.append((pname, pweight, pid))
        return result

    def get_compositions(self):
        """Gets all compositions from database and calculate its params."""

        model = self.model # accelerate database operations
        result = []
        for compname, compid, chunks in model.get_compositions():
            carbohydrates = 0
            for pid, pweight in model.get_composition_content(compid):
                pname, pu, pi = model.get_product_by_id(pid)
                carbohydrates += (pu / 100.0 * pweight)
            result.append((compname, carbohydrates / 11.0, chunks, \
                carbohydrates / chunks / 11.0, compid))
        return result

    def add_category(self, cname):
        """Adds new category to database."""

        if not cname or cname is None:
            return
        if not self.model.add_category(cname.strip()):
            self.view.show_error_dialog( \
                _('Adding category error'), \
                _('Unable to add category.\nCategory already in database!'))

    def update_category(self, cname, cid):
        """Updates existing category."""

        self.model.update_category(cname, cid)

    def remove_category(self, cid):
        """Removes category except 'default' category."""

        if cid != 1:
            self.model.del_category(cid)

    def add_product(self, product):
        """Adds new product to database."""

        pname, pu, pi, cid = product
        if (not pu) or (not pi) or (not cid):
            return
        if not self.model.add_product(pname.strip(), pu, pi, cid):
            self.view.show_error_dialog( \
                _('Adding product error'), \
                _('Unable to add product.\nProduct already in database!'))

    def add_product_to_composition(self, compid, pid, pweight):
        """Adds new products to existing composition."""

        self.model.add_product_to_composition(compid, pid, pweight)

    def update_product(self, pname, pu, pi, pid, cid):
        """Updates existing product."""

        self.model.update_product(pname, pu, pi, pid, cid)

    def update_product_in_composition(self, compid, pid, pweight):
        """Updates product properties in composition."""

        self.model.update_product_in_composition(compid, pid, pweight)

    def remove_product(self, pid):
        """Removes existing product."""

        self.model.del_product(pid)

    def remove_product_from_composition(self, compid, pid):
        """Removes existing product from existing composition."""

        self.model.del_product_from_composition(compid, pid)

    def add_composition(self, compname, chunks):
        """Adds new composition to database."""

        self.model.add_composition(compname, chunks)

    def update_composition(self, compid, compname, chunks):
        """Updates existing composition."""

        self.model.update_composition(compid, compname, chunks)

    def remove_composition(self, compid):
        """Removes existing composition."""

        self.model.del_composition(compid)

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
            return False
        if not self.model.add_category(cname.strip()):
            self.view.show_error_dialog( \
                _('Adding category error'), \
                _('Unable to add category.\nCategory already in database!'))
            return False
        return True

    def update_category(self, cname, cid):
        """Updates existing category."""

        if cname:
            if not self.model.update_category(cname.strip(), cid):
                self.view.show_error_dialog( \
                    _('Updating category error'), \
                    _('Unable to rename category.\nCategory already in ' \
                    'database!'))
                return False
            return True

    def remove_category(self, cid):
        """Removes category except 'default' category."""

        if cid != 1:
            self.model.del_category(cid)

    def add_product(self, product):
        """Adds new product to database."""

        pname, pu, pi, cid = product
        if (not pu) or (not pi) or (not cid):
            return False
        if not self.model.add_product(pname.strip(), pu, pi, cid):
            self.view.show_error_dialog( \
                _('Adding product error'), \
                _('Unable to add product.\nProduct already in database!'))
            return False
        return True

    def add_product_to_composition(self, compid, product):
        """Adds new products to existing composition."""

        pid, pweight = product
        if pweight < 0:
            return False
        if not self.model.add_product_to_composition(compid, pid, pweight):
            self.view.show_error_dialog( \
                _('Adding product error'), \
                _('Unable to add product to composition.\nProduct already in ' \
                'composition!'))
            return False
        return True

    def update_product(self, pname, pu, pi, pid, cid):
        """Updates existing product."""

        if (not pname) or (not pu):
            return False
        if not self.model.update_product(pname.strip(), pu, pi, pid, cid):
            self.view.show_error_dialog( \
                _('Updating product error'), \
                _('Unable to rename product.\nProduct already in database!'))
            return False
        return True

    def update_product_in_composition(self, compid, pid, pweight):
        """Updates product properties in composition."""

        self.model.update_product_in_composition(compid, pid, pweight)

    def remove_product(self, pid):
        """Removes existing product."""

        self.model.del_product(pid)

    def remove_product_from_composition(self, compid, pid):
        """Removes existing product from existing composition."""

        self.model.del_product_from_composition(compid, pid)

    def add_composition(self, composition):
        """Adds new composition to database."""

        compname, chunks = composition
        if (not compname) or (chunks <= 0):
            return False
        if not self.model.add_composition(compname.strip(), chunks):
            self.view.show_error_dialog( \
                _('Adding composition error'), \
                _('Unable to add composition.\nComposition already in database!'))
            return False
        return True

    def update_composition(self, compid, composition):
        """Updates existing composition."""

        compname, chunks = composition
        if (not composition) or (chunks <= 0):
            return False
        if not self.model.update_composition(compid, compname.strip(), chunks):
            self.view.show_error_dialog( \
                _('Updating composition error'), \
                _('Unable to rename composition.\nComposition already in database!'))
            return False
        return True

    def remove_composition(self, compid):
        """Removes existing composition."""

        self.model.del_composition(compid)

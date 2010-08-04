"""
Diabetto controller class
"""


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

    def add_category(self, cname):
        """Adds new category to database."""

        self.model.add_category(cname)

    def update_category(self, cname, cid):
        """Updates existing category."""

        self.model.update_category(cname, cid)

    def remove_category(self, cid):
        """Removes category except 'default' category."""

        if cid != 1:
            self.model.del_category(cid)

    def add_product(self, pname, pu, pi, cid):
        """Adds new product to database."""

        if (not pu) or (not pi) or (not cid):
            return
        self.model.add_product(pname, pu, pi, cid)

    def update_product(self, pname, pu, pi, pid, cid):
        """Updates existing product."""

        self.model.update_product(pname, pu, pi, pid, cid)

    def remove_product(self, pid):
        """Removes product."""

        self.model.del_product(pid)

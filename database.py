#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3

DATABASE_NAME = 'products.db'

SCHEMA = """
    begin;

    create table products(
        pid integer primary key,
        pname text,
        pu real,
        pi real,
        cid integer
    );
    create index i_products on products (pid);

    create table categories(
        cid integer primary key,
        cname text
    );
    create index i_categories on categories (cid);
    insert into categories values(NULL, 'default');

    create table compositions(
        compid integer primary key,
        compname text,
        chunks integer
    );
    create index i_compositions on compositions (compid);

    create table composition_content(
        compid integer,
        pid integer,
        pweight integer
    );
    create index i_composition_content on composition_content (compid);

    commit;
"""


class Database:
    def __init__(self, basedir):
        if basedir.endswith(DATABASE_NAME):
            self._path = basedir
        else:
            self._path = os.path.join(basedir, DATABASE_NAME)
        self.conn = None
        self.connect()

    def connect(self):
        """Connects to database."""

        new_database = not os.path.exists(self._path)
        self.conn = sqlite3.connect(self._path)
        if new_database:
            self.conn.executescript(SCHEMA)
        self.save()

    def close(self):
        """Closes connection with database."""

        self.save()
        self.conn.close()

    def save(self):
        """Save all changes."""

        self.conn.commit()

    def add_product(self, pname, pu, pi, cid):
        """Adds new product to database."""

        if self.conn.execute("""SELECT pname FROM products WHERE \
            pname LIKE '%s'""" % pname.lower()).fetchone() is None:
            self.conn.execute("""INSERT INTO products values(NULL,?,?,?,?)""", \
                (pname.lower(), pu, pi, cid))
            self.save()
            return True
        return False

    def add_product_to_composition(self, compid, pid, pweight):
        """Adds product to existing composition."""

        execute = self.conn.execute
        if execute("""SELECT pid FROM composition_content WHERE compid=? AND \
            pid=?""", (compid, pid)).fetchone() is None:
            execute("""INSERT INTO composition_content values(?,?,?)""", \
                (compid, pid, pweight))
            self.save()
            return True
        return False

    def update_product(self, pname, pu, pi, pid, cid):
        """Updates existing product."""

        self.conn.execute("""UPDATE products SET pname=?, pu=?, pi=?, cid=? \
            WHERE pid=?""", (pname, pu, pi, cid, pid))
        self.save()
        return True

    def update_product_in_composition(self, compid, pid, pweight):
        """Updates product properties in composition."""

        self.conn.execute("""UPDATE composition_content SET pweight=? WHERE \
            compid=? AND pid=?""", (pweight, compid, pid))
        self.save()

    def del_product(self, pid):
        """Remove product from database."""

        execute = self.conn.execute
        execute("""DELETE FROM products WHERE pid=?""", (pid,))
        execute("""DELETE FROM composition_content WHERE pid=?""", (pid,))
        self.save()

    def del_product_from_composition(self, compid, pid):
        """Removes existing product from existing composition."""

        self.conn.execute("""DELETE FROM composition_content WHERE compid=? \
            AND pid=?""", (compid, pid))
        self.save()

    def add_category(self, cname):
        """Adds new category."""

        execute = self.conn.execute
        if execute("""SELECT cname FROM categories WHERE \
            cname LIKE '%s'""" % cname.lower()).fetchone() is None:
            execute("""INSERT INTO categories values(NULL, ?)""", \
                (cname.lower(),))
            self.save()
            return True
        return False

    def update_category(self, cname, cid):
        """Updates existing category."""

        execute = self.conn.execute
        if execute("""SELECT cname FROM categories WHERE \
            cname LIKE '%s'""" % cname.lower()).fetchone() is None:
            execute("""UPDATE categories SET cname=? WHERE cid=?""", \
                (cname.lower(), cid))
            self.save()
            return True
        return False

    def del_category(self, cid, del_products=True):
        """Remove category from database."""

        execute = self.conn.execute
        execute("""DELETE FROM categories WHERE cid=?""", (cid,))
        if del_products:
            execute("""DELETE FROM products WHERE cid=?""", (cid,))
        else:
            execute("""UPDATE products SET cid=1 WHERE cid=?""", (cid,))
        self.save()

    def add_composition(self, compname, chunks):
        """Adds new composition."""

        execute = self.conn.execute
        if execute("""SELECT compname FROM compositions WHERE \
            compname LIKE '%s'""" % compname.lower()).fetchone() is None:
            execute("""INSERT INTO compositions values(NULL, ?, ?)""", \
                (compname.lower(), chunks))
            self.save()
            return True
        return False

    def update_composition(self, compid, compname, chunks):
        """Updates exisiting composition."""

        self.conn.execute("""UPDATE compositions SET compname=?, chunks=? \
            WHERE compid=?""", (compname, chunks, compid))
        self.save()
        return True

    def del_composition(self, compid):
        """Removes composition and its content from database."""

        execute = self.conn.execute
        execute("""DELETE FROM compositions WHERE compid=?""", (compid,))
        execute("""DELETE FROM composition_content WHERE compid=?""", (compid,))
        self.save()

    def get_products(self, cid):
        """Gets all products."""

        if cid is None:
            return self.conn.execute("""SELECT pname, pu, pi, cid, pid FROM \
                products""").fetchall()
        else:
            return self.conn.execute("""SELECT pname, pu, pi, cid, pid FROM \
                products WHERE cid=?""", (cid,)).fetchall()

    def get_compositions(self):
        """Gets all compositions."""

        return self.conn.execute("""SELECT compname, compid, chunks FROM \
            compositions""").fetchall()

    def get_composition_content(self, compid):
        """Gets all composition products."""

        return self.conn.execute("""SELECT pid, pweight FROM \
            composition_content WHERE compid=?""", (compid,)).fetchall()

    def get_categories(self):
        """Gets all categories."""

        return self.conn.execute( \
            """SELECT cname, cid FROM categories""").fetchall()

    def get_category_by_id(self, cid):
        """Gets category by it id."""

        return self.conn.execute("""SELECT cname, cid FROM categories \
            WHERE cid=?""", (cid,)).fetchone()

    def get_product_by_id(self, pid):
        """Gets product details by it id."""

        return self.conn.execute("""SELECT pname, pu, pi FROM products \
            WHERE pid=?""", (pid,)).fetchone()

    def get_products_by_category(self, cid):
        """Gets all products for selected category."""

        return self.conn.execute("""SELECT pname, pid FROM products WHERE \
            cid=?""", (cid,)).fetchall()

    def get_product_category(self, pid):
        """Gets product category for selected product."""

        return self.conn.execute("""SELECT cid FROM products WHERE pid=?""", \
            (pid,)).fetchone()[0]


if __name__ == "__main__":
    db = Database('/tmp')
    # put test code here
    #db.add_category('test'.decode('utf-8'))
    #db.add_product('Product1'.decode('utf-8'),1,2,2)
    #db.add_product('Product2'.decode('utf-8'),1,2,2)
    #db.add_product('Product3'.decode('utf-8'),1,2,3)
    #db.del_category(2, False)
    db.close()

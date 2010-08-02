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
        pu integer,
        pi integer,
        cid integer
    );
    create index i_products on products (pid);

    create table categories(
        cid integer primary key,
        cname text
    );
    create index i_categories on categories (cid);
    insert into categories values(NULL, 'default');
    commit;
"""


class Database:
    def __init__(self, basedir):
        self._path = os.path.join(basedir, DATABASE_NAME)
        self.conn = None
        self.connect()

    def connect(self):
        """Connects to database."""

        new_database = not os.path.exists(self._path)
        self.conn = sqlite3.connect(self._path, isolation_level="EXCLUSIVE")
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

    def del_product(self, pid):
        """Remove product from database."""

        self.conn.execute("""DELETE FROM products WHERE pid=?""", (pid,))
        self.save()

    def add_category(self, cname):
        """Adds new category."""

        execute = self.conn.execute
        if execute("""SELECT cname FROM categories WHERE \
            cname LIKE '%s'""" % cname.lower()).fetchone() is None:
            execute("""INSERT INTO categories values(NULL, ?)""", \
                (cname.lower(),))
        self.save()

    def del_category(self, cid, del_products=True):
        """Remove category from database."""

        execute = self.conn.execute
        execute("""DELETE FROM categories WHERE cid=?""", (cid,))
        if del_products:
            execute("""DELETE FROM products WHERE cid=?)""", (cid,))
        else:
            execute("""UPDATE products SET cid=1 WHERE cid=?""", (cid,))
        self.save()

    def get_products(self):
        """Gets all products."""

        return self.conn.execute( \
            """SELECT pid, pname FROM products""").fetchall()

    def get_categories(self):
        """Gets all categories."""

        return self.conn.execute( \
            """SELECT cid, cname FROM categories""").fetchall()




if __name__ == "__main__":
    db = Database('/tmp')
    # put test code here
    #db.add_category('test'.decode('utf-8'))
    #db.add_product('Product1'.decode('utf-8'),1,2,2)
    #db.add_product('Product2'.decode('utf-8'),1,2,2)
    #db.add_product('Product3'.decode('utf-8'),1,2,3)
    #db.del_category(2, False)
    db.close()

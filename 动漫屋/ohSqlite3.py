import sqlite3
import os

class ohSqlite3(object):
    """ APIs for using Sqlite3.

    Attributes:
        dbpath: the db file path for manipulation
        conn: connection object returned from sqlite3.connect()
        cursor: cursor object returned from conn

        SHOW_SQL_STATEMENT: whether print sql statement, default False
    """

    SHOW_SQL_STATEMENT = False

    def __init__(self, dbpath):
        """inits ohSqlite3 with dbpath"""
        self.dbpath = dbpath
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """init db connection
        
        Raises:
            sqlite3.Error: An error occurred when attempting to connect sqlite db.
        """
        try:
            self.conn = sqlite3.connect(self.dbpath)
        except sqlite3.Error as e:
            print ("Connect {} failed. Error: {}".foramt(self.dbpath, e.args[0]))
        
        self.cursor = self.conn.cursor()

    def execute(self, sql, args = None):
        """execute sql statement

        Args:
            sql: the sql statement to be executed
            args: a tuple of fields to be added to sql, default None

        Returns:
            result of sql statement execution

        Raises:
            Exception: any errors occurred when executing sql statement

        """
        if self.SHOW_SQL_STATEMENT:
            print ("[SQL]{}".format(sql))

        data = None
        try:
            if args:
                self.cursor.execute(sql, args)
            else:
                self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception as e:
            print (e, "[SQL]:" + sql.strip())
            self.conn.rollback()

        self.conn.commit()
        if data:
            return data
        return None

    def query(self, sql, args = None):
        """Same as execute(), different names"""
        return self.execute(sql, args = None)

    def close(self):
        """close all objects"""
        self.cursor.close()
        self.conn.close()

def unitest():
    testdb = "ohSqlite3_test.db"

    # test funcs
    db = ohSqlite3(testdb)
    db.connect()

    db.execute("CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)")

    db.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    db.execute("INSERT INTO stocks VALUES ('2006-03-28', 'BUY', 'IBM', 1000, 45.00)")
    db.execute("INSERT INTO stocks VALUES ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00)")
    db.execute("INSERT INTO stocks VALUES ('2006-04-06', 'SELL', 'IBM', 500, 53.00)")

    assert 4 == db.execute("SELECT count(*) FROM stocks")[0][0]

    db.execute("DROP TABLE stocks")

    db.close()

    # test __with__ statement
    with ohSqlite3(testdb) as db:
        db.query("CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)")

        db.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        db.execute("INSERT INTO stocks VALUES ('2006-03-28', 'BUY', 'IBM', 1000, 45.00)")
        db.execute("INSERT INTO stocks VALUES ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00)")
        db.execute("INSERT INTO stocks VALUES ('2006-04-06', 'SELL', 'IBM', 500, 53.00)")

        assert 4 == db.execute("SELECT count(*) FROM stocks")[0][0]

        db.execute("DROP TABLE stocks")

    os.remove(testdb)


if __name__ == "__main__":
    unitest()

    
# Базовые действия с таблицами

from dbconnection import *

class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return sorted(self.columns().keys(), key = lambda x: x)

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

# метод выполнения запросов с защитой от sql-инъекций
    def execute(self, sql, params=None):
        try:
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, params)
            self.dbconn.conn.commit()
            return cur
        except psycopg2.Error:
            self.dbconn.conn.rollback()
            raise

    def create(self):
        # SQL строится из имён колонок, заданных в коде (не от пользователя),
        # поэтому конкатенация здесь безопасна
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in sorted(self.columns().items(), key=lambda x: x[0])]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        self.execute(sql)
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        self.execute(sql)
        return

    def insert_one(self, vals):
        cols = self.column_names_without_id()
        sql = "INSERT INTO " + self.table_name() + "(" + ", ".join(cols) + ")"
        sql += " VALUES(" + ", ".join(["%s"] * len(cols)) + ")"
        self.execute(sql, list(vals))
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY " + ", ".join(self.primary_key())
        return self.execute(sql).fetchone()

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY " + ", ".join([x + " DESC" for x in self.primary_key()])
        return self.execute(sql).fetchone()
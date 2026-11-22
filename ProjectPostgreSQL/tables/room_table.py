# таблица "Помещения" 
from dbtable import *


class RoomTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "room"

    def columns(self):
        return {
            "id": ["integer", "PRIMARY KEY", "DEFAULT nextval('" + self.dbconn.prefix + "room_seq')"],
            "name": ["varchar(100)", "NOT NULL", "CHECK(char_length(name) > 0)"],
            "useful_volume": ["numeric(10,2)", "NOT NULL", "CHECK(useful_volume > 0)"],
            "min_temp": ["numeric(5,1)", "NOT NULL"],
            "max_temp": ["numeric(5,1)", "NOT NULL", "CHECK(max_temp >= min_temp)"],
            "min_humidity": ["numeric(5,1)", "NOT NULL", "CHECK(min_humidity >= 0)"],
            "max_humidity": ["numeric(5,1)", "NOT NULL", "CHECK(max_humidity <= 100 AND max_humidity >= min_humidity)"],
        }

    def table_constraints(self):
        return ["UNIQUE(name)"]

    def create(self):
        self.execute("CREATE SEQUENCE IF NOT EXISTS " + self.dbconn.prefix + "room_seq")
        super().create()

    def drop(self):
        super().drop()
        self.execute("DROP SEQUENCE IF EXISTS " + self.dbconn.prefix + "room_seq")

    def insert_one(self, vals):
        # vals: [name, useful_volume, min_temp, max_temp, min_humidity, max_humidity]
        sql = "INSERT INTO " + self.table_name()
        sql += " (name, useful_volume, min_temp, max_temp, min_humidity, max_humidity)"
        sql += " VALUES (%s, %s, %s, %s, %s, %s)"
        self.execute(sql, list(vals))

    def all(self):
        sql = "SELECT id, name, useful_volume, min_temp, max_temp, min_humidity, max_humidity FROM "
        sql += self.table_name() + " ORDER BY name"
        return self.execute(sql).fetchall()

    def find_one(self, name):
        sql = "SELECT id FROM " + self.table_name() + " WHERE name = %s"
        return self.execute(sql, (name,)).fetchone()

    def find_by_name(self, name):
        sql = "SELECT id, name, useful_volume, min_temp, max_temp, min_humidity, max_humidity FROM "
        sql += self.table_name() + " WHERE name = %s"
        return self.execute(sql, (name,)).fetchone()

    def update_one(self, room_id, vals):
        # vals: [name, useful_volume, min_temp, max_temp, min_humidity, max_humidity]
        sql = "UPDATE " + self.table_name()
        sql += " SET name = %s, useful_volume = %s, min_temp = %s, max_temp = %s,"
        sql += " min_humidity = %s, max_humidity = %s WHERE id = %s"
        self.execute(sql, list(vals) + [room_id])

    def delete_one(self, val):
        sql = "DELETE FROM " + self.table_name() + " WHERE id = %s"
        self.execute(sql, (val,))
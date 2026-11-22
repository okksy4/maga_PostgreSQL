# Таблица "Стеллажи" 
from dbtable import *

class RackTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "rack"

    def columns(self):
        return {
            "id": ["integer", "PRIMARY KEY", "DEFAULT nextval('" + self.dbconn.prefix + "rack_seq')"],
            "room_id": ["integer", "NOT NULL"],
            "rack_number": ["integer", "NOT NULL", "CHECK(rack_number > 0)"],
            "places": ["integer", "NOT NULL", "CHECK(places > 0)"],
            "place_height": ["numeric(6,2)", "NOT NULL", "CHECK(place_height > 0)"],
            "place_width": ["numeric(6,2)", "NOT NULL", "CHECK(place_width > 0)"],
            "place_length": ["numeric(6,2)", "NOT NULL", "CHECK(place_length > 0)"],
            "max_load": ["numeric(10,2)", "NOT NULL", "CHECK(max_load > 0)"],
        }

    def table_constraints(self):
        return [
            "FOREIGN KEY(room_id) REFERENCES " + self.dbconn.prefix + "room(id)",
            "UNIQUE(room_id, rack_number)",
        ]

    def create(self):
        self.execute("CREATE SEQUENCE IF NOT EXISTS " + self.dbconn.prefix + "rack_seq")
        super().create()

    def drop(self):
        self.execute("DROP TABLE IF EXISTS " + self.table_name() + " CASCADE")
        self.execute("DROP SEQUENCE IF EXISTS " + self.dbconn.prefix + "rack_seq")

    def insert_one(self, vals):
        # vals: [room_id, rack_number, places, place_height, place_width, place_length, max_load]
        sql = "INSERT INTO " + self.table_name()
        sql += " (room_id, rack_number, places, place_height, place_width, place_length, max_load)"
        sql += " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.execute(sql, list(vals))

    def all_by_room(self, room_id):
        sql = "SELECT id, rack_number, places, place_height, place_width, place_length, max_load FROM "
        sql += self.table_name() + " WHERE room_id = %s ORDER BY rack_number"
        return self.execute(sql, (room_id,)).fetchall()

    def count_by_room(self, room_id):
        sql = "SELECT COUNT(*) FROM " + self.table_name() + " WHERE room_id = %s"
        return self.execute(sql, (room_id,)).fetchone()[0]

    def find_one(self, room_id, rack_number):
        sql = "SELECT id FROM " + self.table_name() + " WHERE room_id = %s AND rack_number = %s"
        return self.execute(sql, (room_id, rack_number)).fetchone()

    def delete_one(self, val):
        sql = "DELETE FROM " + self.table_name() + " WHERE id = %s"
        self.execute(sql, (val,))
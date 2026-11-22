# Абрамова Оксана Васильевна
# Группа М26-555
# Вариант 3
# Таблицы помещения и стеллажи без связей с другими таблицами.

import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from room_table import *
from rack_table import *
import psycopg2


# хелперы
def read_int_add(prompt, lo, hi):
    while True:
        s = input(prompt).strip()
        if s.lower() == "отмена":
            return None
        if len(s) == 0:
            print("Пустой ввод! Введите число или 'отмена'.")
            continue
        try:
            n = int(s)
        except ValueError:
            print("Введите целое число или 'отмена'!")
            continue
        if n < lo or n > hi:
            print("Число должно быть от " + str(lo) + " до " + str(hi) + "!")
            continue
        return n

def read_int_row(prompt, hi):
    while True:
        s = input(prompt).strip()
        try:
            n = int(s)
        except ValueError:
            print("Введите целое число!")
            continue
        if n < 0 or n > hi:
            print("Число должно быть от 0 до " + str(hi) + "!")
            continue
        return n

def read_float_add(prompt, lo, hi):
    while True:
        s = input(prompt).strip().replace(",", ".")
        if s.lower() == "отмена":
            return None
        if len(s) == 0:
            print("Пустой ввод! Введите число или 'отмена'.")
            continue
        try:
            n = float(s)
        except ValueError:
            print("Введите число или 'отмена'!")
            continue
        if n < lo or n > hi:
            print("Число должно быть от " + str(lo) + " до " + str(hi) + "!")
            continue
        return n

def read_float_or_cancel(prompt, lo, hi, default):
    while True:
        s = input(prompt).strip().replace(",", ".")
        if s.lower() == "отмена":
            return None
        if len(s) == 0:
            return default
        try:
            n = float(s)
        except ValueError:
            print("Введите число, Enter - оставить текущее, 'отмена' - выйти без изменений!")
            continue
        if n < lo or n > hi:
            print("Число должно быть от " + str(lo) + " до " + str(hi) + "!")
        else:
            return n

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        self.room_id = -1
        self.room_obj = None
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        rt = RoomTable()
        rkt = RackTable()
        rt.create()
        rkt.create()
        return

    def db_insert_somethings(self):
        rt = RoomTable()
        kt = RackTable()
        rt.insert_one(["Склад 1", 1000.00, 0.0, 30.0, 50.0, 75.0])
        rt.insert_one(["Склад 2", 500.00, -18.0, 5.0, 60.0, 95.0])
        rt.insert_one(["Склад 3", 1500.00, 2.0, 5.0, 60.0, 95.0])
        rt.insert_one(["Склад 4", 750.00, -10.0, 40.0, 50.0, 98.0])
        rt.insert_one(["Склад 5", 1500.00, 10.0, 30.0, 55.0, 70.0])
        rt.insert_one(["Склад 6", 1000.00, -18.0, 5.0, 50.0, 75.0])
        rt.insert_one(["Склад 7", 110.00, -30.0, -18.0, 75.0, 98.0])
        r = []
        for i in range(1, 8):
            r.append(rt.find_by_name("Склад " + str(i)))
        kt.insert_one([r[0][0], 1, 20, 1.80, 1.00, 1.20, 350.00])
        kt.insert_one([r[0][0], 2, 20, 1.80, 1.00, 1.20, 350.00])
        kt.insert_one([r[1][0], 1, 45, 2.00, 0.80, 1.00, 200.00])
        kt.insert_one([r[2][0], 1, 12, 1.50, 1.20, 1.50, 500.00])
        kt.insert_one([r[3][0], 1, 24, 1.60, 0.90, 1.10, 300.00])
        kt.insert_one([r[4][0], 1, 18, 1.20, 0.60, 0.80, 150.00])
        kt.insert_one([r[5][0], 1, 40, 1.90, 0.70, 1.00, 250.00])
        return

    def db_drop(self):
        rkt = RackTable()
        rt = RoomTable()
        rkt.drop()
        rt.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр помещений;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_rooms(self):
        self.room_id = -1
        print("Просмотр списка помещений:")
        print("№\tНазвание\tОбъём (м3)\tТемпература\tВлажность")
        lst = RoomTable().all()
        for i, r in enumerate(lst):
            print(str(i + 1) + "\t" + str(r[1]) + "\t" + str(r[2])
                  + "\t" + str(r[3]) + ".." + str(r[4])
                  + "\t" + str(r[5]) + ".." + str(r[6]) + "%")
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового помещения;
    4 - изменение помещения;
    5 - удаление помещения;
    6 - просмотр стеллажей помещения;
    9 - выход."""
        print(menu)
        return

    def after_show_rooms(self, next_step):
        while True:
            if next_step == "3":
                self.show_add_room()
                return "1"
            elif next_step == "4":
                self.show_edit_room()
                return "1"
            elif next_step == "5":
                self.show_delete_room()
                return "1"
            elif next_step == "6":
                next_step = self.show_racks_by_room()
                while next_step not in ("0", "1", "9"):
                    if next_step == "6":
                        self.show_add_rack()
                    elif next_step == "7":
                        self.show_delete_rack()
                    else:
                        print("Выбрано неверное число! Повторите ввод!")
                    next_step = self.show_racks_by_room()
                return next_step
            elif next_step != "0" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_room(self):
        name = input("Введите название помещения ('отмена' - выйти): ").strip()
        if name.lower() == "отмена":
            return
        while len(name) == 0:
            name = input("Название не может быть пустым! Введите название заново ('отмена' - выйти):").strip()
            if name.lower() == "отмена":
                return
        if RoomTable().find_one(name):
            print("Помещение с таким названием уже существует!")
            return
        volume = read_float_add("Введите полезный объём (м3): ", 1, 1000000)
        if volume is None:
            return
        tmin = read_float_add("Введите минимальную температуру: ", -100, 100)
        if tmin is None:
            return
        tmax = read_float_add("Введите максимальную температуру: ", -100, 100)
        while tmax is not None and tmax < tmin:
            print("Максимальная температура должна быть не меньше минимальной!")
            tmax = read_float_add("Введите максимальную температуру заново ('отмена' - выйти): ", -100, 100)
        if tmax is None:
            return
        hmin = read_float_add("Введите минимальную влажность (%): ", 0, 100)
        if hmin is None:
            return
        hmax = read_float_add("Введите максимальную влажность (%): ", 0, 100)
        while hmax is not None and hmax < hmin:
            print("Максимальная влажность должна быть не меньше минимальной!")
            hmax = read_float_add("Введите максимальную влажность заново ('отмена' - выйти): ", 0, 100)
        if hmax is None:
            return
        try:
            RoomTable().insert_one([name, volume, tmin, tmax, hmin, hmax])
            print("Помещение добавлено!")
        except psycopg2.errors.UniqueViolation:
            print("Помещение с таким названием уже существует!")
        except psycopg2.DataError:
            print("Значение не соответствует формату или диапазону поля!")
        except psycopg2.Error as e:
            print("Ошибка базы данных при выполнении операции:", e)
        return

    def show_delete_room(self):
        lst = RoomTable().all()
        if len(lst) == 0:
            print("Нет ни одного помещения!")
            return
        num = read_int_row("Укажите номер строки, в которой записано помещение (0 - отмена): ", len(lst))
        if num == 0:
            return
        room = lst[num - 1]
        cnt = RackTable().count_by_room(room[0])
        if cnt > 0:
            print("В помещении есть стеллажи (" + str(cnt) + " шт.)! Сначала удалите их.")
            return
        answer = input("Удалить помещение '" + str(room[1]) + "'? (да/нет): ").strip().lower()
        while answer != "да" and answer != "нет":
            answer = input("Введите 'да' или 'нет': ").strip().lower()
        if answer == "да":
            try:
                RoomTable().delete_one(room[0])
                print("Помещение удалено!")
            except psycopg2.errors.ForeignKeyViolation:
                print("Нельзя удалить помещение: с ним связаны другие записи!")
            except psycopg2.Error as e:
                print("Ошибка базы данных при выполнении операции:", e)
        return

    def show_edit_room(self):
        lst = RoomTable().all()
        if len(lst) == 0:
            print("Нет ни одного помещения!")
            return
        num = read_int_row("Укажите номер строки, в которой записано помещение (0 - отмена): ", len(lst))
        if num == 0:
            return
        room = lst[num - 1]
        print("Текущие значения: название '" + str(room[1])
              + "', объём " + str(room[2]) + " м3"
              + ", температура " + str(room[3]) + ".." + str(room[4])
              + ", влажность " + str(room[5]) + ".." + str(room[6]) + "%")
        print("Пустой ввод - оставить текущее значение. 'отмена' в любом поле - выйти без изменений.")
        name = input("Введите новое название: ").strip()
        if name.lower() == "отмена":
            return
        if len(name) == 0:
            name = str(room[1])
        elif name != str(room[1]) and RoomTable().find_one(name):
            print("Помещение с таким названием уже существует!")
            return
        volume = read_float_or_cancel("Введите полезный объём (м3): ", 1, 1000000, float(room[2]))
        if volume is None:
            return
        tmin = read_float_or_cancel("Введите минимальную температуру: ", -100, 100, float(room[3]))
        if tmin is None:
            return
        tmax = read_float_or_cancel("Введите максимальную температуру: ", -100, 100, float(room[4]))
        while tmax is not None and tmax < tmin:
            print("Максимальная температура должна быть не меньше минимальной!")
            tmax = read_float_or_cancel("Введите максимальную температуру заново ('отмена' - выйти): ", -100, 100, float(room[4]))
        if tmax is None:
            return
        hmin = read_float_or_cancel("Введите минимальную влажность (%): ", 0, 100, float(room[5]))
        if hmin is None:
            return
        hmax = read_float_or_cancel("Введите максимальную влажность (%): ", 0, 100, float(room[6]))
        while hmax is not None and hmax < hmin:
            print("Максимальная влажность должна быть не меньше минимальной!")
            hmax = read_float_or_cancel("Введите максимальную влажность заново ('отмена' - выйти): ", 0, 100, float(room[6]))
        if hmax is None:
            return
        try:
            RoomTable().update_one(room[0], [name, volume, tmin, tmax, hmin, hmax])
            print("Помещение изменено!")
        except psycopg2.DataError:
            print("Значение не соответствует формату или диапазону поля!")
        except psycopg2.errors.UniqueViolation:
            print("Помещение с таким названием уже существует!")
        return

    def show_racks_by_room(self):
        if self.room_id == -1:
            while True:
                lst = RoomTable().all()
                if len(lst) == 0:
                    print("Нет ни одного помещения!")
                    return "1"
                num = input("Укажите номер строки, в которой записано интересующее Вас помещение (0 - отмена):").strip()
                while len(num) == 0:
                    num = input("Пустая строка. Повторите ввод! Укажите номер строки помещения (0 - отмена):").strip()
                if num == "0":
                    return "1"
                try:
                    num = int(num)
                except ValueError:
                    print("Введите целое число!")
                    continue
                if num < 1 or num > len(lst):
                    print("Введено число, неудовлетворяющее количеству помещений!")
                    continue
                self.room_id = lst[num - 1][0]
                self.room_obj = lst[num - 1]
                break
        print("Выбрано помещение: " + str(self.room_obj[1]))
        print("Стеллажи:")
        print("№\tНомер стеллажа\tМест\tРазмер места (ВxШxД, м)\tМакс. нагрузка (кг)")
        lst = RackTable().all_by_room(self.room_id)
        if len(lst) == 0:
            print("В этом помещении нет стеллажей!")
        for i, r in enumerate(lst):
            size = str(r[3]) + "x" + str(r[4]) + "x" + str(r[5])
            print(str(i + 1) + "\t" + str(r[1]) + "\t" + str(r[2]) + "\t" + size + "\t" + str(r[6]))
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр помещений;
    6 - добавление нового стеллажа;
    7 - удаление стеллажа;
    9 - выход."""
        print(menu)
        return self.read_next_step()

    def show_add_rack(self):
        number = read_int_add("Введите номер стеллажа (1 - 1000, 'отмена' - выйти): ", 1, 1000)
        if number is None:
            return
        if RackTable().find_one(self.room_id, number):
            print("Стеллаж с таким номером уже есть в этом помещении!")
            return
        places = read_int_add("Введите количество мест на стеллаже: ", 1, 100000)
        if places is None:
            return
        h = read_float_add("Введите высоту одного места (м): ", 0.01, 9999.99)
        if h is None:
            return
        w = read_float_add("Введите ширину одного места (м): ", 0.01, 9999.99)
        if w is None:
            return
        l = read_float_add("Введите длину одного места (м): ", 0.01, 9999.99)
        if l is None:
            return
        load = read_float_add("Введите максимальную нагрузку (кг): ", 0.01, 99999999.99)
        if load is None:
            return
        try:
            RackTable().insert_one([self.room_id, number, places, h, w, l, load])
            print("Стеллаж добавлен!")
        except psycopg2.errors.UniqueViolation:
            print("Стеллаж с таким номером уже есть в этом помещении!")
        except psycopg2.DataError:
            print("Значение не соответствует формату или диапазону поля!")
        except psycopg2.Error as e:
            print("Ошибка базы данных при выполнении операции:", e)
        return

    def show_delete_rack(self):
        lst = RackTable().all_by_room(self.room_id)
        if len(lst) == 0:
            print("В этом помещении нет стеллажей!")
            return
        num = read_int_row("Укажите номер строки, в которой записан стеллаж (0 - отмена): ", len(lst))
        if num == 0:
            return
        rack = lst[num - 1]
        answer = input("Удалить стеллаж №" + str(rack[1]) + "? (да/нет): ").strip().lower()
        while answer != "да" and answer != "нет":
            answer = input("Введите 'да' или 'нет': ").strip().lower()
        if answer == "да":
            try:
                RackTable().delete_one(rack[0])
                print("Стеллаж удалён!")
            except psycopg2.Error as e:
                print("Ошибка базы данных при выполнении операции:", e)
        return

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_rooms()
                next_step = self.read_next_step()
                current_menu = self.after_show_rooms(next_step)
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

if __name__ == "__main__":
    m = Main()
    # Откоментируйте эту строку и закоментируйте следующую для теста
    # соединения с БД
    # m.test()
    m.main_cycle()

import sqlite3
import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
from tkcalendar import DateEntry
import os

with sqlite3.connect("БД.db") as db:
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS SELLER(
                                seller  varchar (50) PRIMARY KEY);''')
    cursor.execute('''DELETE FROM SELLER;''')
    cursor.execute(
        '''INSERT INTO SELLER (seller) VALUES ('Обувь от А до Я'), ('Шаги Удачи'), ('Обувной Уголок'), ('Стильная Подошва'), ('Кроссовки и Туфли'), ('Обувь для Каждого'), ('Комфортный Шаг'), ('Трендовая Обувь'), (' Мир Обуви'), ('Элегантные Шаги'); ''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS shoes(
                        id integer primary key autoincrement,
                        seller integer not null,
                        brand varchar(50) ,
                        model varchar(50) not null,
                        count integer(10) not null,
                        price decimal(16,2) not null,
                        total_price decimal(16,2),
                        date date,
                        foreign key (seller) references SELLER(seller));''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS POSITIONS(
                                    positions  varchar (50) PRIMARY KEY);''')
    cursor.execute('''DELETE FROM positions;''')

    cursor.execute('''INSERT INTO POSITIONS (positions) VALUES ('Менеджер магазина'), ('Продавец-консультант'),
     ('Складской работник'), ('Визуальный мерчендайзер'), ('Специалист по работе с клиентами'), ('Маркетолог'),
      ('Финансовый менеджер'), ('Кассир'), (' Товаровед'), ('Специалист по интернет-продажам'); ''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        id_users integer primary key autoincrement,
                        name TEXT,
                        surname text,
                        patronymic text,
                        birthday text,
                        passport_seria text,
                        passport_nomber text,
                        positions varchar(50),
                        login TEXT UNIQUE,
                        password TEXT,
                        foreign key (positions) references POSITIONS(positions))''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id_order integer primary key autoincrement,
                        id_user integer,
                        id_shoes integer,
                        foreign key (id_user) references users (id_users),
                        foreign key (id_shoes) references shoes (id));''')

# ФУНКЦИИ С БД
def get_sellers_from_db():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT seller FROM SELLER;")
        return [row[0] for row in cursor.fetchall()]

def get_position_from_POSITIONS():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT positions FROM POSITIONS;")
        return [row[0] for row in cursor.fetchall()]

def add_data_to_db(seller, brand, model, count, price, date):
    total_price = float(price) * int(count)
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO shoes (seller, brand, model, count, price, total_price, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (seller, brand, model, count, price, total_price, date))
        db.commit()

def get_name_from_name(login, password):
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id_users FROM users WHERE login = ? AND password = ?", (login, password))
        result = cursor.fetchone()
        return result[0] if result else None

def add_name_in_orders(id_shoes):
    with sqlite3.connect("БД.db") as db:
        name = get_name_from_name(login, password)
        boot = id_shoes
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO orders (id_user, id_shoes) VALUES (?, ?)", (name, boot))
        db.commit()

def get_info_from_irders():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT USERS.id_users,  USERS.name, USERS.surname, SHOES.brand, SHOES.model, SHOES.count from USERS join ORDERS on ORDERS.id_user = USERS.id_users JOIN SHOES on SHOES.id = ORDERS.id_shoes;")
        return cursor.fetchall()
def display_orders(table):
    data = get_info_from_irders()
    for item in table.get_children():
        table.delete(item)
    for row in data:
        table.insert("", "end", values=row)
    table.tag_configure('t1', font=('Monaco', 30))

def get_data_from_db():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM shoes")
        return cursor.fetchall()

def det_all_from_users():
    with sqlite3.connect("БД.db")as db:
        cursor = db.cursor()
        cursor.execute("select * from users")
        return cursor.fetchall()

def display_data(table):
    data = get_data_from_db()
    for item in table.get_children():
        table.delete(item)
    for row in data:
        tree.insert("", "end", values=row)
    tree.tag_configure('t1', font=('Monaco', 10))

def get_most_popular_brend():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT brand FROM shoes GROUP BY brand ORDER BY COUNT(brand) DESC")
        result = cursor.fetchone()
        return result[0] if result else "Нет данных"

def get_most_popular_model():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT model
            FROM SHOES
            ORDER BY price DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        return result[0]
def get_most_rich_price():
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT MAX(count), brand, model FROM shoes GROUP BY brand, model ORDER BY MAX(count) DESC")
        result = cursor.fetchone()
        return f"{result[1]} - {result[2]} цена: {result[0]}" if result else "Нет данных"
def find_all_in_users(login):
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        for res in result:
            if (login == res[8]):
                return True

def add_users_to_db(name, surname, patronymic, birthday, passport_seria, passport_nomber, positions, login, password):
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, surname, patronymic, birthday, passport_seria, passport_nomber, positions, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, surname, patronymic, birthday, passport_seria, passport_nomber, positions,  login, password))
        db.commit()
def login_find_all_in_users(login, password):
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        for res in result:
            if (login == res[8] and password == res[9]):
                return True
def export_tovar_to_excel():
    data = get_data_from_db()
    df = pd.DataFrame(data, columns=["ID", "Seller", "brand", "Model", "Count", "Price", "Total Price", "Date"])
    df.to_excel("shoes_data.xlsx", index=False)
    os.startfile("shoes_data.xlsx")
def export_user_to_excel():
    user = det_all_from_users()
    df = pd.DataFrame(user, columns=["ID", "Имя", "Фамилия", "Отчество", "День рождения", "Серия пасспорта", "Номер пасспорта", "Должность", "Логин", "Пароль"])
    df.to_excel("user_data.xlsx", index=False)
    os.startfile("user_data.xlsx")
def export_history_to_excel():
    hisrory = get_info_from_irders()
    df = pd.DataFrame(hisrory, columns=["ID", "Имя", "Фамилия", "Бренд", "модель", "Цена"])
    df.to_excel("history_data.xlsx", index=False)
    os.startfile("history_data.xlsx")


# Функция внутри окна
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def left_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 5) - (width / 5)
    y = (screen_height / 5) - (height / 5)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def full_screen(window):
    x = window.winfo_screenwidth()
    y = window.winfo_screenheight()
    window.geometry(f'{x}x{y}')

def update_shoes_count_in_db(brand, model):
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        # Уменьшаем количество на 1 для выбранного товара
        cursor.execute("UPDATE shoes SET price = price - 1 WHERE brand = ? AND model = ?", (brand, model))
        # Проверяем, стало ли количество равным 0
        cursor.execute("SELECT count FROM shoes WHERE brand = ? AND model = ?", (brand, model))
        result = cursor.fetchone()
        if result and result[0] <= 0:
            # Удаляем товар из базы данных, если количество равно 0
            cursor.execute("DELETE FROM shoes WHERE brand = ? AND model = ?", (brand, model))
        db.commit()

def get_shoes_id_by_brand_and_model(brand, model):
    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM shoes WHERE brand = ? AND model = ?", (brand, model))
        result = cursor.fetchone()
        return result[0] if result else None
def clear_orders(table):
    global selected_items
    global login, password

    user_id = get_name_from_name(login, password)
    if not user_id:
        messagebox.showerror("Ошибка", "Пользователь не найден!")
        return

    with sqlite3.connect("БД.db") as db:
        cursor = db.cursor()
        for item in selected_items:
            brand, model, _ = item

            cursor.execute("SELECT  price, count FROM shoes WHERE brand = ? AND model = ?", (brand, model))
            result = cursor.fetchone()
            if not result:
                continue

            current_count, current_price = result


            new_count = current_count - 1

            if new_count <= 0:
                cursor.execute("DELETE FROM shoes WHERE brand = ? AND model = ?", (brand, model))
            else:
                new_total_price = new_count * current_price

                cursor.execute("UPDATE shoes SET price = ?, total_price = ? WHERE brand = ? AND model = ?",
                               (new_count, new_total_price, brand, model))

            cursor.execute("SELECT id FROM shoes WHERE brand = ? AND model = ?", (brand, model))
            shoes_id = cursor.fetchone()
            if shoes_id:
                cursor.execute("INSERT INTO orders (id_user, id_shoes) VALUES (?, ?)", (user_id, shoes_id[0]))

        db.commit()

    selected_items = []
    for item in table.get_children():
        table.delete(item)

    display_data(tree)

    messagebox.showinfo("INFO", "СПАСИБО ЗА ПОКУПКУ")
def clear_roe_in_orders(table):
    global selected_items
    selected_item = table.selection()  # Получаем выбранный элемент
    if selected_item:
        item_values = table.item(selected_item, "values")  # Получаем значения строки
        if item_values in selected_items:
            selected_items.remove(item_values)  # Удаляем элемент из списка
        table.delete(selected_item)  # Удаляем строку из таблицы

global selected_items
selected_items = []

#ОКНА
def open_registration(names):
    names.withdraw()
    page_registration = tk.Toplevel()  # Создаем новое окно регистрации
    full_screen(page_registration)
    page_registration.title('Регистрация')

    def go_menu():
        page_registration.destroy()  # Закрываем окно регистрации
        names.deiconify()

    def main():
        name = registration_name_enptry.get()
        surname = registration_surname_enptry.get()
        patronymic = registration_patronymic_enptry.get()
        birthday = registration_birthday_enptry.get()
        passport_seria = registration_passport_seria_enptry.get()
        passport_nomber = registration_passport_nomber_enptry.get()
        possition = registration_possition_enptry.get()
        login = registration_login_enptry.get()
        password = registration_password_entry.get()
        redictration = [name, surname, birthday, passport_seria, passport_nomber, possition, login, password]
        redictration1 = ['Имя', 'Фамилия', 'Дата рождения', 'Серия пасспорта', 'Номер пасспорта', "Должность", 'Логин', "Пароль"]
        if (len(name) != 0 and len(surname) != 0 and len(birthday) != 0 and len(passport_seria) != 0 and len(passport_nomber) != 0 and len(possition) != 0 and len(login) != 0 and len(password) != 0):
            repeat = find_all_in_users(login)
            if (repeat == True):
                messagebox.showerror('EROR', "такой логин уже существует")
            else:
                add_users_to_db(name, surname, patronymic, birthday, passport_seria, passport_nomber, possition, login, password)
                messagebox.showinfo("INFO", "Регистрация выполнена")
                page_registration.destroy()  # Закрываем окно регистрации
                names.deiconify()  # Восстанавливаем главное окно
        else:
            messagebox.showerror("ERROR", "Введены не все данные")
            for i in range(0, len(redictration)):
                if (redictration[i] == ""):
                    messagebox.showerror("ERROR", f"Введи данные в поле '{redictration1[i]}'")
                    break
    def validate(new_value):
        return new_value == "" or new_value.isnumeric()

    vcmd = (page_registration.register(validate), '%P')

    registration = ctk.CTkLabel(page_registration, text="Регистрация", text_color="BlueViolet", font=("arial", 35))
    registration.place(anchor="center", relx=0.5, rely=0.1)

    frame_gregistration = ctk.CTkFrame(page_registration, width=500, height=600, fg_color="white", border_color="BlueViolet", border_width=2)
    frame_gregistration.place(anchor="center", relx=0.5, rely=0.5)

    registration_name_label = ctk.CTkLabel(frame_gregistration, text="Имя", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_name_label.place(anchor="center", relx=0.3, rely=0.1)

    registration_name_enptry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5")
    registration_name_enptry.place(anchor="center", relx=0.7, rely=0.1)

    registration_surname_label = ctk.CTkLabel(frame_gregistration, text="Фамилия", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_surname_label.place(anchor="center", relx=0.3, rely=0.2)

    registration_surname_enptry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5")
    registration_surname_enptry.place(anchor="center", relx=0.7, rely=0.2)

    registration_patronymic_label = ctk.CTkLabel(frame_gregistration, text="Отчество \n(при наличии)", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_patronymic_label.place(anchor="center", relx=0.3, rely=0.3)

    registration_patronymic_enptry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5")
    registration_patronymic_enptry.place(anchor="center", relx=0.7, rely=0.3)

    registration_birthday_label = ctk.CTkLabel(frame_gregistration, text="День рождения", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_birthday_label.place(anchor="center", relx=0.3, rely=0.4)

    registration_birthday_enptry = DateEntry(frame_gregistration, year=2000, month=1, day=1, width=26)
    registration_birthday_enptry.place(anchor="center", relx=0.7, rely=0.4)

    registration_passport_seria_label = ctk.CTkLabel(frame_gregistration, text="Серия паспорта", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_passport_seria_label.place(anchor="center", relx=0.3, rely=0.5)

    registration_passport_seria_enptry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5",  validate='key', validatecommand=vcmd)
    registration_passport_seria_enptry.place(anchor="center", relx=0.7, rely=0.5)

    registration_passport_nomber_label = ctk.CTkLabel(frame_gregistration, text="Номер паспорта", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_passport_nomber_label.place(anchor="center", relx=0.3, rely=0.6)

    registration_passport_nomber_enptry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5",  validate='key', validatecommand=vcmd)
    registration_passport_nomber_enptry.place(anchor="center", relx=0.7, rely=0.6)

    registration_possition_label = ctk.CTkLabel(frame_gregistration, text="Должность", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_possition_label.place(anchor="center", relx=0.3, rely=0.7)

    registration_possition = get_position_from_POSITIONS()
    registration_possition_enptry = ctk.CTkComboBox(frame_gregistration, width=180, values=registration_possition, fg_color="white", border_color="#a5a5a5", text_color="black", button_color="#a5a5a5", dropdown_fg_color="white", dropdown_hover_color="#a5a5a5", dropdown_text_color="black")
    registration_possition_enptry.place(anchor="center", relx=0.7, rely=0.7)

    registration_login_label = ctk.CTkLabel(frame_gregistration, text="Логин", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_login_label.place(anchor="center", relx=0.3, rely=0.8)

    registration_login_enptry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5")
    registration_login_enptry.place(anchor="center", relx=0.7, rely=0.8)

    registration_password_label = ctk.CTkLabel(frame_gregistration, text="Пароль", text_color="BlueViolet", fg_color='white', font=("arial", 20))
    registration_password_label.place(anchor="center", relx=0.3, rely=0.9)

    registration_password_entry = ctk.CTkEntry(frame_gregistration, width=180, fg_color="white", placeholder_text_color="black", text_color="black", show="*", border_color="#a5a5a5")
    registration_password_entry.place(anchor="center", relx=0.7, rely=0.9)

    registration_butn = ctk.CTkButton(page_registration, text="Регистрация", font=("Arial", 15), width=100, fg_color="BlueViolet", command=main)
    registration_butn.place(anchor='center', relx=0.45, rely=0.9)

    registration_butn_menu = ctk.CTkButton(page_registration, text="Меню", font=("Arial", 15), width=100,
                                      fg_color="BlueViolet", command=go_menu)
    registration_butn_menu.place(anchor='center', relx=0.55, rely=0.9)

def open_menu(name):
    def show_page():
        name.destroy()
        page = tk.Tk()
        page.title("Menu")
        full_screen(page)
        page.resizable(False, False)

        menu_frame = ctk.CTkFrame(page, width=500, height=600, fg_color="white", border_color="BlueViolet",
                                  border_width=2)
        menu_frame.place(anchor="center", relx=0.5, rely=0.44)

        menu = ctk.CTkLabel(menu_frame, text="Главное меню", text_color="BlueViolet", font=("arial", 50))
        menu.place(anchor="center", relx=0.5, rely=0.2)

        btn_postavka = ctk.CTkButton(menu_frame, text="Принять поставку", command=lambda: open_postavka(page), fg_color="BlueViolet", width=400, font=("arial", 25))
        btn_postavka.place(anchor="center", relx=0.5, rely=0.5)

        btn_zakaz = ctk.CTkButton(menu_frame, text="Aссортимент", command=lambda: open_sell(page), fg_color="BlueViolet", width=400, font=("arial", 25))
        btn_zakaz.place(anchor="center", relx=0.5, rely=0.6)

        bnt_exel = ctk.CTkButton(menu_frame, text="Экспорт в Exel", command=lambda: open_exel(page), fg_color="BlueViolet", width=400, font=("arial", 25))
        bnt_exel.place(anchor="center", relx=0.5, rely=0.7)
    if (name == window):
        global login, password
        login = go_login_enptry.get()
        password = go_password_entry.get()
        if (len(login) != 0 and len(password) != 0):
            log = login_find_all_in_users(login, password)
            if (log == True):
                show_page()
            else:
                messagebox.showerror("EROR","неверный логин или пароль")
        else:
            messagebox.showerror("EROR", "Введены не все данные")
    if (name != window):
        show_page()

def open_exel(name):
    name.destroy()
    page_exel = tk.Tk()
    full_screen(page_exel)
    page_exel.title("Экспорт в excel")

    excel_frame = ctk.CTkFrame(page_exel, width=500, height=600, fg_color="white", border_color="BlueViolet",
                              border_width=2)
    excel_frame.place(anchor="center", relx=0.5, rely=0.44)

    exel_menu = ctk.CTkLabel(excel_frame, text="Экспорт в Exсel", text_color="BlueViolet", font=("arial", 50))
    exel_menu.place(anchor="center", relx=0.5, rely=0.2)

    btn_history = ctk.CTkButton(excel_frame, text="Экспорт истории продаж", command=export_history_to_excel,
                                 fg_color="BlueViolet", width=400, font=("arial", 25))
    btn_history.place(anchor="center", relx=0.5, rely=0.5)

    btn_tovar = ctk.CTkButton(excel_frame, text="Экспорт ассортимента", fg_color="BlueViolet",command=export_tovar_to_excel,
                              width=400, font=("arial", 25))
    btn_tovar.place(anchor="center", relx=0.5, rely=0.6)

    bnt_user = ctk.CTkButton(excel_frame, text="Список сотрудников",  fg_color="BlueViolet", width=400, command=export_user_to_excel,
                             font=("arial", 25))
    bnt_user.place(anchor="center", relx=0.5, rely=0.7)

    btn_menu = ctk.CTkButton(page_exel, text="Меню", fg_color="BlueViolet",command=lambda: open_menu(page_exel),
                              width=200, font=("arial", 25))
    btn_menu.place(anchor="center", relx=0.1, rely=0.1)

def open_postavka(name):
    name.destroy()
    page_postavka = tk.Tk()
    page_postavka.title("Поставка")
    full_screen(page_postavka)
    page_postavka.resizable(False, False)

    frame = ctk.CTkFrame(page_postavka, width=650, height=550, border_color="black", fg_color="white")
    frame.place(anchor="center", relx=0.5, rely=0.42)

    def validate(new_value):
        return new_value == "" or new_value.isnumeric()

    vcmd = (page_postavka.register(validate), '%P')

    title = ctk.CTkLabel(frame, text="Принять поставку", font=("Arial", 30), width=25, text_color="BlueViolet")
    title.place(anchor="center", relx=0.5, rely=0.1)

    postavka_pos = ctk.CTkLabel(frame, text="Поставщик", font=("Arial", 23), text_color="black")
    postavka_pos.place(x=50, rely=0.2)
    pos_str = get_sellers_from_db()
    pos_str = ctk.CTkComboBox(frame, width=305, values=pos_str, fg_color="white", border_color="#a5a5a5", text_color="black", button_color="#a5a5a5", dropdown_fg_color="white", dropdown_hover_color="#a5a5a5",dropdown_text_color="black")
    pos_str.place(x=300, rely=0.21)

    postavka_brend = ctk.CTkLabel(frame, text="Бренд", font=("Arial", 23), text_color="black")
    postavka_brend.place(x=50, rely=0.3)
    brend_str = ctk.CTkEntry(frame, width=305, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5")
    brend_str.place(x=300, rely=0.31)

    postavka_model = ctk.CTkLabel(frame, text="Модель", font=("Arial", 23), text_color="black")
    postavka_model.place(x=50, rely=0.4)
    model_str = ctk.CTkEntry(frame, width=305, fg_color="white", placeholder_text_color="black", text_color="black", border_color="#a5a5a5")
    model_str.place(x=300, rely=0.41)

    postavka_count = ctk.CTkLabel(frame, text="Цена за штуку", font=("Arial", 23), text_color="black")
    postavka_count.place(x=50, rely=0.5)
    count_str = ctk.CTkEntry(frame, width=305, fg_color="white", placeholder_text_color="black", text_color="black",
                             validate='key', validatecommand=vcmd, border_color="#a5a5a5")
    count_str.place(x=300, rely=0.51)

    postavka_price = ctk.CTkLabel(frame, text="Количество", font=("Arial", 23), text_color="black")
    postavka_price.place(x=50, rely=0.6)
    price_str = ctk.CTkEntry(frame, width=305, fg_color="white", placeholder_text_color="black", text_color="black", validate='key', validatecommand=vcmd, border_color="#a5a5a5")
    price_str.place(x=300, rely=0.61)

    postavka_date = ctk.CTkLabel(frame, text="Дата", font=("Arial", 23), text_color="black")
    postavka_date.place(x=50, rely=0.7)
    data_str = DateEntry(frame, width=47, year=2024, month=12, day=10)
    data_str.place(x=300, rely=0.71)

    def save_postavka():
        seller = pos_str.get()
        brand = brend_str.get()
        model = model_str.get()
        count = count_str.get()
        price = price_str.get()
        date = data_str.get()
        list = [seller, brand, model, count, price,date]
        list1 = ['seller', 'Бренд', 'Модель', 'Цена за штуку', 'Количество', 'date']
        if (len(brand) != 0 and len(model) != 0 and len(count) != 0 and len(price) != 0 and len(date) != 0):
            add_data_to_db(seller, brand, model, count, price, date)
            messagebox.showinfo("Поставка", "Поставка принята")
            brend_str.delete(0, tk.END)
            model_str.delete(0, tk.END)
            count_str.delete(0, tk.END)
            price_str.delete(0, tk.END)
            data_str.delete(0, tk.END)
        else:
            messagebox.showerror("ERROR", "Введены не все данные")
            for i in range(0, len(list)):
                if (list[i] == ""):
                    messagebox.showerror("ERROR", f"Введи данные в поле '{list1[i]}'")
                    break

    postavka_create = ctk.CTkButton(frame, text="Принять", font=("Arial", 20), width=140, command=save_postavka, fg_color="BlueViolet")
    postavka_create.place(x=300, rely=0.8)

    postavka_sell = ctk.CTkButton(frame, text="Aссортимент", font=("Arial", 20), width=140, command=lambda: open_sell(page_postavka), fg_color="BlueViolet")
    postavka_sell.place(x=466, rely=0.8)

    postavka_menu = ctk.CTkButton(frame, text="Меню", font=("Arial", 20), width=130, command=lambda: open_menu(page_postavka), fg_color="BlueViolet")
    postavka_menu.place(x=50, rely=0.8)

def open_sell(name):
    name.destroy()
    page_sell = tk.Tk()
    page_sell.title("Aссортимент")
    full_screen(page_sell)
    page_sell.resizable(False, False)

    sell_title = tk.Label(page_sell, text="Aссортимент", font="Arial 20 bold", fg="#6807d3")
    sell_title.place(anchor="center", relx=0.5, rely=0.1)

    l1 = tk.Frame(page_sell, background="black")

    columns = ("m", "o", "n", "a", "e", "b", "t", "l")
    global tree
    tree = ttk.Treeview(l1, columns=columns, show="headings")
    style = ttk.Style()
    style.configure("Treeview.Heading", font="Arial 10 bold")
    tree.pack(fill="x", ipadx=10, ipady=100)
    tree.heading("m", text="ID", anchor="center")
    tree.heading("o", text="Поставщик", anchor="center")
    tree.heading("n", text="Бренд", anchor="center")
    tree.heading("a", text="Модель", anchor="center")
    tree.heading("e", text="цена", anchor="center")
    tree.heading("b", text="количество", anchor="center")
    tree.heading("t", text="общая цена", anchor="center")
    tree.heading("l", text="дата", anchor="center")
    #
    tree.column("#1", width=60, anchor="center")
    tree.column("#2", width=200, anchor="center")
    tree.column("#3", width=200, anchor="center")
    tree.column("#4", width=200, anchor="center")
    tree.column("#5", width=200, anchor="center")
    tree.column("#6", width=200, anchor="center")
    tree.column("#7", width=200, anchor="center")
    tree.column("#8", width=200, anchor="center")

    l1.place(anchor="center", relx=0.5, rely=0.45)

    display_data(tree)


    most_popular_brend = get_most_popular_brend()
    sell_brend = ctk.CTkLabel(page_sell, text=f"Самый популярный бренд: {most_popular_brend}", text_color="BlueViolet", font=("Arial", 19))
    sell_brend.place(x=100, y=630)

    most_popular_model = get_most_popular_model()
    sell_model = ctk.CTkLabel(page_sell, text=f"Самый популярная модель: {most_popular_model}", text_color="BlueViolet", font=("Arial", 19))
    sell_model.place(x=100, y=685)

    most_rich_price = get_most_rich_price()
    sell_price_max = ctk.CTkLabel(page_sell, text=f"Самый дорогая пара: {most_rich_price}", text_color="BlueViolet", font=("Arial", 19))
    sell_price_max.place(x=100, y=740)

    def apdate_brand():
        def change_brand():
            login = login_entry.get()
            password = password_entry.get()
            change_brand_entrance.destroy()
            if (login == "admin" and password == "1234"):
                messagebox.showinfo("Вход", "Доступ открыт")

                def update_brand():
                    selected_item = tree.selection()[0]
                    new_brand = brand_entry.get()
                    if new_brand:
                        with sqlite3.connect("БД.db") as db:
                            cursor = db.cursor()
                            cursor.execute("UPDATE shoes SET brand = ? WHERE id = ?",
                                           (new_brand, tree.item(selected_item)["values"][0]))
                            db.commit()
                        display_data(tree)
                        change_brand_window.destroy()
                    else:
                        messagebox.showerror("Ошибка", "Введите новое значение бренда")

                change_brand_window = tk.Toplevel(page_sell)
                change_brand_window.title("Изменить бренд")
                center_window(change_brand_window, 300, 150)
                change_brand_window.resizable(False, False)

                brand_label = tk.Label(change_brand_window, text="Новый бренд:", font="Arial 15")
                brand_label.pack(pady=10)

                brand_entry = tk.Entry(change_brand_window, width=30)
                brand_entry.pack(pady=10)

                update_button = ctk.CTkButton(change_brand_window, text="Обновить", fg_color="BlueViolet",
                                              command=update_brand)
                update_button.pack(pady=10)
            else:
                messagebox.showerror("EROR", "Неправильный пароль или логин")

        change_brand_entrance = tk.Toplevel(page_sell)
        change_brand_entrance.title("Вход для администратора")
        center_window(change_brand_entrance, 300, 200)
        change_brand_entrance.resizable(False, False)

        login_label = ctk.CTkLabel(change_brand_entrance, text="Логин:", text_color="BlueViolet")
        login_label.place(x=50, y=50)

        login_entry = ctk.CTkEntry(change_brand_entrance, width=100, fg_color="BlueViolet")
        login_entry.place(x=150, y=50)

        password_label = ctk.CTkLabel(change_brand_entrance, text="Пароль:", text_color="BlueViolet")
        password_label.place(x=50, y=100)

        password_entry = ctk.CTkEntry(change_brand_entrance, width=100, fg_color="BlueViolet", show="*")
        password_entry.place(x=150, y=100)

        update_button = ctk.CTkButton(change_brand_entrance, text="Войти", fg_color="BlueViolet", command=change_brand)
        update_button.place(anchor="center", relx=0.5, rely=0.9)

    def apdate_model():
        def change_model():
            login = login_entry.get()
            password = password_entry.get()
            change_model_window.destroy()
            if (login == "admin" and password == "1234"):
                def update_model():
                    selected_item = tree.selection()[0]
                    new_model = brand_entry.get()
                    if new_model:
                        with sqlite3.connect("БД.db") as db:
                            cursor = db.cursor()
                            cursor.execute("UPDATE shoes SET model = ? WHERE id = ?",
                                           (new_model, tree.item(selected_item)["values"][0]))
                            db.commit()
                        display_data(tree)
                        change_brand_window.destroy()
                    else:
                        messagebox.showerror("Ошибка", "Введите новое значение модели")

                change_brand_window = tk.Toplevel(page_sell)
                change_brand_window.title("Изменить модель")
                center_window(change_brand_window, 300, 150)
                change_brand_window.resizable(False, False)

                brand_label = tk.Label(change_brand_window, text="Новая модель:", font="Arial 15")
                brand_label.pack(pady=10)

                brand_entry = tk.Entry(change_brand_window, width=30)
                brand_entry.pack(pady=10)

                update_button = ctk.CTkButton(change_brand_window, text="Обновить", fg_color="BlueViolet",
                                              command=update_model)
                update_button.pack(pady=10)
            else:
                messagebox.showerror("EROR", "Неправильный пароль или логин")

        change_model_window = tk.Toplevel(page_sell)
        change_model_window.title("Вход для администратора")
        center_window(change_model_window, 300, 200)
        change_model_window.resizable(False, False)

        login_label = ctk.CTkLabel(change_model_window, text="Логин:", text_color="BlueViolet")
        login_label.place(x=50, y=50)

        login_entry = ctk.CTkEntry(change_model_window, width=100, fg_color="BlueViolet")
        login_entry.place(x=150, y=50)

        password_label = ctk.CTkLabel(change_model_window, text="Пароль:", text_color="BlueViolet")
        password_label.place(x=50, y=100)

        password_entry = ctk.CTkEntry(change_model_window, width=100, fg_color="BlueViolet", show="*")
        password_entry.place(x=150, y=100)

        update_button = ctk.CTkButton(change_model_window, text="Войти", fg_color="BlueViolet", command=change_model)
        update_button.place(anchor="center", relx=0.5, rely=0.9)

    def apdate_price():
        def change_price():
            login = login_entry.get()
            password = password_entry.get()
            change_price_entrance.destroy()
            if (login == "admin" and password == "1234"):
                def update_price():
                    selected_item = tree.selection()[0]
                    new_price = price_entry.get()
                    if new_price:
                        with sqlite3.connect("БД.db") as db:
                            cursor = db.cursor()
                            cursor.execute("SELECT price FROM shoes WHERE id = ?",
                                           (tree.item(selected_item)["values"][0],))
                            current_price = cursor.fetchone()[0]
                            new_total_price = float(new_price) * current_price
                            cursor.execute("UPDATE shoes SET count = ?, total_price = ? WHERE id = ?",
                                           (new_price, new_total_price, tree.item(selected_item)["values"][0]))
                            db.commit()
                        display_data(tree)
                        change_price_window.destroy()
                    else:
                        messagebox.showerror("Ошибка", "Введите новое значение цены")

                change_price_window = tk.Toplevel(page_sell)
                change_price_window.title("Изменить цену")
                center_window(change_price_window, 300, 150)
                change_price_window.resizable(False, False)

                def validate(new_value):
                    return new_value == "" or new_value.isnumeric()

                vcmd = (change_price_window.register(validate), '%P')

                price_label = tk.Label(change_price_window, text="Новая цена:", font="Arial 15")
                price_label.pack(pady=10)

                price_entry = tk.Entry(change_price_window, width=30,  validate='key', validatecommand=vcmd)
                price_entry.pack(pady=10)

                update_button = ctk.CTkButton(change_price_window, text="Обновить", fg_color="BlueViolet",
                                              command=update_price)
                update_button.pack(pady=10)
            else:
                messagebox.showerror("EROR", "Неправильный пароль или логин")

        change_price_entrance = tk.Toplevel(page_sell)
        change_price_entrance.title("Вход для администратора")
        center_window(change_price_entrance, 300, 200)
        change_price_entrance.resizable(False, False)

        login_label = ctk.CTkLabel(change_price_entrance, text="Логин:", text_color="BlueViolet")
        login_label.place(x=50, y=50)

        login_entry = ctk.CTkEntry(change_price_entrance, width=100, fg_color="BlueViolet")
        login_entry.place(x=150, y=50)

        password_label = ctk.CTkLabel(change_price_entrance, text="Пароль:", text_color="BlueViolet")
        password_label.place(x=50, y=100)

        password_entry = ctk.CTkEntry(change_price_entrance, width=100, fg_color="BlueViolet", show="*")
        password_entry.place(x=150, y=100)

        update_button = ctk.CTkButton(change_price_entrance, text="Войти", fg_color="BlueViolet", command=change_price)
        update_button.place(anchor="center", relx=0.5, rely=0.9)

    def apdate_count():
        def change_count():
            login = login_entry.get()
            password = password_entry.get()
            change_price_entrance.destroy()
            if (login == "admin" and password == "1234"):
                def update_count():
                    selected_item = tree.selection()[0]
                    new_price = price_entry.get()
                    if new_price:
                        with sqlite3.connect("БД.db") as db:
                            cursor = db.cursor()
                            cursor.execute("SELECT count FROM shoes WHERE id = ?",
                                           (tree.item(selected_item)["values"][0],))
                            current_price = cursor.fetchone()[0]
                            new_total_price = float(new_price) * current_price
                            cursor.execute("UPDATE shoes SET price = ?, total_price = ? WHERE id = ?",
                                           (new_price, new_total_price, tree.item(selected_item)["values"][0]))
                            db.commit()
                        display_data(tree)
                        change_price_window.destroy()
                    else:
                        messagebox.showerror("Ошибка", "Введите новое значение цены")

                change_price_window = tk.Toplevel(page_sell)
                change_price_window.title("Изменить количество")
                center_window(change_price_window, 300, 150)
                change_price_window.resizable(False, False)

                def validate(new_value):
                    return new_value == "" or new_value.isnumeric()

                vcmd = (change_price_window.register(validate), '%P')

                price_label = tk.Label(change_price_window, text="Новое количество:", font="Arial 15")
                price_label.pack(pady=10)

                price_entry = tk.Entry(change_price_window, width=30,  validate='key', validatecommand=vcmd)
                price_entry.pack(pady=10)

                update_button = ctk.CTkButton(change_price_window, text="Обновить", fg_color="BlueViolet",
                                              command=update_count)
                update_button.pack(pady=10)
            else:
                messagebox.showerror("EROR", "Неправильный пароль или логин")

        change_price_entrance = tk.Toplevel(page_sell)
        change_price_entrance.title("Вход для администратора")
        center_window(change_price_entrance, 300, 200)
        change_price_entrance.resizable(False, False)

        login_label = ctk.CTkLabel(change_price_entrance, text="Логин:", text_color="BlueViolet")
        login_label.place(x=50, y=50)

        login_entry = ctk.CTkEntry(change_price_entrance, width=100, fg_color="BlueViolet")
        login_entry.place(x=150, y=50)

        password_label = ctk.CTkLabel(change_price_entrance, text="Пароль:", text_color="BlueViolet")
        password_label.place(x=50, y=100)

        password_entry = ctk.CTkEntry(change_price_entrance, width=100, fg_color="BlueViolet", show="*")
        password_entry.place(x=150, y=100)

        update_button = ctk.CTkButton(change_price_entrance, text="Войти", fg_color="BlueViolet", command=change_count)
        update_button.place(anchor="center", relx=0.5, rely=0.9)

    def delete_selected_shoes(tree):
        def delete_item():
            login = login_entry.get()
            password = password_entry.get()
            change_price_entrance.destroy()
            if (login == "admin" and password == "1234"):
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Предупреждение", "Выберите строку для удаления!")
                    return

                item_id = tree.item(selected_item, "values")[0]  # Предполагаем, что первый столбец - это ID

                with sqlite3.connect("БД.db") as db:
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM shoes WHERE id = ?", (item_id,))
                    db.commit()
                tree.delete(selected_item)
                messagebox.showinfo("Успех", "Строка успешно удалена!")
            else:
                messagebox.showerror("EROR", "Неправильный пароль или логин")

        change_price_entrance = tk.Toplevel(page_sell)
        change_price_entrance.title("Вход для администратора")
        center_window(change_price_entrance, 300, 200)
        change_price_entrance.resizable(False, False)

        login_label = ctk.CTkLabel(change_price_entrance, text="Логин:", text_color="BlueViolet")
        login_label.place(x=50, y=50)

        login_entry = ctk.CTkEntry(change_price_entrance, width=100, fg_color="BlueViolet")
        login_entry.place(x=150, y=50)

        password_label = ctk.CTkLabel(change_price_entrance, text="Пароль:", text_color="BlueViolet")
        password_label.place(x=50, y=100)

        password_entry = ctk.CTkEntry(change_price_entrance, width=100, fg_color="BlueViolet", show="*")
        password_entry.place(x=150, y=100)

        update_button = ctk.CTkButton(change_price_entrance, text="Войти", fg_color="BlueViolet", command=delete_item)
        update_button.place(anchor="center", relx=0.5, rely=0.9)

    def search_model():
        model = search_entry.get()
        if model:
            with sqlite3.connect("БД.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT brand, model, count FROM shoes WHERE model LIKE ?", ('%' + model + '%',))
                results = cursor.fetchall()

            if results:
                search_window = tk.Toplevel(page_sell)
                search_window.title("Результаты поиска")
                center_window(search_window, 400, 300)
                search_window.resizable(False, False)

                result_text = tk.Text(search_window, width=50, height=15)
                result_text.pack(pady=10)

                for result in results:
                    result_text.insert(tk.END, f"Бренд: {result[0]}, Модель: {result[1]}, Цена: {result[2]}\n")
            else:
                messagebox.showinfo("Результаты поиска", "Нет результатов")
        else:
            messagebox.showerror("Ошибка", "Введите модель для поиска")

    search_entry = ctk.CTkEntry(page_sell, fg_color="white", placeholder_text="Поиск по модели", bg_color="white", border_width=0, placeholder_text_color="black", text_color="black")
    search_entry.place(relx=0.75, rely=0.15)

    search_btn = ctk.CTkButton(page_sell, text="Поиск", fg_color="BlueViolet", border_width=1, command=search_model, font=("Arial", 18))
    search_btn.place(relx=0.85, rely=0.15)

    delete_button = ctk.CTkButton(page_sell, text="Удалить строку", command=lambda: delete_selected_shoes(tree),
                                  fg_color="red", width=200, font=("Arial", 18))
    delete_button.place(x=1250, y=635)

    sell_change_brend = ctk.CTkButton(page_sell, text="Изменить бренд", fg_color="BlueViolet", command=apdate_brand, width=200, font=("Arial", 18))
    sell_change_brend.place(x=1250, y=685)

    sell_change_model = ctk.CTkButton(page_sell, text="Изменить модель", fg_color="BlueViolet", command=apdate_model, width=200, font=("Arial", 18))
    sell_change_model.place(x=1250, y=735)

    sell_change_price = ctk.CTkButton(page_sell, text="История Продаж", fg_color="BlueViolet", width=200, font=("Arial",18), command=lambda: open_history(page_sell))
    sell_change_price.place(x=980, y=635)

    sell_change_price = ctk.CTkButton(page_sell, text="Изменить цену", fg_color="BlueViolet", command=apdate_price, width=200, font=("Arial", 18))
    sell_change_price.place(x=980, y=685)

    sell_change_count = ctk.CTkButton(page_sell, text="Изменить количество", fg_color="BlueViolet", command=apdate_count, width=200, font=("Arial", 18))
    sell_change_count.place(x=980, y=735)

    sell_menu = ctk.CTkButton(page_sell, text="Меню", fg_color="BlueViolet", width=200, command=lambda: open_menu(page_sell), font=("Arial", 18))
    sell_menu.place(x=710, y=635)

    sell_postavka = ctk.CTkButton(page_sell, text="Принять поставку", fg_color="BlueViolet", width=200, command=lambda: open_postavka(page_sell), font=("Arial", 18))
    sell_postavka.place(x=710, y=685)

    create_order = ctk.CTkButton(page_sell, text="Добавить в заказ", fg_color="BlueViolet", width=200, command=lambda: open_menus(tree, page_sell), font=("Arial", 18))
    create_order.place(x=710, y=735)

    def open_history(name):
        name.destroy()
        page_history = tk.Tk()
        page_history.title("История заказов")
        full_screen(page_history)
        page_history.resizable(False, False)

        page_title = ctk.CTkLabel(page_history, text="История продаж",  font=("arial", 35), text_color="BlueViolet")
        page_title.place(anchor="center", relx=0.5, rely=0.17)

        history_Frame = tk.Frame(page_history, background="black", height=500)
        columns = ("a", "b", "c", "d", 'e', 'f')

        table3 = ttk.Treeview(history_Frame, columns=columns, show="headings")
        style = ttk.Style()
        style.configure("Treeview.Heading", font="Arial 10 bold")
        table3.pack(fill="x", ipadx=10, ipady=40)
        table3.heading("a", text="ID продовца", anchor="center")
        table3.heading("b", text="Имя", anchor="center")
        table3.heading("c", text="Фамилия", anchor="center")
        table3.heading("d", text="Бренд", anchor="center")
        table3.heading("e", text="Модель", anchor="center")
        table3.heading("f", text="Цена", anchor="center")

        table3.column("#1", width=145, anchor="center")
        table3.column("#2", width=145, anchor="center")
        table3.column("#3", width=145, anchor="center")
        table3.column("#4", width=145, anchor="center")
        table3.column("#5", width=145, anchor="center")
        table3.column("#6", width=145, anchor="center")
        display_orders(table3)


        history_Frame.place(anchor="center", relx=0.5, rely=0.4)

        history_menu = ctk.CTkButton(page_history, text="Ассортимент", fg_color="BlueViolet",
                                   command=lambda: open_sell(page_history), font=("arial", 18), width=200)
        history_menu.place(anchor="center", relx=0.1, rely=0.1)



    def open_menus(tree, name):
        global selected_items

        selected_item = tree.selection()

        item_data = tree.item(selected_item, "values")
        brand, model, price = item_data[2], item_data[3], item_data[4]
        selected_items.append((brand, model, price))

        name.destroy()
        page_order = tk.Tk()
        page_order.title("Заказ")
        full_screen(page_order)
        page_order.resizable(False, False)

        page_title = ctk.CTkLabel(page_order, text="Ваш заказ", font=("arial", 35), text_color="BlueViolet")
        page_title.place(anchor="center", relx=0.5, rely=0.17)

        l1 = tk.Frame(page_order, background="black", height=500)
        columns = ("n", "a", "e")

        table2 = ttk.Treeview(l1, columns=columns, show="headings")
        style = ttk.Style()
        style.configure("Treeview.Heading", font="Arial 10 bold")
        table2.pack(fill="x", ipadx=10, ipady=40)
        table2.heading("n", text="Бренд", anchor="center")
        table2.heading("a", text="Модель", anchor="center")
        table2.heading("e", text="Цена", anchor="center")

        table2.column("#1", width=145, anchor="center")
        table2.column("#2", width=145, anchor="center")
        table2.column("#3", width=145, anchor="center")

        l1.place(anchor="center", relx=0.5, rely=0.4)

        # Добавляем выбранные элементы в table2
        for item in selected_items:
            table2.insert("", "end", values=item)

        open_menus = ctk.CTkButton(page_order, text="Ассортимент", fg_color="BlueViolet",
                                   command=lambda: open_sell(page_order), font=("arial", 18), width=200)
        open_menus.place(anchor="center", relx=0.285, rely=0.8)

        clear_order = ctk.CTkButton(page_order, text="удалить из заказа", fg_color="BlueViolet", font=("arial", 18),
                                     width=200, command=lambda: clear_roe_in_orders(table2))
        clear_order.place(anchor="center", relx=0.715, rely=0.8)

        clear_button = ctk.CTkButton(page_order, text="купить", fg_color="BlueViolet", font=("arial", 18),
                                     width=200, command=lambda: clear_orders(table2))
        clear_button.place(anchor="center", relx=0.715, rely=0.1)

        def calculate_total_price(table):
            total_price = 0.0
            for item in table.get_children():
                price = table.item(item, "values")[2]
                total_price += float(price)
            return total_price

        total_price = calculate_total_price(table2)

        total_price_label = ctk.CTkLabel(page_order, text=f"Общая сумма: {total_price}", font=("arial bold", 20), text_color="Black")
        total_price_label.place(anchor="center", relx=0.5, rely=0.8)


#ОКНО ВХОДА

window = tk.Tk()
window.title("Cенин Виктор 306ис-22")
full_screen(window)
window.attributes("-topmost", False)

image = PhotoImage(file='лого3.png')
image = image.subsample(2, 2)
image_label = tk.Label(window, height=150, image=image)
image_label.pack()

f = tk.Label(window, text="Курсовая работа", font=("Arial", 25), foreground="black")
f.place(anchor="center", relx=0.5, rely=0.25)

f1 = tk.Label(window, text="по  теме:", font=("Arial", 25), foreground="black")
f1.place(anchor="center", relx=0.5, rely=0.3)

f2 = ctk.CTkLabel(window, text="\"Обувной магазин\" ", font=("Arial", 45), text_color="BlueViolet")
f2.place(anchor="center", relx=0.5, rely=0.38)

frame_go = ctk.CTkFrame(window, width=400, height=200, fg_color="white", border_color="BlueViolet", border_width=2)
frame_go.place(anchor="center", relx=0.5, rely=0.57)

go_login_label = ctk.CTkLabel(frame_go, text="Логин", text_color="BlueViolet", fg_color='white', font=("arial", 20))
go_login_label.place(anchor="center", relx=0.2, rely=0.3)

go_login_enptry = ctk.CTkEntry(frame_go, width=150, fg_color="white", placeholder_text_color="black", text_color="black")
go_login_enptry.place(anchor="center", relx=0.65, rely=0.3)

go_password_label = ctk.CTkLabel(frame_go, text="Пароль", text_color="BlueViolet", fg_color='white', font=("arial", 20))
go_password_label.place(anchor="center", relx=0.2, rely=0.7)

go_password_entry = ctk.CTkEntry(frame_go, width=150, fg_color="white", placeholder_text_color="black", text_color="black", show="*")
go_password_entry.place(anchor="center", relx=0.65, rely=0.7)

go_button = ctk.CTkButton(window, text='Войти', command=lambda: open_menu(window), fg_color="BlueViolet", width=180, font=("arial", 20))
go_button.place(anchor="center", relx=0.43, rely=0.75)

registration_button = go_button = ctk.CTkButton(window, text='Регистрация', fg_color="BlueViolet", command=lambda : open_registration(window), width=180, font=("arial", 20))
registration_button.place(anchor="center", relx=0.57, rely=0.75)


window.mainloop()


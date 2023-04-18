import psycopg2
from signin import password, username
from functions import *

if __name__ == "__main__":
    with psycopg2.connect(database="netology_hw_db", user=username, password=password) as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_customer(cur, 'Vanda', 'Maksimof', 'red-witch@gmail.com')
            add_customer(cur, 'Natalia', 'Romanof', 'blackW@yandex.ru')
            add_customer(cur, 'Stiven', 'Strandg', 'the-doctor@gmail.com')
            add_customer(cur, 'Anthony', 'Stark', 'genius@gmail.com')
            conn.commit()
            add_phone(cur, '1', '380904883')
            add_phone(cur, '2', '79119111')
            add_phone(cur, '4', '1000000000')
            conn.commit()
            change_customer(cur, '1', first_name="Wanda", last_name='Altron')
            change_customer(cur, '4', first_name='Tony')
            conn.commit()
            find_customer(cur, first_name='Stiven')
            conn.commit()
            delete_phone(cur, phone='1000000000')
            delete_customer(cur, '2')
            conn.commit()

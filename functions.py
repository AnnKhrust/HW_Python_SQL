import psycopg2

def create_db(conn):
    conn.execute("""
        DROP TABLE IF EXISTS phonebook;
        DROP TABLE IF EXISTS customer CASCADE;
        """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customer(
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR (40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(40) UNIQUE 
            );
        """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phonebook(
            customer_id INTEGER REFERENCES customer(customer_id),
            phone INTEGER UNIQUE CHECK(phone >= 0)
            );
        """)

def add_customer(conn, first_name, last_name, email, phones=None):
    conn.execute("""
    INSERT INTO customer (first_name, last_name, email) VALUES(%s, %s, %s);
    """, (first_name, last_name, email))

def add_phone(conn, customer_id, phone):
    conn.execute("""
    INSERT INTO phonebook (customer_id, phone) VALUES(%s, %s);
    """, (customer_id, phone))

def change_customer(conn, customer_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        conn.execute("""
        UPDATE customer SET first_name=%s WHERE customer_id=%s
        """, (first_name, customer_id))
    
    if last_name is not None:
        conn.execute("""
        UPDATE customer SET last_name=%s WHERE customer_id=%s
        """, (last_name, customer_id))
    
    if email is not None:
        conn.execute("""
        UPDATE customer SET email=%s WHERE customer_id=%s
        """, (email, customer_id))
    
    if phone is not None:
        conn.execute("""
        UPDATE phonebook SET phone=%s WHERE customer_id=%s
        """, (customer_id, phone))

def delete_phone(conn, phone):
    conn.execute("""
    DELETE FROM phonebook WHERE phone=%s;
    """, (phone,))

def delete_customer(conn, customer_id):
    conn.execute("""
    DELETE FROM phonebook WHERE customer_id=%s;
    """, (customer_id,))

    conn.execute("""
    DELETE FROM customer WHERE customer_id=%s;
    """, (customer_id,))

def find_customer(conn, first_name=None, last_name=None, email=None, phone=None):
    column = []
    param = []
    if first_name:
        column.append('first_name=%s')
        param.append(first_name)
    if last_name:
        column.append('last_name=%s')
        param.append(last_name)
    if email:
        column.append('email=%s')
        param.append(email)
    if phone:
        column.append('phone=%s')
        param.append(phone)

        
    conn.execute(f"""
        SELECT cl.first_name, cl.last_name, cl.email, ph.phone,  cl.customer_id FROM customer AS cl
        LEFT JOIN phonebook AS ph ON cl.customer_id = ph.customer_id
        WHERE {' and '.join(column)}""", param)

    return conn.fetchone()
    
    

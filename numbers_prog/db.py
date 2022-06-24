from typing import Dict
import psycopg2

def insert(table: str, columns_values: Dict):
    conn = connect_db()
    cursor = conn.cursor()
    columns = ', '.join(columns_values.keys())
    values = tuple(columns_values.values())
    placeholder = ', '.join(['%s'] * len(columns_values.keys()))
    cursor.execute(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholder})",
        values)
    conn.commit()
    conn.close()

def update(table: str, columns_values: Dict):
    conn = connect_db()
    cursor = conn.cursor()
    id_column = tuple(columns_values.keys())[-1]+'=%s'
    columns = ', '.join(map(lambda column: column+'=%s', tuple(columns_values.keys())[:-1]))
    values = tuple(columns_values.values())
    cursor.execute(
        f"UPDATE {table} SET "
        f"{columns} "
        f"WHERE {id_column}",
        values)
    conn.commit()
    conn.close()

def connect_db():
    conn = psycopg2.connect(user='postgres',
                            password='password',
                            host='127.0.0.1',
                            port='5432',
                            database='numbersdb')
    return conn

def _init_db(conn):
    """инициализирует БД"""
    cursor = conn.cursor()

    with open('createdb.sql','r') as f:
        sql = f.read()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def check_db_exists():
    """проверяет инициализирована БД, если нет инициализирует"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pg_tables "
                   "WHERE tablename='orders'")
    table_exists = cursor.fetchall()
    if table_exists:
        conn.close()
        return
    _init_db(conn)

check_db_exists()

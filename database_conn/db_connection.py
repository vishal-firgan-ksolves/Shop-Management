import os
import psycopg2
#
# connection = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="root",
#     host="localhost",
#     port="5432"
# )

# Create a cursor object
# cursor = connection.cursor()

# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)

import psycopg2
import psycopg2
class DBConnection:
    conn_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'root',
        'host': 'localhost',
        'port': '5432'
    }
    _conn = None
    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            try:
                cls._conn = psycopg2.connect(**cls.conn_params)
                print("Database connection established.")
            except Exception as e:
                print(f"Error connecting to database: {e}")
                raise
        return cls._conn

    @classmethod
    def get_cursor(cls):
        _conn = cls.get_connection()
        return _conn.cursor()

    @classmethod
    def execute_query(cls, query, params=None):
        cursor= cls.get_cursor()
        cursor.execute(query, params)
        cls.get_connection().commit()

    @classmethod
    def fetch_one(cls, query, params=None):
        cursor = cls.get_cursor()
        # print(f"Executing query: {query} with parameters: {params}")
        cursor.execute(query, params)
        result = cursor.fetchone()
        # print(f"Query result: {result}")
        return result

    @classmethod
    def fetch_all(cls,query,params=None):
        cursor=cls.get_cursor()
        cursor.execute(query,(params,))
        return cursor.fetchall()

    @classmethod
    def close(cls):
      if cls._conn is not None:
            cls._conn.close()
            cls._conn = None
            print("Connection to db closed")











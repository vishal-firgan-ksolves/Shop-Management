# import bcrypt
# from database_conn.db_connection import DBConnection  # Assuming DBConnection is defined in db_connection.py
#
#
# def insert_admin_user():
#     # Define the username, password, and role for the admin user
#     username = 'admin1'
#     password = 'admin123'
#     role = 'admin'
#
#     # Hash the password
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#
#     # Define the SQL query to insert the admin user
#     insert_query = """
#     INSERT INTO shopdb.users (username, password, role)
#     VALUES (%s, %s, %s);
#     """
#
#     # Define the parameters for the query
#     params = (username, hashed_password.decode('utf-8'), role)
#
#     try:
#         # Execute the query
#         DBConnection.execute_query(insert_query, params)
#         print("Admin user inserted successfully.")
#     except Exception as e:
#         print(f"Error inserting admin user: {e}")
#     finally:
#         # Close the database connection
#         DBConnection.close()
#
#
# if __name__ == "__main__":
#     insert_admin_user()

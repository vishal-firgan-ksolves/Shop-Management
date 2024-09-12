import psycopg2
from psycopg2 import sql
from database_conn.db_connection import DBConnection
from security.user import User
class Suppliers:

    @staticmethod
    def create_supplier(name, contact_no, email, address):
        query = '''
            INSERT INTO shopdb.suppliers (name, contact_no, email, address)
            VALUES (%s, %s, %s, %s)
        '''
        DBConnection.execute_query(query, (name, contact_no, email, address))
        print("Created Successfully")

    @staticmethod
    def delete_supplier(supplierid):
        query = '''
            DELETE FROM shopdb.suppliers
            WHERE supplier_id = %s
        '''
        DBConnection.execute_query(query, (supplierid,))
        print("Deleted Successfully")
    @staticmethod
    def authenticate_admin():

        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        if User.authenticate_user(username, password):
            if User.authorize_user(username, 'admin'):
                print("Admin authenticated successfully.")
                return username
            else:
                print("User does not have admin role.")
                return None
        else:
            print("Authentication failed.")
            return None


# Example usage:
# if __name__ == "__main__":
#
#     is_valid=Suppliers.authenticate_admin()
#
#     if is_valid:
#         while True:
#             choice = input("Enter your choice (1: Create / 2: Delete / 3: Exit): ")
#             if choice == '1':
#                 name=input("Enter name of supp: ")
#                 contact_no=input("Enter contanct number of supp: ")
#                 email=input("Enter email o supp: ")
#                 address=input("Enter address of supp: ")
#                 Suppliers.create_supplier( name, contact_no, email, address)
#             elif choice == '2':
#                 supplier_id = int(input("Enter the supplier ID to delete: "))
#                 Suppliers.delete_supplier(supplier_id)
#             elif choice == '3':
#                 break
#             else:
#                 print("Invalid choice. Please enter a number between 1 and 3.")
#     DBConnection.close()

from dateutil.relativedelta import SU

from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME,SUPPLIERS_TABLE
class Suppliers:

    @staticmethod
    def create_supplier(name, contact_no, email, address):
        query = f'''
            INSERT INTO {SCHEMA_NAME}.{SUPPLIERS_TABLE} (name, contact_no, email, address)
            VALUES (%s, %s, %s, %s)
        '''
        DBConnection.execute_query(query, (name, contact_no, email, address))
        print("Created Successfully")

    @staticmethod
    def view_supplier(supplier_id):

        query = f'''
                SELECT * FROM {SCHEMA_NAME}.{SUPPLIERS_TABLE}
                WHERE supplier_id = %s
            '''
        result = DBConnection.fetch_one(query, (supplier_id,))
        if result:
            print("Supplier Details:")
            print(f"Supplier ID: {result[0]}")
            print(f"Name: {result[1]}")
            print(f"Contact No: {result[2]}")
            print(f"Email: {result[3]}")
            print(f"Address: {result[4]}")
        else:
            print("Supplier not found.")

    @staticmethod
    def list_all_suppliers():

        query = f'''
                SELECT * FROM {SCHEMA_NAME}.{SUPPLIERS_TABLE}
            '''
        results = DBConnection.fetch_all(query)
        if results:
            print("List of Suppliers:")
            for supplier in results:
                print(
                    f"Supplier ID: {supplier[0]}, Name: {supplier[1]}, Contact No: {supplier[2]}, Email: {supplier[3]}, Address: {supplier[4]}")
        else:
            print("No suppliers found.")

    @staticmethod
    def delete_supplier(supplierid):
        query = f'''
            DELETE FROM ={SCHEMA_NAME}.{SUPPLIERS_TABLE}
            WHERE supplier_id = %s
        '''
        DBConnection.execute_query(query, (supplierid,))
        print("Deleted Successfully")

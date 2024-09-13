import psycopg2
from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME,PRODUCTS_TABLE
class Products:

    @staticmethod
    def create_product(name, price, cost_price, supplier_id, quantity):
        query = f'''
            INSERT INTO {SCHEMA_NAME}.{PRODUCTS_TABLE} (name, price, cost_price, supplier_id, quantity)
            VALUES (%s, %s, %s, %s, %s)
        '''
        try:
            DBConnection.execute_query(query, (name, price, cost_price, supplier_id, quantity))
            print("Product created successfully.")
        except Exception as e:
            print(f"Error creating product: {e}")

    @staticmethod
    def update_product(product_id, name=None, price=None, cost_price=None, supplier_id=None, quantity=None):
        updates = []
        params = []

        if name is not None:
            updates.append('name = %s')
            params.append(name)
        if price is not None:
            updates.append('price = %s')
            params.append(price)
        if cost_price is not None:
            updates.append('cost_price = %s')
            params.append(cost_price)
        if supplier_id is not None:
            updates.append('supplier_id = %s')
            params.append(supplier_id)
        if quantity is not None:
            updates.append('quantity = %s')
            params.append(quantity)

        if not updates:
            raise ValueError("No fields to update")

        query = f'''
            UPDATE {SCHEMA_NAME}.{PRODUCTS_TABLE}
            SET {', '.join(updates)}
            WHERE product_id = %s
        '''
        params.append(product_id)

        try:
            DBConnection.execute_query(query, tuple(params))
            print("Product updated successfully.")
        except Exception as e:
            print(f"Error updating product: {e}")

    @staticmethod
    def delete_product(product_id):
        query = f'''
            DELETE FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
            WHERE product_id = %s
        '''
        try:
            DBConnection.execute_query(query, (product_id,))
            print("Product deleted successfully.")
        except Exception as e:
            print(f"Error deleting product: {e}")

    @staticmethod
    def fetch_product(product_id):
        query = f'''
            SELECT * FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
            WHERE product_id = %s
        '''
        return DBConnection.fetch_one(query, (product_id,))

    @staticmethod
    def fetch_all_products():
        query = f'''
            SELECT * FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
        '''
        return DBConnection.fetch_all(query)

    @staticmethod
    def get_product_cost(product_id):

        query = f'''
               SELECT cost_price FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
               WHERE product_id = %s
           '''
        result = DBConnection.fetch_one(query, (product_id,))
        return result[0] if result else 0.0



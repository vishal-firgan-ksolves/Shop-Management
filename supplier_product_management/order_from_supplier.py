import psycopg2
from database_conn.db_connection import DBConnection
from product_management import Products
from constants.constants import SCHEMA_NAME, PURCHASE_ORDERS_TABLE, PRODUCTS_TABLE


class PurchaseOrders:

    @staticmethod
    def create_order(supplier_id,product_id, quantity):

        try:
            total_amount = 0.0
            total_amount= Products.get_product_cost(product_id)* quantity

            query = f'''
                INSERT INTO {SCHEMA_NAME}.{PURCHASE_ORDERS_TABLE} (supplier_id, product_id,quantity ,total_amount)
                VALUES (%s, %s, %s,%s)  
            '''

            DBConnection.execute_query(query, (supplier_id, product_id, quantity, total_amount))
            PurchaseOrders.update_inventory(product_id, quantity)
        except Exception as e:
            print(f"Error while creating purchase order {e}")

    @staticmethod
    def update_inventory(product_id, quantity):
        query = f'''
            UPDATE {SCHEMA_NAME}.{PRODUCTS_TABLE}
            SET quantity = quantity + %s
            WHERE product_id = %s
        '''
        try:
            DBConnection.execute_query(query, (quantity, product_id))
            print(f"Inventory updated for product {product_id}.")
        except Exception as e:
            print(f"Error updating inventory: {e}")

    @staticmethod
    def delete_order(order_id):
        query = f'''
            DELETE FROM {SCHEMA_NAME}.{PURCHASE_ORDERS_TABLE}
            WHERE order_id = %s
        '''
        q=f"select product_id,quantity from {SCHEMA_NAME}.{PURCHASE_ORDERS_TABLE} where order_id=%s"
        p_id,quan=DBConnection.fetch_one(q,(order_id,))

        try:
            DBConnection.execute_query(query, (order_id,))
            PurchaseOrders.update_inventory(p_id, -quan)
            print("Purchase order deleted successfully.")
        except Exception as e:
            print(f"Error deleting purchase order: {e}")

    @staticmethod
    def fetch_order(order_id):

        query = f'''
            SELECT * FROM {SCHEMA_NAME}.{PURCHASE_ORDERS_TABLE}
            WHERE order_id = %s
        '''
        return DBConnection.fetch_one(query, (order_id,))

    @staticmethod
    def fetch_all_orders():
        query = f'''
            SELECT * FROM {SCHEMA_NAME}.{PURCHASE_ORDERS_TABLE}
        '''
        return DBConnection.fetch_all(query)

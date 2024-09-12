import psycopg2
from database_conn.db_connection import DBConnection
from product_management import Products


class PurchaseOrders:

    @staticmethod
    def create_order(supplier_id,product_id, quantity):

        try:
            total_amount = 0.0
            total_amount= Products.get_product_cost(product_id)* quantity

            query = '''
                INSERT INTO shopdb.purchase_orders (supplier_id, product_id,quantity ,total_amount)
                VALUES (%s, %s, %s,%s)  
            '''

            DBConnection.execute_query(query, (supplier_id, product_id, quantity, total_amount))
            PurchaseOrders.update_inventory(product_id, quantity)
        except Exception as e:
            print(f"Error while creating purchase order {e}")


    @staticmethod
    def update_inventory(product_id, quantity):
        query = '''
            UPDATE shopdb.products
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
        query = '''
            DELETE FROM shopdb.purchase_orders
            WHERE order_id = %s
        '''
        q="select product_id,quantity from shopdb.purchase_orders where order_id=%s"
        p_id,quan=DBConnection.fetch_one(q,(order_id,))

        try:
            DBConnection.execute_query(query, (order_id,))
            PurchaseOrders.update_inventory(p_id, -quan)
            print("Purchase order deleted successfully.")
        except Exception as e:
            print(f"Error deleting purchase order: {e}")

    @staticmethod
    def fetch_order(order_id):

        query = '''
            SELECT * FROM shopdb.purchase_orders
            WHERE order_id = %s
        '''
        return DBConnection.fetch_one(query, (order_id,))

    @staticmethod
    def fetch_all_orders():
        query = '''
            SELECT * FROM shopdb.purchase_orders
        '''
        return DBConnection.fetch_all(query)

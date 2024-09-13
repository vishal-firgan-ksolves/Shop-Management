from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME, SALES_TABLE, PRODUCTS_TABLE, ORDERS_TABLE


class ProductRecommendationService:

    @staticmethod
    def get_customer_purchase_history(customer_id):

        query = f'''
            SELECT s.order_id, s.product_id, s.quantity, s.discount_amt, s.sale_date
            FROM {SCHEMA_NAME}.{SALES_TABLE} s
            JOIN {SCHEMA_NAME}.{ORDERS_TABLE} o
            ON o.order_id = s.order_id
            WHERE o.customer_id = %s
            ORDER BY s.sale_date DESC
            limit 4
        '''
        return DBConnection.fetch_all(query, (customer_id,))

    @staticmethod
    def get_product_categories(purchase_history):
        # got list of tuples
        product_ids = set()
        for item in purchase_history:
            # adding each purchased products id in set
            product_ids.add(item[1])

        if not product_ids:
            return {}

        # Convert set to a list
        product_ids_list = list(product_ids)

        query = f'''
            SELECT product_id, category
            FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
            WHERE product_id = ANY(%s)
        '''
        category_data = DBConnection.fetch_all(query, (product_ids_list,))

        # using dict to store the id with category so that no duplicates for keys
        product_categories = {}
        # below category_data is in list of tuples so upacking the tuple then using
        for product_id, category in category_data:
            product_categories[product_id] = category

        return product_categories

    @staticmethod
    def suggest_related_products(product_category, top_n=3):

        query = f'''
            SELECT product_id, name
            FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
            WHERE category = %s
            LIMIT %s
        '''
        return DBConnection.fetch_all(query, (product_category, top_n))

    @staticmethod
    def recommend_products_for_customer(customer_id):
        #  purchase history for the customer
        purchase_history = ProductRecommendationService.get_customer_purchase_history(customer_id)
        print(f"Purchase history for customer {customer_id}:")
        # print(purchase_history)
        for p in purchase_history:
            print(p)

        if not purchase_history:
            print("No purchase history found for this customer.")
            return

        # getting product categories from purchase history
        product_categories = ProductRecommendationService.get_product_categories(purchase_history)
        if not product_categories:
            print("No product categories found.")
            return

        # Collect categories from all purchased products
        categories = set()
        for category in product_categories.values():
            categories.add(category)

        for category in categories:
            # Suggest related products based on the category
            related_products = ProductRecommendationService.suggest_related_products(category)
            print(f"\nRelated products in category '{category}':")
            for product_id, product_name in related_products:
                print(f"Product ID: {product_id}, Name: {product_name}")


# Example usage
if __name__ == "__main__":
    customer_id = 100006  # Example customer ID
    ProductRecommendationService.recommend_products_for_customer(customer_id)
    DBConnection.close()

from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME, PRODUCTS_TABLE, SUPPLIERS_TABLE


class Search:
    def __init__(self):
       pass
    @staticmethod
    def search_by_category(search_category):
        found_by_category = []
        query = f"""SELECT product_id, name, quantity, price FROM {SCHEMA_NAME}.{PRODUCTS_TABLE} WHERE LOWER(category) = %s"""
        result = DBConnection.fetch_all(query, (search_category,))

        for row in result:
            db_name = row[1].lower()
            db_p_id = row[0]
            db_quantity = row[2]
            db_price = row[3]

            found_by_category.append({
                'name': db_name,
                'product_id': db_p_id,
                'quantity': db_quantity,
                'price': db_price
            })

        print("\n\n\n")


        if found_by_category:
            print(f"<<<<<<<< List of all products in category: {search_category} >>>>>>>>>")
            for product in found_by_category:
                print(f"Name: {product['name']}",end=" | " )
                print(f"Product ID: {product['product_id']}",end=" | " )
                print(f"Quantity: {product['quantity']}",end=" | " )
                print(f"Price: ${product['price']:.2f}")
                print("-" * 30)
        else:
            print("No products found in this category.")

    @staticmethod
    def search_by_supplier(search_supplier):
        if search_supplier is None:
            print("No supplier specified.")
            return

        found_by_supplier = []
        query = f"""SELECT p.product_id, p.name, p.quantity, p.price, s.supplier_id, s.name 
                      FROM {SCHEMA_NAME}.{PRODUCTS_TABLE} p
                      JOIN {SCHEMA_NAME}.{SUPPLIERS_TABLE} s ON p.supplier_id = s.supplier_id
                      WHERE LOWER(s.name) = %s"""
        result = DBConnection.fetch_all(query, (search_supplier,))

        for row in result:
            db_name = row[1].lower()
            db_p_id = row[0]
            db_quantity = row[2]
            db_price = row[3]
            supplier_id = row[4]
            supplier_name = row[5].lower()

            found_by_supplier.append({
                'name': db_name,
                'product_id': db_p_id,
                'quantity': db_quantity,
                'price': db_price,
                'supplier_id': supplier_id,
                'supplier_name': supplier_name
            })

        print("\n\n\n")
        print(f"<<<<<<<< List of all products from supplier: {search_supplier} >>>>>>>>>")

        if found_by_supplier:
            for product in found_by_supplier:
                print(f"Name: {product['name']}")
                print(f"Product ID: {product['product_id']}")
                print(f"Quantity: {product['quantity']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Supplier ID: {product['supplier_id']}")
                print(f"Supplier Name: {product['supplier_name']}")
                print("-" * 30)
        else:
            print("No products found from this supplier.")
    @staticmethod
    def search_by_name(search_string):
        query = """SELECT product_id, name, quantity, price FROM shopdb.products"""
        result = DBConnection.fetch_all(query)
        found_products = []

        for row in result:
            db_name = row[1].lower()
            db_p_id = row[0]
            db_quantity = row[2]
            db_price = row[3]

            if (search_string == db_name or
                    db_name.startswith(search_string) or
                    db_name.endswith(search_string) or
                    search_string in db_name):
                found_products.append({
                    'name': db_name,
                    'product_id': db_p_id,
                    'quantity': db_quantity,
                    'price': db_price
                })

        if found_products:
            print("\n\nFound Products by search:")
            for product in found_products:
                print(f"Name: {product['name']}",end=" | " )
                print(f"Product ID: {product['product_id']}",end=" | " )
                print(f"Quantity: {product['quantity']}",end=" | " )
                print(f"Price: ${product['price']:.2f}"  )
                print("-" * 30)
        else:
            print("No products found with that name.")




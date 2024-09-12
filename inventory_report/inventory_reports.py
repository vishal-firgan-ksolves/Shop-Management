from datetime import datetime
from getpass import getpass
from database_conn.db_connection import DBConnection
from security.user import User


class InventoryReport:
    def __init__(self):
        self.today = datetime.now()

    def fetch_expired_products(self):
        query = """
        SELECT
            product_id,
            name,
            expiry_date
        FROM
            shopdb.products
        WHERE
            expiry_date < CURRENT_DATE;
        """
        result = DBConnection.fetch_all(query)
        return result

    def fetch_about_to_expire_products(self):
        query = """
        SELECT
            product_id,
            name,
            expiry_date
        FROM
            shopdb.products
        WHERE
            expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days';
        """
        result = DBConnection.fetch_all(query)
        return result

    def print_report(self):
        print("\nExpired Products Report")
        print("=" * len("Expired Products Report"))
        expired_products = self.fetch_expired_products()
        if expired_products:
            for product in expired_products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Expiry Date: {product[2]}")
        else:
            print("No products have expired.")

        print("\nProducts About to Expire Report")
        print("=" * len("Products About to Expire Report"))
        about_to_expire_products = self.fetch_about_to_expire_products()
        if about_to_expire_products:
            for product in about_to_expire_products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Expiry Date: {product[2]}")
        else:
            print("No products are about to expire.")
    @staticmethod
    def remove_expired_products():
        # Fetch expired products (optional, for reporting/logging)
        fetch_query = """
        SELECT name, expiry_date 
        FROM shopdb.products 
        WHERE expiry_date < CURRENT_DATE
        """
        expired_products = DBConnection.fetch_all(fetch_query)

        # Optionally, log or print expired products for review
        if expired_products:
            print("Expired Products:")
            for product in expired_products:
                print(f"Name: {product[0]}, Expiration Date: {product[1]}")
        else:
            print("No expired products found.")

        # Delete expired products
        delete_query = """
        DELETE FROM shopdb.products 
        WHERE expiry_date < CURRENT_DATE
        """
        try:
            DBConnection.execute_query(delete_query)
            print("Expired products have been removed.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":

    username = input("Enter  username: ")
    password = input("Enter  password: ")

    if User.authenticate_user(username, password):
            print("User authenticated successfully.")
            report_generator = InventoryReport()
            report_generator.print_report()
            flag = input("Want to remove expired products? yes/no : ").lower()
            if flag == 'yes':
                InventoryReport.remove_expired_products()
    else:
        print("Authentication failed.")




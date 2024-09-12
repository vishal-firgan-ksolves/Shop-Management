from database_conn.db_connection import DBConnection
from orders import Order

import datetime
from security.user import User

def generate_order_id():
    prefix = "OR"
    timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    return prefix + timestamp

def process_order():
    order_id = generate_order_id()
    customer_id = int(input("Enter Customer ID: "))
    payment_method = input("Enter Payment Method: ")
    list_low_stock_products()
    order = Order(order_id, customer_id, payment_method)
    while True:
        product_id = int(input("Enter Product ID (or 0 to finish): "))

        if product_id == 0:
            break

        # Fetch product details including current quantity,id and expiry_date
        product_info = DBConnection.fetch_one(
            "SELECT product_id, quantity,expiry_date FROM shopdb.products WHERE product_id = %s",
            (product_id,))

        if product_info is None:
            print("Product not found.")
            continue

        current_quantity = product_info[1]

        quantity = int(input("Enter Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            continue

        if quantity > current_quantity:
            print(f"Insufficient stock. Only {current_quantity} units available.")
            continue
        curr_date = DBConnection.fetch_one("select current_date")[0]

        if product_info[2] is not None and product_info[2] < curr_date:
            print("The product is expired .")
            flag=input("Want to remove expired products Yes/No").lower()
            if flag== 'yes':
                Order.remove_expired_products()
            continue

        discount_per = float(input("Enter Discount Percentage: "))
        order.add_product(product_id, quantity, discount_per)

    order.create_order()

    order.generate_pdf_bill()

    print("Order created and bill generated successfully.")

def list_low_stock_products():
    threshold=15

    fetch_query = """
      SELECT product_id, name, quantity
      FROM shopdb.products
      WHERE quantity < %s
      """
    try:
        low_stock_products = DBConnection.fetch_all(fetch_query, (threshold,))

        # Log or print low stock products for review
        if low_stock_products:
            print("Low Stock Products:")
            for product in low_stock_products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}")
        else:
            print("No products with low stock found.")

    except Exception as e:
        print(f"An error occurred while fetching low stock products: e")

def main():
    username = input("Enter  username: ")
    password = input("Enter  password: ")

    if User.authenticate_user(username, password):
        print("Admin authenticated successfully.")
        while True:
            print("\n1. Create Order")
            print("2. Remove Expired Products")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                process_order()
            elif choice == '2':
                Order.remove_expired_products()
                print("Expired products removed successfully.")
            elif choice == '0':
                DBConnection.close()
                break

    else:
        print("Authentication failed.")


if __name__ == "__main__":
    main()

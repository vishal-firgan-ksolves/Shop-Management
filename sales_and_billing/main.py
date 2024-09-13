from database_conn.db_connection import DBConnection
from orders import Order
from constants.constants import SCHEMA_NAME,PRODUCTS_TABLE
import datetime
from security.user import User
from customer_management.customer_manager import Customer
from product_recommendation.recommendation_service import ProductRecommendationService
def generate_order_id():
    prefix = "OR"
    timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    return prefix + timestamp

def process_order():
    print("===========================================")
    list_low_stock_products()
    print("===========================================")
    print()
    order_id = generate_order_id()
    new_custo=input("New customer? y/n :").lower()
    customer_id=None
    if new_custo=='y':
        cname=input("Enter name of customer:")
        ccontact_no=input("Enter conatact no of customer:")
        cemail=input("Enter email of customer: ")
        caddress=input("Enter address of customer: ")
        Customer.create_customer(cname,ccontact_no,cemail,caddress)
        print("Customer created with id: ",Customer.get_customer_by_name(cname)[0])

    customer_id = int(input("Enter Customer ID: "))
    payment_method = input("Enter Payment Method: ")
    print("Some Recommended Products for customer ",customer_id)
    print("===========================================")
    print()
    ProductRecommendationService.recommend_products_for_customer(customer_id)

    order = Order(order_id, customer_id, payment_method)
    while True:
        product_id = int(input("Enter Product ID (or 0 to finish): "))

        if product_id == 0:
            break

        # getting  product details including current quantity,id and expiry_date
        product_info = DBConnection.fetch_one(
            f"SELECT product_id, quantity,expiry_date FROM {SCHEMA_NAME}.{PRODUCTS_TABLE} WHERE product_id = %s",
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

    fetch_query = f"""
      SELECT product_id, name, quantity
      FROM {SCHEMA_NAME}.{PRODUCTS_TABLE}
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
        DBConnection.close()
        print("Authentication failed.")


if __name__ == "__main__":
    main()

from datetime import datetime
from itertools import product
from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from database_conn.db_connection import DBConnection
from sales import Sale
from transactions import Transaction


class Order:
    def __init__(self, order_id, customer_id, product_id, quantity, discount_per, payment_method):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.discount_per = discount_per
        self.payment_method = payment_method

        # Initialize other attributes with default values
        self.price = None
        self.cost_price = None
        self.sell_price = None
        self.total_amount = None
        self.final_amount = None
        self.discount_amt = None
        self.available_quantity = None
        self.expiry_date = None
        self.customer_name=None
        self.product_name=None

        self.customer_name= DBConnection.fetch_one("select name from shopdb.customers where customer_id=%s",(self.customer_id,))
        self.product_name=DBConnection.fetch_one("select name from shopdb.products where product_id=%s",(self.product_id,))
    def fetch_product_details(self):
        print("Inside fetch ",self.product_id)
        query = "SELECT price, cost_price, quantity, expiry_date FROM shopdb.products WHERE product_id = %s"
        result = DBConnection.fetch_one(query, (self.product_id,))
        # print(type(result),"type of result")
        # print("The result is ",result)
        if result:
            self.price, self.cost_price, self.available_quantity, self.expiry_date = result
            print(f"Fetched details for product {self.product_id}: Price = {self.price}, Cost Price = {self.cost_price}, Quantity = {self.available_quantity}, Expiry Date = {self.expiry_date}")
            self.check_availability()
            self.check_expiry()
        else:
            print("Product not found")
            return

    @staticmethod
    def remove_expired_products():
        query = """
           DELETE FROM shopdb.products
           WHERE expiry_date < %s
           """
        params = (datetime.now().date(),)
        DBConnection.execute_query(query, params)
        print("Expired products have been removed from the inventory.")

    def check_availability(self):
        if self.quantity > self.available_quantity:
           print("Insufficient stock available")
           return

    def check_expiry(self):
       if self.expiry_date is  None:
         return
       current_date = datetime.now().date()
       if self.expiry_date < current_date:
            print("Product is expired")
            return

    def calculate_totals(self):
            discount_per_product=(self.price * Decimal(self.discount_per)) / Decimal('100.00')
            self.discount_amt = discount_per_product *Decimal(self.quantity) #  all are Decimal
            self.sell_price = self.price - discount_per_product
            self.total_amount = self.price*self.quantity # con quantity to Decimal
            self.final_amount = self.total_amount-self.discount_amt
            print("The discount amt is",self.discount_amt)

    def generate_pdf_bill(self, path=None):
        if path is None:
            path = os.getcwd()  # Default to the current working directory

        pdf_filename = os.path.join(path, f"{self.order_id}_bill.pdf")
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter

        # Add heading
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "XYZ Shop")

        # Add order details
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Order ID: {self.order_id}")

        c.drawString(50, height - 100, f"Customer Name: {self.customer_name}")
        c.drawString(50, height - 120, f"Product Name: {self.product_name}")
        c.drawString(50, height - 140, f"Quantity: {self.quantity}")
        c.drawString(50, height - 160, f"Price per Unit: ${self.price:.2f}")
        c.drawString(50, height - 180, f"Discount Percentage: {self.discount_per:.2f}%")
        c.drawString(50, height - 200, f"Discount Amount: ${self.discount_amt:.2f}")
        c.drawString(50, height - 220, f"Sell Price: ${self.sell_price:.2f}")
        c.drawString(50, height - 240, f"Total Amount: ${self.total_amount:.2f}")
        c.drawString(50, height - 260, f"Final Amount: ${self.final_amount:.2f}")
        c.drawString(50, height - 280, f"Payment Method: {self.payment_method}")

        c.save()
        print(f"PDF bill generated: {pdf_filename}")
    def create_order(self):
        # Fetch product details before creating an order
        self.fetch_product_details()
        #  Remove expired products
        self.remove_expired_products()
        # Calculate totals
        self.calculate_totals()

        # Check if the order can be created

        if self.quantity <= self.available_quantity:
            query = """
            INSERT INTO shopdb.orders (
                order_id, customer_id, order_date, product_id, price, sell_price, quantity,
                discount_per, discount_amt, total_amount, final_amount, payment_method
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.order_id, self.customer_id, datetime.now().date(), self.product_id, self.price, self.sell_price,
                self.quantity, self.discount_per, self.discount_amt, self.total_amount,
                self.final_amount, self.payment_method)

            DBConnection.execute_query(query, params)

            # Update product quantity in inventory
            self.update_product_quantity()

        else:
            print("Order could not be created due to product issues.")

    def update_product_quantity(self):
        query = """
        UPDATE shopdb.products
        SET quantity = quantity - %s
        WHERE product_id = %s
        """
        params = (self.quantity, self.product_id)
        DBConnection.execute_query(query, params)



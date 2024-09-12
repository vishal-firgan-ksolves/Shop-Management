from datetime import datetime
from decimal import Decimal
from functools import total_ordering
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
import os
from database_conn.db_connection import DBConnection
from sales import Sale
from transactions import Transaction

class Order:
    def __init__(self, order_id, customer_id, payment_method):
        self.order_id = order_id
        self.customer_id = customer_id
        self.payment_method = payment_method
        self.order_date = datetime.now().date()
        self.details = []  # List to store product details as dicts
        self.total_amount = Decimal('0.00')
        self.discount_amt = Decimal('0.00')
        self.final_amount = Decimal('0.00')

    def add_product(self, product_id, quantity, discount_per):
        self.details.append({
            'product_id': product_id,
            'quantity': quantity,
            'discount_per': discount_per
        })

    def fetch_product_details(self, product_id):
        query = "SELECT price, price, quantity, expiry_date FROM shopdb.products WHERE product_id = %s"
        result = DBConnection.fetch_one(query, (product_id,))
        if result:
         return result
        else:
           print("product not found!")

    def fetch_product_name(self, product_id):
        query = "SELECT name,price FROM shopdb.products WHERE product_id = %s"
        result = DBConnection.fetch_one(query, (product_id,))
        if result:
            print("Found the product.....")
            return result[0],result[1]  #  getting product name from the result tuple
        else:
            print("Unable to find the product")
            print(f"Product ID {product_id} not found.")
            return 'Unknown'

    def calculate_totals(self):
        for detail in self.details:
            result = self.fetch_product_details(detail['product_id'])
            if result is None:
                print(f"Product ID {detail['product_id']} not found.")
                continue

            price, cost_price, available_quantity, expiry_date = result
            if price is None:
                print(f"Product ID {detail['product_id']} not found.")
                continue

            discount_per_product = (price * Decimal(detail['discount_per'])) / Decimal('100.00')
            detail['discount_amt'] = discount_per_product * Decimal(detail['quantity'])
            detail['sell_price'] = price - discount_per_product
            detail['total_amount'] = price * Decimal(detail['quantity'])
            detail['final_amount'] = detail['total_amount'] - detail['discount_amt']
            detail['cost_price'] = cost_price  # Ensure this key is set

            self.total_amount += detail['total_amount']
            self.discount_amt += detail['discount_amt']
            self.final_amount += detail['final_amount']

    def create_order(self):
        self.calculate_totals()

        # Insert into orders table
        query = """
        INSERT INTO shopdb.orders (
            order_id, customer_id, order_date, payment_method, total_amount, discount_amt, final_amount
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.order_id, self.customer_id, self.order_date, self.payment_method,
            self.total_amount, self.discount_amt, self.final_amount
        )
        DBConnection.execute_query(query, params)

        # Insert into order_details table and create sales records
        for detail in self.details:
            result = self.fetch_product_details(detail['product_id'])
            if result is None:
                print(f"Product ID {detail['product_id']} not found.")
                continue

            price, cost_price, _, _ = result
            product_name = self.fetch_product_name(detail['product_id'])[0]

            # Insert into order_details table
            query = """
            INSERT INTO shopdb.order_details (
                order_id, product_id, product_name, quantity, price, sell_price, discount_per_unit
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.order_id, detail['product_id'], product_name, detail['quantity'],
                cost_price, detail['sell_price'], detail['discount_per']
            )
            DBConnection.execute_query(query, params)

            # Record the sale details
            sale = Sale(
                sale_id=f"SL{self.order_id[2:]}_{detail['product_id']}",  # Ensure unique sale_id
                order_id=self.order_id,
                product_id=detail['product_id'],
                quantity=detail['quantity'],
                total_amount=detail['total_amount'],
                discount_amt=detail['discount_amt'],
                cost_price=detail['cost_price'],
                sell_price=detail['sell_price'],
                final_amount=detail['final_amount']
            )
            sale.create_sale()

            # Update product quantity
            self.update_product_quantity(detail['product_id'], detail['quantity'])

        # Record the transaction
        transaction = Transaction(
            transaction_id=f"TR{self.order_id[2:]}",
            amount=self.total_amount,
            discount_amt=self.discount_amt,
            transaction_type='sell',
            order_id=self.order_id,
            customer_id=self.customer_id,
            payment_method=self.payment_method,
            final_amount=self.final_amount
        )
        transaction.create_transaction()

    def update_product_quantity(self, product_id, quantity):
        query = """
        UPDATE shopdb.products
        SET quantity = quantity - %s
        WHERE product_id = %s
        """
        params = (quantity, product_id)
        DBConnection.execute_query(query, params)

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

    def generate_pdf_bill(self, path=None):
        if path is None:
            path = os.getcwd()  # Default to the current working directory

        pdf_filename = os.path.join(path, f"{self.order_id}_bill.pdf")
        margin = 0.5 * inch  # Set margin size
        document = SimpleDocTemplate(
            pdf_filename,
            pagesize=letter,
            leftMargin=margin,
            rightMargin=margin,
            topMargin=margin,
            bottomMargin=margin
        )
        content = []

        # Define styles with text wrapping
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        heading_style = styles['Title']
        normal_style.alignment = 1  # Center alignment for headings

        # Add heading
        heading = Paragraph("XYZ Shop", heading_style)
        content.append(heading)

        # Add order details
        order_details = [
            ["Order ID:", self.order_id],
            ["Customer ID:", self.customer_id],
            ["Payment Method:", self.payment_method],
            ["Order Date:", self.order_date.strftime("%Y-%m-%d")]
        ]
        order_details_table = Table(order_details, colWidths=[2 * inch, 4 * inch])
        order_details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        content.append(order_details_table)

        # Add product details
        product_headers = ["Product ID", "Product Name", "Quantity","Price", "Sell Price", "Discount %",
                            "Total Amount","Discount Amount", "Final Amount"]
        product_rows = []
        for detail in self.details:
            product_name,price = self.fetch_product_name(detail['product_id'])
            product_row = [
                detail['product_id'],
                Paragraph(product_name, normal_style),
                detail['quantity'],
                f"{price:2f}",
                f"{detail['sell_price']:.2f}",
                f"{detail['discount_per']:.2f}%",
                f"{detail['total_amount']:.2f}",
                f"{detail['discount_amt']:.2f}",
                f"{detail['final_amount']:.2f}"
            ]
            product_rows.append(product_row)

        product_table = Table([product_headers] + product_rows, colWidths=[1 * inch] * 9)
        product_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        content.append(product_table)
        content.append(Paragraph("", normal_style))  # Add an empty paragraph to create space
        content.append(Paragraph("", normal_style))
        # Add summary details
        summary_data = [
            ["Gross Total", f"Rs. {self.total_amount:.2f}"],
            ["Discount", f"Rs. {self.discount_amt:.2f}"],
            ["Subtotal after Discount", f"Rs. {self.final_amount:.2f}"],
            ["Net Total", f"Rs. {self.final_amount:.2f}"]
        ]
        summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        content.append(summary_table)

        # Build the PDF
        document.build(content)
        print(f"PDF bill generated: {pdf_filename}")



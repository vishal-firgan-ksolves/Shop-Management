from datetime import datetime
from decimal import Decimal
from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME, SALES_TABLE


class Sale:
    def __init__(self, sale_id, order_id, product_id, quantity, total_amount, discount_amt, cost_price, sell_price, final_amount):
        self.sale_id = sale_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_amount = total_amount
        self.discount_amt = discount_amt
        self.cost_price = cost_price
        self.sell_price = sell_price
        self.final_amount = final_amount
        self.date = datetime.now().date()  # Current date

    def create_sale(self):
        query = f"""
        INSERT INTO {SCHEMA_NAME}.{SALES_TABLE} (
            sale_id, order_id, product_id, quantity, total_amount, discount_amt, price, sell_price, final_amount, sale_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.sale_id, self.order_id, self.product_id, self.quantity, self.total_amount, self.discount_amt,
            self.cost_price, self.sell_price, self.final_amount, self.date
        )
        try:
            DBConnection.execute_query(query, params)
            print(f"Sale {self.sale_id} recorded successfully.")
        except Exception as e:
            print(f"Error recording sale {self.sale_id}: {e}")
            # Optionally, you could also log this error or handle it in a way that suits your needs

# Example usage
if __name__ == "__main__":
    sale = Sale(
        sale_id="SL12345",
        order_id="OR12345",
        product_id=1,
        quantity=2,
        total_amount=Decimal('200.00'),
        discount_amt=Decimal('20.00'),
        cost_price=Decimal('150.00'),
        sell_price=Decimal('180.00'),
        final_amount=Decimal('180.00')
    )
    sale.create_sale()

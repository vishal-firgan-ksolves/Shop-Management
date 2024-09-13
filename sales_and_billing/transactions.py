from datetime import datetime
from decimal import Decimal
from database_conn.db_connection import DBConnection
from constants.constants import SCHEMA_NAME,TRANSACTION_TABLE
class Transaction:
    def __init__(self, transaction_id, amount, discount_amt, transaction_type, order_id, customer_id, payment_method, final_amount):
        self.transaction_id = transaction_id
        self.amount = amount
        self.discount_amt = discount_amt
        self.transaction_type = transaction_type
        self.order_id = order_id
        self.customer_id = customer_id
        self.payment_method = payment_method
        self.final_amount = final_amount
        self.timestamp = datetime.now()  # Current timestamp

    def create_transaction(self):
        query = f"""
        INSERT INTO {SCHEMA_NAME}.{TRANSACTION_TABLE} (
            transaction_id, amount, discount_amt, transaction_type, order_id, customer_id, payment_method, final_amount, transaction_timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.transaction_id, self.amount, self.discount_amt, self.transaction_type, self.order_id,
            self.customer_id, self.payment_method, self.final_amount, self.timestamp
        )
        DBConnection.execute_query(query, params)
        print(f"Transaction {self.transaction_id} created successfully.")

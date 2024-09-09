from database_conn.db_connection import DBConnection

class Transaction:
    def __init__(self, transaction_id, amount, discount_amt, trans_type, order_id, customer_id, payment_method,final_amount):
        self.transaction_id = transaction_id
        self.amount = amount
        self.discount_amt = discount_amt
        self.trans_type = trans_type
        self.final_amount=final_amount
        self.order_id = order_id
        self.customer_id = customer_id
        self.payment_method = payment_method

    def create_transaction(self):
        query = """
        INSERT INTO shopdb.transactions (
            transaction_id, total_amount, discount_amt,final_amount, type, order_id, customer_id, payment_method
        ) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        params = (
            self.transaction_id, self.amount, self.discount_amt,self.final_amount, self.trans_type,
            self.order_id, self.customer_id, self.payment_method
        )
        DBConnection.execute_query(query, params)
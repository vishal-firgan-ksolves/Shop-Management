from database_conn.db_connection import DBConnection

class Sale:
    def __init__(self, sale_id, order_id, quantity, total_amount, discount_amount, cost_price, sell_price,final_amt):
        self.sale_id = sale_id
        self.order_id = order_id
        self.quantity = quantity
        self.final_amt=final_amt
        self.total_amount = total_amount
        self.discount_amount = discount_amount
        self.cost_price = cost_price
        self.sell_price = sell_price
        self.profit_loss = (sell_price - cost_price) * quantity

    def create_sale(self):
        query = """
        INSERT INTO shopdb.sales (
            sale_id, order_id, quantity, total_amount, discount_amount,final_amount, cost_price, sell_price, profit_loss
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        params = (
            self.sale_id, self.order_id, self.quantity, self.total_amount,
            self.discount_amount,self.final_amt, self.cost_price, self.sell_price, self.profit_loss
        )
        DBConnection.execute_query(query, params)

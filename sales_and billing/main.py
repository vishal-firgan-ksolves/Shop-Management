from database_conn.db_connection import DBConnection
from orders import Order
from transactions import Transaction
from sales import Sale

def main():
    while True:
        print("\n1. Create Order")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            o_id = input("Enter Order ID: ")
            order_id = "OR" + o_id
            customer_id = int(input("Enter Customer ID: "))
            product_id = int(input("Enter Product ID: "))
            quantity = int(input("Enter Quantity: "))
            discount_per = float(input("Enter Discount Percentage: "))
            payment_method = input("Enter Payment Method: ")

            # Create order
            order = Order(order_id, customer_id, product_id, quantity, discount_per, payment_method)
            order.create_order()
            order.generate_pdf_bill()
            #  after order  corresponding transaction and sale entries
            transaction_id = "TR" + order.order_id[2:]  # Generate transaction_id, this is just an example
            transaction = Transaction(transaction_id, order.total_amount, order.discount_amt, 'sell', order.order_id, customer_id, payment_method,order.final_amount)
            transaction.create_transaction()

            sale_id = "SL" + order.order_id[2:]  # Generate sale_id, this is just an example
            sale = Sale(sale_id, order.order_id, quantity, order.total_amount, order.discount_amt, order.cost_price, order.sell_price,order.final_amount)
            sale.create_sale()

        elif choice=='0':
            DBConnection.close()
            break


if __name__ == "__main__":
    main()
from database_conn.db_connection import DBConnection


class Filter:
    def __init__(self, sort_order):

        self.sort_order = sort_order.lower()

    def filter_by_price(self):

        if self.sort_order not in ['low_to_high', 'high_to_low']:
            print("Invalid  order. Enter 'low_to_high' or 'high_to_low'.")
            return

        # Determine the sort direction for SQL query
        sort_direction = 'ASC' if self.sort_order == 'low_to_high' else 'DESC'

        query = f"""SELECT product_id, name, quantity, price 
                    FROM shopdb.products 
                    ORDER BY price {sort_direction}"""

        result = DBConnection.fetch_all(query)

        if result:
            print(f"\nProducts sorted by price in ({self.sort_order} order:")
            for row in result:
                db_p_id = row[0]
                db_name = row[1]
                db_quantity = row[2]
                db_price = row[3]

                print(f"Product ID: {db_p_id}")
                print(f"Name: {db_name}")
                print(f"Quantity: {db_quantity}")
                print(f"Price: ${db_price:.2f}")
                print("-" * 30)
        else:
            print("No products found.")


# if __name__ == '__main__':
#     sort_order = input("Enter sort order ('low_to_high' or 'high_to_low'): ").strip()
#     filter = Filter(sort_order)
#     filter.filter_by_price()

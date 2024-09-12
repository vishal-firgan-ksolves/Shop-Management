from datetime import datetime
from decimal import Decimal
from database_conn.db_connection import DBConnection
from security.user import User

class ProfitLossStatement:
    def __init__(self):
        pass

    def fetch_revenue(self, start_date, end_date):
        query = """
        SELECT
            SUM(final_amount) AS total_revenue
        FROM
            shopdb.sales
        WHERE
            sale_date BETWEEN %s AND %s;
        """
        # Fetch result and ensure it's a Decimal, default to 0.0
        result = DBConnection.fetch_one(query, (start_date, end_date))
        return result[0] if result and result[0] is not None else Decimal('0.0')

    def fetch_cogs(self, start_date, end_date):
        query = """
        SELECT
            SUM(p.cost_price * s.quantity) AS total_cogs
        FROM
            shopdb.sales s
        JOIN
            shopdb.products p
        ON
            s.product_id = p.product_id
        WHERE
            s.sale_date BETWEEN %s AND %s;
        """
        # Fetch result and ensure it's a Decimal, default to 0.0
        result = DBConnection.fetch_one(query, (start_date, end_date))
        return result[0] if result and result[0] is not None else Decimal('0.0')

    def get_operational_expenses(self):
        #  taking input from user for operational expenses
        try:
            rent = float(input("Enter total rent expense: "))
            wages = float(input("Enter total wages expense: "))
            utilities = float(input("Enter total utilities expense: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return self.get_operational_expenses()

        return float(rent + wages + utilities)

    def generate_p_and_l_statement(self):
        # Define the time period for the P&L statement
        start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')  #start of current month
        end_date = datetime.now().strftime('%Y-%m-%d')

        revenue = self.fetch_revenue(start_date, end_date)
        cogs = self.fetch_cogs(start_date, end_date)
        operational_expenses = self.get_operational_expenses()

        # Ensure consistency in types
        gross_profit = float(revenue) - float(cogs)
        net_profit = gross_profit - operational_expenses

        print(f"\nProfit & Loss Statement for {datetime.now().strftime('%B %Y')}")
        print(f"Total Revenue: {revenue:.2f}")
        print(f"Total COGS: {cogs:.2f}")
        print(f"Gross Profit: {gross_profit:.2f}")
        print(f"Total Operational Expenses: {operational_expenses:.2f}")
        print(f"Net Profit: {net_profit:.2f}")
        print(DBConnection.fetch_one("select current_date"),">>>>>>>>>>>>>>")

if __name__ == "__main__":
    username = input("Enter  username: ")
    password = input("Enter  password: ")

    if User.authenticate_user(username, password):
        if User.authorize_user(username, 'admin'):
            print("Admin authenticated successfully.")
            pnl_generator = ProfitLossStatement()
            pnl_generator.generate_p_and_l_statement()
        else:
            print("User does not have admin role.")
    else:
        print("Authentication failed.")


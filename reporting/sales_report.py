from datetime import datetime, timedelta
from database_conn.db_connection import DBConnection
from security.user import User

class SalesReport:
    def __init__(self):
       pass

    def generate_daily_report(self):
        query = """
    SELECT
    sale_date AS period,
    COUNT( order_id) AS total_sales,
    SUM(final_amount) AS total_revenue,
    SUM(final_amount) - SUM(p.cost_price * s.quantity) AS total_profit
     FROM
    shopdb.sales s
    join shopdb.products p 
    on s.product_id =p.product_id 
     WHERE
    sale_date = CURRENT_DATE
     GROUP BY
    sale_date;
        """
        return DBConnection.fetch_all(query)

    def generate_weekly_report(self):
        start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        end_date = datetime.now()

        query = """
         SELECT
        date_trunc('week', s.sale_date) AS period,
        COUNT(s.order_id) AS total_sales,
        SUM(s.final_amount) AS total_revenue,
        SUM(s.final_amount) - SUM(p.cost_price * s.quantity) AS total_profit
          FROM
        shopdb.sales s
        JOIN shopdb.products p 
        ON s.product_id = p.product_id
          WHERE
        s.sale_date >= date_trunc('week', CURRENT_DATE) 
          GROUP BY
        date_trunc('week', s.sale_date); """
        return DBConnection.fetch_all(query, (start_date, end_date))

    def generate_monthly_report(self):
        start_date = datetime.now().replace(day=1)
        end_date = datetime.now()

        query = """
          SELECT
        date_trunc('month', s.sale_date) AS period,
        COUNT(s.order_id) AS total_sales,
        SUM(s.final_amount) AS total_revenue,
        SUM(s.final_amount) - SUM(p.cost_price * s.quantity) AS total_profit
          FROM
        shopdb.sales s
          JOIN 
        shopdb.products p 
        ON s.product_id = p.product_id
           WHERE
        s.sale_date >= date_trunc('month', CURRENT_DATE)
         GROUP BY
        date_trunc('month', s.sale_date);
        """
        return DBConnection.fetch_all(query, (start_date, end_date))

    def print_report(self, title, data):
        print(f"\n{title}")
        print("=" * len(title))
        for row in data:
            print(f"Day: {row[0]}")
            print(f"Total Sales: {row[1]}")
            print(f"Total Revenue: {row[2]:.2f}")
            print(f"Total Profit: {row[3]:.2f}")
            print()

    def generate_reports(self):
        # daily report
        daily_data = self.generate_daily_report()
        self.print_report("Daily Sales Report", daily_data)

        # weekly report
        weekly_data = self.generate_weekly_report()
        self.print_report("Weekly Sales Report", weekly_data)

        # monthly report
        monthly_data = self.generate_monthly_report()
        self.print_report("Monthly Sales Report", monthly_data)

if __name__ == "__main__":

    username = input("Enter  username: ")
    password = input("Enter  password: ")

    if User.authenticate_user(username, password):
        if User.authorize_user(username, 'admin'):
            print("Admin authenticated successfully.")
            report_generator = SalesReport()
            report_generator.generate_reports()
        else:
            print("User does not have admin role.")
    else:
        print("Authentication failed.")





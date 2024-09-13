from constants.constants import CUSTOMERS_TABLE,SCHEMA_NAME
from database_conn.db_connection import DBConnection

class Customer:
    def __init__(self):
        pass

    @staticmethod
    def create_customer(name,contact_no,email,address):
        query=f"""insert into {SCHEMA_NAME}.{CUSTOMERS_TABLE}
        (name,contact_no,email,address) values (%s,%s,%s,%s);
             """
        DBConnection.execute_query(query, (name, contact_no, email, address))
        print("Created Customer Successfully")
    @staticmethod
    def get_customer(id):
        query=f"""select * from  {SCHEMA_NAME}.{CUSTOMERS_TABLE}
        where customer_id=%s;
             """
        return  DBConnection.fetch_one(query,(id,))
    @staticmethod
    def view_all_customers():
        query = f"""select * from  {SCHEMA_NAME}.{CUSTOMERS_TABLE}; """
        print("Here are all customers: ")
        print()
        return DBConnection.fetch_all(query)
    @staticmethod
    def delete_customer(id):
        query = f"""delete  from  {SCHEMA_NAME}.{CUSTOMERS_TABLE}
                where customer_id=%s; """
        print("Customer deleted successfully")
        DBConnection.execute_query(query,(id,))
    @staticmethod
    def get_customer_by_name(name):
        query = f"""select * from  {SCHEMA_NAME}.{CUSTOMERS_TABLE}
                where name=%s;  """
        print("Here is customer:")
        return DBConnection.fetch_one(query, (name,))


if __name__ == '__main__':

   # Customer.create_customer("sachin kumar",123321123,'rohit@gmail.com','pune')
   # c= Customer.get_customer(100002)
   # print(c)
   # c=Customer.get_customer_by_name("sachin kumar")
   # print(c)
   # cs=Customer.view_all_customers()
   # for row in cs:
   #     print(row)
   # Customer.delete_customer(3)
   DBConnection.close()


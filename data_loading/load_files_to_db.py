import zipfile
import os
import pandas as pd
import psycopg2
from concurrent.futures import ThreadPoolExecutor
from database_conn.db_connection import DBConnection
from psycopg2 import connect

# from database_conn.db_connection import DBConnection

class ZipExtractor:
    def __init__(self, zip_path, extract_to):
        self.zip_path = zip_path
        self.extract_to = extract_to

    def extract(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_to)
        print(f"Extracted {self.zip_path} to path: {self.extract_to} ")

class DatabaseHandler:
    def __init__(self):
        self.conn=DBConnection.get_connection()
        self.cur=DBConnection.get_cursor()

    def load_csv(self, file_path):
        try:
            # reading csv file into DataFrame of pandas
            df = pd.read_csv(file_path)
            # Insert data into db
            for index, row in df.iterrows():
                self.cur.execute('''
                    INSERT INTO shopdb.products (product_id, name, category, price, quantity, expiry_date, supplier_id, cost_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ''', (row['product_id'], row['name'], row['category'], row['price'], row['quantity'],
                      row['expiry_date'] if pd.notna(row['expiry_date']) else None, row['supplier_id'],
                      row['cost_price']))
            # commit transaction
            self.conn.commit()
            print(f"Successfully added data to db")
        except Exception as e:
            print(f"Error while adding data: {e}")
        finally:
            self.close()

    def delete_product(self,id):
        query="delete from shopdb.products where product_id=%s"
        try:
          self.cur.execute(query,(id,))
          self.conn.commit()
          DBConnection.close()
          print("Product deleted successfully.")
        except Exception as e:
            print(f"Error while deleting {e}")
            self.conn.rollback()

    def update_product(self, product_id=None, name=None, category=None, price=None, quantity=None, expiry_date=None,
                       supplier_id=None, cost_price=None):
        query = "update shopdb.products set "
        # list to store the set clauses
        set_clauses = []
        # list to store the values for the query
        values = []
        # appending clauses and values based on which parameters
        if name is not None:
            set_clauses.append("name = %s")
            values.append(name)
        if category is not None:
            set_clauses.append("category = %s")
            values.append(category)
        if price is not None:
            set_clauses.append("price = %s")
            values.append(price)
        if quantity is not None:
            set_clauses.append("quantity = %s")
            values.append(quantity)
        if expiry_date is not None:
            set_clauses.append("expiry_date = %s")
            values.append(expiry_date)
        if supplier_id is not None:
            set_clauses.append("supplier_id = %s")
            values.append(supplier_id)
        if cost_price is not None:
            set_clauses.append("cost_price = %s")
            values.append(cost_price)
        # If no columns to update, return early
        if not set_clauses:
            print("No fields to update.")
            return

        # joining set clauses
        query += ", ".join(set_clauses) + " WHERE product_id = %s"
        values.append(product_id)
        try:
            self.cur.execute(query, values)
            self.conn.commit()
            print("Product updated successfully.")
        except Exception as e:
            print(f"Error while updating product: {e}")

class DataPipelineZip:
    def __init__(self, zip_path, extract_to):
        self.zip_path = zip_path
        self.extract_to = extract_to
        self.conn=DBConnection.get_connection()
        self.cursor=DBConnection.get_cursor()

    def run(self):
        # Extract ZIP file
        zip_handler = ZipExtractor(self.zip_path, self.extract_to)
        zip_handler.extract()

        # Get list of CSV data_loading
        # csv_files = [os.path.join(self.extract_to, file) for file in os.listdir(self.extract_to) if
        #              file.endswith('.csv')]
        csv_files = []
        for file in os.listdir(self.extract_to):
            if file.endswith('.csv'):
                full_path = os.path.join(self.extract_to, file)
                csv_files.append(full_path)
        # Load csv data_loading into db using multithreading
        with ThreadPoolExecutor(max_workers=3) as executor:
            loader = DatabaseHandler()
            executor.map(loader.load_csv, csv_files)

class DataPinelineFolder:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.conn = DBConnection.get_connection()
        self.cursor=DBConnection.get_cursor()

    def run(self):
        # getting all the data_loading from the folder
        csv_files = os.listdir(self.folder_path)
        # filtering only csv data_loading
        csv_files = [os.path.join(self.folder_path, file) for file in csv_files if file.endswith('.csv')]

        with ThreadPoolExecutor(max_workers=3) as executor:
            loader = DatabaseHandler()
            executor.map(loader.load_csv, csv_files)



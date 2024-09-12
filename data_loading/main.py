from security.user import User

from load_files_to_db import DatabaseHandler,DataPipelineZip,DataPinelineFolder
from database_conn.db_connection import DBConnection
if __name__ == '__main__':
    # paths
    username=input("Enter admin/emp username: ")
    password=input("Enter admin/emp password: ")

    is_valid=User.authenticate_user(username, password)

    if is_valid:
        zip_file_path = '/home/vishalks1122/Documents/product_data.zip'
        extraction_dir = '/home/vishalks1122/Documents/extracted_csvs'
        folder_path='/home/vishalks1122/new_product_files'

      # loading data from zip
      #   pipelinezip = DataPipelineZip(zip_file_path, extraction_dir)
      #   pipelinezip.run()

      # loading data from folder
      #   pipelinefolder = DataPinelineFolder(folder_path)
      #   pipelinefolder.run()

      # deleting and updating

        role=User.get_role(username)

        if role=='admin':
          flag=input("Want to update the product? y/n: ")
          obj = DatabaseHandler()
          if flag.lower()=='y':
             obj.update_product(18, quantity=80)

          flag=input("Want to delete product? y/n: ")
          if flag.lower()=='y':
             did=int(input("Enter id of product to delete:") )
             obj.delete_product(did)

    else:
     print("User is not authenticated. Wrong username or password entered!")
DBConnection.close()




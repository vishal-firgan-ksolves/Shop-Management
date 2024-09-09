

from load_files_to_db import DatabaseHandler,DataPipelineZip,DataPinelineFolder
from database_conn.db_connection import DBConnection
if __name__ == '__main__':
    # paths
    zip_file_path = '/home/vishalks1122/Documents/product_data.zip'
    extraction_dir = '/home/vishalks1122/Documents/extracted_csvs'
    folder_path='/home/vishalks1122/new_product_files'

    # loading data from zip
    # pipelinezip = DataPipelineZip(zip_file_path, extraction_dir)
    # pipelinezip.run()

    # loading data from folder
    # pipelinefolder = DataPinelineFolder(folder_path)
    # pipelinefolder.run()

    # deleting and updating
    obj= DatabaseHandler()
    # obj.update_product(14,"Fridge",price=500)
    # obj.delete_product(14)

    DBConnection.close()




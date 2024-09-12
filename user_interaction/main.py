from security.user import User
from filter_products import Filter
from product_search import Search

if __name__ == '__main__':
    username = input("Enter  username: ")
    password = input("Enter  password: ")

    if User.authenticate_user(username, password):
        print("User authenticated successfully.")
        print("Make your choise: ")
        while(True):
            choise = input("1.Filter \n  2.Search \n  3.Exit \n : ")
            if choise == '1':
                sort_order = input("Enter sort order ('low_to_high' or 'high_to_low'): ").strip()
                filter = Filter(sort_order)
                filter.filter_by_price()
                continue
            elif choise=='2':
                way=input("In which way want to search name/category/supplier : \n").lower()
                if way=='name':
                    search_string = input("Enter name of product you want to search for: ").lower()
                    Search.search_by_name(search_string)
                elif way=='category':
                    search_category = input("Enter category of products: ").lower()
                    Search.search_by_category(search_category)
                elif way=='supplier':
                    search_supplier = input("Enter supplier name: ").lower()
                    Search.search_by_supplier(search_supplier)
                else:
                    print("Try Again!")
                    continue
            elif choise=='3':
                break
    else:
        print("Authentication failed.")



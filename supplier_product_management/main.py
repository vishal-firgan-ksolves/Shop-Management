from suppliers import Suppliers
from database_conn.db_connection import DBConnection
from order_from_supplier import PurchaseOrders,Products

def menu():
    while True:
        print("1. Manage Suppliers")
        print("2. Manage Purchase Orders")
        print("3. Manage Products")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("1. Create Supplier")
            print("2. Delete Supplier")
            supplier_choice = input("Enter your choice: ")

            if supplier_choice == '1':
                name = input("Enter name of supp: ")
                contact_no = input("Enter contanct number of supp: ")
                email = input("Enter email o supp: ")
                address = input("Enter address of supp: ")
                Suppliers.create_supplier(name, contact_no, email, address)
            elif supplier_choice == '2':
                supplier_id = int(input("Enter the supplier ID to delete: "))
                Suppliers.delete_supplier(supplier_id)
            else:
                print("Invalid choice.")

        elif choice == '2':
             print("1. Create Order")
             print("2.  Delete Order")
             print("3. View Order")
             print("4. View All Orders")
             order_choice = input("Enter your choice: ")

             if order_choice == '1':
                supplier_id = int(input("Enter supplier ID: "))
                items = []
                while True:
                    product_id = int(input("Enter product ID (0 to finish): "))
                    if product_id == 0:
                        break
                    quantity = int(input("Enter quantity: "))
                    # items.append((product_id, quantity))
                    PurchaseOrders.create_order(supplier_id,product_id,quantity)


             elif order_choice == '2':
                order_id = int(input("Enter the order ID to delete: "))
                PurchaseOrders.delete_order(order_id)


             elif order_choice == '3':
                order_id = int(input("Enter the order ID to view: "))
                order = PurchaseOrders.fetch_order(order_id)
                print(order)

             elif order_choice == '4':
                orders = PurchaseOrders.fetch_all_orders()
                # (2, 103, datetime.date(2024, 9, 12), 15, 10, Decimal('1100.00'))
                # (3, 103, datetime.date(2024, 9, 12), 15, 128, Decimal('14080.00'))
                for order in orders:
                    # print(order)
                    print(f"Order_id:{order[0]}| sup_id: {order[1]} | order_date:{order[2]} | product_id:{order[3]} | quantity_ordered: {order[4]} | total_amount: {order[5]}")


             else:
                print("Invalid choice.")

        elif choice == '3':
             print("1. Create Product")
             print("2. Update Product")
             print("3. Delete Product")
             print("4. View Product")
             print("5. View All Products")
             product_choice = input("Enter your choice: ")

             if product_choice == '1':
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                cost_price = float(input("Enter product cost price: "))
                supplier_id = int(input("Enter supplier ID: "))
                quantity = int(input("Enter initial quantity: "))
                Products.create_product(name, price, cost_price, supplier_id, quantity)

             elif product_choice == '2':
                product_id = int(input("Enter product ID to update: "))
                name = input("Enter new name (or press Enter to skip): ")
                price = input("Enter new price (or press Enter to skip): ")
                cost_price = input("Enter new cost price (or press Enter to skip): ")
                supplier_id = input("Enter new supplier ID (or press Enter to skip): ")
                quantity = input("Enter new quantity (or press Enter to skip): ")
                Products.update_product(
                    product_id,
                    name=name if name else None,
                    price=float(price) if price else None,
                    cost_price=float(cost_price) if cost_price else None,
                    supplier_id=int(supplier_id) if supplier_id else None,
                    quantity=int(quantity) if quantity else None
                )

             elif product_choice == '3':
                product_id = int(input("Enter product ID to delete: "))
                Products.delete_product(product_id)

             elif product_choice == '4':
                product_id = int(input("Enter product ID to view: "))
                product = Products.fetch_product(product_id)
                print(product)

             elif product_choice == '5':
                products = Products.fetch_all_products()
                for product in products:
                    print(product)
             else:
                print("Invalid choice.")

        elif choice == '4':
          print("Exiting...")
          break
        else:
          print("Invalid choice. Please enter a valid number.")

if __name__ == "__main__":
    DBConnection.get_connection()

    try:
        is_valid = Suppliers.authenticate_admin()

        if is_valid:
            # while True:
            #     print("1. Manage Suppliers")
            #     print("2. Manage Purchase Orders")
            #     print("3. Manage Products")
            #     print("4. Exit")
            #     choice = input("Enter your choice: ")
            #
            #     if choice == '1':
            #         print("1. Create Supplier")
            #         print("2. Delete Supplier")
            #         supplier_choice = input("Enter your choice: ")
            #
            #         if supplier_choice == '1':
            #             Suppliers.create_supplier('Supplier D', '1200567000', 'contact@supplierd.com', 'Pune')
            #         elif supplier_choice == '2':
            #             supplier_id = int(input("Enter the supplier ID to delete: "))
            #             Suppliers.delete_supplier(supplier_id)
            #         else:
            #             print("Invalid choice.")
            #
            #     elif choice == '2':
            #         print("1. Create Order")
            #         print("2. Update Order")
            #         print("3. Delete Order")
            #         print("4. View Order")
            #         print("5. View All Orders")
            #         order_choice = input("Enter your choice: ")
            #
            #         if order_choice == '1':
            #             supplier_id = int(input("Enter supplier ID: "))
            #             order_date = input("Enter order date (YYYY-MM-DD): ")
            #             items = []
            #             while True:
            #                 product_id = int(input("Enter product ID (0 to finish): "))
            #                 if product_id == 0:
            #                     break
            #                 quantity = int(input("Enter quantity: "))
            #                 items.append((product_id, quantity))
            #             PurchaseOrders.create_order(supplier_id, order_date, items)
            #
            #         elif order_choice == '2':
            #             order_id = int(input("Enter the order ID to update: "))
            #             supplier_id = input("Enter new supplier ID (or press Enter to skip): ")
            #             order_date = input("Enter new order date (YYYY-MM-DD, or press Enter to skip): ")
            #             items = input(
            #                 "Enter new items in format 'productid:quantity' separated by commas (or press Enter to skip): ")
            #             items = [(int(item.split(':')[0]), int(item.split(':')[1])) for item in
            #                      items.split(',')] if items else None
            #             PurchaseOrders.update_order(
            #                 order_id,
            #                 supplierid=supplier_id if supplier_id else None,
            #                 order_date=order_date if order_date else None,
            #                 items=items
            #             )
            #
            #         elif order_choice == '3':
            #             order_id = int(input("Enter the order ID to delete: "))
            #             PurchaseOrders.delete_order(order_id)
            #
            #         elif order_choice == '4':
            #             order_id = int(input("Enter the order ID to view: "))
            #             order = PurchaseOrders.fetch_order(order_id)
            #             print(order)
            #
            #         elif order_choice == '5':
            #             orders = PurchaseOrders.fetch_all_orders()
            #             for order in orders:
            #                 print(order)
            #
            #         else:
            #             print("Invalid choice.")
            #
            #     elif choice == '3':
            #         print("1. Create Product")
            #         print("2. Update Product")
            #         print("3. Delete Product")
            #         print("4. View Product")
            #         print("5. View All Products")
            #         product_choice = input("Enter your choice: ")
            #
            #         if product_choice == '1':
            #             name = input("Enter product name: ")
            #             price = float(input("Enter product price: "))
            #             cost_price = float(input("Enter product cost price: "))
            #             supplier_id = int(input("Enter supplier ID: "))
            #             quantity = int(input("Enter initial quantity: "))
            #             Products.create_product(name, price, cost_price, supplier_id, quantity)
            #
            #         elif product_choice == '2':
            #             product_id = int(input("Enter product ID to update: "))
            #             name = input("Enter new name (or press Enter to skip): ")
            #             price = input("Enter new price (or press Enter to skip): ")
            #             cost_price = input("Enter new cost price (or press Enter to skip): ")
            #             supplier_id = input("Enter new supplier ID (or press Enter to skip): ")
            #             quantity = input("Enter new quantity (or press Enter to skip): ")
            #             Products.update_product(
            #                 product_id,
            #                 name=name if name else None,
            #                 price=float(price) if price else None,
            #                 cost_price=float(cost_price) if cost_price else None,
            #                 supplier_id=int(supplier_id) if supplier_id else None,
            #                 quantity=int(quantity) if quantity else None
            #             )
            #
            #         elif product_choice == '3':
            #             product_id = int(input("Enter product ID to delete: "))
            #             Products.delete_product(product_id)
            #
            #         elif product_choice == '4':
            #             product_id = int(input("Enter product ID to view: "))
            #             product = Products.fetch_product(product_id)
            #             print(product)
            #
            #         elif product_choice == '5':
            #             products = Products.fetch_all_products()
            #             for product in products:
            #                 print(product)
            #
            #         else:
            #             print("Invalid choice.")
            #
            #     elif choice == '4':
            #         print("Exiting...")
            #         break
            #
            #     else:
            #         print("Invalid choice. Please enter a valid number.")
            menu()
        else:
            flag=Suppliers.authenticate_admin()
            if flag:
                menu()

    finally:
        DBConnection.close()

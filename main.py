
import argparse
import pymysql
import db
import fill
class DatabaseParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
    def add_arguments(self):
        self.parser.add_argument('-command', choices=['add_user', 'create_order', 'add_product', 'create_tables',
                                                      'fill'], help='Enter the command to execute')
        self.parser.add_argument('-name', type=str, help='User name')
        self.parser.add_argument('-email', type=str, help='User email')
        self.parser.add_argument('-address', type=str, help='User address')
        self.parser.add_argument('-client_id', type=int, help='Client ID')
        self.parser.add_argument('-delivery', type=str, help='Delivery details')
        self.parser.add_argument('-order_id', type=int, help='Order ID')
        self.parser.add_argument('-product_id', type=int, help='Product ID')
        self.parser.add_argument('-number', type=int, help='Quantity')
        return self.parser
    def args_as_dict(self, args):
        args_dict = {}
        for key, value in args._get_kwargs():
            if value is not None:
                args_dict[key] = value
        return args_dict

class OnlineShopManager:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = pymysql.connect(host=server, user=username, password=password, database=database)
    def add_user_to_database(self, name, email, address):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Client (Name, email, adress) VALUES (%s, %s, %s)", (name, email, address))
        self.conn.commit()
        cursor.close()
    def create_order(self, client_id, delivery):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Orders (id_client, delivery) VALUES (%s, %s)", (client_id, delivery))
        self.conn.commit()
        cursor.close()
    def add_product_to_order(self, order_id, product_id, number):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Order_products (id_order, id_product, number) VALUES (%s, %s, %s)", (order_id, product_id, number))
        self.conn.commit()
        cursor.close()
if __name__ == "__main__":
    db_parser = DatabaseParser()
    parser = db_parser.add_arguments()
    args = db_parser.args_as_dict(parser.parse_args())
    online_shop_manager = OnlineShopManager('localhost', 'onlineshop', 'user1', '1234')
    if args["command"] == "add_user":
        online_shop_manager.add_user_to_database(args["name"], args["email"], args["address"])
    elif args["command"] == "create_tables":
        db.CreateTables()
    elif args["command"] == "fill":
        fill.fill()
    elif args["command"] == "create_order":
        online_shop_manager.create_order(args["client_id"], args["delivery"])
    elif args["command"] == "add_product":
        online_shop_manager.add_product_to_order(args["order_id"], args["product_id"], args["number"])
    else:
        print("Invalid command")
    online_shop_manager.conn.close()
import pymysql

class DatabaseManager:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=self.server, user=self.username, password=self.password, database=self.database)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(create_table_query)

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
def CreateTables():
    server = 'localhost'
    database = 'OnlineShop'
    username = 'user1'
    password = '1234'

    db_manager = DatabaseManager(server, database, username, password)
    db_manager.connect()

    client_columns = ["Id INT AUTO_INCREMENT PRIMARY KEY", "Name NVARCHAR(255)", "email NVARCHAR(255)",
                      "adress NVARCHAR(255)"]
    db_manager.create_table("Client", client_columns)

    products_columns = ["Id INT AUTO_INCREMENT PRIMARY KEY", "name NVARCHAR(255)", "price INT"]
    db_manager.create_table("Products", products_columns)

    orders_columns = ["id_order INT AUTO_INCREMENT PRIMARY KEY", "id_client INT", "delivery NVARCHAR(255)",
                      "FOREIGN KEY (id_client) REFERENCES Client(Id)"]
    db_manager.create_table("Orders", orders_columns)

    order_products_columns = ["id_order INT", "id_product INT", "number INT", "PRIMARY KEY (id_order, id_product)",
                              "FOREIGN KEY (id_order) REFERENCES Orders(id_order)",
                              "FOREIGN KEY (id_product) REFERENCES Products(Id)"]
    db_manager.create_table("Order_Products", order_products_columns)

    db_manager.commit_and_close()
import pymysql
import random
from faker import Faker

class DatabaseFiller:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def connect(self):
        self.conn = pymysql.connect(host=self.server, user=self.username, password=self.password, database=self.database)
        self.cursor = self.conn.cursor()

    def fill_client_table(self, num_records=1000):
        fake = Faker()
        try:
            for _ in range(num_records):
                name = fake.name()
                email = fake.email()
                address = fake.address().replace("'", "''")
                query = f"INSERT INTO Client (Name, email, adress) VALUES ('{name}', '{email}', '{address}')"
                self.cursor.execute(query)
        except pymysql.IntegrityError as e:
            print("IntegrityError occurred:", e)

    def fill_products_table(self, num_records=1000):
        fake = Faker()
        try:
            for _ in range(num_records):
                name = fake.word()
                price = random.randint(10, 1000)
                query = f"INSERT INTO Products (name, price) VALUES ('{name}', {price})"
                self.cursor.execute(query)
        except pymysql.IntegrityError as e:
            print("IntegrityError occurred:", e)

    def fill_orders_table(self, num_records=1000):
        try:
            for _ in range(num_records):
                client_id = random.randint(1, 1000)  # Assuming 1000 clients exist
                delivery = random.choice(['CDEK', 'Mail'])  # Randomly choose between CDEK and Mail
                query = f"INSERT INTO Orders (id_client, delivery) VALUES ({client_id}, '{delivery}')"
                self.cursor.execute(query)
        except pymysql.IntegrityError as e:
            print("IntegrityError occurred:", e)

    def fill_orders_products_table(self, num_records=1000):
        try:
            for _ in range(num_records):
                order_id = random.randint(1, 1000)  # Assuming 1000 orders exist
                product_id = random.randint(1, 1000)  # Assuming 1000 products exist
                number = random.randint(1, 10)
                query = f"INSERT INTO Order_Products (id_order, id_product, number) VALUES ({order_id}, {product_id}, {number})"
                self.cursor.execute(query)
        except pymysql.IntegrityError as e:
            print("IntegrityError occurred:", e)

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
def fill():
    server = 'localhost'
    database = 'OnlineShop'
    username = 'user1'
    password = '1234'

    filler = DatabaseFiller(server, database, username, password)
    filler.connect()
    filler.fill_client_table()
    filler.fill_products_table()
    filler.fill_orders_table()
    filler.fill_orders_products_table()
    filler.commit_and_close()


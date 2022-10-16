import time
import unittest
from contextlib import closing
from config import HOST, USER, PASSWORD
from main import process_command, create_order, add_product_order, show_order_from_order_id, show_all_orders
import mysql.connector

class TestProcessCommand(unittest.TestCase):

    def setUp(self):
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password'
    )
        with closing(cnx) as db_connection:
            with closing(db_connection.cursor()) as cur:
                cur.execute("""
                    CREATE DATABASE test_order_management_2""")
                cur.execute(""" 
                    USE test_order_management_2""")
                cur.execute(""" 
                    CREATE TABLE `order` (
                    order_id MEDIUMINT UNSIGNED AUTO_INCREMENT,
                    order_status VARCHAR(10) DEFAULT 'DRAFT',
                    PRIMARY KEY (order_id))""")
                cur.execute(""" 
                    CREATE TABLE order_line (
                    product_name VARCHAR(100),
                    product_quantity SMALLINT UNSIGNED,
                    order_id MEDIUMINT UNSIGNED,
                    FOREIGN KEY (order_id) REFERENCES `order`(order_id));""")
                cur.execute("""ALTER TABLE order_line ADD UNIQUE product_order_index (order_id, product_name)""")
                cur.execute("""
                    INSERT INTO `order` () 
                    VALUES (), (), ()""")
                cur.execute("""
                    INSERT INTO order_line 
                    (product_name, product_quantity, order_id)
                    VALUES 
                    ('Apples', 15, 1),
                    ('Oranges', 10, 1),
                    ('Pears', 3, 1),
                    ('Apples', 12, 2),
                    ('Peaches', 9, 2),
                    ('Plums', 20, 2),
                    ('Bananas', 5, 2),
                    ('Apples', 15, 3),
                    ('Blueberries', 8, 3)""")
                db_connection.commit()
                print("db created")

    def tearDown(self):
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password'
        )
        with closing(cnx) as db_connection:
            with closing(db_connection.cursor()) as cur:
                cur.execute("""
                    DROP DATABASE test_order_management_2
                """)
                db_connection.commit()

    def test_create_order(self):
        output = process_command("CREATE_ORDER")
        self.assertRegex(output, 'Order created with id \\d')

    def test_add_product_order(self):
        output = process_command("ADD_PRODUCT_ORDER 3 'Bananas' 10")
        self.assertEqual(output, '10 Bananas added to order 3')

    def test_show_order_from_order_id(self):
        output = process_command("SHOW ORDER [order_id")
        self.assertEqual(output, 'Order 1 DRAFT 28\nApples 15 DRAFT\nOranges 10 DRAFT\nPears 3 DRAFT')

    def test_show_all_orders(self):
        output = process_command("SHOW ORDERS")
        self.assertEqual(output, 'Order 1 DRAFT 28\nApples 15 DRAFT\nOranges 10 DRAFT\nPears 3 DRAFT\nOrder 2 DRAFT 41\nApples 12 DRAFT\nPeaches 9 DRAFT\nPlums 20 DRAFT\nBananas 5 DRAFT\nOrder 3 DRAFT 23\n Apples 15 DRAFT\nBlueberries 8 DRAFT')



if __name__ == '__main__':
    unittest.main()
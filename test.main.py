import unittest
from contextlib import closing
from config import HOST, USER, PASSWORD
from main import process_command
import db_utils
import mysql.connector

test_database_name = "test_order_management"


class TestProcessCommand(unittest.TestCase):
    def setUp(self):
        cnx = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, auth_plugin="mysql_native_password"
        )
        with closing(cnx) as db_connection:
            with closing(db_connection.cursor()) as cur:
                cur.execute(
                    """
                    DROP DATABASE IF EXISTS test_order_management"""
                )
                cur.execute(
                    """
                    CREATE DATABASE test_order_management"""
                )
                cur.execute(
                    """ 
                    USE test_order_management"""
                )
                cur.execute(
                    """ 
                    CREATE TABLE `order` (
                    order_id MEDIUMINT UNSIGNED AUTO_INCREMENT,
                    order_status VARCHAR(10) DEFAULT 'DRAFT',
                    PRIMARY KEY (order_id))"""
                )
                cur.execute(
                    """ 
                    CREATE TABLE order_line (
                    product_name VARCHAR(100),
                    product_quantity SMALLINT UNSIGNED,
                    order_id MEDIUMINT UNSIGNED,
                    status VARCHAR(10) DEFAULT 'DRAFT',
                    FOREIGN KEY (order_id) REFERENCES `order`(order_id));"""
                )
                cur.execute(
                    """ALTER TABLE order_line ADD UNIQUE product_order_index (order_id, product_name)"""
                )
                cur.execute(
                    """
                    INSERT INTO `order` () 
                    VALUES (), (), ()"""
                )
                cur.execute(
                    """
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
                    ('Blueberries', 8, 3)"""
                )
                db_connection.commit()
                print("db created")
        db_utils.test_database_name = "test_order_management"

    def tearDown(self):
        cnx = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, auth_plugin="mysql_native_password"
        )
        with closing(cnx) as db_connection:
            with closing(db_connection.cursor()) as cur:
                cur.execute(
                    """
                    DROP DATABASE test_order_management
                """
                )
                db_connection.commit()
        db_utils.test_database_name = None

    def test_create_order(self):
        output = process_command("CREATE_ORDER")
        print("Output is: {output}".format(output=output))
        self.assertRegex(output, r"Order created with id \d+")

    def test_add_product_order(self):
        output = process_command("ADD_ORDERLINE 3 Mangos 10")
        self.assertEqual(output, "10 Mangos added to order 3")

    def test_show_order_from_order_id(self):
        output = process_command("SHOW_ORDER 1")
        self.assertEqual(
            output, "Order 1 DRAFT 28\nApples 15 DRAFT\nOranges 10 DRAFT\nPears 3 DRAFT"
        )

    def test_show_all_orders(self):
        output = process_command("SHOW_ORDERS")
        self.assertEqual(
            output,
            "Order 1 DRAFT 28\nApples 15 DRAFT\nOranges 10 DRAFT\nPears 3 DRAFT\nOrder 2 DRAFT 46\nApples 12 DRAFT\nBananas 5 DRAFT\nPeaches 9 DRAFT\nPlums 20 DRAFT\nOrder 3 DRAFT 23\nApples 15 DRAFT\nBlueberries 8 DRAFT",
        )

    def test_returns_error_if_args_given_to_create_order(self):
        output = process_command("CREATE_ORDER 1")
        self.assertEqual(
            output,
            "Please check your input and try again:\nCREATE_ORDER should not take any arguments",
        )

    def test_returns_error_if_args_missing_from_add_order_line(self):
        output = process_command("ADD_ORDERLINE Mango 3")
        self.assertEqual(
            output,
            "Please check your input and try again:\nADD_ORDERLINE must be provided with product_name, product_quantity and order_id",
        )

    def test_returns_error_if_args_missing_from_show_order(self):
        output = process_command("SHOW_ORDER")
        self.assertEqual(
            output,
            "Please check your input and try again:\nSHOW_ORDER must take one argument of an order_id",
        )

    def test_returns_error_if_additional_args_given_to_show_order(self):
        output = process_command("SHOW_ORDER 1 Banana")
        self.assertEqual(
            output,
            "Please check your input and try again:\nSHOW_ORDER must take one argument of an order_id",
        )

    def test_returns_error_if_args_given_to_show_orders(self):
        output = process_command("SHOW_ORDERS 1")
        self.assertEqual(
            output,
            "Please check your input and try again:\nSHOW_ORDERS should not take any arguments",
        )


if __name__ == "__main__":
    unittest.main()

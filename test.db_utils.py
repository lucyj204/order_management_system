import unittest
import unittest.mock
import mysql.connector
from config import HOST, USER, PASSWORD, DATABASE_NAME
from db_utils import create_order_db, add_order_line, get_total_quantity_for_all_orders, get_total_quantity_for_order_id

test_database_name = "test_order_management_2"
class TestConnection(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE_NAME,
            auth_plugin='mysql_native_password'
        )

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def test_is_connected(self):
        self.assertTrue(self.connection.is_connected())

class TestDBFunctions(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE_NAME,
            auth_plugin='mysql_native_password'
        )

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def test_create_order(self):
        output = create_order_db()
        self.assertRegex(output, 'Order created with id \\d')

    def test_add_order_line_output(self):
        output = add_order_line('Banana', 10, 4)
        self.assertEqual(output, '10 Banana added to order 4')


if __name__ == '__main__':
    unittest.main()


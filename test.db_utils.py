import unittest
import unittest.mock
import io
import sys
import re
import mysql.connector
from config import HOST, USER, PASSWORD, DATABASE_NAME
from db_utils import DbConnectionError, create_order, add_orderline, get_total_quantity_for_all_orders, get_total_quantity_for_order_id
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
        output = create_order()
        self.assertRegex(output, 'Order created with id \\d')

    def test_add_orderline_output(self):
        output = add_orderline('Banana', 10, 4)
        self.assertEqual(output, '10 Banana added to order 4')

    def test_add_orderline(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        add_orderline('Orange', 5, 13)
        sys.stdout = sys.__stdout__
        print('Captured', capturedOutput.getvalue())


if __name__ == '__main__':
    unittest.main()


from audioop import add
import unittest
import unittest.mock
import io
import sys
import mysql.connector
from config import HOST, USER, PASSWORD
from db_utils import DbConnectionError, create_order, add_orderline
class TestConnection(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database='order_management'
        )

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def test_is_connected(self):
        self.assertTrue(self.connection.is_connected())

    def test_add_orderline(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        add_orderline('Orange', 5, 1)
        sys.stdout = sys.__stdout__
        print('Captured', capturedOutput.getvalue())


if __name__ == '__main__':
    unittest.main()


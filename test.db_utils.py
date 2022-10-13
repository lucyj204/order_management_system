import unittest
import mysql.connector
from config import HOST, USER, PASSWORD
from db_utils import create_order

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


if __name__ == '__main__':
    unittest.main()


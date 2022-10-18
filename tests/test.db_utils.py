import unittest
import unittest.mock
import mysql.connector
from config import HOST, USER, PASSWORD, DATABASE_NAME

test_database_name = "test_order_management_2"

class TestConnection(unittest.TestCase):
    connection = None

    def setUp(self):
        self.connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE_NAME,
            auth_plugin="mysql_native_password",
        )

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def test_is_connected(self):
        self.assertTrue(self.connection.is_connected())



if __name__ == "__main__":
    unittest.main()

from contextlib import closing
from collections import namedtuple
import mysql.connector
from config import USER, PASSWORD, HOST, DATABASE_NAME

test_database_name = None

Order = namedtuple("Order", ["id", "status"])
OrderLine = namedtuple(
    "OrderLine", ["order_id", "product_name", "product_quantity", "status"]
)


def connect_to_db():
    """
    Establishes connection with MySQL server and returns the connection
    """
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME if test_database_name is None else test_database_name,
        auth_plugin="mysql_native_password",
    )
    return cnx


def create_order_db():
    """
    Returns the ID of the created row from the DB
    """
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute(
                """
                INSERT INTO `order` ()
                VALUES ();
            """
            )
            db_connection.commit()
            return cur.lastrowid


def add_order_line(product_name, product_quantity, order_id):
    """
    Inserts new order line to the DB
    """

    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute(
                """
                INSERT INTO order_line (product_name, product_quantity, order_id)
                VALUES (%(product_name)s, %(product_quantity)s, %(order_id)s)
            """,
                {
                    "product_name": product_name,
                    "product_quantity": product_quantity,
                    "order_id": order_id,
                },
            )
            db_connection.commit()


def get_order(order_id):
    """
    Returns Order object for single order
    """
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute(
                """
                    SELECT order_id, order_status
                    FROM `order` 
                    WHERE order_id = %(order_id)s
                """,
                {"order_id": order_id},
            )
            rows = cur.fetchall()
            row = rows[0]
            return Order(row[0], row[1])


def get_order_lines(order_id):
    """
    Returns a list of OrderLine
    """
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute(
                """
                    SELECT order_id, product_name, product_quantity, status
                    FROM order_line
                    WHERE order_id = %(order_id)s
                """,
                {"order_id": order_id},
            )
            rows = cur.fetchall()
            return [OrderLine(row[0], row[1], row[2], row[3]) for row in rows]


def get_order_ids_for_all_orders():
    """
    Returns a list of order_id
    """
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute(
                """
                SELECT DISTINCT order_id 
                FROM `order`
            """
            )
            rows = cur.fetchall()
            return [row[0] for row in rows]

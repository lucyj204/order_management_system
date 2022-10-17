from contextlib import closing
import mysql.connector
from config import USER, PASSWORD, HOST, DATABASE_NAME

test_database_name = None

def connect_to_db():
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME if test_database_name is None else test_database_name,
        auth_plugin='mysql_native_password'
    )
    return cnx

def create_order_db():
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                INSERT INTO `order` ()
                VALUES ();
            """)
            db_connection.commit()
            return cur.lastrowid

def add_orderline(product_name, product_quantity, order_id):
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                INSERT INTO order_line (product_name, product_quantity, order_id)
                VALUES ('{product_name}', {product_quantity}, {order_id})
            """.format(product_name=product_name, product_quantity=product_quantity, order_id=order_id))
            db_connection.commit()
            return True
            #TODO: Think about how to handle errors from duplicate item entered to add to order

def show_order(order_id):
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                SELECT `order` . *, order_line . *
                FROM `order`
                INNER JOIN order_line
                ON `order`.order_id = order_line.order_id
                WHERE order_line.order_id = {order_id}
            """.format(order_id=order_id))
            result = cur.fetchall()
            return result
            #TODO: Handle errors if no products added to order ID

def show_orders():
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                SELECT ord.order_id, ord.order_status, ol.product_name, ol.product_quantity
                FROM `order` ord
                LEFT JOIN order_line ol ON ord.order_id = ol.order_id
                WHERE ol.product_name IS NOT NULL
                ORDER BY ord.order_id;
            """)
            result = cur.fetchall()
            return result

def get_order_ids_for_all_orders():
    # TODO: Improve to show all order ids - only showing those with products added at present
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                SELECT DISTINCT order_id 
                FROM order_line
            """)
            result = cur.fetchall()
            return result

def get_total_quantity_for_order_id(order_id):
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                SELECT SUM(product_quantity) AS total_quantity
                FROM order_line
                WHERE order_id = {order_id}
            """.format(order_id=order_id))
            result = cur.fetchall()
            return result[0][0]


from contextlib import closing
import mysql.connector
from config import USER, PASSWORD, HOST, DATABASE_NAME
class DbConnectionError(Exception):
    pass

def connect_to_db():
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME,
        auth_plugin='mysql_native_password'
    )
    return cnx

def create_order():
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                INSERT INTO `order` ()
                VALUES ();
            """)
            db_connection.commit()
            return 'Order created with id {id}'.format(id=cur.lastrowid)

def add_orderline(product_name, product_quantity, order_id):
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                INSERT INTO order_line (product_name, product_quantity, order_id)
                VALUES ('{product_name}', {product_quantity}, {order_id})
            """.format(product_name=product_name, product_quantity=product_quantity, order_id=order_id))
            db_connection.commit()
            print('{quantity} {name} added to order {id}'.format(quantity=product_quantity, name=product_name, id=order_id))
            return '{quantity} {name} added to order {id}'.format(quantity=product_quantity, name=product_name, id=order_id)
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
            format_results_for_order_id(result)
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
            format_results_for_all_orders(result)

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

def get_total_quantity_for_all_orders():
    with closing(connect_to_db()) as db_connection:
        with closing(db_connection.cursor()) as cur:
            cur.execute("""
                SELECT SUM(product_quantity) AS total_quantity
                FROM order_line
            """)
            result = cur.fetchall()
            return result[0][0]

def format_results_for_order_id(order):
    total_orders = get_total_quantity_for_order_id(order[0][0])
    print('Order {id} {status} {count}'.format(id=order[0][0], status=order[0][1], count=total_orders))
    for product in range(len(order)):
        print("{name} {quantity} {status}".format(name=order[product][2], quantity=order[product][3], status=order[product][1]))
        product +=1

def format_results_for_all_orders(order):
    print('order is: {order}'.format(order=order))
    total_orders = get_total_quantity_for_all_orders()
    print('Order {id} {status} {count}'.format(id=order[0][0], status=order[0][1], count=total_orders))
    for product in range(len(order)):
        print("{name} {quantity} {status}".format(name=order[product][2], quantity=order[product][3], status=order[product][1]))
        product +=1
        #TODO: format correctly so orders are listed by ID

if __name__ == '__main__':
    # create_order()
    # add_orderline('Orange', 9, 1)
    # add_orderline('Orange', 2, 8)
    # add_orderline('Apple', 5, 5)
    # add_orderline('', 1, 1)
    show_order(1)
    # show_orders_2()
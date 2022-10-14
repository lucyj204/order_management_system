import mysql.connector
from config import USER, PASSWORD, HOST;

from utils import format_results_for_all_orders, format_results_for_order_id

class DbConnectionError(Exception):
    pass

def connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx

def create_order():
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        INSERT INTO `order` ()
        VALUES ();
        """

        cur.execute(query)
        id = get_created_id()
        print('Order created with id {id}'.format(id=id))
        db_connection.commit()
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to connect to database")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def get_created_id():
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT MAX(`order`.order_id)
        FROM `order`
        """
        #TODO: change query so that that we are getting correct id when first id created.

        cur.execute(query)
        result = cur.fetchall()
        print(result)
        db_connection.commit()
        cur.close()
        return result[0][0]
    
    except Exception:
        raise DbConnectionError("Failed to connect to database")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def add_orderline(product_name: str, product_quantity: int, order_id: int):
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        INSERT INTO order_line (product_name, product_quantity, order_id)
        VALUES ('{product_name}', {product_quantity}, {order_id})
        """.format(product_name=product_name, product_quantity=product_quantity, order_id=order_id)

        print(query)
        print('{quantity} {name} added to order {id}'.format(quantity=product_quantity, name=product_name, id=order_id))
        cur.execute(query)
        db_connection.commit()
        db_connection.close()

    except Exception:
        #TODO: create DBDuplicationError case if product already exists in the DB
        raise DbConnectionError("Failed to update DB")
    
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def show_order(order_id):
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT `order` . *, order_line . *
        FROM `order`
        INNER JOIN order_line
        ON `order`.order_id = order_line.order_id
        WHERE order_line.order_id = {order_id}
        """.format(order_id=order_id)

        print(query)
        cur.execute(query)
        result = cur.fetchall()
        format_results_for_order_id(result)
        db_connection.close()
    
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def show_orders():
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT ord.order_id, ord.order_status, ol.product_name, ol.product_quantity
        FROM `order` ord
        LEFT JOIN order_line ol ON ord.order_id = ol.order_id
        WHERE ol.product_name IS NOT NULL
        ORDER BY ord.order_id;
        """

        print(query)
        cur.execute(query)
        result = cur.fetchall()
        format_results_for_all_orders(result)
        # print(result)
        # print('first result: {result[0]}'.format(result=result))
        db_connection.close()
    
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def get_total_quantity_for_order_id(order_id):
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT SUM(product_quantity) AS total_quantity
        FROM order_line
        WHERE order_id = {order_id}
        """.format(order_id=order_id)

        print(query)
        cur.execute(query)
        result = cur.fetchall()
        db_connection.close()
        return result[0][0]
    
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def get_total_quantity_for_all_orders():
    try:
        db_name = "order_management"
        db_connection = connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT SUM(product_quantity) AS total_quantity
        FROM order_line
        """

        print(query)
        cur.execute(query)
        result = cur.fetchall()
        db_connection.close()
        return result[0][0]
    
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

if __name__ == '__main__':
    # create_order()
    # add_orderline('Orange', 9, 1)
    # add_orderline('Orange', 2, 2)
    # add_orderline('', 1, 1)
    show_order(1)
    show_orders()




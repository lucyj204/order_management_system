import mysql.connector
from config import USER, PASSWORD, HOST;

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
        db_connection.commit()
        cur.close()

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
        cur.execute(query)
        db_connection.commit()
        db_connection.close()

    except Exception:
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
        print(result)
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
        SELECT `order` . *, order_line . *
        FROM `order`
        INNER JOIN order_line
        ON `order`.order_id = order_line.order_id
        ORDER BY `order`.order_id
        """

        print(query)
        cur.execute(query)
        result = cur.fetchall()
        print(result)
        db_connection.close()
    
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

if __name__ == '__main__':
    show_orders()



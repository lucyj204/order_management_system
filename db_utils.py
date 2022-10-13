from multiprocessing import connection
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
        INSERT INTO orders ()
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


if __name__ == '__main__':
    create_order()



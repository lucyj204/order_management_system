import shlex
import db_utils

inventory = ["Bananas", "Apples", "Oranges", "Pears", "Plums", "Peaches", "Mangos", "Blueberries"]


def run():
    print()
    print("HELLO, WELCOME TO THE ORDER MANAGEMENT SYSTEM")
    print()
    print("AVAILABLE COMMANDS:")
    print("1. CREATE_ORDER")
    print("2. ADD_ORDERLINE [order_id] [product_name] [product_quantity]")
    print("3. SHOW_ORDER [order_id]")
    print("4. SHOW_ORDERS")
    print()
    print("ITEMS CURRENTLY IN INVENTORY:")
    print(inventory)
    while True:
        print()
        command = input("ENTER CHOSEN COMMAND: ")
        print()
        print(process_command(command))


def process_command(command):
    args = shlex.split(command)

    if command == "":
        print("Please enter a command")
    elif args[0] == "CREATE_ORDER":
        return create_order(args[1:])
    elif args[0] == "ADD_ORDERLINE":
        return add_order_line(args[1:])
    elif args[0] == "SHOW_ORDER":
        return show_order(args[1:])
    elif args[0] == "SHOW_ORDERS":
        return show_orders(args[1:])
    else:
        return "COMMAND NOT RECOGNISED\nPlease check the spelling of the command and make sure _ has been included where specified"


def create_order(args):
    """
    Returns string with created id
    """
    if len(args) > 0:
        return "Please check your input and try again:\nCREATE_ORDER should not take any arguments"
    id = db_utils.create_order_db()
    return f"Order created with id {id}"


def add_order_line(args):
    """
    Takes a list of strings and returns a single string with product quantity, product name and order id
    """
    if len(args) != 3:
        return "Please check your input and try again:\nADD_ORDERLINE must be provided with product_name, product_quantity and order_id"
    order_id = int(args[0])
    product_name = str(args[1]).capitalize()
    product_quantity = int(args[2])

    if str(product_name).capitalize() not in inventory:
        return f"Product {product_name} does not exist"
    elif order_id not in db_utils.get_order_ids_for_all_orders():
        return f"Order with id {order_id} does not exist"
    elif product_name in show_order(args[0]):
        return f"{product_name} already added to order {order_id}"
    else:
        db_utils.add_order_line(
            order_id=order_id,
            product_name=product_name,
            product_quantity=product_quantity,
        )
        return f"{product_quantity} {product_name} added to order {order_id}"


def show_order(args):
    """Takes a list of string and returns a list of strings"""
    if len(args) != 1:
        return "Please check your input and try again:\nSHOW_ORDER must take one argument of an order_id"
    order_id = int(args[0])
    return show_single_order(order_id)


def show_orders(args):
    """Takes a list of string and returns a list of strings"""
    if len(args) > 0:
        return "Please check your input and try again:\nSHOW_ORDERS should not take any arguments"
    order_ids = db_utils.get_order_ids_for_all_orders()
    response_list = [show_single_order(id) for id in order_ids]
    return "\n".join(response_list)


def show_single_order(order_id):
    """Takes an integer and returns a list of strings"""
    order = db_utils.get_order(order_id)
    order_lines = db_utils.get_order_lines(order_id)
    total_quantity = sum([order_line.product_quantity for order_line in order_lines])
    total_order_return = f"Order {order.id} {order.status} {total_quantity}"
    output_lines = [total_order_return] + [
        f"{ol.product_name} {ol.product_quantity} {ol.status}" for ol in order_lines
    ]
    return "\n".join(output_lines)


if __name__ == "__main__":
    run()

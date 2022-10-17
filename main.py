import shlex
import db_utils


def run():
    print()
    print("HELLO, WELCOME TO THE ORDER MANAGEMENT SYSTEM")
    print()
    print("AVAILABLE COMMANDS:")
    print("1. CREATE_ORDER")
    print("2. ADD_PRODUCT_ORDER [order_id] [product_name] [product_quantity]")
    print("3. SHOW_ORDER [order_id]")
    print("4. SHOW_ORDERS")
    while True:
        print()
        command = input("ENTER CHOSEN COMMAND: ")
        print()
        print(process_command(command))


def process_command(command):
    args = shlex.split(command)

    if args[0] == "CREATE_ORDER":
        return create_order(args[1:])
    elif args[0] == "ADD_PRODUCT_ORDER":
        return add_product_order(args[1:])
    elif args[0] == "SHOW_ORDER":
        return show_order(args[1:])
    elif args[0] == "SHOW_ORDERS":
        return show_orders(args[1:])
    else:
        return "COMMAND NOT RECOGNISED"


def create_order(args):
    id = db_utils.create_order_db()
    return f"Order created with id {id}"


def add_product_order(args):
    order_id = int(args[0])
    product_name = args[1]
    product_quantity = int(args[2])
    db_utils.add_order_line(
        order_id=order_id, product_name=product_name, product_quantity=product_quantity
    )
    return f"{product_quantity} {product_name} added to order {order_id}"


def show_order(args):
    order_id = int(args[0])
    return show_single_order(order_id)


def show_orders(args):
    order_ids = db_utils.get_order_ids_for_all_orders()
    response_list = [show_single_order(id) for id in order_ids]
    return "\n".join(response_list)


def show_single_order(order_id):
    order = db_utils.get_order(order_id)
    order_lines = db_utils.get_order_lines(order_id)
    total_quantity = sum([order_line.product_quantity for order_line in order_lines])
    total_order_return = f"Order {order.id} {order.status} {total_quantity}"
    output_lines = [total_order_return] + [
        f"{ol.product_name} {ol.product_quantity} {ol.status}" for ol in order_lines
    ]
    return "\n".join(output_lines)

    # TODO: Error handling of args


if __name__ == "__main__":
    run()

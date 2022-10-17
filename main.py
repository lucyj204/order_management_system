import re
from db_utils import create_order_db, add_orderline, show_order, show_orders, get_total_quantity_for_order_id, get_order_ids_for_all_orders

def run():
    print()
    print('HELLO, WELCOME TO THE ORDER MANAGEMENT SYSTEM')
    print()
    command = input('AVAILABLE COMMANDS:\n\n1. CREATE_ORDER\n2. ADD_PRODUCT_ORDER [order_id] [product_name] [product_quantity]\n3. SHOW_ORDER [order_id]\n4. SHOW_ORDERS\n\nENTER CHOSEN COMMAND: ')
    print()
    print()
    process_command(command)
    

def process_command(command):
    add_product_regex = re.match(r"ADD_PRODUCT_ORDER\s\d\s\w+\s\d+", command, re.IGNORECASE)
    show_order_regex = re.match(r"SHOW_ORDER\s\d+", command, re.IGNORECASE)
    add_order_regex_object = re.search(r"ADD_PRODUCT_ORDER\s\d\s\w+\s\d+", command)

    if command == "CREATE_ORDER":
        id = create_order()
        response = "Order created with id {id}".format(id=id)
        print(response)
        return response
    elif add_product_regex:
        add_product_as_list = add_order_regex_object.group().split(" ")
        order_id = add_product_as_list[1]
        product_name = add_product_as_list[2]
        product_quantity = add_product_as_list[3]
        if add_product_order(order_id, product_name, product_quantity):
            response = "{quantity} {name} added to order {id}".format(quantity=product_quantity, name=product_name, id=order_id)
            print(response)
            return response
        else:
            print("error")
            # TODO: Improve error message to user
    elif show_order_regex:
       show_order_list = show_order_regex.group().split(" ")
       order_id = show_order_list[1]
       response = show_order_from_order_id(order_id)
       print(response)
       return response
    elif command == "SHOW_ORDERS":
        response = show_all_orders()
        print(response)
        return response
    else:
        print("command not recognised")
        # Improve message to user
        return

def create_order():
    order_id = create_order_db()
    return order_id

def add_product_order(id, name, quantity):
    if add_orderline(order_id=id, product_name=name, product_quantity=quantity):
        return True

def show_order_from_order_id(order_id):
    orders = show_order(order_id)
    total_orders = get_total_quantity_for_order_id(orders[0][0])
    total_order_return = 'Order {id} {status} {count}'.format(id=orders[0][0], status=orders[0][1], count=total_orders)
    order_list = []
    order_list.append(total_order_return)
    for idx in range(len(orders)):
        order_list.append("{name} {quantity} {status}".format(name=orders[idx][2], quantity=orders[idx][3], status=orders[idx][1]))
        idx +=1
    split = '\n'.join(order_list)
    return split

def show_all_orders():
    id_list = []
    response_list = []
    order_ids = get_order_ids_for_all_orders()
    for idx in order_ids:
        id_list.append(idx[0])
    for idx in id_list:
        response = show_order_from_order_id(idx)
        response_list.append(response)
        idx += 1
    return '\n'.join(response_list)



if __name__ == '__main__':
    run()
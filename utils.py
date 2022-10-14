from db_utils import get_total_quantity_for_all_orders, get_total_quantity_for_order_id

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
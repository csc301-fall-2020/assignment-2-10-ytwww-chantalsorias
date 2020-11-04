class Orders:
    def __init__(self):
        self.orders = []
        self.current_order_number = 1

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order):
        self.orders.remove(order)

    def find_order(self, order_number):
        for order in self.orders:
            if order.order_number == order_number:
                return order
        return "order does not exist"

    def new_order(self):
        new_order = Order(self.current_order_number)
        self.orders.append(new_order)
        self.current_order_number += 1
        return new_order


class Order:
    def __init__(self, order_number):
        self.order_number = order_number
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def display_items(self):
        items_in_order = {}
        for item in self.items:
            if item.name in items_in_order:
                items_in_order[item.name]["quantity"] += 1
            else:
                # If a custom pizza, display toppings
                if hasattr(item, "toppings"):
                    items_in_order[item.name] = {
                        "toppings": self.display_toppings(item.toppings), "price": item.price, "quantity": 1}
                else:
                    items_in_order[item.name] = {
                        "price": item.price, "quantity": 1}
        return items_in_order

    def display_toppings(self, toppings):
        display_toppings = {}
        for topping in toppings:
            display_toppings[topping.name] = topping.price
        return display_toppings


class OrderItem:
    def __init__(self, order_number, item):
        self.order_number = order_number
        self.item = item

from MenuItem import CustomPizza


class Orders:
    def __init__(self):
        self.orders = []
        self.current_order_number = 1

    def remove_order(self, order):
        self.orders.remove(order)

    def get_order(self, order_number):
        for order in self.orders:
            if order.order_number == order_number:
                return order

    def new_order(self):
        new_order = Order(self.current_order_number)
        self.orders.append(new_order)
        self.current_order_number += 1
        return new_order


class Order:
    def __init__(self, order_number):
        self.order_number = order_number
        self.custom_pizza_number = 1
        self.order_complete = False
        self.items = []

    def add_item(self, item):
        if (isinstance(item, CustomPizza)):
            self.custom_pizza_number += 1

        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return
        return "The order does not contain " + item_name + "."

    def display_items(self):
        items_in_order = {}
        for item in self.items:
            if item.name in items_in_order:
                items_in_order[item.name]["quantity"] += 1
            else:
                # If a custom pizza, display toppings
                if hasattr(item, "toppings"):
                    items_in_order[item.name] = {"size": item.size.serialize(),
                                                 "toppings": self.display_toppings(item.toppings), "price": item.price, "quantity": 1}
                else:
                    items_in_order[item.name] = {
                        "price": item.price, "quantity": 1}
            subtotal = self.calculate_price()
            total = subtotal * 1.13
            items_in_order["subtotal"] = subtotal
            items_in_order["total"] = round(total, 2)

        return items_in_order

    def display_toppings(self, toppings):
        display_toppings = {}
        for topping in toppings:
            display_toppings[topping.name] = topping.price
        return display_toppings

    def checkout(self):
        self.order_complete = True
        subtotal = self.calculate_price()
        total = round(subtotal * 1.13, 2)
        return subtotal, total

    def has_items(self):
        return len(self.items) != 0

    def calculate_price(self):
        price = 0
        for item in self.items:
            price += item.price
        return round(price, 2)

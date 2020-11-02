class Order:
    def __init__(self, order_number):
        self.order_number = order_number
        self.items = []


class OrderItem:
    def __init__(self, order_number, item):
        self.order_number = order_number
        self.item = item

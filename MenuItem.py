class Menu:
    def __init__(self):
        self.pizzas = []
        self.drinks = []
        self.toppings = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)

    def add_drink(self, drink):
        self.drinks.append(drink)
    
    def add_topping(self, topping):
        self.toppings.append(topping)

    def find_pizza(self, pizza_name):
        for pizza in self.pizzas:
            if pizza.name.lower() == pizza_name.lower():
                return pizza.serialize()
        return "Pizza does not exist"

    def find_drink(self, drink_name):
        for drink in self.drinks:
            if drink.name.lower() == drink_name.lower():
                return drink.serialize()
        return "Drink does not exist"

    def find_topping(self, topping_name):
        for topping in self.toppings:
            if topping.name.lower() == topping_name.lower():
                return topping.serialize()
        return "Topping does not exist"

    def get_menu_items(self):
        menu = {}
        for item in self.pizzas:
            menu[item.name] = item.price
        for item in self.drinks:
            menu[item.name] = item.price
        for item in self.toppings:
            menu[item.name] = item.price
        return menu

    def get_pizzas(self):
        pizzas = {}
        for item in self.pizzas:
            pizzas[item.name] = item.price
        return pizzas

    def get_drinks(self):
        drinks = {}
        for item in self.drinks:
            drinks[item.name] = item.price
        return drinks

    def get_toppings(self):
        toppings = {}
        for item in self.toppings:
            toppings[item.name] = item.price
        return toppings


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def print_price(self):
        print(self.price)

    def __str__(self):
        return "Name: " + self.name + " Price: " + str(self.price)

    def serialize(self):
        return {"name": self.name,
                "price": self.price}


class Drink(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)


class Pizza(MenuItem):
    def __init__(self, pizza_type, price):
        MenuItem.__init__(self, pizza_type, price)


class Topping(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)


class Size(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)


class CustomPizza(MenuItem):
    def __init__(self, id, size, toppings):
        self.id = id
        self.size = size
        self.toppings = toppings
        self.price = self.calculate_price()
        MenuItem.__init__(self, "custom_pizza " + str(self.id), self.price)

    def calculate_price(self):
        price = self.size.price
        for topping in self.toppings:
            price += topping.price

        return price

    def serialize(self):
        return {"size": {"name": self.size, "price": self.price, "toppings": self.toppings}}

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

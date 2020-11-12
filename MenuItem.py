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

    def get_pizza(self, pizza_name):
        for pizza in self.pizzas:
            if pizza.name.lower() == pizza_name.lower():
                return pizza

    def get_drink(self, drink_name):
        for drink in self.drinks:
            if drink.name.lower() == drink_name.lower():
                return drink

    def get_topping(self, topping_name):
        for topping in self.toppings:
            if topping.name.lower() == topping_name.lower():
                return topping

    def get_menu_items(self):
        menus = {"pizza": self.get_pizzas(), "topping": self.get_toppings(),
                 "drink": self.get_drinks()}
        return menus

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

    def serialize(self):
        return {"name": self.name,
                "price": self.price}

    def __str__(self):
        return 'MenuItem(name='+self.name+', price='+str(self.price) + ')'


class Drink(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def __str__(self):
        return 'Drink(name='+self.name+', price='+str(self.price) + ')'


class Topping(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def __str__(self):
        return 'Topping(name='+self.name+', price='+str(self.price) + ')'


class Size(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def __str__(self):
        return 'Size(name='+self.name+', price='+str(self.price) + ')'


class PredefinedPizza(MenuItem):
    def __init__(self, name, price):
        MenuItem.__init__(self, name, price)

    def __str__(self):
        return 'PredefinedPizza(name='+self.name+', price='+str(self.price) + ')'


class Pizza(MenuItem):
    def __init__(self, pizza_type, size):
        self.pizza_type = pizza_type
        self.size = size
        self.price = pizza_type.price + self.size.price
        MenuItem.__init__(self, self.size.name + "-" +
                          pizza_type.name, self.price)

    def serialize(self):
        return {"name": self.name, "size": {"name": self.size.name, "price": self.size.price}, "price": self.price}

    def __str__(self):
        return 'Pizza(name='+self.name+', price='+str(self.price)+', type=' + str(self.pizza_type) + ', size=' + str(self.size) + ')'


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
        return {"name": self.name, "size": {"name": self.size.name, "price": self.size.price}, "price": self.price, "toppings": self.get_all_toppings_serialized()}

    def get_all_toppings_serialized(self):
        topping_list = []
        for topping in self.toppings:
            topping_list.append(topping.serialize())
        return topping_list

    def get_all_str_toppings(self):
        topping_list = []
        for topping in self.toppings:
            topping_list.append(str(topping))
        return topping_list

    def __str__(self):
        return 'CustomPizza(name='+self.name+', price='+str(self.price) + ', size=' + str(self.size) + ', toppings=' + str(self.get_all_str_toppings()) + ')'

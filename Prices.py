from MenuItem import Pizza
from MenuItem import Drink
from MenuItem import Topping
from MenuItem import Menu


def priceReader(filename):
    d = dict()
    with open("prices/" + filename) as f:
        for line in f:
            (key, val) = line.split()
            d[key] = float(val)
    return d


drinkPrices = priceReader("drinks.txt")
toppingPrices = priceReader("toppings.txt")
pizzaPrices = priceReader("pizzas.txt")

# menu_items = {}
# pizzas = []
# drinks = []
menu = Menu()

for key in pizzaPrices:
    p = Pizza(key, pizzaPrices[key])
    # pizzas.append(p)
    menu.add_pizza(p)

for key in drinkPrices:
    d = Drink(key, drinkPrices[key])
    # drinks.append(d)
    menu.add_drink(d)

for key in toppingPrices:
    d = Topping(key, toppingPrices[key])
    menu.add_topping(d)

# menu_items["pizzas"] = pizzas
# menu_items["drinks"] = drinks

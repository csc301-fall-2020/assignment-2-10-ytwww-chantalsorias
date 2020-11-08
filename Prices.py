from MenuItem import PredefinedPizza, Pizza, Drink, Topping, Menu


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

menu = Menu()

for key in pizzaPrices:
    p = PredefinedPizza(key, pizzaPrices[key])
    menu.add_pizza(p)

for key in drinkPrices:
    d = Drink(key, drinkPrices[key])
    menu.add_drink(d)

for key in toppingPrices:
    d = Topping(key, toppingPrices[key])
    menu.add_topping(d)

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

# Use the following line to access the dictionary
# from Prices import drinks, toppings, pizzas

# print(drinks)
# print(toppings)
# print(pizzas)

def priceReader(filename):
    d = dict()
    with open("prices/" + filename) as f:
        for line in f:
            (key, val) = line.split()
            d[key] = float(val)
    return d

drinks = priceReader("drinks.txt")
toppings = priceReader("toppings.txt")
pizzas = priceReader("pizzas.txt")

# Use the following line to access the dictionary
# from readPrices import drinks, toppings, pizzas

# print(drinks)
# print(toppings)
# print(pizzas)

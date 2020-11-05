from flask import Flask, request
from MenuItem import Pizza
from MenuItem import Drink
from MenuItem import Menu
from MenuItem import CustomPizza
from MenuItem import Size
from MenuItem import Topping
from Order import OrderItem
from Order import Orders

app = Flask("Assignment 2")

menu_items = {}

pepporoni_pizza = Pizza("pepperonipizza", 7.99)
pizzas = []
pizzas.append(pepporoni_pizza)

menu_items["pizzas"] = pizzas


pepsi = Drink("pepsi", 1.88)
coke = Drink("coke", 1.88)
dietpepsi = Drink("dietpepsi", 1.88)
drinks = []
drinks.append(pepsi)
drinks.append(coke)
drinks.append(dietpepsi)

menu_items["drinks"] = drinks

order_number = 1
order_items = []
orders = Orders()
menu = Menu()
menu.add_pizza(pepporoni_pizza)
menu.add_drink(pepsi)
menu.add_drink(dietpepsi)
menu.add_drink(coke)


def generate_new_order_number():
    global order_number
    new_order_number = order_number
    order_number += 1
    return str(new_order_number)


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


# routes
@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


@app.route('/menu')
def get_menu_items():
    # pizzas = get_pizzas()
    # drinks = get_drinks()
    # menu = merge_two_dicts(pizzas, drinks)
    # return menu
    return menu.get_menu_items()


# @app.route('/menu/<menu_item_type>/<item_name>')
# def get_menu_item(menu_item_type, item_name):
    # for item in menu_items[menu_item_type]:
    #     if item.name == item_name:
    #         return str(item.price)
@app.route('/menu/pizzas/<pizza_name>')
def get_pizza_price(pizza_name):
    return str(menu.find_pizza(pizza_name).price)


@app.route('/menu/drinks/<drink_name>')
def get_drink_price(drink_name):
    return str(menu.find_drink(drink_name).price)


@app.route('/menu/toppings/<topping_name>')
def get_topping_price(topping_name):
    return str(menu.find_topping(topping_name).price)


@app.route('/menu/pizzas')
def get_pizzas():
    return menu.get_pizzas()
    # pizzas = {}
    # for item in menu_items["pizzas"]:
    #     pizzas[item.name] = item.price
    # return pizzas


@app.route('/menu/drinks')
def get_drinks():
    return menu.get_drinks()
    # drinks = {}
    # for item in menu_items["drinks"]:
    #     drinks[item.name] = item.price
    # return drinks

# order routes


@app.route('/menu/toppings')
def get_toppings():
    return menu.get_toppings()


@app.route('/order')
def new_order():
    new_order = orders.new_order()
    # orders.add_order(new_order)
    return "Your order number is " + str(new_order.order_number)
    # # return generate_new_order_number()


@app.route('/order/<order_number>', methods=['GET', 'DELETE'])
def get_order(order_number):
    order = orders.find_order(int(order_number))
    if isinstance(order, str):
        return order
    if request.method == 'GET':
        return order.display_items()
        # items_in_order = {}
        # for item in order_items:
        #     if item.order_number == order_number:
        #         if item.item.name in items_in_order:
        #             items_in_order[item.item.name]["quantity"] += 1
        #         else:
        #             items_in_order[item.item.name] = {
        #                 "price": item.item.price, "quantity": 1}

        # return items_in_order

    if request.method == 'DELETE':
        orders.remove_order(order)
        # for order_item in order_items:
        #     if order_item.order_number == order_number:
        #         order_items.remove(order_item)
        return "order " + order_number + " canceled!"


# @app.route('/order/<order_number>/drink/<item_name>')
# def add_item_to_order(order_number, item_name):
#     # item_to_add = {}
#     # for drink in menu_items["drinks"]:
#     #     if drink.name == item_name:
#     #         item_to_add = drink
#     #         break

#     # new_order_item = OrderItem(order_number, item_to_add)
#     # order_items.append(new_order_item)
#     return "item added!"


@app.route('/order/<order_number>/drink', methods=['POST'])
def add_drink_to_order(order_number):
    order = orders.find_order(int(order_number))
    if isinstance(order, str):
        return order
    req_data = request.get_json()
    drink_name = req_data['name']
    drink_price = req_data['price']
    # drink = menu.find_drink(item_name)
    order.add_item(Drink(drink_name, drink_price))

    # drink_to_add = Drink(drink_name, drink_price)

    # new_order_item = OrderItem(order_number, drink_to_add)
    # order_items.append(new_order_item)
    return str(drink_name) + " item added!"


@app.route('/order/<order_number>/pizza', methods=['POST'])
def add_pizza_to_order(order_number):
    order = orders.find_order(int(order_number))
    if isinstance(order, str):
        return order
    req_data = request.get_json()
    pizza_name = req_data['name']
    pizza_price = req_data['price']
    order.add_item(Pizza(pizza_name, pizza_price))
    # pizza_to_add = Pizza(pizza_name, pizza_price)

    # new_order_item = OrderItem(order_number, pizza_to_add)
    # order_items.append(new_order_item)
    return str(pizza_name) + " item added!"


@app.route('/order/<order_number>/custompizza', methods=['POST'])
def add_custom_pizza_to_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if isinstance(order, str):
        return order
    # Otherwise add pizza
    req_data = request.get_json()
    pizza_id = req_data['id']
    pizza_size = req_data['size']
    size = Size(pizza_size["name"], pizza_size["price"])
    pizza_toppings = req_data['toppings']
    toppings = []
    for topping in pizza_toppings:
        toppings.append(Topping(topping["name"], topping["price"]))
    print(pizza_size)
    print(pizza_toppings)
    order.add_item(CustomPizza(pizza_id, size, toppings))

    return "custom pizza added!"


if __name__ == "__main__":
    app.run()

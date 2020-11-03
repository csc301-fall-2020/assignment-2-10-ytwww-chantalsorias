from flask import Flask, request
from MenuItem import Pizza
from MenuItem import Drink
from Order import OrderItem

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
    pizzas = get_pizzas()
    drinks = get_drinks()
    menu = merge_two_dicts(pizzas, drinks)
    return menu


@app.route('/menu/<menu_item_type>/<item_name>')
def get_menu_item(menu_item_type, item_name):
    for item in menu_items[menu_item_type]:
        if item.name == item_name:
            return str(item.price)


@app.route('/menu/pizzas')
def get_pizzas():
    pizzas = {}
    for item in menu_items["pizzas"]:
        pizzas[item.name] = item.price
    return pizzas


@app.route('/menu/drinks')
def get_drinks():
    drinks = {}
    for item in menu_items["drinks"]:
        drinks[item.name] = item.price
    return drinks

# order routes


@app.route('/order')
def new_order():
    return generate_new_order_number()


@app.route('/order/<order_number>', methods=['GET', 'DELETE'])
def get_order(order_number):
    if request.method == 'GET':
        items_in_order = {}
        for item in order_items:
            if item.order_number == order_number:
                if item.item.name in items_in_order:
                    items_in_order[item.item.name]["quantity"] += 1
                else:
                    items_in_order[item.item.name] = {
                        "price": item.item.price, "quantity": 1}

        return items_in_order

    if request.method == 'DELETE':
        for order_item in order_items:
            if order_item.order_number == order_number:
                order_items.remove(order_item)
        return "order " + order_number + " canceled!"


@app.route('/order/<order_number>/drink/<item_name>')
def add_item_to_order(order_number, item_name):
    item_to_add = {}
    for drink in menu_items["drinks"]:
        if drink.name == item_name:
            item_to_add = drink
            break

    new_order_item = OrderItem(order_number, item_to_add)
    order_items.append(new_order_item)
    return "item added!"


@app.route('/order/<order_number>/drink', methods=['POST'])
def add_drink_to_order(order_number):
    req_data = request.get_json()
    drink_name = req_data['name']
    drink_price = req_data['price']

    drink_to_add = Drink(drink_name, drink_price)

    new_order_item = OrderItem(order_number, drink_to_add)
    order_items.append(new_order_item)
    return str(drink_name) + " item added!"


@app.route('/order/<order_number>/pizza', methods=['POST'])
def add_pizza_to_order(order_number):
    req_data = request.get_json()
    pizza_name = req_data['name']
    pizza_price = req_data['price']

    pizza_to_add = Pizza(pizza_name, pizza_price)

    new_order_item = OrderItem(order_number, pizza_to_add)
    order_items.append(new_order_item)
    return str(pizza_name) + " item added!"


if __name__ == "__main__":
    app.run()

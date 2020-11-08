from flask import Flask, request
from MenuItem import Pizza
from MenuItem import Drink
from MenuItem import Menu
from MenuItem import CustomPizza
from MenuItem import Size
from MenuItem import Topping
from Order import OrderItem, Orders
from Prices import menu


app = Flask("Assignment 2")

order_number = 1
order_items = []
orders = Orders()


def format(d):
    'Convert a dict to a more readible format'
    res = ""
    for key in d:
        res += "%-12s%-12s\n" % (key, d[key])
    return res

# routes


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


# ---------- menu routes ----------


@app.route('/menu')
def get_menu_items():
    res = "      Menu\n"
    menus = menu.get_menu_items()
    for title in menus:
        res += "\n     " + title + "\n" + format(menus[title])
    return res


@app.route('/menu/pizzas/<pizza_name>')
def get_pizza_price(pizza_name):
    pizza = menu.find_pizza(pizza_name)
    if (not pizza):
        return "Pizza does not exist", 400
    return str(pizza.price)


@app.route('/menu/drinks/<drink_name>')
def get_drink_price(drink_name):
    drink = menu.find_drink(drink_name)
    if (not drink):
        return "Drink does not exist", 400
    return str(drink.price)


@app.route('/menu/toppings/<topping_name>')
def get_topping_price(topping_name):
    topping = menu.find_topping(topping_name)
    if (not topping):
        return "Topping does not exist", 400
    return str(topping.price)


@app.route('/menu/pizzas')
def get_pizzas():
    return format(menu.get_pizzas())


@app.route('/menu/drinks')
def get_drinks():
    return format(menu.get_drinks())


@app.route('/menu/toppings')
def get_toppings():
    return format(menu.get_toppings())

# ---------- order routes ----------


@app.route('/order')
def new_order():
    new_order = orders.new_order()
    return "New order started:\nYour order number is " + str(new_order.order_number)


@app.route('/order/<order_number>', methods=['GET', 'DELETE'])
def get_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if (not order):
        return "order does not exist", 400
    # If GET, display items in order
    if request.method == 'GET':
        return order.display_items()
    # If DELETE, delete order
    if request.method == 'DELETE':
        orders.remove_order(order)
        return "order " + order_number + " canceled!"


@app.route('/order/<order_number>/drink', methods=['POST', 'DELETE'])
def add_drink_to_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if (not order):
        return "order does not exist", 400
    # Add drink if POST
    req_data = request.get_json()
    drink_name = req_data['name']
    if request.method == 'POST':
        drink_price = req_data['price']
        order.add_item(Drink(drink_name, drink_price))
        return str(drink_name) + " item added!"
    # Remove drink if DELETE
    elif request.method == 'DELETE':
        order.remove_item(drink_name)
        return str(drink_name) + " item removed!"


@app.route('/order/<order_number>/pizza', methods=['POST', 'DELETE'])
def add_pizza_to_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if (not order):
        return "order does not exist", 400
    # Add pizza if POST
    req_data = request.get_json()
    pizza_name = req_data['name']
    if request.method == 'POST':
        pizza_size = menu.find_pizza(req_data['size'])
        if (not pizza_size):
            return "Size does not exist", 400
        predefined_pizza = menu.find_pizza(pizza_name)
        if (not predefined_pizza):
            return "Pizza does not exist", 400

        # pizza_price = req_data['price']
        order.add_item(Pizza(predefined_pizza, pizza_size))
        return str(pizza_size.name + "-" + pizza_name) + " item added!"
    # Remove pizza if DELETE
    elif request.method == 'DELETE':
        order.remove_item(pizza_name)
        return str(pizza_name) + " item removed!"


@app.route('/order/<order_number>/custompizza', methods=['POST', 'DELETE'])
def add_custom_pizza_to_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if (not order):
        return "order does not exist", 400
    # Add custom pizza if POST
    req_data = request.get_json()
    if request.method == 'POST':
        pizza_id = order.custom_pizza_number
        pizza_size = req_data['size']
        size = Size(pizza_size["name"], pizza_size["price"])
        pizza_toppings = req_data['toppings']
        toppings = []
        for topping in pizza_toppings:
            toppings.append(Topping(topping["name"], topping["price"]))
        order.add_item(CustomPizza(pizza_id, size, toppings))

        return "custom pizza added!"
    # Remove custom pizza if DELETE
    elif request.method == 'DELETE':
        pizza_name = req_data['name']
        order.remove_item(pizza_name)
        return str(pizza_name) + " item removed!"


# ---------- checkout routes ----------
@app.route('/checkout/pickup', methods=['POST'])
def pickup_checkout():
    if request.method == 'POST':
        return "Pickup"

@app.route('/checkout/inhouse', methods=['POST'])
def in_house_checkout():
    if request.method == 'POST':
        return checkout(request, "in-house delivery")


@app.route('/checkout/ubereats', methods=['POST'])
def ubereats_checkout():
    if request.method == 'POST':
        return checkout(request, "UberEats")


def checkout(req_data, delivery_method):
    req_data = request.get_json()
    order_number = req_data['order_number']
    order = orders.find_order(int(order_number))
    # Check if order exists
    if (not order):
        return "order does not exist", 400
    # Check if order has been checkout already
    if order.order_complete == True:
        return "Order " + str(order_number) + " is already complete", 400
    # Check if order has items
    if not order.has_items():
        return "Order " + str(order_number) + " does not have any items", 400
    # Otherwise, checkout
    order.checkout()
    address = req_data['address']
    order_details = req_data['order_details']
    return "Order " + str(order_number) + " complete. Delivering to " + address + " via " + delivery_method

#TODO: Foodora


if __name__ == "__main__":
    app.run()

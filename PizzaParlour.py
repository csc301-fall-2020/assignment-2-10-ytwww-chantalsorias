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

# routes
@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


@app.route('/menu')
def get_menu_items():
    return menu.get_menu_items()


@app.route('/menu/pizzas/<pizza_name>')
def get_pizza_price(pizza_name):
    pizza = menu.find_pizza(pizza_name)
    if "price" in pizza:
        return str(pizza["price"])
    return pizza


@app.route('/menu/drinks/<drink_name>')
def get_drink_price(drink_name):
    drink = menu.find_drink(drink_name)
    if "price" in drink:
        return str(drink["price"])
    return drink


@app.route('/menu/toppings/<topping_name>')
def get_topping_price(topping_name):
    topping = menu.find_topping(topping_name)
    if "price" in topping:
        return str(topping["price"])
    return topping


@app.route('/menu/pizzas')
def get_pizzas():
    return menu.get_pizzas()


@app.route('/menu/drinks')
def get_drinks():
    return menu.get_drinks()

# order routes


@app.route('/menu/toppings')
def get_toppings():
    return menu.get_toppings()

# Create a new order


@app.route('/order')
def new_order():
    new_order = orders.new_order()
    return "Your order number is " + str(new_order.order_number)


@app.route('/order/<order_number>', methods=['GET', 'DELETE'])
def get_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if isinstance(order, str):
        return order
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
    if isinstance(order, str):
        return order
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
    if isinstance(order, str):
        return order
    # Add pizza if POST
    req_data = request.get_json()
    pizza_name = req_data['name']
    if request.method == 'POST':
        pizza_price = req_data['price']
        order.add_item(Pizza(pizza_name, pizza_price))
        return str(pizza_name) + " item added!"
    # Remove pizza if DELETE
    elif request.method == 'DELETE':
        order.remove_item(pizza_name)
        return str(pizza_name) + " item removed!"


@app.route('/order/<order_number>/custompizza', methods=['POST', 'DELETE'])
def add_custom_pizza_to_order(order_number):
    order = orders.find_order(int(order_number))
    # Check if order exists
    if isinstance(order, str):
        return order
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


if __name__ == "__main__":
    app.run()

from PizzaParlour import app
from MenuItem import Drink, Pizza, CustomPizza
import Shell as s
import json
from Prices import drinkPrices, pizzaPrices, toppingPrices
HEADERS = {'Content-Type': 'application/json'}


def test_parse():
    assert s.parse("   1    DrINK    DR.pepPer      ") == [
        "1", "drink", "drpepper"]

def test_format():
    assert s.format({"vegetarian": "3.99", "margherita": "7.99"}
                    ) == "%-12s%-12s\n%-12s%-12s\n" % ("vegetarian", "3.99", "margherita", "7.99")

# Tests for menu
def test_menu_wrong_category():
    assert s.menu_helper(
        ["dessert"]) == "Please enter one of the following as category:  pizza  topping  drink"

def test_new_wrong_input():
    assert s.add_helper(
        ["drink", "coke"]) == "Please specify order number, category and item name. E.g. add 1 drink coke, add 1 custompizza small beef"

# Tests for add
def test_add_incomplete_input():
    assert s.add_helper(
        ["drink", "coke"]) == "Please specify order number, category and item name. E.g. add 1 drink coke, add 1 custompizza small beef"


def test_add_wrong_category():
    assert s.add_helper(["1", "dessert", "coke"]
                        ) == "Please enter one of the following as category:  pizza  topping  drink custompizza"

# Tests for server
def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


def test_new_order():
    response = app.test_client().get('/order')

    assert response.status_code == 200
    assert response.data == b'Your order number is 1'


def test_add_drink():
    drink = Drink("coke", 1.88).serialize()

    response = app.test_client().post('/order/1/drink', json=drink, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'coke item added!'


def test_add_pizza():
    pizza = Pizza("neapolitan", 7.99).serialize()

    response = app.test_client().post('/order/1/pizza', json=pizza, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'neapolitan item added!'


def test_add_custom_pizza():
    pizza = {"size": {"name": "small", "price": 6.25},
             "toppings": [{"name": "beef", "price": 2.5}]}

    response = app.test_client().post(
        '/order/1/custompizza', json=pizza, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b"custom pizza added!"


def test_remove_drink():
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().delete('/order/1/drink', json=drink, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'coke item removed!'


def test_cancel_order():
    response = app.test_client().delete('/order/1')

    assert response.status_code == 200
    assert response.data == b'order 1 canceled!'

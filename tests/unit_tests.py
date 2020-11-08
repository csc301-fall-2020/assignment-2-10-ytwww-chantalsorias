from PizzaParlour import app, format
from MenuItem import Drink, Pizza, CustomPizza
import Shell as s
import json
from Prices import drinkPrices, pizzaPrices, toppingPrices
HEADERS = {'Content-Type': 'application/json'}


def test_parse():
    assert s.parse("   1    DrINK    DR.pepPer      ") == [
        "1", "drink", "drpepper"]


def test_parse_address():
    assert s.parse("   1    DrINK    DR.pepPer      (40 St George St, Toronto, ON M5S 2E4)") == [
        "1", "drink", "drpepper", "40 St George St, Toronto, ON M5S 2E4"]

def test_valid_item_drink():
    assert s.isValidItem("drink", "coke") == True

def test_valid_item_pizza():
    assert s.isValidItem("pizza", "margherita") == True

def test_valid_item_topping():
    assert s.isValidItem("topping", "olives") == True

def test_valid_item_false():
    assert s.isValidItem("drink", "pizza") == False

def test_format():
    assert format({"vegetarian": "3.99", "margherita": "7.99"}
                  ) == "%-12s%-12s\n%-12s%-12s\n" % ("vegetarian", "3.99", "margherita", "7.99")

# Tests for menu
def test_menu_too_many_arguments():
    assert s.menu_helper(["drink", "coke", "water"]
                         ) == "Please type \"? menu\" to see usage."


def test_menu_wrong_category():
    assert s.menu_helper(
        ["dessert"]) == "Please enter one of the following as category:  pizza  topping  drink"


def test_menu_wrong_item_name():
    assert s.menu_helper(
        ["drink", "rootbeer"]) == "Drink does not exist."

# Tests for add
def test_add_incomplete_input():
    assert s.add_helper(
        ["drink", "coke"]) == "Please type \"? add\" to see usage."


def test_add_wrong_category():
    assert s.add_helper(["1", "dessert", "coke"]
                        ) == "Please type \"? add\" to see usage."


def test_cart_wrong_input():
    assert s.cart_helper([]) == "usage: cart <order-number>"


def test_new_order_wrong_input():
    assert s.new_helper(["10"]) == "usage: new"


def test_remove_wrong_input():
    assert s.remove_helper(
        []) == "Please specify order number, category, and name. E.g. remove 1 drink coke, remove 1 custompizza small"


def test_cancel_wrong_input():
    assert s.cancel_helper([]) == "Please specify order number. E.g. cancel 1"

def test_checkout_wrong_input():
    assert s.checkout_helper([]) == "Please type \"? checkout\" to see usage."

def test_checkout_wrong_carrier():
    assert s.checkout_helper(["1", "delivery", "skipthedishes", "this is a address"]) == "Please type \"? checkout\" to see usage."

# Tests for server
def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


def test_new_order():
    response = app.test_client().get('/order')

    assert response.status_code == 200
    assert response.data == b'New order started:\nYour order number is 1'


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

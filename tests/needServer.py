from PizzaParlour import app
from MenuItem import Drink, Pizza, CustomPizza
import Shell as s
import json
from Prices import drinkPrices, pizzaPrices, toppingPrices
HEADERS = {'Content-Type': 'application/json'}


def test_full_menu(): # pass if server is running
    res = "The full menu:\npizzas\n" + s.format(app.test_client().get("/menu/pizzas").json) + "\ntoppings\n" + s.format(
        app.test_client().get("/menu/toppings").json) + "\ndrinks\n" + s.format(app.test_client().get("/menu/drinks").json)
    assert s.menu_helper([]) == res


def test_drink_menu(): # pass if server is running
    assert s.menu_helper(["drink"]) == s.format(
        app.test_client().get("/menu/drinks").json)


def test_pizza_menu(): # pass if server is running
    assert s.menu_helper(["pizza"]) == s.format(
        app.test_client().get("/menu/pizzas").json)


def test_topping_menu(): # pass if server is running
    assert s.menu_helper(["topping"]) == s.format(
        app.test_client().get("/menu/toppings").json)

def test_cli_add_drink(): # pass if server is running
    s.new_helper([])
    assert s.add_helper(["1", "drink", "coke"]) == "coke item added!"


def test_cli_add_pizza(): # pass if server is running
    assert s.add_helper(["1", "pizza", "neapolitan"]
                        ) == "neapolitan item added!"


def test_cli_add_custom_pizza(): # pass if server is running
    assert s.add_helper(["1", "custompizza", "small", "beef",
                         "mushrooms"]) == "custom pizza added!"

def test_menu_item_price(): # pass if server is not running, fail otherwise
    assert app.test_client().get('/menu/drinks/water').data == b"1.88"

def test_menu_wrong_item_name(): # pass if server is not running, fail otherwise
    assert s.menu_helper(["drink", "rootbeer"]
                         ) == "Please enter a valid item name."

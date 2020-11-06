from PizzaParlour import app
from MenuItem import Drink, Pizza
import Shell as s
import json
HEADERS = {'Content-Type': 'application/json'}

# Tests for Shell without a server
def test_parse():
    assert s.parse("   1    DrINK    DR.pepPer      ") == ["1", "drink", "drpepper"]

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


def test_remove_drink():
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().delete('/order/1/drink', json=drink, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'coke item removed!'


def test_cancel_order():
    response = app.test_client().delete('/order/1')

    assert response.status_code == 200
    assert response.data == b'order 1 canceled!'

# # Tests for Shell with a server
# def test_full_menu():
#     # assert menu_helper(["menu"]) == ["1", "drink", "coke"]

# def test_pizza_menu():
#     assert True

# def test_drink_menu():
#     assert True

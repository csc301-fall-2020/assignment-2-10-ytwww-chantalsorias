from PizzaParlour import app, format
from MenuItem import Drink, Pizza, CustomPizza, PredefinedPizza, Size
import Shell as s
import json
from Prices import drinkPrices, pizzaPrices, toppingPrices
import csv
import io
HEADERS = {'Content-Type': 'application/json'}

# Tests for shell


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


def test_requester_wrong_method():
    assert s.requester(("paste", "")) == "Please provide a correct method."


def test_menu_too_many_arguments():
    assert s.menu_helper(["drink", "coke", "water"]
                         ) == ("", "Please type \"? menu\" to see usage.")


def test_menu_wrong_category():
    assert s.menu_helper(
        ["dessert"]) == ("", "Please enter one of the following as category:  pizza  topping  drink")


def test_menu_wrong_item_name():
    assert s.menu_helper(
        ["drink", "rootbeer"]) == ("", "Drink does not exist.")


def test_menu_by_category_drinks():
    assert s.menu_helper(
        ["drink"]) == ("get", "http://127.0.0.1:5000/menu/drinks")


def test_menu_by_category_pizzas():
    assert s.menu_helper(
        ["pizza"]) == ("get", "http://127.0.0.1:5000/menu/pizzas")


def test_menu_by_category_toppings():
    assert s.menu_helper(
        ["topping"]) == ("get", "http://127.0.0.1:5000/menu/toppings")


def test_menu_by_item_drink():
    assert s.menu_helper(
        ["drink", "coke"]) == ("get", "http://127.0.0.1:5000/menu/drinks/coke")


def test_menu_by_item_pizza():
    assert s.menu_helper(
        ["pizza", "vegetarian"]) == ("get", "http://127.0.0.1:5000/menu/pizzas/vegetarian")


def test_menu_by_item_topping():
    assert s.menu_helper(
        ["topping", "olives"]) == ("get", "http://127.0.0.1:5000/menu/toppings/olives")


def test_add_incomplete_input():
    assert s.add_helper(
        ["drink", "coke"]) == ("", "Please type \"? add\" to see usage.")


def test_add_wrong_category():
    assert s.add_helper(["1", "dessert", "coke"]
                        ) == ("", "Please type \"? add\" to see usage.")


def test_shell_add_drink():
    assert s.add_helper(["1", "drink", "coke"]
                        ) == ("post", "http://127.0.0.1:5000/order/1/drink", {"name": "coke", "price": drinkPrices["coke"]})


def test_shell_add_preset_pizza():
    assert s.add_helper(["1", "pizza", "margherita", "small"]
                        ) == ("post", "http://127.0.0.1:5000/order/1/pizza", {"name": "margherita", "price": pizzaPrices["margherita"], "size": "small"})


def test_shell_add_custom_pizza():
    assert s.add_helper(["1", "custompizza", "small", "beef"]
                        ) == ("post", "http://127.0.0.1:5000/order/1/custompizza", {"size": {"name": "small",
                                                                                             "price": pizzaPrices["small"]}, "toppings": [{"name": "beef", "price": toppingPrices["beef"]}]})


def test_cart_wrong_input():
    assert s.cart_helper([]) == ("", "usage: cart <order-number>")


def test_cart_correct_input():
    assert s.cart_helper(["1"]) == (
        "get", "http://127.0.0.1:5000/order/1")


def test_new_order_wrong_input():
    assert s.new_helper(["10"]) == ("", "usage: new")


def test_new_order_correct_input():
    assert s.new_helper([]) == ("get", "http://127.0.0.1:5000/order")


def test_remove_wrong_input():
    assert s.remove_helper(
        []) == ("", "Please type \"? remove\" to see usage.")


def test_remove_wrong_pizza_input():
    assert s.remove_helper(
        ["1", "pizza", "vegetarian"]) == ("", "Usage: remove <order-number> pizza <name> <size>")


def test_remove_wrong_category():
    assert s.remove_helper(
        ["1", "dessert", "applepie"]) == ("", "Please enter one of the following as category:  pizza  custompizza  drink")


def test_remove_correct_input():
    assert s.remove_helper(
        ["1", "drink", "coke"]) == ("deletedata", "http://127.0.0.1:5000/order/1/drink", {"name": "coke"})


def test_remove_correct_input_pizza():
    assert s.remove_helper(
        ["1", "pizza", "vegetarian", "large"]) == ("deletedata", "http://127.0.0.1:5000/order/1/pizza", {"name": "large-vegetarian"})


def test_cancel_wrong_input():
    assert s.cancel_helper([]) == (
        "", "Please specify order number. E.g. cancel 1")


def test_cancel_correct_input():
    assert s.cancel_helper(["1"]) == (
        "delete", "http://127.0.0.1:5000/order/1")


def test_checkout_wrong_input():
    assert s.checkout_helper([]) == (
        "", "Please type \"? checkout\" to see usage.")


def test_checkout_wrong_carrier():
    assert s.checkout_helper(["1", "delivery", "skipthedishes",
                              "this is a address"]) == ("", "Please type \"? checkout\" to see usage.")


def test_shell_checkout_pickup():
    assert s.checkout_helper(["1", "pickup"]) == (
        "post", "http://127.0.0.1:5000/checkout/pickup", {"order_number": 1})


def test_checkout_delivery():
    item = {"order_number": 1, "carrier": "ubereats",
            "address": "27 King's College Cir, Toronto, ON M5S"}
    assert s.checkout_helper(["1", "delivery", "ubereats", "27 King's College Cir, Toronto, ON M5S"]) == (
        "get", "http://127.0.0.1:5000/order/1", item)


def test_delivery_csv():
    item = {"order_number": 1, "carrier": "foodora",
            "address": "27 King's College Cir, Toronto, ON M5S"}
    details = str({"subtotal": 1.88, "total": 2.12,
                   "water": {"price": 1.88, "quantity": 1}})
    fullitem = item
    fullitem["order_details"] = details
    csv_columns = ['order_number', "carrier", 'address', 'order_details']
    csvfile = io.StringIO()
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerow(fullitem)
    csv_string = csvfile.getvalue()
    assert s.delivery_helper(item, details) == (
        "postdata", "http://127.0.0.1:5000/checkout/foodora", csv_string)


def test_delivery_json():
    item = {"order_number": 1, "carrier": "ubereats",
            "address": "27 King's College Cir, Toronto, ON M5S"}
    details = {"coke": {"price": 1.66, "quantity": 1},
               "subtotal": 1.66, "total": 1.88}
    assert s.delivery_helper(item, details) == (
        "post", "http://127.0.0.1:5000/checkout/ubereats", item)


def test_shell_close():
    shell = s.PizzaShell()
    assert shell.do_q("") == True


def test_shell_menu():
    shell = s.PizzaShell()
    assert shell.do_menu("") == None


def test_shell_cart():
    shell = s.PizzaShell()
    assert shell.do_cart("1") == None


def test_shell_new():
    shell = s.PizzaShell()
    assert shell.do_new("") == None


def test_shell_add():
    shell = s.PizzaShell()
    assert shell.do_add("1 drink coke") == None


def test_shell_remove():
    shell = s.PizzaShell()
    assert shell.do_remove("1 drink coke") == None


def test_shell_checkout():
    shell = s.PizzaShell()
    assert shell.do_checkout("1 pickup") == None


def test_shell_cancel():
    shell = s.PizzaShell()
    assert shell.do_cancel("1") == None


def test_shell_emptyline():
    shell = s.PizzaShell()
    assert shell.emptyline() == None

# Tests for server


def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


def test_menu_pizza_pepperoni():
    response = app.test_client().get('/menu/pizzas/pepperoni')

    assert response.status_code == 200
    assert response.data == b'7.99'


def test_menu_pizza_does_not_exist():
    response = app.test_client().get('/menu/pizzas/hawaiian')

    assert response.status_code == 400
    assert response.data == b'Pizza does not exist'


def test_menu_drink_coke():
    response = app.test_client().get('/menu/drinks/coke')

    assert response.status_code == 200
    assert response.data == b'1.66'


def test_menu_drink_does_not_exist():
    response = app.test_client().get('/menu/drinks/rootbeer')

    assert response.status_code == 400
    assert response.data == b'Drink does not exist'


def test_menu_topping_beef():
    response = app.test_client().get('/menu/toppings/beef')

    assert response.status_code == 200
    assert response.data == b'1.35'


def test_menu_topping_does_not_exist():
    response = app.test_client().get('/menu/toppings/feta')

    assert response.status_code == 400
    assert response.data == b'Topping does not exist'


def test_menu_all_pizzas():
    response = app.test_client().get('/menu/pizzas')
    assert response.status_code == 200
    assert response.data == b'small       3.99        \nmedium      5.99        \nlarge       7.99        \npepperoni   7.99        \nmargherita  7.99        \nvegetarian  7.99        \nneapolitan  7.99        \n'


def test_menu_all_drinks():
    response = app.test_client().get('/menu/drinks')
    assert response.status_code == 200
    assert response.data == b'coke        1.66        \ndietcoke    1.66        \ncokezero    1.66        \npepsi       1.77        \ndietpepsi   1.77        \ndrpepper    1.88        \nwater       1.88        \njuice       1.88        \n'


def test_menu_all_toppings():
    response = app.test_client().get('/menu/toppings')
    assert response.status_code == 200
    assert response.data == b'olives      1.22        \ntomatoes    1.22        \nmushrooms   1.22        \njalapenos   1.22        \nchicken     1.35        \nbeef        1.35        \npepperoni   1.35        \n'


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
    pizza = {"name": "neapolitan", "price": 7.99, "size": "small"}

    response = app.test_client().post('/order/1/pizza', json=pizza, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'small-neapolitan item added!'


def test_add_pizza_size_does_not_exist():
    pizza = {"name": "neapolitan", "price": 7.99, "size": "x-large"}

    response = app.test_client().post('/order/1/pizza', json=pizza, headers=HEADERS)

    assert response.status_code == 400
    assert response.data == b'Size does not exist'


def test_add_pizza_does_not_exist():
    pizza = {"name": "hawaiian", "price": 7.99, "size": "large"}

    response = app.test_client().post('/order/1/pizza', json=pizza, headers=HEADERS)

    assert response.status_code == 400
    assert response.data == b'Pizza does not exist'


def test_add_custom_pizza():
    pizza = {"size": {"name": "small", "price": 6.25},
             "toppings": [{"name": "beef", "price": 2.5}]}

    response = app.test_client().post(
        '/order/1/custompizza', json=pizza, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b"custom pizza added!"


def test_get_order():
    response = app.test_client().get('/order/1')

    assert response.status_code == 200
    assert response.data == b'Order 1\n1. Drink(name=coke, price=1.88)\n2. Pizza(name=small-neapolitan, ' + b'price=11.98, type=PredefinedPizza(name=neapolitan, price=7.99), size=Size(na' + \
        b'me=small, price=3.99))\n3. CustomPizza(name=custom-pizza-1, price=8.75, s' + \
        b"ize=Size(name=small, price=6.25), toppings=['Topping(name=beef, price=2.5)']" + \
        b')\nSubtotal: $22.61\nTotal: $25.55\n'


def test_remove_pizza():
    pizza = {"name": "pepperoni", "price": 7.99, "size": "large"}
    response = app.test_client().post('/order/1/pizza', json=pizza, headers=HEADERS)
    pizza_to_remove = {"name": "large-pepperoni"}
    response = app.test_client().delete(
        '/order/1/pizza', json=pizza_to_remove, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'large-pepperoni item removed!'


def test_remove_drink():
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().delete('/order/1/drink', json=drink, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'coke item removed!'


def test_remove_custom_pizza():
    pizza = {"name": "custom-pizza-1"}
    response = app.test_client().delete(
        '/order/1/custompizza', json=pizza, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'custom-pizza-1 item removed!'


def test_checkout_pickup_no_items():
    app.test_client().get('/order')
    address = "123 Banana Street"
    order_details = {"dietcoke": {"price": 1.66, "quantity": 1}, "medium-pepperoni": {
        "price": 13.98, "quantity": 1}, "subtotal": 15.64, "total": 17.67}
    order = {"order_number": 2, "address": address,
             "order_details": order_details}
    response = app.test_client().post('/checkout/pickup', json=order, headers=HEADERS)

    assert response.status_code == 400
    assert response.data == b'Order 2 does not have any items'


def test_checkout_pickup_order_does_not_exist():
    drink = Drink("coke", 1.88).serialize()

    response = app.test_client().post('/order/6/drink', json=drink, headers=HEADERS)
    assert response.status_code == 400
    assert response.data == b'Order does not exist'


def test_checkout_pickup():
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().post('/order/2/drink', json=drink, headers=HEADERS)
    address = "123 Banana Street"
    order_details = {"dietcoke": {"price": 1.66, "quantity": 1}, "medium-pepperoni": {
        "price": 13.98, "quantity": 1}, "subtotal": 15.64, "total": 17.67}
    order = {"order_number": 2, "address": address,
             "order_details": order_details}
    response = app.test_client().post('/checkout/pickup', json=order, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'Order 2 complete. Ready for pickup. Subtotal is $1.88. Total is $2.12'


def test_checkout_ubereats():
    app.test_client().get('/order')
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().post('/order/3/drink', json=drink, headers=HEADERS)
    address = "123 Banana Street"
    order_details = {"dietcoke": {"price": 1.66, "quantity": 1}, "medium-pepperoni": {
        "price": 13.98, "quantity": 1}, "subtotal": 15.64, "total": 17.67}
    order = {"order_number": 3, "address": address,
             "order_details": order_details}
    response = app.test_client().post('/checkout/ubereats', json=order, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'Order 3 complete. Delivering to 123 Banana Street via UberEats. Subtotal is $1.88. Total is $2.12'


def test_checkout_ubereats_already_complete():
    app.test_client().get('/order')
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().post('/order/3/drink', json=drink, headers=HEADERS)
    address = "123 Banana Street"
    order_details = {"dietcoke": {"price": 1.66, "quantity": 1}, "medium-pepperoni": {
        "price": 13.98, "quantity": 1}, "subtotal": 15.64, "total": 17.67}
    order = {"order_number": 3, "address": address,
             "order_details": order_details}
    response = app.test_client().post('/checkout/ubereats', json=order, headers=HEADERS)

    assert response.status_code == 400
    assert response.data == b'Order 3 is already complete'


def test_checkout_foodora():
    app.test_client().get('/order')
    drink = Drink("coke", 1.88).serialize()
    response = app.test_client().post('/order/4/drink', json=drink, headers=HEADERS)
    address = "123 Banana Street"
    order_details = {"dietcoke": {"price": 1.66, "quantity": 1}, "medium-pepperoni": {
        "price": 13.98, "quantity": 1}, "subtotal": 15.64, "total": 17.67}
    order = {"order_number": 4, "address": address,
             "order_details": order_details}
    csv_columns = ['order_number', "carrier",
                                   'address', 'order_details']
    csvfile = io.StringIO()
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerow(order)
    csv_string = csvfile.getvalue()
    response = app.test_client().post(
        '/checkout/foodora', data=csv_string, headers=HEADERS)

    assert response.status_code == 200
    assert response.data == b'Order 4 complete. Delivering to 123 Banana Street via Foodora. Subtotal is $1.88. Total is $2.12'


def test_cancel_order():
    response = app.test_client().delete('/order/1')

    assert response.status_code == 200
    assert response.data == b'order 1 canceled!'

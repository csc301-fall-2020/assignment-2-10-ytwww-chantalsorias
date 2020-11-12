import cmd
import sys
import requests
import csv
import io
from Prices import drinkPrices, toppingPrices, pizzaPrices

HEADERS = {'Content-Type': 'application/json'}


class PizzaShell(cmd.Cmd):
    intro = '\nWelcome to Pizza Parlour.\nType ? to list commands. Type q to quit.\n'
    prompt = '[ Pizza Parlour ] '

    def do_menu(self, arg):
        '- show the full menu:  menu\n- show pizza menu:  menu pizza\n- show topping menu:  menu topping\n- show drink menu:  menu drink\n- Show price for a specific item:\n    menu <category> <name>\n    menu pizza vegetarian\n    menu drink coke\n    menu topping mushroom'
        res = requester(menu_helper(parse(arg)))
        print(res)

    def do_new(self, arg):
        'Start a new order:  new'
        res = requester(new_helper(parse(arg)))
        print(res)

    def do_cart(self, arg):
        'View the cart:  cart <order-number>'
        res = requester(cart_helper(parse(arg)))
        print(res)

    def do_add(self, arg):
        'Add an item to the cart\n- To add a drink\n  add <order-number> drink <name>\n- To add a predefined pizza\n  add <order-number> pizza <name> <size>\n- To add a custom pizza:\n  add <order-number> custompizza <size> <topping 1> <topping 2> ...\nExamples:\n  add 1 drink coke\n  add 1 pizza margherita medium\n  add 1 custompizza large beef mushrooms olives'
        res = requester(add_helper(parse(arg)))
        print(res)

    def do_remove(self, arg):
        'Remove 1 specified item from the cart:\nUsage:\n  remove <order-number> drink <name>\n  remove <order-number> pizza <name> <size>\n  remove <order-number> custompizza custom-pizza-<id>\n  (Find out <id> using \"cart <order-number>\")\nE.g.\n  remove 1 drink coke\n  remove 1 pizza vegetarian small\n  remove 1 custompizza custom-pizza-1'
        res = requester(remove_helper(parse(arg)))
        print(res)

    def do_checkout(self, arg):
        'Checkout the order:\n- checkout <order-number> pickup\n- checkout <order-number> delivery <carrier> (<address>)\nExamples:\n  checkout 1 pickup\n  checkout 2 delivery inhouse (6301 Silver Dart Dr, Mississauga, ON L5P 1B2)\n  checkout 3 delivery foodora (290 Bremner Blvd, Toronto, ON M5V 3L9)\n  checkout 4 delivery ubereats (27 King\'s College Cir, Toronto, ON M5S)'
        res = checkout_helper(parse(arg))
        details = requester(res)
        if res[0] == "get":
            item = res[2]
            res = requester(delivery_helper(item, details))
        else:
            res = details
        print(res)

    def do_cancel(self, arg):
        'Cancel order: cancel <order-number>'
        res = requester(cancel_helper(parse(arg)))
        print(res)

    def do_q(self, arg):
        'Exit the shell:  q'
        print('Thank you for visiting Pizza Parlour. Please come again.\n')
        return True

    def emptyline(self):
        'Prevent input from being executed again'
        return


def parse(arg):
    'Convert the user input to a list'
    raw = arg.replace('.', '')
    start = raw.find("(")
    end = raw.find(")", start)
    if start != -1:
        return (raw[:start].lower()).split() + [raw[start+1:end]]
    else:
        return (raw.lower()).split()


def requester(t):
    method = t[0]
    if method == "":
        message = t[1]
        return message
    try:
        if method == "get":
            return requests.get(t[1]).text
        elif method == "post":
            url, data = t[1], t[2]
            return requests.post(url, headers=HEADERS, json=data).text
        elif method == "postdata":
            url, data = t[1], t[2]
            return requests.post(url, headers=HEADERS, data=data).text
        elif method == "deletedata":
            url, data = t[1], t[2]
            return requests.delete(url, headers=HEADERS, json=data).text
        elif method == "delete":
            url = t[1]
            return requests.delete(url).text
        else:
            return "Please provide a correct method."
    except:
        return "Server Error."


def new_helper(L):
    if len(L) == 0:
        return "get", "http://127.0.0.1:5000/order"
    else:
        return "", "usage: new"


def cart_helper(L):
    if len(L) == 1 and L[0].isdigit():
        return "get", "http://127.0.0.1:5000/order/" + L[0]
    else:
        return "", "usage: cart <order-number>"


def menu_helper(L):
    # base route to get full menu
    url = "http://127.0.0.1:5000/menu"
    length = len(L)
    # wrong number of arguments
    if length > 2:
        return "", "Please type \"? menu\" to see usage."
    # wrong category
    elif length > 0 and L[0] not in ["topping", "pizza", "drink"]:
        return "", "Please enter one of the following as category:  pizza  topping  drink"
    # correct category but wrong item name
    elif length == 2 and not isValidItem(L[0], L[1]):
        return "", L[0].capitalize() + " does not exist."
    # route to get menu by category
    elif length == 1:
        url += "/" + L[0] + "s"
    # route to get item price
    elif length == 2:
        url += "/" + L[0] + "s/" + L[1]
    return "get", url


def add_helper(L):
    length = len(L)
    if length < 3 or not L[0].isdigit():
        return "", "Please type \"? add\" to see usage."
    orderNum, category, name = L[0], L[1], L[2]
    # add a drink
    if category == "drink" and length == 3 and isValidItem(category, L[2]):
        item = {"name": name, "price": drinkPrices[name]}
    # add a predefined pizza
    elif category == "pizza" and length == 4:
        size = L[3]
        item = {"name": name, "price": pizzaPrices[name], "size": size}
    # add a custom pizza
    elif category == "custompizza" and length >= 4:
        size = L[2]
        toppings = L[3:]
        toppings_json_list = []
        for top in toppings:
            if isValidItem("topping", top):
                top_json = {"name": top, "price": toppingPrices[top]}
                toppings_json_list.append(top_json)
            else:
                return "", "Topping " + top + " does not exist."
        item = {"size": {"name": size,
                         "price": pizzaPrices[size]}, "toppings": toppings_json_list}
    else:
        return "", "Please type \"? add\" to see usage."
    return "post", "http://127.0.0.1:5000/order/" + orderNum + "/" + category, item


def checkout_helper(L):
    if (len(L) != 2 and len(L) != 4) or (len(L) > 0 and not L[0].isdigit()):
        return "", "Please type \"? checkout\" to see usage."
    # pickup
    elif len(L) == 2 and L[1] == "pickup":
        item = {"order_number": int(L[0])}
        return "post", "http://127.0.0.1:5000/checkout/pickup", item
    # delivery
    elif len(L) == 4 and L[1] == "delivery" and L[2] in ["inhouse", "foodora", "ubereats"]:
        orderNum, carrier, address = L[0], L[2], L[3]
        item = {"order_number": int(
            L[0]), "carrier": carrier, "address": address}
        return "get", "http://127.0.0.1:5000/order/" + orderNum, item
    else:
        return "", "Please type \"? checkout\" to see usage."


def delivery_helper(item, details):
    item["order_details"] = details
    if item["carrier"] == "foodora":
        csv_columns = ['order_number', "carrier", 'address', 'order_details']
        csvfile = io.StringIO()
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerow(item)
        csv_string = csvfile.getvalue()
        return "postdata", "http://127.0.0.1:5000/checkout/" + item["carrier"], csv_string
    else:
        return "post", "http://127.0.0.1:5000/checkout/" + item["carrier"], item


def remove_helper(args):
    if len(args) < 3 or (not args[0].isdigit()):
        return "", "Please type \"? remove\" to see usage."
    order_number, category, name = args[0], args[1], args[2]
    if category not in ["drink", "pizza", "custompizza"]:
        return "", "Please enter one of the following as category:  pizza  custompizza  drink"
    if category == "pizza" and len(args) != 4:
        return "", "Usage: remove <order-number> pizza <name> <size>"
    elif category == "pizza":
        size = args[3]
        name = size + "-" + name
    item = {"name": name}
    url = "http://127.0.0.1:5000/order/" + order_number + "/" + category
    return "deletedata", url, item


def cancel_helper(args):
    if len(args) != 1 or not args[0].isdigit():
        return "", "Please specify order number. E.g. cancel 1"
    order_number = args[0]
    url = "http://127.0.0.1:5000/order/" + order_number
    return "delete", url


def isValidItem(category, name):
    if category in ["pizza", "custompizza"]:
        return name in pizzaPrices
    elif category == "drink":
        return name in drinkPrices
    elif category == "topping":
        return name in toppingPrices
    else:
        return False


if __name__ == '__main__':
    PizzaShell().cmdloop()

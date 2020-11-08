import cmd
import sys
import requests
from Prices import drinkPrices, toppingPrices, pizzaPrices

HEADERS = {'Content-Type': 'application/json'}


class PizzaShell(cmd.Cmd):
    intro = '\nWelcome to Pizza Parlour.\nType ? to list commands. Type q to quit.\n'
    prompt = '[ Pizza Parlour ] '

    def do_menu(self, arg):
        '- show the full menu:  menu\n- show pizza menu:  menu pizza\n- show topping menu:  menu topping\n- show drink menu:  menu drink\n- Show price for a specific item:\n    menu <category> <name>\n    menu pizza vegetarian\n    menu drink coke\n    menu topping mushroom'
        print(menu_helper(parse(arg)))

    def do_new(self, arg):
        'Start a new order:  new'
        print(new_helper(parse(arg)))

    def do_cart(self, arg):
        'View the cart:  cart <order-number>'
        print(cart_helper(parse(arg)))

    def do_add(self, arg):
        'Add an item to the cart\n- To add a drink\n  add <order-number> drink <name>\n- To add a predefined pizza\n  add <order-number> pizza <name> <size>\n- To add a custom pizza:\n  add <order-number> custompizza <size> <topping 1> <topping 2> ...\nExamples:\n  add 1 drink coke\n  add 1 pizza margherita medium\n  add 1 custompizza large beef mushrooms olives'
        print(add_helper(parse(arg)))

    def do_remove(self, arg):
        'Remove 1 specified item from the cart:  remove <order-number> <category> <name>'
        print(remove_helper(parse(arg)))

    def do_checkout(self, arg):
        'Checkout the order:\n- checkout <order-number> pickup\n- checkout <order-number> delivery <carrier> (<address>)\nExamples:\n  checkout 1 pickup\n  checkout 2 delivery inhouse (6301 Silver Dart Dr, Mississauga, ON L5P 1B2)\n  checkout 3 delivery foodora (290 Bremner Blvd, Toronto, ON M5V 3L9)\n  checkout 4 delivery ubereats (27 King\'s College Cir, Toronto, ON M5S)'
        print(checkout_helper(parse(arg)))

    def do_cancel(self, arg):
        'Cancel order: cancal <order-number>'
        print(cancel_helper(parse(arg)))

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


def new_helper(L):
    if len(L) == 0:
        return requests.get("http://127.0.0.1:5000/order").text
    else:
        return "usage: new"


def cart_helper(L):
    if len(L) == 1 and L[0].isdigit():
        return requests.get("http://127.0.0.1:5000/order/" + L[0]).text
    else:
        return "usage: cart <order-number>"


def menu_helper(L):
    # base route to get full menu
    url = "http://127.0.0.1:5000/menu"
    length = len(L)
    # wrong number of arguments
    if length > 2:
        return "Please type \"? menu\" to see usage."
    # wrong category
    elif length > 0 and L[0] not in ["topping", "pizza", "drink"]:
        return "Please enter one of the following as category:  pizza  topping  drink"
    # correct category but wrong item name
    elif length == 2 and not isValidItem(L[0], L[1]):
        return L[0].capitalize() + " does not exist."
    # route to get menu by category
    elif length == 1:
        url += "/" + L[0] + "s"
    # route to get item price
    elif length == 2:
        url += "/" + L[0] + "s/" + L[1]
    # ask server for menu
    try:
        return requests.get(url).text
    except:
        return "Server failed to send menu."


def add_helper(L):
    length = len(L)
    if length < 3 or not L[0].isdigit():
        return "Please type \"? add\" to see usage."
    orderNum, category = L[0], L[1]
    # add a drink
    if category == "drink" and length == 3:
        name = L[2]
        item = {"name": name, "price": drinkPrices[name]}
    # add a predefined pizza
    elif category == "pizza" and length == 4:
        name, size = L[2], L[3]
        item = {"name": name, "price": pizzaPrices[name], "size": size}
    # add a custom pizza
    elif category == "custompizza" and length >= 4:
        size = L[2]
        toppings = L[3:]
        toppings_json_list = []
        for top in toppings:
            top_json = {"name": top, "price": toppingPrices[top]}
            toppings_json_list.append(top_json)
        item = {"size": {"name": name,
                         "price": pizzaPrices[name]}, "toppings": toppings_json_list}
    else:
        return "Please type \"? add\" to see usage."
    # server call
    try:
        return requests.post("http://127.0.0.1:5000/order/" + orderNum + "/" + category, headers=HEADERS, json=item).text
    except:
        return "Server failed to add this item."


def checkout_helper(L):
    if (len(L) != 2 and len(L) != 4) or (len(L) > 0 and not L[0].isdigit()):
        return "Please type \"? checkout\" to see usage."
    # pickup
    elif len(L) == 2 and L[1] == "pickup":
        return L  # TODO
    # delivery
    elif len(L) == 4 and L[1] == "delivery" and L[2] in ["inhouse", "foodora", "ubereats"]:
        address = L[3]
        if L[2] == "inhouse":
            return L[2], address  # TODO
        elif L[2] == "foodora":
            return L[2], address  # TODO
        else:
            return L[2], address  # TODO
    else:
        return "Please type \"? checkout\" to see usage."


def remove_helper(args):
    if len(args) != 3 or (not args[0].isdigit()) or (not isValidItem(args[1], args[2])):
        return "Please specify order number, category, and name. E.g. remove 1 drink coke, remove 1 custompizza small"
    else:
        try:
            order_number, category, name = args[0], args[1], args[2]
            if category not in ["topping", "pizza", "drink", "custompizza"]:
                return "Please enter one of the following as category:  pizza  drink  custompizza"
            item = {"name": name}
            r = requests.delete(
                "http://127.0.0.1:5000/order/" + order_number + "/" + category, headers=HEADERS, json=item)
            return r.text
        except:
            return "Usage: remove <order-number> <category> <name>"


def cancel_helper(args):
    if len(args) != 1 or not args[0].isdigit():
        return "Please specify order number. E.g. cancel 1"
    else:
        try:
            order_number = args[0]
            r = requests.delete("http://127.0.0.1:5000/order/" + order_number)
            return r.text
        except:
            return "Server failed to cancel the order."


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

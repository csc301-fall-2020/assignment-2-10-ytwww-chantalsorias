import cmd
import sys
import requests
from Prices import drinkPrices, toppingPrices, pizzaPrices

HEADERS = {'Content-Type': 'application/json'}
CATEGORIES = ["topping", "pizza", "drink"]


class PizzaShell(cmd.Cmd):
    intro = '\nWelcome to Pizza Parlour.\nType ? to list commands. Type q to quit.\n'
    prompt = '[ Pizza Parlour ] '
    file = None

    def do_menu(self, arg):
        '- show the full menu:  menu\n- show pizza menu:  menu pizza\n- show topping menu:  menu topping\n- show drink menu:  menu drink\n- Show price for a specific item:\n    menu <category> <name>\n    menu pizza vegetarian\n    menu drink coke\n    menu topping mushroom'
        print(menu_helper(parse(arg)))

    def do_new(self, arg):
        'Start a new order:  new'
        print(new_helper(parse(arg)))

    def do_cart(self, arg):
        'View the cart:  cart <order number>'
        print(cart_helper(parse(arg)))

    def do_add(self, arg):
        'Add an item to the cart\n\n- To add a drink or a predefined pizza:\n  add <order number> <category> <name>\n- To add a custom pizza:\n  add <order number> custompizza <size> <topping 1> <topping 2> ...\n\nExamples:\n  add 1 pizza pepperoni\n  add 1 drink coke\n  add 1 custompizza large beef mushrooms olives'
        print(add_helper(parse(arg)))

    def do_remove(self, arg):
        'Remove 1 specified item from the cart:  remove <order number> <category> <name>'
        print(remove_helper(parse(arg)))

    def do_cancel(self, arg):
        'Cancel order: cancal <order number>'
        print(cancel_helper(parse(arg)))

    def do_q(self, arg):
        'Exit the shell:  q'
        print('Thank you for visiting Pizza Parlour. Please come again.\n')
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def emptyline(self):
        'Prevent input from being executing again'
        return


def parse(arg):
    'Convert the user input to a list'
    return ((arg.lower()).replace('.', '')).split()


def new_helper(L):
    if len(L) == 0:
        return requests.get("http://127.0.0.1:5000/order").text
    else:
        return "usage: new"


def cart_helper(L):
    if len(L) == 1 and L[0].isdigit():
        return requests.get("http://127.0.0.1:5000/order/" + L[0]).text
    else:
        return "usage: cart <order number>"


def menu_helper(L):
    # base route to get full menu
    url = "http://127.0.0.1:5000/menu"
    length = len(L)
    # wrong number of arguments
    if length > 2:
        return "Please type \"? menu\" to see usage."
    # wrong category
    elif length >= 1 and L[0] not in CATEGORIES:
        return "Please enter one of the following as category:  pizza  topping  drink"
    # correct category but wrong item name
    elif length == 2 and not isValidItem(L[1]):
        return "Please enter a valid item name."
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
    res = ""
    if len(L) < 3:
        res = "Please specify order number, category and item name. E.g. add 1 drink coke, add 1 custompizza small beef"
    elif not L[0].isdigit():
        res = "Please provide an order number. Type \"? add\" to learn more"
    else:
        order_number, category, name = L[0], L[1], L[2]
        if category not in ["topping", "pizza", "drink", "custompizza"]:
            res = "Please enter one of the following as category:  pizza  topping  drink custompizza"
        else:
            if category == "topping":
                d = toppingPrices
            elif category == "pizza" or category == "custompizza":
                d = pizzaPrices
            elif category == "drink":
                d = drinkPrices
            try:
                # add a custom pizza
                if category == "custompizza":
                    toppings = L[3:]
                    toppings_json_list = []
                    for top in toppings:
                        top_json = {"name": top, "price": toppingPrices[top]}
                        toppings_json_list.append(top_json)

                    item = {"size": {"name": name,
                                     "price": d[name]}, "toppings": toppings_json_list}
                # add a drink or a predefined pizza
                else:
                    item = {"name": name, "price": d[name]}
                r = requests.post(
                    "http://127.0.0.1:5000/order/" + order_number + "/" + category, headers=HEADERS, json=item)
                res = r.text
            except:
                res = "Please enter a valid item name."
    return res


def remove_helper(args):
    if len(args) != 3:
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
            return "Usage: remove <order number> <category> <name>"


def cancel_helper(args):
    if len(args) != 1:
        return "Please specify order number. E.g. cancel 1"
    else:
        try:
            order_number = args[0]
            r = requests.delete("http://127.0.0.1:5000/order/" + order_number)
            return r.text
        except:
            return "Usage: cancel <order number>"


def isValidItem(name):
    return (name in drinkPrices) or (name in pizzaPrices) or (name in toppingPrices)


if __name__ == '__main__':
    print(isValidItem('pepperoni'))
    PizzaShell().cmdloop()

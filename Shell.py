import cmd
import sys
import requests
from Prices import drinkPrices, toppingPrices, pizzaPrices

HEADERS = {'Content-Type': 'application/json'}


class PizzaShell(cmd.Cmd):
    intro = '\nWelcome to Pizza Parlour.\nType ? to list commands. Type q to quit.\n'
    prompt = '[ Pizza Parlour ] '
    file = None
    # def preloop

    def do_menu(self, arg):
        '- show the full menu:  menu\n- show pizza menu:  menu pizza\n- show topping menu:  menu topping\n- show drink menu:  menu drink\n- Show price for a specific item:\n    menu pizza vegetarian\n    menu drink coke\n    menu topping mushroom'
        print(menu_helper(parse(arg)))

    def do_new(self, arg):
        'start a new order:  new'
        print("New order started:")
        print(requests.get("http://127.0.0.1:5000/order").text)

    def do_cart(self, n):
        'View the cart:  cart'
        if n:
            print(requests.get("http://127.0.0.1:5000/order/" + str(n)).text)
        else:
            print("Please enter your order number.")

    def do_add(self, arg):
        'Add an item to the cart:\n  add pizza pepperoni\n  add drink coke\n  add topping mushroom'
        print(add_helper(parse(arg)))

    def do_remove(self, arg):
        'Remove 1 item from the cart:  remove <order number> <category> <name>'
        print(remove_helper(parse(arg)))

    def do_cancel(self, arg):
        'Cancel order'
        print(cancel_helper(parse(arg)))

    def do_q(self, arg):
        'exit the shell:  q'
        print('Thank you for visiting Pizza Parlour. Please come again.\n')
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


def parse(arg):
    'Convert the user input to a list'
    return ((arg.lower()).replace('.', '')).split()


def format(d):
    'Convert a dict to a more readible format'
    res = ""
    for key in d:
        res += "%-12s%-12s\n" % (key, d[key])
    return res


def menu_helper(L):
    url = "http://127.0.0.1:5000/menu"
    res = ""
    if 1 <= len(L) <= 2:
        category = L[0]
        if category in ["topping", "pizza", "drink"]:
            route = "/" + category + "s"
            # price for a specified item
            if len(L) == 2:
                try:
                    res = requests.get(url + route + "/" + L[1]).text
                except:
                    res = "Please enter a valid item name."
            # menu by category
            else:
                try:
                    res = format(requests.get(url + route).json())
                except:
                    res = "Server failed to send menu."
        else:
            res = "Please enter one of the following as category:  pizza  topping  drink"
    # full menu
    else:
        try:
            res = "The full menu:"
            for category in ["/pizzas", "/toppings", "/drinks"]:
                res += "\n" + category[1:] + "\n" + format(requests.get(url + category).json())
        except:
            res = "Server failed to send menu."
    return res


def add_helper(L):
    res = ""
    if len(L) < 3:
        res = "Please specify order number, category and item name. E.g. add 1 drink coke, add 1 custompizza small beef"
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
                if category == "custompizza":
                    toppings = L[3:]
                    toppings_json_list = []
                    for top in toppings:
                        top_json = {"name": top, "price": toppingPrices[top]}
                        toppings_json_list.append(top_json)

                    item = {"size": {"name": name,
                                     "price": d[name]}, "toppings": toppings_json_list}
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
        return "Please specify order number, category, and name. E.g. remove 1 drink coke"
    else:
        try:
            order_number, category, name = args[0], args[1], args[2]
            if category not in ["topping", "pizza", "drink", "custompizza"]:
                return "Please enter one of the following as category:  pizza  topping  drink custompizza"
            item = {"name": name}
            r = requests.delete(
                "http://127.0.0.1:5000/order/" + order_number + "/" + category, headers=HEADERS, json=item)
            return r.text
        except:
            "Remove 1 item from the cart:  remove <order number> <category> <name>"


def cancel_helper(args):
    if len(args) != 1:
        return "Please specify order number. E.g. cancel 1"
    else:
        try:
            order_number = args[0]
            r = requests.delete("http://127.0.0.1:5000/order/" + order_number)
            return r.text
        except:
            return "Please enter a valid order number."


if __name__ == '__main__':
    PizzaShell().cmdloop()

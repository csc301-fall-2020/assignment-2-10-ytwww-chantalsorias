import cmd
import sys
import requests
from Prices import drinkPrices, toppingPrices, pizzaPrices
# import json
# from MenuItem import Drink, Pizza


class PizzaShell(cmd.Cmd):
    intro = '\nWelcome to Pizza Parlour.\nType ? to list commands. Type q to quit.\n'
    prompt = '[ Pizza Parlour ] '
    file = None

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
        add_helper(parse(arg))

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
    return (arg.lower()).split()


def menu_helper(L):
    url = "http://127.0.0.1:5000/menu"
    res = ""
    if 1 <= len(L) <= 2:
        category = L[0]
        if category in ["topping", "pizza", "drink"]:
            route = "/" + category + "s"
            if len(L) == 2:
                try:
                    res = requests.get(url + route + "/" + L[1]).text
                except:
                    res = "Please enter a valid item name."
            else:
                try:
                    res = requests.get(url + route).json()
                except:
                    res = "Server failed to send menu."
        else:
            res = "Please enter one of the following as category:  pizza  topping  drink"
    else:
        res = "The full menu:\n" + str(requests.get(url).json())
    return res


def add_helper(L):
    res = ""
    if len(L) != 3:
        print("Please specify order number, category and item name. E.g. add 1 drink coke")
    else:
        n, category, name = L[0], L[1], L[2]
        if category not in ["topping", "pizza", "drink"]:
            res = "Please enter one of the following as category:  pizza  topping  drink"
        else:
            if category == "topping":
                d = toppingPrices
            elif category == "pizza":
                d = pizzaPrices
            elif category == "drink":
                d = drinkPrices
            try:
                # drink = Drink(name, drinks[name])
                # jdrink = json.dumps(drink)
                # print(requests.post(
                #     'http://127.0.0.1:5000/order/1/drink', json=jdrink).text)
                item = {"name": name, "price": d[name]}
                r = requests.post(
                    "http://127.0.0.1:5000/order/" + n + "/" + category, item)
                res = r.text
                print(item, r, res)
            except:
                res = "Please enter a valid item name."
    return res


if __name__ == '__main__':
    PizzaShell().cmdloop()

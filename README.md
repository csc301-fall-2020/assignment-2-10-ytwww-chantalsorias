# Instructions about Testing and Starting

Please have the following packages installed before starting: `flask`, `pytest`, `pytest-cov`, `requests`

- To run tests with coverage, type `pytest --cov-report term --cov=. tests/unit_tests.py`
- To run the app:
  - First, run the main Flask module by running `python3 PizzaParlour.py`
  - Then, in another terminal, run the Shell module by running `python3 Shell.py`

# How to interact with Pizza Shell

- `?` or `help` list all commands


- `? <cmd>` or `help <cmd>` display guide about `<cmd>`

  - Examples: `? add`, `? checkout`, `help menu`


- `new` starts a new order, will return `<order-number>`


- `menu` shows full menu


- `menu <category>` shows menu by category.

  - `<category>` is one of `pizza`, `topping`, `drink`.
  
  - Examples: `menu pizza`, `menu drink`, `menu topping`


- `menu <category> <name>` shows price for a specific item.

  - `<category>` is one of `pizza`, `topping`, `drink`.
  
    - For `<category>` `pizza`, `<name>` is one of `small`, `medium`, `large`, `pepperoni`, `margherita`, `vegetarian`, `neapolitan`
    - For `<category>` `topping`, `<name>` is one of `olives`, `tomatoes`, `mushrooms`, `jalapenos`, `chicken`, `beef`, `pepperoni`
    - For `<category>` `drink`, `<name>` is one of `coke`, `dietcoke`, `cokezero`, `pepsi`, `dietpepsi`, `drpepper`, `water`, `juice`
    
  - Examples: `menu pizza neapolitan`, `menu pizza small`, `menu drink juice`, `menu topping jalapenos`


- `cart <order-number>` shows the cart of the order with `<order-number>`

  - Example: `cart 1`


- `add <order-number> drink <name>` adds a drink to the order with `<order-number>`

  - `<name>` is one of `coke`, `dietcoke`, `cokezero`, `pepsi`, `dietpepsi`, `drpepper`, `water`, `juice`
  
  - Example: `add 1 drink coke`


- `add <order-number> pizza <name> <size>` adds a predefined pizza to the order with `<order-number>`

  - `<name>` is one of `pepperoni`, `margherita`, `vegetarian`, `neapolitan`
  
  - `<size>` is one of `small`, `medium`, `large`.
  
  - Example: `add 1 pizza neapolitan large`


- `add <order-number> custompizza <size> <topping-1> <topping-2> ...` adds a custom pizza to the order with `<order-number>`

  - `<size>` is one of `small`, `medium`, `large`.
  
  - `<topping-n>` is one of `olives`, `tomatoes`, `mushrooms`, `jalapenos`, `chicken`, `beef`, `pepperoni`
  
  - Example: `add 1 custompizza large beef olives mushrooms`


- `checkout <order-number> pickup`

  - Example: `checkout 1 pickup`


- `checkout <order-number> delivery <carrier> (<address>)`

  - `<carrier>` is one of `inhouse`, `foodora`, `ubereats`
  
  - Example: `checkout 2 delivery inhouse (6301 Silver Dart Dr, Mississauga, ON L5P 1B2)`


- `remove <order-number> drink <name>` removes a drink from the cart of the order with `<order-number>`

  - Example: `remove 1 drink coke`


- `remove <order-number> pizza <name> <size>` removes a preset pizza from the cart of the order with `<order-number>`

  - Example: `remove 1 pizza vegetarian small`


- `remove <order-number> custompizza custom-pizza-<id>` removes a custom pizza from the cart of the order with `<order-number>`

  - Find out `<id>` using `cart <order-number>`
  
  - Example: `remove 1 custompizza custom-pizza-1`


- `cancel <order-number>` cancels the order with `<order number>`

  - Example: `cancel 2`


- `q` exits the shell.

# Pair Programming

## Process

We used Zoom's screen sharing feature to do pair programming. We had 5 two-hour sessions where both of us experienced being a driver and a navigator at least twice. This can be seen in commits with a title starting with "driver" in the git history.

Chantal was the driver while Ya-Tzu was the navigator for removing an item and cancelling an order. This involved working on the remove and cancel functions in Shell.py. Testing it and then working on the tests in unit_tests.py.

Ya-Tzu was the driver while Chantal was the navigator for adding items to the order. This involved working on the add function in Shell.py. Testing it and then working on the tests in unit_tests.py.

## Chantal's Reflection

Pair programming has great benefits. It allows two minds to work together. This means that when working together, we can help each other out and brainstorm on getting a functionality to work. While pair programming there were times when one of us did not know how to do something and the other did and would help programming go faster. Other times when we both did not know something, we would both search it up and this allowed us to find an answer faster. Other times, the driver would continue coding until the navigator found an answer to something. Pair programming also allows one to learn things from the other programmer. We both use the same text editor and when Ya-Tzu started commiting and pushing from within the program, I learned something new. I always did it through the terminal. Other postives are few mistakes and bugs and increased code quality. Lastly, it improved team morale because we can talk to each other and help solve problems so that we would not be stuck on something for a long time.

Some negatives would be if the driver is perfectly capable of programming a feature by themselves and does not need feedback from the navigator then the navigator could be working on something else in the mean time. This leads to the next problem of finishing a project on time. We would not be able to pair program for all features because it would take a longer amount of time compared to doing some individually.

## Ya-Tzu's Reflection

Pair programming allows me to gain a greater understanding of how different modules work together. Had we not used pair programming, I would not have known so much about how my partner's feature is implemented. Knowing about the implementation of the features that are not mine makes me create better modules that work well with others. I have also found that debugging becomes a breeze and less time-consuming with the navigator present since the driver, being the one writing the code, usually has some blind spots that are easy for others to find but difficult to find yourself. Another benefit of pair programming is that it is good for team-building since we need to communicate a lot during the session.

A setback for pair programming is that it is not easy for the driver to focus on coding the feature since many discussions happen during coding. If the feature for pair programming is not too complex, the time spent on the feature may not be worth it. 

# Program design

The class MenuItem is designed with Factory Method in mind. MenuItem is a parent class with "name" and "price" attributes. The children classes of MenuItem includes Drink, PredefinedPizza, Pizza, and CustomPizza. We decided this because all products share similarities such as price and name. The parent class MenuItem takes care of basics such as representing products in serialization while the children classes adds on these functionalities with their special needs. One example is the child class CustomPizza that has the added attributes of "size" and "toppings". For the "price" attribute, we needed to use a function to calculate it because every custom pizza could be different and the price depends on its size and toppings.

The class Orders is designed with Singleton design pattern. There is only one instance of the class Orders at all times. The Orders class keeps track of shared resources such as counter for a order number and all. Its purpose is to store a list of Order objects and responsibilities include creating, removing, and getting an order.

We use Singleton as a design pattern for the Menu class as well, as there is only one instance during a run of the program. It stores a list of MenuItem objects and its responsibilities include adding and getting MenuItems.

To comply with single-responsibility principle, we make sure that each module has its unique purpose. The Price module converts the text files containing product details to objects to be used by other modules. The prices are stored in text files to achieve persistence. The Menu module represents products, and the Order module deal with order-related functionalities. The PizzaParlour module is the server. The Shell module is the command-line interface that send requests to the server based on interactions with user input.

Since all modules only perform specific related tasks then this means there is high cohesion. Therefore the methods relate to the intention of the class. The modules do not depend on each other. Order only requires items to have a price attribute in order to calculate total price of the order. This means there is low coupling and that changing something major in one class should not affect the other.

# Code Craftsmanship

For formatting code, we use VSCode's autopep8 formatter.  
For linters, we use Pylint.

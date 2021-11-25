"""Import module used to access google sheets"""
from contextlib import suppress  # module used in convert_to_int function.
from google.oauth2.service_account import Credentials
import gspread
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('easy_grocery')

# global variable

# List of recipes
grocery_recipe_list = []

# List of ingredients
grocery_list = []


def choose_meals():
    """
    Print dish type options to the user and get user choice.
    Validate input data.
    Call function to create a recipes dictionary.
    Iterate over dictionary to access keys.
    Call print_words function to generate print statements.
    """
    while True:
        print('Please select a dish type:\n')
        print('Press 1 for Vegetarian')
        print('Press 2 for Chicken')
        print('Press 3 for Beef')
        print('Press 4 for Fish\n')

        user_choice = input('Enter your option here:\n')
        print('')

        if validate_data(user_choice, 4):
            int_choice = int(user_choice)
            str_user_choice = get_dish_type(int_choice)
            words = format_string(str_user_choice)
            print(f'{words[0]} {words[1]} selected.\n')
            break

    while True:
        recipes_dict = create_dict_recipes(str_user_choice)
        choose_meals.recipes_list = list(recipes_dict.keys())
        list_len = len(choose_meals.recipes_list)
        print('Please select a recipe to add it to the Grocery List:\n')
        # This part handles the selection of recipes from  choosen type.
        for key in recipes_dict:
            words = format_string(key)
            print_words(words, recipes_dict[key])
        print('')
        dish_choice = input('Enter your option here:\n')
        print('')

        if validate_data(dish_choice, list_len):
            recipe_str = [
                word for word, num in recipes_dict.items()
                if num == int(dish_choice)
            ]
            words = format_string(recipe_str[0])
            print_words2(words)
            user_recipe_pick = choose_meals.recipes_list[int(dish_choice) - 1]
            break
    # Append choosen recipe to recipes list.
    grocery_recipe_list.append(user_recipe_pick)
    # This function will ask user if they want to add another meal
    # controling the code flow.
    another_meal()


def print_words2(string):
    """
    Check how many words are in string and print related statement
    """
    if len(string) == 1:
        print(f'Adding {string[0]} to Grocery List...\n')
        print(f'{string[0]} added.\n')
    elif len(string) == 2:
        print(f'Adding {string[0]} {string[1]} to Grocery List...\n')
        print(f'{string[0]} {string[1]} added.\n')
    elif len(string) == 3:
        print(
            f'Adding {string[0]} {string[1]} {string[2]} to Grocery List...\n'
        )
        print(f'{string[0]} {string[1]} {string[2]} added.\n')


def print_words(string, num_key):
    """
    Check how many words are in string and print related statement
    """
    if len(string) == 1:
        print(f'Press {num_key} for {string[0]}')
    elif len(string) == 2:
        print(f'Press {num_key} for {string[0]} {string[1]}')
    elif len(string) == 3:
        print(f'Press {num_key} for {string[0]} {string[1]} {string[2]}')


def validate_data(value, length):
    """
    From inside the try converts value to integer.
    Raises ValueError if value is not an integer between 1 and
    paramenter length.
    """
    try:
        if int(value) < 1 or int(value) > length:
            raise ValueError(
            )
    except ValueError:
        print(
            f'Invalid data: Choose between 1 and {length}, please try again.\n'
        )
        return False

    return True


def format_string(word):
    """
    Format string into two separated and capitalized words
    """
    result = []
    if '_' in word:
        user_choice_split = word.split('_')
        for item in user_choice_split:
            word = item.capitalize()
            result.append(word)
    else:
        result.append(word.capitalize())

    return result


def get_dish_type(dish_type):
    """
    Convert integer to string.
    """
    if dish_type == 1:
        dish_type = 'vegetarian_recipes'
    elif dish_type == 2:
        dish_type = 'chicken_recipes'
    elif dish_type == 3:
        dish_type = 'beef_recipes'
    elif dish_type == 4:
        dish_type = 'fish_recipes'

    return dish_type


def create_dict_recipes(recipe_type):
    """
    Get recipes of a kind and create a dictionary.
    """
    meals_list = SHEET.worksheet(recipe_type)
    data = meals_list.col_values(1)
    number = [num for num in range(1, len(data) + 1)]

    return dict(zip(data, number))


def another_meal():
    """
    Display picked recipes.
    Call choose_meals function if user wants to add another meal.
    Call check_stock if user wants to check stock
    before generate shopping list.
    Call generate_grocery_list if user want to proceed
    without checking the stock.
    """
    while True:
        print('You already picked:\n')
        for word in grocery_recipe_list:
            formated_word = format_string(word)
            print(*formated_word)
        print('\n')
        print('Would you like to add another meal?\n')

        user_answer = input('Type 1 for YES or 2 for NO:\n')

        if validate_data(user_answer, 2):
            if int(user_answer) == 1:
                print('')
                print('Retrieving recipes list...\n')
                choose_meals()
            elif int(user_answer) == 2:
                while True:
                    print('')
                    print(
                        'Would you like to use ingredients in stock?'
                    )
                    user_answer = input('Type 1 for YES or 2 for NO:\n')

                    if validate_data(user_answer, 2):
                        if int(user_answer) == 1:
                            print('')
                            print('Checking stock...\n')
                            stock_list = check_stock(grocery_recipe_list)
                            grocry = generate_grocery_list(grocery_recipe_list)
                            update_grocery_list(stock_list, grocry)
                        elif int(user_answer) == 2:
                            print('')
                            print('Generating Grocery list...')
                            generate_grocery_list(grocery_recipe_list)
                        break
            break


def check_stock(recipes):
    """
    Iterates through lists and dictionaries
    to create a list of ingredients that are in the recipes and in the stock.
    Iterates through stock and get the quantity of each ingredient.
    Return a dictionary of ingredients and quantities that are already in stock
    and should be deleted from grocery list.
    """
    stock = SHEET.worksheet('stock')
    in_stock = []  # List of ingredients for recipes that are in stock.
    quantity_in_stock = []  # List with quantity of each ingredient.
    for recipe in recipes:  # Iterates with list of recipes.
        one_recipe = SHEET.worksheet(recipe)
        # Get ingredients in a recipe.
        ingredients_col = one_recipe.col_values(1)
        stock_col = stock.col_values(1)  # Get ingredients in stock.
        for one_ingredient_stock in stock_col[1:]:
            for one_ingredient_recipe in ingredients_col[1:]:
                # Compare if ingredient is in stock.
                if one_ingredient_stock == one_ingredient_recipe:
                    # Add ingredient to list.
                    in_stock.append(one_ingredient_stock)

    stock_quantity = stock.get_all_records()
    print(stock_quantity)
    # Iterates through list of dictionaries.
    for item in stock_quantity:
        for stock in in_stock:  # Iterates through stock.
            if stock in item.values():
                # Iterates over quantity of ingredient in stock.
                for value in item.values():
                    integer = convert_to_int(value)
                    # Check if is an integer.
                    if isinstance(integer, int):
                        # Add quantity to list.
                        quantity_in_stock.append(value)

    return dict(zip(in_stock, quantity_in_stock))


def convert_to_int(string):
    """
    Converts a string into int or ignore it.
    """
    with suppress(Exception):
        return int(string)


def update_grocery_list(stock_list, grocery_generated):
    """
    Compares stock with grocery list and update grocery list.
    """
    print(stock_list)
    print(grocery_generated)
    # Iterates through groceries dictionary keys.
    for key in list(grocery_generated[0].keys()):
        # Iterates through stock dictionary keys.
        for item in stock_list.keys():
            if item == key:  # Check if we have the item in stock.
                in_stock = grocery_generated[0][item]
                print(in_stock)
                # Update grocery list.
                grocery_generated[0][item] = (in_stock - stock_list[key])
                for value in list(grocery_generated[0].values()):
                    if value <= 0:
                        # Delete item if item is not needed in grocery list.
                        del grocery_generated[0][item]

    print(grocery_generated)


def generate_grocery_list(recipe):
    """
    Use list of recipes to get list of ingredients from google sheets.
    """
    list_of_ingredients = []
    quantity_of_ingredients = []
    units = []
    for meal in recipe:  # Iterates through list of recipes.dict()
        num_of_meals = recipe.count(meal)
        ingredients = SHEET.worksheet(meal)
        data = ingredients.get_all_values()
        for item in data[1:]:  # Iterates through recipes and get ingredients.
            list_of_ingredients.append(item[0])
            units.append(item[2])
            # Check if a meal was added more than one time
            if num_of_meals > 1:
                quantity_of_ingredients.append(float(item[1]) * num_of_meals)
            elif num_of_meals == 1:
                quantity_of_ingredients.append(float(item[1]))

    dictionary = dict(zip(list_of_ingredients, quantity_of_ingredients))
    return [dictionary, units]


choose_meals()

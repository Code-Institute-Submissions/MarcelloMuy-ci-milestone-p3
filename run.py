"""
Import modules used to access google sheets, tabulate and colorama
"""
from contextlib import suppress  # module used in convert_to_int function.
# Module used to create a table in display_list function.
from tabulate import tabulate
# Import gspread module
from google.oauth2.service_account import Credentials
import gspread
# Import colorama module
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
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


def run_program():
    """
    Run welcoming message and the initial menu.
    Validates input data.
    Calls respective functions.
    """
    global grocery_recipe_list
    grocery_recipe_list = []
    global grocery_list
    grocery_list = []
    while True:
        print('')
        print(Fore.GREEN + 'Welcome to' + Style.BRIGHT + ' EasyGrocery!')
        print('Your grocery list generator.\n')
        print(Fore.CYAN + 'Would you like to see the instructions?')
        print('Press 1 for YES or 2 for NO:\n')

        instr_user_choice = input('Enter your option here:\n')

        if validate_data(instr_user_choice, 2):
            if int(instr_user_choice) == 1:
                print('')
                print('Loading instructions...\n')
                instructions()
                break
            elif int(instr_user_choice) == 2:
                print('')
                print('Loading program...\n')
                break

    while True:
        print(Fore.CYAN + 'What would you like to do?\n')
        print('Press 1 to pick your meals.')
        print('Press 2 to see your stock.\n')

        first_user_choice = input('Enter your option here:\n')

        if validate_data(first_user_choice, 2):
            if int(first_user_choice) == 1:
                print('')
                print('Loading recipes selection...\n')
                choose_meals()
                break
            elif int(first_user_choice) == 2:
                print('')
                print('Loading stock...\n')
                print('This is what you have in stock:\n')
                see_stock()
                break


def instructions():
    """
    Program Instructions
    """
    print('')
    easy_grocery = Fore.GREEN + Style.BRIGHT + 'EasyGrocery ' + Style.RESET_ALL
    print(
        easy_grocery + 'will help you to generate your weekly grocery list.\n'
        )
    print('You only need to add the recipes you want to cook this week,')
    print('and we will create a grocery list for you.\n')
    print('You decide if you want to generate a complete grocery list or')
    print(
        'if you want to use the ingredients you have already in stock.\n'
        )


def see_stock():
    """
    Get data from google sheets and display it to the user.
    """
    invetory = SHEET.worksheet('stock')
    data = invetory.get_all_values()
    print(Fore.YELLOW + tabulate(data, headers='firstrow'))

    while True:
        print('')
        print(Fore.CYAN + 'What would you like to do?\n')
        print('Press 1 to pick your meals.')
        print('Press 2 to restart the program\n')

        from_stock_user_choice = input('Enter your option here:\n')

        if validate_data(from_stock_user_choice, 2):
            if int(from_stock_user_choice) == 1:
                print('')
                print('Loading recipes...\n')
                choose_meals()
                break
            elif int(from_stock_user_choice) == 2:
                print('')
                print('Restarting the program...\n')
                run_program()
                break


def choose_meals():
    """
    Print dish type options to the user and get user choice.
    Validate input data.
    Call function to create a recipes dictionary.
    Iterate over dictionary to access keys.
    Call print_words function to generate print statements.
    """
    while True:
        print(Fore.CYAN + 'Please select a dish type:\n')
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
        colo = Fore.CYAN
        print(colo + 'Please select a recipe to add it to the Grocery List:\n')
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
        please = ', please try again.\n'
        print('')
        print(
            f'{Fore.RED} Invalid data: Choose between 1 and {length}{please}'
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
        if len(grocery_recipe_list) == 1:
            print('Your chosen meal for the week is:\n')
        else:
            print('Your chosen meals for the week are:\n')

        for word in grocery_recipe_list:
            formated_word = format_string(word)
            bullet = Fore.YELLOW + '*'
            print(bullet, *formated_word)
        print('')
        print(Fore.CYAN + 'Would you like to add another meal?')

        user_answer = input('Type 1 for YES or 2 for NO:\n')

        if validate_data(user_answer, 2):
            if int(user_answer) == 1:
                print('')
                print('Retrieving recipes list...\n')
                choose_meals()
            elif int(user_answer) == 2:
                while True:
                    print('')
                    colo = Fore.CYAN
                    print(
                        colo + 'Would you like to use ingredients in stock?'
                    )
                    user_answer = input('Type 1 for YES or 2 for NO:\n')

                    if validate_data(user_answer, 2):
                        if int(user_answer) == 1:
                            print('')
                            print('Checking stock...\n')
                            stck_li = check_stock(grocery_recipe_list)
                            grocry = generate_grocery_list(grocery_recipe_list)
                            gro_updated = update_grocery_list(stck_li, grocry)
                            display_list(gro_updated)
                        elif int(user_answer) == 2:
                            print('')
                            print('Generating Grocery list...\n')
                            g_list = grocery_recipe_list
                            full_grocery_list = generate_grocery_list(g_list)
                            display_list(full_grocery_list)
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
    # Iterates through groceries dictionary keys.
    for key in list(grocery_generated[0].keys()):
        # Iterates through stock dictionary keys.
        for item in stock_list.keys():
            if item == key:  # Check if we have the item in stock.
                in_stock = grocery_generated[0][item]
                # Update grocery list.
                grocery_generated[0][item] = (in_stock - stock_list[key])
                for value in list(grocery_generated[0].values()):
                    if value <= 0:
                        # Delete item if item is not needed in grocery list.
                        del grocery_generated[0][item]
                        del grocery_generated[1][item]
    return grocery_generated


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

    dict_value_quant = dict(zip(list_of_ingredients, quantity_of_ingredients))
    dict_value_unit = dict(zip(list_of_ingredients, units))
    return [dict_value_quant, dict_value_unit]


def display_list(grocery_list_display):
    """
    Iterates through dictionaries and displays data to the user.
    """
    final_grocery_list = []
    # Dictionary with ingredients names and quantities.
    dict1 = grocery_list_display[0].items()
    # Dictionary with ingredients names and units.
    dict2 = grocery_list_display[1].items()
    # Append headers to grocery list.
    final_grocery_list.append(['Ingredients', 'Quantity', 'Unit'])

    for (ingr, quant), (ingr2, unit) in zip(dict1, dict2):
        one_list = []
        # Format strings.
        f_ingr = format_string(ingr)
        f_unit = format_string(unit)
        if len(f_ingr) > 1:  # Checks if recipe name has more than one word.
            new_word = ' '.join(f_ingr)
            # Check quantity and unit to make it plural or not.
            if quant > 1 and f_unit[0][-1] != 's':
                f_unit = ''.join((*f_unit, 's'))
                one_list.extend([new_word, quant, f_unit])
            else:
                one_list.extend([new_word, quant, *f_unit])
        else:
            # Check quantity and unit to make it plural or not.
            if quant > 1 and f_unit[0][-1] != 's':
                f_unit = ''.join((*f_unit, 's'))
                one_list.extend([*f_ingr, quant, f_unit])
            else:
                one_list.extend([*f_ingr, quant, *f_unit])

        # Append list with ingr, quant and unit formated and ready to use.
        final_grocery_list.append(one_list)

    print(Fore.GREEN + 'Your grocery list is ready!\n')
    # Create a table and display it.
    print(Fore.YELLOW + tabulate(final_grocery_list, headers='firstrow'))

    thank_you()


def thank_you():
    """
    Display thank you message.
    Ask the user if they want to rerun the program.
    """
    while True:
        print('')
        bright = Style.BRIGHT
        print(
            'Thank you for using' + bright + Fore.GREEN + ' EasyGrocery!\n'
            )
        print('If you want to create a new grocery list')
        print('press 1 to rerun the program.\n')

        rerun_user_choice = input('Enter your option here:\n')

        if validate_data(rerun_user_choice, 1):
            print('')
            print('Loading program...\n')
            run_program()
            break


run_program()

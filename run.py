"""Import module used to access google sheets"""
import gspread
from google.oauth2.service_account import Credentials

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
    Call function to create a recipes dict.
    Iterate over dictionary to access keys and display keys to the user.
    """
    while True:
        print('Please select a dish type:\n')
        print('Type 1 for Vegetarian')
        print('Type 2 for Chicken')
        print('Type 3 for Beef')
        print('Type 4 for Fish\n')

        user_choice = input('Enter your option here: ')
        print('')

        if validate_data(user_choice, 4):
            int_choice = int(user_choice)
            str_user_choice = get_dish_type(int_choice)
            user_choice_split = str_user_choice.split('_')
            first_word = user_choice_split[0].capitalize()
            second_word = user_choice_split[1].capitalize()
            print(f'{first_word} {second_word} selected.\n')
            break

    while True:
        recipes_dict = create_dict_recipes(str_user_choice)
        choose_meals.recipes_list = list(recipes_dict.keys())
        list_len = len(choose_meals.recipes_list)
        print('Please select a recipe to add it to the Grocery List.\n')

        for key in recipes_dict:
            key_str = key.split('_')
            first_word = key_str[0].capitalize()
            second_word = key_str[1].capitalize()
            print(f'Press {recipes_dict[key]} for {first_word} {second_word}.')
        print('')
        dish_choice = input('Enter your option here: ')
        print('')

        if validate_data(dish_choice, list_len):
            recipe_str = [word for word, num in recipes_dict.items() if num == int(dish_choice)]
            key_str = recipe_str[0].split('_')
            first_word = key_str[0].capitalize()
            second_word = key_str[1].capitalize()
            print(f'Adding {first_word} {second_word} to Grocery List...\n')
            print(f'{first_word} {second_word} added.\n')
            user_recipe_pick = choose_meals.recipes_list[int(dish_choice) - 1]
            break

    add_dish_to_grocery_list(user_recipe_pick)


def validate_data(value, length):
    """
    From inside the try converts value to integer.
    Raises ValueError if value is not an integer between 1 and
    paramenter length.
    """
    try:
        if int(value) < 1 or int(value) > length:
            raise ValueError(
                f'Pick a number between 1 and {length},'
                f' you choose {int(value)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True


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


def add_dish_to_grocery_list(picked_meal):
    """
    Add dish to Grocery recipe list.
    Call choose_meals function if user wants to add another meal.
    Call generate_grocery_list if user don't want to add another meal.
    """
    while True:
        grocery_recipe_list.append(picked_meal)
        print('Would you like to add another meal?\n')

        user_answer = input('Type 1 for YES or 2 for NO: ')

        if validate_data(user_answer, 2):
            if int(user_answer) == 1:
                print('')
                print('Retrieving recipes list...\n')
                choose_meals()
            elif int(user_answer) == 2:
                print('')
                print('Generating Grocery list...\n')
                generate_grocery_list(grocery_recipe_list)
            break


def generate_grocery_list(recipe):
    """
    Use list of recipes to get list of ingredients from google sheets.
    """
    print(recipe)

    for meal in recipe:
        ingredients = SHEET.worksheet(meal)
        data = ingredients.row_values(1)
        print(data)


choose_meals()

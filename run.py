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
SHEET = GSPREAD_CLIENT.open('easy_groceries')


def choose_meals():
    """
    Print dish type options to the user and get user choice.
    Validate input data.
    Call function to create a recipes dict and display it to the user.
    """
    while True:
        print('Please select a dish type:')
        print('Type 1 for Vegetarian')
        print('Type 2 for Chicken')
        print('Type 3 for Beef')
        print('Type 4 for Fish')

        user_choice = input('Enter your option here: ')

        if validate_data(user_choice):
            int_choice = int(user_choice)
            str_user_choice = get_dish_type(int_choice)
            print(f'You choose {str_user_choice}\n')
            break

    while True:
        recipes_dict = create_dict_recipes(str_user_choice)
        choose_meals.recipes_list = list(recipes_dict.keys())
        print('Plese type recipe number to add it to groceries list.\n')
        print(f'{recipes_dict}\n')

        dish_choice = input('Enter your choice here: ')

        if validate_dish_choice(dish_choice):
            print(choose_meals.recipes_list[int(dish_choice) - 1])
            break


def validate_data(value):
    """
    From inside the try converts value to integer.
    Raises ValueError if value is not an integer between 1 and 4.
    """
    try:
        if int(value) < 1 or int(value) > 4:
            raise ValueError(
                f'Pick a number between 1 and 4, you choose {int(value)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True


def validate_dish_choice(value):
    """
    From inside the try converts value to integer.
    Raises ValueError if value is not an integer
    between 1 and and recipes list length.
    """
    list_len = len(choose_meals.recipes_list)
    try:
        if int(value) < 0 or int(value) >= list_len + 1:
            raise ValueError(
                f'Pick a number between 1 and {list_len}, you choose {value}'
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


def add_dish_to_groceries_list():
    """
    Add dish to groceries.
    """


choose_meals()

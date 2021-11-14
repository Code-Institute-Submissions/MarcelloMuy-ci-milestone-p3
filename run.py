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

# global variable
groceries_list = []


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

        if validate_data(user_choice, 4):
            int_choice = int(user_choice)
            str_user_choice = get_dish_type(int_choice)
            user_choice_split = str_user_choice.split('_')
            print(f'{user_choice_split[0].capitalize()} {user_choice_split[1]} selected.\n')
            break

    while True:
        recipes_dict = create_dict_recipes(str_user_choice)
        choose_meals.recipes_list = list(recipes_dict.keys())
        list_len = len(choose_meals.recipes_list)
        print('Plese type recipe value number to add it to groceries list.\n')
        print(f'{recipes_dict}\n')

        dish_choice = input('Enter your choice here: ')

        if validate_data(dish_choice, list_len):
            print(f'Adding {dish_choice} to groceries list...')
            user_recipe_pick = choose_meals.recipes_list[int(dish_choice) - 1]
            break

    add_dish_to_groceries_list(user_recipe_pick)


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


def add_dish_to_groceries_list(picked_meal):
    """
    Add dish to groceries list.
    """
    while True:
        groceries_list.append(picked_meal)
        print('Would you like to add another meal?\n')

        user_answer = input('Type 1 for Yes or 2 for No: ')

        if validate_data(user_answer, 2):
            print(f'You choose {user_answer}.')
            if int(user_answer) == 1:
                choose_meals()
            elif int(user_answer) == 2:
                print(groceries_list)
            break


choose_meals()

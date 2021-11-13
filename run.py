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
    Print dish type options to the user and get user choice
    """
    print('Please select a dish type:')
    print('Type 1 for Vegetarian')
    print('Type 2 for Chicken')
    print('Type 3 for Beef')
    print('Type 4 for Fish')

    user_choice = input('Enter your option here: ')
    validate_data(user_choice)


def validate_data(value):
    """
    From inside the try converts value to integer.
    Raises ValueError if value is not an integer between 1 and 4
    """
    try:
        if int(value) < 1 or int(value) > 4:
            raise ValueError(
                f'Choose an option between 1 and 4, you choose {int(value)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')


def get_dish_type(dish_type):
    """
    Get list of recipes of specific type
    """
    meals_list = SHEET.worksheet(dish_type)
    data = meals_list.get_all_values()
    return data


choose_meals()

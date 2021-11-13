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
    Print dish type options to the user and get user option
    """
    print('Please select a dish type:')
    print('Type 1 for Vegetarian')
    print('Type 2 for Chicken')
    print('Type 3 for Beef')
    print('Type 4 for Fish')

    user_option = input('Enter your option here: ')
    print(f'You typed: {user_option}')


def get_dish_type(dish_type):
    """
    Get list of recipes of specific type
    """
    meals_list = SHEET.worksheet(dish_type)
    data = meals_list.get_all_values()
    return data


choose_meals()

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


def get_dish_type(dish_type):
    """
    Get list of recipes of specific type
    """
    meals_list = SHEET.worksheet(dish_type)
    data = meals_list.get_all_values()
    print(data)

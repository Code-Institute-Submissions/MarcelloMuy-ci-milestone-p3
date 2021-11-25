# EasyGrocery Project

EasyGrocery
In this project I tried to create a grocery list generator using Python language and google sheets as a database. The user would choose recipes from a selection of recipes the program would generate a grocery list with all the necessary ingredients based in the user’s choice of recipes.
The program also gives the user the choice to check a stock before generating the list making the process of figuring out what ingredients should you buy and what you already have in stock a lot easier. 

You can find the program live version by [clicking here!]( https://easy-grocery-marcellomuy.herokuapp.com/)

##Table of contents
1. [Plans and structure](#plans-and-structure)
    - [Objectives](#objectives)
	- [Changes throughout the process](#changes-throughout-the-process)
    - [Flowchart](#flowchart)

## Plans and structure 

<img src="images/" alt="Screenshot">  

### Objectives:

- I want to create a program that is easy to navigate.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - This was achieved by using numbers as option keys, the user will choose between 1 and 2 for YES and NO questions and between 1 and 4 for dish types and dish recipes options.
- I want the program to display the recipes by category.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - This was achieved by creating dish type lists with the recipes names in the database. These lists can be accessed separately and have the recipes names extracted from it. 
- I want the program to run in a loop asking the user if they want to add another meal.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - After picking a meal the program will prompt the user if they want to add another meal 1 for YES or 2 for NO. If the user type 1 it will go back to the dish type selection screen. If the user type 2 it will finish the recipes selection phase. 
- I want the program to display on screen the recipes that have already been picked when asking the user to add another meal.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - By placing a for loop with a print statement inside the while True loop in the another_meal() function that handles this part of the code.
- I want the program to give the user the option to have the full grocery list or have an updated list with the ingredients in stock removed from it.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - After selecting meals, the program will ask if user wants to check the stock before generating grocery list 1 for YES or 2 for NO. If 1 is selected the program will compare the full grocery list against the ingredients in stock and generate the updated list. If 2 is selected a full grocery list with no adjustments will be generated.
- I want the program to display to the user what is in stock.
    - Was this achieved?
        - 
    - How was this achieved?
        - This was achieved by using...


### Changes throughout the process:

- Initially I have the idea to create a program that would have the stock database updated after an ingredient was used for a recipe, due to the limit of time and security reasons I decided to keep the data base read only.

- I had plans to give the user the option to add new recipes, but this function was also not added due to the reasons above.

### Flowchart:


Go back to [Table of contents](#table-of-contents)

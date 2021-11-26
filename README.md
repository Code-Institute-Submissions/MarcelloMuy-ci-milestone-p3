# EasyGrocery Project

In this project, I tried to create a grocery list generator using Python and google sheets as a database. The user can choose from a selection of recipes, and the program will generate a grocery list with all the necessary ingredients based on the user’s choices. The program also gives the user the option to check the stock before generating the list, making figuring out what ingredients you should buy and what you already have in inventory a lot easier.

You can find a live version of the program [here.](https://easy-grocery-marcellomuy.herokuapp.com/)

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
        - By using numbers as the option choices. The user can choose between 1 and 2 for YES or NO questions and between 1 and 4 for dish types and dish recipes questions.
- I want the program to display the recipes by category.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - By creating a list with the names of the recipes for each dish type in the database. These lists can be accessed separately and have the names of the recipes extracted from them.
- I want the program to run in a loop asking the user if they want to add another meal.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - After picking a meal, the program will ask the user if they want to add another meal, 1 for YES or 2 for NO. If the user types 1, it will go back to the dish type selection screen. If the user types 2, it will finish the recipes selection phase.
- I want the program to display on-screen the picked recipes when asking the user to add another meal.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - By placing a print statement that displays the recipes list inside the while True loop in the another_meal() function that handles this part of the code.
- I want the program to give the user the option to have the complete grocery list or have an updated list with the ingredients in stock removed from it.
    - Was this achieved?
        - Yes
    - How was this achieved?
        - After selecting meals, the program will ask if the user wants to check the stock before generating a grocery list, 1 for YES or 2 for NO. If 1, is selected the program will compare the complete grocery list against the ingredients in stock and generate the updated list. If 2, is selected a complete grocery list with no adjustments will be generated.
- I want the program to display to the user what is in stock.
    - Was this achieved?
        - 
    - How was this achieved?
        - This was achieved by using...


### Changes throughout the process:

- Initially, I had the idea to create a program that would have the stock database updated after an ingredient is used for a recipe. Due to the limit of time and security reasons, I decided to keep the database read-only.

- I had plans to give the user the option to add new recipes, but this function was also not added due to the reasons above.

### Flowchart:


Go back to [Table of contents](#table-of-contents)

# --------------------------------
# FRONT END OF INVESTMENT DATABASE
# --------------------------------

# TODO:
# - add crypto support
# - add P/L tracker for different time periods (1D, 1W, 1M, 3M, 1Y, 5Y)
# - interactive graph?

from update_db import update_portfolios
from graph_value import graph_value
from user_utils import *


OPTIONS = ["List Holdings", "Auto-Update Database", "Add Purchase Order", "Add Sell Order", "Render Portfolio Value PNG", "Close Account", "Exit"]

# User selects to sign in, register, or quit
print("Do you have an existing account?")
already_exists = int(input("Enter 0 to sign in, 1 to register, or 2 to quit: "))
user_id = None
if (already_exists == 0):
    user_id = user_signin()
elif (already_exists == 1):
    goodAccount = create_account()
    while (goodAccount == False):
       print("Try again.")
       goodAccount = create_account()
    if (goodAccount == True):
        print("Success, account created.")
        user_id = user_signin()
elif (already_exists == 2):
    exit()
else:
    print("Invalid selection. Quitting...")
    exit()


# If valid sign in, user is presented with options
if (user_id == None):
    print("Error: Invalid sign in.")
    exit()
else:
    optionLen = len(OPTIONS)
    keepGoing = True
    while (keepGoing):
        for i in range(optionLen):
            print(i, ": ", OPTIONS[i])
        choice = int(input("Select an option: "))
        
        if (choice == 0):
            list_holdings(user_id)
        elif (choice == 1):
            update_portfolios()
        elif (choice == 2):
            add_purchase(user_id)
        elif (choice == 3):
            add_sell(user_id)
        elif (choice == 4):
            graph_value(user_id)
        elif (choice == 5):
            close = close_account(user_id)
            if (close == True):
                keepGoing = False
                exit()
        elif (choice == 6):
            keepGoing = False
            exit()
        else:
            print("Error: Invalid selection.")



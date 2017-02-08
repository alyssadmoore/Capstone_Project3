import db
import warnings
from sqlalchemy import exc


# Check if user input is a valid int type
def check_int(user_input):
    try:
        int(user_input)
        return True
    except ValueError:
        return False


# Check if user input is a valid float type
def check_float(user_input):
    try:
        float(user_input)
        return True
    except ValueError:
        return False


# It seemed better to leave a way for the user to quickly back out of an action without closing the entire application
# (like if they made a typo in item name, for example) than to keep rerouting back to it infinitely or
# after a set number of tries. This general rule is applied throughout the UI.
print('\nWelcome to Merch Manager! If you ever want to back out of an action, '
      'simply enter invalid entry to be rerouted back to the main options.\n')

# Start of program loop
while True:

    # First ask which table we are working with, make sure user provided valid entry
    table_choice = input('Which table would you like to work with? '
                         'Enter 1 for merch, 2 for shows, 3 for sales, 4 to view statistics, or 5 to quit:\n')
    if check_int(table_choice):
        if 5 >= int(table_choice) >= 1:
            # Next ask what we should do with the table: view it, add to it, delete from it, or edit it
            # (and check validity of user entry again) if user chose a table to work with
            if table_choice == '1' or table_choice == '2' or table_choice == '3':
                action_choice = input('What action would you like to perform? Enter 1 to view all entries, '
                                      '2 to add an entry, or 3 to search for an entry:\n')

            # Print statistics (must ignore a warning given which alerts that slight rounding errors may occur)
            elif table_choice == '4':
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=exc.SAWarning)
                    print(db.get_stats())
                    # Set action choice to invalid number so user is rerouted back to main options
                    action_choice = '6'

            # Quit program
            elif table_choice == '5':
                print("Goodbye!")
                break

            if check_int(action_choice):
                if 3 >= int(action_choice) >= 1:

                    # View block
                    if action_choice == '1':

                        if table_choice == '1':
                            merch = db.view_merch()
                            for item in merch:
                                print(merch)

                        elif table_choice == '2':
                            shows = db.view_shows()
                            for show in shows:
                                print(show)

                        elif table_choice == '3':
                            sales = db.view_sales()
                            for sale in sales:
                                print(sale)

                    # Add block
                    elif action_choice == '2':

                        if table_choice == '1':
                            item = input("Item?\n")
                            price = input("Price?\n")
                            if check_float(price):
                                db.add_merch(item, price)
                            else:
                                print("That wasn't a valid price, please try again.")

                        elif table_choice == '2':
                            date = input("Date?\n")
                            venue = input("Venue?\n")
                            db.add_show(date, venue)

                        elif table_choice == '3':
                            show_id = input("Show id?\n")
                            if check_int(show_id):
                                if db.check_id(show_id):
                                    item = input("Item?\n")
                                    if db.check_item(item):
                                        sold = input("Sold?\n")
                                        if check_int(sold):
                                            db.add_sale(show_id, item, sold)
                                        else:
                                            print("That wasn't a valid item, please try again.")
                                    else:
                                        print("That wasn't a valid item, please try again.")
                                else:
                                    print("That isn't a valid show id, please try again.")
                            else:
                                print("That wasn't a valid number, please try again.")

                    # Search block
                    elif action_choice == '3':

                        if table_choice == '1':
                            term = input("Search term?\n")
                            column = input("Searching Item or Price? Enter 1 for Item or 2 for Price.\n")
                            if column != '1' and column != '2':
                                print("Must enter 1 or 2, please try again.")
                            else:
                                results = db.search_merch(term, column)
                                for item in results:
                                    print(item)

                        elif table_choice == '2':
                            term = input("Search term?\n")
                            column = input("Searching Show ID, Date, or Venue? Enter 1 for item, 2 for Date, for 3 for Venue.\n")
                            if column != '1' and column != '2' and column != '3':
                                print("Must enter 1, 2, or 3, please try again.")
                            else:
                                results = db.search_shows(term, column)
                                for item in results:
                                    print(item)

                        elif table_choice == '3':
                            term = input("Search term?\n")
                            column = input("Searching Show ID, Item, or Sold? Enter 1 for Show ID, 2 for Item, or 3 for Sold.\n")
                            if column != '1' and column != '2' and column != '3':
                                print("Must enter 1, 2, or 3, please try again.")
                            else:
                                results = db.search_sales(term, column)
                                for item in results:
                                    print(item)

                else:
                    print("That number isn't a valid choice, please try again.")
            else:
                print("That wasn't an integer, please try again.")
        else:
            print("That number isn't a valid choice, please try again.")
    else:
        print("That wasn't an integer, please try again.")

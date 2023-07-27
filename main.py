import psycopg2


USA_selector = 'SELECT "date", "cases", "deaths" FROM "USACountry"'
Peru_selector = "TODO"


def main():
    # get user input
    user_selection = get_user_selection()

    # Fetch the data basedo on the user selection
    if user_selection == "U":
        print("TODO, EXITING")
        exit()
    elif user_selection == "P":
        print("TODO, EXITING")
        exit()
    else:
        print("That is not a valid selection, exiting program")
        exit()

# this function takes in a selector and pulls data from the OU database based on the selector


def fetch_data_from_database(country_selection):
    print('todo')
    return

# gets and returns user input


def get_user_selection():
  # get input from user
    user_selection = ''
    user_selection = input(
        "What country would you like data for?\nPress U for USA Press P for Peru:\n")

    # set input to uppercase for cosistency
    user_selection = user_selection.upper()

    return user_selection


if __name__ == "__main__":
    main()

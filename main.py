import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


USA_selector = 'SELECT "date", "cases", "deaths" FROM "USACountry"'
Peru_selector = "TODO"


def main():
    # get user input
    user_selection = get_user_selection()

    # Fetch the data based on the user selection
    country_selection = ''

    if user_selection == "U":
        country_selection = USA_selector
    elif user_selection == "P":
        print("TODO, EXITING")
        exit()
    else:
        print("That is not a valid selection, exiting program")
        exit()

    # now pull the data from the database
    database_results = fetch_data_from_database(country_selection)

# this function takes in a selector and pulls data from the OU database based on the selector


def fetch_data_from_database(country_selection):
    try:
        conn = psycopg2.connect(
            host="pixel.ourcloud.ou.edu",
            port=5432,
            database="panviz",
            user="panviz_readonly",
            password="T3u&c7U58V9H"
        )
    except Exception as err:
        print("Unable to connect! Exiting! Error:", err)
        exit()
    cursor = conn.cursor()
    cursor.execute(country_selection)
    results = cursor.fetchall()
    conn.close()
    return results

# gets and returns user input


def get_user_selection():
  # get input from user
    user_selection = ''
    user_selection = input(
        "What country would you like data for?\nPress U for USA Press P for Peru:\n")

    # set input to uppercase for cosistency
    user_selection = user_selection.upper()

    return user_selection

# Function to create 3d scatter plots


def create_3d_scatter_plot(dates, cases, deaths):
    dates_numeric = mdates.date2num(dates)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_date(dates_numeric, cases, deaths,
                 marker='o', linestyle='-', tz=None)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.set_zlabel("Deaths")
    ax.set_title("COVID-19 Cases and Deaths Over Time")
    # Change the number of ticks as needed
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    return fig, ax


if __name__ == "__main__":
    main()

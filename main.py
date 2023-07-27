import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd


USA_selector = 'SELECT "date", "cases", "deaths" FROM "USACountry"'
Peru_selector = 'SELECT "fecha_resultado", "num_death_cases", "num_positive_cases" FROM public.distrito_death_positive_cases'


def main():
    # get user input
    user_selection = get_user_selection()

    # Fetch the data based on the user selection
    country_selection = ''

    if user_selection == "U":
        country_selection = USA_selector
        database_results = fetch_data_from_database(country_selection)
        plot_3D(database_results)
    elif user_selection == "P":
        country_selection = Peru_selector
        database_results = fetch_data_from_database(country_selection)

        # Create a DataFrame from your data
        df = pd.DataFrame(database_results, columns=[
                          'fecha_resultado', 'num_death_cases', 'num_positive_cases'])

        # Convert 'num_positive_cases' and 'num_death_cases' to integers
        df['num_positive_cases'] = df['num_positive_cases'].astype(int)
        df['num_death_cases'] = df['num_death_cases'].astype(int)

        # Group by date and sum cases and deaths
        grouped_df = df.groupby('fecha_resultado').agg(
            {'num_positive_cases': 'sum', 'num_death_cases': 'sum'}).reset_index()

        # Convert 'fecha_resultado' to datetime
        grouped_df['fecha_resultado'] = pd.to_datetime(
            grouped_df['fecha_resultado'])

        # Save the original dates for later
        date_labels = grouped_df['fecha_resultado'].dt.strftime('%Y-%m-%d')

        # Convert 'fecha_resultado' to a numerical value for plotting (e.g., number of days since the first date in the dataset)
        grouped_df['fecha_resultado'] = (
            grouped_df['fecha_resultado'] - grouped_df['fecha_resultado'].min()).dt.days

        # Create 3D scatter plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(grouped_df['fecha_resultado'],
                   grouped_df['num_positive_cases'], grouped_df['num_death_cases'])

        # Set the x-ticks and their labels
        step_size = min(60, len(grouped_df['fecha_resultado']))
        ax.set_xticks(grouped_df['fecha_resultado']
                      [::step_size])  # Choose every nth date
        # Choose every nth date label
        ax.set_xticklabels(date_labels[::step_size], rotation=45, ha='right')

        ax.set_xlabel('Fecha Resultado')
        ax.set_ylabel('Num Positive Cases')
        ax.set_zlabel('Num Death Cases')

        plt.show()
    else:
        print("That is not a valid selection, exiting program")
        exit()


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


def plot_3D(database_results):
    # break the data down into components
    dates = [result[0] for result in database_results]
    cases = [result[1] for result in database_results]
    deaths = [result[2] for result in database_results]

    fig, ax = create_3d_scatter_plot(dates, cases, deaths)

    plt.show()


if __name__ == "__main__":
    main()

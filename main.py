# Import necessary libraries
import psycopg2  # For connecting to and interacting with the database
import matplotlib.pyplot as plt  # For creating plots
import pandas as pd  # For data manipulation
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots

# SQL commands to fetch data from the database
USA_selector = 'SELECT "date", "cases", "deaths" FROM "USACountry"'
Peru_selector = 'SELECT "fecha_resultado", "num_positive_cases", "num_death_cases" FROM public.distrito_death_positive_cases'


def main():
    # Get the user's choice (U for USA or P for Peru)
    user_selection = get_user_selection()

    # Based on the user's choice, fetch the appropriate data and plot it
    if user_selection == "U":
        plot_3D(USA_selector, ['date', 'cases', 'deaths'])
    elif user_selection == "P":
        plot_3D(Peru_selector, ['fecha_resultado',
                'num_positive_cases', 'num_death_cases'])
    else:
        print("That is not a valid selection, exiting program")
        exit()


def fetch_data_from_database(country_selection):
    # Try to connect to the database
    try:
        conn = psycopg2.connect(
            host="pixel.ourcloud.ou.edu",
            port=5432,
            database="panviz",
            user="panviz_readonly",
            password="T3u&c7U58V9H"
        )
    except Exception as err:
        # If the connection fails, print the error message and exit the program
        print("Unable to connect! Exiting! Error:", err)
        exit()

    # If the connection is successful, fetch the data
    cursor = conn.cursor()
    cursor.execute(country_selection)
    results = cursor.fetchall()

    # Print out the first line of the returned data
    print("First line of data:", results[0])

    # Close the connection to the database
    conn.close()

    # Return the fetched data
    return results


def get_user_selection():
    # Ask the user to choose a country and return their choice
    user_selection = input(
        "What country would you like data for?\nPress U for USA Press P for Peru:\n")
    # Convert the choice to uppercase for consistency
    user_selection = user_selection.upper()
    return user_selection


def plot_3D(country_selection, column_names):
    # Fetch the data
    database_results = fetch_data_from_database(country_selection)

    # Convert the data into a DataFrame (a table-like data structure)
    df = pd.DataFrame(database_results, columns=column_names)

    # Make sure the numbers in the 'cases' and 'deaths' columns are integers
    df[column_names[1]] = df[column_names[1]].astype(int)
    df[column_names[2]] = df[column_names[2]].astype(int)

    # Group the data by date and add up the number of cases and deaths for each date
    grouped_df = df.groupby(column_names[0]).agg(
        {column_names[1]: 'sum', column_names[2]: 'sum'}).reset_index()

    # Normalize the 'cases' and 'deaths' columns
    grouped_df[column_names[1]] = (grouped_df[column_names[1]] - grouped_df[column_names[1]].min()) / (
        grouped_df[column_names[1]].max() - grouped_df[column_names[1]].min())
    grouped_df[column_names[2]] = (grouped_df[column_names[2]] - grouped_df[column_names[2]].min()) / (
        grouped_df[column_names[2]].max() - grouped_df[column_names[2]].min())

    # Convert the dates to a format that can be used for plotting
    grouped_df[column_names[0]] = pd.to_datetime(grouped_df[column_names[0]])

    # Save the dates as strings for the x-axis labels
    date_labels = grouped_df[column_names[0]].dt.strftime('%Y-%m-%d')

    # Convert the dates to numbers (number of days since the first date) for plotting
    grouped_df[column_names[0]] = (
        grouped_df[column_names[0]] - grouped_df[column_names[0]].min()).dt.days

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Add the data to the plot
    ax.scatter(grouped_df[column_names[0]],
               grouped_df[column_names[1]], grouped_df[column_names[2]])

    # Set the x-axis labels to show every 60th date
    step_size = min(60, len(grouped_df[column_names[0]]))
    ax.set_xticks(grouped_df[column_names[0]][::step_size])
    ax.set_xticklabels(date_labels[::step_size], rotation=45, ha='right')

    # Set the labels for the x, y, and z axes
    ax.set_xlabel(column_names[0])
    ax.set_ylabel(column_names[1])
    ax.set_zlabel(column_names[2])

    # Show the plot
    plt.show()


# If this script is being run directly (not imported as a module), start the program by calling the main() function
if __name__ == "__main__":
    main()

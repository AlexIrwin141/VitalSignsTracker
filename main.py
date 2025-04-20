import pandas as pd
from datetime import datetime
from AddData import get_bp, get_date, get_pulse_rate , get_temp, get_weight, get_notes
from matplotlib import pyplot as plt
import matplotlib.dates as mdates



#import tkinter as tk
#from tkinter import filedialog
# This is a different test comment for gitlab ci/cd testing.

class csv_source:
    """
    A class to handle CSV file operations for storing and retrieving vital sign data.
    Manages data loading, creation, and filtering based on date ranges.
    """

    COLUMN_NAMES = ["date", "bp_sys", "bp_dia", "pulse_rate", "weight", "temp", "notes"]
    FILE_NAME = "vitals.csv"
    DATE_FORMAT = "%m/%d/%Y"
    DATA_DICT = {
                "date": "string",
                "bp_sys": "int",
                "bp_dia": "int",
                "pulse_rate": "int",
                "weight": "int",
                "temp": "float",
                "notes": "string"
                }
    
    @classmethod
    def get_data(cls):
        """
        Load or create a CSV file containing vital sign records.

        Returns:
            pd.DataFrame: A DataFrame containing the loaded data or an empty DataFrame if the file does not exist.
        """
        try:
            mydf = pd.read_csv(cls.FILE_NAME, dtype=cls.DATA_DICT, parse_dates=["date"])
            return mydf

        except FileNotFoundError:
            mydf = pd.DataFrame(columns = cls.COLUMN_NAMES).astype(cls.DATA_DICT    )
            mydf.to_csv(cls.FILE_NAME, index = False)
            print('Created new file')
            return mydf


    @classmethod
    def show_range(cls, begin_date, end_date):
        """
        Display records within a specified date range and optionally plot a visualization.

        Parameters:
            begin_date (str): The start date of the range (formatted as 'mm/dd/yyyy').
            end_date (str): The end date of the range (formatted as 'mm/dd/yyyy').

        Returns:
            None: Prints the filtered data and displays a plot if requested.
        """
        df = cls.get_data()

        df['date'] = pd.to_datetime(df["date"], format=csv_source.DATE_FORMAT)
        begin_date = datetime.strptime(begin_date, csv_source.DATE_FORMAT)
        end_date = datetime.strptime(end_date, csv_source.DATE_FORMAT)

        filtered_df = df.loc[(df["date"] >= begin_date) & (df["date"] <= end_date)].copy()
        filtered_df['notes'] = filtered_df['notes'].fillna('')
        filtered_df.set_index(filtered_df.date, inplace=True)

        filtered_df.index.name='Filter1'


        filtered_df.set_index('date', drop = False, inplace=True)
        filtered_df = filtered_df.resample('D').asfreq(fill_value = 0)

        # Ensure 'notes' column exists and mark missing days
        if 'notes' not in filtered_df.columns:
            filtered_df['notes'] = ""

        # Define which columns should be checked for all zero values
        vital_columns = ['bp_sys', 'bp_dia', 'pulse_rate', 'weight', 'temp']
        filtered_df[vital_columns] = filtered_df[vital_columns].apply(pd.to_numeric, errors='coerce')
        # Identify rows where all values in vital_columns are zero
        filtered_df.loc[filtered_df[vital_columns].eq(0).all(axis=1), 'notes'] = 'missing day'


        filtered_df['date_index'] = filtered_df.index
        filtered_df.index.name = 'BBID'


        if filtered_df.empty:
            print('No entries found within given range.')
        else:

            # Find the minimum and maximum dates
            begin_date = begin_date.strftime(csv_source.DATE_FORMAT)
            end_date = end_date.strftime(csv_source.DATE_FORMAT)


            print(f'Here are the most recent 10 entries from {begin_date} to {end_date}')

            print(filtered_df.tail(10).to_string(index=False, formatters={"date_index" : lambda x: x.strftime(csv_source.DATE_FORMAT)  }))

            if input('WWould you like to see a visualization? ').lower() == 'y':

                title_for_plot = f'Here are the most recent 10 entries from {begin_date} to {end_date}'

                vitals_display(filtered_df, begin_date, end_date)


def add_or_update_record(date, sys_bp, dia_bp, pulse_rate, weight, temp, notes):
    """
    Add a new record or update an existing record based on the date.

    Parameters:
        date (str): The date of the record to add or update (formatted as 'mm/dd/yyyy').
        sys_bp (int): Systolic blood pressure value.
        dia_bp (int): Diastolic blood pressure value.
        pulse_rate (int): Pulse rate in beats per minute.
        weight (int): Weight in pounds.
        temp (float): Body temperature in degrees Fahrenheit.
        notes (str): Additional notes for the record.

    Returns:
        None: Prints confirmation of the record addition or update and writes to the CSV file.
    """
 
    df = csv_source.get_data()

    # Check if the date already exists
    if date in df['date'].values:
        # Update existing entry
        df.loc[df['date'] == date, ['bp_sys', 'bp_dia', 'pulse_rate', 'weight', 'temp', 'notes']] = \
            [int(sys_bp), int(dia_bp), int(pulse_rate), int(weight), float(temp), notes]
        print(f"Updated existing record for {date}")
    else:
        # Append new entry
        new_record = pd.DataFrame([{
            "date": date, "bp_sys": sys_bp, "bp_dia": dia_bp,
            "pulse_rate": pulse_rate, "weight": weight,
            "temp": temp, "notes": notes
        }])
        df = pd.concat([df, new_record], ignore_index=True)
    try:
        df.to_csv(csv_source.FILE_NAME, index=False)
        print(f"Added new record for {date}")
    except PermissionError:
        print('Unable to write to file')




def new_entry():
    """
    Prompt the user for vital sign data and add it to the CSV file.
    
    Returns:
        None: Collects user input and calls `add_or_update_record` to save the data.
    """

    this_df = csv_source.get_data()

    # Collect data
    date= get_date("date or leave blank for today's date", this_df, allow_default=True)
    bp_sys, bp_dia = get_bp()
    pulse_rate = get_pulse_rate()
    weight = get_weight()
    temp = get_temp()
    notes = get_notes()

    # Use the new function to add or update the record
    add_or_update_record(date, bp_sys, bp_dia, pulse_rate, weight, temp, notes)
    

def vitals_display(df: pd.DataFrame, begin_date, end_date):
    """
    Plot the vital signs for a specified date range.

    Parameters:
        df (pd.DataFrame): DataFrame containing the filtered data for the date range.
        begin_date (str): The beginning date of the displayed range (formatted as 'mm/dd/yyyy').
        end_date (str): The ending date of the displayed range (formatted as 'mm/dd/yyyy').

    Returns:
        None: Displays a multi-plot chart with vital sign trends over time.
    """

    fig, ax = plt.subplots(4, figsize = (15, 8), sharex=True)


    # Set x-axis to only show full days
    ax[0].xaxis.set_major_locator(mdates.DayLocator())
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))    

    ax[0].xaxis.set_tick_params(rotation = 90)

    ax[0].set_title(f'Vital signs from {begin_date} to {end_date}.')
    ax[3].set_xlabel('Date')
    ax[0].set_ylabel('Pressure')

    ax[1].set_ylabel('Weight lbs')
    ax[2].set_ylabel('Temperature F.')
    ax[3].set_ylabel('Pulse Rate')
    ax[3].xaxis.set_tick_params(rotation = 90)


    if len(df) ==1:
        # Just the one point to plot
        ax1, = ax[0].plot(df['date_index'], df['bp_sys'], 'o', label='Systolic BP', color='blue')
        ax2, = ax[0].plot(df['date_index'], df['bp_dia'], 'o', label='Diastolic BP', color='cyan')
        ax3, = ax[1].plot(df['date_index'], df['weight'], 'o', label='Weight', color='orange')
        ax4, = ax[2].plot(df['date_index'], df['temp'], 'o', label='Temperature', color='green')
        ax5, = ax[3].plot(df['date_index'], df['pulse_rate'], 'o', label='Pulse Rate', color='red')
    else:
        ax1, = ax[0].plot(df['date_index'], df['bp_sys'], label = 'BP Systolic')
        ax2, = ax[0].plot(df['date_index'], df['bp_dia'], label = 'BP Diastolic')
        ax3, = ax[1].plot(df['date_index'], df['weight'])
        ax4, = ax[2].plot(df['date_index'], df['temp'], color = 'green')
        ax5, = ax[3].plot(df['date_index'], df['pulse_rate'], color = 'red')


    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[3].grid()


    ax1.set_label('Systolic')
    ax2.set_label('Diastolic')
    ax3.set_label('Weight')
    ax4.set_label('Temperaure F')
    ax5.set_label('Pulse rate')

    ax[0].legend()

    fig.autofmt_xdate(rotation=45)
    plt.tight_layout()

    plt.show()



def main():
    """
    Main function to present options for adding data, viewing records, or exiting.
    Repeats until the user selects 'Exit'.

    Returns:
        None: Prompts the user for input and calls the appropriate functions.
    """
    while True:

        print("\nPlease choose from the following options.")
        print("1. Add new entry.")
        print("2. View records in a date range.")
        print("3. Exit")
        choice = input("Press 1, 2 or 3. ")

        # cycle through the options until we find the selected one.
        if choice == '1':
            new_entry()
        elif choice == '2':
            begin_date = get_date("start date", None, True)
            end_date = get_date("end date", None, True)
            csv_source.show_range(begin_date, end_date)
        elif choice == '3':
            print("Now leaving the program.")
            break
        else:
            print("Invalid entry. Please select 1, 2 or 3")

if __name__ == "__main__":
    main()
        


    
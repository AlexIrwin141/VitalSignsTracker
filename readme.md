Vital Signs Tracking CLI Application  

A command-line application for tracking daily vital signs such as blood pressure, pulse rate, weight, and temperature. This application allows users to record and view health metrics over time, with the option to add notes for each entry. It also provides visualizations for better analysis of health trends within a specified date range.  

I wrote this both as a way to help me learn python and also when I was discharged from hospital after a lengthy stay and major surgery I had to keep track of my vital signs each day and periodically report them.


Features  

Add New Entry: Enter vital signs for the day, including blood pressure (systolic and diastolic), pulse rate, weight, temperature, and notes.
View Records: Display records within a user-specified date range, including any missing days.
Data Visualization: Generate a plot of selected vital signs over a date range for easy analysis.
CSV Storage: All records are saved to a CSV file, allowing for simple data storage and retrieval.


Requirements  
Python 3.7+

Ensure dependencies are installed:
pip install -r requirements.txt  

Installation
Clone the Repository:
git clone https://github.com/AlexIrwin141/VitalSignsTracker
cd VitalSignsTracker

Set up Virtual Environment:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Usage  

Add New Entry:

Choose the option to add a new entry.
Follow prompts to enter the date, blood pressure (systolic and diastolic), pulse rate, weight, temperature, and any notes.
Entries are automatically validated to ensure they are within realistic ranges.  

View Records:

Choose the option to view records within a date range.
Enter the start and end dates.
The application will display records in that range, with missing days indicated in the notes.
Optionally, generate a visualization of the data.  

Exit:

Choose the exit option to close the application.  

File Structure  

main.py: The main entry point of the application, including the menu and core functions for data input and display.  
csv_source: Contains the methods for reading and writing to the CSV file.  
AddData.py: Contains input validation and data prompting functions.  
vitals.csv: The CSV file where all records are stored.  

Code Structure  

csv_source Class
get_data: Loads the CSV file or creates a new one if it doesn’t exist.  
show_range: Displays records within a specific date range and generates a visualization if requested.  

Utility Functions  

add_or_update_record: Adds a new entry or updates an existing record if the date already exists.  
get_date, get_bp, get_pulse_rate, get_weight, get_temp, get_notes: Utility functions for validating and collecting user input for each data field.  

License
This project is licensed under the MIT License. See the LICENSE file for details.

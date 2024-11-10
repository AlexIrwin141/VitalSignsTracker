from datetime import datetime

date_format = "%m/%d/%Y"
BP_SYS_MIN, BP_SYS_MAX = 50, 250
BP_DIA_MIN, BP_DIA_MAX = 30, 150
PULSE_RATE_MIN, PULSE_RATE_MAX = 45, 250
WEIGHT_MIN, WEIGHT_MAX = 50, 500
TEMP_MIN, TEMP_MAX = 90, 115

# Adding a prompt here to ask the user what the date represents
def get_date(which_date, this_df, allow_default = True):

    """
    Prompt the user for a date, validate the format, and return it.
    
    Parameters:
        which_date (str): Description of the date to prompt for.
        allow_default (bool): Whether to use today's date as the default if no input is given.
        
    Returns:
        str: The validated date as a string in the specified format.
    """    
    while True:
        my_date = input(f"please enter the {which_date} in the format mm/dd/yyyy:")
        #if default is allowed and no date is entered return todays date
        if allow_default and not my_date:
            useToday = input(f"No date entered. Use today's date ({datetime.today().strftime(date_format)})? (Y/N): ")
            if useToday.strip().upper() == 'Y':
                return datetime.today().strftime(date_format)
            else:
                continue  # Prompt for date

        # validate the date
        try:
            #try and get the date into a date type in the correct format
            valid_date = datetime.strptime(my_date, date_format)
            return valid_date.strftime(date_format)

        except ValueError:
            print('Invalid date')
    


def get_bp():
    """
    Prompt the user to enter their blood pressure as systolic/diastolic, validate it, 
    and provide feedback on the reading level.

    The function requests the user to input systolic and diastolic blood pressure values 
    in the format "120/80". It then performs the following checks:
    - Ensures the systolic and diastolic values are numeric and within acceptable ranges.
    - Verifies that systolic is greater than diastolic.
    - Provides a brief health warning message based on the user's input.

    If input is invalid, the function will re-prompt the user.

    Returns:
        tuple: A tuple (bpsys, bpdia) where `bpsys` is the validated systolic blood pressure 
        and `bpdia` is the validated diastolic blood pressure as integers.
    """
        
    #check to see we have values within realistic levels
    try:
        bp = input(f"Please enter sys bp in whatever it is measured in, e.g. 120/80: ").split('/')
        if len(bp) != 2 or not (bp[0].isnumeric() and bp[1].isnumeric()):
            raise ValueError
    
        bpsys, bpdia = int(bp[0]), int(bp[1])

        # Check for unrealistic values or if the diastolic value is higher that the systolic value (it shouldn't be)

        if not (BP_SYS_MIN <= bpsys <= BP_SYS_MAX and BP_DIA_MIN <= bpdia <= BP_DIA_MAX and bpsys > bpdia):
            print('Please enter some realistic values')
            return get_bp()

        # Going to check on any possible worrying levels to mention.
        if (120 <= bpsys <= 129) and (bpdia < 80):
            bp_warning = 'Just saying your BP is slightly elevated'
        elif (130 <= bpsys <=139) or (80 <= bpdia <= 90):
            bp_warning = 'High BP. Possibly hypertension stage 1'
        elif bpsys >= 140 or bpdia >= 90:
            bp_warning = 'High BP. Possibly hypertension stage 2'
        elif bpsys > 180 or bpdia > 120:
            bp_warning = 'High BP. Possibly hypertensive crisis. Please consult a doctor.'
        else:
            bp_warning = 'Great. Looks normal.'

        print(bp_warning)

        return (bpsys, bpdia)
    except ValueError:
        return get_bp()

def validate_numeric_input(prompt, min_val, max_val):
    """
    Prompt for a numeric input, validate range, and return it.

    Parameters:
        prompt (str): Input prompt for the user.
        min_val (int/float): Minimum allowed value.
        max_val (int/float): Maximum allowed value.

    Returns:
        int/float: Validated numeric input.
    """
    while True:
        try:
            value = float(input(prompt))
            if not (min_val <= value <= max_val):
                print(f"Please enter a value between {min_val} and {max_val}.")
                continue
            return value
            
        except ValueError:
            print("Invalid input. Please enter a number.")

    
def get_pulse_rate():
    return int(validate_numeric_input("Please enter your pulse rate: ", PULSE_RATE_MIN, PULSE_RATE_MAX))


def get_weight():
    return validate_numeric_input("Please enter your weight in pounds: ", WEIGHT_MIN, WEIGHT_MAX)


def get_temp():
    return validate_numeric_input("Please enter your temperature in °F: ", TEMP_MIN, TEMP_MAX)


def get_notes():
    notes = input("Are there any notes you would like to add? Leave blank if not.: ")
    return notes if notes.strip() else ''

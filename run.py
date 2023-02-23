from datetime import date
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('codeinstitute-utilities')
custom_theme = Theme({
    "error": "red3", 
    "success": "green3", 
    "title": "bold bright_green", 
    "choice": "gold1",
    "description": "cornflower_blue"
    })
console = Console(theme=custom_theme)

# Main function

def main():
    """
    Run all program functions.
    """
    while True:
        choose_utilitie()

# Menu functions

def choose_utilitie():
    """
    Calls the appropriate utility function based on the users selection.
    """
    while True:
        console.print("Main menu.\n", style="title")
        console.print("Enter 1 to manage 'electricity' worksheet.", style="choice")
        console.print("Enter 2 to manage 'broadband' worksheet.", style="choice")
        console.print("Enter 3 to manage 'food' worksheet.", style="choice")
        console.print("Enter 4 to manage 'gas' worksheet.\n", style="choice")
        option = input("Enter your choice:\n")
        if option == '1':
            edit_worksheet('electricity')
        elif option == '2':
            edit_worksheet('broadband')
        elif option == '3':
            edit_worksheet('food')
        elif option == '4':
            edit_worksheet('gas')
        else:
            console.print("There is no such option. Retry your input.\n", style="error")


def edit_worksheet(worksheet):
    """
    Choice of the relevant worksheets for editing.
    """
    while True:
        console.print(f"\nActions with {worksheet} worksheet:\n", style="title")
        console.print("Enter 1 to 'add' one row.", style="choice")
        console.print("Enter 2 to 'delete' last row.", style="choice")
        console.print("Enter 3 to check 'statistics'.", style="choice")
        console.print("Enter 4 to see the 'table'.", style="choice")
        console.print("Enter 0 to go 'back'.\n", style="choice")
        option = input("Enter your choice:\n")
        if option == '1':
            if worksheet == 'electricity':
                data = get_data_with_meter(worksheet)
                update_worksheet(data, worksheet)
            elif worksheet == 'food':
                data = get_data_without_meter(worksheet)
                update_worksheet(data, worksheet)
            elif worksheet == 'broadband':
                data = get_data_without_meter(worksheet)
                update_worksheet(data, worksheet)
            elif worksheet == 'gas':
                data = get_data_without_meter(worksheet)
                update_worksheet(data, worksheet)
            else:
                print(f"Action is not ready for worksheet {worksheet}!\n", style="error")
                main()
        elif option == '2':
            delete_last_row(worksheet)
        elif option == '3':
            statistics(worksheet)
        elif option == '4':
            visualize(worksheet)
        elif option == '0':
            print()
            main()
        else:
            console.print("There is no such option. Retry your input.", style="error")


def statistics(worksheet):
    """
    Shows statistics for relevant worksheet.
    """
    while True:
        console.print(f"\nSelect statistics from {worksheet} worksheet.\n", style="title")
        console.print("Enter 1 to show statistics 'at all'.", style="choice")
        console.print("Enter 2 to show statistics for 'last month'.", style="choice")
        console.print("Enter 3 to show statistics for 'last 3 months'.", style="choice")
        console.print("Enter 0 to go 'back'.", style="choice")
        option = input("\nEnter your choice:\n")
        if option == '1':
            statistics_average_all(worksheet)
        if option == '2':
            term = 30
            statistics_average_term(worksheet, term)
        if option == '3':
            term = 91
            statistics_average_term(worksheet, term)
        elif option == '0':
            edit_worksheet(worksheet)
        else:
            console.print("There is no such option. Retry your input.", style="error")

# Vizualize function to see the table

def visualize(worksheet):
    """
    Build vizual viewing of a relevant worksheet.
    """
    worksheet_data = SHEET.worksheet(worksheet).get_all_values()
    table = Table(title=f"\nTable of {worksheet} worksheet")

    for heading in worksheet_data[0]:
        table.add_column(f"{heading}")

    for row in worksheet_data[1::1]:
        table.add_row(*row)

    console.print(table)

# Calculating statistics function

def statistics_average_all(worksheet):
    """
    Calculate average cost per day of relevant utility for all time.
    """
    days_list = SHEET.worksheet(worksheet).col_values(3)[2:]
    costs_per_day = SHEET.worksheet(worksheet).col_values(4)[2:]
    if worksheet == 'electricity':
        days_list = SHEET.worksheet(worksheet).col_values(5)[2:]
        costs_per_day = SHEET.worksheet(worksheet).col_values(7)[2:]
    costs_sum = 0
    days_sum = 0
    for days, cost_per_day in zip(days_list, costs_per_day):
        costs_sum = costs_sum + (int(days) * float(cost_per_day))
        days_sum = days_sum + int(days)
    average = round((costs_sum / days_sum), 2)
    console.print(f"\nStatistics for all time from {worksheet} worksheet.\n", style="title")
    console.print(f"Total number of days: {days_sum}.", style="description")
    console.print(f"Total costs for all time: {round(costs_sum, 2)}.", style="description")
    console.print(f"Average cost per day for all time: {average}.", style="description")

    statistics(worksheet)


def statistics_average_term(worksheet, term):
    """
    Calculate average cost per day of relevant utility for last month.
    """
    days_list = SHEET.worksheet(worksheet).col_values(3)[2:]
    costs_per_day = SHEET.worksheet(worksheet).col_values(4)[2:]
    if worksheet == 'electricity':
        days_list = SHEET.worksheet(worksheet).col_values(5)[2:]
        costs_per_day = SHEET.worksheet(worksheet).col_values(7)[2:]
    days_sum = 0
    days_list.reverse()
    i = 0
    for days in days_list:
        i = i + 1
        days_sum = days_sum + int(days)
        if days_sum >= term:
            break
    days_exceeded = days_sum - term
    costs_per_day.reverse()
    costs_sum = 0
    for days, cost_per_day in zip(days_list[0:i], costs_per_day[0:i]):
        costs_sum = costs_sum + (int(days) * float(cost_per_day))
    average = round((costs_sum / days_sum), 2)
    if days_exceeded > 0:
        costs_sum_term = average * (days_sum - days_exceeded)
    else:
        costs_sum_term = costs_sum
    if term == 30:
        console.print(f"\nStatistics for last month from {worksheet} worksheet.\n", style="title")
        console.print(f"Total costs for last month: {round(costs_sum_term, 2)}.", style="description")
        console.print(f"Average cost per day for last month: {average}.", style="description")
    elif term == 91:
        console.print(f"\nStatistics for last 3 months from {worksheet} worksheet.\n", style="title")
        console.print(f"Total costs for last 3 months: {round(costs_sum_term, 2)}.", style="description")
        console.print(f"Average cost per day for last 3 months: {average}.", style="description")

    statistics(worksheet)

# Get functions

def get_data_with_meter(worksheet):
    """
    Gets date, meter reading and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must date, be meter reading and price.
    The loops will repeatedly request data, until it is valid.
    """
    console.print(f"\nPlease enter {worksheet} data.", style="description")
    console.print("Data should be: date, meter reading and unit price.", style="description")

    while True:

        today = date.today().strftime("%d.%m.%Y")
        last_date = SHEET.worksheet(worksheet).get_all_values()[-1][0]
        console.print("\nEnter the date. Leave blank to enter today's date.", style="choice")
        date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")
        validated_date = validate_date(worksheet, date_input, last_date)

        if validated_date:

            while True:

                last_meter_reading = SHEET.worksheet(worksheet).get_all_values()[-1][1]
                console.print("\nEnter meter reading.", style="choice")
                meter_reading = input(f"Previous value: {last_meter_reading}.\n")
                validated_meter = validate_meter(meter_reading, worksheet)

                if validated_meter:

                    while True:
                        last_price = SHEET.worksheet(worksheet).get_all_values()[-1][2]
                        console.print("\nEnter the price, €.", style="choice")
                        price_input = input(f"Leave blank for previous price: {last_price}€.\n")

                        validated_price = validate_price(price_input, last_price)
                        if validated_price:
                            break

                    break

            break

    entered_data = [str(validated_date), str(validated_meter), str(validated_price)]
    calculated_data = calculate_data(entered_data, worksheet)

    return calculated_data


def get_data_without_meter(worksheet):
    """
    Gets date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be date and price.
    The loops will repeatedly request data, until it is valid.
    """
    console.print(f"\nPlease enter {worksheet} data.", style="description")
    console.print("Data should be: date and price from last bill.", style="description")

    while True:

        today = date.today().strftime("%d.%m.%Y")
        last_date = SHEET.worksheet(worksheet).get_all_values()[-1][0]
        console.print("\nEnter the date. Leave blank to enter today's date.", style="choice")
        date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")
        validated_date = validate_date(worksheet, date_input, last_date)

        if validated_date:

            while True:

                last_price = SHEET.worksheet(worksheet).get_all_values()[-1][1]
                console.print("\nEnter the price, €.", style="choice")
                price_input = input(f"Leave blank for previous price: {last_price}€.\n")
                validated_price = validate_price(price_input, last_price)

                if validated_price:
                    break

            break

    entered_data = [str(validated_date), str(validated_price)]
    calculated_data = calculate_data(entered_data, worksheet)

    return calculated_data

# Calculate function

def calculate_data(data, worksheet):
    """
    Calculation of the total utility consumption and the number of days
    between the last data and the entered one.
    Calculation of average utility consumption per day and cost per day.
    """
    console.print("\nCalculating...", style="success")
    last_data = SHEET.worksheet(worksheet).get_all_values()[-1]
    if worksheet == 'electricity': # calculating meeter reading
        # Calculation of how much electricity has been spent since the last measurement
        diff_meter = float(data[1]) - float(last_data[1])
        diff_meter_rounded = round(diff_meter, 1)
        data.append(str(diff_meter_rounded))
    # Calculation of the number of days since the last enter
    date_format = "%d.%m.%Y"
    prev_date = datetime.strptime(last_data[0], date_format)
    new_date = datetime.strptime(data[0], date_format)
    diff_days = new_date - prev_date
    diff_days_num = diff_days.days
    data.append(str(diff_days_num))
    if worksheet == 'electricity': # costs depends on meeter reading
        # Calculation of average electricity consumption per day since the last measurement
        consumption = diff_meter / diff_days_num
        consumption_rounded = round(consumption, 1)
        data.append(str(consumption_rounded))
        # Calculation of the average cost of electricity consumed per day since the last measurement
        cost = consumption * float(data[2])
        cost_rounded = round(cost, 2)
        data.append(str(cost_rounded))
    elif worksheet == 'broadband': # bills after consumption
        # Calculation of average broadband price per day
        consumption = float(data[1]) / diff_days_num
        consumption_rounded = round(consumption, 2)
        data.append(str(consumption_rounded))
    else: # bills before consumption
        # Calculation of average utility price per day
        consumption = float(last_data[1]) / diff_days_num
        consumption_rounded = round(consumption, 2)
        data.append(str(consumption_rounded))
    console.print("\ncalculation finished.", style="success")

    return data

# Validate functions

def validate_meter(value, worksheet):
    """
    Recieves a data as a string. Inside the try,
    checks if it's not empty string, and then converts it to float.
    Raises ValueError if string can not be converted into float.
    Checks if it's not less than previous meter reading.
    """
    try:
        if value == '':
            raise ValueError(
                "meter readings value cannot be empty"
            )

        new_meter_reading = float(value)
        last_meter_reading = float(SHEET.worksheet(worksheet).get_all_values()[-1][1])

        if new_meter_reading < last_meter_reading:
            raise ValueError(
                f"new meter value {new_meter_reading} cannot be less then previous {last_meter_reading}"
            )
        console.print("Meter readings is valid.", style="success")

    except ValueError as error:
        error_string = str(error)
        if error_string.startswith("could not convert string to float"):
            console.print("Meter readings do not support word or letter input,", style="error")
            console.print("enter numbers: decimals must be separated by a dot, please try again.", style="error")
        else:
            console.print(f"Invalid data: {error}, please try again.", style="error")
        return False

    return new_meter_reading


def validate_price(value, last_price):
    """
    Recieves a price as a string.
    Checks if it's empty string, to return previous price.
    Inside the try, converts string value into float.
    Raises ValueError if strings can not be converted into float.
    Checks if it's not a zero.
    """
    try:
        if value == '':
            value = last_price
            console.print(f"No date provided, entering last known price: {value}€.", style="success")
            return value

        float_value = float(value)

        if float_value == 0:
            console.print("Utility cannot be free, please try again.", style="error")
            return False
        elif float_value < 0:
            console.print("Price cannot be negative, please try again.", style="error")
            return False

        console.print(f"Price {float_value}€ is valid.", style="success")
        return float_value

    except ValueError as error:
        error_string = str(error)
        if error_string.startswith("could not convert string to float"):
            console.print("Price don't support word or letter input, enter numbers:", style="error")
            console.print("decimals must be separated by a dot, please try again.", style="error")
        else:
            print(f"Invalid data: {error}, please try again.", style="error")
        return False


def validate_date(worksheet, value, last_date):
    """
    Recieves a date as a string.
    Checks if it's empty string, to return today's date.
    Inside the try, converts string value into date.
    Raises ValueError if strings can not be converted into date.
    Checks if it's not before last date and after today's date.
    """
    today = date.today().strftime("%d.%m.%Y")
    date_format = "%d.%m.%Y"
    try:

        if value == '':
            value = date.today().strftime(date_format)

            date_value = datetime.strptime(value, date_format)
            last_date_value = datetime.strptime(last_date, date_format)
            today_value = datetime.strptime(today, date_format)

            if last_date_value == today_value:
                console.print(f"Entered date {value} cannot be the same day as last entered date {last_date}.", style="error")
                console.print("Come back tomorrow.\n", style="description")
                edit_worksheet(worksheet)

            console.print(f"No date provided, entering today's date: {value}", style="success")
            return value

        date_value = datetime.strptime(value, date_format)
        last_date_value = datetime.strptime(last_date, date_format)
        today_value = datetime.strptime(today, date_format)

        if date_value == last_date_value:
            console.print(f"Entered date {value} cannot be the same day as last entered day {last_date}.", style="error")
            console.print("Try again or leave blank to enter today's date or exit if today is the last entered date.", style="description")
            return False

        if date_value < last_date_value:
            console.print(f"Entered date {value} cannot be before or equal to the last date {last_date}.", style="error")
            return False

        if date_value > today_value:
            console.print(f"Entered date {value} cannot be in the future. Today is {today}.", style="error")
            return False

        console.print("Date is valid.", style="success")
        return value

    except ValueError as error:
        error_string = str(error)
        if error_string.startswith("time data"):
            console.print("Date doesn't support word or letter input,", style="error")
            console.print("enter numbers: first the day, then the month", style="error")
            console.print("and finally the year (four digits), the numbers", style="error")
            console.print("must be separated by a dot, please try again.", style="error")
        else:
            console.print(f"Invalid data: {error} please try again.", style="error")
        return False

# Update functions

def update_worksheet(data, worksheet):
    """
    Receives a list of data to be inserted into a worksheet
    and a string with the name of the worksheet.
    Update the worksheet with the data provided.
    """
    console.print(f"\nUpdating {worksheet} worksheet...\n", style="success")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    console.print(f"{worksheet} worksheet updated successfully.", style="success")
    edit_worksheet(worksheet)


def delete_last_row(worksheet):
    """
    Deleting the last row in the relevant worksheet.
    """
    while True:
        console.print(f"\nAre you sure you want to delete the last row in the {worksheet} worksheet?\n", style="title")
        console.print(f"Enter '1' to confirm deletion of the last row on the {worksheet} worksheet.", style="choice")
        console.print("Enter '0' to cancel and go back.\n", style="choice")
        confirm = input("Enter your choice:\n")
        if confirm == '1':
            worksheet_del_last = SHEET.worksheet(worksheet)
            worksheet_all_values = SHEET.worksheet(worksheet).get_all_values()
            count_rows_data = len(worksheet_all_values)
            if count_rows_data > 2:
                worksheet_del_last.delete_rows(count_rows_data)
                console.print(f"The last row on the {worksheet} worksheet has been removed.", style="success")
                edit_worksheet(worksheet)
            else:
                console.print("It is forbidden to delete the original information.", style="error")
                edit_worksheet(worksheet)
        elif confirm == '0':
            edit_worksheet(worksheet)
        else:
            console.print("There is no such option. Retry your input.", style="error")

# Program lunch

console.print("\nWelcome to v.2.0.0!\n", style="title")
console.print("This program is designed to account for utilities.", style="description")
console.print("You can select a utility service and then the action you want", style="description")
console.print("to perform or view the information.\n", style="description")
console.print("To exit program, just close the tab.", style="description")
console.print("To restart program, click button above: 'Run program'.\n", style="description")
main()

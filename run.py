from datetime import date
from datetime import datetime
from rich.console import Console
from rich.table import Table
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
        print("Main menu.\n")
        print("Enter '1' to manage electricity worksheet.")
        print("Enter '2' to manage broadband worksheet.")
        print("Enter '3' to manage food worksheet.")
        print("Enter '4' to manage gas worksheet.")
        print()
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
            print("\nCheck your choice\n")


def edit_worksheet(worksheet):
    """
    Choice of the relevant worksheets for editing.
    """
    while True:
        print()
        print(f"Actions with {worksheet} worksheet:")
        print()
        print("Enter '1' to add one row.")
        print("Enter '2' to delete last row.")
        print("Enter '3' to check statistics.")
        print("Enter '4' to see the table.")
        print("Enter '0' to go back.")
        print()
        option = input("Enter your choice:\n")
        if option == '1':
            if worksheet == 'electricity':
                data = get_electricity_data(worksheet)
                update_worksheet(data, worksheet)
            elif worksheet == 'food':
                data = get_food_data(worksheet)
                update_worksheet(data, worksheet)
            elif worksheet == 'broadband':
                data = get_broadband_data(worksheet)
                update_worksheet(data, worksheet)
            elif worksheet == 'gas':
                data = get_gas_data(worksheet)
                update_worksheet(data, worksheet)
            else:
                print(f"Action is not ready for worksheet {worksheet}!\n")
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
            print("\nCheck your choice")


def statistics(worksheet):
    """
    Shows statistics for relevant worksheet.
    """
    while True:
        print()
        print(f"Statistics from {worksheet} worksheet.")
        print()
        print("Enter '1' to show average spendings per day at all.")
        print("Enter '2' to show average spendings per day for last month.")
        print("Enter '3' to show average spendings per day for last 3 months.")
        print("Enter '0' to go back.")
        print()
        option = input("Enter your choice:\n")
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
    
    console = Console()
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
    print(f"\nTotal number of days: {days_sum}.")
    print(f"Total costs for all time: {round(costs_sum, 2)}.")
    print(f"Average cost per day for all time: {average}.")

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
        print(f"Total costs for last month: {round(costs_sum_term, 2)}.")
        print(f"Average cost per day for last month: {average}.")
    elif term == 91:
        print(f"Total costs for last 3 months: {round(costs_sum_term, 2)}.")
        print(f"Average cost per day for last 3 months: {average}.")

    statistics(worksheet)

# Get functions

def get_electricity_data(worksheet):
    """
    Gets electricity, date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be meter reading, date and price.
    The loops will repeatedly request data, until it is valid.
    """
    print("\nPlease enter electricity data.")
    print("Data should be: date, meter reading and price per kWh.")

    while True:

        today = date.today().strftime("%d.%m.%Y")
        last_date = SHEET.worksheet('electricity').get_all_values()[-1][0]
        print("\nEnter the date. Leave blank to enter today's date.")
        date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")
        validated_date = validate_date(date_input, last_date)

        if validated_date:

            while True:

                last_electricity_meter_reading = SHEET.worksheet('electricity').get_all_values()[-1][1]
                print("\nEnter meter reading.")
                electricity_meter_reading = input(f"Previous value: {last_electricity_meter_reading}.\n")
                validated_electricity_meter = validate_electricity_meter(electricity_meter_reading)

                if validated_electricity_meter:

                    while True:
                        last_price = SHEET.worksheet('electricity').get_all_values()[-1][2]
                        print("\nEnter the price, €.")
                        price_input = input(f"Leave blank for previous price: {last_price}€.\n")

                        validated_price = validate_price(price_input, last_price)
                        if validated_price:
                            break

                    break

            break

    electricity_data = [str(validated_date), str(validated_electricity_meter), str(validated_price)]
    calculated_electricity_data = calculate_data(electricity_data, worksheet)

    return calculated_electricity_data


def get_food_data(worksheet):
    """
    Gets date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be date and price.
    The loops will repeatedly request data, until it is valid.
    """

    print("\nPlease enter food data.")
    print("Data should be: date and price from last bill.")

    while True:

        today = date.today().strftime("%d.%m.%Y")
        last_date = SHEET.worksheet('food').get_all_values()[-1][0]
        print("\nEnter the date. Leave blank to enter today's date.")
        date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")
        validated_date = validate_date(date_input, last_date)

        if validated_date:

            while True:

                last_price = SHEET.worksheet('food').get_all_values()[-1][1]
                print("\nEnter the price, €.")
                price_input = input(f"Leave blank for previous price: {last_price}€.\n")
                validated_price = validate_price(price_input, last_price)

                if validated_price:
                    break

            break

    food_data = [str(validated_date), str(validated_price)]
    calculated_food_data = calculate_data(food_data, worksheet)

    return calculated_food_data


def get_broadband_data(worksheet):
    """
    Gets date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be date and price.
    The loops will repeatedly request data, until it is valid.
    """
    print("\nPlease enter broadband data.")
    print("Data should be: date and price from last bill.")

    while True:

        today = date.today().strftime("%d.%m.%Y")
        last_date = SHEET.worksheet('broadband').get_all_values()[-1][0]
        print("\nEnter the date. Leave blank to enter today's date.")
        date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")
        validated_date = validate_date(date_input, last_date)

        if validated_date:

            while True:

                last_price = SHEET.worksheet('broadband').get_all_values()[-1][1]
                print("\nEnter the price, €.")
                price_input = input(f"Leave blank for previous price: {last_price}€.\n")
                validated_price = validate_price(price_input, last_price)

                if validated_price:
                    break

            break

    broadband_data = [str(validated_date), str(validated_price)]
    calculated_broadband_data = calculate_data(broadband_data, worksheet)

    return calculated_broadband_data


def get_gas_data(worksheet):
    """
    Gets date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be date and price.
    The loops will repeatedly request data, until it is valid.
    """
    print("\nPlease enter gas data.")
    print("Data should be: date and price from last bill.")

    while True:

        today = date.today().strftime("%d.%m.%Y")
        last_date = SHEET.worksheet('gas').get_all_values()[-1][0]
        print("\nEnter the date. Leave blank to enter today's date.")
        date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")
        validated_date = validate_date(date_input, last_date)

        if validated_date:

            while True:

                last_price = SHEET.worksheet('gas').get_all_values()[-1][1]
                print("\nEnter the price, €.")
                price_input = input(f"Leave blank for previous price: {last_price}€.\n")
                validated_price = validate_price(price_input, last_price)

                if validated_price:
                    break

            break

    gas_data = [str(validated_date), str(validated_price)]
    calculated_gas_data = calculate_data(gas_data, worksheet)

    return calculated_gas_data

# Calculate function

def calculate_data(data, worksheet):
    """
    Calculation of the total utility consumption and the number of days
    between the last data and the entered one.
    Calculation of average utility consumption per day and cost per day.
    """
    print("\nCalculating...")
    last_data = SHEET.worksheet(worksheet).get_all_values()[-1]
    if worksheet == 'electricity':
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
    if worksheet == 'electricity':
        # Calculation of average electricity consumption per day since the last measurement
        consumption = diff_meter / diff_days_num
        consumption_rounded = round(consumption, 1)
        data.append(str(consumption_rounded))
        # Calculation of the average cost of electricity consumed per day since the last measurement
        cost = consumption * float(data[2])
        cost_rounded = round(cost, 2)
        data.append(str(cost_rounded))
    elif worksheet == 'broadband':
        # Calculation of average broadband price per day
        consumption = float(data[1]) / diff_days_num
        consumption_rounded = round(consumption, 2)
        data.append(str(consumption_rounded))
    else:
        # Calculation of average utility price per day
        consumption = float(last_data[1]) / diff_days_num
        consumption_rounded = round(consumption, 2)
        data.append(str(consumption_rounded))
    print("\nCalculation finished.")

    return data

# Validate functions

def validate_electricity_meter(value):
    """
    Recieves a date as a string. Inside the try,
    checks if it's not empty string, and then converts it to float.
    Raises ValueError if string can not be converted into float.
    Checks if it's not less than previous meter reading.
    """
    try:
        if value == '':
            raise ValueError(
                "electricity meter value cannot be empty"
            )

        new_electricity_meter_reading = float(value)
        last_electricity_meter_reading = float(SHEET.worksheet('electricity').get_all_values()[-1][1])

        if new_electricity_meter_reading < last_electricity_meter_reading:
            raise ValueError(
                f"new electricity meter value {new_electricity_meter_reading} cannot be less then previous {last_electricity_meter_reading}"
            )
        print("Electricity meter is valid.")

    except ValueError:
        print("Invalid data: please try again.")
        return False

    return new_electricity_meter_reading


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
            print(f"No date provided, entering last known price: {value}€.")
            return value

        float_value = float(value)

        if float_value == 0:
            print("Utility cannot be free, please try again.")
            return False
        elif float_value < 0:
            print("Price cannot be negative, please try again.")
            return False

        print(f"Price {float_value}€ is valid.")
        return float_value

    except ValueError:
        print("Invalid data, please try again.")
        return False


def validate_date(value, last_date):
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
                print(f"Entered date {value} cannot be the same day as last entered date {last_date}.")
                print("Come back tomorrow.\n")
                choose_utilitie()

            print(f"No date provided, entering today's date: {value}")
            return value

        date_value = datetime.strptime(value, date_format)
        last_date_value = datetime.strptime(last_date, date_format)
        today_value = datetime.strptime(today, date_format)

        if date_value == last_date_value:
            print(f"Entered date {value} cannot be the same day as last entered day {last_date}.")
            print("Try again or leave blank to enter today's date or exit if today is the last entered date.")
            return False

        if date_value < last_date_value:
            print(f"Entered date {value} cannot be before or equal to the last date {last_date}.")
            return False

        if date_value > today_value:
            print(f"Entered date {value} cannot be in the future. Today is {today}.")
            return False

        print("Date is valid.")
        return value

    except ValueError:
        print("Invalid data: please try again.")
        return False

# Update functions

def update_worksheet(data, worksheet):
    """
    Receives a list of data to be inserted into a worksheet
    and a string with the name of the worksheet.
    Update the worksheet with the data provided.
    """
    print(f"\nUpdating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.")
    edit_worksheet(worksheet)


def delete_last_row(worksheet):
    """
    Deleting the last row in the relevant worksheet.
    """
    while True:
        print(f"\nAre you sure you want to delete the last row in the {worksheet} worksheet?")
        print(f"Enter '1' to confirm deletion of the last row on the {worksheet} worksheet.")
        print("Enter '0' to cancel and go back.\n")
        confirm = input("Enter your choice:\n")
        if confirm == '1':
            worksheet_del_last = SHEET.worksheet(worksheet)
            worksheet_all_values = SHEET.worksheet(worksheet).get_all_values()
            count_rows_data = len(worksheet_all_values)
            if count_rows_data > 2:
                worksheet_del_last.delete_rows(count_rows_data)
                print(f"The last row on the {worksheet} worksheet has been removed.")
                edit_worksheet(worksheet)
            else:
                print("It is forbidden to delete the original information.")
                edit_worksheet(worksheet)
        elif confirm == '0':
            edit_worksheet(worksheet)
        else:
            print("\nCheck your choice.")

# Programm lunch

print("\nWelcome to v.1.6.8!\n")
print("This program is designed to account for utilities.")
print("You can select a utility service and then the action you want to perform")
print("or view the information.\n")
main()

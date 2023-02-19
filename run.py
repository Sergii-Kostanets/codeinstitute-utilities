from datetime import date
from datetime import datetime
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
    Run all program functions
    """
    while True:
        choose_utilitie()

# Menu functions

def choose_utilitie():
    """
    Calls the appropriate utility function based on the users selection.
    """
    utility = [
        ["1", "electricity"],
        ["2", "food"],
        ["3", "broadband"]
        ]
    while True:
        print(f"Enter '{utility[0][0]}' to update {utility[0][1]}")
        print(f"Enter '{utility[1][0]}' to update {utility[1][1]}")
        print(f"Enter '{utility[2][0]}' to update {utility[2][1]}")
        print()
        option = input("Enter your choice:\n")
        if option == utility[0][0]:
            edit_worksheet(utility[0][1])
        elif option == utility[1][0]:
            edit_worksheet(utility[1][1])
        elif option == utility[2][0]:
            edit_worksheet(utility[2][1])
        else:
            print("\nCheck your choice\n")


def edit_worksheet(worksheet):
    """
    Choice of the relevant worksheets for editing.
    """
    while True:
        print()
        print(f"Actions with {worksheet} worksheet.")
        print()
        print("Enter '1' to add one row.")
        print("Enter '2' to delete last row.")
        print("Enter '3' to delete all rows.")
        print("Enter '4' to add default data.")
        print("Enter '5' to check statistics.")
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
            else:
                print(f"Worksheet {worksheet} not found!")
                main()
        elif option == '2':
            delete_last_row(worksheet)
        elif option == '3':
            delete_all(worksheet)
        elif option == '4':
            add_default(worksheet)
        elif option == '5':
            statistics(worksheet)
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
        print("Enter '0' to go back.")
        print()
        option = input("Enter your choice:\n")
        if option == '1':
            statistics_average_all(worksheet)
        if option == '2':
            statistics_average_month(worksheet)
        elif option == '0':
            edit_worksheet(worksheet)

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


def statistics_average_month(worksheet):
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
        if days_sum >= 30:
            break
    days_exceeded = days_sum - 30
    costs_per_day.reverse()
    costs_sum = 0
    for days, cost_per_day in zip(days_list[0:i], costs_per_day[0:i]):
        costs_sum = costs_sum + (int(days) * float(cost_per_day))
    average = round((costs_sum / days_sum), 2)
    if days_exceeded > 0:
        costs_sum_month = average * (days_sum - days_exceeded)
    else:
        costs_sum_month = costs_sum
    print(f"Total costs for last month: {round(costs_sum_month, 2)}.")
    print(f"Average cost per day for last month: {average}.")

    statistics(worksheet)

# MERGE GET FUNCTIONS !!!

def get_electricity_data(worksheet):
    """
    Gets electricity, date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be meter reading, date and price.
    The loops will repeatedly request data, until it is valid.
    """
    print("\nPlease enter electricity data.")
    print("Data should be: meter reading, date and price per kWh.")

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

    except ValueError as error:
        print(f"Invalid data: {error}, please try again.")
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

        print(f"Price {float_value}€ is valid.")
        return float_value

    except ValueError as error:
        print(f"Invalid price: {error}, please try again.")
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

    except ValueError as error:
        print(f"Invalid data: {error}, please try again.")
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
    worksheet_del_last = SHEET.worksheet(worksheet)
    worksheet_all_values = SHEET.worksheet(worksheet).get_all_values()
    count_rows_data = len(worksheet_all_values)
    worksheet_del_last.delete_rows(count_rows_data)
    print(f"The last row on the {worksheet} worksheet has been removed.")
    edit_worksheet(worksheet)


def delete_all(worksheet):
    """
    Deleting all data in the relevant worksheet.
    """
    worksheet_del_all = SHEET.worksheet(worksheet)
    worksheet_all_values = SHEET.worksheet(worksheet).get_all_values()
    count_rows_data = len(worksheet_all_values)
    worksheet_del_all.delete_rows(1, count_rows_data)
    print(f"All rows on the {worksheet} worksheet have been removed.")
    edit_worksheet(worksheet)


def add_default(worksheet):
    """
    Adding default data in the relevant worksheet.
    """
    worksheet_add_default = SHEET.worksheet(worksheet)

    if worksheet == 'electricity':
        default_data = [
            ['date', 'meter', 'price, €', 'consumption, kWh', 'days', 'per day, kWh', 'per day, €'],
            ['10.01.2023', '23570.0', '0.42', '', '', '', ''],
            ['14.01.2023', '23603.8', '0.42', '33.8', '4', '8.4', '3.55'],
            ['17.01.2023', '23660.0', '0.42', '14.6', '1', '14.6', '6.13'],
            ['18.01.2023', '23669.0', '0.42', '9.0', '1', '9.0', '3.78'],
            ['19.01.2023', '23690.0', '0.42', '21.0', '1', '21.0', '8.82'],
            ['23.01.2023', '23728.5', '0.42', '38.5', '4', '9.6', '4.04'],
            ['24.01.2023', '23740.0', '0.42', '11.5', '1', '11.5', '4.83'],
            ['31.01.2023', '23822.6', '0.42', '82.6', '7', '11.8', '4.96'],
            ['01.02.2023', '23835.6', '0.42', '13.0', '1', '13.0', '5.46'],
            ['09.02.2023', '23922.2', '0.42', '86.6', '8', '10.8', '4.55'],
            ['16.02.2023', '23996.0', '0.42', '73.8', '7', '10.5', '4.43']
            ]
    elif worksheet == 'food':
        default_data = [
            ['data', 'price, €', 'days', 'per day, €'],
            ['01.02.2023', '20.47', '', ''],
            ['03.02.2023', '43.19', '2', '10.23'],
            ['06.02.2023', '13.15', '3', '14.4'],
            ['09.02.2023', '35.63', '3', '4.38']
            ]
    elif worksheet == 'broadband':
        default_data = [
            ['date', 'price, €', 'days', 'per day, €'],
            ['15.10.2022', '', '', ''],
            ['30.11.2022', '61.84', '46', '1.34'],
            ['21.12.2022', '64.14', '21', '2.94'],
            ['17.01.2023', '50.12', '27', '2.38'],
            ['04.02.2023', '33.54', '18', '2.78']
            ]
    else:
        print("Worksheet not found.\n")
        main()

    worksheet_add_default.append_rows(default_data)
    print(f"Default rows on the {worksheet} worksheet have been appended.")
    edit_worksheet(worksheet)

# Programm lunch

print("\nWelcome to v.1.4.6!\n")
main()

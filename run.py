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


def calculate_electricity_data(data):
    """
    Calculation of the total electricity consumption and the number of days
    between the last data and the entered ones.
    Calculation of average electricity consumption per day and cost per day.
    """
    last_data = SHEET.worksheet('electricity').get_all_values()[-1]
    # Calculation of how much electricity has been spent since the last measurement
    diff_meter = float(data[0]) - float(last_data[0])
    diff_meter_rounded = round(diff_meter, 1)
    data.append(str(diff_meter_rounded))
    # Calculation of the number of days since the last measurement
    date_format = "%d.%m.%Y"
    prev_date = datetime.strptime(last_data[1], date_format)
    new_date = datetime.strptime(data[1], date_format)
    diff_days = new_date - prev_date
    diff_days_num = diff_days.days
    data.append(str(diff_days_num))
    # Calculation of average electricity consumption per day since the last measurement
    consumption = diff_meter / diff_days_num
    consumption_rounded = round(consumption, 1)
    data.append(str(consumption_rounded))
    # Calculation of the average cost of electricity consumed per day since the last measurement
    cost = consumption * float(data[2])
    cost_rounded = round(cost, 2)
    data.append(str(cost_rounded))

    return data


def get_electricity_data():
    """
    Gets electricity, date and price input from the user.
    Run a while loops to collect a valid data from the user
    via the terminal, which must be meter reading, date and price.
    The loops will repeatedly request data, until it is valid.
    """
    while True:
        print("\nPlease enter electricity data.")
        print("Data should be: meter reading, date and price per kWh.\n")

        last_electricity_meter_reading = SHEET.worksheet('electricity').get_all_values()[-1][0]
        print("Enter meter reading.")
        electricity_meter_reading = input(f"Previous value: {last_electricity_meter_reading}.\n")

        validated_electricity_meter = validate_electricity_meter(electricity_meter_reading)
        if validated_electricity_meter:

            while True:
                today = date.today().strftime("%d.%m.%Y")
                last_date = SHEET.worksheet('electricity').get_all_values()[-1][1]
                print("\nEnter the date. Leave blank to enter today's date.")
                date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")

                validated_date = validate_date(date_input)
                if validated_date:

                    while True:
                        last_price = SHEET.worksheet('electricity').get_all_values()[-1][2]
                        print("\nEnter the price, €.")
                        price_input = input(f"Leave blank for previous price: {last_price}€.\n")

                        validated_price = validate_price(price_input)
                        if validated_price:
                            break

                    break

            break

    electricity_data = [str(validated_electricity_meter), str(validated_date), str(validated_price)]
    calculated_electricity_data = calculate_electricity_data(electricity_data)

    return calculated_electricity_data


def validate_price(value):
    """
    Recieves a price as a string.
    Checks if it's empty string, to return previous price.
    Inside the try, converts string value into float.
    Raises ValueError if strings can not be converted into float.
    Checks if it's not a zero.
    """
    last_price = SHEET.worksheet('electricity').get_all_values()[-1][2]

    try:
        if value == '':
            value = last_price
            print(f"No date provided, entering last known price: {value}€.")
            return value

        float_value = float(value)

        if float_value == 0:
            print("Electricity cannot be free, please try again.")
            return False

        print(f"Price {float_value}€ is valid.")
        return float_value

    except ValueError as error:
        print(f"Invalid price: {error}, please try again.")
        return False


def validate_date(value):
    """
    Recieves a date as a string.
    Checks if it's empty string, to return today's date.
    Inside the try, converts string value into date.
    Raises ValueError if strings can not be converted into date.
    Checks if it's not before last date and after today's date.
    """
    today = date.today().strftime("%d.%m.%Y")
    last_date = SHEET.worksheet('electricity').get_all_values()[-1][1]
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
        last_electricity_meter_reading = float(SHEET.worksheet('electricity').get_all_values()[-1][0])

        if new_electricity_meter_reading < last_electricity_meter_reading:
            raise ValueError(
                f"new electricity meter value {new_electricity_meter_reading} cannot be less then previous {last_electricity_meter_reading}"
            )
        print("Electricity meter is valid.")

    except ValueError as error:
        print(f"Invalid data: {error}, please try again.")
        return False

    return new_electricity_meter_reading


def update_worksheet_electricity(data):
    """
    Receives a list of data to be inserted into an electricity worksheet.
    Update the electricity worksheet with the data provided.
    """
    print(f"\nUpdating electricity worksheet...\n")
    worksheet_to_update = SHEET.worksheet('electricity')
    worksheet_to_update.append_row(data)
    print(f"Electricity worksheet updated successfully.\n")


def edit_worksheet(worksheet):
    """
    Choice of the relevant worksheets for editing.
    """
    while True:
        print()
        print(f"Editing mode of {worksheet} worksheet.")
        print()
        print("Enter 'delete' to delete last row")
        print("Enter 'delete all' to delete all data")
        print("Enter 'add' to add defaul data")
        print()
        option = input("Enter your choice:\n")
        if option == "delete":
            delete_last_row(worksheet)
            break
        elif option == "delete all":
            delete_all(worksheet)
            break
        elif option == "add":
            add_default(worksheet)
            break
        else:
            print("\nCheck your choice")


def delete_last_row(worksheet):
    """
    Deleting the last row in the relevant worksheet.
    """
    worksheet_del_last = SHEET.worksheet(worksheet)
    worksheet_all_values = SHEET.worksheet(worksheet).get_all_values()
    count_rows_data = len(worksheet_all_values)
    worksheet_del_last.delete_rows(count_rows_data)
    print(f"The last row on the {worksheet} worksheet has been removed.\n")
    main()


def delete_all(worksheet):
    """
    Deleting all data in the relevant worksheet.
    """
    worksheet_del_all = SHEET.worksheet(worksheet)
    worksheet_all_values = SHEET.worksheet(worksheet).get_all_values()
    count_rows_data = len(worksheet_all_values)
    worksheet_del_all.delete_rows(1, count_rows_data)
    print(f"All rows on the {worksheet} worksheet have been removed.\n")
    main()


def add_default(worksheet):
    """
    Adding default data in the relevant worksheet.
    """
    worksheet_add_default = SHEET.worksheet(worksheet)

    default_data_electricity = [
        ['meter', 'date', 'price, €', 'consumption, kWh', 'days', 'per day, kWh', 'per day, €'],
        ['23570.0', '10.01.2023', '0.42', '', '', '', ''],
        ['23603.8', '14.01.2023', '0.42', '33.8', '4', '8.4', '3.55'],
        ['23660.0', '17.01.2023', '0.42', '14.6', '1', '14.6', '6.13'],
        ['23669.0', '18.01.2023', '0.42', '9.0', '1', '9.0', '3.78'],
        ['23690.0', '19.01.2023', '0.42', '21.0', '1', '21.0', '8.82'],
        ['23728.5', '23.01.2023', '0.42', '38.5', '4', '9.6', '4.04'],
        ['23740.0', '24.01.2023', '0.42', '11.5', '1', '11.5', '4.83'],
        ['23822.6', '31.01.2023', '0.42', '82.6', '7', '11.8', '4.96'],
        ['23835.6', '01.02.2023', '0.42', '13.0', '1', '13.0', '5.46'],
        ['23922.2', '09.02.2023', '0.42', '86.6', '8', '10.8', '4.55'],
        ['23996.0', '16.02.2023', '0.42', '73.8', '7', '10.5', '4.43']
        ]

    worksheet_add_default.append_rows(default_data_electricity)
    print(f"Default rows on the {worksheet} worksheet have been appended.\n")
    main()


def choose_utilitie():
    """
    Calls the appropriate utility function based on the users selection.
    """
    while True:
        print("Enter 1 to update electricity")
        print("Enter 2 to update food")
        print("Enter 3 to update broadband")
        print()
        print("Enter 11 to edit electricity")
        print("Enter 22 to edit food")
        print("Enter 33 to edit broadband")
        print()
        option = input("Enter your choice:\n")
        if option == "1":
            data = get_electricity_data()
            update_worksheet_electricity(data)
            break
        elif option == "2":
            get_food_data()
            break
        elif option == "3":
            get_broadband_data()
            break
        elif option == "11":
            worksheet = 'electricity'
            edit_worksheet(worksheet)
            break
        elif option == "22":
            worksheet = 'food'
            edit_worksheet(worksheet)
            break
        elif option == "33":
            worksheet = 'broadband'
            edit_worksheet(worksheet)
            break
        else:
            print("\nCheck your choice")


def main():
    """
    Run all program functions
    """
    while True:
        choose_utilitie()


print("\nWelcome!\n")
main()

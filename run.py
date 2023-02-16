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
    """
    last_data = SHEET.worksheet('electricity').get_all_values()[-1]
    print(last_data) # DEL IT
    print(data) # DEL IT
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
    print(data[2]) # DEL IT
    cost = consumption * float(data[2])
    cost_rounded = round(cost, 2)
    data.append(str(cost_rounded))

    print(data) # DELIT

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
                print("Enter the date. Leave blank to enter today's date.")
                date_input = input(f"Last entered date is: {last_date}. Today is: {today}.\n")

                validated_date = validate_date(date_input)
                if validated_date:

                    while True:
                        last_price = SHEET.worksheet('electricity').get_all_values()[-1][2]
                        print("Enter the price, €.")
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
            print("Try again or leave blanc to enter today's date or exit if today is the last entered date.")
            return False

        if date_value < last_date_value:
            print(f"Entered date {value} cannot be before last date {last_date}.")
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
    """
    print(f"\nUpdating electricity worksheet...\n")
    worksheet_to_update = SHEET.worksheet('electricity')
    worksheet_to_update.append_row(data)
    print(f"Electricity worksheet updated successfully.\n")


def choose_utilitie():
    """
    """
    while True:
        print("Enter 1 to update electricity\nEnter 2 to update food\nEnter 3 to update broadband\n")
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
        else:
            print("\nCheck your choice")


def main():
    """
    """
    print("\nWelcome!\n")
    while True:
        choose_utilitie()


main()
# calculate_electricity_data(["24000.3", "16.02.2023", "0.42"])

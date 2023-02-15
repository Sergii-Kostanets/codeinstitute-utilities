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


# electricity = SHEET.worksheet('electricity')

# data = electricity.get_all_values()

# print(data)

def get_electricity_data():
    """
    """
    while True:
        print("\nPlease enter electricity data.")
        print("Data should be: meter reading, date and price per kWh.\n")

        last_electricity_meter_reading = SHEET.worksheet('electricity').get_all_values()[-1][0]
        electricity_meter_reading = input(f"Enter meter reading.\nPrevious value: {last_electricity_meter_reading}\n")

        validated_electricity_meter = validate_electricity_meter(electricity_meter_reading)
        if validated_electricity_meter:

            while True:
                today = date.today().strftime("%d.%m.%Y")
                last_date = SHEET.worksheet('electricity').get_all_values()[-1][1]
                date_input = input(f"Enter the date (optional, leave blank to enter today's date).\nLast entered date is: {last_date}. Today is: {today}.\n")

                validated_date = validate_date(date_input)
                if validated_date:

                    while True:
                        last_price = SHEET.worksheet('electricity').get_all_values()[-1][2]
                        price_input = input(f"Enter the price, € (optional, leave blank to enter the previous price: {last_price}€).\n")

                        validated_price = validate_price(price_input)
                        if validated_price:
                            break

                    break

            break

    electricity_data = (str(validated_electricity_meter), str(validated_date), str(validated_price))

    return electricity_data


def validate_price(value):
    """
    """
    last_price = SHEET.worksheet('electricity').get_all_values()[-1][2]

    try:
        if value == '':
            value = last_price
            print(f"No date provided, entering last known price: {value}€.")
            return value

        value = float(value)
        print(f"Price {value}€ is valid.")
        return value

    except ValueError as error:
        print(f"Invalid price: {error}, please try again.")
        return False


def validate_date(value):
    """
    """
    today = date.today().strftime("%d.%m.%Y")
    last_date = SHEET.worksheet('electricity').get_all_values()[-1][1]
    date_format = "%d.%m.%Y"
    try:
        if value == '':
            value = date.today().strftime(date_format)
            print(f"No date provided, entering today's date: {value}")
            return value

        date_value = datetime.strptime(value, date_format)
        last_date_value = datetime.strptime(last_date, date_format)
        today_value = datetime.strptime(today, date_format)

        if date_value < last_date_value:
            print(f"Entered date {value} can not be before last date {last_date}.")
            return False

        if date_value > today_value:
            print(f"Entered date {value} can not be in the future. Today is {today}.")
            return False

        print("Date is valid.")
        return value

    except ValueError as error:
        print(f"Invalid data: {error}, please try again.")
        return False


def validate_electricity_meter(value):
    """
    """
    try:
        if value == '':
            raise ValueError(
                "electricity meter value can not be empty"
            )
        new_electricity_meter_reading = float(value)
        last_electricity_meter_reading = float(SHEET.worksheet('electricity').get_all_values()[-1][0])
        if new_electricity_meter_reading < last_electricity_meter_reading:
            raise ValueError(
                f"new electricity meter value {new_electricity_meter_reading} can not be less then previous {last_electricity_meter_reading}"
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
        print("\nEnter 1 to update electricity\nEnter 2 to update food\nEnter 3 to update broadband\n")
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
    print("\nWelcome!")
    choose_utilitie()


main()
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
    # while True:
    print("\nPlease enter electricity data.")
    print("Data should be meter reading, data and price per kWh.")
    print("")
    electricity_meter_reading = input("Meter reading:\nExample: 30120.5\n")
    date = input("Date (optional, leave blank to enter today's date):\nExample: 15.02.2023\n")
    price = input("Price (optional, leave blank to enter the previous price):\nExample: 0.42\n")
    electricity_data = (electricity_meter_reading, date, price)


        # data_str = input("Enter your data here:\n")

        # electricity_data = data_str.split(",")

        # if validate_data(electricity_data):
        #     print("Data is valid!")
        #     break

    return electricity_data


# def validate_data(values):
#     """
#     """
#     try:
#         [int(value) for value in values]
#         if len(values) != 6:
#             raise ValueError(
#                 f"Exactly 6 values required, you provided {len(values)}"
#             )
#     except ValueError as e:
#         print(f"Invalid data: {e}, please try again.\n")
#         return False

#     return True


def update_worksheet_electricity(data):
    """
    """
    print(f"Updating electricity worksheet...\n")
    worksheet_to_update = SHEET.worksheet('electricity')
    worksheet_to_update.append_row(data)
    print(f"Electricity worksheet updated successfully.\n")


def choose_utilitie():
    """
    """
    while True:
        print("\nPress 1 to update electricity\nPress 2 to update food\nPress 3 to update broadband\n")
        option = input("Enter your choice\n")
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
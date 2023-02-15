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
    print("Data should be meter reading, data and price per kWh, separated by commas.")
    print("Example: 30120.5,15.02.2023,0.42\n")

    data_str = input("Enter your data here:\n")

    electricity_data = data_str.split(",")

        # if validate_data(electricity_data):
        #     print("Data is valid!")
        #     break

    return electricity_data


def update_worksheet_electricity(data):
    """
    """
    print(f"Updating electricity worksheet...\n")
    worksheet_to_update = SHEET.worksheet('electricity')
    worksheet_to_update.append_row(data)
    print(f"Electricity worksheet updated successfully.\n")


def main():
    """
    """
    data = get_electricity_data()
    update_worksheet_electricity(data)


main()
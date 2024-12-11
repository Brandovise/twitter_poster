import os
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ExcelData:
    def __init__(self, sheet_id, range_name):
        """
        Initializes the ExcelData class by reading data from a Google Sheet.
        
        Args:
            sheet_id (str): The Google Sheets ID.
            range_name (str): The range of cells to read from the sheet.
        """
        
        self.json_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        if not self.json_file:
            raise EnvironmentError("Environment variable 'GOOGLE_SERVICE_ACCOUNT_JSON' is not set.")
        self.read_google_sheet(sheet_id, range_name)

    def load_excel_data(self, excel_file_path):
        """
        Loads data from an Excel file and sets each column as an attribute of the class.

        Args:
            excel_file_path (str): Path to the Excel file.
        """
        self.data = pd.read_excel(excel_file_path)
        for column in self.data.columns:
            setattr(self, column, self.data[column].tolist())

    def get_the_row(self, row_number):
        """
        Retrieves a specific row by its index.

        Args:
            row_number (int): The index of the row to retrieve.

        Returns:
            dict: A dictionary representing the row's data.

        Raises:
            ValueError: If the data is not loaded or not in the correct format.
        """
        if not hasattr(self, 'data') or not isinstance(self.data, list):
            raise ValueError("Data is not loaded or is not in the correct format.")
        return self.data[row_number]

    def read_google_sheet(self, spreadsheet_id, range_name):
        """
        Reads data from a Google Sheet and stores it as a list of dictionaries.

        Args:
            spreadsheet_id (str): The Google Sheets ID.
            range_name (str): The range of cells to read from the sheet.

        Raises:
            ValueError: If no data is found in the specified range.
            HttpError: If an error occurs during the API call.
        """
        creds = Credentials.from_service_account_file(self.json_file)
        service = build('sheets', 'v4', credentials=creds)

        try:
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])

            if not values:
                raise ValueError("No data found in the specified range.")

            headers = values[0]
            self.data = [dict(zip(headers, row)) for row in values[1:]]
        except HttpError as error:
            print(f"An error occurred: {error}")

    def append_values(self, spreadsheet_id, range_name, value_input_option, values):
        """
        Appends values to a Google Sheet.

        Args:
            spreadsheet_id (str): The Google Sheets ID.
            range_name (str): The range of cells to append data to.
            value_input_option (str): How the input data should be interpreted (e.g., 'RAW', 'USER_ENTERED').
            values (list): The data to append as a list of lists.

        Returns:
            dict: The API response object, or None if an error occurs.

        Raises:
            HttpError: If an error occurs during the API call.
        """
        creds = Credentials.from_service_account_file(self.json_file)

        try:
            service = build("sheets", "v4", credentials=creds)
            body = {"values": values}

            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption=value_input_option,
                    body=body,
                )
                .execute()
            )

            updated_cells = result.get('updates', {}).get('updatedCells', 0)
            print(f"{updated_cells} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

# Usage example
if __name__ == "__main__":
    # Ensure the environment variable is set for the service account JSON file
    if not os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'):
        raise EnvironmentError("Please set the 'GOOGLE_SERVICE_ACCOUNT_JSON' environment variable.")

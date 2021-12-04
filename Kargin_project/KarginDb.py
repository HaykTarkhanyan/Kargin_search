import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime

import logging
logging.basicConfig(format='%(asctime)s - %(message)s')

# https://docs.google.com/spreadsheets/d/1OGGS1aMO1WubVaj2cGJHv29AaWvOxxc3ijTNvv4TC5I/edit?usp=sharing

#connecting to google sheets

class SheetsDb:
    def __init__(self, sheet_name="կարգին դատաբազա", creds_path='../sheets_creds.json'):
        self.creds_path = creds_path
        self.sheet_name = "կարգին դատաբազա"

        self.db = None
        self.df = None

    def connect(self):
        logging.debug('connecting to google sheets db')
        try:
            scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets', \
                     "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, scope)
            client = gspread.authorize(creds)

            self.dbs = [client.open(self.sheet_name).get_worksheet(0)]
            logging.debug('Successfully connected')
        except Exception as e:
            error_message = f'Error connecting to {self.sheet_name}: {e}'
            logging.critical(error_message)
            raise ValueError(error_message)

    def write(self, list_to_insert, worksheet_index):
        logging.debug(f'Trying to write {list_to_insert} to {worksheet_index}')
        try:
            self.dbs[worksheet_index].insert_row(list_to_insert, 2)
        except Exception as e:
            error_message = f'Error inserting {list_to_insert} to {worksheet_index}: {e}'
            logging.critical(error_message)
            raise ValueError(error_message)

    def read(self, worksheet_index): 
        logging.debug(f'Trying to read {worksheet_index} from {self.sheets_name}')
        try:
            results = self.dbs[worksheet_index].get_all_records()
            self.df = pd.DataFrame(results) 
            return self.df
        except Exception as e: 
            error_message = f'Error reading {worksheet_index} from {self.sheets}: {e}'
            logging.critical(error_message)
            raise ValueError(error_message)


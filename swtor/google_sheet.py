from __future__ import print_function
import pickle
import os.path
import gspread
import datetime

class GoogleSheet:
    _scopes = ['https://www.googleapis.com/auth/spreadsheets']
    _gtn_prices_spreadsheet_id = '15wgfiy8trtWIt0dgI_S3hSBvpCVAT08cZCujF0Mp2No'
    _decorations_sheet_name = 'Decorations'

    def __init__(self):
        gc = gspread.service_account(filename = 'service_account.json')
        self.__gtn_prices_spreadsheet = gc.open_by_key(GoogleSheet._gtn_prices_spreadsheet_id)
        self.__decorations_worksheet = self.__gtn_prices_spreadsheet.worksheet(GoogleSheet._decorations_sheet_name)
        self.all_values = self.__decorations_worksheet.get_all_records()

    def __get_cell_indices(self, contents):
        try:
            cell_with_contents = self.__decorations_worksheet.find(contents)
        except:
            return None

        return (cell_with_contents.row, cell_with_contents.col)

    def _add_new_prices_column(self):
        item_cell_indices = self.__get_cell_indices('Item')
        item_column_index = item_cell_indices[1]
        self.__gtn_prices_spreadsheet.batch_update({
            'requests': [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "COLUMNS",
                            "startIndex": item_column_index,
                            "endIndex": item_column_index + 1
                        },
                        "inheritFromBefore": True
                    }
                }
            ]
        })
        self.__decorations_worksheet.update_cell(item_cell_indices[0], item_column_index + 1, datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())
        return item_column_index + 1

    def __auto_size_column(self, column_index):
        self.__gtn_prices_spreadsheet.batch_update({
            "requests": [
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": 0,
                            "dimension": "COLUMNS",
                            "startIndex": column_index,
                            "endIndex": column_index + 1
                        }
                    }
                }
            ]
        })

    def add_new_item_prices(self, prices):
        price_column_index = self._add_new_prices_column()
        item_cell_indices = self.__get_cell_indices('Item')
        item_row_index = item_cell_indices[0]
        for item_name, price in prices.items():
            actual_item_indices = self.__get_cell_indices(item_name)
            price_scaled = price / 10e5 if price else 0
            if not actual_item_indices:
                 self.__decorations_worksheet.insert_row([item_name, price_scaled], item_row_index + 1)
            else:
                self.__decorations_worksheet.update_cell(actual_item_indices[0], price_column_index, price_scaled)

        self.__auto_size_column(price_column_index)

    def to_sqlite(self):
        from .sqlite_db import SqliteDb
        import datetime
        sqlite_db = SqliteDb()
        all_records = self.__decorations_worksheet.get_all_records()
        for record in all_records:
            item_name = record['Item']
            del record['Item']
            for date, price in record.items():
                if not price:
                    continue

                item_id = sqlite_db.upsert_item(item_name)
                date = f'{date}/20'
                sqlite_db.insert_price(item_id, price * 10e5, datetime.datetime.strptime(date, '%m/%d/%y').timestamp())


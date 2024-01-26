from .swtor_window import SwtorWindow
from .gtn_window import GtnWindow
from .inventory_window import InventoryWindow
from .options_window import OptionsWindow
from .cargo_hold_window import CargoHoldWindow
from .window import Window
from .window_not_found_error import WindowNotFoundError
from .crew_skills_window import CrewSkillsWindow
from ahk import AHK
import time
import swtor.global_data as global_data
from tkinter import Tk
from .sqlite_db import SqliteDb
from tabulate import tabulate
import datetime
import pandas as pd
import logging

class SwtorGame:
    def __init__(self, logger = None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

        self.swtor_window = SwtorWindow(logger)
        self.options_window = OptionsWindow(logger)
        self.inventory_window = InventoryWindow(logger)
        self.gtn_window = GtnWindow(logger)
        self.cargo_hold_window = CargoHoldWindow(logger)
        self.__sqlite_db = SqliteDb(logger)
        self.crew_skills_window = CrewSkillsWindow(logger)

    def __close_all_windows(self):
        windows_closed = 0
        while windows_closed < global_data.max_windows_to_close:
            if self.options_window.visible:
                self.swtor_window.send('{Escape}')
                return

            self.swtor_window.send('{Escape}')
            windows_closed += 1

    def __open_gtn_and_inventory_windows(self):
        self.__close_all_windows()
        self.swtor_window.right_click(self.swtor_window.screen_center)
        while not self.gtn_window.visible or not self.inventory_window.visible:
            time.sleep(0.01)

    def __price_is_current_in_db(self, item_name, time_to_check):
        most_recent_price_timestamp = self.__sqlite_db.get_most_recent_price_timestamp(item_name)
        if most_recent_price_timestamp and time_to_check - most_recent_price_timestamp < 3600:
            return True

        return False

    def __check_inventory_gtn_lowest_price(self, item_name, current_time):
        if self.__price_is_current_in_db(item_name, current_time):
            self.__print_item_prices(item_name)
            return

        self.gtn_window.search()
        time.sleep(1)
        if not self.gtn_window.is_sorted_ascending:
            self.gtn_window.sort_by_unit_price_ascending()
            self.gtn_window.is_sorted_ascending = True

        item_price = self.gtn_window.lowest_price(item_name)
        self.save_price_to_db(item_name, item_price, current_time)
        self.__print_item_prices(item_name)

    def check_inventory_gtn_lowest_price(self):
        self.gtn_window.is_sorted_ascending = False
        self.__iterate_slot_loctions(self.__check_inventory_gtn_lowest_price)

    def __check_inventory_gtn(self, item_name, current_time):
        if self.__price_is_current_in_db(item_name, current_time):
            self.logger.debug('Skipping search because prices are recent')
            self.__print_item_prices(item_name)
            return

        self.gtn_window.search()
        time.sleep(1)
        if not self.gtn_window.is_sorted_ascending:
            self.gtn_window.sort_by_unit_price_ascending()
            self.gtn_window.is_sorted_ascending = True

        results = self.gtn_window.results(item_name)
        self.logger.debug(f'Found {len(results) if results is not None else 0} results for {item_name}')
        self.save_results_to_db(results, current_time)
        self.__print_item_prices(item_name)

    def check_inventory_gtn(self):
        self.gtn_window.is_sorted_ascending = False
        self.__iterate_slot_loctions(self.__check_inventory_gtn)

    def _timestamp_to_mm_dd(self, t):
        return datetime.datetime.fromtimestamp(t).strftime('%m/%d')

    def __iterate_slot_loctions(self, func):
        self.__open_gtn_and_inventory_windows()
        self.logger.debug(f'GTN window location is {self.gtn_window.location}')
        self.logger.debug(f'Inventory window location is {self.inventory_window.location}')
        slot_locations = self.inventory_window.slot_locations
        self.logger.debug(f'Found {len(slot_locations)} slot locations at positions {slot_locations}')
        current_time = int(time.time())
        self.logger.debug(f'Current timestamp is {current_time} ({self._timestamp_to_mm_dd(current_time)})')
        for slot_location_index, slot_location in enumerate(slot_locations):
            self.swtor_window.shift_click(slot_location)
            item_name = self.gtn_window.searched_item_name
            self.logger.debug(f'Slot {slot_location_index + 1} of {len(slot_locations)}: {item_name}')
            func(item_name, current_time)

    def __print_results(self, results, time_stamp):
        table_headings = ['Item Name', 'Date', 'Unit Price']
        table_values = []
        for result in results:
            result_unit_price = result.unit_price / 10e5 if result.unit_price else None
            result_date = datetime.datetime.fromtimestamp(time_stamp).strftime('%m/%d')
            table_values.append([result.name, result_date, result_unit_price])

        print(tabulate(table_values, table_headings, tablefmt = 'fancy_grid'))

    def __print_item_prices(self, item_name):
        prices = self.__sqlite_db.get_prices_by_item_name(item_name)
        prices_df = pd.DataFrame.from_records(prices, columns = ['price', 'time_stamp']).groupby('time_stamp', as_index = False).min().sort_values('time_stamp', ascending = False)
        table_headings = ['Item Name']
        table_values = [item_name]
        table_headings.extend(map(self._timestamp_to_mm_dd, prices_df._get_column_array(0)))
        table_values.extend(map(lambda x: x / 10e5 if x else None, prices_df._get_column_array(1)))
        print(tabulate([table_headings, table_values], tablefmt = 'fancy_grid'))

    def save_price_to_db(self, item_name, price, time_stamp):
        item_id = self.__sqlite_db.upsert_item(item_name)
        self.__sqlite_db.insert_price(item_id, price, time_stamp)

    def save_results_to_db(self, results, time_stamp):
        if not results:
            return

        for result in results:
            self.save_price_to_db(result.name, result.unit_price, time_stamp)

    def transfer_inventory_to_cargo_hold(self):
        # Assume Cargo Hold window and Inventory window are
        # already open, with Cargo Hold bay already selected
        while not self.cargo_hold_window.visible or not self.inventory_window.visible:
            time.sleep(0.1)

        inventory_slot_locations = self.inventory_window.slot_locations
        for slot_location in inventory_slot_locations:
            self.swtor_window.right_click(slot_location, mouse_speed = 0)

    def transfer_cargo_hold_to_inventory(self):
        # Assume Cargo Hold window and Inventory window are
        # already open, with Cargo Hold bay already selected
        while not self.cargo_hold_window.visible or not self.inventory_window.visible:
            time.sleep(0.1)

        cargo_hold_slot_locations = self.cargo_hold_window.slot_locations
        for slot_location in cargo_hold_slot_locations:
            self.swtor_window.right_click(slot_location, mouse_speed = 0)

    def ocr_on_gtn_window_first_price(self):
        self.gtn_window.save_first_item_price_image()

    def ocr_on_gtn_window_all_prices_on_page(self):
        self.gtn_window.save_all_item_price_images_on_page_raw()

    def ocr_on_gtn_window_all_prices_on_page_single_image(self):
        self.gtn_window.save_all_item_price_images_on_page_raw_single_image()

    def open_crew_skills_window(self):
        self.__close_all_windows()
        self.swtor_window.send(CrewSkillsWindow.hotkey)
        while not self.crew_skills_window.visible:
            time.sleep(0.01)

        print(self.crew_skills_window.location)